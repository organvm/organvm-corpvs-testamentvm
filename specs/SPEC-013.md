# SPEC-013: Agent Swarm Topology

```
Document ID:      SPEC-013
Title:            Agent Swarm Topology
Version:          1.0
Status:           RATIFIED
Layer:            L5 — Swarm Governance
Authoritative:    Multi-Agent Coordination
Parent Specs:     SPEC-000 (System Manifesto), SPEC-001 (Ontology Charter), SPEC-005 (Rulebook)
Date Ratified:    2026-03-19
Grounding:        post-flood/specs/SPEC-013/grounding.md
Risk Register:    post-flood/specs/SPEC-013/risk-register.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. Agent Architecture Classification

ORGANVM's agents follow a hybrid/layered architecture combining reactive behavior (CI bots, linters, pre-commit hooks) with deliberative behavior (Claude Code sessions with plans and beliefs), per Wooldridge's (2009) three-family taxonomy. The hybrid architecture is not incidental but constitutionally required: AX-000-004 (Constitutional Governance) demands that governance constraints be enforced at every level of agent capability, from stimulus-response automation to planned multi-step reasoning.

### SWARM-001: Agent Classes

Four agent classes operate within ORGANVM, distinguished by architecture type, capability profile, and failure mode:

| Agent Class | Architecture | Capabilities | Primary Failure Mode | Persistence |
|-------------|-------------|-------------|---------------------|------------|
| **Human Operator** | Deliberative (BDI) | Direction, review, authorization, constitutional judgment | Fatigue, anchoring bias, attention scarcity | Persistent across sessions |
| **Claude Code** | Deliberative (BDI) | Code generation, governance operations, multi-file editing, registry modification | Hallucination, context-window overflow, confident incompetence | No persistence across sessions |
| **Gemini** | Deliberative (BDI) | Research synthesis, literature survey, analytical reasoning | Destructive file rewrites, drops frameworks under long context, assumes git tracking | No persistence across sessions |
| **Codex** | Reactive/Deliberative | Batch operations, file transformations, code execution | Encrypted reasoning (unauditable), limited interactive judgment | No persistence across sessions |
| **CI Bot** | Reactive | Test execution, lint checking, build verification | False negatives (flaky tests), no governance awareness | Stateless per run |

Each agent class maps to the BDI model (Wooldridge 2009) with varying fidelity:

- **Beliefs**: Registry state, seed contracts, governance rules injected via CLAUDE.md context. CI bots have no beliefs -- they respond to stimuli.
- **Desires**: Session scope declaration (the goal the operator assigns). CI bots have fixed objectives (pass/fail).
- **Intentions**: Plan files committed during the session. CI bots produce no plans.

### SWARM-002: The Honest-but-Incompetent Threat Model

All AI agent classes operate under the honest-but-incompetent threat model (Anderson 2020). Agents do not maliciously circumvent governance but may:

1. **Hallucinate governance state** -- believe a repo is GRADUATED when it is CANDIDATE
2. **Lose context mid-session** -- operate on stale assumptions about system state
3. **Misapply governance rules** -- pattern-match on similar-but-different scenarios from training data
4. **Overwrite protected data** -- generate wholesale file replacements that destroy existing content
5. **Assume environmental state** -- believe files are tracked by git when `.gitignore` excludes them

This threat model constrains every downstream design decision in SPEC-013 through SPEC-017. Authority constraints must be mechanically enforced, not advisory.

---

## 2. Organizational Meta-Model (AGR)

ORGANVM adopts Ferber's (1999) Agent/Group/Role (AGR) organizational meta-model as the structural backbone for multi-agent coordination. The system is explicitly organization-centered: the eight-organ topology, governance hierarchy, and promotion state machine are constitutionally imposed. No agent may unilaterally restructure the system.

### SWARM-003: Agent Registration

Every active agent session must be registered in the system's coordination infrastructure:

| Field | Description | Source |
|-------|-------------|--------|
| `agent_id` | Unique session identifier | Generated at session start |
| `agent_class` | One of: human-operator, claude, gemini, codex, ci-bot | Declared at invocation |
| `agent_handle` | Thematic identifier from word pools | `coordination/claims.py` |
| `session_scope` | Declared work objective | Operator specification |
| `organ_scope` | Which organs this session may operate within | Derived from session scope |
| `role` | Authority class (Section 3) | Assigned by operator or derived from agent class |
| `start_time` | Session initialization timestamp | System clock |
| `claims` | Active file/resource claims | `coordination/claims.py` |

Registration is recorded in `~/.organvm/claims.jsonl` as an append-only audit trail.

### SWARM-004: Group Structure

Groups are organ-scoped work contexts. A session working in ORGAN-III operates within ORGAN-III's group context, receiving ORGAN-III-specific beliefs (CLAUDE.md, seed contracts, aesthetic constraints). Group membership constrains the agent's operational scope:

| Group | Context Injection | Authority Scope |
|-------|------------------|----------------|
| META-ORGANVM | Constitutional corpus, repo-registry.json, governance-rules.json, all schemas | System-wide governance operations |
| ORGAN-I | Theoria CLAUDE.md, theoretical foundations, recursive systems | ORGAN-I repos only |
| ORGAN-II | Poiesis CLAUDE.md, creative production, generative systems | ORGAN-II repos only |
| ORGAN-III | Ergon CLAUDE.md, product specifications, revenue models | ORGAN-III repos only |
| ORGAN-IV | Taxis CLAUDE.md, orchestration protocols, conductor system | Cross-organ coordination |
| ORGAN-V | Logos CLAUDE.md, discourse, editorial | ORGAN-V repos only |
| ORGAN-VI | Koinonia CLAUDE.md, community infrastructure | ORGAN-VI repos only |
| ORGAN-VII | Kerygma CLAUDE.md, distribution automation | ORGAN-VII repos only |

An agent may belong to multiple groups when a session spans organs (e.g., cross-organ dependency refactoring). Multi-group membership requires elevated authority (Section 3).

### SWARM-005: Role Assignments

Roles are abstract functional positions within groups that constrain behavior. Roles are assigned, not self-selected:

| Role | Default Agent Class | Assignment Authority |
|------|-------------------|---------------------|
| `governance-authority` | Human Operator | Constitutional (AX-000-003) |
| `orchestrator-agent` | Claude Code (system-scoped sessions) | Operator assignment |
| `domain-agent` | Claude Code, Gemini, Codex | Operator assignment or default |
| `ci-bot` | CI Bot | Automatic (trigger-based) |
| `read-only-observer` | Any (when monitoring) | Default for unscoped agents |

Role hierarchy: `governance-authority` > `orchestrator-agent` > `domain-agent` > `ci-bot` > `read-only-observer`. Permission inheritance follows Sandhu's RBAC1 model (SPEC-017, Section 2).

---

## 3. Supervisory Hierarchy

The supervisory hierarchy implements the constitutional authority stack (SPEC-000, Section 5) for agent governance:

```
                    Human Operator
                 (governance-authority)
                         |
            +-----------+-----------+
            |                       |
    Orchestrator Agent         Orchestrator Agent
    (META / cross-organ)       (organ-scoped)
            |                       |
    +-------+-------+       +------+------+
    |       |       |       |      |      |
  Domain  Domain  Domain  Domain Domain Domain
  Agent   Agent   Agent   Agent  Agent  Agent
    |       |       |       |      |      |
   CI      CI      CI     CI     CI     CI
   Bot     Bot     Bot    Bot    Bot    Bot
```

### SWARM-006: Authority Chain

Every agent action traces to the human operator through the supervisory chain:

1. The **human operator** holds constitutional authority (AX-000-003). All authority derives from operator delegation.
2. **Orchestrator agents** receive delegated authority for system-wide or organ-scoped coordination. They may direct domain agents but may not authorize critical governance operations (GRADUATED promotion, constitutional revision, governance-rules modification) without human confirmation.
3. **Domain agents** receive task-scoped authority within their declared session scope. They may not exceed their scope without re-authorization.
4. **CI bots** have fixed, non-delegable authority: execute tests, run linters, report results. They may block merges (reactive enforcement) but may not initiate governance actions.

### SWARM-007: Delegation Constraints

Authority delegation follows Saltzer and Schroeder's (1975) least privilege principle:

1. An agent may delegate only permissions it holds (no privilege escalation through delegation)
2. Delegation is scope-bound: an orchestrator delegating to a domain agent constrains the delegation to a specific organ, repo set, or task
3. Delegation is time-bound: it expires at session end unless explicitly renewed
4. Delegation is revocable: the delegating agent (or the human operator) may revoke at any time
5. Delegation is auditable: every delegation is recorded in the claims registry

---

## 4. CTDE Coordination Paradigm

ORGANVM adopts the Centralized Training with Decentralized Execution (CTDE) paradigm (Du & Ding 2021), structurally adapted for LLM agents. The structural insight -- centralized context plus decentralized action -- transfers from multi-agent reinforcement learning even though the learning mechanism does not.

### SWARM-008: Centralized Context (the "Training" Analog)

Shared coordination context aligns all agents toward system goals without requiring real-time communication:

| Context Source | Content | Injection Mechanism |
|---------------|---------|-------------------|
| SPEC-000 through SPEC-017 | Constitutional commitments, axioms, invariants | CLAUDE.md context blocks |
| `repo-registry.json` | System-wide repo state, promotion status, dependencies | MCP server queries, CLAUDE.md summaries |
| `governance-rules.json` | Governance constraints, allowed transitions, dependency rules | CLAUDE.md governance sections |
| `seed.yaml` (per repo) | Per-repo contracts, produces/consumes edges, event subscriptions | Direct file reads |
| Organ-level CLAUDE.md | Organ-specific conventions, build commands, architectural constraints | Automatic context injection |
| `claims.jsonl` | Active agent sessions, resource claims, coordination state | `coordination/claims.py` queries |

### SWARM-009: Decentralized Execution

Each agent acts independently within its session scope, making local decisions based on its beliefs about system state:

1. **Session autonomy**: Within declared scope, agents select implementation strategies, file editing approaches, and testing methods without real-time coordination
2. **Local decision-making**: Agents satisfice (Simon 1979) within tractable subsets rather than optimizing globally
3. **Coordination through artifacts**: Agents coordinate through shared filesystem state (registry, seeds, code), not through direct messaging
4. **Post-hoc integration**: Agent outputs are integrated through git (commits, PRs, merges), not through real-time state synchronization

### SWARM-010: Communication Model

ORGANVM restricts agents to mediated communication. No direct agent-to-agent messaging is permitted:

| Communication Type | Mechanism | Rationale |
|-------------------|-----------|-----------|
| **Blackboard** | Shared filesystem (registry, seeds, code, CLAUDE.md) | All state changes are observable (INV-000-005) |
| **Mediated** | Claims registry, tool checkout line | Coordination without direct coupling |
| **Broadcast** | Context-sync pipeline (CLAUDE.md regeneration) | Shared beliefs updated after state changes |

**Prohibited**: Direct agent-to-agent messaging, real-time chat between agent sessions, shared mutable state outside the filesystem. This constraint is motivated by INV-000-005 (Observability): direct communication would create unobservable coordination state.

---

## 5. Organizational Paradigm Hybrid

ORGANVM's topology is a hybrid combining three of Horling and Lesser's (2004) nine organizational paradigms. Horling and Lesser's key finding -- hybrid organizations outperform pure paradigms in domains with both hierarchical authority requirements and dynamic task allocation -- justifies this combination.

### SWARM-011: Hierarchy (Governance Authority)

The governance authority chain (Section 3) provides clear escalation paths, conflict resolution, and constitutional enforcement. Authority flows downward; information flows in all directions.

**Hierarchy handles**: Promotion authorization, governance constraint enforcement, constitutional revision, conflict resolution between concurrent agents.

### SWARM-012: Holarchy (Recursive Structure)

The organ/repo/module structure is holarchic: each node is both a self-contained whole and a part of a larger whole (Koestler's "holon"). Recursive self-similarity enables independent operation at each level while maintaining structural coherence.

| Level | Self-Contained Unit | Part Of |
|-------|-------------------|---------|
| Module | Independent function with own tests | Repository |
| Repository | Independent project with own CI, commits, releases | Organ |
| Organ | Independent domain with own aesthetic, conventions | System |
| System | Independent institution with own constitution | Environment |

**Holarchy handles**: Scope decomposition, local autonomy, independent development at each level.

### SWARM-013: Team-Based Coordination (Session Groups)

Sessions form temporary teams with shared goals. A Claude session working on engine tests may coordinate with a Gemini session conducting literature research for the same feature. Teams dissolve when the session ends.

**Team mechanisms**: Shared plan files, claims registry entries, organ-scoped CLAUDE.md context, session review summaries.

**Team handles**: Goal-directed collaboration, shared mental models, mutual commitment to declared scope.

---

## 6. Operational Bounds

### SWARM-014: Session Lifecycle

Every agent session follows a governed lifecycle:

```
SPAWN → CLAIM → OPERATE → RELEASE → DEBRIEF
```

1. **SPAWN**: Agent invoked with session scope declaration. Agent handle assigned. Claims registry entry created.
2. **CLAIM**: Agent declares resource claims (files, repos, organs it will operate on). Tool checkout line reserves heavy resources.
3. **OPERATE**: Agent executes within declared scope and authority. All governance-mutating operations pass through authority checks.
4. **RELEASE**: Agent releases resource claims. Tool checkout entries cleared. Work products committed to git.
5. **DEBRIEF**: Session review generated. Prompts extracted. Plan compliance assessed. Findings recorded.

### SWARM-015: Concurrency Constraints

Concurrent agent operations are governed by the tool checkout line (`coordination/tool_lock.py`):

| Lane | Concurrency | Operations | Rationale |
|------|------------|------------|-----------|
| **Heavy** | 1 concurrent | pytest, build, full lint | Memory-constrained (16GB); concurrent test suites cause OOM |
| **Medium** | 2 concurrent | ruff (single file), git commit | Moderate resource consumption |
| **Light** | Unlimited | File reads, registry queries, grep, context inspection | Negligible resource impact |

Resource capacity weight categories: light=1, medium=2, heavy=3, with a total budget of 6 units.

### SWARM-016: Non-Stationarity Management

Each agent's environment changes due to other agents' actions (Du & Ding 2021). Without coordination mechanisms, concurrent agents destabilize each other. Two mechanisms manage non-stationarity:

1. **Claims registry**: Makes each agent's activity visible to others. Before operating on a file, an agent checks whether another agent has claimed it.
2. **Tool checkout line**: Serializes access to heavy operations. Prevents concurrent test runs from exhausting system memory.

Auto-expiry (5 minutes) prevents stale claims from blocking other agents when a session crashes without cleanup.

---

## 7. Contestation Disclosures

### 7.1 CTDE Without Reinforcement Learning

**Status: ADAPTED** (risk register claim #4)

The CTDE paradigm (Du & Ding 2021) was developed for multi-agent reinforcement learning where agents have learnable parameters. ORGANVM's agents are LLMs with fixed weights and injected context. The coordination structure (centralized context + decentralized execution) transfers; the learning mechanism does not. ORGANVM's "centralized training" is context injection -- constitutional documents, governance rules, and registry state -- not gradient-based parameter updates.

### 7.2 Mediated-Only Communication

**Status: ADAPTED** (risk register claim #5)

The deliberate restriction to mediated-only communication goes against standard MAS recommendations for rich communication (Ferber 1999, Wooldridge 2009). ORGANVM accepts this tradeoff because INV-000-005 (Observability) requires that all state changes be observable. Direct agent-to-agent communication would create unobservable coordination state. The tradeoff (coordination efficiency vs. auditability) is acknowledged and accepted.

### 7.3 Agents Without Persistent State

The primary practical gap between MAS theory and ORGANVM's reality: theoretical agents have persistent state, well-defined capabilities, and reliable behavior. ORGANVM's LLM agents have no persistent state across sessions, probabilistic capabilities, and hallucination-prone behavior. The topology must be designed for agents that forget everything between sessions and may confidently assert false beliefs within sessions. This gap motivates SPEC-014 (bounded rationality constraints) and SPEC-017 (authority matrix enforcement).

---

## 8. Evolution Constraints

SPEC-013 may be amended through the following governed process only. This process is self-contained.

### 8.1 Amendment Types

| Type | Definition | Requirements |
|------|-----------|-------------|
| **Agent Class Addition** | Adds a new agent class (SWARM-001) with architecture classification and failure mode profile | Adversarial review + creator sign-off |
| **Organizational Revision** | Modifies the AGR structure (groups, roles, hierarchy) | Impact assessment on SPEC-017 (authority matrix) + adversarial review + creator sign-off |
| **Paradigm Revision** | Changes the organizational paradigm hybrid (hierarchy/holarchy/team) | New grounding narrative + adversarial review + human spot-check + creator sign-off |
| **Communication Model Change** | Permits direct agent communication or modifies mediated channels | Demonstration that INV-000-005 (observability) is preserved + adversarial review + creator sign-off |

### 8.2 Permanent Identifiers

SWARM identifiers (SWARM-001 through SWARM-016) are permanent. Removed items have their identifiers retired, not reassigned.

### 8.3 Versioning

The original SPEC-013 is never overwritten. Amendments are versioned: SPEC-013-v1.1, v1.2, etc.

---

## 9. Traceability

### 9.1 Upward Traceability (to SPEC-000)

| SPEC-000 Element | SPEC-013 Grounding |
|------------------|--------------------|
| AX-000-002 (Organizational Closure) | SWARM-008/009 -- CTDE ensures constitutive processes are coordinated through constitutional channels |
| AX-000-003 (Individual Primacy) | SWARM-006 -- human operator holds constitutional authority at hierarchy apex |
| AX-000-004 (Constitutional Governance) | SWARM-003/004/005 -- AGR model imposes constitutional structure on agent organization |
| AX-000-005 (Evolutionary Recursivity) | Section 8 -- the topology itself evolves through governed amendment |
| INV-000-001 (Dependency Acyclicity) | SWARM-012 -- holarchic structure preserves acyclic containment |
| INV-000-004 (Constitutional Supremacy) | SWARM-006/007 -- authority chain enforces hierarchical constraint precedence |
| INV-000-005 (Observability) | SWARM-010 -- mediated-only communication ensures all coordination is observable |

### 9.2 Lateral Traceability

| Peer Spec | Connection |
|-----------|-----------|
| SPEC-001 (Ontology Charter) | ONT-015 (SESSION) is the ontological classification of agent work episodes |
| SPEC-005 (Rulebook) | RULE-013 (Meta Governance) constrains orchestrator agents operating in META group |
| SPEC-014 (Resource Constraints) | Agent lifecycle (SWARM-014) is constrained by resource budgets |
| SPEC-015 (Escalation Policy) | Supervisory hierarchy (SWARM-006) defines the escalation chain |
| SPEC-016 (Epistemic Routing) | Group context (SWARM-004) determines epistemic scope |
| SPEC-017 (Authority Matrix) | Role assignments (SWARM-005) map to authority levels |

### 9.3 Downward Traceability (to implementation)

| SPEC-013 Element | Current Code Location | Alignment |
|------------------|-----------------------|-----------|
| Agent registration (SWARM-003) | `coordination/claims.py` punch_in/punch_out | ALIGNED |
| Agent handles | `coordination/claims.py` thematic word pools | ALIGNED |
| Tool checkout line (SWARM-015) | `coordination/tool_lock.py` heavy/medium/light lanes | ALIGNED |
| Resource capacity weights | `coordination/tool_lock.py` weight categories | ALIGNED |
| Claims registry (SWARM-016) | `~/.organvm/claims.jsonl` append-only JSONL | ALIGNED |
| Session debrief (SWARM-014) | `session/debrief.py` structured close-out | ALIGNED |
| AGR group context (SWARM-004) | `contextmd/generator.py` organ-level CLAUDE.md | DRIFT -- not formally linked to AGR model |
| Role hierarchy (SWARM-005) | Not implemented as formal RBAC | MISSING |
| Delegation constraints (SWARM-007) | Not implemented | MISSING |
| CTDE context injection (SWARM-008) | CLAUDE.md files, MCP server | DRIFT -- ad hoc, not formally structured |

### 9.4 Academic Lineage

| SPEC-013 Element | Traditions | Key Sources |
|------------------|-----------|-------------|
| Agent classification (SWARM-001) | Multi-agent systems | Wooldridge 2009 |
| AGR meta-model (SWARM-003/004/005) | Organizational MAS | Ferber 1999 |
| Hybrid topology (SWARM-011/012/013) | Organizational paradigms | Horling & Lesser 2004 |
| CTDE coordination (SWARM-008/009) | Multi-agent RL | Du & Ding 2021 |
| Honest-but-incompetent model (SWARM-002) | Security engineering | Anderson 2020 |

Full grounding narrative: `post-flood/specs/SPEC-013/grounding.md` (3,700+ words)
Full risk register: `post-flood/specs/SPEC-013/risk-register.md` (5 classified claims)
Full bibliography: `post-flood/specs/bibliography.bib`
