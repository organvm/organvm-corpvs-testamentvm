# Codex 6-Repo Dispatch — Ready to Paste

Paste this into a Codex CLI terminal. It will build 6 new repos from the TDD plan.

---

```
Build 6 new ORGANVM Python repos from the complete TDD plan at ~/.claude/plans/2026-04-16-unspoken-sentences-full-implementation.md.

Execution order:
1. organvm--patchbay at ~/organvm--patchbay/ — unified patchbay signal substrate with emit/query protocol
2. logos--commercium at ~/Workspace/organvm-v-logos/logos--commercium/ — subscriber tier paywall
3. salon--editorial at ~/Workspace/organvm-v-logos/salon--editorial/ — transcript ingester
4. organvm--auto-agents at ~/Workspace/meta-organvm/organvm--auto-agents/ — repo classifier + coverage matrix
5. theoria--gubernans at ~/Workspace/organvm-i-theoria/theoria--gubernans/ — lifecycle state machine
6. theoria--viva at ~/Workspace/organvm-i-theoria/theoria--viva/ — Spencer Brown mark calculus

For each repo: scaffold → failing tests → implement → passing tests → seed.yaml → targeted registry entry → git commit + push.

Read the plan file for EXACT file contents and test code — execute every step verbatim.

CONSTRAINTS:
- NEVER overwrite registry-v2.json wholesale — only targeted inserts
- NEVER touch governance-rules.json
- Every repo must have seed.yaml matching the exact content in the plan
- Python 3.11+ only — use dict[str, Any] union syntax
- TDD strictly: write failing test first, verify it fails, then implement
- git push after each repo is complete
- Conventional Commits format
```
