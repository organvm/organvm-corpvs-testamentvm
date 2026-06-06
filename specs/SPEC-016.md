# SPEC-016: Epistemic Routing Specification

```
Document ID:      SPEC-016
Title:            Epistemic Routing Specification
Version:          1.0
Status:           RATIFIED
Layer:            L5 — Swarm Governance
Authoritative:    Knowledge Coordination
Parent Specs:     SPEC-000 (System Manifesto), SPEC-001 (Ontology Charter), SPEC-007 (Interface Contract Spec)
Date Ratified:    2026-03-19
Grounding:        post-flood/specs/SPEC-016/grounding.md
Risk Register:    post-flood/specs/SPEC-016/risk-register.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. The Distributed-Knowledge Thesis

ORGANVM's knowledge is inherently distributed, local, and often tacit. No single omniscient agent is feasible. Hayek (1945) argued that the central economic problem is not optimization given known resources but coordination given distributed knowledge: "the knowledge of the particular circumstances of time and place" is inherently local and non-centralizable.

Attempting to centralize all system knowledge in a single context window or a single knowledge base would not merely exceed capacity -- it would decontextualize the knowledge, stripping it of the local circumstances that give it meaning.

### EPIS-001: Knowledge Distribution Map

| Knowledge Domain | Local Knowledge Holder | Knowledge Type | Centralizability |
|-----------------|----------------------|---------------|-----------------|
| Theoretical foundations | ORGAN-I repos, post-flood corpus | Explicit + tacit | Low -- contextual |
| Creative production | ORGAN-II repos, aesthetic cascades | Tacit-heavy | Very low |
| Product specifications | ORGAN-III repos, ecosystem.yaml | Explicit | Medium |
| Orchestration protocols | ORGAN-IV repos, conductor system | Explicit | Medium |
| Editorial standards | ORGAN-V repos | Tacit + explicit | Low |
| Community patterns | ORGAN-VI repos | Tacit-heavy | Very low |
| Distribution rules | ORGAN-VII repos, kerygma profiles | Explicit | High |
| Constitutional architecture | META repos, SPEC corpus | Explicit | High (already centralized) |
| Design intent | Human operator memory, session transcripts | Tacit | Non-centralizable |
| Implementation state | Registry, seeds, CI results | Explicit | High (already centralized) |

### EPIS-002: The Epistemic Routing Principle

Epistemic routing MUST route queries to local knowledge holders, not aggregate all knowledge centrally. When an agent needs to know ORGAN-III's product specifications, the route goes to ORGAN-III's seeds and documentation -- not to a global knowledge base. When an agent needs the dependency implications of a proposed change, the route goes to the seed graph and governance rules -- not to the operator's memory.

The constitutional corpus functions as ORGANVM's coordination mechanism -- analogous in function (not scale) to Hayek's price system. CLAUDE.md files, seed.yaml contracts, and governance-rules.json encode distributed system knowledge into navigable specifications that enable coordination without requiring any participant to hold all knowledge.

---

## 2. Source-of-Truth Registry

Every knowledge query must resolve to a definitive source. Ambiguity in source authority produces conflicting agent beliefs, which produce conflicting actions.

### EPIS-003: Source-of-Truth Hierarchy

| Query Domain | Authoritative Source | Secondary Sources | Conflict Resolution |
|-------------|---------------------|-------------------|-------------------|
| System identity and axioms | SPEC-000 through SPEC-017 | CLAUDE.md summaries | SPEC documents are canonical |
| Repo metadata (status, tier, dependencies) | `repo-registry.json` | MCP server responses, CLAUDE.md summaries | Registry is canonical |
| Repo contracts (produces, consumes, events) | `seed.yaml` (per repo) | Registry summaries, MCP responses | seed.yaml is canonical |
| Governance constraints | `governance-rules.json` | SPEC-005 prose descriptions | governance-rules.json is canonical for enforcement; SPEC-005 for intent |
| Entity identity (UIDs, naming) | `ontologia/entities.json` | Registry names | Ontologia is canonical |
| Entity history (events, transitions) | `ontologia/events.jsonl` | Git history | Ontologia is canonical |
| Schema definitions | `schema-definitions/schemas/` | Documentation references | Schema files are canonical |
| Implementation state (code, tests) | Source code in repos | Documentation, CLAUDE.md | Source code is canonical |
| Design intent | Human operator judgment | Session transcripts, plan files | Operator is canonical |
| Aesthetic standards | `organ-aesthetic.yaml`, `taste.yaml` | CLAUDE.md summaries | YAML files are canonical |

### EPIS-004: Source Conflict Protocol

When an agent encounters conflicting information from two sources:

1. **Check hierarchy**: The higher source in EPIS-003's hierarchy is canonical
2. **If same level**: The most recently modified source takes precedence (freshness)
3. **If freshness unclear**: Escalate to operator as T2 (SPEC-015, ESCL-002)
4. **Never resolve conflicts by averaging, interpolating, or synthesizing** -- pick one authoritative source

---

## 3. Context Injection Architecture

Context injection is the mechanism by which agents receive their beliefs about system state. This is the "centralized training" analog in the CTDE paradigm (SPEC-013, SWARM-008).

### EPIS-005: Context Injection Pipeline

```
Constitutional Layer        SPEC-000 axioms, invariants, governance principles
         |
         v
Workspace Layer             ~/Workspace/CLAUDE.md — multi-repo workspace map
         |
         v
Organ Layer                 <organ>/CLAUDE.md — organ-specific conventions, commands
         |
         v
Repo Layer                  <repo>/CLAUDE.md — repo-specific build, test, architecture
         |
         v
Session Layer               Session scope declaration, plan files, active claims
```

Each layer adds context without contradicting higher layers. Contradictions between layers are prohibited: a repo CLAUDE.md may not grant permissions that the organ CLAUDE.md restricts.

### EPIS-006: Context Generation

Context files are generated by `contextmd/generator.py` from templates that compose:

| Template Component | Content | Source |
|-------------------|---------|--------|
| Organ identity | Name, description, repo count | `organ_config.py`, registry |
| Organ-specific rules | Organ dictums from SPEC-005 | `governance-rules.json` |
| Development setup | Build, test, lint commands | Per-repo configuration |
| Data integrity rules | Protected files, read-before-write | System-wide constant |
| Dependency information | What this repo produces/consumes | `seed.yaml` |
| Ontologia context | Entity UID, naming history | `ontologia/` store |
| Session review section | Recent session summaries, active plans | Session infrastructure |

### EPIS-007: Context Consistency Invariant

For every agent at every moment: the agent's injected context MUST be consistent with the current source-of-truth hierarchy (EPIS-003). Stale context -- generated before the most recent source change -- violates this invariant.

| Staleness Detection | Mechanism |
|--------------------|-----------|
| Registry changed since context generation | Compare registry mtime against CLAUDE.md mtime |
| Seed changed since context generation | Compare seed.yaml mtime against CLAUDE.md mtime |
| Governance rules changed | Compare governance-rules.json mtime |

Remediation: `organvm context sync` regenerates all context files from current sources.

---

## 4. Context Budget Allocation

Agent context windows are finite. Not all system knowledge can be injected simultaneously. Context budget allocation determines what knowledge reaches the agent.

### EPIS-008: Context Budget Tiers

| Tier | Content | Priority | Budget Share |
|------|---------|----------|-------------|
| **Constitutional** | Axioms, invariants, data integrity rules, protected files | Mandatory -- always injected | Fixed overhead (~2K tokens) |
| **Structural** | Organ map, repo list, dependency graph summary | Mandatory for cross-organ sessions | Fixed (~3K tokens) |
| **Operational** | Build commands, test commands, lint configuration | Mandatory for the active repo | Variable by repo complexity |
| **Historical** | Recent sessions, plan files, session reviews | Optional -- injected when relevant | Variable by session age |
| **Aesthetic** | organ-aesthetic.yaml, taste.yaml cascades | Optional -- injected for creative work | Variable by organ |

### EPIS-009: Budget Allocation Rules

1. **Constitutional tier is non-negotiable**: Axioms, invariants, and data integrity rules are always present regardless of remaining budget
2. **Structural tier is mandatory for cross-organ work**: An agent operating across organs receives the organ map; an agent operating within a single repo may receive a compressed summary
3. **Operational tier scales with task complexity**: A simple bug fix needs minimal operational context; a refactoring needs comprehensive architecture documentation
4. **Historical and aesthetic tiers are demand-driven**: Injected only when the session scope requires them
5. **When budget is exceeded**: Compress lower tiers before truncating higher tiers. Never compress the constitutional tier.

### EPIS-010: Context Overflow Protocol

When total context exceeds the agent's context window capacity:

1. Remove historical tier (session reviews, old plan files)
2. Compress aesthetic tier to summary form
3. Compress structural tier to active-organ-only
4. If still exceeded: split task into multiple sessions with narrower scope

**Never**: Truncate constitutional tier, omit data integrity rules, or remove protected-file declarations to save space.

---

## 5. Knowledge Types and Routing Mechanisms

Following Nonaka and Takeuchi's (1995) SECI model, ORGANVM's knowledge exists at four codification levels, each requiring a different routing mechanism.

### EPIS-011: SECI Knowledge Types in ORGANVM

| SECI Type | Knowledge Conversion | ORGANVM Manifestation | Routing Mechanism |
|-----------|---------------------|----------------------|-------------------|
| **Socialization** (tacit to tacit) | Shared experience transfers uncodified knowledge | Operator working alongside agent in session; tacit design intuitions influencing agent behavior | Session-scoped shared context. The operator's presence IS the routing. |
| **Externalization** (tacit to explicit) | Articulation through concepts and models | Operator formalizing judgments into taste.yaml, governance-rules.json, SPEC documents | Document-mediated access. Once externalized, routable through file reads. |
| **Combination** (explicit to explicit) | Systematization and integration of codified knowledge | Registry queries, seed graph traversal, governance audit, metric computation, variable resolution | Computational routing. The dominant ORGANVM routing mode. |
| **Internalization** (explicit to tacit) | Learning-by-doing embeds knowledge | Repeated exposure changes operator intuitions; refined context injection improves agent responses | No explicit routing. Occurs through accumulated experience. |

### EPIS-012: Routing by Knowledge Type

| Query Type | SECI Classification | Route |
|-----------|-------------------|-------|
| "What is repo X's promotion status?" | Combination | Registry query (`organvm registry show X`) |
| "What does repo X produce?" | Combination | Seed query (`seed.yaml` read) |
| "Is this dependency graph acyclic?" | Combination | Governance check (`organvm governance check-deps`) |
| "What is the aesthetic tone for ORGAN-II?" | Combination | Aesthetic file read (`organ-aesthetic.yaml`) |
| "Should this repo be in ORGAN-III or ORGAN-I?" | Externalization needed | Escalate to operator (tacit knowledge of design intent) |
| "What is the right architectural pattern for this feature?" | Socialization | Operator involvement in session (shared design context) |
| "Why was this repo dissolved?" | Combination or Externalization | Ontologia lineage query; if insufficient, escalate to operator |

### EPIS-013: Externalization Prompts

When a Combination query fails (the explicit sources do not contain the answer), the system should prompt the operator to externalize tacit knowledge rather than allowing the agent to hallucinate:

| Failed Query | Externalization Prompt |
|-------------|----------------------|
| "What organ should this new repo belong to?" | "Operator: what functional domain does this repo serve? (See organ descriptions in SPEC-000 Section 5)" |
| "What aesthetic constraints apply to this output?" | "Operator: is there a taste.yaml or organ-aesthetic.yaml for this organ? If not, please specify tone and style." |
| "What is the design rationale for this architecture?" | "Operator: no design rationale found in CLAUDE.md or plan files. Please document intent for future queries." |

---

## 6. Active Inference as Conceptual Framework

Friston's (2010) free-energy principle provides a conceptual framework for understanding epistemic routing as query selection. An agent choosing what to query next is performing active inference -- selecting the action (query) that is expected to maximally reduce uncertainty about system state.

### EPIS-014: Hierarchical Generative Model

The constitutional hierarchy functions as a hierarchical generative model in the active inference sense:

```
SPEC-000 (axioms)          → generates predictions about system-level properties
    |
SPEC-003 (invariants)      → constrains predictions about governance properties
    |
governance-rules.json      → constrains predictions about operational properties
    |
seed.yaml (per repo)       → constrains predictions about repo-level properties
    |
Source code                 → observable state
```

Prediction errors (observations that deviate from predictions) propagate upward: a repo with missing seed.yaml generates a prediction error at the governance level, which propagates to the system level (governance coverage incomplete), which may reach the constitutional level (observability invariant threatened).

### EPIS-015: Uncertainty-Driven Query Selection

When an agent must decide what to query next, the optimal strategy is to query the source expected to maximally reduce uncertainty:

| Current Uncertainty | Optimal Query Target | Rationale |
|-------------------|---------------------|-----------|
| "Does this change break dependencies?" | Seed graph (`organvm seed graph`) | Dependency structure answers directly |
| "Is this repo's CI passing?" | CI runner (`organvm ci check`) | Direct observation, not inference |
| "What promotion criteria remain unmet?" | Governance engine (`organvm governance audit`) | Structured compliance check |
| "Is this architectural pattern acceptable?" | Organ CLAUDE.md + operator | Requires contextual judgment |
| "What is the system's overall health?" | Organism (`organvm organism`) | Aggregated diagnostic |

**ORGANVM does not literally compute variational free energy.** The active inference framework provides vocabulary and conceptual justification for the routing heuristics, not a computational implementation. The framework is a vocabulary, not a mechanism.

---

## 7. Convergence: Centralized Structure, Distributed Execution

The three theoretical traditions (Hayek, Friston, Nonaka) converge on a single architectural recommendation from radically different directions:

| Tradition | Centralized Component | Distributed Component |
|-----------|----------------------|----------------------|
| Hayek (economics) | Price signals | Local decisions |
| Friston (neuroscience) | Hierarchical generative model | Local prediction-error processing |
| Nonaka (management) | Organizational knowledge framework (ba) | Individual knowledge creation |
| **ORGANVM** | **Constitutional corpus** | **Autonomous agent sessions** |

SPEC-016 formalizes how queries traverse this structure -- from local agent context, through organ-specific knowledge sources, to system-level governance infrastructure, and if necessary, to the human operator as ultimate epistemic authority.

---

## 8. Contestation Disclosures

### 8.1 Active Inference Without Variational Computation

**Status: ADAPTED** (risk register claim #2)

Friston's (2010) free-energy principle describes biological neural processes operating through variational inference on continuous signals. ORGANVM's epistemic routing is a discrete decision process operating on structured data sources. The mathematical framework provides conceptual grounding, not computational implementation. ORGANVM does not compute variational free energy; it routes queries using heuristics that approximate the information-gain maximization that free-energy minimization implies.

### 8.2 Tacit Knowledge for AI Agents

**Status: ADAPTED** (risk register claim #3)

Nonaka and Takeuchi's (1995) tacit knowledge is embodied human know-how. ORGANVM's agents do not possess tacit knowledge in Nonaka's sense. The reinterpretation: "tacit" in ORGANVM means knowledge that exists in the system but is not codified in queryable form (operator intuitions, aesthetic judgments, architectural visions recorded only in session transcripts). This is a weaker form of tacit than Nonaka intends but captures a real epistemic category.

### 8.3 Constitutional Corpus as "Price System"

**Status: ADAPTED** (risk register claim #4)

Hayek's prices are compact numerical signals that compress distributed knowledge into a single scalar. ORGANVM's constitutional signals (CLAUDE.md, seed.yaml, governance-rules.json) are structured documents, not scalar values. The functional parallel holds -- both enable coordination without centralized knowledge -- but the mechanism (encoding vs. articulation) differs substantially. The constitutional corpus is more like a legal code than a price system.

---

## 9. Evolution Constraints

SPEC-016 may be amended through the following governed process only.

### 9.1 Amendment Types

| Type | Definition | Requirements |
|------|-----------|-------------|
| **Source Addition** | Adds a new source to the source-of-truth hierarchy (EPIS-003) | Adversarial review + creator sign-off |
| **Context Tier Adjustment** | Modifies budget tiers or allocation rules (EPIS-008/009) | Demonstrated context-window improvement + adversarial review + creator sign-off |
| **Routing Rule Addition** | Adds new query-to-source routing rules (EPIS-012) | Adversarial review + creator sign-off |
| **Framework Revision** | Changes the SECI mapping or active inference framework | New grounding narrative + adversarial review + human spot-check + creator sign-off |

### 9.2 Permanent Identifiers

EPIS identifiers (EPIS-001 through EPIS-015) are permanent. Removed items have their identifiers retired, not reassigned.

### 9.3 Versioning

The original SPEC-016 is never overwritten. Amendments are versioned: SPEC-016-v1.1, v1.2, etc.

---

## 10. Traceability

### 10.1 Upward Traceability (to SPEC-000)

| SPEC-000 Element | SPEC-016 Grounding |
|------------------|--------------------|
| AX-000-002 (Organizational Closure) | EPIS-005 -- context injection pipeline is itself a constitutive process producing coordination communications |
| AX-000-003 (Individual Primacy) | EPIS-003 -- operator holds ultimate epistemic authority for design intent |
| AX-000-004 (Constitutional Governance) | EPIS-003/004 -- source-of-truth hierarchy ensures governance knowledge is authoritative |
| AX-000-008 (Multiplex Flow Governance) | EPIS-001 -- epistemic routing operates through the information flow layer (G^info) |
| INV-000-005 (Observability) | EPIS-007 -- context consistency invariant ensures agents observe current state |

### 10.2 Lateral Traceability

| Peer Spec | Connection |
|-----------|-----------|
| SPEC-001 (Ontology Charter) | Ontologia entities (ONT-001 through ONT-028) are routable knowledge objects |
| SPEC-007 (Interface Contract) | Signal classes (SIG-NNN) define what knowledge flows between organs |
| SPEC-013 (Swarm Topology) | Group context (SWARM-004) determines epistemic scope per session |
| SPEC-014 (Resource Constraints) | Context budget (EPIS-008) is a bounded rationality constraint |
| SPEC-015 (Escalation Policy) | SA maintenance (ESCL-011) uses epistemic routing for state reconstruction |
| SPEC-017 (Authority Matrix) | Source access (EPIS-003) is constrained by authority levels |

### 10.3 Downward Traceability (to implementation)

| SPEC-016 Element | Current Code Location | Alignment |
|------------------|-----------------------|-----------|
| Context generation (EPIS-005/006) | `contextmd/generator.py`, `contextmd/templates.py` | ALIGNED |
| Context sync pipeline | `contextmd/sync.py`, CLI: `organvm context sync` | ALIGNED |
| Ontologia context injection | `contextmd/generator.py` `_build_ontologia_context()` | ALIGNED |
| MCP server as query router | `organvm_mcp/server.py` (the current MCP tool suite) | ALIGNED |
| Source-of-truth hierarchy (EPIS-003) | Implicit in code -- not formally declared | DRIFT |
| Context budget allocation (EPIS-008/009) | Not implemented | MISSING |
| Context consistency checking (EPIS-007) | Not implemented -- no mtime comparison | MISSING |
| SECI routing classification (EPIS-011/012) | Not implemented | MISSING |
| Externalization prompts (EPIS-013) | Not implemented | MISSING |
| Active inference heuristics (EPIS-015) | Not implemented -- agents choose queries ad hoc | MISSING |

### 10.4 Academic Lineage

| SPEC-016 Element | Traditions | Key Sources |
|------------------|-----------|-------------|
| Distributed knowledge (EPIS-001/002) | Economic epistemology | Hayek 1945 |
| Active inference (EPIS-014/015) | Computational neuroscience | Friston 2010 |
| SECI knowledge types (EPIS-011/012) | Knowledge management | Nonaka & Takeuchi 1995 |
| Centralized structure / distributed execution (Section 7) | Cross-disciplinary convergence | Hayek 1945, Friston 2010, Nonaka & Takeuchi 1995 |

Full grounding narrative: `post-flood/specs/SPEC-016/grounding.md` (4,000+ words)
Full risk register: `post-flood/specs/SPEC-016/risk-register.md` (5 classified claims)
Full bibliography: `post-flood/specs/bibliography.bib`
