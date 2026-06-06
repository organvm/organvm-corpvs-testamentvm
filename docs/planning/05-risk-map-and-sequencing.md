# 05: RISK MAP & SEQUENCING

Dependency analysis, critical path, risks, and optimal sequencing for Phase 1 execution.

---

## Part 1: Dependency Map

### Critical Path Dependencies

**Foundation Layer (Sprint 1, must complete before Sprint 2):**
1. README Audit Framework (1.1) → All 7 organ templates
2. Repo Inventory Audit (1.2) → Task list for Sprint 2
3. Strategic Decisions (1.2) → Which repos to populate/archive
4. Task Setup (1.6) → Assign Sprint 2 work

**If any foundation incomplete:** Sprint 2 cannot begin.

### Within-Organ Dependencies

**ORGAN-I (Theory):**
- Independent repos (no internal deps)
- Order: Write ORGAN-I repos in parallel (no blocking)

**ORGAN-II (Art):**
- Depends on: ORGAN-I documentation must be accessible (for cross-refs)
- Order: Start ORGAN-II only after ORGAN-I templates finalized
- Portfolio infrastructure (showcase, archive, cases) must be populated before ORGAN-II complete

**ORGAN-III (Commerce):**
- Depends on: ORGAN-I/II documentation (for cross-refs)
- Order: Can start after ORGAN-I/II begin
- commerce--meta repo must be created before ORGAN-III complete

**ORGAN-IV (Orchestration):**
- Depends on: All other organs documented (for registry accuracy)
- Order: Do ORGAN-IV last (incorporates findings from others)

**ORGAN-V (Public):**
- Depends on: All other organs' READMEs (essays will reference them)
- Order: Write public-process README early, but essays second (Sprint 3)

**ORGAN-VI/VII:**
- Minimal dependencies
- Can be done anytime in Sprint 2

### Critical Path (Fastest to Completion)

```
Sprint 1:
  Day 1: Framework (1.1) ✅
  Day 2-3: Audit (1.2) + Decisions ✅
  Day 3-4: Templates (1.3) ✅
  Day 5: Setup (1.6) ✅

Sprint 2:
  Days 1-3: ORGAN-I + ORGAN-III (parallel, ~1.5M TE)
  Days 2-4: ORGAN-II portfolio (must complete ~110K TE showcase)
  Days 4-5: ORGAN-IV/V/VI/VII (fast, ~590K TE)
  Days 5: Validation + link checking

CRITICAL: Portfolio infrastructure (ORGAN-II) must be done early.
If delayed, causes cascading effects on ORGAN-II completeness.
```

---

## Part 2: Risk Assessment

### Risk 1: Documentation Burden Feels Overwhelming

**Probability:** High (60 repos = intimidating)
**Impact:** Schedule slip (5-10 days)
**Mitigation:**
- Use templates religiously (saves ~30% TE)
- Batch similar repos (write ORGAN-I theory together)
- Break into smaller chunks (3 repos/day = manageable)
- Remember: You already know what these repos do; you're just writing it down

**Contingency:** If overwhelmed by day 3, reduce scope:
- ORGAN-I: 3 priority repos only (instead of 10)
- ORGAN-II: Portfolio infrastructure + 2 flagships (instead of 13)
- Result: 70 repos → 50 repos, still shows complete system

---

### Risk 2: Code Examples Don't Work

**Probability:** Medium (40 repos have code)  
**Impact:** Credibility damage if broken examples go public  
**Mitigation:**
- Test every code example before committing
- Note if example requires specific setup (dependencies, versions)
- If example is complex, provide working Docker/environment file
- Get second person to run examples (confirm they work)

**Contingency:** If example breaks after publish:
- Fix immediately + update README
- Note in GitHub issue: "Fixed broken example in X.Y commit"
- No hiding failures; transparency is better

---

### Risk 3: Dependencies Incomplete

**Probability:** Low (audit in 1.2 catches these)  
**Impact:** Phase 2 validation fails on broken links  
**Mitigation:**
- Audit lists all dependencies upfront (1.2)
- Validate all links in phase 1.11 (validation pass)
- Second person checks links independently

**Contingency:** If link broken discovered in Phase 2:
- Fix in phase 1 extension (~15K TE)
- Delays phase 2 start by 1 day
- Acceptable cost for data accuracy

---

### Risk 4: Strategic Decisions Delayed

**Probability:** Medium (personal account decision unclear)
**Impact:** Blocks Sprint 2 (can't start until decision made)  
**Mitigation:**
- Make decisions by Thursday (Feb 13)
- If undecided: default to "Archive" (simpler)
- Get second opinion if stuck (5 min consultation)
- Record decision in registry immediately

**Contingency:** If decision missed deadline:
- Make decision Monday morning (Feb 17) before Sprint 2
- Cost: ~50K TE delay
- Still doable

---

### Risk 5: Review Quality Degradation

**Probability:** Medium (60 AI-generated READMEs to validate)
**Impact:** Generic or inaccurate content goes public
**Mitigation:**
- AI performs first-pass validation (template compliance, link checking, word count)
- Human reviews in focused batches (3-5 repos at a time per organ)
- Use Document 04 checklist for systematic coverage
- Prioritize review of flagship repos (ORGAN-I/II/III) over support organs

**Contingency:** If review fatigue sets in:
- Focus human review on portfolio-critical repos first
- Use AI cross-reference checking to catch link errors automatically
- Defer cosmetic review of ORGAN-VI/VII to Phase 2

---

### Risk 6: Empty/Skeleton Repo Decision Changes

**Probability:** Low  
**Impact:** Changes effort estimate  
**Mitigation:**
- Make populate/archive decision Friday (decision #3)
- Recommendation: Populate 4 critical repos only
- Record decision in registry
- Stick with decision (don't change mid-week)

**Contingency:** If decision changes mid-week:
- Note impact on effort estimate
- Adjust Sprint 2 schedule (add ~135K TE if populating additional repos)
- Update task list accordingly

---

### Risk 7: Sprint 2 Schedule Slips

**Probability:** Medium (~2.4M TE is compressed)
**Impact:** Cascading delays into Phase 2
**Mitigation:**
- Build ~95K TE contingency buffer (included in ~4.4M TE)
- Prioritize: ORGAN-I/III/II first (80% of value)
- If behind: Reduce ORGAN-VI/VII (lower priority)
- Track daily progress (3 repos/day = on track)

**Contingency:** If behind by ~150K TE:
- Extend Sprint 2 into weekend
- Delay Phase 2 start by 1 sprint if necessary
- Better late + complete than rushed + incomplete

---

## Part 3: Optimal Sequencing

### Sprint 2 Daily Breakdown (Optimal Order)

**Monday (Feb 17): High-Effort Orgs**
- ORGAN-I repos 1-3: ~210K TE
- ORGAN-III repos 1-3: ~210K TE
- Total: ~420K TE
- **Why:** Hardest content early, fresh mind

**Tuesday (Feb 18): Continue Heavy Lifting**
- ORGAN-I repos 4-7: ~280K TE
- ORGAN-III repos 4-6: ~210K TE
- Total: ~490K TE
- **Why:** Momentum + batch similar content

**Wednesday (Feb 19): Finish Core + Start Portfolio**
- ORGAN-I repos 8-10: ~170K TE
- ORGAN-III repos 7-12: ~350K TE
- **Critical: ORGAN-II showcase portfolio begins** (~88K TE)
- Total: ~608K TE
- **Why:** Portfolio must be 50% done by midweek to finish

**Thursday (Feb 20): ORGAN-II Push**
- ORGAN-II repos 1-5: ~350K TE
- portfolio showcase: ~88K TE (finish)
- archive-past-works: ~88K TE
- Total: ~526K TE
- **Why:** Portfolio infrastructure critical; knock it out

**Friday (Feb 21): Remaining Art + Meta**
- ORGAN-II repos 6-13: ~280K TE
- Org About sections: ~105K TE
- Local repos migration: ~50K TE
- Total: ~435K TE
- **Why:** Less TE on Friday = acceptable since we're caught up

**Saturday (Feb 22) - Optional Catch-Up**
- ORGAN-IV/V/VI/VII: ~250K TE (if needed)
- Link validation: ~45K TE
- Total: ~295K TE (contingency buffer)

**Sunday (Feb 23) - Final Review**
- Human review pass: 4 hours
- Final validation: ~30K TE
- repo-registry.json updates: ~30K TE
- Total: ~60K TE + human review (final push if needed)

### Critical Path Milestones

**Friday, Feb 14 (EOD Sprint 1):**
- ✅ All templates created
- ✅ All repos audited + scored
- ✅ 3 strategic decisions made
- ✅ Sprint 2 task list ready

**Wednesday, Feb 19 (Mid-Sprint 2):**
- ✅ ORGAN-I 70% done (7/10 repos)
- ✅ ORGAN-III 50% done (6/12 repos)
- ✅ ORGAN-II portfolio infrastructure 50% (showcase + archive started)
- **Status check:** On track?

**Friday, Feb 21 (EOD Sprint 2):**
- ✅ All 60 repos have draft README
- ✅ Portfolio infrastructure 90% (showcase, archive, cases mostly done)
- ✅ Peer review 50% (30 repos reviewed)
- **Status check:** Ready for validation pass?

**Sunday, Feb 23 (Final):**
- ✅ All 60 repos peer-reviewed + approved
- ✅ All links validated
- ✅ repo-registry.json updated
- ✅ All GitHub org About sections done
- ✅ Phase 1 COMPLETE ✅

---

## Part 4: What Can Go Wrong (Detailed)

### Scenario A: Code Examples Break (Tuesday, discovered)

**Problem:** ORGAN-I code example tested on Mac, doesn't work on Linux
**Timeline:** Discover in peer review (Tuesday afternoon)
**Action:** Author fixes example (~50K TE)
**Impact:** Delay that README 1 day, but OK (~95K TE contingency absorbs)
**Prevention:** Test on multiple platforms upfront

### Scenario B: Personal Account Consolidation Blocked (Wednesday, still undecided)

**Problem:** Still deciding between archive vs. mirror
**Timeline:** Blocks Sprint 2 task assignments
**Action:** Make executive decision "Archive" (~50K TE)
**Impact:** Minimal (decision made, move forward)
**Prevention:** Decide by Thursday deadline, not Wednesday

### Scenario C: Portfolio Infrastructure Incomplete (Wednesday, falling behind)

**Problem:** showcase-portfolio + archive-past-works bigger than estimated
**Timeline:** Wednesday check-in shows 20% instead of 50% complete
**Action:** Reduce scope: Put 8 works in showcase (not 15), archive 4 (not 10)
**Impact:** Trade completeness for timeliness; still sufficient
**Prevention:** Estimate portfolio work as ~135K TE (not ~110K TE) upfront

### Scenario D: Peer Reviewer Unavailable (Thursday)

**Problem:** Human reviewer capacity drops, can't keep up with AI output volume
**Timeline:** Discovered Thursday, 30 repos still need review
**Action:** Increase AI validation scope, focus human review on flagship repos only (add ~88K TE)
**Impact:** Saturday work mandatory, but doable
**Prevention:** Identify backup peer early (identify Monday)

### Scenario E: ORGAN-III Governance Docs Incomplete (Friday)

**Problem:** Realized ORGAN-III repos need contract templates/SLA docs (not just README)
**Timeline:** Friday afternoon, commerce--meta repo empty
**Action:** Create minimal governance scaffold (~50K TE)
**Impact:** Extended Phase 1 by ~50K TE, Phase 2 starts Monday instead
**Prevention:** Audit governance needs in 1.2 (upfront discovery)

---

## Part 5: Go/No-Go Decisions

### Friday, Feb 14 EOD: Sprint 1 Gate

**Go criteria:**
- [ ] All templates created (01-07)
- [ ] All 59 repos audited + scored
- [ ] 3 strategic decisions made + recorded
- [ ] Sprint 2 task list + assignments clear
- [ ] No blockers identified

**No-Go triggers:**
- ❌ Strategic decisions still unclear → Decide immediately or slip to Monday
- ❌ Templates incomplete → Can't start Sprint 2 without them
- ❌ Repo audit incomplete → Task list invalid

**Decision:** Should we proceed to Sprint 2?
- **If all criteria met:** YES, begin Sprint 2 Monday with full confidence
- **If 1 criterion unmet:** MINOR DELAY (fix Friday evening, start Monday with small gap)
- **If 2+ criteria unmet:** SLIP SPRINT 2 TO FOLLOWING MONDAY (not ideal, but better than rushed)

### Wednesday, Feb 19 Mid-Sprint: Mid-Sprint Check

**On-track criteria:**
- [ ] ORGAN-I 70% (7/10 repos complete)
- [ ] ORGAN-III 50% (6/12 repos complete)
- [ ] ORGAN-II portfolio 50% (showcase + archive started)
- [ ] Daily average TE on track
- [ ] Peer review lag < 10 repos

**If on track:** Continue as planned, finish Friday/weekend
**If behind by ~95K TE:** Adjust — extend one session, reduce scope slightly
**If behind by ~300K+ TE:** Decide Monday:
  - Extend Phase 1 to March 1 (adds 1 sprint)
  - OR reduce scope (50 priority repos only)
  - OR increase daily throughput for final days

### Sunday, Feb 23 EOD: Launch Gate

**Ready-to-launch criteria:**
- [ ] All 60 repos have comprehensive README
- [ ] All 14 local repos migrated
- [ ] All READMEs peer-reviewed + approved
- [ ] All links validated (0 broken)
- [ ] All GitHub org About sections complete
- [ ] repo-registry.json updated
- [ ] 0 critical issues remaining

**If all criteria met:** Phase 1 COMPLETE ✅ Launch Phase 2 immediately
**If 1-2 criteria unmet:** Fix in Phase 2 extension (~50K-72K TE Monday morning)
**If 3+ criteria unmet:** Phase 1 incomplete, delay Phase 2 start by 1 sprint

---

## Contingency Timeline (If schedule slips)

```
If Sprint 1 extends to Feb 17:
  → Sprint 2 shifts to Feb 17-24
  → Phase 2 starts Mar 3

If Sprint 2 extends to Mar 2:
  → Phase 2 starts Mar 10
  → Phase 3 starts Mar 31
  → Public launch moves to Mar 31

Cost: 2-sprint slip = acceptable. Better than rushed + incomplete docs.
```

---

**Risk Assessment:** Complete  
**Optimal Sequencing:** Ready to execute  
**Go/No-Go Gates:** Clear + documented  
**Phase 1 Ready:** YES ✅

Begin Sprint 1 immediately. Follow sequencing. Check gates per sprint.

