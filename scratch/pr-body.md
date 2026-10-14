Complete the hosted-service part of the [Academy rename · PR #283](https://github.com/loopflowstudio/fantasia/pull/283): deployment commands now target `academy-play` and `fantasia-website` in `loopflow-studio`, with Cloudflare credentials in `fantasia/prd`.

The existing `etude.gg` and `etudefantasia` domains stay unchanged. DNS aliases and certificate-validation records point to the new apps. The shared Etude experiment project and its credentials remain intact; only the four Cloudflare entries were copied. Frozen S3 and wandb evidence keeps its existing identity.

The first new play deployment exposed a missing `manabot` package in the image. Include it and import the actual ASGI entrypoint during the build, using only the packaged runtime dependencies, so missing startup modules fail before deployment.

Checks: 14 website tests pass on Python 3.12; shell syntax and both Fly configs validate. Both images deployed successfully and all seven certificates are Ready. Direct HTTPS and WebSocket checks of the new app passed: play Mountain, cast Lightning Bolt, target the opponent, pass priority, verify three damage, then open the curated Lessons versus Allies matchup. Public traffic has been switched; final public-domain checks and old-app retirement are in progress. In-app browser unavailable, so no visual-browser verification is claimed.
