import ast
from html import escape
import json
from pathlib import Path
import subprocess

head='81100af355e60bd5ff7e5b314ba586c740396ab3'
base='a108ed3428a7f8c363a28c7df5dc71a4cd8d2719'
integrated='e052ac30a7eeca77f7af4365a9eed6b5b75a6b2b'

def excerpt(path: str, symbol: str, limit: int | None = None) -> str:
    raw=subprocess.check_output(['git','show',f'{head}:{path}'],text=True)
    node=next(n for n in ast.parse(raw).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==symbol)
    start=node.lineno; end=min(node.end_lineno,start+limit-1) if limit else node.end_lineno
    body='\n'.join(raw.splitlines()[start-1:end])
    if end < node.end_lineno: body += '\n# … remaining validation omitted from this excerpt'
    caption=f'{path} · {symbol} · {head[:8]} · lines {start}–{end}'
    return f'<figure><figcaption><a href="https://github.com/loopflowstudio/etude/blob/{head}/{path}#L{start}-L{end}">{escape(caption)}</a></figcaption><pre><code>{escape(body)}</code></pre></figure>'

proof_path=Path('experiments/data/etu123-remote-jobs/proof.json')
proof=json.loads(proof_path.read_text()) if proof_path.exists() else None
proof_text='Live proof is still running. Offline fixtures are not CUDA acceptance.' if proof is None else f'''The submitting client exited at update {proof['updates_at_client_exit']}. The same job finished {proof['final_updates']} updates on CUDA, with {proof['later_evaluations_after_client_exit']} later checkpoint evaluations starting after that exit. {proof['complete_arena_games']} arena games completed. All {proof['verified_bundle_files']} bundle files verified after deletion; {proof['admitted_raw_ema_policies']} raw/EMA policies passed ordinary admission. Inventory was empty. Both proof attempts cost ${proof['etu123_total_estimated_dollars']:.4f} estimated, inside the shared $3 reservation. This proves execution survival and evidence retrieval, not learning strength.'''
html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Remote jobs · PR 254</title><style>
:root{{color-scheme:light}}*{{box-sizing:border-box}}body{{margin:0;background:#faf9f6;color:#222a2b;font:17px/1.6 system-ui,sans-serif}}main{{max-width:1120px;margin:64px auto;padding:0 28px}}h1{{font-size:38px;line-height:1.15;font-weight:600;max-width:800px}}h2{{margin:68px 0 18px;font-size:28px;font-weight:550}}p{{max-width:850px}}a{{color:#195963;text-underline-offset:3px}}nav{{display:flex;flex-wrap:wrap;gap:20px;margin:28px 0}}.meta,figcaption{{font-size:13px;color:#566568}}.map{{display:grid;grid-template-columns:1.1fr 2fr 2fr;border-top:1px solid #c8cdca}}.map>div{{padding:16px 12px;border-bottom:1px solid #c8cdca}}.map .label{{font-weight:600}}figure{{margin:28px 0}}figcaption{{margin-bottom:9px}}pre{{background:#eff1ed;padding:22px;overflow:auto;font:14px/1.55 ui-monospace,SFMono-Regular,Consolas,monospace;border-left:2px solid #638889}}.terminal{{background:#e8eeec}}code{{tab-size:4}}details{{margin:24px 0}}summary{{cursor:pointer}}a:focus-visible,summary:focus-visible{{outline:3px solid #a25d24;outline-offset:4px}}@media(max-width:680px){{main{{margin:32px auto;padding:0 18px}}h1{{font-size:29px}}.map{{display:block}}.map>div{{padding:10px 0}}.map .label{{margin-top:16px;border:0}}pre{{font-size:12px;padding:14px}}}}@media print{{main{{margin:0;max-width:none}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}nav{{display:none}}figure{{break-inside:avoid}}}}
</style></head><body><main><p class="meta"><a href="https://github.com/loopflowstudio/etude/pull/254">PR #254</a> · Unmerged; Jack Heart’s review pending</p><h1>Close the laptop. Return to the same training job.</h1><p>Remote training previously needed a connected client to run evaluation, retrieve artifacts and delete the rental. A durable job now gives the rental that responsibility and lets another client reconnect by ID.</p><p class="meta">Base {base[:8]} · Implementation head {head[:8]} · PR253 shared APIs integrated at {integrated[:8]}. The full branch includes that unmerged dependency. This source includes the shared resource-admission and cancellation refactor at 8ecf6e45. The publication update changes review artifacts and working notes only; all implementation excerpts bind the source head above. Live proof source: {escape(proof['source'][:8] if proof else 'pending')}.</p>
<nav aria-label="Review sections"><a href="#submit">Submit and retry</a><a href="#disconnect">Disconnect and return</a><a href="#evidence">Retrieve evidence</a><a href="#limits">Failures and limits</a></nav>
<div class="map"><div class="label">When you submit or retry</div><div>The same ID retains its first plan and deadline. An uncertain create cannot rent a replacement.</div><div><a href="#submit">RemoteJobSpec binds intent; _provision fences provider creation in S3.</a></div><div class="label">When the laptop goes offline</div><div>The rental continues learning, evaluating checkpoints, uploading and shutting down.</div><div><a href="#disconnect">The provider starts the supervisor; RemoteJobRecord separates progress from freshness and evidence.</a></div><div class="label">When you return after deletion</div><div>You fetch a committed artifact generation and regenerate the notebook/HTML locally.</div><div><a href="#evidence">publish_snapshot commits verified bytes before publishing the manifest.</a></div><div class="label">When work must stop</div><div>Cancel requests remote finalization. Forced reconciliation can delete a failed setup; Ctrl-C only detaches.</div><div><a href="#limits">A durable cancellation mailbox and independent guardian preserve the distinction.</a></div></div>
<h2 id="submit">1. Submit once; reconcile uncertainty</h2><p>Illustrative public commands below use a previously compiled source-pinned plan. The observed paid proof calls the same prepare_job/submit_job API from its retained driver.</p><pre class="terminal">uv run --extra artifacts manabot deploy \\
  --plan .runs/remote-plan.json --job-id example-001 \\
  --monitoring .runs/monitoring.json
uv run --extra artifacts manabot deploy status --job-id example-001</pre>
{excerpt('manabot/remote/cli.py','deploy_command')}
{excerpt('manabot/remote/jobs.py','RemoteJobSpec')}
{excerpt('manabot/remote/job_client.py','_provision')}
{excerpt('manabot/remote/jobs.py','Resource')}
<p>Client admission and remote execution use the same Resource.validate_for contract to check job identity, price and hardware. The supervisor does not import the submission client.</p>
<p>The create claim is permanent. A crash between claiming and issuing the request can leave the job ambiguous; no lease timeout silently creates another rental. Reconciliation is deliberately conservative.</p>
<h2 id="disconnect">2. Remote ownership survives the client</h2><p>{escape(proof_text)}</p>
{excerpt('manabot/remote/jobs.py','RemoteJobRecord')}
{excerpt('manabot/remote/supervisor.py','main')}
<p>Provider startup runs pinned-source setup before supervisor acceptance. The separate shell guardian starts first and keeps the original absolute deadline even if Python or S3 fails. A stale heartbeat never means the learner completed.</p>
<h2 id="evidence">3. Fetch after the rental is gone</h2><p>Fresh clients used <code>deploy fetch</code> after deletion; the report reuses the existing create-once notebook and experiment dashboard. TrainingRun and VerifyStore still own learning. Bundle owns paths and hashes.</p>
<p class="meta">Retained CLI transcript from the earlier deploy-only review pass at b4e861e4, after provider deletion. It was not rerun at the source head above and incurred no rental.</p><pre class="terminal">uv run --extra artifacts manabot deploy fetch --job-id etu123-disconnect-001 \\
  --out .runs/etu123-disconnect/cli-returned
.runs/etu123-disconnect/cli-returned/generation-000008

uv run --extra artifacts --extra notebook manabot deploy report \\
  --evidence .runs/etu123-disconnect/cli-returned/generation-000008 \\
  --out .runs/etu123-disconnect/cli-report
.runs/etu123-disconnect/cli-report/comparison.html</pre>
{excerpt('manabot/remote/snapshots.py','publish_snapshot')}
<p>SQLite’s online backup supplies one consistent database cut. Its run JSON is derived from that same backup; committed artifacts and closed evaluator attempts retain their original bytes. An upload failure leaves the previous committed generation readable.</p>
<h2 id="limits">4. Cancellation, evidence gaps and the review boundary</h2>
{excerpt('manabot/remote/job_client.py','cancel_job')}
<p>The first live attempt reached acceptance but failed before learner launch because S3 returns 403 for a missing key to the restricted worker. Submission now creates the empty mailbox first. Its setup artifacts and cost remain retained; permissions were not widened to bucket listing. The successful proof’s final status poll lagged at 139 updates while its database held 160. Current status reads VerifyStore; a regression covers that correction. Frozen evidence was not rewritten or rerun.</p><p>SSO role chaining currently admits less than one hour including reserves. Reconnection is observation and retrieval, not CUDA process recovery. Historical arbitrary SSH calibration callbacks fail before rental until those callers adopt a serializable workload. The only registered lifecycle namespace is <code>manabot deploy</code>; there is no compatibility alias. Publication is not merge approval.</p>
<details><summary>Verification and retained evidence</summary><p>Recorded before the shared-contract refactor: 94 local deployment and focused evaluator/storage checks passed (one CUDA-host skip). After the refactor at 8ecf6e45, 32 job/CLI checks passed, including rejection of the removed namespace; focused Ruff and diff checks also passed. These checks cover subprocess detachment, uncertain creation, concurrent intent, cancellation, deadline, upload failure, immutable snapshot verification and the guardian. CUDA-host checks are skipped locally; the retained live proof is separate. Full private evidence remains in <code>.runs/etu123-disconnect</code>. The durable contract is <a href="https://github.com/loopflowstudio/etude/blob/{head}/docs/remote-jobs.md">docs/remote-jobs.md</a>.</p></details>
<p class="meta">Rendering is unavailable in this headless handoff. The HTML and source excerpts are refreshed; retained desktop/narrow PNGs predate this refresh and do not verify its layout.</p>
<p class="meta">This walkthrough describes the pinned source above. No merge decision or scientific strength claim is made.</p></main></body></html>'''
Path('scratch/pr-review.html').write_text(html)
# Keep the focused code-capture page on the same source revision.
prefix = html.split('<main>', 1)[0] + '<main>'
evidence = html.split('<h2 id="evidence">', 1)[1].split('<h2 id="limits">', 1)[0]
Path('scratch/pr-review-code-capture.html').write_text(prefix + '<h2 id="evidence">' + evidence + '</main></body></html>')
print(f'scratch/pr-review.html pinned to {head}')
