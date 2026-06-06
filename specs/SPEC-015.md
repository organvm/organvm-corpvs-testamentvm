# SPEC-015: Escalation & Attention Policy

```
Document ID:      SPEC-015
Title:            Escalation & Attention Policy
Version:          1.0
Status:           RATIFIED
Layer:            L5 — Swarm Governance
Authoritative:    Human-Agent Coordination
Parent Specs:     SPEC-000 (System Manifesto), SPEC-003 (Invariant Register), SPEC-005 (Rulebook)
Date Ratified:    2026-03-19
Grounding:        post-flood/specs/SPEC-015/grounding.md
Risk Register:    post-flood/specs/SPEC-015/risk-register.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. Attention as the Scarce Resource

SPEC-015 is fundamentally an attention-conservation system, not an information-routing system. Simon (1971) identified the foundational asymmetry: "A wealth of information creates a poverty of attention and a need to allocate that attention efficiently among the overabundance of information sources that might consume it."

Every escalation that reaches the human operator consumes irreplaceable attention. Unlike LLM tokens (which can be purchased) or CI minutes (which renew monthly), human attention is a fixed-capacity resource that degrades with fatigue, cannot be stockpiled, and regenerates only through rest. An escalation policy that routes every anomaly to the operator is a denial-of-service attack on the system's most critical resource.

### ESCL-001: The Attention-Conservation Principle

Simon's criterion for a well-designed information subsystem: it "absorbs more information than it produces -- it listens and thinks more than it speaks." Applied to SPEC-015:

1. Each level of the escalation hierarchy MUST be a net attention absorber
2. Agents MUST exhaust their own resolution capacity before escalating
3. Escalation summaries MUST be pre-digested, not raw
4. The operator's response options MUST be pre-structured (approve/deny/modify), not open-ended

**Operational test**: Does the escalation hierarchy reduce net demand on the operator's attention? If the system without escalation would require monitoring all 112 repos continuously, and the system with escalation requires 5-10 escalation responses per session, the hierarchy is functioning. If the pipeline produces 50 escalation alerts per session, it has failed -- it is generating attention demand, not absorbing it.

---

## 2. Four-Level Triage

Escalation events are classified into four severity levels. Classification determines routing, presentation format, and required response.

### ESCL-002: Triage Levels

| Level | Name | Condition | Routing | Response Time |
|-------|------|-----------|---------|--------------|
| **T1** | Routine | Agent can resolve within scope; no governance impact | No escalation -- agent resolves autonomously | Immediate (agent handles) |
| **T2** | Elevated | Agent needs confirmation but situation is bounded; governance impact is local | Escalation to operator with recommendation | Next review session |
| **T3** | Critical | Invariant threatened or cross-organ impact; agent cannot resolve without authority | Immediate escalation with three-level SA summary | Within current session |
| **T4** | Emergency | System-wide invariant violation, data corruption risk, or constitutional breach | Immediate escalation with compressed summary; all agent operations paused | Immediate |

### ESCL-003: Triage Classification Criteria

| Criterion | T1 (Routine) | T2 (Elevated) | T3 (Critical) | T4 (Emergency) |
|-----------|-------------|---------------|---------------|----------------|
| Governance scope | No governance change | Single-repo governance | Cross-repo or cross-organ governance | Constitutional or system-wide |
| Invariant impact | No invariant affected | Invariant preserved with care | Invariant at risk | Invariant violated or actively degrading |
| Reversibility | Easily reversible | Reversible with effort | Difficult to reverse | Irreversible (data loss, corruption) |
| Blast radius | Single file or function | Single repo | Multiple repos or organs | System-wide |
| Precedent | Routine operation | Known pattern | Novel situation | No precedent |

### ESCL-004: Classification Examples

| Situation | Level | Rationale |
|-----------|-------|-----------|
| Adding tests to a module | T1 | No governance impact; fully within agent scope |
| Promoting a repo from LOCAL to CANDIDATE | T2 | Governance change, but bounded and reversible |
| Promoting a repo to GRADUATED | T3 | Cross-organ implications; effectively irreversible in practice |
| Dependency cycle detected in production registry | T4 | INV-000-001 violated; system integrity at risk |
| Agent discovers repo-registry.json has < 50 repos | T4 | Data corruption; save_registry guard would fire |
| Modifying governance-rules.json | T3 | Constitutional impact; requires human confirmation |
| Agent finds conflicting instructions in two CLAUDE.md files | T2 | Bounded ambiguity; agent should report and request clarification |
| Agent cannot determine whether a change violates AX-000-003 | T3 | Constitutional judgment required; agent cannot resolve |

---

## 3. Three-Level Situation Awareness

Every escalation carries three levels of situation awareness information (Endsley 1995). An escalation providing only Level 1 forces the operator to reconstruct Levels 2 and 3 from scratch -- the most attention-intensive part of escalation handling.

### ESCL-005: SA Level Requirements

| SA Level | Content | Example (T3: GRADUATED promotion) |
|----------|---------|----------------------------------|
| **Level 1: Perception** | What elements are involved? Which repos, agents, governance rules? What changed? | "Repo X in ORGAN-III has passed all SPEC-004 guard conditions. Claude session ABC is requesting promotion to GRADUATED." |
| **Level 2: Comprehension** | What does it mean? Which invariants are affected? What is the blast radius? | "Promotion would make repo X the 2nd GRADUATED repo in ORGAN-III. All soak-test criteria met for 30 days. Downstream dependency impact: repos Y and Z consume repo X's produces edges." |
| **Level 3: Projection** | What will happen next? If no action is taken, will the system degrade? Deadlines at risk? | "Omega criterion #14 (GRADUATED promotion) advances from 4/17 to 5/17. No negative trajectory detected. Deferring promotion has no deadline consequence." |

### ESCL-006: SA Error Prevention

Endsley's (1995) SA error taxonomy identifies three failure types that SPEC-015's escalation format must prevent:

| SA Error Type | Agent Failure | Escalation Design Prevention |
|---------------|--------------|------------------------------|
| **Level 1 failure** (perception) | Escalation omits critical context | ESCL-005 mandates explicit element listing |
| **Level 2 failure** (comprehension) | Escalation provides numbers without meaning ("3 violations" without specifying which) | ESCL-005 mandates invariant identification and blast radius |
| **Level 3 failure** (projection) | Escalation lacks trend data or deadline context | ESCL-005 mandates trajectory projection and deadline impact |

---

## 4. Escalation Presentation

### ESCL-007: Structured Escalation Format

Every T2+ escalation follows this format:

```
ESCALATION [T2|T3|T4]
═══════════════════════
SITUATION (Level 1):
  Agent:       [agent handle and class]
  Scope:       [session scope declaration]
  Element:     [specific repo/organ/file involved]
  Trigger:     [what triggered the escalation]

ASSESSMENT (Level 2):
  Invariants:  [which invariants are affected, if any]
  Blast radius: [what else is impacted]
  Precedent:   [has this situation occurred before?]
  Rule refs:   [which RULE-NNN or INV-NNN apply]

PROJECTION (Level 3):
  If approved: [expected outcome]
  If deferred: [what happens if no action taken]
  If denied:   [consequences of denial]
  Deadline:    [relevant time constraints]

RECOMMENDATION:
  [Agent's recommended action with justification]

RESPONSE OPTIONS:
  [A] Approve recommendation
  [B] Approve with modification: ___
  [C] Deny with reason: ___
  [D] Request more information: ___
```

### ESCL-008: Anti-Clumsy-Automation Requirement

Woods and Hollnagel (2005) identified "clumsy automation" as the design pathology where automation works well under normal conditions but increases human workload precisely during anomalies. SPEC-015's anti-clumsy-automation requirement:

**Escalation presentations MUST be inversely proportional to situation severity.** The worse the crisis, the more compressed the initial summary must be, with drill-down available on demand.

| Level | Initial Presentation | Drill-Down Available |
|-------|---------------------|---------------------|
| T2 | Full structured format (ESCL-007) | Detailed context on request |
| T3 | Compressed: 3-sentence summary + response options | Full format on request |
| T4 | Single-line: "[EMERGENCY] INV-000-001 violated in repo-registry.json. All agent operations paused. [A] Investigate [B] Revert" | Full format + audit trail on request |

A T4 emergency that presents 47 individual violation reports (rather than a single synthesized summary with drill-down) violates ESCL-008.

---

## 5. Dilemma Reports

Not all escalations involve governance violations. Some involve genuine normative ambiguity where the agent cannot determine the correct action because the governance rules produce competing obligations.

### ESCL-009: Dilemma Report Structure

A Dilemma Report is generated when an agent encounters a situation where:

1. Two or more RULE-NNN obligations apply to the same entity in the same context
2. Satisfying one obligation prevents satisfying another
3. The agent cannot resolve the conflict through SPEC-005's defeasibility rules (priority ordering)
4. The conflict is not a rule error but a genuine normative tension

```
DILEMMA REPORT [T3]
════════════════════
CONFLICTING OBLIGATIONS:
  Rule A: [RULE-NNN] requires [action X]
  Rule B: [RULE-NNN] requires [action Y]
  Conflict: [action X] prevents [action Y]

DEFEASIBILITY ANALYSIS:
  Priority ordering: [result of SPEC-005 Section 5.1 analysis]
  Specificity: [result of specificity comparison]
  Resolution: [why SPEC-005's resolution mechanism fails here]

RECOMMENDED RESOLUTION:
  [Agent's recommended interpretation with justification]

GOVERNANCE CONSEQUENCE:
  [What precedent this resolution sets for future cases]
```

### ESCL-010: Dilemma Resolution Authority

| Dilemma Type | Resolution Authority | Governance Record |
|-------------|---------------------|-------------------|
| Operational (RULE vs. RULE within same level) | Human operator | Recorded as governance event in ontologia |
| Constitutional (RULE vs. invariant) | Human operator + adversarial review | Recorded as potential SPEC amendment trigger |
| Meta-governance (constraint about constraints) | Human operator + documented precedent | Recorded as constitutional interpretation |

---

## 6. Situation Awareness Maintenance

### ESCL-011: The Automation Paradox

As ORGANVM's agents handle more governance tasks autonomously, the operator has fewer routine interactions maintaining familiarity with system state. When an escalation arrives, the operator must reconstruct SA from a degraded baseline (Endsley 1995). SPEC-015 counteracts this with SA maintenance mechanisms independent of escalation events:

| Mechanism | Frequency | Content | SA Level Maintained |
|-----------|-----------|---------|-------------------|
| **Organism snapshot** | On-demand via `organvm organism` | System-wide health state, organ density, gate status | Level 1 (perception) |
| **Session review summary** | End of each session | What changed, what was reviewed, what remains | Level 2 (comprehension) |
| **Heartbeat report** | Daily (when system is active) | Aggregate: promotions today, test results, staleness warnings | Level 1 + Level 2 |
| **Trajectory projection** | Weekly or on-demand | Omega progress, deadline status, promotion pipeline forecast | Level 3 (projection) |
| **Governance audit** | On-demand via `organvm governance audit` | Full compliance report across all rules | All three levels |

### ESCL-012: SA Maintenance Is Not Escalation

SA maintenance mechanisms operate on a pull model (operator requests when ready) rather than a push model (system interrupts operator). The distinction is critical:

- **Escalation** (push): system interrupts operator because agent authority is insufficient
- **SA maintenance** (pull): operator queries system state to maintain mental model calibration

The only exception: T4 emergencies push notifications regardless of operator readiness, because system integrity is at stake.

---

## 7. Joint Cognitive System Design

ORGANVM is a joint cognitive system (Woods & Hollnagel 2005): the human operator and AI agents function as a coupled unit, not as separate entities exchanging data. The unit of analysis is the JCS, not the human or the machine in isolation.

### ESCL-013: The Substitution Myth

When agents take over governance tasks that the operator previously performed, the operator's role does not diminish -- it transforms. The operator moves from "doing governance" to "monitoring agent governance and handling exceptions." This transformation changes cognitive demands:

| Before (doing) | After (monitoring) | Cognitive Shift |
|----------------|-------------------|----------------|
| Reviewing every code change | Reviewing agent-flagged changes | From generation to evaluation |
| Running governance audits manually | Reviewing automated audit results | From procedure execution to anomaly detection |
| Making promotion decisions case-by-case | Confirming or overriding agent recommendations | From deliberation to judgment |
| Tracking system state continuously | Reconstructing state from snapshots | From maintenance to reconstruction |

SPEC-015 designs for the "after" cognitive demands, not the "before" demands.

### ESCL-014: Coordination Cost Budgeting

Every transfer of authority between human and agent incurs coordination overhead (Woods & Hollnagel 2005). The structured handoff protocol minimizes this overhead:

1. **Agent provides**: Situation summary at all three SA levels (ESCL-005)
2. **Operator selects**: From pre-structured response options (ESCL-007)
3. **Agent confirms**: Selected option and resumes execution
4. **System records**: Handoff in governance audit trail

Coordination cost per handoff should decrease as agent and operator develop shared conventions. But since AI agents have no persistent state, the conventions must be encoded in context (CLAUDE.md), not in agent memory -- an asymmetry the JCS framework was not designed for (see Section 8.1).

---

## 8. Contestation Disclosures

### 8.1 JCS in Asynchronous Context

**Status: ADAPTED** (risk register claim #5)

Woods and Hollnagel (2005) developed JCS for tightly coupled, real-time human-machine systems (aviation cockpits, nuclear control rooms). ORGANVM's human-AI coupling is looser: asynchronous sessions, git-mediated state, multiple concurrent agents. The JCS principles (coordination costs, substitution myth, authority negotiation) apply, but the coupling dynamics differ. Real-time JCS requires split-second handoff protocols; ORGANVM's handoffs operate on the timescale of minutes to hours.

### 8.2 Single-Operator Assumption

SPEC-015 designs for a single human operator (AX-000-003). If ORGANVM ever acquires multiple operators (contributors, collaborators), the escalation architecture must handle multi-stakeholder attention allocation -- a fundamentally different problem from single-operator attention conservation. The current architecture is optimized for the solo-operator case and will require redesign for multi-operator governance.

---

## 9. Evolution Constraints

SPEC-015 may be amended through the following governed process only.

### 9.1 Amendment Types

| Type | Definition | Requirements |
|------|-----------|-------------|
| **Triage Adjustment** | Modifies classification criteria or adds examples to triage levels | Adversarial review + creator sign-off |
| **Format Revision** | Modifies the escalation presentation format (ESCL-007) | Demonstrated attention-conservation improvement + adversarial review + creator sign-off |
| **SA Mechanism Addition** | Adds a new situation awareness maintenance mechanism | Evidence of SA gap + adversarial review + creator sign-off |
| **Level Addition** | Adds a 5th triage level or modifies the T1-T4 structure | New grounding narrative + adversarial review + human spot-check + creator sign-off |

### 9.2 Permanent Identifiers

ESCL identifiers (ESCL-001 through ESCL-014) are permanent. Removed items have their identifiers retired, not reassigned.

### 9.3 Versioning

The original SPEC-015 is never overwritten. Amendments are versioned: SPEC-015-v1.1, v1.2, etc.

---

## 10. Traceability

### 10.1 Upward Traceability (to SPEC-000)

| SPEC-000 Element | SPEC-015 Grounding |
|------------------|--------------------|
| AX-000-003 (Individual Primacy) | ESCL-001 -- escalation conserves the operator's irreplaceable attention |
| AX-000-004 (Constitutional Governance) | ESCL-002/003 -- triage levels ensure governance violations reach appropriate authority |
| AX-000-005 (Evolutionary Recursivity) | Section 9 -- escalation policy evolves through governed amendment |
| INV-000-004 (Constitutional Supremacy) | ESCL-010 -- dilemma resolution respects constitutional hierarchy |
| INV-000-005 (Observability) | ESCL-011 -- SA maintenance mechanisms ensure system state is observable to the operator |

### 10.2 Lateral Traceability

| Peer Spec | Connection |
|-----------|-----------|
| SPEC-003 (Invariant Register) | Triage classification (ESCL-003) references invariant impact as key criterion |
| SPEC-005 (Rulebook) | Dilemma Reports (ESCL-009) invoke SPEC-005 defeasibility analysis |
| SPEC-013 (Swarm Topology) | Supervisory hierarchy (SWARM-006) defines the escalation chain |
| SPEC-014 (Resource Constraints) | Human attention budget (RSRC-011) motivates attention conservation |
| SPEC-016 (Epistemic Routing) | SA maintenance (ESCL-011) routes knowledge queries for state reconstruction |
| SPEC-017 (Authority Matrix) | Triage routing (ESCL-002) respects authority level requirements |

### 10.3 Downward Traceability (to implementation)

| SPEC-015 Element | Current Code Location | Alignment |
|------------------|-----------------------|-----------|
| Organism snapshot (ESCL-011) | `metrics/organism.py`, CLI: `organvm organism` | ALIGNED |
| Session review (ESCL-011) | `session/debrief.py`, `session/analysis.py` | ALIGNED |
| Governance audit (ESCL-011) | `governance/audit.py`, CLI: `organvm governance audit` | ALIGNED |
| Triage classification (ESCL-002/003) | Not implemented | MISSING |
| Structured escalation format (ESCL-007) | Not implemented | MISSING |
| Dilemma Reports (ESCL-009) | Not implemented | MISSING |
| Anti-clumsy-automation (ESCL-008) | Not implemented | MISSING |
| Heartbeat reports (ESCL-011) | Not implemented | MISSING |
| Trajectory projection (ESCL-011) | `omega/scorecard.py` (partial -- omega status only) | DRIFT |

### 10.4 Academic Lineage

| SPEC-015 Element | Traditions | Key Sources |
|------------------|-----------|-------------|
| Attention conservation (ESCL-001) | Information economics | Simon 1971 |
| Triage levels (ESCL-002/003) | Human factors engineering | Endsley 1995 |
| Three-level SA (ESCL-005/006) | Situation awareness theory | Endsley 1995 |
| Anti-clumsy-automation (ESCL-008) | Cognitive systems engineering | Woods & Hollnagel 2005 |
| Automation paradox (ESCL-011) | Human factors | Endsley 1995, Woods & Hollnagel 2005 |
| JCS design (ESCL-013/014) | Joint cognitive systems | Woods & Hollnagel 2005 |

Full grounding narrative: `post-flood/specs/SPEC-015/grounding.md` (4,200+ words)
Full risk register: `post-flood/specs/SPEC-015/risk-register.md` (5 classified claims)
Full bibliography: `post-flood/specs/bibliography.bib`
