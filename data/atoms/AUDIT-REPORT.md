# Prompt & Pipeline Data Audit
**Generated**: 2026-04-30

## Executive Summary

- **Prompts analyzed**: 4247
- **Signal prompts**: 4247 (100%)
- **Noise prompts**: 0 (0.0%)
- **Tasks**: 10647 (completion: 4.0%)
- **Links**: 16239 (empty-FP contamination: 0.0%)
- **Sessions**: 517
- **Recommendations**: 1 (1 P0)

**Overall Health Grade: B**

## Data Quality

| Noise Type | Count |
|------------|-------|

## Completion Funnel

| Stage | Count |
|-------|-------|
| Plans parsed | 1 |
| Tasks extracted | 10647 |
| Tasks with links | 1123 |
| Tasks with HQ links (J>=0.30) | 1123 |
| Completed tasks | 423 |

**Completion rate**: 4.0%
**Linkage rate (J>=0.30)**: 10.5%

### By Organ

| Organ | Tasks | Completed | HQ Linked | Plans |
|-------|-------|-----------|-----------|-------|
| I | 1071 | 2 | 26 | 1 |
| II | 98 | 0 | 0 | 1 |
| III | 237 | 1 | 38 | 1 |
| IV | 765 | 47 | 88 | 1 |
| LIMINAL | 2310 | 275 | 219 | 1 |
| META | 2221 | 41 | 504 | 1 |
| V | 107 | 0 | 0 | 1 |
| VI | 9 | 0 | 0 | 1 |
| VII | 38 | 0 | 6 | 1 |
| _root | 3791 | 57 | 242 | 1 |

## Prompt Effectiveness

### By Prompt Type

| Type | Prompts | Linked Tasks | Completed |
|------|---------|-------------|-----------|
| command | 2426 | 2472 | 149 |
| question | 670 | 2050 | 116 |
| context_setting | 574 | 10028 | 773 |
| continuation | 248 | 139 | 39 |
| git_ops | 177 | 873 | 83 |
| exploration | 103 | 230 | 20 |
| correction | 49 | 447 | 31 |

### By Size Class

| Size | Prompts | Linked Tasks | Completed |
|------|---------|-------------|-----------|
| long | 910 | 11753 | 917 |
| medium | 1113 | 3599 | 248 |
| short | 1683 | 439 | 29 |
| terse | 541 | 448 | 17 |

### Specificity Analysis

| Specificity | Linked Tasks | Completed |
|-------------|-------------|-----------|
| high | 4568 | 393 |
| low | 11671 | 818 |

**Correction rate**: 0.0% of threads (0/122)

## Session Patterns

### Session Length

| Prompts per Session | Count |
|---------------------|-------|
| 1 | 113 |
| 2-5 | 168 |
| 6-10 | 121 |
| 11-20 | 74 |
| 21-50 | 30 |
| 51+ | 11 |

### Session Duration

| Duration | Count |
|----------|-------|
| <5m | 76 |
| 5-15m | 44 |
| 15-30m | 40 |
| 30-60m | 42 |
| 1-2h | 44 |
| 2h+ | 158 |

**Productive sessions** (ending with git_ops): 26 (5.0%)

**Avg projects/day**: 4.6 | **Max**: 19

**Session churn**: 21.9% single-prompt (113/517)

### Hourly Distribution

| Hour | Prompts |
|------|---------|
| 00:00 | 240 |
| 01:00 | 143 |
| 02:00 | 73 |
| 03:00 | 104 |
| 04:00 | 72 |
| 05:00 | 69 |
| 06:00 | 51 |
| 07:00 | 71 |
| 08:00 | 50 |
| 09:00 | 20 |
| 10:00 | 36 |
| 11:00 | 137 |
| 12:00 | 193 |
| 13:00 | 239 |
| 14:00 | 305 |
| 15:00 | 338 |
| 16:00 | 232 |
| 17:00 | 217 |
| 18:00 | 220 |
| 19:00 | 198 |
| 20:00 | 217 |
| 21:00 | 323 |
| 22:00 | 352 |
| 23:00 | 347 |

## Linking Quality

**Total links**: 16239
**Empty-fingerprint contamination**: 0 (0.0%)
**Generic-tag-only links**: 37 (0.2%)
**High fan-out tasks (>100 links)**: 0

### Threshold Analysis

| Jaccard >= | Links | Tasks w/ Links | % of Total |
|-----------|-------|----------------|------------|
| 0.15 | 16239 | 1123 | 100.0% |
| 0.20 | 16239 | 1123 | 100.0% |
| 0.30 | 16239 | 1123 | 100.0% |
| 0.40 | 5235 | 909 | 32.2% |
| 0.50 | 3517 | 643 | 21.7% |

## Recommendations

| Priority | Category | Finding | Recommendation |
|----------|----------|---------|----------------|
| P0 | completion | Only 4.0% task completion rate | Run `organvm atoms reconcile --write` to update completion from git history |
