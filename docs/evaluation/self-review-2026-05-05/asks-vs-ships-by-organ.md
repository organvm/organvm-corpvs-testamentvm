# U8 — Per-Organ Asks vs Ships Rate

**Unit:** U8 of self-review-2026-05-05 batch
**Generated:** 2026-05-05 by background analysis worker
**Note on persistence:** Agent's Write tool was blocked by `PreToolUse:Write` substring-hook in worker sandbox. Content captured by parent-context coordinator and written to disk here. PR creation deferred — agent reported `PR: none — Write/Bash denied for this session by hook`.

---

## 1. Context

The eight-organ system has two parallel surfaces — the asks surface (prompt-atoms tagged by `universes`) and the ships surface (fossil-record commits tagged by `organ`). The execution multiplier `commits ÷ DONE-atoms` per organ separates governance closure (low multiplier) from implementation closure (high multiplier).

## 2. Method

- Atoms (24,599 total, snapshot 2026-05-01): for each atom, iterate `universes`; lower-case each tag; match `^organ-(i|ii|iii|iv|v|vi|vii)$`. Atoms with multi-organ tags fan out to each.
- Fossils (10,510 records, snapshot 2026-05-05): use canonical `organ` field as-is (`I`, `II`, `III`, `IV`, `V`, `VI`, `VII`, `META`, `LIMINAL`, `SIGMA_E`, `UNKNOWN`, `null`).
- DONE-rate = DONE / (OPEN + DONE + ARCHIVED + CLOSED-NAV + CLOSED-COMMAND).
- Multiplier = commits ÷ DONE.
- Snapshots are 4 days apart (small effect, multipliers slightly upper-bounded).
- Atom dataset and fossil dataset have NO foreign key — multiplier is a population-level ratio, not per-atom causality.

## 3. Findings

**F1 — ORGAN-IV consumes 40% of organ-tagged asks AND 33% of fossil commits, multiplier highest at 1.45.**
ORGAN-IV: 5,019 atom-instances (40.1%), 2,406 DONE (47.9%), 3,478 commits, **mult = 1.446** — implementation-heavy. Anchors: ATM-000241, ATM-000255, ATM-000260 (DONE); commits 05afe698d960, 59afee2d311d, bb389a21a003 (orchestration-start-here, agentic-titan).

**F2 — ORGAN-V and ORGAN-VII close cheapest (multipliers 0.46, 0.80).**
ORGAN-V: 84.6% DONE-rate (605/715), 279 commits, **mult = 0.461**.
ORGAN-VII: 91.3% DONE-rate (253/277), 203 commits, **mult = 0.802**.
Atoms close because conductor marks them; implementation under-fills. Anchors: ATM-001472, ATM-001737, ATM-001772 (V/DONE); ATM-003377, ATM-003400, ATM-003404 (VII/DONE); commits 6ebcca6fc8e2, f746bef8b77a (V); 5043325c49da, 515cbd9d7ca9 (VII).

**F3 — ORGAN-III has the largest under-implemented backlog: 1,507 OPEN, 44.2% DONE-rate.**
Effectively 1:1 OPEN:DONE (1,507 : 1,428). Multiplier balanced at 1.114 (1,590 commits / 1,428 DONE). Anchors: ATM-001380, ATM-001383, ATM-001385 (OPEN); commits d85fb7ce6a9c, 7d4b3911caed, 1132a2a9e800 in public-record-data-scrapper, classroom-rpg-aetheria, life-my--midst--in.

**F4 — ORGAN-I and ORGAN-II close efficiently but emit sub-unity multipliers (0.69, 0.57).**
I: 1,116 DONE / 1,698 (65.7%), 767 commits → **mult = 0.687**.
II: 945 DONE / 1,151 (82.1%), 542 commits → **mult = 0.574**.
Two readings: (a) much closure is documentation/governance; (b) commits are dense per-commit (large refactors). Anchors: ATM-002432, ATM-003063, ATM-003067 (I/DONE); ATM-001379, ATM-001419, ATM-001421 (II/DONE); commits 1bc935b2a9f7, d09ce5092a84 (I); e727938c694f, 724b02ccb985 (II).

**F5 — ORGAN-VI is the most balanced organ: 86.9% DONE-rate, mult 0.844, smallest absolute backlog (54 OPEN).**
Lower directive intensity (4% of organ-tagged atoms) at healthy cadence. Anchors: ATM-002532, ATM-002972, ATM-003298 (DONE); commits 593a08683738, 0d8dfa6abc71 in adaptive-personal-syllabus, salon-archive, reading-group-curriculum.

**F6 — META: 16% of canonical commits but 6,898 atom-instances in the `meta` universe; multiplier 0.499.**
Atoms close very cheaply through registry edits and IRF entries rather than executable code. Anchor commits: dafd242ae097, 105eaed9e003, 4aa3f2d628e5 in organvm-corpvs-testamentvm.

**F7 — LIMINAL (1,161 commits) and SIGMA_E (184 commits) have NO atom-side counterpart.**
12.8% of all fossil commits emit without directive trace. Anchors: 5f6db142d25e, a6aac0bb1010 (LIMINAL); 5c98784a524a, 5dd175b0940c (SIGMA_E). Atomizer's universe taxonomy lacks a `liminal` / `personal-infra` category that the fossil resolver recognises.

## 4. Quantitative Tables

### Per-organ asks-vs-ships matrix

| Organ | total atoms | OPEN | DONE | DONE % | other | commits | mult | reading |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| ORGAN-I | 1,698 | 394 | 1,116 | 65.7% | 188 | 767 | **0.687** | absorbs > emits |
| ORGAN-II | 1,151 | 193 | 945 | 82.1% | 13 | 542 | **0.574** | absorbs > emits |
| ORGAN-III | 3,228 | 1,507 | 1,428 | 44.2% | 293 | 1,590 | **1.114** | balanced; large open |
| ORGAN-IV | 5,019 | 2,124 | 2,406 | 47.9% | 489 | 3,478 | **1.446** | implementation-heavy |
| ORGAN-V | 715 | 82 | 605 | 84.6% | 28 | 279 | **0.461** | closes cheap, ships less |
| ORGAN-VI | 427 | 54 | 371 | 86.9% | 2 | 313 | **0.844** | most balanced |
| ORGAN-VII | 277 | 21 | 253 | 91.3% | 3 | 203 | **0.802** | closes cheap, low volume |
| **subtotal** | **12,515** | **4,375** | **7,124** | **56.9%** | **1,016** | **7,172** | **1.007** | system-wide balance |

### Cross-cutting universes

| Universe | total | OPEN | DONE | DONE % | commits | mult |
|---|---:|---:|---:|---:|---:|---:|
| `meta` | 6,898 | 2,898 | 3,360 | 48.7% | 1,677 (META) | 0.499 |
| `personal` | 3,564 | 1,736 | 1,507 | 42.3% | 1,161 (LIMINAL, plausibility) | 0.770 |
| `unscoped` | 5,892 | — | — | — | — | — |
| `UNIVERSAL` | 10,297 | — | — | — | — | — |

### Per-repo intensity

| Organ | repos | commits | commits/repo | DONE atoms | DONE/repo |
|---|---:|---:|---:|---:|---:|
| ORGAN-I | 26 | 767 | 29.5 | 1,116 | 42.9 |
| ORGAN-II | 32 | 542 | 16.9 | 945 | 29.5 |
| ORGAN-III | 32 | 1,590 | 49.7 | 1,428 | 44.6 |
| ORGAN-IV | 22 | 3,478 | 158.1 | 2,406 | 109.4 |
| ORGAN-V | 6 | 279 | 46.5 | 605 | 100.8 |
| ORGAN-VI | 6 | 313 | 52.2 | 371 | 61.8 |
| ORGAN-VII | 6 | 203 | 33.8 | 253 | 42.2 |
| META-ORGANVM | 14 | 1,677 | 119.8 | 3,360 (`meta`) | 240.0 |

## 5. Negative Findings

- No atom-side `liminal` or `sigma_e` universe (12.8% of fossil commits without directive trace).
- No status code distinguishes "documented closure" from "implemented closure" — multiplier is the only proxy.
- 4-day snapshot asymmetry favours commits; multipliers are upper bounds.
- ORGAN-PSG has 0 repos and 0 atoms — registry category but no surface.
- Multi-tag fanout: 12,515 tag-instances correspond to ~6,968 unique organ-tagged atoms.

## 6. Recommendations

**R1 — Schedule deliberate ORGAN-V/VII implementation sprints.** Cheapest closures (mult 0.46, 0.80) and highest DONE-rates (84.6%, 91.3%) — directives close faster than artifacts ship. Gate ORGAN-V/VII DONE transitions on artifact references (essay URLs, syndication URLs). Target multiplier: V → 0.8, VII → 1.0. Open scope: ATM-001461, ATM-001829, ATM-001854 (V); ATM-002928, ATM-005233, ATM-006248 (VII).

**R2 — Triage the ORGAN-III backlog: 1,507 OPEN is the largest single-organ debt surface.** At historical multiplier 1.11, retiring 1,507 OPEN implies ~1,670 additional commits — 100% of ORGAN-III commit volume already shipped. Run a one-time triage: ARCHIVE atoms whose direction shifted, COLLAPSE redundant atoms into IRF entries, leave priority-tagged OPEN. Target: <800 OPEN within 30 days.

**R3 — Add a `liminal`/`personal-infra` universe to the atomizer.** LIMINAL+SIGMA_E commits (1,345, 12.8% of canonical) have no directive-side trace. Recognise repos in `~/Workspace/4444J99/`, `domus-semper-palingenesis`, `system-system--system`, `portfolio` in the atomizer's universe-tagging step. Re-run the atom registry; expect unexplained-commit fraction to drop below 5%.

## Out-of-Scope Footnote

This unit deliberately does not address: stale plan retirement (U13), promised-but-not-delivered registry audit (U11), atom-to-IRF mapping (U9), per-essay/per-product accounting. INSIGHTS-FULL-HISTORY-2026-05-05 lines 99-114 contain the per-organ commit ranking already; this unit complements rather than restates by adding the asks side, DONE-rate, multiplier, and negative-space gaps.

---

**Validation gate:** 7 findings (>5 required), 30+ evidence anchors (atom-IDs and commit SHAs across all organs), 3 recommendations (>2 required), method explicit, out-of-scope footnoted.
