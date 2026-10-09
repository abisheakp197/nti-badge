# NTI Modes

The nti-badge codebase runs in three modes. Same code. Different behavior.
Choose by setting `NTI_MODE` in your environment.

## Standalone (default)

- No federation. No hub. Private node.
- Badges work. Certificates verify. Registry endpoint works.
- The `/api/federation` endpoint returns `"enabled": false`.
- Best for: private projects, enterprises that can't federate, local development.

## Federated

- Same as standalone, PLUS:
- The node announces itself to hubs listed in `NTI_HUB_URLS`.
- Hubs can pull this node's public index.
- `/api/federation` lists which hubs this node publishes to.
- Best for: open-source projects that want public proof of quality.

## Hub

- Same as federated, PLUS:
- This node also aggregates indexes from other nodes.
- Exposes `/api/hub/register`, `/api/hub/nodes`, `/api/hub/index`, `/api/hub/leaderboard`.
- Other hubs can register with this hub (hub-of-hubs mesh).
- Best for: NTI Foundation reference hub, org-level internal hubs.

## Database Options

Bring your own DB. Set ONE of:
- `KV_URL` — Redis-compatible URL
- `REDIS_URL` — Alias for KV_URL
- `UPSTASH_REDIS_REST_URL` + `UPSTASH_REDIS_REST_TOKEN` — REST API
- None → file-based local fallback (works anywhere)

## Switching Modes

Modes are determined at cold-start. To switch:
1. Update env var in Vercel (or your host)
2. Redeploy

Data persists across modes. Standalone → federated keeps all existing scores.

## Data Custody Reminder

In every mode, the node holds only:
- repo, score, cert_hash, timestamp, tier, signature_verified

The full certificate lives in the user's repository. The node cannot leak
data it never held.
