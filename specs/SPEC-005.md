# SPEC-005: Rulebook

```
Document ID:      SPEC-005
Title:            Rulebook
Version:          1.1
Status:           RATIFIED (G3 review incorporated)
Layer:            L2 — Constitutional Logic
Authoritative:    Governance Rules
Parent Specs:     SPEC-000 (System Manifesto), SPEC-003 (Invariant Register)
Date Ratified:    2026-03-19
Grounding:        post-flood/specs/SPEC-005/grounding.md
Risk Register:    post-flood/specs/SPEC-005/risk-register.md
Inventory:        post-flood/specs/SPEC-005/inventory.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. ADICO Decomposition

Every governance dictum in `governance-rules.json` is decomposed into its institutional components following Crawford and Ostrom's institutional grammar (1995). Each statement is parsed into five components: **A** (Attribute -- who is bound), **D** (Deontic -- MUST/MUST NOT/MAY), **I** (aIm -- the required action), **C** (Condition -- activation context), and **O** (Or-else -- consequence of non-compliance).

SPEC-005 mandates explicit Or-else for all rules. A statement with A-D-I-C but no O is a *norm* (Crawford & Ostrom 1995), not a *rule*. Norms depend on voluntary compliance. Rules carry formal sanctions. ORGANVM's governance must be constituted by rules, not norms.

### 1.1 Axioms

#### RULE-001: DAG Invariant (derives from AX-000-004, AX-000-008)

| Component | Content |
|-----------|---------|
| **A** | Any repository in the system (all organs including META) |
| **D** | MUST NOT |
| **I** | Create a dependency cycle in the inter-organ dependency graph |
| **C** | Always -- applies to every dependency edge declaration |
| **O** | `validate_dag_invariant()` rejects the edge. If manual registry edit bypasses the validator: O(revert_edit) otimes O(remove_violating_edge) otimes O(escalate_to_constitutional_review) |

**Classification:** Full ADICO rule. Structurally enforced for normal engine operation. Manual-bypass Or-else chain added by SPEC-005.

#### RULE-002: Epistemic Membranes (derives from AX-000-004, AX-000-008)

| Component | Content |
|-----------|---------|
| **A** | Any repository |
| **D** | MUST NOT |
| **I** | Have undeclared cross-organ data flow (imports, shared databases, implicit coupling) |
| **C** | For all inter-organ interactions |
| **O** | O(declare_edge_in_seed_yaml) otimes O(remove_undeclared_coupling) otimes O(flag_for_governance_review_and_block_promotion) |

**Classification:** Elevated from norm (ADIC) to rule (ADICO). The Or-else chain provides a remediation path: first declare the flow, then remove it if undeclarable, then block promotion if neither action is taken.

#### RULE-003: TTL Eviction (derives from AX-000-004)

| Component | Content |
|-----------|---------|
| **A** | Every repository (general); INCUBATOR repos (specific) |
| **D** | MUST |
| **I** | Show activity within 90 days (general); graduate to LOCAL or archive within 14 days (specific INCUBATOR) |
| **C** | Always -- continuous monitoring (see SPEC-004 TIMED-001, TIMED-003) |
| **O** | General: O(show_activity) otimes O(respond_to_staleness_warning_within_30_days) otimes O(auto_archive_with_governance_flag). INCUBATOR: O(graduate_to_LOCAL) otimes O(archive_with_ttl_flag) |

**Classification:** Elevated from norm to rule. Two-stage Or-else with explicit time bounds. The 30-day response window (SPEC-004 TIMED-003) operationalizes the escalation.

#### RULE-004: Registry Coherence (derives from AX-000-004)

| Component | Content |
|-----------|---------|
| **A** | Every repository entry in repo-registry.json |
| **D** | MUST |
| **I** | Appear in exactly one organ, have non-empty name, be counted correctly in repository_count |
| **C** | On every registry operation (load, save, update) |
| **O** | O(correct_malformation) otimes O(reject_write_with_validation_error) otimes O(save_registry_refuses_write -- 50-repo corruption guard) |

**Classification:** The most structurally enforced axiom. `save_registry()` refuses to write fewer than 50 repos (corruption guard). Validation rejects malformed entries. SPEC-005 adds the explicit escalation chain.

#### RULE-005: Organ Placement (derives from AX-000-004, AX-000-005)

| Component | Content |
|-----------|---------|
| **A** | Every non-archived repository |
| **D** | MUST |
| **I** | Satisfy its organ's inclusion criteria and not trigger exclusion criteria. Revenue-generating repos belong in ORGAN-III. Orchestration repos belong in ORGAN-IV. |
| **C** | On placement and on every governance audit |
| **O** | O(reassign_to_correct_organ) otimes O(justify_placement_with_documented_exception) otimes O(flag_misplacement_as_critical_audit_finding) |

**Classification:** Elevated from norm to rule. The Or-else provides a correction path before escalation.

### 1.2 Organ Dictums

#### RULE-006: Theoria Purity (OD-I)

| Component | Content |
|-----------|---------|
| **A** | Any ORGAN-I repository |
| **D** | MUST NOT |
| **I** | Depend on ORGAN-II or ORGAN-III |
| **C** | Always -- applies to every dependency declaration |
| **O** | O(remove_forbidden_dependency) otimes O(relocate_repo_to_correct_organ) otimes O(block_promotion_and_flag_critical) |

#### RULE-007: Poiesis Derivation (OD-II)

| Component | Content |
|-----------|---------|
| **A** | Any ORGAN-II repository |
| **D** | MUST NOT |
| **I** | Depend on ORGAN-III |
| **C** | Always |
| **O** | O(remove_forbidden_dependency) otimes O(relocate_repo_to_ORGAN-III) otimes O(block_promotion_and_flag_critical) |

#### RULE-008: Ergon Factory Gate (OD-III)

| Component | Content |
|-----------|---------|
| **A** | Every non-archived ORGAN-III repository |
| **D** | MUST |
| **I** | Declare a revenue_model AND have CI configured |
| **C** | Before promotion beyond CANDIDATE |
| **O** | O(configure_ci_and_declare_revenue_model) otimes O(request_organ_reassignment_with_justification) otimes O(demote_to_LOCAL_with_governance_flag) |

#### RULE-009: Taxis Orchestration (OD-IV)

| Component | Content |
|-----------|---------|
| **A** | Any ORGAN-IV repository |
| **D** | MUST NOT |
| **I** | Contain domain logic belonging to ORGAN-I, ORGAN-II, or ORGAN-III |
| **C** | Always |
| **O** | O(extract_domain_logic_to_correct_organ) otimes O(document_exception_with_architectural_justification) otimes O(flag_as_warning_and_schedule_refactor) |

#### RULE-010: Logos Write Scope (OD-V)

| Component | Content |
|-----------|---------|
| **A** | Any ORGAN-V repository |
| **D** | MUST |
| **I** | Produce only to its own domain. seed.yaml produces edges must target ORGAN-V. |
| **C** | Always |
| **O** | O(remove_out-of-scope_produces_edge) otimes O(relocate_production_to_correct_organ) otimes O(block_promotion_and_flag_write_scope_violation) |

#### RULE-011: Koinonia Community (OD-VI)

| Component | Content |
|-----------|---------|
| **A** | Any ORGAN-VI repository |
| **D** | MUST |
| **I** | Receive from products via declared event edges |
| **C** | For all product-community interactions |
| **O** | O(declare_event_edge_in_seed_yaml) otimes O(document_alternative_community_channel) otimes O(flag_as_warning_in_audit) |

#### RULE-012: Kerygma Consumer (OD-VII)

| Component | Content |
|-----------|---------|
| **A** | Any ORGAN-VII repository |
| **D** | MUST NOT |
| **I** | Have produces edges in seed.yaml -- ORGAN-VII generates no original domain content |
| **C** | Always |
| **O** | O(remove_produces_edge) otimes O(relocate_content_production_to_source_organ) otimes O(block_promotion_and_flag_critical) |

#### RULE-013: Meta Governance (OD-META)

| Component | Content |
|-----------|---------|
| **A** | Any META-ORGANVM repository |
| **D** | MUST |
| **I** | Serve the structural substrate function -- changes propagate system-wide |
| **C** | Always |
| **O** | O(verify_system_wide_impact_before_merge) otimes O(require_adversarial_review_for_breaking_changes) otimes O(block_merge_pending_constitutional_review) |

### 1.3 Repo Rules

#### RULE-014: Seed Contract Mandate (RR-1)

| Component | Content |
|-----------|---------|
| **A** | Every non-archived repository |
| **D** | MUST |
| **I** | Have a seed.yaml declaring organ membership, tier, and produces/consumes edges |
| **C** | Always |
| **O** | O(create_seed_yaml) otimes O(register_in_LIMINAL_pending_placement) otimes O(flag_ungoverned_and_block_promotion) |

#### RULE-015: Single Responsibility (RR-2)

| Component | Content |
|-----------|---------|
| **A** | Every repository |
| **D** | SHOULD |
| **I** | Have a single, well-defined responsibility. Monoliths should be decomposed; micro-repos should be consolidated. |
| **C** | On governance audit |
| **O** | O(document_responsibility_boundary) otimes O(schedule_decomposition_or_consolidation) otimes O(flag_as_info_in_audit) |

**Note:** Deontic is SHOULD (recommendation), not MUST (obligation). This is a norm by design -- single responsibility is a judgment call, not a machine-checkable property. The Or-else reflects the softer deontic force.

#### RULE-016: Event Handshake (RR-3)

| Component | Content |
|-----------|---------|
| **A** | Repos that declare event subscriptions or productions in seed.yaml |
| **D** | MUST |
| **I** | Reference events that exist in the event catalog. No orphaned event edges. |
| **C** | On seed validation |
| **O** | O(add_event_to_catalog) otimes O(remove_orphaned_edge) otimes O(flag_as_warning_and_block_promotion) |

#### RULE-017: README Mandate (RR-4)

| Component | Content |
|-----------|---------|
| **A** | Every non-archived repository |
| **D** | MUST |
| **I** | Have documentation. documentation_status must not be EMPTY or missing. |
| **C** | Always |
| **O** | O(create_README) otimes O(mark_documentation_status_DRAFT) otimes O(flag_as_critical_audit_finding) |

#### RULE-018: Promotion Integrity (RR-5)

| Component | Content |
|-----------|---------|
| **A** | Every repository |
| **D** | MUST |
| **I** | Have a valid promotion_status from the state machine. No invented states, no skipped transitions. |
| **C** | On every registry operation |
| **O** | O(correct_to_valid_state) otimes O(roll_back_to_last_valid_state) otimes O(flag_as_critical_and_freeze_repo) |

---

## 2. Rule Classification

Every rule from Section 1 is classified according to Ostrom's seven functional rule types (2005). A single rule may serve multiple functional roles. Each classification carries a TYPE identifier.

### TYPE-001: Position Rules

Position rules define roles and positions within the institutional structure.

| Rule | Position Defined | Coverage |
|------|-----------------|----------|
| RULE-005 (Organ Placement) | Organ membership -- which organ a repo occupies | Well-specified |
| RULE-014 (Seed Contract) | Tier assignment (flagship, standard, infrastructure) via seed.yaml | Well-specified |
| RULE-008 (Factory Gate) | Commercial product status within ORGAN-III | Well-specified |
| RULE-009 (Taxis Orchestration) | Orchestrator role for ORGAN-IV | Moderately specified |

**Coverage assessment:** Position rules are well-covered. The registry schema requires organ and tier fields, and `validate_organ_placement()` enforces placement criteria.

### TYPE-002: Boundary Rules

Boundary rules govern entry to and exit from positions.

| Rule | Boundary Governed | Coverage |
|------|------------------|----------|
| RULE-018 (Promotion Integrity) | Entry/exit criteria for all promotion states | Well-specified (SPEC-004 statechart) |
| RULE-003 (TTL Eviction) | Exit from INCUBATOR (14-day), exit from active status (90-day) | Well-specified |
| RULE-005 (Organ Placement) | Entry criteria for organ membership | Well-specified |
| RULE-008 (Factory Gate) | Entry criteria for PUBLIC_PROCESS in ORGAN-III | Well-specified |

**Coverage assessment:** Boundary rules are the strongest category. The promotion state machine (SPEC-004), guard conditions, and TTL constraints provide structural enforcement.

### TYPE-003: Choice Rules

Choice rules determine what actions are available at each position.

| Rule | Choice Governed | Coverage |
|------|----------------|----------|
| RULE-006 (Theoria Purity) | ORGAN-I repos MAY NOT depend on II or III | Explicit prohibition |
| RULE-007 (Poiesis Derivation) | ORGAN-II repos MAY depend on I, MAY NOT depend on III | Explicit prohibition |
| RULE-010 (Logos Write Scope) | ORGAN-V repos MAY produce only to own domain | Explicit constraint |
| RULE-012 (Kerygma Consumer) | ORGAN-VII repos MAY NOT produce original content | Explicit prohibition |

**Coverage assessment:** Choice rules are specified as prohibitions (what repos MUST NOT do) but not as permissions (what repos MAY do). The system tells organs what is forbidden but does not enumerate what is permitted at each promotion status. This gap means the governance architecture cannot formally distinguish between "permitted but discouraged" and "prohibited."

**Gap:** What operations are available to a LOCAL repo vs. a CANDIDATE repo vs. a PUBLIC_PROCESS repo? These constraints exist implicitly in code but are not declared in `governance-rules.json`.

### TYPE-004: Information Rules

Information rules control visibility and access.

| Rule | Information Governed | Coverage |
|------|---------------------|----------|
| RULE-002 (Epistemic Membranes) | Cross-organ data flow must be declared | Well-specified |
| RULE-001 (DAG Invariant) | Dependency visibility restricted to allowed_edges | Well-specified |
| RULE-013 (Meta Governance) | META changes propagate system-wide -- awareness requirement | Moderately specified |

**Coverage assessment:** Information rules are moderately well-covered through the dependency graph validator and epistemic membrane checks. The gap is in finer-grained access control: whether repos in one organ may read documentation or configuration from another organ is not governed.

### TYPE-005: Aggregation Rules

Aggregation rules specify how individual conditions compose into collective outcomes.

| Rule | Aggregation Governed | Coverage |
|------|---------------------|----------|
| SPEC-004 LOG-005 (CANDIDATE exit) | Three parallel regions compose via conjunction (CI AND platinum AND implementation) | Well-specified |
| Omega scorecard | 17 binary criteria aggregate into system maturity score | Well-specified |
| RULE-004 (Registry Coherence) | Multiple validity checks compose into registry health | Well-specified |

**Coverage assessment:** Explicit aggregation rules are well-defined where they exist, but many governance decisions involve implicit aggregation not yet formalized. For example, "5 warnings and 0 criticals is acceptable" is an implicit severity-weighted aggregation with no formal rule.

### TYPE-006: Payoff Rules

Payoff rules assign costs and benefits to actions and outcomes.

| Rule | Payoff Governed | Coverage |
|------|----------------|----------|
| RULE-008 (Factory Gate) | Revenue model requirement for ORGAN-III | Field exists; no formal cost/benefit calculus |

**Coverage assessment:** Payoff rules are the most under-specified category. The `revenue_model` and `revenue_status` registry fields exist but carry no formal incentive structure. Compliance depends on the operator's governance discipline rather than systematic incentives. This is the most significant institutional design gap.

### TYPE-007: Scope Rules

Scope rules define the range of permissible outcomes.

| Rule | Scope Governed | Coverage |
|------|---------------|----------|
| ARCHIVED terminal state | Once entered, the outcome space is empty -- no transitions out | Well-specified |
| SPEC-000 invariants | Constitutional-level constraints on reachable system states | Well-specified |
| RULE-015 (Single Responsibility) | Defines acceptable structural outcomes for repos | Softly specified (SHOULD, not MUST) |

**Coverage assessment:** Scope rules are partially covered. The terminal ARCHIVED state and constitutional invariants provide hard bounds. Softer scope constraints (acceptable architectural patterns, quality thresholds beyond binary pass/fail) are under-specified.

### Coverage Summary

| Rule Type | Coverage Level | Institutional Maturity |
|-----------|---------------|----------------------|
| Position | Well-covered | High |
| Boundary | Well-covered | High |
| Choice | Under-specified | Low -- prohibitions only, no permissions |
| Information | Moderate | Medium -- dependency-level, not content-level |
| Aggregation | Moderate | Medium -- explicit where defined, implicit elsewhere |
| Payoff | Under-specified | Low -- fields exist, no calculus |
| Scope | Partial | Medium -- hard bounds exist, soft bounds missing |

---

## 3. Violation Handling

Every rule from Section 1 specifies an Or-else chain. This section formalizes the violation handling framework using Governatori and Rotolo's contrary-to-duty obligation chains (2006). The chain operator otimes (`O(a) otimes O(b) otimes O(c)`) reads: "a is obligatory; if a is violated, b becomes obligatory; if b is also violated, c becomes obligatory."

### VIOL-001: Promotion Prerequisite Violation

**Triggered by:** RULE-008 (Factory Gate), SPEC-004 LOG-005 guard failure.
**Context:** A promotion request is filed but prerequisites are not met.

```
O(satisfy_all_prerequisites)
  otimes O(file_waiver_with_justification, deadline: 14 days)
  otimes O(demote_to_LOCAL_with_governance_flag)
```

**Chain semantics:** If prerequisites are missing, the first reparational duty is to file a waiver -- a formal justification requesting a time-limited exemption. The waiver must specify which prerequisite is unmet, why it cannot be met, and a proposed timeline. If no waiver is filed within 14 days, or if a waiver is filed and expires unsatisfied, the terminal obligation is demotion to LOCAL.

**Escape valve:** The waiver mechanism accommodates legitimate exceptions (e.g., a pure documentation corpus that cannot have CI). The default without waiver is demotion, preserving governance discipline.

### VIOL-002: Dependency Acyclicity Violation

**Triggered by:** RULE-001 (DAG Invariant), SPEC-004 TEMP-001 failure.
**Context:** A dependency cycle is detected in the inter-organ graph.

```
O(maintain_acyclic_dependencies)
  otimes O(remove_violating_edge, deadline: immediate)
  otimes O(restructure_cyclic_subgraph, deadline: 7 days)
  otimes O(escalate_to_constitutional_review)
```

**Chain semantics:** Cycles are the most severe governance violation. The first reparational duty is immediate edge removal. If the cycle involves legitimate mutual dependencies irreducible to a single edge, the second duty is architectural restructuring within 7 days. If restructuring fails, constitutional review determines whether the dependency model itself needs amendment.

### VIOL-003: Staleness Eviction Violation

**Triggered by:** RULE-003 (TTL Eviction), SPEC-004 TIMED-003 expiration.
**Context:** A repository exceeds the 90-day inactivity threshold.

```
O(show_activity_within_90_days)
  otimes O(respond_to_staleness_warning, deadline: 30 days)
  otimes O(auto_archive_with_governance_flag)
```

**Chain semantics:** The 90-day threshold triggers a warning. The 30-day reparational window gives the operator time to either update the repo or declare maintenance mode. Expiration without response triggers automatic archival with a governance flag preserved in the audit record.

**INCUBATOR variant:**
```
O(graduate_to_LOCAL_within_14_days)
  otimes O(archive_with_ttl_expiration_flag)
```

No intermediate waiver for INCUBATOR repos -- the 14-day TTL is a hard constitutional constraint.

### VIOL-004: Epistemic Membrane Violation

**Triggered by:** RULE-002 (Epistemic Membranes).
**Context:** Undeclared cross-organ data flow detected.

```
O(no_undeclared_cross_organ_flow)
  otimes O(declare_edge_in_seed_yaml, deadline: 7 days)
  otimes O(remove_undeclared_coupling, deadline: 14 days)
  otimes O(block_promotion_and_flag_critical)
```

**Chain semantics:** Discovery of undeclared coupling triggers a 7-day window to formalize the dependency. If formalization is not possible (the coupling is architecturally unsound), removal is required within 14 days. Failure to act results in promotion blockade and critical audit finding.

### VIOL-005: Registry Coherence Violation

**Triggered by:** RULE-004 (Registry Coherence).
**Context:** Registry validation detects malformed entries, duplicate organ membership, or count mismatches.

```
O(maintain_registry_coherence)
  otimes O(correct_malformation, deadline: immediate)
  otimes O(reject_write_with_validation_error)
  otimes O(save_registry_corruption_guard -- 50-repo minimum)
```

**Chain semantics:** The 50-repo write guard (`save_registry()` refuses writes below threshold) is a structural safety net. Malformed entries are rejected on write. The chain ensures progressive defense: first correct, then reject, then refuse.

### VIOL-006: Ungoverned Component

**Triggered by:** RULE-014 (Seed Contract Mandate).
**Context:** A repository exists in the workspace without seed.yaml.

```
O(every_repo_has_seed_yaml)
  otimes O(create_seed_yaml_with_minimal_declaration, deadline: 7 days)
  otimes O(register_in_LIMINAL_pending_placement, deadline: 14 days)
  otimes O(flag_as_ungoverned_and_exclude_from_system_metrics)
```

**Chain semantics:** Ungoverned components are invisible to the governance apparatus. The chain provides a 7-day window to create the minimal seed contract, a 14-day window for LIMINAL registration, and permanent exclusion from system metrics as the terminal consequence. Exclusion is not deletion -- the repo remains in the workspace but is not counted in system health, omega scorecard, or governance audits.

### VIOL-007: Write Scope Violation

**Triggered by:** RULE-010 (Logos Write Scope), RULE-012 (Kerygma Consumer).
**Context:** An organ produces content outside its constitutional domain.

```
O(produce_only_within_domain)
  otimes O(remove_out_of_scope_produces_edge, deadline: 7 days)
  otimes O(relocate_production_to_source_organ, deadline: 14 days)
  otimes O(block_promotion_and_flag_domain_violation)
```

**Chain semantics:** Write scope violations are structural misplacements. The chain directs correction (remove the edge) before relocation (move the production), with promotion blockade as the terminal consequence.

### Terminal Violations

When the entire obligation chain is exhausted without remediation, the entity enters a **terminal violation state**: archived with a violation flag, governance findings preserved in the audit record, re-activation requiring explicit constitutional-level review. Terminal violations are rare by design -- every chain provides multiple off-ramps. The violation flag ensures that governance history is preserved for future promotion decisions.

---

## 4. Evaluation Engine

The governance rulebook requires an evaluation mechanism. Following Forgy's Rete algorithm (1982), the engine adopts the principle of incremental evaluation: rules are re-evaluated only when relevant working memory changes, not on every audit cycle.

### 4.1 Working Memory

The evaluation engine's working memory consists of:

| Fact Type | Source | Change Frequency |
|-----------|--------|-----------------|
| Registry entries | `repo-registry.json` | On registry update |
| Seed declarations | `seed.yaml` per repo | On seed modification |
| Governance rules | `governance-rules.json` | On constitutional revision |
| Entity states | `ontologia/entities.json` | On entity lifecycle event |
| Promotion history | `ontologia/events.jsonl` | On state transition |
| Clock values | SPEC-004 timed constraints | Continuous (daily tick) |

### 4.2 Match-Resolve-Act Cycle

The evaluation cycle follows the production system pattern:

1. **Match:** Identify all rules whose conditions are satisfied by current working memory. Each RULE-NNN from Section 1 maps to a condition-action pair: the Condition (C) component determines activation; the Aim (I) and Or-else (O) components determine the action.

2. **Resolve:** When multiple rules fire simultaneously, apply conflict resolution:
   - **Specificity priority:** Organ dictums (RULE-006 through RULE-013) take precedence over repo rules (RULE-014 through RULE-018) within their organ scope. Axioms (RULE-001 through RULE-005) take precedence over all.
   - **Recency priority:** Rules triggered by the most recent working memory change fire first.
   - **Constitutional hierarchy:** Constitutional-level rules (axioms) defeat collective-choice rules (dictums) defeat operational rules (repo rules). This implements INV-000-004 (Constitutional Supremacy).

3. **Act:** Execute the action. For violation handling, this means advancing through the obligation chain (Section 3). For guard evaluation, this means computing the guard predicate for the relevant SPEC-004 transition.

### 4.3 Incremental Evaluation

At current scale (~27 rules, ~112 repos), linear evaluation is fast enough. The Rete principle is adopted as an architectural constraint, not a current implementation requirement:

- **On registry change:** Re-evaluate only rules whose Attribute (A) and Condition (C) match the changed entity.
- **On governance rule change:** Re-evaluate all entities against the modified rule.
- **On clock tick:** Re-evaluate only timed constraints (TIMED-001 through TIMED-004) for entities whose clocks have crossed a threshold.

The full alpha/beta network construction is deferred until rule count or entity count makes linear evaluation a performance concern.

### 4.4 Evaluation Output

The evaluation engine produces structured responses, replacing the current binary `(bool, message)` return from `check_transition()`:

```
EvaluationResult = {
  rule_id:           RULE-NNN identifier
  entity:            repo name or UID
  verdict:           SATISFIED | VIOLATED | WAIVED
  primary_violation: description of the unmet condition (if VIOLATED)
  obligation_chain:  the applicable VIOL-NNN chain
  chain_position:    which obligation in the chain is currently active
  deadline:          when the current obligation expires
  remediation_path:  structured guidance for resolution
}
```

---

## 5. Defeasibility

When rule scopes overlap, a priority ordering determines which rule prevails. Defeasibility (Governatori & Rotolo 2006) provides the formal mechanism: specific rules defeat general rules when their scopes intersect.

### 5.1 Priority Hierarchy

The priority ordering follows McGinnis's IAD levels (2011):

| Priority | Level | Examples |
|----------|-------|---------|
| 1 (highest) | Constitutional | Axioms (RULE-001 through RULE-005), SPEC-000 invariants |
| 2 | Organ-constitutional | Organ dictums (RULE-006 through RULE-013) |
| 3 | Operational | Repo rules (RULE-014 through RULE-018) |

Within the same level, specificity determines priority: a rule scoped to a single organ defeats a rule scoped to all organs; a rule scoped to a specific tier defeats a rule scoped to all tiers.

### 5.2 Tier-Based Exemptions

Not all rules apply uniformly across tiers. Defeasibility handles exemptions through explicit defeating rules:

| General Rule | Defeating Condition | Defeated Scope |
|-------------|--------------------|----|
| RULE-008 (Factory Gate: revenue_model required) | `tier = infrastructure AND organ = ORGAN-III` | Infrastructure repos within ORGAN-III are exempt from revenue_model requirement |
| RULE-017 (README Mandate) | `tier = infrastructure AND repo_type = ci_configuration` | CI configuration repos may use minimal README |
| RULE-015 (Single Responsibility) | `tier = flagship` | Flagship repos may have broader responsibility scope |

### 5.3 Waiver Mechanism

When no defeating rule applies but a rule produces an unjust result, the waiver mechanism (VIOL-001) provides a governed exception path:

1. **Filing:** The operator files a waiver citing the specific RULE-NNN, the entity affected, the reason the rule cannot be satisfied, and a proposed resolution timeline.
2. **Review:** Waivers are recorded in `ontologia/events.jsonl` as governance events. Constitutional-level waivers (defeating an axiom) require adversarial review. Operational-level waivers require only operator justification.
3. **Expiration:** Every waiver has a deadline. Expired waivers reinstate the original obligation chain at the next position.
4. **Audit trail:** Waivers are never deleted. They constitute governance evidence (SPEC-002, Section 3.5) and are visible in conformance checking (SPEC-004, Section 4).

### 5.4 Conflict Resolution

When two rules at the same priority level produce contradictory obligations for the same entity:

1. **Specificity wins:** The more specific rule defeats the more general rule.
2. **If equally specific:** The more recent rule (most recently ratified or amended) takes precedence.
3. **If still tied:** The rule with the higher severity (`critical` > `warning` > `info`) takes precedence.
4. **If still tied:** Flag for human governance review. The system does not resolve genuine normative conflicts autonomously.

---

## 6. Contestation Disclosures

### 6.1 The Or-Else Gap Is Empirical, Not Theoretical

**Status:** NOVEL (risk register claim #6)

The finding that most ORGANVM dictums are norms (ADIC) rather than rules (ADICO) is an empirical observation from analyzing `governance-rules.json`, not a theoretical speculation. Any analyst performing the ADICO decomposition on the current dictums would reach the same conclusion. The Or-else chains in Section 1 are SPEC-005's prescriptive response to this descriptive finding.

### 6.2 Rete Algorithm Is Overengineered at Current Scale

**Status:** ADAPTED (risk register claim #1)

The full Rete alpha/beta network was designed for expert systems with hundreds of rules and large working memory. ORGANVM has approximately 27 dictums and 112 repos. The Rete principle (incremental matching) is adopted; the full algorithm is deferred. At current scale, a simplified reactive validator that re-evaluates affected rules on registry change suffices.

### 6.3 Defeasibility Is Simplified

**Status:** ADAPTED (risk register claim #7)

Governatori and Rotolo's full defeasible deontic logic provides formal proof rules for skeptical and credulous inference under rule conflict. SPEC-005 simplifies to priority ordering (constitutional > organ > operational) with specificity as tiebreaker. Full defeasible logic is reserved for future institutional complexity where the simplified ordering produces incorrect results.

---

## 7. Evolution Constraints

SPEC-005 may be amended through the following governed process only. This process is self-contained -- it does not depend on any downstream spec for its authority.

### 7.1 Amendment Types

| Type | Definition | Requirements |
|------|-----------|-------------|
| **Conservative Refinement** | Adds Or-else chains to existing rules, refines existing obligation chains, or adjusts deadlines. Does not add new RULE identifiers. | Adversarial review + creator sign-off |
| **Constrained Extension** | Adds new rules (new RULE-NNN identifiers). Must classify the new rule by Ostrom type and provide a complete ADICO decomposition with explicit Or-else. | Adversarial review + impact assessment on SPEC-004 (Logical Specification) + creator sign-off |
| **Rule Retraction** | Removes a rule by demonstrating it is redundant with remaining rules or no longer applicable. | Adversarial review + migration plan for all entities currently governed by the rule + creator sign-off |
| **Breaking Revision** | Changes the deontic force (MUST to MAY, or vice versa), changes the priority ordering, or modifies the defeasibility framework. | New grounding narrative + adversarial review + human spot-check + review of all downstream specs + creator sign-off |

### 7.2 Permanent Identifiers

RULE identifiers (RULE-001 through RULE-018), TYPE identifiers (TYPE-001 through TYPE-007), and VIOL identifiers (VIOL-001 through VIOL-007) are permanent. Removed items have their identifiers retired, not reassigned.

### 7.3 Versioning

The original SPEC-005 is never overwritten. Amendments are versioned: SPEC-005-v1.1, v1.2, etc.

---

## 8. Traceability

### 8.1 Upward Traceability (to SPEC-000)

| SPEC-000 Element | SPEC-005 Grounding |
|------------------|--------------------|
| AX-000-001 (Ontological Primacy) | RULE-001 -- DAG invariant decomposed into ADICO with structural enforcement |
| AX-000-002 (Organizational Closure) | Section 4 -- evaluation engine is itself a constitutive process specified by system rules |
| AX-000-003 (Individual Primacy) | Section 5.3 -- waiver mechanism preserves individual judgment over mechanical enforcement |
| AX-000-004 (Constitutional Governance) | RULE-001 through RULE-018 -- every dictum decomposed with explicit Or-else |
| AX-000-005 (Evolutionary Recursivity) | Section 7 -- the rulebook itself evolves through governed revision |
| AX-000-007 (Alchemical Inheritance) | Section 3 (Terminal Violations) -- violation flags preserved as governance evidence |
| AX-000-008 (Multiplex Flow Governance) | RULE-002 -- epistemic membrane enforcement across flow types |
| INV-000-001 (Dependency Acyclicity) | RULE-001 -- ADICO decomposition with structural Or-else |
| INV-000-002 (Governance Reachability) | RULE-014 -- seed contract mandate ensures every repo has governance path |
| INV-000-003 (Identity Persistence) | Section 3 -- terminal violations archive but never destroy identity |
| INV-000-004 (Constitutional Supremacy) | Section 4.2 -- constitutional hierarchy in conflict resolution; Section 5.1 -- priority ordering |
| INV-000-005 (Observability) | Section 4.4 -- evaluation output is structured, not boolean |

### 8.2 Lateral Traceability

| Peer Spec | Connection |
|-----------|-----------|
| SPEC-001 (Ontology Charter) | GovernanceObject (SPEC-002 Section 3.4) is the entity class for RULE-NNN objects |
| SPEC-002 (Primitive Register) | Rules are Constraints (PRIM-006) with Entity identity (PRIM-001); violations are Events (PRIM-004) |
| SPEC-003 (Invariant Register) | Invariants formalized as TEMP properties in SPEC-004 are enforced by RULE-NNN chains |
| SPEC-004 (Logical Specification) | Guards in the transitions table reference RULE-NNN conditions; VIOL chains operationalize TEMP property failures |

### 8.3 Downward Traceability (to implementation)

| SPEC-005 Element | Current Code Location | Alignment |
|------------------|-----------------------|-----------|
| ADICO decomposition (Section 1) | `governance-rules.json` dictums section | DRIFT -- rules lack explicit Or-else fields |
| Ostrom classification (Section 2) | Not implemented | MISSING -- no rule-type metadata in governance-rules.json |
| Obligation chains (Section 3) | `governance/state_machine.py` check_transition() | DRIFT -- returns (bool, message), not structured EvaluationResult |
| Evaluation engine (Section 4) | `governance/audit.py` run_audit() | DRIFT -- batch linear evaluation, not incremental reactive |
| Defeasibility (Section 5) | Not implemented | MISSING -- all rules apply uniformly |
| Waiver mechanism (Section 5.3) | Not implemented | MISSING -- no waiver filing or tracking |
| Structured evaluation output (Section 4.4) | `check_transition()` returns (bool, str) | DRIFT -- binary, not structured |

### 8.4 Academic Lineage

| SPEC-005 Element | Traditions | Key Sources |
|------------------|-----------|-------------|
| ADICO decomposition | Institutional grammar | Crawford & Ostrom 1995 |
| Seven rule types | Institutional Analysis and Development | Ostrom 2005 |
| IAD governance levels | Multi-level institutional design | McGinnis 2011 |
| Obligation chains | Contrary-to-duty deontic logic | Governatori & Rotolo 2006 |
| Evaluation engine | Production rule systems | Forgy 1982 |
| Defeasibility | Defeasible deontic logic | Governatori & Rotolo 2006 |

Full grounding narrative: `post-flood/specs/SPEC-005/grounding.md` (4,573 words)
Full risk register: `post-flood/specs/SPEC-005/risk-register.md` (7 classified claims)
Current state inventory: `post-flood/specs/SPEC-005/inventory.md` (4 component assessments)
Full bibliography: `post-flood/specs/bibliography.bib`
