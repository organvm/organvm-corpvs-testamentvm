# ADR-010: Cross-Org Dispatch Architecture

## Status

Accepted

## Date

2026-02-11

## Context

The eight-organ system spans 8 GitHub organizations. GitHub Actions workflows in one org cannot natively trigger workflows in another org — `repository_dispatch` events are scoped to a single repository, and `workflow_dispatch` requires targeting a specific repo.

The system needed cross-org communication for:
1. **Promotion events**: When orchestration-start-here promotes a repo, the target org's workflows should react
2. **Distribution events**: When a new essay is detected in ORGAN-V, ORGAN-VII distribution workflows should fire
3. **Health checks**: The soak test in meta-organvm needs to query CI status across all 8 orgs
4. **Registry updates**: Changes to repo-registry.json should trigger validation across the system

## Decision

### Architecture

1. **Central dispatcher**: `orchestration-start-here` (ORGAN-IV) is the hub. It holds a `CROSS_ORG_TOKEN` — a Personal Access Token with `repo` and `workflow` scope across all 8 organizations.

2. **Dispatch receivers**: Each of the 8 organizations has a `.github` repository containing `dispatch-receiver.yml` — a workflow triggered by `repository_dispatch` events with typed payloads.

3. **Event flow**:
   ```
   Triggering workflow (any org)
     → gh api POST /repos/{target-org}/.github/dispatches
     → dispatch-receiver.yml in target org
     → routes to appropriate workflow based on event_type
   ```

4. **Token storage**: `CROSS_ORG_TOKEN` is stored as an organization secret in `orchestration-start-here` and `corpvs-testamentvm` (the two repos that initiate cross-org communication).

5. **Distribution secrets**: `MASTODON_TOKEN` and `DISCORD_WEBHOOK` are stored in `orchestration-start-here` for the POSSE distribution pipeline.

### Security Model

- The token has broad access (necessary for cross-org dispatch) but is only stored in 2 repositories
- Dispatch receivers validate `event_type` before executing — unknown types are ignored
- No secrets are passed in dispatch payloads — receivers use their own org-level secrets

## Consequences

### Positive

- **Decoupled organs**: Each org operates independently; cross-org communication is event-driven, not polling
- **Centralized routing**: All cross-org events flow through ORGAN-IV, making the communication graph auditable
- **Standard GitHub mechanism**: Uses `repository_dispatch`, a native GitHub feature — no external message brokers
- **Verified working**: Mastodon and Discord distribution tested and confirmed (HTTP 200/204) during AUTOMATA sprint

### Negative

- **Single token risk**: If `CROSS_ORG_TOKEN` is compromised, an attacker has write access to all 8 orgs. Mitigation: token is stored only in 2 repos, not exposed in logs.
- **Token rotation is manual**: PAT expiration requires manual renewal across both storage locations
- **GitHub rate limits**: Cross-org API calls consume the token's rate limit budget. High-frequency dispatching could hit limits.
- **Debugging is hard**: When a cross-org dispatch fails silently (event sent but receiver doesn't trigger), there's no centralized log — you must check both the sender's run and the receiver's run history
- **Free-plan limitations**: Branch protection and some workflow features are restricted on GitHub Free — cross-org dispatch works but some complementary features don't

## References

- Dispatch receiver template: `.github/dispatch-receiver.yml` in each org's `.github` repo
- Token setup: Sprint 29 AUTOMATA (`docs/specs/sprints/29-automata.md`)
- Distribution verification: HERMETICUM session (2026-02-17)
- Orchestration design: `docs/implementation/orchestration-system-v2.md`
