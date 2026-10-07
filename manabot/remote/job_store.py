"""Private S3 job control and least-privilege, expiring worker credentials.

Conditional create claims are permanent fences, not renewable leases. A timed-out
PUT may have succeeded; callers reconcile reads and never repeat provider create.
Only the worker's runtime prefix is writable with the delegated STS session.
"""

from dataclasses import dataclass
import json
import math
import time
from typing import Any, Protocol

from manabot.infra.artifacts import split_s3_uri

from .jobs import RemoteJobSpec


@dataclass(frozen=True)
class StoredValue:
    data: bytes
    etag: str


class JobStore(Protocol):
    def read(self, key: str) -> StoredValue | None: ...
    def create(self, key: str, data: bytes) -> bool: ...
    def replace(self, key: str, data: bytes, etag: str) -> bool: ...


class S3JobStore:
    def __init__(self, prefix: str) -> None:
        import boto3
        from botocore.config import Config

        self.bucket, self.prefix = split_s3_uri(prefix)
        # SDK responses are narrowed at this adapter. Bound every network call;
        # the independent guardian is not subject to these timeouts.
        self.client: Any = boto3.client("s3", config=Config(
            connect_timeout=5, read_timeout=10, retries={"max_attempts": 1},
        ))

    def _key(self, key: str) -> str:
        if key.startswith("/") or ".." in key.split("/"):
            raise ValueError("invalid job control key")
        return f"{self.prefix.rstrip('/')}/{key}"

    def read(self, key: str) -> StoredValue | None:
        from botocore.exceptions import ClientError

        try:
            response = self.client.get_object(Bucket=self.bucket, Key=self._key(key))
        except ClientError as error:
            if error.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                return None
            raise RuntimeError("job storage read unavailable") from None
        body = response["Body"]
        try:
            data = body.read(16 * 1024**2 + 1)
            if len(data) > 16 * 1024**2:
                raise ValueError("job control object exceeds limit")
            return StoredValue(data, str(response["ETag"]))
        finally:
            body.close()

    def _put(self, key: str, data: bytes, condition: dict[str, str]) -> bool:
        from botocore.exceptions import ClientError

        try:
            self.client.put_object(Bucket=self.bucket, Key=self._key(key), Body=data,
                                   ContentType="application/json", **condition)
            return True
        except ClientError as error:
            if error.response["ResponseMetadata"]["HTTPStatusCode"] == 412:
                return False
            raise RuntimeError("job storage write uncertain; reconcile by job ID") from None

    def create(self, key: str, data: bytes) -> bool:
        return self._put(key, data, {"IfNoneMatch": "*"})

    def replace(self, key: str, data: bytes, etag: str) -> bool:
        return self._put(key, data, {"IfMatch": etag})


def worker_credentials(spec: RemoteJobSpec) -> dict[str, str]:
    """Obtain an expiring session restricted to this job; never forward account keys.

    Requires STS GetFederationToken via the standard AWS chain (IAM user).
    Unsupported credential types fail before a provider claim or rental.
    """
    import boto3

    bucket, prefix = split_s3_uri(spec.prefix)
    arn = f"arn:aws:s3:::{bucket}/{prefix}"
    policy = {"Version": "2012-10-17", "Statement": [
        {"Effect": "Allow", "Action": ["s3:GetObject"],
         "Resource": [f"{arn}/spec.json", f"{arn}/cancel.json", f"{arn}/training.json"]},
        {"Effect": "Allow", "Action": ["s3:GetObject", "s3:GetObjectVersion", "s3:PutObject"],
         "Resource": [f"{arn}/runtime/*"]},
    ]}
    session = boto3.Session()
    try:
        result = session.client("sts").get_federation_token(
            Name=f"manabot-{spec.identity[:24]}",
            DurationSeconds=max(900, math.ceil(spec.deadline - time.time()) + 300),
            Policy=json.dumps(policy, separators=(",", ":")),
        )
        credentials = result["Credentials"]
        if credentials["Expiration"].timestamp() < spec.deadline:
            raise ValueError("worker credentials expire before billing deadline")
        return {
            "AWS_ACCESS_KEY_ID": str(credentials["AccessKeyId"]),
            "AWS_SECRET_ACCESS_KEY": str(credentials["SecretAccessKey"]),
            "AWS_SESSION_TOKEN": str(credentials["SessionToken"]),
            "AWS_DEFAULT_REGION": session.region_name or "us-west-2",
        }
    except Exception:
        raise RuntimeError("scoped STS credentials unavailable; no rental created") from None
