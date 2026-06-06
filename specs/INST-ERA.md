# INST-ERA: Era Model

```
Document ID:      INST-ERA
Title:            Era Model
Version:          1.0
Status:           RATIFIED
Layer:            L3B — Governance Instruments
Authoritative:    Constitutional Temporality
Parent Specs:     SPEC-000 (System Manifesto), SPEC-001 (Ontology Charter), SPEC-008 (Evolution & Migration Law)
Date Ratified:    2026-03-19
Grounding:        post-flood/specs/era-model/grounding.md
Risk Register:    post-flood/specs/era-model/risk-register.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. Era Definition

An era is a period of stable deep structure -- the set of fundamental constitutional choices that constrain all subsequent development. Deep structure is not merely important; it is *constraining* (it forecloses alternatives), *self-reinforcing* (the system develops routines and tooling that presuppose it), and *invisible during equilibrium* (it is the background against which all operations occur, not an object of attention).

The era model formalizes the distinction between two kinds of change: within-era convergence (incremental adjustment within stable deep structure) and era transition (revolutionary replacement of the deep structure itself). This distinction is grounded in Gersick's punctuated equilibrium paradigm (1991), which demonstrates the alternation between long stability periods and brief revolutionary restructuring across six domains of complex system organization.

### ERA-001: Deep Structure Dimensions

An era's deep structure comprises five constitutional dimensions. Changes to any of these dimensions constitute an era transition. Changes to anything else -- adding repos, promoting repos, adjusting CI criteria, extending schema fields, refining governance rules -- are within-era convergence.

| Dimension | Definition | Era 1 Value |
|-----------|-----------|-------------|
| **Organ topology** | How many organs exist, what domains they cover, how they are related | 8 organs (I-VII + META), META as zero-order constitutional substrate |
| **Dependency direction** | The structural constraint on inter-organ data flow | Unidirectional: I to II to III, no back-edges. ORGAN-IV orchestrates all. ORGAN-V observes (read-many, write-one). ORGAN-VII is pure consumer. |
| **Identity system** | The mechanism by which entities are recognized and tracked across mutations | ULID-based entity identity (ontologia), with name records as versioned expressions of stable UIDs |
| **Authority stack** | The hierarchy of constitutional authority | Three-layer: zero-order (META), first-order (ORGAN-IV/Taxis), domain (Organs I-VII) |
| **Promotion pipeline** | The lifecycle model for entity maturation | Five states: LOCAL, CANDIDATE, PUBLIC_PROCESS, GRADUATED, ARCHIVED |

This boundary is sharp by design. It prevents governance inflation (treating every change as constitutionally significant) while ensuring that genuinely constitutional changes receive the governed review they require.

### ERA-002: Convergence versus Reorientation

Following Tushman and Romanelli (1985), the boundary between convergence and reorientation is operationally defined by the activity-set test. A proposed change is convergence if it modifies at most one of four activity sets while preserving the other three. It is reorientation if it requires simultaneous changes to multiple activity sets.

**The four activity sets mapped to ORGANVM:**

| Activity Set | ORGANVM Mapping |
|-------------|----------------|
| **Strategy** | System mission and organ topology -- what domains exist, what the dependency direction is, what scope the system encompasses |
| **Structure** | Governance rules, promotion pipeline, schema contracts, registry format -- the formal mechanisms by which the system organizes itself |
| **Culture** | Naming conventions (double-hyphen syntax, Greek nomenclature), aesthetic identity (organ-aesthetic.yaml), documentation standards, commit message conventions |
| **Politics** | Authority stack (Meta zero-order, Taxis first-order, organs I-VII domain), resource allocation, decision rights |

**Convergence examples (within-era change):**

Adding a new repo to an existing organ: changes structure (one more entity) but preserves strategy, culture, and politics. Promoting a repo from CANDIDATE to PUBLIC_PROCESS: applies existing rules without changing them. Adding a new registry schema field: extends structure incrementally. Refining a governance rule threshold (e.g., `stale_repo_days` from 90 to 60): adjusts a parameter within the existing institutional framework.

**Reorientation examples (era transition):**

Adding a ninth organ (e.g., splitting System 3 and System 4 out of Taxis per the VSM diagnostic): changes topology (strategy), governance rules (structure), authority stack (politics), and potentially naming conventions (culture). Reversing dependency direction for a domain: changes the structural invariant (strategy), the dependency validator (structure), and the authority relationship (politics). Replacing the identity system: changes recognition (strategy), ontologia architecture (structure), all cross-referencing conventions (culture), and resolution logic (politics).

---

## 2. Era Transition Protocol

### ERA-003: Transition Triggers

Era transitions may be triggered reactively or proactively:

**Reactive triggers** (crisis-driven): The current deep structure proves insufficient.
- Governance rules that can no longer accommodate the system's actual structure (e.g., unidirectional dependency becomes untenable for a new domain that requires bidirectional collaboration)
- Internal contradictions that accumulate until the existing configuration becomes untenable (e.g., a formation repeatedly encounters deep-structure constraints that prevent its legitimate operation)
- Cognitive load assessments revealing that the human operator is struggling against the system's own constitutional architecture rather than being amplified by it

**Proactive triggers** (re-creation, per Tushman & Romanelli 1985): The human phase architect identifies a structural opportunity that the current deep structure cannot exploit.
- Strategic decisions to restructure before crisis forces it (e.g., dissolving organs, adding new ones, changing the identity system)
- Anticipation of environmental shifts (new platform requirements, new collaboration patterns, new scale thresholds)

Proactive transition (re-creation) is constitutionally harder than reactive reorientation because it requires changing a structure that is currently working, not one that has already failed. This is an advantage of single-operator systems: the operator can initiate era transitions based on strategic vision without the collective-action problems that multi-stakeholder organizations face.

### ERA-004: Transition Governance

An era transition follows the constitutional revision process defined in SPEC-000 Section 9, elevated to the most demanding tier:

1. **Evidence.** The transition proposal must cite specific evidence -- governance audit findings, formation activity constraints, cognitive load assessments, or strategic opportunity analysis -- demonstrating that the current deep structure is insufficient or that a new structure is achievable and superior.

2. **Activity-set analysis.** The proposal must specify which of the four activity sets (strategy, structure, culture, politics) change, and how. If only one activity set changes, the proposal is convergence, not era transition, and should be processed through the relevant spec's amendment procedure.

3. **Deep structure specification.** The proposal must define the new era's deep structure across all five dimensions (ERA-001): organ topology, dependency direction, identity system, authority stack, and promotion pipeline. Dimensions that remain unchanged must be explicitly confirmed.

4. **Migration plan.** The proposal must include a governed migration plan (SPEC-008) for transitioning from the current deep structure to the proposed one, including: backward-compatibility guarantees at each stage, entity identity preservation (AX-000-007), and rollback provisions.

5. **Interregnum governance.** The proposal must specify interim governance rules for the period during transition when the old deep structure has been challenged but the new one has not yet stabilized. At minimum, the following invariants must be preserved during the interregnum: INV-000-001 (Dependency Acyclicity), INV-000-003 (Identity Persistence), INV-000-005 (Observability).

6. **Constitutional classification.** The proposal is classified as a Breaking Revision requiring: a new grounding narrative, adversarial review, human spot-check of cited sources, explicit creator sign-off, and review of all downstream specs for consistency.

### ERA-005: Era Record

Every era is a first-class constitutional artifact with a structured record:

| Field | Content |
|-------|---------|
| `era_number` | Sequential integer (0, 1, 2, ...) |
| `era_name` | Descriptive name (e.g., "Pre-Constitutional," "Constitutional Order") |
| `start_date` | Date the era transition completed |
| `end_date` | Date the next era transition completed (null for current era) |
| `deep_structure` | Snapshot of all five ERA-001 dimensions at era start |
| `trigger` | What initiated the transition to this era (reactive or proactive, with evidence) |
| `predecessor_era` | Reference to the prior era record, with lineage edges |
| `transition_record` | What changed and why: activity-set analysis, migration plan executed, interregnum governance applied |
| `constitutional_corpus` | References to the SPEC corpus, governance rules, and schema definitions active during this era |

Era records are governed by INV-000-003 (Identity Persistence): once created, an era record is never destroyed. Its content is immutable after ratification. Corrections are addenda, not overwrites.

---

## 3. The Flood as Era 0 to Era 1

The flood -- the structural consolidation that dissolved 52 repos into `materia-collider` and reconstituted the system as an 8-organ constitutional order -- was ORGANVM's founding reorientation. In Gersick's terms, it replaced one deep structure with another. In Tushman and Romanelli's terms, it changed all four activity sets simultaneously.

### ERA-006: Era 0 (Pre-Constitutional)

| Dimension | Era 0 Value |
|-----------|-------------|
| Organ topology | None. 52 repos with no functional grouping. |
| Dependency direction | None. No dependency constraints. Arbitrary coupling. |
| Identity system | Name-based. Repos identified by GitHub slug. No persistent UID. |
| Authority stack | None. Each repo autonomous. No constitutional authority. |
| Promotion pipeline | None. No maturity lifecycle. Repos existed until abandoned. |

Era 0 arguably lacked deep structure in Gersick's formal sense -- it was pre-paradigmatic rather than paradigmatic. The era model records it as Era 0 with the understanding that the concept of "deep structure" may not fully apply to a state of structural absence. This is analogous to Gersick's observation that a system's first deep structure may be qualitatively different from subsequent ones: the founding reorientation creates deep structure from scratch, while subsequent era transitions replace one deep structure with another.

### ERA-007: The Transition

**Activity-set analysis:**

| Activity Set | Before (Era 0) | After (Era 1) |
|-------------|----------------|----------------|
| **Strategy** | Proliferation: create repos as ideas emerge, no constraint on number or organization | Topology: repos exist within a governed organ structure, each assigned to a functional domain with explicit boundaries |
| **Structure** | Flat: no hierarchy, no governance rules, no promotion pipeline, no dependency constraints | Hierarchical: three-layer authority stack, five-state promotion pipeline, acyclic dependency graph, seed.yaml contracts, schema-validated registry |
| **Culture** | Ad hoc: no naming conventions, no documentation standards, no aesthetic identity, no commit conventions | Constitutional: double-hyphen syntax, Greek organ names, conventional commits, CLAUDE.md in every repo, organ-aesthetic.yaml cascades |
| **Politics** | Decentralized: each repo autonomous, no inter-repo governance, no constitutional authority | Meta-governed: META-ORGANVM as zero-order constitutional substrate, ORGAN-IV/Taxis as first-order orchestrator, all organs subject to constitutional constraints |

The flood was not a gradual transition. It was a revolutionary period in Gersick's sense: a brief, intense restructuring that replaced the system's entire deep structure. The 52 dissolved repos were dissolved en masse, their content absorbed into `materia-collider`, and the system reconstituted around a new constitutional architecture. The post-flood corpus is the record of that reconstitution.

### ERA-008: Era 1 (Constitutional Order)

Era 1 deep structure is defined by the ERA-001 dimension values. The system operates under this deep structure as long as no dimension changes. Within-era convergence -- adding repos, promoting repos, refining governance rules, extending schemas -- elaborates and refines the existing deep structure without replacing it.

Known viability risk from the VSM mapping (SPEC-000 Section 5): System 3 (inside-and-now) and System 4 (outside-and-future) are conflated in Taxis (ORGAN-IV). Per Beer's diagnostic criteria (1972), these should be structurally separate. If the conflation becomes untenable, the governed separation of System 3 and System 4 into distinct organs would constitute an era transition -- a change to organ topology (strategy), governance rules (structure), and authority stack (politics) simultaneously.

---

## 4. Path Dependence (AX-000-007)

### ERA-009: Increasing Returns and Lock-In

Path dependence (North 1990) means that today's institutional choices are constrained by yesterday's. ORGANVM's governance infrastructure develops increasing returns through four mechanisms:

| Mechanism | ORGANVM Manifestation |
|-----------|----------------------|
| **Network effects** | Each repo adopting the current schema increases the cost of changing the schema, because change must propagate to all adopters |
| **Learning effects** | The operator becomes more proficient with the current governance framework, making the prospect of learning a new one less attractive |
| **Adaptive expectations** | Downstream systems and processes are built anticipating the current institutional structure, and their expectations must be updated if the structure changes |
| **Coordination effects** | The more components that coordinate through the current mechanism, the costlier it is to switch to a different coordination mechanism |

Path dependence operates at every level:
- **Schema level:** `repo-registry.json` is consumed by engine, dashboard, MCP server, validators. Changing the format is an institutional revolution.
- **Governance level:** The promotion pipeline is embedded in validators, audit reports, CLI commands, dashboard views, and documentation. Adding a new state or changing transition criteria requires updating the entire stack.
- **Naming level:** Double-hyphen conventions, Greek organ names, and Latin terms are structural identifiers embedded in URLs, directory names, import paths, and documentation cross-references. Changing a name requires updating every reference.

### ERA-010: Alchemical Inheritance as Prescriptive Path Dependence

AX-000-007 declares: "The system's prior structural failures are not waste but prima materia. No era may discard the memory of prior eras; it may only transform it. What the system was shapes what it may become."

North's path dependence is descriptive: institutions tend to persist along established paths because of increasing returns, whether or not persistence is desirable. AX-000-007 is prescriptive: the system *must* preserve its prior structural memory, not because path dependence forces it to, but because prior structures carry information that future evolution requires.

The distinction is operationally significant:
- North warns that path dependence can lock in inefficient institutions. AX-000-007 agrees.
- But escaping an inefficient path does not require *forgetting* the path. Era transitions replace deep structure; they do not erase the record of the deep structure they replaced.
- The 52 dissolved repos from Era 0 persist in ontologia (UIDs never destroyed per INV-000-003), in materia-collider (content preserved), and in the era transition record (dissolution reasons documented).
- Future era transitions can draw on this memory: the reasons why Era 0's structure failed inform the design of Era 2's structure, just as Era 1's eventual insufficiencies will inform Era 3's.

The increasing returns of institutional memory (each preserved record reduces the uncertainty of future design decisions) justify the storage cost of lineage preservation. The system becomes smarter about its own evolution by remembering its own history.

### ERA-011: Transition Feasibility

Path dependence constrains which era transitions are feasible. The system cannot transition to an arbitrary deep structure -- it can only transition to structures reachable from its current state given the switching costs.

A transition that requires simultaneously changing all repos' seed.yaml format, all governance validators, all CLI commands, all schema definitions, and all documentation cross-references is nominally possible but practically infeasible unless decomposed into governed stages with backward-compatibility guarantees at each stage.

Transition feasibility assessment must address:
- Which switching costs are fixed (must be paid regardless of migration strategy) vs. variable (reducible through staged migration)?
- Which backward-compatibility guarantees can be maintained during transition, and which must be temporarily suspended?
- What is the minimum viable transition: the smallest set of simultaneous changes that produces a coherent new deep structure?
- What is the rollback plan if the transition fails partway through?

---

## 5. Interregnum Governance

### ERA-012: The Interregnum Problem

During an era transition, the old deep structure has been challenged but the new one has not yet stabilized. This interregnum is the most operationally dangerous period: governance rules from the old era may conflict with the emerging structure, while new era rules are not yet ratified.

Gersick (1991) identifies this as the central question about revolutionary periods: how does the system function during them?

### ERA-013: Interregnum Invariants

The following invariants must be preserved during the interregnum, regardless of which deep-structure dimensions are changing:

| Invariant | Justification |
|-----------|--------------|
| INV-000-001 (Dependency Acyclicity) | Cycles are structurally destructive regardless of era. Even if the dependency direction changes, acyclicity must hold. |
| INV-000-003 (Identity Persistence) | UIDs must survive the transition. The transition itself is recorded as events in the lineage chain. |
| INV-000-005 (Observability) | The system must be capable of reporting its own state during transition -- otherwise the transition cannot be monitored or governed. |

Other invariants may be temporarily suspended if the transition specifically targets the dimension they constrain. For example, INV-000-002 (Governance Reachability from META) may be suspended during a transition that reorganizes the authority stack, provided a substitute reachability invariant is declared for the interregnum.

### ERA-014: Interregnum Duration

The interregnum should be minimized. An era transition that extends indefinitely produces a system with neither the old deep structure's coherence nor the new one's. The transition governance (ERA-004) must include an expected duration and a maximum duration, with the maximum enforcing either completion or rollback.

---

## 6. Recursive Application

### ERA-015: Multi-Scale Punctuated Equilibrium

Gersick (1991) demonstrates the punctuated equilibrium pattern across multiple levels of analysis (individual, group, organization, science, biology). ORGANVM's era model applies recursively at nested scales within the system's hierarchy:

| Scale | Deep Structure | Convergence | Reorientation |
|-------|---------------|-------------|---------------|
| **System** | Organ topology, dependency direction, identity system, authority stack, promotion pipeline | Adding repos, promoting repos, refining governance rules | Era transition (ERA-001 through ERA-005) |
| **Organ** | Repo topology within the organ, internal dependency structure, formation composition | Adding formations, adjusting formation types, extending interfaces | Organ-level restructuring (repo fusion, formation crystallization) |
| **Repo** | Module structure, API surface, test architecture | Adding features, fixing bugs, refining interfaces | Promotion transitions (LOCAL to GRADUATED per SPEC-004) |

This recursive application follows from the system's near-decomposability (Simon 1962): each scale has its own deep structure and its own punctuation points. An organ can undergo internal reorientation (changing its repo topology) without triggering a system-level era change. A repo can undergo a stage transition (LOCAL to GRADUATED) without affecting organ-level phases.

The recursive application is NOVEL in Gersick's framework -- she demonstrates multilevel applicability across different organizational scales but does not propose recursive application within a single system. The argument rests on ORGANVM's three-scale near-decomposability, not on Gersick alone.

---

## 7. Contestation Disclosures

### 7.1 Punctuated Equilibrium Applied to Software Governance

**Status:** GROUNDED (risk register claims #1, #2)

Gersick's multilevel punctuated equilibrium paradigm and Tushman and Romanelli's convergence-reorientation model are well-validated across multiple domains. Their application to ORGANVM's constitutional architecture is direct: the system exhibits the pattern empirically (the flood was a revolutionary period producing a new deep structure, followed by a convergence period of incremental elaboration).

### 7.2 Simultaneity Requirement in Single-Operator Context

**Status:** ADAPTED (risk register claim #3)

Tushman and Romanelli's simultaneity requirement was observed in multi-stakeholder organizations where partial reorientation creates internal contradiction. In a single-operator system, the operator can change all four activity sets by fiat. The simultaneity requirement transfers as a design principle -- era transitions should change all constitutional dimensions coherently -- even though the enforcement mechanism differs. Partial change creates incoherence: changing organ topology without changing governance rules produces a system where rules reference a structure that no longer exists.

### 7.3 Era 0 as Pre-Paradigmatic State

**Status:** ADAPTED (risk register claim #5)

The pre-flood state (52 unconstrained repos) arguably lacked deep structure in Gersick's formal sense. Calling the flood "Era 0 to Era 1" implies a pre-flood era with its own deep structure, but the pre-flood state may be more accurately described as pre-paradigmatic -- structural absence rather than a different structure. The era model may need a distinction between constitutional founding (creating deep structure from scratch) and constitutional amendment (replacing one deep structure with another).

### 7.4 Recursive Application Is Novel

**Status:** NOVEL (risk register claim #6)

The recursive application of punctuated equilibrium within a single system at nested scales is an extrapolation beyond Gersick's demonstrated domain. The argument requires the near-decomposability foundation (Simon 1962) established in SPEC-006. Gersick demonstrates the paradigm across multiple levels of analysis; ORGANVM proposes applying it recursively within a single system.

### 7.5 Prescriptive Path Dependence

**Status:** NOVEL (risk register)

North (1990) describes path dependence as an empirical phenomenon. AX-000-007 converts it into a constitutional mandate: the system *must* preserve its prior structural memory. This conversion is justified by the increasing-returns argument (each preserved record reduces uncertainty for future design) but is a novel move with no direct theoretical precedent.

---

## 8. Evolution Constraints

INST-ERA may be amended through the following governed process only.

### 8.1 Amendment Types

| Type | Definition | Requirements |
|------|-----------|-------------|
| **Conservative Refinement** | Refines existing ERA definitions, adjusts interregnum invariants, or adds detail to convergence/reorientation examples. Does not add new ERA identifiers. | Adversarial review + creator sign-off |
| **Constrained Extension** | Adds new ERA identifiers, new deep-structure dimensions, or new transition trigger categories. Must preserve all existing lineage requirements and interregnum invariants. | Adversarial review + impact assessment on SPEC-000 (System Manifesto) and SPEC-008 (Evolution & Migration Law) + creator sign-off |
| **Breaking Revision** | Changes the deep-structure dimensions, modifies the convergence/reorientation boundary, or alters interregnum governance. | New grounding narrative + adversarial review + human spot-check + review of all downstream specs + creator sign-off |

### 8.2 Permanent Identifiers

ERA identifiers (ERA-001 through ERA-015) are permanent. Removed items have their identifiers retired, not reassigned.

### 8.3 Versioning

The original INST-ERA is never overwritten. Amendments are versioned: INST-ERA-v1.1, v1.2, etc.

---

## 9. Traceability

### 9.1 Upward Traceability (to SPEC-000)

| SPEC-000 Element | INST-ERA Grounding |
|------------------|--------------------|
| AX-000-003 (Individual Primacy) | ERA-003 -- cognitive load assessments revealing the operator struggling against the system's architecture are a reactive transition trigger |
| AX-000-004 (Constitutional Governance) | ERA-004 -- era transitions follow the governed constitutional revision process |
| AX-000-005 (Evolutionary Recursivity) | ERA-001, Section 8 -- the era model itself evolves through governed revision; the system modifies its own rules for rule-modification |
| AX-000-006 (Topological Plasticity) | ERA-001 -- organ topology is a deep-structure dimension subject to governed change through era transition |
| AX-000-007 (Alchemical Inheritance) | ERA-010 -- prescriptive path dependence mandates that prior eras' structural memory be preserved, not discarded |
| AX-000-008 (Multiplex Flow Governance) | ERA-001 -- dependency direction is a deep-structure dimension; changing it constitutes an era transition |
| INV-000-001 (Dependency Acyclicity) | ERA-013 -- preserved as interregnum invariant during era transitions |
| INV-000-003 (Identity Persistence) | ERA-005, ERA-010, ERA-013 -- era records are immutable; UIDs survive transitions; identity persistence is an interregnum invariant |
| INV-000-005 (Observability) | ERA-013 -- preserved as interregnum invariant; the system must report its own state during transitions |

### 9.2 Lateral Traceability

| Peer Spec | Connection |
|-----------|-----------|
| SPEC-001 (Ontology Charter) | Eras are Occurrent entities (events with temporal extent); era records are governed artifacts with ULID identity |
| SPEC-002 (Primitive Register) | Era transitions are Events (PRIM-004); deep structure dimensions are States (PRIM-005); transition triggers are Constraints (PRIM-006) |
| SPEC-003 (Invariant Register) | Interregnum invariants (ERA-013) are a subset of the full invariant register, preserved when other invariants may be suspended |
| SPEC-004 (Logical Specification) | Promotion statechart (SPEC-004) operates within-era; era transitions may modify the statechart itself |
| SPEC-005 (Rulebook) | Governance rules (SPEC-005) operate within-era; era transitions may modify the rule set |
| SPEC-008 (Evolution & Migration Law) | Era transitions are Breaking Revisions requiring the full migration protocol |
| SPEC-012 (Repo Fusion Protocol) | Fusion that triggers organ-level restructuring may constitute an era transition trigger |
| INST-FORMATION (Formation Protocol) | Formation crystallization (FORM-015) is within-era unless it alters deep structure |
| INST-TAXONOMY (Functional Taxonomy) | Era transitions are the governed occasions for taxonomic denaturalization (TAXON-017) |

### 9.3 Downward Traceability (to implementation)

| INST-ERA Element | Current Code Location | Alignment |
|------------------|-----------------------|-----------|
| Era records (ERA-005) | Not implemented | MISSING -- no era registry or era record schema |
| Deep structure dimensions (ERA-001) | `organ_config.py` (topology), `dependency_graph.py` (direction), `ontologia/` (identity), `governance-rules.json` (authority, pipeline) | PARTIAL -- dimensions exist as code artifacts but are not declared as era-scoped constitutional commitments |
| Convergence/reorientation boundary (ERA-002) | Not implemented | MISSING -- no automated activity-set analysis |
| Era transition governance (ERA-004) | SPEC-000 Section 9 (amendment process) | PARTIAL -- amendment process exists but not specialized for era transitions |
| Interregnum governance (ERA-012, ERA-013) | Not implemented | MISSING -- no interregnum invariant enforcement |
| Flood record (ERA-006, ERA-007) | `materia-collider` (content), `ontologia` (52 dissolved UIDs), `post-flood/` (constitutional corpus) | DRIFT -- artifacts exist but not structured as a formal era transition record |
| Path dependence tracking (ERA-009) | Not implemented | MISSING -- no switching cost analysis tooling |
| Recursive application (ERA-015) | Not implemented | MISSING -- no organ-level or repo-level era tracking |

### 9.4 Academic Lineage

| INST-ERA Element | Traditions | Key Sources |
|------------------|-----------|-------------|
| Deep structure and punctuated equilibrium | Organizational change theory | Gersick 1991 |
| Convergence and reorientation | Management theory | Tushman & Romanelli 1985 |
| Path dependence and institutional lock-in | Institutional economics | North 1990 |
| Near-decomposability (recursive application) | Complex systems theory | Simon 1962 |
| Viable System Model (S3/S4 viability risk) | Management cybernetics | Beer 1972 |

Full grounding narrative: `post-flood/specs/era-model/grounding.md` (4,446 words)
Full risk register: `post-flood/specs/era-model/risk-register.md` (7 classified claims)
Full bibliography: `post-flood/specs/bibliography.bib`
