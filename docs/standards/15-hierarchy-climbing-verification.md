# 15: Hierarchy-Climbing Verification (Falsification Cascade)

**Date:** 2026-04-30
**Status:** ACTIVE — operational protocol for any verification question of the form "is X by design, accidental, or drift?"
**Derived from:** Plan `decoding-design-paths-for-inherited-wand.md` (2026-04-30), IRF-OPS-023 (split-origin audit, 2026-04-30), ADR-013 (seed-yaml schema), ADR-2026-04-20 (topology consolidation movement map)
**Complements:** `10-repository-standards.md` (repo standards), `13-organ-identity-and-placement.md` (placement rules), `INST-INDEX-RERUM-FACIENDARUM.md` (acknowledged-drift register)

---

## 1. Purpose & Scope

When an investigator encounters a configuration question of the form *"is artifact X intentional, or is it drift?"* the temptation is to stop at the first plausible reading. This document specifies a verification protocol that does not stop at plausible — it stops at **mathematically forced**, where the alternative reading is ruled out by a constraint that some layer's schema explicitly enforces.

Typical questions in scope:
- Are these two similarly-named repos canonical-and-variant, or duplicates from accidental fork?
- Is this repo's `public: false` setting design-intent, or a private-by-accident leftover?
- Does this `git remote origin` pointing at `a-organvm/<repo>.git` indicate drift from the `seed.yaml.org` declaration, or is it constitutional post-consolidation reality?
- Is this dependency edge an intentional cross-organ flow, or a back-edge that violates Key Invariant #2?

This protocol does **not** authorize any remediation. It produces a *finding* (one of three terminal states) which feeds into separate ADR/IRF protocols for action.

## 2. The Authority Hierarchy

Six layers in two strata. Observable layers surface drift signatures; declarative layers encode design intent. Mathematical force lives only at declarative layers.

### Observable strata (cannot encode intent)

- **L1: Git remotes** — `git remote -v`. Indicates current physical home.
- **L2: Branch topology** — `git branch -a`, `git log --all --oneline`. Indicates work history.
- **L3: Commit messages and timing** — `git log`. Indicates author intent at the per-commit grain.
- **L4: Repo metadata** — visibility (`gh repo view`), default branch, description. Indicates current GitHub-side state.

### Declarative strata (encode intent)

- **L5: Repo content** — `<organ-dir>/<repo>/seed.yaml`, `<organ-dir>/<repo>/CLAUDE.md`, `<organ-dir>/<repo>/README.md`. Declares the repo's self-understanding of its role.
- **L6: Parent-org declarations** — `registry-v2.json` (single source of truth per Key Invariant #1), `registry/<ORGAN>.json` (per-organ shard), `specs/INST-TAXONOMY.md` (functional-class definitions). Declares the system's understanding of the repo's role.
- **L7: Workspace constitutional** — `CLAUDE.md` Key Invariants, `organ-topology.json`, `ecosystem.yaml`, `governance-rules.json`, `governance-config.yaml`, `INST-INDEX-RERUM-FACIENDARUM.md`. Declares the constitutional structural reality that registry instances are validated against.

Relative authority is fixed by ADR-013: **registry is authoritative over seed.yaml** (seed.yaml is generated from registry by `scripts/generate-seed-yaml.py`). Workspace files sit above registry — they declare the structural defaults registry entries are checked against.

## 3. The Cascade

For each declarative layer, the protocol specifies: which files to read, what schema-level constraints that layer enforces, what alternative readings the layer falsifies, what residual ambiguity (if any) passes upward.

### L5 — Repo content

**Read.**
- `<organ-dir>/<repo>/seed.yaml`
- `<organ-dir>/<repo>/CLAUDE.md`
- `<organ-dir>/<repo>/README.md`
- Schema reference: `docs/adr/013-seed-yaml-schema.md`

**Falsifies.**
- Disjoint `produces` sets referenced by independently-declared third parties → `H_accident-duplication` is impossible. Distinct graph nodes.
- Identical `produces` with no third-party `consumes` distinction → `H_design-twin-canonicals` is impossible at L5. No observable system role distinguishes them.
- Repo `CLAUDE.md` whose stated repository path contradicts both `seed.yaml.org` AND `registry-v2.json` → the drift signature of IRF-OPS-023.

**Residual.** L5 cannot adjudicate when `seed.yaml` files themselves disagree, because seed.yaml is generated; any conflict is an L6 artifact. Climb.

### L6 — Parent-org declarations

**Read.**
- `registry-v2.json`
- `registry/<ORGAN>.json`
- `specs/INST-TAXONOMY.md`

**Schema-validated fields per repo.** `org`, `public`, `tier` (flagship | standard | stub | archive | infrastructure), `promotion_status` (LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED → ARCHIVED), `functional_class`, `functional_class_secondary`, `dependencies`, `revenue_model` (ORGAN-III), `type` (ORGAN-III), `implementation_status`, `ci_workflow`.

**Per-organ.** `public_visibility` (FULLY PUBLIC | MOSTLY PUBLIC | MIXED), `repository_count`, `launch_status`.

**Falsifies.**
- Two repos differ on ≥ 1 schema-validated field AND parent organ's `public_visibility` permits the split AND L5 `produces`/`consumes` show non-overlapping roles → **`H_accident` eliminated**. Registry validation has admitted the difference.
- Two repos identical on those fields AND parent organ is FULLY PUBLIC → **`H_design` eliminated for any private sibling**. The variant cannot be intentional under the organ-level constraint.

**Residual.** L6 cannot resolve cases where registry has been retroactively edited to legitimize a prior accident, or where registry has not yet caught up to a post-consolidation L7 declaration. Climb.

### L7 — Workspace constitutional

**Read.**
- `CLAUDE.md` (Key Invariants)
- `organ-topology.json` — dir → org structural mapping; `_comment` field records consolidation dates.
- `ecosystem.yaml` — per-repo delivery and content channel declarations.
- `governance-rules.json`, `governance-config.yaml` — enforceable rules.
- `INST-INDEX-RERUM-FACIENDARUM.md` — the workspace's own register of acknowledged drift.

**Falsifies.**
- L1 git-remote pattern matches a structural mapping in `organ-topology.json` → the apparent drift is constitutional. `H_accident-drift` eliminated.
- IRF carries an open audit item naming the exact case → **both `H_design` AND `H_accident` eliminated**. The case is in **acknowledged-drift, awaiting policy**.

## 4. Stopping Rule (Mathematical Impossibility Criterion)

The cascade halts when one of these three conditions holds. Otherwise, climb. If after L7 both hypotheses still survive AND no IRF item exists, **open a new IRF item** under `OPS` or `SYS` — do not declare.

| Halt | Layer | Terminal state | Condition |
|------|-------|----------------|-----------|
| **A** | L6 | **by design, registry-conclusive** | Two repos differ on ≥ 1 schema-validated field; parent-organ `public_visibility` permits; produces/consumes non-overlap. |
| **B** | L7 | **by design, workspace-conclusive** | L6 alone insufficient; `organ-topology.json` or CLAUDE.md Key Invariant declares the structural pattern; IRF has no open item against the case. |
| **C** | L7 | **acknowledged drift, awaiting policy** | IRF carries an open item naming the case. Resolution direction is fixed by ADR hierarchy: L7 is always canonical relative to L6. |

## 5. Worked Examples

### Example 1 — Halt A (by design, registry-conclusive)

**Question:** Is the contrast between public `metasystem-master` (ORGAN-II) and private `trade-perpetual-future` (ORGAN-III) intentional?

**L5.** Disjoint `produces` graphs (engine artifacts vs SaaS trading product). No third-party consumes one without the other.

**L6.** Schema-validated differences across five fields:

| Field | metasystem-master | trade-perpetual-future |
|-------|-------------------|------------------------|
| `org` | organvm-ii-poiesis | organvm-iii-ergon |
| `public` | true | false |
| `tier` | flagship | standard |
| `functional_class` | ENGINE | APPLICATION |
| `revenue_model` | (n/a) | subscription |

Parent organs differ on `public_visibility`: ORGAN-II is MOSTLY PUBLIC; ORGAN-III is MIXED (4 private, 18 public). Both visibility settings *license* their respective public/private states.

**Verdict.** Halt A. `H_accident` is inconsistent with five orthogonal schema-validated differences and two organ-level licensing declarations. The split is by design.

### Example 2 — Halt C (acknowledged drift) — THIS CORPUS REPO

**Question:** Is `organvm-corpvs-testamentvm`'s `git remote origin = a-organvm/organvm-corpvs-testamentvm.git` design or drift, given that `registry-v2.json` declares `org: meta-organvm`?

**L1.** `git remote -v` → `a-organvm/organvm-corpvs-testamentvm`.

**L5.** This repo's own CLAUDE.md states `Repo: organvm-corpvs-testamentvm` and `Org: meta-organvm`. L1 ≠ L5.

**L6.** `registry-v2.json` declares `"org": "meta-organvm"`. L6 agrees with L5, disagrees with L1.

**L7.**
- `organ-topology.json` declares `"META": {"dir": "organvm", "registry_key": "META-ORGANVM", "org": "a-organvm", ...}` with `_comment` "Post-consolidation topology — all organs map to single 'organvm' directory, GitHub org 'a-organvm'. 2026-04-21." **L1 agrees with L7. L6 disagrees with L7.**
- IRF-OPS-023 (P2, 2026-04-30) explicitly names this corpus repo: "this corpus repo (`organvm-corpvs-testamentvm`) has the same drift — its own CLAUDE.md says `Repository: meta-organvm/organvm-corpvs-testamentvm` but actual `git remote origin` points at `a-organvm/...`. The IRF row sits in a repo with the pathology it describes."

**Verdict.** Halt C. **Acknowledged drift, awaiting policy.** Resolution direction is `L6 ← L7` (registry should be reconciled to post-consolidation topology), not the reverse. The 119-repo coordination is a campaign requiring policy decisions per IRF-OPS-023; do not act unilaterally.

### Example 3 — Halt B (by design, workspace-conclusive)

**Question** (illustrative): Is a `~/Workspace/4444J99/application-pipeline/` directory tracked under registry key `SIGMA-E` valid, given that registry's `organs` enumeration is ORGAN-I through ORGAN-VII + META-ORGANVM?

**L6.** Registry does carry organ keys `SIGMA-E` and `PERSONAL` (as `4444j99/...`) — but documentation in CLAUDE.md describes only eight organs (I–VII + Meta). L6 alone shows the entries; L6 alone does not prove they are constitutional.

**L7.** `organ-topology.json` declares `"SIGMA_E": {"dir": "4444J99", "registry_key": "SIGMA-E", "org": "4444j99", "label": "sigma"}` and `"LIMINAL": {"dir": "4444J99", "registry_key": "PERSONAL", "org": "4444j99", "label": "liminal"}`. IRF has no open item challenging these. **Halt B** — the extra-organ registry entries are constitutional under post-consolidation topology, even though the eight-organ narrative in repo-level CLAUDE.md predates them.

## 6. Recipes

### L5

```bash
yq '.org, .produces, .consumes' "<organ-dir>/<repo>/seed.yaml"
grep -nE '^Repository:|^Org:|github.com/' "<organ-dir>/<repo>/CLAUDE.md"
```

### L6

```bash
jq -r --arg n "<repo>" '
  .organs[] as $o |
  $o.repositories[]? | select(.name==$n) |
  {organ:$o.name, public_visibility:$o.public_visibility,
   repo:.name, org:.org, public:.public, tier:.tier,
   functional_class:.functional_class,
   functional_class_secondary:.functional_class_secondary,
   promotion_status:.promotion_status,
   revenue_model:.revenue_model, type:.type}
' registry-v2.json
```

### L7

```bash
grep -nE 'Key Invariant|registry-v2.json' CLAUDE.md
jq -r 'to_entries[] | select(.key|test("^[A-Z]"))' organ-topology.json
grep -nE 'IRF-OPS-|split-origin|<repo>' INST-INDEX-RERUM-FACIENDARUM.md
```

## 7. Resolution Direction

When L6 and L7 disagree (Example 2 above), the canonical resolution direction is **always `L6 ← L7`** — registry is updated to match constitutional topology, never the reverse. This follows from ADR-013's principle that L7 declarations are constitutional and from the operational reality that `organ-topology.json` is the post-consolidation movement map (ADR-2026-04-20).

This direction is enforced procedurally by `scripts/v3-registry-reconciliation.py` (registry drift reconciler) and `scripts/generate-seed-yaml.py` (regenerates L5 from L6 — so L5 inherits the corrected L6 automatically).

## 8. When the Cascade Cannot Halt

If after L7 both `H_design` and `H_accident` survive AND no IRF item exists:

1. Do **not** declare. The configuration is genuinely under-determined by current declarations.
2. Open a new IRF item under `OPS` (operational drift) or `SYS` (systemic gap), with title `<repo>/<artifact>: under-determined hierarchy`, capturing the constraints checked and the residual ambiguity.
3. Surface the new IRF item in the next session-close summary so policy can be assigned.

This is the system's mechanism for converting unanswered questions into tracked work, rather than letting them be silently answered by whoever next touches the repo.

## 9. Anti-Patterns

- **Stopping at L4** — repo metadata can never prove design intent; it can only surface drift signatures. Declaring "by design" from L4 alone is unsound.
- **Trusting `seed.yaml` over `registry-v2.json`** — seed.yaml is generated. Treating it as source of truth inverts the ADR-013 authority order.
- **Reconciling L7 → L6** — updating `organ-topology.json` to match registry inverts the constitutional hierarchy. Direction is always `L6 ← L7`.
- **Silently overwriting on disagreement** — if L1 and L6 disagree, check L7 *before* changing either. The disagreement may already be acknowledged drift.
- **Treating "acknowledged drift" as "by accident"** — they are distinct terminal states. Acknowledged drift has a policy queue (IRF); accident has a remediation path (registry edit + commit).

## 10. Cross-References

- ADR-013: seed-yaml schema (`docs/adr/013-seed-yaml-schema.md`)
- ADR-2026-04-20: topology consolidation movement map (`docs/adr/2026-04-20-topology-consolidation-movement-map.md`)
- IRF-OPS-023: split-origin audit (`INST-INDEX-RERUM-FACIENDARUM.md`)
- Plan: `decoding-design-paths-for-inherited-wand.md` (originating methodology)
- Key Invariant #1: registry-v2.json is the single source of truth (corpus `CLAUDE.md`)
- `scripts/v3-registry-reconciliation.py`: registry drift reconciler
- `scripts/generate-seed-yaml.py`: L5 regenerator
