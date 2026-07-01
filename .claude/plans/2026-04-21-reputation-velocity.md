# Reputation Velocity — PR Triage + Distribution

## Context

24 open PRs across major open source projects (Anthropic, OpenAI, LangChain, Coinbase, Grafana, dbt, Dapr, DataDog, etc.). 2 PRs already merged but not yet announced on social media. Zero-income crisis makes visible reputation acceleration the highest-leverage work. ORGAN-VII distribution infrastructure is 75% built — templates, platform clients, and pipeline exist. The missing link: a `contribution-merged` template and the LinkedIn announcement drafts themselves.

Previous session (2026-04-20): bumped 4 stale PRs, fixed camel-ai CI (ruff), identified langgraph as merge-ready, pushed fastapi_mcp and coinbase for merge.

## Phase A: PR Intelligence Sweep

**Goal:** Check all 21 tracked PRs for activity since yesterday. Categorize. Respond where needed.

### A.1 — Bulk Status Fetch

Use `mcp__github__pull_request_read` (method: `get`, `minimal_output: true`) for each PR. Wave through 3 batches (memory-conscious):

**Wave 1 — High-value (yesterday's targets):**
- `camel-ai/camel#3974` — CI fixed yesterday, check if passing now
- `langchain-ai/langgraph#7237` — was merge-ready, check if merged
- `tadata-org/fastapi_mcp#274` — pushed for merge
- `coinbase/agentkit#1054` — pushed for merge
- `anthropics/anthropic-sdk-python#1306`
- `openai/openai-agents-python#2802`
- `modelcontextprotocol/python-sdk#2361`

**Wave 2 — Mid-tier:**
- `dapr/dapr#9719`, `databricks/dbt-databricks#1376`, `DataDog/guarddog#703`
- `grafana/k6#5770`, `makenotion/notion-mcp-server#242`
- `a2aproject/a2a-python#915`, `indeedeng/iwf#601`

**Wave 3 — Remaining:**
- `anthropics/skills#723`, `Clyra-AI/gait#110`, `ipqwery/ipapi-py#8`
- `m13v/summarize_recent_commit#2`, `primeinc/github-stars#39`

### A.2 — Categorize Each PR

| Category | Criteria | Action |
|----------|----------|--------|
| `needs-response` | New comment/review from maintainer | Draft + post response |
| `close-to-merge` | Approved, CI passing | Wait or gentle bump |
| `waiting-on-maintainer` | No activity, CI passing | Log; bump if >7 days |
| `stale` | No activity >14 days | Polite bump comment |
| `blocked` | CI failing, merge conflicts | Fix CI or rebase |
| `newly-merged` | State changed to merged | Queue for Phase B |

### A.3 — Draft and Post Responses

For `needs-response` PRs: read comments, draft contextual response, post via `mcp__github__add_issue_comment`.
For `blocked` PRs: diagnose CI failure, fix locally if possible (like the ruff fix on camel-ai).
For `stale` PRs: post polite bump.

### A.4 — Update Backflow Manifest

**File:** `~/Workspace/organvm/organvm-corpvs-testamentvm/data/atoms/backflow-manifest.yaml`
Update `pr_state` for any PRs whose state changed. Add `last_checked` timestamp.

---

## Phase B: Distribution of Merged PRs

**Goal:** Create LinkedIn announcements for the 2 merged PRs. Create the missing `contribution-merged` template first.

### B.1 — Create `contribution-merged` Template

**New file:** `~/Workspace/organvm/announcement-templates/templates/community/contribution-merged.md`

Frontmatter variables: `contrib.project_name`, `contrib.pr_number`, `contrib.pr_title`, `contrib.pr_url`, `contrib.problem`, `contrib.solution`, `contrib.language`, `contrib.project_significance`

Channel blocks: mastodon (500 chars), discord (4096), bluesky (300), linkedin (1300), ghost (unlimited).

**Structural reference:** `~/Workspace/organvm/announcement-templates/templates/launch/repo-launch.md` — the only existing template with a `{{#channel linkedin}}` block.

### B.2 — Register in EVENT_TEMPLATE_MAP

**File:** `~/Workspace/organvm/kerygma-pipeline/kerygma_pipeline.py` line ~108
Add: `"contribution-merged": "contribution-merged"` to the map.

### B.3 — Draft LinkedIn Announcements

**dbt-labs/dbt-mcp#669:**
- Project: dbt MCP Server (dbt-labs) — brings MCP to the analytics engineering ecosystem
- Fix: Clarified OAuth page wording so non-configuring developers understand they're authorizing access, not setting up credentials
- Angle: UX clarity in developer tooling, dbt ecosystem contribution

**PrefectHQ/fastmcp#3662:**
- Project: FastMCP (PrefectHQ) — one of the most-used MCP server frameworks
- Fix: Corrected serialization of object query parameters per OpenAPI style/explode rules
- Angle: Deep protocol-level fix in core MCP infrastructure

**LinkedIn format target:** 800-1100 chars (within 1300 limit). Hook → problem → solution → significance → link → 3-5 hashtags.

### B.4 — Present Drafts for Review

Render announcements. Present to user. If approved, either:
- User posts manually to LinkedIn
- Use `mcp__claude-in-chrome` browser tools to navigate to LinkedIn and compose post

---

## Phase C: PR Status Checker Script

**Goal:** Replace manual GitHub API checking with a reusable script.

### C.1 — Create Script

**New file:** `~/Workspace/organvm/organvm-corpvs-testamentvm/scripts/pr-status-checker.py`

- Reads backflow manifest YAML for PR list
- Uses `gh pr view <url> --json state,title,updatedAt,labels,reviews,statusCheckRollup` for each PR
- Categorizes per A.2 logic
- Outputs summary table to stdout
- `--update` flag writes back to manifest
- Dependencies: stdlib + pyyaml only

### C.2 — Commit and Push

Commit new template, pipeline map update, checker script, and updated manifest to their respective repos.

---

## Critical Files

| File | Operation | Repo |
|------|-----------|------|
| `organvm/organvm-corpvs-testamentvm/data/atoms/backflow-manifest.yaml` | Read + Update | meta-organvm |
| `organvm/announcement-templates/templates/community/contribution-merged.md` | Create | organvm-vii-kerygma |
| `organvm/announcement-templates/templates/launch/repo-launch.md` | Reference only | organvm-vii-kerygma |
| `organvm/kerygma-pipeline/kerygma_pipeline.py` | Edit (line ~108) | organvm-vii-kerygma |
| `organvm/announcement-templates/kerygma_templates/quality_checker.py` | Reference (linkedin: 1300) | organvm-vii-kerygma |
| `organvm/organvm-corpvs-testamentvm/scripts/pr-status-checker.py` | Create | meta-organvm |

## Verification

1. **Phase A:** After sweep, verify PR count matches manifest (21 tracked). Any newly-merged PRs should appear in the Phase B queue.
2. **Phase B:** Render template with test data. Run quality checker against LinkedIn 1300 char limit. Verify no unresolved `{{ }}` variables in output.
3. **Phase C:** Run `python scripts/pr-status-checker.py` and verify it produces a table matching the manual sweep results from Phase A.

## Execution Order

```
A.1 → A.2 → A.3 + A.4 (parallel)
         ↓ (any newly-merged PRs feed into B)
B.1 → B.2 → B.3 → B.4
C.1 (can start after A.2, parallel with B)
C.2 (after all phases complete)
```

Phase A runs first because it may discover additional merged PRs. Phase B and C overlap.
