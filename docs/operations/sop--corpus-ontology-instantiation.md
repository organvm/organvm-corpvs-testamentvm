> **Canonical location:** `praxis-perpetua/standards/SOP--corpus-ontology-instantiation.md`. This file is a reference copy retained for local context (drafted in the originating corpus before propagation).

# SOP: Corpus Ontology Instantiation

**Created:** 2026-05-09
**Author:** @4444j99 (AI-conductor model)
**Status:** ACTIVE
**Companions:** [`operational-cadence.md`](./operational-cadence.md), [`key-workflows.md`](./key-workflows.md), [`stranger-test-protocol.md`](./stranger-test-protocol.md)
**Precedent:** Originating instantiation in `meta-organvm/organvm-corpvs-testamentvm` (PR #337) — closed `Symmetry: 0.0 (VACUUM)` for the corpus that hosts the standards mandating logos coverage everywhere else
**Standards implemented:** `docs/standards/14-logos-documentation-layer.md` (inner-tier ontology), `docs/standards/15-three-pure-systems.md` (outer-tier ontology)
**Toolchain:** `python3 scripts/generate-claude-md.py`, `organvm refresh`, `organvm ontologia status`, `gh` CLI, `find`/`grep`

---

> Systematic protocol for bringing any repository in the eight-organ ecosystem into compliance with the inner- and outer-tier ontologies. Closes the `Symmetry: 0.0 (VACUUM)` flag reported by `organvm refresh` for repos that have not yet declared their logos layer or system boundaries.

---

## Table of Contents

1. [Part A: Thesis / Antithesis / Synthesis](#part-a-thesis--antithesis--synthesis)
2. [Part B: The Protocol (Phases 1–5)](#part-b-the-protocol)
3. [Part C: Project Instantiation Template](#part-c-project-instantiation-template)
4. [Part D: Anti-Patterns](#part-d-anti-patterns)
5. [Part E: Verification Battery](#part-e-verification-battery)

---

## Part A: Thesis / Antithesis / Synthesis

### Thesis — What healthy ontology-bearing repositories exhibit

1. **Inner-tier completeness.** All five mandated logos files present and substantive: `telos`, `pragma`, `praxis`, `receptio`, `alchemical-io`. None are placeholder or template-fill.
2. **Outer-tier discipline.** Every non-substrate file belongs to exactly one of CORPUS / ENGINE / SURFACE; vocabulary discipline holds (TELOS/PRAGMA/etc. never leaks into ENGINE or SURFACE classifications).
3. **Bidirectional reception.** `receptio.md` covers both outward reception (how the polis reads the repo) and inward absorption (what the repo absorbs from its contextual universe — sibling repos, scholarly lineages, conversation corpora, external tools).
4. **Pragma anchored in fact.** Each narrative cites concrete data from repo-registry.json, Live System Variables, and on-disk audit; not generic boilerplate.
5. **Recursive self-coherence.** The repo honors the same standards it imposes on others; the ontology describes its own existence without contradiction.

### Antithesis — Structural failure modes common to ontology instantiation

1. **The Empty Compliance.** Five files exist, each three sentences long. Symmetry index reports PRESENT but the corpus is functionally still VACUUM. AI-conductor failure: volume target without quality target.
2. **Vocabulary leakage.** TELOS/PRAGMA/PRAXIS/RECEPTIO terms applied to `scripts/`, `.github/`, or `portfolio-site/` artifacts. Indicates the author confused inner- and outer-tier ontologies — symptom of skipping `15-three-pure-systems.md`.
3. **Forced symmetry / Dream production.** Closing VACUUM by writing fluff produces a Dream (lush narrative, no implementation). Worse than Ghost (high implementation, no narrative) because it contaminates the Symmetry signal — a fake green.
4. **Generic boilerplate.** Five repos with near-identical `telos.md` content. Indicates copy-paste from a template without engaging the specific repo's actual telos. Discoverable by diffing telos files across repos.
5. **Auto-gen template lag.** `docs/logos/` materializes but CLAUDE.md auto-gen still reports VACUUM because `scripts/generate-claude-md.py`'s template hasn't been updated to detect non-empty logos directories. Symptom of fixing the artifact without fixing the detector.
6. **Schema drift.** `seed.yaml` claims schema v1.0 but the repo references v1.2 fields (telos/pragma/praxis/receptio summaries); or vice versa. Indicates schema migration was done by hand without full sweep.
7. **System-boundary dispute.** `_posts/`, `templates/`, or `site-data/` end up classified differently by different agents. Indicates `15-three-pure-systems.md` §5 (Edge Cases) wasn't consulted.

### Synthesis — Universal structural principles

1. **Audit before authoring.** Phase 1 is non-skippable. Without a fact-grounded audit (file count, depth, organ membership, Live System Variables), narratives become fluff and forced symmetry follows.
2. **Order matters: telos → pragma → praxis → receptio → alchemical-io.** Each later file references earlier files; chronological authoring minimizes back-references and forces the author to think through the pipeline.
3. **Substrate-test, then system-test, then form-test.** Classify each file in three stages: is it externally mandated (SUBSTRATE)? If not, which of CORPUS/ENGINE/SURFACE? If CORPUS, which inner form? Skipping stages collapses categories.
4. **Vocabulary discipline is mechanically checkable.** A grep across `scripts/` and `.github/` for inner-tier terms catches vocabulary leakage without manual review. Build it into the SOP, not into the reviewer's intuition.
5. **Self-coherence via own-dogfooding.** A repo that authors a logos layer must demonstrate the logos describes the *real* repo, not an idealized one. The pragma file's distance-to-telos table is the load-bearing artifact for self-coherence.
6. **Cross-AI validation as a smell test.** If a different AI agent reading the new logos files cannot articulate what each form means in the repo's specific context, the narratives are too generic. Optional but recommended.

---

## Part B: The Protocol

### Phase 1 — Audit (Current State)

#### 1.1 Verify standards adoption
Confirm the target repo's `docs/standards/` (or local equivalent) recognizes:
- `14-logos-documentation-layer.md` — inner-tier mandate
- `15-three-pure-systems.md` — outer-tier doctrine

If either is missing, this is a **precondition failure**. Do not proceed; coordinate with the meta corpus to backport the standards. Standards must precede their instantiation.

#### 1.2 Check current logos status
```bash
ls docs/logos/ 2>/dev/null
grep -A1 "Logos Documentation Layer" CLAUDE.md
```

State machine:
| State | Trigger | Next |
|---|---|---|
| **VACUUM** | `docs/logos/` absent OR empty | Phase 2 (full instantiation) |
| **PARTIAL** | some files exist, < 5 mandated | Phase 2 (partial fill — author missing files only) |
| **STALE** | all 5 exist but pragma data is > 1 quarter old | Phase 2 (refresh pass — re-audit, update narratives) |
| **COMPLETE** | all 5 exist, recently authored, substantive | Phase 4 only (verification + cross-AI sanity) |

#### 1.3 Survey the repo's pragma state (data anchors for narratives)

```bash
# Structure
find . -type d \( -name '.git' -o -name 'node_modules' -o -name '__pycache__' \) -prune -o -type d -print | wc -l
find . -type f \( -name '.git/*' \) -prune -o -type f -print | wc -l

# Identity
cat seed.yaml | grep -E "(implementation_status|tier|promotion_status|sprint|organ|repo|org)"

# Registry view (run from corpus host or via MCP)
jq '.repos["<this-repo-name>"]' repo-registry.json 2>/dev/null

# Live System Variables (auto-gen zone)
grep -A20 "Live System Variables" CLAUDE.md
```

Capture: depth distribution, top-level directory inventory, organ membership, current tier, promotion status, dependency edges (`Edges` section of CLAUDE.md auto-gen), live system variable values.

#### 1.4 Classify top-level directories under the three pure systems

For each top-level directory and each root file, assign one of: SUBSTRATE / CORPUS / ENGINE / SURFACE. Use `15-three-pure-systems.md` §4 as the canonical mapping.

Output: a table or short note. If any directory does not fit cleanly, log it as an IRF candidate (per `15-three-pure-systems.md` §5 Edge Cases) and note in the audit, but do not block.

---

### Phase 2 — Instantiation

#### 2.1 Create the directory if absent
```bash
mkdir -p docs/logos
```

#### 2.2 Author the five mandated files in order

Recommended order: **telos → pragma → praxis → receptio → alchemical-io**.

| # | File | Word target | Required sections |
|---|---|---|---|
| 1 | `telos.md` | 500–1500 | The Ideal Form; Theoretical Grounding; Three Pure Systems claim; Inner Forms; Distance to Telos pointer |
| 2 | `pragma.md` | 800–2000 | What Exists Today (depth/file counts); State of Three Pure Systems; State of Eight Organs (or organ-N peers); Distance from Telos table; Notable Pragma Properties; Self-Audit Triggers |
| 3 | `praxis.md` | 800–1500 | Praxis Disposition; Governing Quadrilateral; Active Attack Vectors (each with Gap/Move/Status/Next); Anti-Patterns to Avoid; Recursive Praxis; Cadence; Ordering Discipline; Exit Criteria |
| 4 | `receptio.md` | 1000–2000 | **Two Directions** (outward + inward); Outward subsections; Inward subsections (conversation corpora, fossils, pulse, sibling repos, scholarly lineages, external tools); Discipline of Absorption (provenance/routing/triage); Vacuum Closure note; Ongoing Demand |
| 5 | `alchemical-io.md` | 1000–2000 | Source (7+ input streams); Transmutation (6 stages: Capture, Triage, Distillation, Coagulation, Weaving, Broadcast); Return (4+ output classes); Future Self; Metabolic Cadence; The Repo as Living Metabolism |

**Substantive-content rule:** every section must reference at least one concrete artifact from the §1.3 audit. No section may be all-generic; if you cannot tie a section to specific repo data, that section is a defect signal — do not paper over it.

#### 2.3 Cross-reference weave

Within the five files, link to:
- The two implementing standards (`14-...md`, `15-...md`)
- The `constitution.md` if present
- Sibling-repo names (per CLAUDE.md `Siblings` section in auto-gen)
- IRF entries by ID where the praxis vector is tracked
- The repo's `seed.yaml` (mention schema version explicitly)

---

### Phase 3 — Cross-Reference Weaving Outward

#### 3.1 Update `DIRECTORY.md` (or repo equivalent)
Add a `docs/logos/` section listing the five files with one-line purposes. Bring the `docs/standards/` section up to date if it lags (older repos may list 10/11 only).

#### 3.2 Update `seed.yaml` if schema v1.2+ supported
Per `14-logos-documentation-layer.md` §2.1:
```yaml
logos:
  telos:    "1–2 paragraph machine-readable summary of the dream"
  pragma:   "1–2 paragraph machine-readable summary of current state"
  praxis:   "1–2 paragraph machine-readable summary of attack vectors"
  receptio: "1–2 paragraph machine-readable summary of bidirectional reception"
```
If schema v1.2 not yet supported, defer and open IRF entry under `IRF-DOC` namespace.

#### 3.3 Refresh CLAUDE.md auto-gen zone
```bash
python3 scripts/generate-claude-md.py
# or system-wide:
organvm refresh
```

The Logos Documentation Layer section should now report `Status: PRESENT` with non-zero Symmetry. If it still reports VACUUM after `docs/logos/` has been populated with substantive content, the auto-gen template is reading the wrong signal — open an IRF entry under `IRF-OPS` to fix the template (this is a known failure mode; do not silently work around it).

#### 3.4 Trigger `organvm ontologia` resolution if applicable
```bash
organvm ontologia status
organvm ontologia resolve <repo-name>
```
Confirm the repo's UID and live variables incorporate the new symmetry data.

---

### Phase 4 — Verification

Run the full battery in [Part E](#part-e-verification-battery). Do not advance to Phase 5 until all green.

---

### Phase 5 — Commit & Promotion

#### 5.1 Branching
- Branch name: `claude/logos-instantiation-<repo-short-name>` or sprint-stamped equivalent
- Base: `main`

#### 5.2 Commit message format
```
feat(logos): instantiate logos layer for <repo-name>

Closes Symmetry: 0.0 (VACUUM) status reported in CLAUDE.md auto-gen.
Honors docs/standards/14-logos-documentation-layer.md and
docs/standards/15-three-pure-systems.md.

Five new files in docs/logos/ + DIRECTORY.md cross-reference.
```

#### 5.3 PR description should include
- Summary of what was filled
- Pragma state snapshot (file counts, organ membership) anchoring the narratives
- List of deferred items (e.g., schema v1.2 migration, ENGINE/SURFACE self-descriptions)
- Test plan citing Part E checks

Open as **draft** until cross-AI validation (§E.5) is executed.

#### 5.4 IRF closure
Close any IRF entries this work resolves:
```bash
python3 scripts/check-done-id.py
```

#### 5.5 Promotion through state machine
After review and merge, advance the repo's logos status per `14-logos-documentation-layer.md` §4:

| Repo's promotion_status | Logos requirement after this SOP |
|---|---|
| LOCAL | Scaffolding (this SOP minimum) — done |
| CANDIDATE | Drafts of all 5 files (this SOP exit) — done |
| PUBLIC_PROCESS | Peer-reviewed narratives — schedule review |
| GRADUATED | Fully verified symmetry — Phase 4 must report all green for sustained quarter |

---

## Part C: Project Instantiation Template

### Pre-flight checklist (run before starting)
- [ ] Target repo is checked out and clean (`git status` reports nothing to commit)
- [ ] You are on a fresh branch named per §5.1
- [ ] Standards `14-...md` and `15-...md` are present (in this repo or referenced)
- [ ] `seed.yaml` exists; note its schema version
- [ ] CLAUDE.md auto-gen zone reports current Symmetry status (record before-state)
- [ ] Access to `python3 scripts/` invocations confirmed
- [ ] You have read this SOP end-to-end

### Audit data capture template (for §1.3)
Save to a scratch file (not committed) for use across all five narratives:
```
Repo: <name>
Org: <github-org>
Organ: <I/II/III/IV/V/VI/VII/Meta>
Tier: <flagship/standard/stub/archive>
promotion_status: <LOCAL/CANDIDATE/PUBLIC_PROCESS/GRADUATED>
implementation_status: <PRODUCTION/INCUBATING/etc.>
last_validated: <date>

Structure:
  total_dirs: <N>  total_files: <N>  max_depth: <N>
  top-level dirs: [<list>]

Live System Variables (excerpt):
  active_repos: <N>
  ci_workflows: <N>
  published_essays: <N>
  ...

Edges:
  Produces: <list>
  Consumes: <list>

Siblings: <list>

Active Directives applicable: <count>
```

### Per-narrative authoring template
Each of the five files starts with:
```markdown
# <Form> — `<org>/<repo>`

> *<Greek meaning>. <One-line form definition per 14-logos-documentation-layer.md>*

**Status:** Initial draft (filling the documented vacuum per `14-logos-documentation-layer.md`)
**Date:** <YYYY-MM-DD>
**Counterpart files:** [other four logos files]

---

[Body sections per Part B §2.2 table]
```

### Scaffolding command
If the `organvm` CLI is available, the appendix of `14-logos-documentation-layer.md` provides:
```bash
organvm context logos --scaffold
```
This creates the directory and populates the files with standard prompts. **Do not stop at scaffolding** — the prompts are starting points, not finished narratives. Replace every prompt with substantive content per Part B §2.2.

---

## Part D: Anti-Patterns

| ID | Name | Symptom | Remedy |
|---|---|---|---|
| **AP-LI-1** | Empty Compliance | All 5 files exist but each < 200 words; CLAUDE.md auto-gen flips to PRESENT but content is vacuous | Apply Part B §2.2 word-count and required-sections rules; defer the PR if content cannot be substantive |
| **AP-LI-2** | Vocabulary Leakage | TELOS/PRAGMA/PRAXIS/RECEPTIO terms appear in `scripts/`, `.github/`, or `portfolio-site/` files outside comment headers | Run grep check from §E.3; refactor offending files to use ENGINE/SURFACE vocabulary |
| **AP-LI-3** | Forced Symmetry / Dream | Narratives describe an idealized repo that doesn't match implementation reality (e.g., claims 'extensive testing' for a repo with `repos_with_tests: 0`) | Pragma file MUST cite Live System Variables verbatim; if the data contradicts the narrative, fix the narrative, not the data |
| **AP-LI-4** | Boilerplate Drift | Two repos' `telos.md` files diff to nearly identical content | Each telos must be specific to the repo's actual function; if diff < 30%, redo |
| **AP-LI-5** | Skip Audit | Phase 1 was abbreviated to "I know this repo" intuition | Re-run Phase 1 with file-system queries; intuition fails for the long-tail repos especially |
| **AP-LI-6** | Premature ENGINE/SURFACE Mixing | The PR also adds `scripts/X.py` or `.github/workflows/Y.yml` | Split the PR; this SOP produces only CORPUS-typed artifacts (per `15-three-pure-systems.md` Demand 4) |
| **AP-LI-7** | Auto-gen Template Lag | `docs/logos/` populated but CLAUDE.md still reports VACUUM | Open IRF entry under `IRF-OPS` to fix `scripts/generate-claude-md.py` template; do not silently work around |

---

## Part E: Verification Battery

### E.1 — File existence
```bash
for f in telos pragma praxis receptio alchemical-io; do
  test -s "docs/logos/${f}.md" || echo "MISSING_OR_EMPTY: $f"
done
```
Expected output: empty (all five present and non-empty).

### E.2 — Cross-reference integrity
```bash
# Extract all relative .md links from logos files; verify each resolves
grep -hoE "\([^)]+\.md\)" docs/logos/*.md | tr -d '()' | sort -u | while read p; do
  test -e "$(dirname docs/logos/_)/$p" -o -e "$p" || echo "BROKEN: $p"
done
```
Expected output: empty.

### E.3 — Vocabulary discipline
```bash
# Inner-tier vocabulary should not appear inside ENGINE or SURFACE territories
grep -rEn "\b(telos|pragma|praxis|receptio|alchemical-io)\b" \
  scripts/ templates/ .github/ .github-template/ portfolio-site/ _posts/ 2>/dev/null \
  | grep -vE "(^[^:]+:[^:]+:#|^[^:]+:[^:]+:--)" | head
```
Expected output: empty (or only comment-header acknowledgements). Hits in code or YAML keys are violations.

### E.4 — Symmetry index after auto-gen refresh
```bash
python3 scripts/generate-claude-md.py
grep -A1 "Logos Documentation Layer" CLAUDE.md
```
Expected:
- Status: `PRESENT` (or equivalent non-VACUUM marker)
- Symmetry: `> 0.0`

### E.5 — Cross-AI sanity check (recommended)
Run a second-agent read-through (Codex, Gemini, GitHub Copilot CLI):
```bash
# Example: redirect a different agent to summarize each file
gh copilot suggest "Summarize the telos of this repo from docs/logos/telos.md in 50 words"
```
Significant disagreement on what each form means in this repo's specific context indicates the narratives are too generic — return to Phase 2.

### E.6 — Three-pure-systems compliance (when applicable)
If the repo has authored its own classification under `15-three-pure-systems.md`:
```bash
# Confirm CORPUS files only live in CORPUS-territory paths
# (placeholder for future generator from scripts/generate-system-manifests.py)
```

### E.7 — IRF surface
```bash
python3 scripts/check-done-id.py
```
Confirms no IRF entries are being closed or opened spuriously by this SOP run.

---

## Maintenance

This SOP is a CORPUS / PRAXIS / sops artifact in the originating repo. Revisions are governed by the standards it implements:
- If `14-logos-documentation-layer.md` changes (e.g., a sixth mandated file is added), update Part B §2.2 word/section table and Part E §E.1 enumeration
- If `15-three-pure-systems.md` changes (e.g., a fourth pure system is recognized), update Phase 1.4 classification logic and Part D §AP-LI-2
- After every five repo applications, sweep Part D for new anti-patterns observed in the field

The canonical copy migrates to `praxis-perpetua/standards/SOP--corpus-ontology-instantiation.md` once the originating PR (the meta-corpus's instantiation) is merged. Subsequent revisions edit the canonical copy and propagate via library sync, not this local copy.
