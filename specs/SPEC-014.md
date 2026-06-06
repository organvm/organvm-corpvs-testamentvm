# SPEC-014: Resource & Compute Constraints

```
Document ID:      SPEC-014
Title:            Resource & Compute Constraints
Version:          1.0
Status:           RATIFIED
Layer:            L5 — Swarm Governance
Authoritative:    Agent Resource Governance
Parent Specs:     SPEC-000 (System Manifesto), SPEC-003 (Invariant Register), SPEC-005 (Rulebook)
Date Ratified:    2026-03-19
Grounding:        post-flood/specs/SPEC-014/grounding.md
Risk Register:    post-flood/specs/SPEC-014/risk-register.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. Bounded Rationality as Design Premise

SPEC-014 is grounded in a theoretical certainty: no agent in ORGANVM -- human or AI -- can optimize. Simon (1979) proved that real decision-makers cannot optimize because they lack complete information, cannot foresee all consequences, and have limited computational capacity. Satisficing -- searching until an adequate solution is found, then stopping -- is the rational decision model under bounded conditions.

This is not a concession to imperfection. Spending resources on exhaustive search when an adequate solution is available is itself irrational. SPEC-014 formalizes satisficing at three levels:

### RSRC-001: Agent-Level Satisficing

Each agent session searches within tractable subsets rather than optimizing globally:

| Agent | Search Bound | Satisficing Criterion |
|-------|-------------|---------------------|
| Claude Code | Context window (~200K tokens) | Heuristic search (grep, dependency tracing, recent commits) until bug found or change implemented |
| Gemini | Context window + research scope | Literature survey until coverage threshold met or diminishing returns detected |
| Codex | Batch operation scope | File transformation until all targets processed |
| Human Operator | Attention budget per session | Review until confidence threshold met or fatigue detected |

### RSRC-002: Governance-Level Satisficing

The promotion pipeline does not verify every possible property of a repo before promoting it. It checks a defined set of criteria (SPEC-004 guard conditions) and promotes when criteria are met:

| Promotion | Satisficing Criteria | Not Checked |
|-----------|---------------------|------------|
| LOCAL -> CANDIDATE | seed.yaml exists, organ membership declared | Code quality, test coverage, documentation completeness |
| CANDIDATE -> PUBLIC_PROCESS | CI workflow configured, platinum status, implementation active | Architectural coherence, cross-organ impact, aesthetic compliance |
| PUBLIC_PROCESS -> GRADUATED | Soak test passing, documentation complete, cross-organ validation | Optimality of architecture, maximum possible test coverage |

### RSRC-003: System-Level Satisficing

The operator does not review every line of every agent's output. The review protocol focuses attention on high-risk changes and samples from low-risk ones:

| Review Category | Attention Investment | Rationale |
|----------------|---------------------|-----------|
| Governance-mutating changes | Full review | Constitutional integrity |
| Registry/schema modifications | Full review | System-wide propagation |
| New code in flagships | Targeted review | High-impact components |
| Test additions | Spot-check | Low risk, high volume |
| Documentation | Sampling | Low structural impact |

---

## 2. Cognitive Bias Guards

Kahneman (2003) demonstrated that even with adequate information, decision-makers systematically deviate from optimal due to cognitive biases that persist regardless of expertise or incentive. Three failure modes are particularly relevant to ORGANVM's agents.

### RSRC-004: Attribute Substitution Guard

**Bias**: When a target attribute is hard to assess, System 1 substitutes an easier heuristic attribute. For LLM agents, this manifests as hallucination: when the agent cannot determine the actual registry state of a repo, it substitutes a plausible-sounding state based on training data patterns.

**Guard**: Agents MUST query actual state before acting on governance assumptions. No governance-mutating operation may proceed based on pattern-matched beliefs alone.

| Target Attribute | Substitution Risk | Required Query |
|-----------------|-------------------|---------------|
| Repo promotion status | Agent believes status based on recent context | `organvm registry show <repo>` or repo-registry.json read |
| Dependency graph state | Agent assumes dependency structure | `organvm governance check-deps` |
| CI status | Agent assumes tests pass based on code inspection | Actual CI run or `organvm ci check <repo>` |
| Seed contract content | Agent generates plausible seed.yaml from memory | Direct seed.yaml file read |

### RSRC-005: Framing Normalization

**Bias**: Logically equivalent descriptions yield different decisions because they activate different associations. For LLM agents, this manifests as prompt sensitivity: the same governance constraint, presented in different phrasings, produces different agent behavior.

**Guard**: Constitutional constraints are injected through standardized context (CLAUDE.md, seed.yaml, governance-rules.json). Context injection uses canonical phrasings, not ad hoc descriptions. The `contextmd/generator.py` pipeline ensures framing consistency across all agents and sessions.

| Context Source | Framing Standard |
|---------------|-----------------|
| CLAUDE.md (workspace) | Generated by `organvm context sync` -- canonical format |
| CLAUDE.md (organ) | Generated by `contextmd/generator.py` -- organ-specific canonical format |
| CLAUDE.md (repo) | Generated by `contextmd/generator.py` -- repo-specific canonical format |
| governance-rules.json | Machine-readable constraint definitions -- no natural language ambiguity |

### RSRC-006: Accessibility Bias Mitigation

**Bias**: The most recently encountered or most easily recalled information dominates judgment. For LLM agents, this manifests as context-window recency bias: information at the end of the context window is more "accessible" than information at the beginning.

**Guard**: Critical constitutional constraints are structurally emphasized through placement and repetition:

1. **Constitutional constraints** appear in the CLAUDE.md header block (early in context) AND in the relevant section body (later in context)
2. **Data integrity rules** are repeated in both workspace CLAUDE.md and organ/repo CLAUDE.md
3. **Protected files** are listed explicitly in every context injection that grants write access
4. **Invariant violations** are surfaced at the point of the governance operation, not only in the initial context

### RSRC-007: Human Reviewer Bias Guards

The human operator is also subject to cognitive biases (Kahneman 2003). SPEC-014 mandates review protocols that address specific human failure modes:

| Bias | Manifestation | Mitigation |
|------|--------------|------------|
| **Fatigue** | Review quality degrades over long sessions; reduced System 2 engagement | Time-box review sessions; review critical changes first |
| **Anchoring** | Reviewer anchors on AI's initial output, biases toward acceptance | Review governance changes before code changes; independent state verification |
| **Accessibility** | Recently reviewed material receives more scrutiny; earlier output is under-reviewed | Rotate review focus across organs; use session review summaries for coverage |
| **Confirmation** | Reviewer seeks evidence confirming the AI's approach, ignoring contradictions | Structured review checklist with explicit disconfirmation questions |

---

## 3. Agent Lifecycle

Every agent session follows a governed lifecycle that constrains resource consumption at each phase:

### RSRC-008: Lifecycle Phases

```
SPAWN → CLAIM → OPERATE → RELEASE → DEBRIEF
```

| Phase | Resource Action | Governance Requirement |
|-------|----------------|----------------------|
| **SPAWN** | Agent process created; context window allocated; coordination entry created | Session scope declared; agent handle assigned; claims registry entry written |
| **CLAIM** | File locks acquired; tool checkout entries created; organ scope registered | Claims visible in `claims.jsonl`; tool checkout respects lane limits |
| **OPERATE** | Token consumption; file I/O; CI invocations; registry queries | Authority checks on every governance-mutating operation |
| **RELEASE** | File locks released; tool checkout entries cleared; work products committed | All modified files committed or explicitly abandoned; claims cleared |
| **DEBRIEF** | Session review generated; prompts extracted; plan compliance assessed | Debrief record written; test obligations collected for prove sweep |

### RSRC-009: Spawn Constraints

Agent spawning is constrained by system capacity:

| Constraint | Limit | Enforcement |
|-----------|-------|------------|
| Total concurrent agents | 3 (1 heavy + 2 medium, or 6 light units) | `coordination/tool_lock.py` weight system |
| Memory budget | 16GB total system | Heavy operations (pytest, build) limited to 1 concurrent |
| Context window per agent | Model-dependent (Claude ~200K, Gemini ~1M, Codex ~128K) | No enforcement -- natural model limit |
| Human attention budget | 1 operator | SPEC-015 escalation policy conserves attention |

### RSRC-010: Garbage Collection

Stale agent state must be cleaned up to prevent resource leaks:

| State Type | Staleness Threshold | Cleanup Action |
|-----------|-------------------|---------------|
| Claims registry entries | 5 minutes without heartbeat | Auto-expire, release claimed files |
| Tool checkout entries | 5 minutes without activity | Auto-expire, free lane slot |
| Orphaned plan files | No associated session in last 30 days | Flag for human review (not auto-deleted) |
| Stale context files | Generated > 7 days ago with source changes since | Regenerate on next `organvm context sync` |

---

## 4. Token Budgets

ORGANVM's compute resources are common-pool resources in Ostrom's (1990) sense: subtractable (tokens consumed by one agent are unavailable to others) and non-excludable within the system (any authorized agent can consume tokens).

### RSRC-011: Resource Classification

| Resource | CPR Character | Governance Mechanism |
|----------|--------------|---------------------|
| **LLM API tokens** | Subtractable, non-excludable | Per-session budget awareness (no hard enforcement -- API billing is external) |
| **CI minutes** | Subtractable, monthly renewal | Tool checkout line limits concurrent CI invocations |
| **System memory** | Subtractable, fixed | Heavy/medium/light lane concurrency limits |
| **Disk I/O** | Subtractable during heavy writes | Claims registry prevents concurrent writes to same files |
| **Human attention** | Subtractable, non-replenishable per session | SPEC-015 escalation policy (attention conservation) |

### RSRC-012: Ostrom's Design Principles Applied

Ostrom's (1990) eight design principles for sustainable common-pool resource governance map to SPEC-014 mechanisms:

| Ostrom Principle | ORGANVM Mechanism |
|-----------------|-------------------|
| (i) Clearly defined boundaries | Organ-scoped resource pools; session scope declarations |
| (ii) Congruence between rules and local conditions | Per-organ resource rules reflect organ ecology |
| (iii) Collective-choice arrangements | SPEC-015 escalation allows agents to request resource reallocation |
| (iv) Monitoring | Claims registry (`claims.jsonl`) tracks who is consuming what |
| (v) Graduated sanctions | Tool checkout line enforces graduated access (heavy: 1, medium: 2, light: unlimited) |
| (vi) Conflict resolution | Governance audit identifies resource conflicts between concurrent agents |
| (vii) Minimal recognition of rights to organize | Agents have constitutional autonomy to organize work within constraints |
| (viii) Nested enterprises | Organ/repo/module hierarchy provides nested resource accounting |

The institutional-design approach (self-governing rules) rather than centralized allocation (a scheduler that assigns tokens to agents) is a deliberate architectural choice. Centralized allocation requires a central authority with complete information about all agents' needs -- but Simon's bounded rationality proves that no such authority can exist.

---

## 5. The AI-Conductor Model

The AI-conductor model -- "human directs, AI generates volume, human reviews" -- is a rational organizational design in Simon's (1979) framework. It decomposes the decision space between two bounded agents along their respective comparative advantages.

### RSRC-013: Decision Decomposition

| Party | Decision Type | Satisficing Mode |
|-------|-------------|-----------------|
| **Human Operator** | Direction (what to work on) | Select based on strategic priorities, constitutional intent, tacit knowledge |
| **Human Operator** | Review (is output adequate?) | "Good enough?" not "optimal?" -- accept when criteria met |
| **AI Agent** | Generation (produce candidates) | Pattern matching, code synthesis, volume -- stop when scope satisfied |
| **AI Agent** | Execution (apply to codebase) | Mechanical tasks (file editing, test running, registry updating) |

Neither party optimizes. The human does not exhaustively evaluate all possible directions before choosing; the AI does not exhaustively search all possible implementations before generating. Both satisfice within their respective bounds. SPEC-014 formalizes these bounds: context-window limits for AI, attention budgets for human, token budgets for the system.

### RSRC-014: Effort Measurement

System effort is measured in LLM tokens, not person-hours. This reflects the AI-conductor model's resource structure:

| Metric | Unit | Tracked By |
|--------|------|-----------|
| Session token consumption | Tokens (input + output) | Session metadata / API billing |
| Session duration | Wall clock time | Session start/end timestamps |
| Review effort | Human attention minutes | Not automated -- self-reported |
| CI consumption | Pipeline minutes | GitHub Actions billing |

---

## 6. Contestation Disclosures

### 6.1 LLM Cognitive Biases as Kahneman Analogy

**Status: ADAPTED** (risk register claim #2)

Kahneman's dual-process theory describes human cognition. The application to LLM agents is behavioral, not mechanistic: LLMs exhibit pattern-matching (fast, associative, prone to hallucination -- System 1-like) and chain-of-thought reasoning (slower, serial, auditable -- System 2-like). The behavioral parallels are well-documented in LLM evaluation literature even though the underlying mechanisms differ. LLMs do not have neurological System 1 and System 2 circuits.

### 6.2 Ostrom's Principles Without Adaptive Learning

**Status: Acknowledged gap**

Ostrom's CPR governance works because human resource users learn from sanctions, adjust behavior based on monitoring, and develop shared norms over time. ORGANVM's AI agents do not learn between sessions, do not adjust behavior based on sanctions (they have no memory of being sanctioned), and do not develop norms. The institutional design constrains current behavior but does not produce the adaptive learning that makes Ostrom's institutions sustainable over time. The human operator must serve as the adaptive learner, adjusting institutional rules based on observed agent behavior.

---

## 7. Evolution Constraints

SPEC-014 may be amended through the following governed process only.

### 7.1 Amendment Types

| Type | Definition | Requirements |
|------|-----------|-------------|
| **Budget Adjustment** | Modifies token budgets, concurrency limits, or staleness thresholds | Adversarial review + creator sign-off |
| **Bias Guard Addition** | Adds a new cognitive bias guard (RSRC-004 through RSRC-007 pattern) | Empirical evidence of the bias + adversarial review + creator sign-off |
| **Lifecycle Revision** | Modifies the agent lifecycle phases (RSRC-008) | Impact assessment on SPEC-013 (topology) and SPEC-015 (escalation) + adversarial review + creator sign-off |
| **CPR Framework Change** | Modifies the Ostrom principle mapping or resource classification | New grounding narrative + adversarial review + human spot-check + creator sign-off |

### 7.2 Permanent Identifiers

RSRC identifiers (RSRC-001 through RSRC-014) are permanent. Removed items have their identifiers retired, not reassigned.

### 7.3 Versioning

The original SPEC-014 is never overwritten. Amendments are versioned: SPEC-014-v1.1, v1.2, etc.

---

## 8. Traceability

### 8.1 Upward Traceability (to SPEC-000)

| SPEC-000 Element | SPEC-014 Grounding |
|------------------|--------------------|
| AX-000-003 (Individual Primacy) | RSRC-013 -- human operator retains direction and review authority despite bounded rationality |
| AX-000-004 (Constitutional Governance) | RSRC-008 -- agent lifecycle phases are governed, not ad hoc |
| AX-000-005 (Evolutionary Recursivity) | Section 7 -- resource constraints evolve through governed amendment |
| INV-000-005 (Observability) | RSRC-011/012 -- resource consumption is monitored through claims registry |

### 8.2 Lateral Traceability

| Peer Spec | Connection |
|-----------|-----------|
| SPEC-003 (Invariant Register) | INV-000-005 (Observability) requires resource monitoring capabilities |
| SPEC-005 (Rulebook) | Governance-level satisficing (RSRC-002) maps to RULE guard conditions |
| SPEC-013 (Swarm Topology) | Agent lifecycle (RSRC-008) is the resource view of SWARM-014 |
| SPEC-015 (Escalation Policy) | Human attention budget (RSRC-011) motivates escalation conservation |
| SPEC-017 (Authority Matrix) | Cognitive bias guards (RSRC-004/005/006) complement authority enforcement |

### 8.3 Downward Traceability (to implementation)

| SPEC-014 Element | Current Code Location | Alignment |
|------------------|-----------------------|-----------|
| Tool checkout line (RSRC-009/011) | `coordination/tool_lock.py` | ALIGNED |
| Claims registry (RSRC-010/012) | `coordination/claims.py`, `~/.organvm/claims.jsonl` | ALIGNED |
| Resource weight categories (RSRC-009) | `coordination/tool_lock.py` (light=1, medium=2, heavy=3, budget=6) | ALIGNED |
| Auto-expiry (RSRC-010) | `coordination/tool_lock.py` 5-minute expiry | ALIGNED |
| Session debrief (RSRC-008) | `session/debrief.py` | ALIGNED |
| Context framing normalization (RSRC-005) | `contextmd/generator.py` | DRIFT -- not formally linked to bias mitigation |
| Token budget tracking (RSRC-011) | Not implemented | MISSING |
| Human reviewer bias protocols (RSRC-007) | Not implemented | MISSING |
| Governance-level satisficing criteria (RSRC-002) | `governance/state_machine.py` guard conditions | DRIFT -- implicit, not declared as satisficing |

### 8.4 Academic Lineage

| SPEC-014 Element | Traditions | Key Sources |
|------------------|-----------|-------------|
| Bounded rationality (RSRC-001/002/003) | Decision theory | Simon 1979 |
| Cognitive bias guards (RSRC-004/005/006/007) | Behavioral economics | Kahneman 2003 |
| CPR governance (RSRC-011/012) | Institutional economics | Ostrom 1990 |
| AI-conductor model (RSRC-013/014) | Organizational design | Simon 1979 |

Full grounding narrative: `post-flood/specs/SPEC-014/grounding.md` (3,800+ words)
Full risk register: `post-flood/specs/SPEC-014/risk-register.md` (5 classified claims)
Full bibliography: `post-flood/specs/bibliography.bib`
