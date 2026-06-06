# SPEC-017: Agent Authority Matrix

```
Document ID:      SPEC-017
Title:            Agent Authority Matrix
Version:          1.0
Status:           RATIFIED
Layer:            L5 — Swarm Governance
Authoritative:    Agent Access Control
Parent Specs:     SPEC-000 (System Manifesto), SPEC-003 (Invariant Register), SPEC-005 (Rulebook)
Date Ratified:    2026-03-19
Grounding:        post-flood/specs/SPEC-017/grounding.md
Risk Register:    post-flood/specs/SPEC-017/risk-register.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. The Authority Gap

An AI agent that can do anything is an agent that can destroy anything. The gap between an agent's capability (what it can technically do -- edit files, modify JSON, invoke CLI commands) and its authority (what it is permitted to do within the governance framework) is the gap SPEC-017 fills.

The threat model is not adversarial. ORGANVM's agents are honest-but-incompetent actors (Anderson 2020) who may hallucinate governance state, lose context mid-session, misapply governance rules, or overwrite protected data through confident incompetence. The authority matrix MUST be mechanically enforced (not advisory), always checked (complete mediation), and designed so that common errors result in denial rather than corruption (fail-safe defaults).

---

## 2. Authority Levels

SPEC-017 defines four authority levels forming a strict partial order. Each level subsumes the permissions of all lower levels.

### AUTH-001: Authority Level Definitions

| Level | Name | Permissions | Characteristic |
|-------|------|------------|---------------|
| **L1** | Read | Query registry, read files, inspect state, run diagnostics, view governance audit results | Observation without mutation |
| **L2** | Propose | All L1 + create branches, draft PRs, write plan files, generate recommendations, file escalation reports | Suggestion without commitment |
| **L3** | Mutate | All L2 + commit code, modify seed.yaml, update registry fields, run tests, execute CI | State change within scope |
| **L4** | Approve | All L3 + authorize promotion transitions, modify governance-rules.json, ratify SPEC amendments, grant/revoke agent authority | Constitutional and governance mutation |

### AUTH-002: Level Assignment by Role

Default authority levels per role (SPEC-013, SWARM-005). The human operator may elevate or restrict authority for specific sessions:

| Role | Default Level | Elevation Conditions | Maximum Level |
|------|--------------|---------------------|--------------|
| `governance-authority` (Human Operator) | L4 | N/A -- inherent | L4 |
| `orchestrator-agent` | L3 | Explicit operator grant for specific L4 operations | L4 (per-operation only) |
| `domain-agent` | L3 | Scope-restricted to declared organ/repo set | L3 |
| `ci-bot` | L1 | May block merges (reactive L3 for specific merge operations) | L1 (+merge-block) |
| `read-only-observer` | L1 | None | L1 |

### AUTH-003: Scope Restriction

Authority levels are always scope-restricted. An agent with L3 (Mutate) authority does not have system-wide mutation permission -- it has mutation permission within its declared session scope:

| Scope Type | Description | Example |
|-----------|-------------|---------|
| **Organ scope** | Authority restricted to repos within specified organs | "L3 for ORGAN-III repos only" |
| **Repo scope** | Authority restricted to specific repositories | "L3 for organvm-engine and schema-definitions" |
| **File scope** | Authority restricted to specific file patterns | "L3 for src/ and tests/ only; L1 for everything else" |
| **Operation scope** | Authority restricted to specific operation types | "L3 for code changes; L1 for governance operations" |

---

## 3. Security Design Principles

SPEC-017 implements six of Saltzer and Schroeder's (1975) eight design principles for protection mechanisms:

### AUTH-004: Least Privilege

Every agent session receives only the permissions needed for its declared scope -- not full system access:

| Session Scope | Granted Permissions | Denied Permissions |
|--------------|--------------------|--------------------|
| "Write tests for ORGAN-III engine module" | L3 code:write for ORGAN-III | governance:promote, registry:write, governance-rules:modify |
| "Conduct governance audit" | L1 governance:audit (read-only) | governance:promote, registry:write, code:write |
| "Promote repo X to PUBLIC_PROCESS" | L3 governance:promote for repo X | governance-rules:modify, constitutional:amend |
| "Review and merge PR #123" | L3 code:merge for specific PR | governance:promote, registry:write beyond PR scope |

### AUTH-005: Complete Mediation

The authority matrix is checked at the point of each governance-mutating operation, not just at session initialization:

1. A session authorized to modify a repo at session start MAY lose that authorization mid-session if another agent promotes the repo (changing its governance tier and required authority)
2. Every mutation operation queries current authority, not cached authorization from session start
3. Authority checks are synchronous -- the operation blocks until authorization is confirmed

### AUTH-006: Fail-Safe Defaults

Access decisions default to denial, not permission:

1. A new agent type (not yet classified in AUTH-002) starts with L1 (Read) access
2. An unrecognized operation (a CLI command not in the known operation set) defaults to denial
3. An ambiguous scope (session scope declaration does not clearly include the target) defaults to denial
4. On authority check failure: the operation is denied, the agent receives a structured denial message (not a silent failure), and the denial is logged in the coordination audit trail

### AUTH-007: Separation of Privilege

Critical operations require multiple authorization factors:

| Operation | Factor 1 | Factor 2 | Rationale |
|-----------|----------|----------|-----------|
| Promote to GRADUATED | Agent execution (criteria met) | Human confirmation | Effectively irreversible; system-wide impact |
| Modify governance-rules.json | Agent proposal | Human approval + adversarial review | Constitutional impact |
| Amend SPEC documents | Agent draft | Human approval + adversarial review | Constitutional authority |
| Delete entity from ontologia | Agent proposal | Human confirmation | INV-000-003 (identity persistence) |
| Modify repo-registry.json (> 5 fields) | Agent execution | Human review before write | Data corruption risk |

### AUTH-008: Economy of Mechanism

The authority matrix itself must be simple enough to audit:

1. Four authority levels (not dozens of fine-grained permissions)
2. Five roles (not a complex role hierarchy)
3. Four scope types (not arbitrary scope expressions)
4. Clear subsumption: L4 > L3 > L2 > L1

Complexity of the authority model is itself a governance risk. A system too complex for the operator to understand is a system the operator cannot govern.

### AUTH-009: Psychological Acceptability

The authority constraints must be comprehensible to both parties:

1. **For the human operator**: The authority matrix is expressible as a simple table (AUTH-002). The operator can understand and modify it without security expertise.
2. **For AI agents**: Authority constraints are injected through CLAUDE.md context in natural language. If the authority rules are incomprehensible to the agent, the agent will violate them through misunderstanding rather than malice.

---

## 4. RBAC Reference Model

SPEC-017 adopts Sandhu et al.'s (1996) RBAC3 reference model: role hierarchies (RBAC1) combined with separation-of-duty constraints (RBAC2).

### AUTH-010: Role Hierarchy (RBAC1)

```
governance-authority (L4)
         |
  orchestrator-agent (L3)
         |
    domain-agent (L3, scope-restricted)
         |
       ci-bot (L1 + merge-block)
         |
  read-only-observer (L1)
```

Senior roles inherit all permissions of junior roles. The human operator inherits all permissions of all subordinate roles. The orchestrator agent inherits domain-agent and ci-bot permissions but not governance-authority permissions (it cannot authorize critical operations unilaterally).

### AUTH-011: Separation-of-Duty Constraints (RBAC2)

**Static Separation of Duty** (SSD): Mutually exclusive role assignments:

| SSD Constraint | Rationale |
|---------------|-----------|
| An agent with `code:write` for a repo MUST NOT simultaneously hold `code:review` for the same repo | No self-review |
| An agent generating a governance recommendation MUST NOT approve the same recommendation | No self-authorization |

**Dynamic Separation of Duty** (DSD): Mutually exclusive role activations within a session:

| DSD Constraint | Rationale |
|---------------|-----------|
| An agent with active `governance:promote` session MUST NOT simultaneously hold `registry:write` session for the same repo | Prevent race conditions during promotion |
| An agent with active `code:write` session MUST NOT simultaneously hold `governance:audit` session for repos it is modifying | Audit must be independent of modification |

**Cardinality Constraints**:

| Constraint | Limit | Rationale |
|-----------|-------|-----------|
| `governance:promote` sessions per repo | Max 1 | Prevent conflicting concurrent promotion attempts |
| `registry:write` sessions system-wide | Max 1 | Prevent concurrent registry corruption |
| `governance-rules:modify` sessions | Max 1 | Constitutional changes must be serialized |

### AUTH-012: Meta-Governance

Who administers RBAC itself? Who can assign agents to roles? Who can modify role permissions?

Meta-governance authority rests exclusively with the human operator (AX-000-003). This is a constitutional constraint, not an RBAC configuration:

1. No agent may modify the authority matrix
2. No agent may elevate its own authority level
3. No agent may assign roles to other agents without operator authorization
4. Authority matrix changes require the same amendment process as other SPEC changes (Section 8)

---

## 5. Integrity Hierarchy (Biba Model)

The Biba integrity model (Anderson 2020) -- "no read down, no write up" -- provides the formal framework for ORGANVM's data integrity hierarchy. High-integrity data must not be writable by low-integrity agents.

### AUTH-013: Integrity Levels

| Integrity Level | Data Classification | Write Authority |
|----------------|-------------------|----------------|
| **Constitutional** (highest) | SPEC-000 through SPEC-017, `archive_original/` | Human operator only; `archive_original/` is read-only for all |
| **Governance** | `governance-rules.json`, `repo-registry.json`, schema definitions | L4 (Approve) with human confirmation |
| **Contractual** | `seed.yaml` files, organ-aesthetic.yaml, taste.yaml | L3 (Mutate) within scope |
| **Operational** | Source code, tests, documentation, CLAUDE.md | L3 (Mutate) within scope |
| **Session** (lowest) | Plan files, session logs, claims registry entries | Any authorized agent |

### AUTH-014: Biba Enforcement Rules

**"No write up"**: A domain agent operating at operational integrity MUST NOT directly modify governance-rules.json (governance integrity) or SPEC documents (constitutional integrity). It must escalate (SPEC-015) to a higher-authority entity.

**"No read down"**: Not enforced in ORGANVM. All agents may read all non-sensitive data regardless of integrity level. The Biba model is applied asymmetrically: write restrictions are enforced; read restrictions are not. This reflects the observability invariant (INV-000-005): restricting reads would reduce system transparency.

### AUTH-015: Protected Files

The following files carry explicit integrity protection. No agent may write to these files without the specified authority:

| File | Integrity Level | Required Authority | Code Guard |
|------|----------------|-------------------|-----------|
| `archive_original/*` | Constitutional | No write access (read-only for all) | N/A -- filesystem permissions |
| SPEC-000 through SPEC-017 | Constitutional | L4 + adversarial review + creator sign-off | Git branch protection |
| `governance-rules.json` | Governance | L4 + human confirmation | Manual review |
| `repo-registry.json` | Governance | L3 with `save_registry()` corruption guard (min 50 repos) | `save_registry()` in `registry/loader.py` |
| `schema-definitions/schemas/*` | Governance | L4 + schema validation | Schema self-validation |
| `seed.yaml` (any repo) | Contractual | L3 within organ scope | Seed validation on write |
| `ontologia/entities.json` | Governance | L3 through ontologia API only (append-only) | Store API enforces append-only |

---

## 6. Immutability Declarations

Certain system artifacts are constitutionally immutable -- they may not be modified by any agent at any authority level.

### AUTH-016: Absolute Immutability

| Artifact | Immutability Type | Rationale |
|----------|------------------|-----------|
| `archive_original/` (post-flood source transcripts) | Absolute -- no modifications by any entity | Source-of-record for constitutional theory (AX-000-007) |
| Entity UIDs in ontologia | Absolute -- no UID may be deleted or reassigned | INV-000-003 (Identity Persistence) |
| SPEC identifiers (SPEC-NNN, AX-NNN, INV-NNN) | Absolute -- retired, never reassigned | Traceability integrity |
| RULE identifiers (RULE-NNN, VIOL-NNN) | Absolute -- retired, never reassigned | SPEC-005 Section 7.2 |

### AUTH-017: Versioned Immutability

These artifacts may not be overwritten but may be versioned (new versions created alongside originals):

| Artifact | Versioning Rule |
|----------|----------------|
| SPEC documents | Amendments create SPEC-NNN-v1.1, v1.2, etc. |
| Governance-rules.json | Changes tracked through git history; no wholesale replacement |
| Registry-v2.json | Changes tracked through git history; `save_registry()` prevents corruption |
| Session transcripts (JSONL) | Append-only; no modification of past entries |

---

## 7. Reference Monitor

Anderson's (2020) reference monitor concept requires three properties for the authority enforcement mechanism:

### AUTH-018: Reference Monitor Properties

| Property | Requirement | ORGANVM Implementation | Status |
|----------|------------|----------------------|--------|
| **Always invoked** | Every governance-mutating operation passes through authority check | Promotion: `state_machine.py`. Claims: `claims.py`. Tool locks: `tool_lock.py`. | PARTIAL -- file edits bypass |
| **Tamper-proof** | Authority matrix cannot be modified by agents subject to it | Code protected by git; no runtime authority modification API | PARTIAL -- agents can edit Python source |
| **Verifiable** | Authority logic is small enough to audit completely | State machine: ~200 lines. Claims: ~150 lines. Tool locks: ~100 lines. | ALIGNED -- total < 500 lines |

### AUTH-019: Reference Monitor Gaps

| Gap | Risk | Mitigation |
|-----|------|-----------|
| Direct file edits bypass authority checks | Agent with filesystem access can edit governance-rules.json directly | `save_registry()` corruption guard; git pre-commit hooks (not yet implemented) |
| Agents can modify authority code | Agent with `code:write` can theoretically edit `state_machine.py` | Git review process; SPEC-013 SWARM-005 role constraints |
| No hardware enforcement | Python-level guards, not OS-level access control | Acceptable at current scale (single operator, trusted environment) |

**Scale warning**: If ORGANVM acquires multiple operators or untrusted agents, code-level enforcement will be insufficient. Hardware-enforced access control, cryptographic audit trails, and formal verification of the reference monitor would become necessary.

---

## 8. Operation Classification

Every operation in ORGANVM is classified by its authority requirement:

### AUTH-020: Operation Authority Matrix

| Operation | Authority Level | Scope Requirement | Notes |
|-----------|----------------|-------------------|-------|
| Read registry | L1 | None | Always permitted for authorized agents |
| Read seed.yaml | L1 | None | Always permitted |
| Read source code | L1 | None | Always permitted (except sensitive paths) |
| Run governance audit | L1 | None | Read-only diagnostic |
| Query organism state | L1 | None | Read-only diagnostic |
| Create branch | L2 | Repo scope | Proposal, no commitment |
| Draft PR | L2 | Repo scope | Proposal, no commitment |
| Write plan file | L2 | Session scope | Plan, not execution |
| File escalation report | L2 | None | SPEC-015 escalation |
| Commit code | L3 | Repo scope | State change |
| Modify seed.yaml | L3 | Repo scope | Contractual change |
| Update registry fields | L3 | Repo scope | Governance state change |
| Run tests | L3 | Repo scope | Resource consumption |
| Execute CI | L3 | Repo scope | Resource consumption |
| Promote LOCAL -> CANDIDATE | L3 | Repo scope | Bounded governance change |
| Promote CANDIDATE -> PUBLIC_PROCESS | L3 | Repo scope | Bounded governance change |
| Promote to GRADUATED | L4 | Repo scope + human confirmation | System-wide impact |
| Modify governance-rules.json | L4 | System scope + human confirmation | Constitutional impact |
| Modify SPEC documents | L4 | System scope + adversarial review + creator sign-off | Constitutional authority |
| Grant/revoke agent authority | L4 | System scope | Meta-governance |
| Archive entity | L3 | Repo scope + human confirmation | Lineage preservation required |
| Modify organ topology | L4 | System scope + constitutional revision | AX-000-006 governed change |

---

## 9. Contestation Disclosures

### 9.1 Biba Without Formal Security Labels

**Status: ADAPTED** (risk register claim #3)

Biba's integrity model was designed for military/government information systems with formal security clearances. ORGANVM's "integrity levels" (AUTH-013) are architectural conventions, not formally labeled classifications. The "no write up" principle applies structurally: a domain agent at operational integrity cannot modify governance-rules.json at governance integrity. But enforcement is through code-level guards, not formal Biba enforcement mechanisms.

### 9.2 Reference Monitor Without Hardware Enforcement

**Status: ADAPTED** (risk register claim #4)

Anderson's (2020) reference monitor assumes a trusted computing base with hardware enforcement. ORGANVM's reference monitor is Python code running without hardware protection. Property (1) always-invoked: satisfied for promotion operations but not for direct file edits. Property (2) tamper-proof: partially satisfied via git review but agents can modify Python source. Property (3) verifiable: satisfied if authority logic remains minimal (< 500 lines).

The gap is manageable at current scale (single operator, trusted development environment, honest-but-incompetent agents). If the threat model evolves, the enforcement mechanism must evolve with it.

---

## 10. Evolution Constraints

SPEC-017 may be amended through the following governed process only.

### 10.1 Amendment Types

| Type | Definition | Requirements |
|------|-----------|-------------|
| **Permission Addition** | Adds new operations to AUTH-020 | Adversarial review + creator sign-off |
| **Role Revision** | Modifies role definitions or hierarchy (AUTH-010) | Impact assessment on all SPEC-013 through SPEC-016 + adversarial review + creator sign-off |
| **Integrity Level Change** | Modifies the integrity hierarchy (AUTH-013) or protected files (AUTH-015) | Demonstration that invariants are preserved + adversarial review + creator sign-off |
| **Immutability Declaration** | Adds or modifies immutability declarations (AUTH-016/017) | New grounding narrative + adversarial review + human spot-check + creator sign-off |

### 10.2 Permanent Identifiers

AUTH identifiers (AUTH-001 through AUTH-020) are permanent. Removed items have their identifiers retired, not reassigned.

### 10.3 Versioning

The original SPEC-017 is never overwritten. Amendments are versioned: SPEC-017-v1.1, v1.2, etc.

---

## 11. Traceability

### 11.1 Upward Traceability (to SPEC-000)

| SPEC-000 Element | SPEC-017 Grounding |
|------------------|--------------------|
| AX-000-003 (Individual Primacy) | AUTH-012 -- meta-governance authority rests exclusively with human operator |
| AX-000-004 (Constitutional Governance) | AUTH-001/020 -- every governance-mutating operation requires appropriate authority |
| AX-000-005 (Evolutionary Recursivity) | Section 10 -- the authority matrix itself evolves through governed amendment |
| AX-000-007 (Alchemical Inheritance) | AUTH-016 -- immutability declarations preserve lineage artifacts |
| INV-000-001 (Dependency Acyclicity) | AUTH-020 -- dependency mutations require L3 authority |
| INV-000-003 (Identity Persistence) | AUTH-016 -- entity UIDs are absolutely immutable |
| INV-000-004 (Constitutional Supremacy) | AUTH-013/014 -- Biba integrity hierarchy enforces constitutional precedence |
| INV-000-005 (Observability) | AUTH-014 -- asymmetric Biba (write-restricted, read-open) preserves observability |

### 11.2 Lateral Traceability

| Peer Spec | Connection |
|-----------|-----------|
| SPEC-003 (Invariant Register) | AUTH-013 integrity levels protect invariant-critical data |
| SPEC-005 (Rulebook) | AUTH-020 operation classification references RULE-NNN enforcement |
| SPEC-013 (Swarm Topology) | Role assignments (SWARM-005) map directly to AUTH-002 authority levels |
| SPEC-014 (Resource Constraints) | Cognitive bias guards (RSRC-004/005/006) complement authority enforcement |
| SPEC-015 (Escalation Policy) | Triage routing (ESCL-002) respects authority level requirements for resolution |
| SPEC-016 (Epistemic Routing) | Source access (EPIS-003) is constrained by authority levels (AUTH-014) |

### 11.3 Downward Traceability (to implementation)

| SPEC-017 Element | Current Code Location | Alignment |
|------------------|-----------------------|-----------|
| Promotion authority checks | `governance/state_machine.py` check_transition() | DRIFT -- checks criteria, not agent authority level |
| Registry corruption guard | `registry/loader.py` save_registry() (50-repo minimum) | ALIGNED |
| Claims registry | `coordination/claims.py` | ALIGNED -- tracks agent claims |
| Tool checkout line | `coordination/tool_lock.py` | ALIGNED -- serializes heavy operations |
| Ontologia append-only store | `ontologia/store.py` | ALIGNED -- structural UID persistence |
| RBAC role hierarchy (AUTH-010) | Not implemented | MISSING |
| Separation-of-duty constraints (AUTH-011) | Not implemented | MISSING |
| Biba integrity enforcement (AUTH-014) | Implicit in code guards | DRIFT -- not formally declared |
| Reference monitor (AUTH-018) | Distributed across state_machine.py, claims.py, tool_lock.py | DRIFT -- not unified |
| Operation authority matrix (AUTH-020) | Not implemented as formal matrix | MISSING |
| Immutability declarations (AUTH-016/017) | Implicit (archive_original in .gitignore; UIDs append-only) | DRIFT |

### 11.4 Academic Lineage

| SPEC-017 Element | Traditions | Key Sources |
|------------------|-----------|-------------|
| Security design principles (AUTH-004 through AUTH-009) | Computer security | Saltzer & Schroeder 1975 |
| RBAC model (AUTH-010/011) | Access control | Sandhu et al. 1996 |
| Biba integrity model (AUTH-013/014) | Security engineering | Anderson 2020 |
| Reference monitor (AUTH-018/019) | Security engineering | Anderson 2020 |
| Honest-but-incompetent threat model | Security engineering | Anderson 2020 |

Full grounding narrative: `post-flood/specs/SPEC-017/grounding.md` (3,900+ words)
Full risk register: `post-flood/specs/SPEC-017/risk-register.md` (6 classified claims)
Full bibliography: `post-flood/specs/bibliography.bib`
