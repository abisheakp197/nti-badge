# NTI Federation Flow

## Roles

| Role | Holds | Publishes To | Aggregates From |
|---|---|---|---|
| Standalone node | Own index | Nobody | Nobody |
| Federated node | Own index | Hubs | Nobody |
| Hub | Node registry + own index | Other hubs | All registered nodes |

## Flow: A node verifies a certificate

1. `nti-scanner` runs in a user's GitHub Action
2. It generates a Dilithium5-signed `nti-certificate.json`
3. It POSTs to the node's `/api/verify` (OIDC token + cert)
4. Node validates OIDC, validates cert signature, indexes hash + score
5. Node returns success
6. User commits `nti-certificate.json` to their repo (permanent proof)
7. Badge in README renders from node's `/api/badge`

## Flow: A federated node publishes to hubs

1. Cron (or manual POST) hits `/api/federation/publish`
2. Node POSTs its URL to each hub's `/api/hub/register`
3. Hub stores the node's URL + metadata (name, contact)
4. Hub does NOT receive the node's data
5. When someone queries `/api/hub/index`, the hub pulls each node's `/api/registry` on demand
6. Hub merges results and returns a unified view

## Flow: A hub-of-hubs

1. Hub A registers with Hub B via Hub B's `/api/hub/register` (kind=hub)
2. Hub B stores Hub A's URL
3. When Hub B aggregates, it pulls Hub A's `/api/hub/index`
4. Recursion continues (with depth limits)

## Data Sovereignty Invariants

1. Hubs NEVER store full certificates
2. Nodes NEVER give data to hubs (only URLs)
3. Aggregation is PULL-based (hub fetches from node)
4. Any node can leave at any time (just stop announcing)
5. Any hub can be replaced (nodes list multiple hubs)

## Federation Topology

- Star: many nodes → one hub
- Mesh: hubs ↔ hubs (hub-of-hubs)
- Hybrid: nodes in multiple hubs, hubs in multiple meshes
- Isolated: no federation (standalone)

Every topology uses the same codebase. The difference is configuration.
