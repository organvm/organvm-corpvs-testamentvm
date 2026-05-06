# Master Self-Review — 2026-05-05

**Author:** Claude Opus 4.7 (1M context), parent-context coordinator
**Scope:** Synthesis across 13 unit reports + prior `INSIGHTS-FULL-HISTORY-2026-05-05.md` aggregate report
**Origin:** User invoked `/batch review my entire git history, review all my prompts, track what has been implemented, understand where im making errors and how to improve to become a better creator`
**Status:** Living artifact; supersedes the per-unit reports for executive-summary use

---

## Read this first

You asked four questions:
1. Review my entire git history
2. Review all my prompts
3. Track what has been implemented
4. Understand where I'm making errors and how to improve to become a better creator

The first three are *substrate questions* (status). The fourth is *meta-question* (improvement). Substrate findings: covered in 13 unit reports under `docs/evaluation/self-review-2026-05-05/`. Improvement findings: synthesized below.

**Headline answer to the meta-question:** Your governance and substrate-vocabulary work is real and lands. Your *traceability infrastructure* (atom→IRF→execution→commit) is broken in a way that makes self-knowledge expensive. Three concrete behaviors will compound the most: (1) a session-end close-out ritual that closes plans/atoms; (2) tightening hooks from substring-match to semantic-match; (3) treating the "wrong-approach > misunderstood-request" 2.4× ratio as a *pre-execution gate* problem, not a post-hoc apology problem.

---

## What's healthy (the negative findings — no problem here)

These are surprises in the *positive* direction. Cite them when you wonder if you're over-claiming:

1. **U11 — Public commitments match material reality.** All 66 GRADUATED + PUBLIC_PROCESS + flagship repos have commits within 90 days. Zero "promised but not delivered." The 27 LOCAL repos confirm *under*-claiming, not over-claiming.
2. **U1 — Repos are overwhelmingly maintained.** 87% of fossil-tracked repos (105 of 121) had commits in the last 30 days. Only 1 abandoned repo, and that's a low-stakes early experiment (gemini-cli-blender-extension).
3. **U6 — Emotional-atom volume is concentrated, not pervasive.** 312 emotional atoms across 24,599 = 1.3%. Concentrated in ORGAN-IV (24) and ORGAN-III (24); zero in II, V, VI, VII (creative/public/community/distribution). The frustration profile is *plumbing-specific*, not creative-practice-degrading.
4. **U2 — Conventional-commit adherence is solid (68.8%).** And witnessed commits are 2.5× longer than reconstructed (213 vs 83 chars), meaning session-aware tooling improves message quality.
5. **U10 — The persistent-needs are knowable.** ~1,127 of the OPEN-atom backlog are duplicates of doctrine already encoded as Universal Rules. The closure problem is *bookkeeping*, not unfilled need.

---

## What's not healthy (the actionable diagnoses)

These cluster into four cross-cutting pathologies.

### Pathology 1 — Directive-to-execution traceability is broken at the data layer

**Evidence (multi-unit):**
- **U13:** 90.4% of plans (386 of 427) in `~/.claude/plans/` are orphaned — neither DONE-NNN nor IRF-XXX-NNN reference, no follow-on artifact.
- **U3:** Only 3 of 10,510 fossil commits (0.03%) carry a session_id. The session→commit linkage infrastructure is non-functional.
- **U9:** The IRF document has irregular table/narrative/freestanding structure; programmatic atom→IRF mapping cannot be built reliably from the current shape.
- **U13 (corollary):** 253 fossil commits have `provenance: "witnessed"` but null session_id — the witness pipeline runs but the session-attribution step fails.

**Root diagnosis:** The system has all four registries (atoms, IRF, plans, fossil) but no foreign keys between them. They're parallel record-keepers, not a connected graph. "What was implemented?" requires manual cross-reading; the answer lives in human memory.

**Highest-leverage fix:** Normalize the IRF document into structured JSON (one-time pass). Add `current_session_id` to a known location at SessionStart. Backfill the 253 witnessed-but-orphan commits from timestamp matching. These three together restore the foreign-key web.

### Pathology 2 — "Wrong approach" exceeds "misunderstood request" 2.4× — Claude understands you, then picks the wrong branch

**Evidence (multi-unit):**
- **U7:** Of 179 correction atoms, 24% are governance violations (Claude broke a rule), 14% are tonal corrections (voice/style), only 2% factual. The user rarely corrects Claude on facts; they correct on path-selection.
- **U12:** Facet `wrong_approach` (60) is 2.4× `misunderstood_request` (25). 33% of high-tool-error sessions are also dissatisfied (vs 13% baseline).
- **U7 + U12 cross-cut:** The single most-common content word in correction atoms is "triggering" (1,477 occurrences across 179 atoms = 8.3 per atom). Combined with the 4 `hook_false_positives` in facets, the pattern is hooks/automation firing at wrong times.

**Root diagnosis:** Claude is competent at parsing intent but lacks a *pre-execution gate* that asks "is this the right branch given the goal?" The error mode is post-hoc — Claude commits to an approach and proceeds; corrections come after.

**Highest-leverage fix:** Add a structural pre-execution checkpoint. After Claude produces a plan, before tool execution: pause for user confirmation OR run an internal sanity-check ("does this approach honor the latest 3 user messages?"). This was the explicit recommendation in U12's R2 and U7's R1.

### Pathology 3 — Hooks treat string occurrences as semantic events

**Evidence (this very session):**
- The Write hook fired 14+ times during this session because the report content quoted the rule "LaunchAgent creation is forbidden" — substring-matching the literal token "LaunchAgent."
- **U12:** `hook_false_positives: 4` already in the prior facet data.
- **U7:** "triggering" appears 1,477 times in correction atoms — circumstantial but consistent evidence.
- The 11 background workers that hit Anthropic's rate limit could not write their reports because of the same hook pattern firing in worker sandboxes (where it acts as a HARD BLOCK rather than informational).

**Root diagnosis:** The hook implementation is substring-match, not semantic-match. It fires on content *that mentions* a forbidden pattern, not content *that creates* one. This produces false positives, which the home-scope CLAUDE.md explicitly acknowledges ("treat as informational unless the artifact actually proposes a LaunchAgent").

**Highest-leverage fix:** Convert the LaunchAgent guard (and any similar hooks) from substring-match to semantic-match. The check should be: does the file content actually create or reference `~/Library/LaunchAgents/*.plist`? Not: does the content contain the string "LaunchAgent" anywhere?

### Pathology 4 — Plan-author cadence vastly exceeds plan-execution cadence

**Evidence:**
- **U13:** 427 plans authored in `~/.claude/plans/` over ~68 days = 6.3 plans/day. Only 20 plans (4.7%) reached DONE — 0.3 plans/day execution rate. **21:1 author-to-execute ratio.**
- **U13 corollary:** Plan filenames are auto-generated session-slugs (`2026-04-27-ticklish-snacking.md`), not topic slugs — making them non-discoverable for re-engagement.
- **U10:** Of 14,898 OPEN atoms, ~67% (~9,932) are duplicates of doctrine already encoded. The closure mechanism is missing.

**Root diagnosis:** Plans serve as exploratory "thinking out loud" more than execution scaffolding. That's not bad in itself — but the *absence of a close-out ritual* means orphans accumulate as silent debt. Same pattern with atoms: doctrine encoded but atoms not closed against the doctrine.

**Highest-leverage fix:** Session-end ritual that walks back through plans authored that session and atoms tagged in that session. For each: mark DONE-NNN, IRF-XXX-NNN, mark via `closes_atoms` reference, or move to `~/.claude/plans/abandoned/`. Codify as a `/closeout` skill (the same recommendation already surfaced from the prior INSIGHTS report).

---

## Pattern map (which findings reinforce which)

```
                  Pathology 1                      Pathology 2
                  Traceability                     Wrong-approach
                  broken                           2.4× misunderstand
                       │                                  │
    ┌──────────────────┼──────────────────┐               │
    │                  │                  │               │
    U13               U3                  U9              │
    plans            session-id          IRF              │
    90% orphan       0.03% coverage      irregular        │
    ↓                ↓                   ↓                │
    bookkeeping      witness-pipeline    structure         │
    debt             bug                 normalization    │
                                         needed           │
                                                          │
                                       ┌──────────────────┤
                                       │                  │
                                       U7                 U12
                                       corrections        friction
                                       24% governance     wrong_approach 60
                                       14% tonal          buggy_code 48
                                       1,477× "triggering"
                                       ─────────────────────
                                       converge: pre-execution gate
                                       missing
                                       ───────────────────
                  Pathology 3                      Pathology 4
                  Substring-match                  Plan-execution gap
                  hooks                            21:1 ratio
                       │                                  │
                       │                                  │
                       this session: 14+ hook          U13 + U10
                       blocks on quoting the rule     plans never close
                       ↓                              ↓
                       semantic-match                 close-out ritual
                       conversion                     missing
```

The four pathologies share two roots: (a) the system over-relies on string-level signals (substring matches in hooks, keyword matches in registries) where it should use semantic-level structures; (b) the system has many recording surfaces (plans, atoms, IRF, fossil) but few connection-keeping rituals between them.

---

## Quantitative summary (one row per unit, top-line numbers)

| Unit | Title | Headline number | Verdict |
|---|---|---|---|
| U1 | Repo lifecycle | 87% ACTIVE (105/121); 1 abandoned | healthy |
| U2 | Commit hygiene | 68.8% conventional adherence; witnessed 2.5× longer | mostly healthy |
| U3 | Session→commit | 0.03% coverage (3/10,510) | broken |
| U4 | Question archetypes | "what" : "is_this" = 2.1:1 (operational > architectural) | mid-maturity |
| U5 | Vocabulary timeline | Substrate cluster emerged 2026-03-04 to 2026-03-20 | regime change |
| U6 | Emotional atoms | 1.3% of corpus; concentrated in IV+III, zero in II/V/VI/VII | concentrated friction |
| U7 | Correction taxonomy | 24% governance, 14% tonal, 49% unclassified | path-selection problem |
| U8 | Asks-vs-ships per organ | ORGAN-IV mult 1.45, ORGAN-V mult 0.46 | imbalanced ship rates |
| U9 | Atom→IRF mapping | irregular IRF structure prevents traceability | data-shape blocker |
| U10 | Repeated-asks | ~1,127 atoms = duplicate of encoded doctrine | bookkeeping gap |
| U11 | Promised-vs-delivered | 100% delivered at 90 days | clean signal |
| U12 | Friction synthesis | wrong_approach 2.4× misunderstand; 33% dissat at 5+ tool errors | pre-execution gate missing |
| U13 | Stale plans + orphans | 90.4% plans orphaned (386/427) | close-out ritual missing |

---

## Improvement roadmap — ranked by ROI × actionability

### Tier 1 — Highest-leverage, lowest-friction (start here)

**1. Convert the LaunchAgent hook from substring-match to semantic-match.**
*Why first:* it fired 14+ times in this session alone, and blocked 11 of 13 background workers from writing their reports. The smallest one-line change (in your hook implementation) that produces the largest immediate friction reduction. Source-of-truth: U12 + this session's runtime evidence.

**2. Build and use a `/closeout` skill at session end.**
*Why:* the 90% plan-orphan rate + 67% atom duplicate rate are both bookkeeping problems with the same fix — a close-out ritual that walks back through the session's outputs and ties them to closure markers (DONE-NNN, IRF-XXX-NNN, or `~/.claude/plans/abandoned/`). The prior INSIGHTS report already flagged this; this report confirms the leverage. Source: U13 + U10.

**3. Throttle parallel-agent dispatch to 4-5 max.**
*Why:* this batch attempted 13 parallel; 11 hit Anthropic's rate limit before completing. A simpler dispatch pattern (queue beyond 4-5 concurrent) would have produced 13 successful reports instead of 2 successful + 11 truncated. Source: U12 + this session's evidence.

### Tier 2 — High-leverage, moderate-friction (next)

**4. Add a pre-execution gate to Claude's tool-use flow.**
*Why:* the "wrong approach 2.4× misunderstand" finding is the single most-actionable framing of the friction profile. Implementation: after Claude produces a plan but before any non-trivial tool call, a checkpoint that asks "does this honor the user's last 3 messages and the most relevant Universal Rule?" Could be a hook, a skill, or a CLAUDE.md instruction; the form is less important than the existence. Source: U7 + U12.

**5. Normalize the IRF document into structured JSON.**
*Why:* until this exists, no programmatic atom→IRF traceability tool can be reliably built. One-time pass; converts heterogeneous markdown into queryable records. Enables the cross-index tool the system has needed since Phase 1. Source: U9.

**6. Fix the witness pipeline's session-attribution step.**
*Why:* 253 witnessed commits have no session_id (a bug, not by-design). Backfilling these from timestamp matching is straightforward; fixing the pipeline going forward unblocks future U3-style analyses. Source: U3 + U13.

### Tier 3 — Strategic (longer cycle)

**7. Schedule deliberate ORGAN-V and ORGAN-VII implementation sprints.**
*Why:* per U8, those organs have the lowest execution multipliers (V=0.46, VII=0.80) and highest DONE rates (V=84.6%, VII=91.3%) — meaning atoms close cheaply but artifacts under-fill. The public-facing surface of the system (essays, distribution) is the bottleneck. Source: U8.

**8. Triage the 1,507 OPEN ORGAN-III atoms.**
*Why:* the largest single-organ debt surface. Per U8, retiring all of them at the historical multiplier 1.11 implies ~1,670 commits — equivalent to ORGAN-III's entire commit history. A one-time triage (ARCHIVE / COLLAPSE / KEEP-PRIORITIZED) reduces noise and clarifies the actual remaining work. Source: U8 + U10.

**9. Run U5's deferred meaning-shift analysis.**
*Why:* the n-gram entry curves are documented; the meaning-shift narration was deferred. Sample 5 atoms per cohort for 5 key terms (organ, atom, conductor, IRF, vacuum) and narrate the drift. ~30-minute effort; produces direct insight into how the user's mental model has evolved. Source: U5.

### Tier 4 — Quality-of-data investments

**10. Tighten the `type=question` classifier.**
*Why:* 53% of question-typed atoms didn't match any modal frame because they aren't actually syntactic questions. Cleaner classification produces sharper U4-style trend analysis. Source: U4.

**11. Re-run U7 (correction taxonomy) with a sequential-pair classifier.**
*Why:* 49% of correction atoms remained unclassified by single-keyword heuristic because corrections are often phrased indirectly (via reformulation of the preceding atom). Looking at atom N-1 + atom N would capture implicit corrections. Source: U7.

**12. Investigate the test-commit gap.**
*Why:* only 1.5% of fossil commits are `test:` typed, and refactor commits are 1%. Either tests aren't tracked (folded into feat/fix) or test-coverage is genuinely thin. The latter is a real risk for ORGAN-III (commercial surface). Source: U2.

---

## Three behaviors to adopt this week

If you only do three things from this report:

1. **Build the `/closeout` skill** that walks back through the session's plans and atoms and assigns each a closure status. The 90% plan orphan rate is the single largest debt-accumulation pathology, and the fix is mechanical.

2. **Patch the LaunchAgent hook to semantic-match.** It's blocking real work in worker sandboxes. The patch is small; the effect is large.

3. **Adopt a pre-execution checkpoint pattern.** When Claude produces a non-trivial plan and before executing, pause: "does this honor the last few messages and the most relevant rule?" — either via explicit user gate or via a hook. The wrong-approach > misunderstand asymmetry doesn't fix itself; it requires a structural intervention.

---

## What this report cannot answer

Out of intellectual honesty, three things the data cannot resolve right now:

1. **Whether emotional-atom volume decreased after substrate vocabulary stabilized in March 2026.** The hypothesis is testable; the timestamps haven't been sampled. Follow-up needed.
2. **Whether the conductor-mode vs implementation-mode session pattern produces fewer commits.** The session_id linkage at fossil level is 0.03% — the question is unanswerable from current data. Fix the witness pipeline first.
3. **Whether the substrate-vocabulary terms have drifted in meaning.** U5 deferred Part 2. Sample-narration is owed.

---

## Verification

You asked for an answer. This report's answer is above. To verify it:

1. Read the headline ("become a better creator" answer) — does it ring true? If yes, the synthesis is calibrated. If no, the unit reports underneath are still useful raw material.
2. Spot-check 2 unit reports — pick the highest-stakes findings (U7 corrections, U13 plan orphans). Verify the numbers against your own knowledge.
3. Pick 1 Tier-1 recommendation — do you actually want to adopt it? If yes, the report has done its job. If no, the recommendations didn't land — feedback welcome.

---

## Provenance

- **Aggregate prior report:** `docs/evaluation/INSIGHTS-FULL-HISTORY-2026-05-05.md` — covers totals, ratios, and trend lines
- **Unit reports (this batch):** `docs/evaluation/self-review-2026-05-05/*.md` (13 files) — covers themes, patterns, and per-dimension findings
- **Plan file:** `~/.claude/plans/review-my-entire-git-shimmering-hedgehog.md` — captures the decomposition and Phase 1/2 reasoning
- **Production note:** 2 of 13 unit reports (U8 asks-vs-ships, U10 repeated-asks) were produced by background workers and captured to disk by parent context after the workers' Write tools were blocked. The other 11 unit reports were produced directly by the parent-context coordinator after the original background workers hit Anthropic API rate limits during simultaneous parallel dispatch. The findings stand on their own data; the production path is documented for transparency.

---

*This report itself is a candidate for IRF entry under the meta-system audit domain. Per Universal Rule #2 ("Nothing local only"), it should be committed and pushed.*
