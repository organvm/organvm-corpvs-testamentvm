# INST — Index Nominum

**Status:** LAW BUILT · census pending
**Created:** 2026-06-24
**Authority:** META — System-wide reference + governance instrument
**Purpose:** Registry of all named entities — *and the law that governs their naming.*
**Enforcement instrument:** `NOMENCLATOR` (`limen/scripts/nomenclator.py`), reading `limen/spec/index-nominum/canon.yaml`.

> *Index Nominum* — the classical index of names. Third of the four-part scholarly apparatus. Unlike
> its siblings, it is not only a reference instrument: it is also a **governance instrument**. It has
> two faces — the **Canon** (the law a name must obey) and the **Census** (the roll of names that
> exist) — and is kept by the **Nomenclator**, the official of names.
>
> **Nomenclator vs Censor.** The Roman *censor* did two jobs: the census *and* the *regimen morum*
> (conduct). In this estate those are two distinct organs: **NOMENCLATOR** governs *names* (this
> index); **CENSOR** (the insights→actions institution, `limen/scripts/censor.py`) governs *conduct*.
> Keeping them apart was the Index Nominum's first ruling — two organs had reached for "censor."

### The Four Indices

| Index | Latin | Purpose | Status |
|-------|-------|---------|--------|
| **Index Rerum Faciendarum** | *Things to be done* | Universal work registry | `INST-INDEX-RERUM-FACIENDARUM.md` |
| **Index Locorum** | *Index of places* | Canonical map of where everything lives | `INST-INDEX-LOCORUM.md` |
| **Index Nominum** | *Index of names* | Registry of named entities + the naming law | **THIS DOCUMENT** (law built; census pending) |
| **Index Rerum** | *Index of things* | Ontological inventory of what exists | IRF-IDX-003 (planned) |

---

## Part I — The Canon (the naming law)

The law every name in the estate must obey. It is machine-readable and **enforced**, not aspirational.
The canonical source lives in the `limen` conductor (where the heartbeat + organ-health + CI live);
this index is its constitutional declaration.

| Artifact | Location | Role |
|----------|----------|------|
| **Canon** (machine) | `limen/spec/index-nominum/canon.yaml` | substitutions, forbidden set, morphology grammar, token vocabulary — the single source the Nomenclator reads (derive-never-pin) |
| **Charter** (prose) | `limen/NAMING.md` | the orthography canon with worked examples |
| **Census seed** | `limen/spec/index-nominum/roll.yaml` | the roll of canonical names (this index's Part II, in nuce) |
| **NOMENCLATOR** (enforcer) | `limen/scripts/nomenclator.py` | marks any name that breaks canon; wired as CI gate + heartbeat organ (`LIMEN_NOMENCLATOR`) + organ-health rung |

### The five layers

The institution unifies naming knowledge currently smeared across the estate. Layer one is in-canon
and enforced; the rest are convergence targets.

| Layer | Governs | Status | Converge from |
|-------|---------|--------|---------------|
| **Orthographia** | letterforms — `U→V`, `J→I`, `W→VV`, `QU→QV`; the forbidden set | ✅ in canon + enforced | `limen/NAMING.md` |
| **Morphologia** | structure `<essence>--<function>[-<cadence>]` + Latin token vocabulary | ◻ scattered | `docs/standards/22-essence-function-naming-convention.md` · `organvm/brainstorm-…/03-latin-naming-schema…` |
| **Identitas** | identity math — content-addressed UID, genus–differentia | ◻ scattered | `organvm/system-system--system--monad/system--naming-calculus.md` |
| **Lentes** | semantic naming-chains (substrate × tradition lenses) | ◻ scattered | `sovereign-systems--elevate-align/src/data/aesthetics-vocabulary.ts` |
| **Vox** | editorial voice, frontmatter + tag governance | ◻ scattered | `organvm/editorial-standards/` |

### Registers

- **Classical / Augustan** (default) — `U→V, J→I, W→VV, QU→QV`, AE/OE digraphs, all caps.
- **Archaic / Old Latin** — also `G→C`, `K` before A.
- **Greek-inflected** — `K` over `C`, keep `Y/Z`, `KH/PH/TH` for χ/φ/θ.

The estate already obeys the canon in its repo names (`organvm`, `corpvs`, `specvla`, `avditor-mvndi`).

---

## Part II — The Census (the roll of named entities)

The registry of every named entity. **Status: pending** — the law (Part I) is built; the full census
is the remaining `IRF-IDX-002` work, to be generated (not hand-fabricated) via `IRF-IDX-004`
(`organvm index generate nominum`). Sources below are verified to exist; this section is the schema
the generator fills.

| Section | Source of record | Approx. |
|---------|------------------|---------|
| Organs | `organvm-engine` organ_config.py | 8 (Greek-named) |
| Repositories | `registry-v2.json` (display_name) | ~118 |
| CLI tools | `pyproject.toml [project.scripts]` | 7 |
| Agent personas | Hermeneus `personas.ts` | 2+ |
| Vigiles regimes | `vigiles-aeternae` engine | 22 |
| Watcher orders | `vigiles-aeternae` engine | 8 |
| Specifications | `specs/SPEC-*.md` | 22 |
| Standard Operating Procedures | `praxis-perpetua/standards/` | 57+ |
| Dissertations | `inquiry-log.yaml` | 3 (D-001/002/003) |
| Named protocols | governance docs | Testament · Descent · Membrane · Styx |
| People | governance docs | Anthony (operator/creator) · Chris (the Provost) |
| IRF namespaces | `concordance.md` | 21 |
| Ontologia entities | `~/.organvm/ontologia` | ~1836 |

> **Census builder note:** every entity admitted to the census MUST pass the Nomenclator
> (`python3 limen/scripts/nomenclator.py --check "<name>"`). The canon is the gate; the census is
> what passes through it. Seed entries already validated live in `limen/spec/index-nominum/roll.yaml`.

---

## Provenance

- **2026-06-24** — Index Nominum established as the constitution's naming **law** (Part I): canon +
  NOMENCLATOR enforcer built in `limen` and incorporated here. Advances `IRF-IDX-002` from *planned*
  to *law built; census pending*. The Part II census remains open (`IRF-IDX-002` / `IRF-IDX-004`).
  First ruling: separated NOMENCLATOR (names) from CENSOR (conduct) — a name collision, resolved.
