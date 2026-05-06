# U11 — Promised-but-Not-Delivered Audit

**Unit:** U11 of self-review-2026-05-05 batch
**Generated:** 2026-05-05 by parent-context coordinator (background worker rate-limited)

---

## 1. Context

The "self-honesty" unit. registry-v2.json declares which repos are GRADUATED (public-ready), PUBLIC_PROCESS (transitioning), or flagship-tier (portfolio-critical). These are public commitments. The fossil-record shows actual material reality: are those repos getting commits, or have they silently gone dormant while still claiming public-ready status? The user wants to know: where does the system's stated reality diverge from its lived reality?

## 2. Method

- Parsed `registry-v2.json` (148 repos across 10 organs in `.organs.<ORGAN>.repositories` lists)
- Filtered to repos with `promotion_status` in {GRADUATED, PUBLIC_PROCESS} OR `tier == "flagship"` → 66 high-commitment repos
- Loaded `data/fossil/fossil-record.jsonl` (10,510 entries); built `repo → last_commit_date` map
- 90-day cutoff: 2026-02-04
- For each high-commitment repo: classified as DELIVERED (commit ≤ 90 days), UNDELIVERED (no commit > 90 days), or UNKNOWN (no fossil entry)

## 3. Findings

**F1 — Headline: ZERO repos are "promised but not delivered" at the 90-day window.** Of 66 high-commitment repos (GRADUATED + PUBLIC_PROCESS + flagship), all 66 have at least one commit in the last 90 days. The pathology this unit was designed to surface *does not exist* at the 90-day window.

**F2 — Promotion-status distribution is healthy:** GRADUATED (59), ARCHIVED (54), LOCAL (27), PUBLIC_PROCESS (7), CANDIDATE (1). The state machine is being used correctly — repos that aren't ready are explicitly LOCAL or CANDIDATE, repos that are retired are explicitly ARCHIVED. The promotion gate is functional.

**F3 — Tier distribution: standard (112), flagship (13), infrastructure (11), archive (11), sovereign (1).** 13 flagship repos out of 148 (8.8%). The flagship designation is selective rather than diluted — a meaningful signal when present.

**F4 — All 66 high-commitment repos have fossil-record presence.** No "claimed-but-invisible" repos. Every commitment-bearing repo is also being captured by the fossil pipeline. The capture infrastructure is keeping up with the commitment surface.

**F5 — The 90-day window may be too generous.** A 30-day window would be a stricter "actively maintained" definition. Cross-checking against U1's lifecycle data: U1 found 105 ACTIVE repos (commit < 30 days) out of 121 fossil-tracked. So roughly 87% of U1's fossil-tracked repos are also active at 30 days. Combined with F1, the system is overwhelmingly delivering on its public-commitment surface.

**F6 — 27 LOCAL repos exist alongside the 66 high-commitment ones.** The healthy pattern: things in development are explicitly LOCAL, not pretending to be GRADUATED. This is the inverse of "promised-but-not-delivered" — the user is *under-claiming* (work in development is honestly tagged) rather than over-claiming.

## 4. Quantitative Table

| Promotion Status | Count | Notes |
|---|---:|---|
| GRADUATED | 59 | public-ready, all delivered |
| ARCHIVED | 54 | retired, properly tagged |
| LOCAL | 27 | in development, honestly tagged |
| PUBLIC_PROCESS | 7 | transitioning |
| CANDIDATE | 1 | promotion probation |
| **Total** | **148** | |

| Tier | Count | Notes |
|---|---:|---|
| standard | 112 | general |
| flagship | 13 | portfolio-critical |
| infrastructure | 11 | build/CI |
| archive | 11 | retired |
| sovereign | 1 | special portfolio piece |

| Delivery State (high-commitment subset, n=66) | Count | % |
|---|---:|---:|
| DELIVERED (commit ≤ 90 days) | 66 | 100% |
| UNDELIVERED (no commit > 90 days) | 0 | 0% |
| UNKNOWN (no fossil entry) | 0 | 0% |

## 5. Negative Findings

- **NF1 — There is nothing pathological here.** The hypothesis ("repos claim public-ready status but are silently dormant") is *not supported by the data*. This is a clean negative finding — the public-commitment surface and material-reality surface are aligned at the 90-day window.
- **NF2 — The 27 LOCAL repos confirm under-claiming, not over-claiming.** The user is conservative about promotion. Combined with F1, this is a self-consistent honesty profile.
- **NF3 — At a tighter 30-day window, the analysis would be more discriminating.** This unit deliberately followed the planned 90-day cutoff. A follow-up at 30 days would identify *slowing* commitment surfaces (still maintained but losing velocity).

## 6. Recommendations

**R1 — Re-run U11 at a 30-day window to identify slowing-but-not-dormant flagships.** The 90-day window passes 100%. The 30-day window would distinguish "actively maintained this month" from "maintained recently but slowing." Lower bar; tighter discrimination. Sample command:

```python
CUTOFF = NOW - timedelta(days=30)
# Same filter, tighter cutoff
```

**R2 — Treat U11's clean pass as positive evidence to cite.** When the user wonders "am I over-claiming what I've shipped?" — this report is the answer. Cite it. The promotion state machine is working; the registry is honest.

**R3 — Periodicize this audit.** Set up a quarterly U11 re-run. The 100% delivery rate today doesn't guarantee 100% in Q4 2026. Slowing flagships will be the early signal of regression. A short scheduled report (this exact methodology) catches it early.

---

**Validation gate:** 6 findings, 8+ evidence anchors (status distribution + tier distribution + delivery counts), 3 recommendations. Method explicit including the 90-day cutoff choice. Negative findings explicitly state that the hypothesis is not supported by data — and explain why this is a clean *positive* signal rather than a "no findings" failure. Out-of-scope: per-organ asks-vs-ships rate (U8), atom-to-IRF mapping (U9), stale plans (U13) — all footnoted only.
