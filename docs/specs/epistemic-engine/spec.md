# Feature Specification: Epistemic Engine (Theoretical, Layer-1)

**Created:** 2026-05-19
**Status:** RATIFIED for design handoff
**Layer:** L1 — Metaphysical Identity (specification *of the engine*, not specification of *an implementation*)
**Source Mandate:** IRF-THE-033; user directive 2026-05-19 in session `S-2026-05-19-pick-abc-conductor-handoff`
**TE Budget Band:** 120K TE (essay-class)
**Constitution:** [`docs/memory/constitution.md`](../../memory/constitution.md) (all articles apply)
**SDD Methodology:** [`docs/standards/11-specification-driven-development.md`](../../standards/11-specification-driven-development.md)

> **Directive of origin.** The mandate this document fulfills is unusual. It does not authorize a 5-node implementation, even though a 5-node decomposition (Intake → Compiler → Workbench → Oracle/Factory → Maintainer) was proposed by the originating session. The user's instruction was explicit: *produce the theoretical detailed specification for a different take entirely of the artifact so that another agent will design something that is true to the rules set internally of logic but none of the code or physical manifestations in reality.*
>
> This specification therefore declines to name a substrate. It defines the engine in terms a downstream designer can satisfy in many different ways. The 5-node decomposition is acknowledged in §7 (Decoupling Clause) as one valid manifestation, not as the canonical one.

---

## 1. Identity

An **Epistemic Engine** is a self-correcting machine for the production of warranted knowledge from unwarranted material.

The minimal definition has four moving parts:

1. A **substrate** — the medium in which atoms of meaning are inscribed, retrieved, and related. The substrate is not specified; it is whatever the designer makes durable enough to outlast the engine's volatile working memory.
2. A **vocabulary of operations** — a small set of primitive verbs the engine can perform on its substrate. The vocabulary is closed; new operations are derived as compositions of primitives. This specification fixes the vocabulary (§3).
3. A **provenance discipline** — every atom in the substrate carries an unforgeable answer to *whence* and *by what authority*. Atoms without provenance are not yet citizens of the engine. This specification fixes the discipline (§4, AX-2).
4. A **directional teleology** — the engine has a direction of travel: it reduces the friction between a well-formed question and its warranted answer. An engine that does not converge in this direction is not an Epistemic Engine, regardless of how many of the primitives it implements. This specification fixes the teleology (§5).

An Epistemic Engine is not a knowledge base, not a search engine, not a notebook, and not a chatbot. It can be partially confused with each. The negation conditions (§6) make the boundaries sharp.

---

## 2. Purpose

The engine exists to dissolve the asymmetry between a practitioner's *intake bandwidth* (high — the world floods them with material) and their *recall bandwidth* (low — they cannot keep what they have read).

A practitioner without an Epistemic Engine has knowledge equal to what they can hold in working memory plus what they can re-derive in the moment plus what they can look up. The first quantity is small. The second quantity is unreliable. The third quantity grows in the input volume but does not compose — every lookup is a fresh expedition.

An engine has knowledge equal to its substrate. Once an atom is captured, attested, linked, and ratified, the engine carries it forever and surfaces it on demand. The compounding interest of every prior session compounds against every future session.

The engine therefore exists for **compositional recall**: knowledge becomes capital.

---

## 3. Primitives

The engine recognizes exactly **eight primitives**. Every higher-order operation — search, summarize, synthesize, contradict, repair — is a composition of these eight. The number is not magical; it is the smallest closed set under the axioms in §4. A designer may not introduce a ninth without amending this specification.

Each primitive carries a **Closure Status**: whether its inputs and outputs are guaranteed to remain inside the engine's substrate (closed) or may cross the boundary to the world (open).

| ID | Primitive | Signature (informal) | Closure |
|----|-----------|----------------------|---------|
| P-1 | **CAPTURE** | World → Substrate (raw atom) | Open at intake |
| P-2 | **DISSOLVE** | Composite atom → set of finer atoms | Closed |
| P-3 | **ATTEST** | Atom → Atom + provenance + confidence | Closed |
| P-4 | **LINK** | (Atom, Atom, relation-type) → typed edge | Closed |
| P-5 | **RATIFY** | Candidate atom → established atom | Closed |
| P-6 | **RECUR** | Operation × Operation.outputs → Operation' | Closed |
| P-7 | **IMPUTE** | Known-gap → candidate atom drawn from World | Open at intake |
| P-8 | **INVALIDATE** | Established atom → revoked atom (with cause) | Closed |

### Notes on the eight

- **CAPTURE** is the only primitive that creates new atoms from outside. It is unceremonious: an atom enters in whatever form the world delivered it.
- **DISSOLVE** is what an engine does that an archive does not. An archive holds composites. An engine reduces composites into atoms small enough that they can be linked into many contexts.
- **ATTEST** binds an atom to a witness — what saw it, when, with what confidence. An atom that has not been attested is a rumor.
- **LINK** is the source of compositionality. Two atoms with a typed edge between them are a third structure with derivable properties.
- **RATIFY** is the state transition that promotes a candidate to a citizen. The engine's promotion machinery (which atoms cross the threshold, by what rule) is one of the spaces where designers must decide.
- **RECUR** is the only primitive that takes operations as inputs. It is what makes the engine self-improving: the engine can apply its own primitives to its own outputs without leaving the substrate.
- **IMPUTE** is gap-driven. The engine maintains an inventory of known unknowns and reaches into the world to fill them. An engine without IMPUTE is closed-world; it may be complete on its substrate but it has no method for noticing what is missing.
- **INVALIDATE** is the conjugate of RATIFY. Without it, the substrate accumulates falsehoods forever. With it, the substrate is alive — it forgets.

The pairing structure is intentional. Six primitives form three conjugate pairs (CAPTURE↔INVALIDATE govern the boundary; ATTEST↔RATIFY govern citizenship; DISSOLVE↔LINK govern structure). The remaining two (RECUR, IMPUTE) are the engine's self-action and its outward-action. The engine is therefore symmetric except in its capacity for self-modification and its capacity for active inquiry — and those two asymmetries are what distinguish an engine from a passive store.

---

## 4. Axioms

The following axioms are irreducible commitments. No design choice may violate them. Each is annotated with a **Formalization Status** indicating whether a machine-checkable validator can be specified (following the convention of `specs/SPEC-000.md`).

### EE-AX-1: Provenance Completeness

**Every atom in the substrate has provenance, and provenance is a first-class atom.**

There are no anonymous citizens. The witness, time, source-medium, and confidence of every atom are themselves atoms — they can be CAPTURE'd, DISSOLVE'd, LINK'd, and (in extremis) INVALIDATE'd. Provenance is not a side-channel.

*Formalization: FORMAL. Validator: for every atom A in substrate, ∃ provenance-atom P such that LINK(A, P, "attested-by") exists.*

### EE-AX-2: Compositional Closure

**Every well-formed structure inside the engine is reachable by composition of the eight primitives.**

A designer may not introduce a hidden operation that bypasses the primitive vocabulary, even for "efficiency." If a desired behavior cannot be expressed as a composition of the eight, the desired behavior is not yet within the engine's reach and the designer must either decompose the behavior or amend this specification.

*Formalization: FORMALIZABLE. Validator (post-execution): every state transition in the engine's event log corresponds to one of the eight primitive types.*

### EE-AX-3: Conservative Citizenship

**No atom is treated as established knowledge until it has been RATIFY'd.**

Candidate atoms (CAPTURE'd but not yet RATIFY'd) live in a quarantine. They may be inspected, attested, linked, and dissolved, but the engine may not derive new ratified claims from them. The quarantine is the engine's discipline against premature consolidation.

*Formalization: FORMAL. Validator: every RATIFY(A) requires at least one ATTEST(A) in the engine's event log.*

### EE-AX-4: Reversibility of Trust

**Any RATIFY can be undone by an INVALIDATE; the engine has no terminal commitments.**

The substrate is not a graveyard. A claim once accepted may be revoked when new evidence warrants. INVALIDATE must record cause and must propagate: derived claims downstream of an invalidated atom enter a *re-attestation queue* and either re-ratify under new attestation or fall back to candidate status.

*Formalization: FORMALIZABLE. Validator: every INVALIDATE(A) produces a downstream-impact set D(A); every atom in D(A) is either re-RATIFY'd or returned to candidate status within a designer-specified window.*

### EE-AX-5: Gap Awareness

**The engine maintains an explicit inventory of known unknowns.**

A well-formed question that the engine cannot answer from its substrate is not a failure; it is a gap-atom. Gap-atoms are first-class: they are CAPTURE'd, ATTEST'd, LINK'd to the context that surfaced them, and held until IMPUTE either fills them or INVALIDATE retires them as unanswerable. An engine that does not record its gaps cannot direct its inquiry.

*Formalization: FORMAL. Validator: every query (Q) that fails to produce a warranted answer A appends a gap-atom G to the substrate with provenance LINK(G, Q, "surfaced-by").*

### EE-AX-6: Recursive Self-Action

**The engine can apply its primitives to its own outputs without leaving the substrate.**

RECUR is not optional. An engine without RECUR is exoskeletal: it requires an external operator for every operation. An engine with RECUR can summarize its summaries, link its links, attest its attestations. This is the engine's only mechanism for outpacing the practitioner's labor.

*Formalization: FORMALIZABLE. Validator: at least one RECUR-class operation per atom-creation operation in the engine's event log, over any non-trivial window. (Threshold determined per-deployment.)*

### EE-AX-7: Two-Bandwidth Asymmetry

**The engine writes faster than the practitioner reads; the engine reads faster than the practitioner writes.**

This is the constitutive asymmetry of the engine. It is what justifies its existence. A system in which the practitioner's read/write rates dominate is a notebook, not an engine. The asymmetry must be designed in: the engine's CAPTURE and IMPUTE rates exceed the practitioner's, while the engine's surfacing (composed LINK + RATIFY against a query) returns warranted answers in less time than the practitioner can re-derive them.

*Formalization: JUDGMENT. The threshold of "exceeds" is a per-deployment judgment by the human principal. No automated validator can determine when an engine has crossed it.*

---

## 5. Teleology

The engine's directional purpose is a **convergence in the limit**:

> Given a well-formed question Q whose answer A is derivable from the engine's substrate, the engine surfaces A in time bounded by the practitioner's attention budget for Q.

This is a teleological commitment, not a performance specification. It cannot be measured at a point in time. It can only be observed as a trajectory: over months, the time-to-answer for repeated question-classes monotonically decreases, holding question difficulty fixed.

A secondary teleology is **compositional recall**: knowledge once captured remains capital. The engine's monthly cost is bounded; the engine's stored knowledge is unbounded. An engine in which knowledge depreciates as fast as it accumulates has failed its teleology.

A tertiary teleology is **honest ignorance**: the engine's claim of "I don't know" is itself a warranted claim — backed by a gap-atom, attested, ratified. The engine's silence has provenance.

---

## 6. Negation Conditions (Falsifiers)

The following conditions, if observed, falsify the claim that a given system is an Epistemic Engine in the sense of this specification. Each is a *test*: the system must survive all of them.

- **NF-1.** The system holds composite atoms it cannot DISSOLVE. (Then it is an archive.)
- **NF-2.** The system retrieves atoms but does not compose them via LINK. (Then it is a search engine.)
- **NF-3.** The system produces output not derivable from its substrate by composition of the eight primitives. (Then it has hallucinated; falsifies EE-AX-2.)
- **NF-4.** The system contains atoms with no provenance. (Then it is unauditable; falsifies EE-AX-1.)
- **NF-5.** The system has no INVALIDATE operation, or INVALIDATE does not propagate. (Then the substrate is a graveyard; falsifies EE-AX-4.)
- **NF-6.** The system does not maintain an inventory of known unknowns. (Then it is closed-world; falsifies EE-AX-5.)
- **NF-7.** The practitioner's read/write rates dominate the engine's. (Then it is a notebook; falsifies EE-AX-7.)
- **NF-8.** Time-to-answer for repeated question-classes does not decrease over time. (Then the engine has no teleology; falsifies §5.)

If a candidate system fails any falsifier, the designer may rename it (archive, notebook, search engine, etc.) and ship it without further appeal to this specification.

---

## 7. Decoupling Clause

The 5-node architecture proposed in the originating session — Intake → Compiler → Workbench → Oracle/Factory → Maintainer — is **one valid manifestation** of this specification. It maps the eight primitives onto five modules:

| Module | Primitives it executes (typical) |
|--------|----------------------------------|
| Intake | CAPTURE |
| Compiler | DISSOLVE, ATTEST, LINK, RATIFY |
| Workbench | LINK, RATIFY (human-in-the-loop) |
| Oracle / Factory | RECUR, LINK (output-bound) |
| Maintainer | IMPUTE, INVALIDATE |

It is not the only valid manifestation. The specification is consistent with at least the following alternative decompositions:

- **By tier:** *Atoms / Molecules / Compounds* — three substrates of increasing composition, with the eight primitives operating uniformly on all three.
- **By lifecycle:** *Capture / Curation / Synthesis / Decay* — four phases, with RECUR cross-cutting all phases.
- **By agency:** *Human / Agent / System* — three operator classes, each holding a different subset of primitive privileges; ATTEST is reserved to humans and agents.
- **By tense:** *Past (archive) / Present (working set) / Future (gap-driven inquiry)* — three temporal regions, with INVALIDATE acting on Past, RATIFY on Present, IMPUTE on Future.
- **By signal:** A pipeline of *typed-signal transducers* with no named modules at all, only edges. The eight primitives become eight edge-types.

A designer is free to choose any manifestation provided the eight primitives are present, the seven axioms hold, the teleology is observable, and the falsifiers are survived. The specification is silent on substrate, language, runtime, interface, and storage form.

---

## 8. Handoff to the Designer

A downstream agent receiving this specification must produce, at minimum, a **design document** answering each of the following questions. The answers compose into an implementable system; each answer is a design decision the specification does not pre-empt.

### 8.1 Substrate

- In what medium are atoms inscribed? (File-system, database, graph store, vector store, hybrid?)
- What is the unit of atomicity? (A note, a paragraph, a sentence, a claim, a token?)
- How is the substrate made durable and replicable?
- What guarantees does the substrate provide against partial writes and concurrent edits?

### 8.2 Vocabulary Realization

- For each of the eight primitives, what is the concrete interface? (Function signature, command, message, edge-type?)
- What is the event-log format? (Every primitive invocation must be recoverable from an event log to satisfy EE-AX-2's validator.)
- How are higher-order operations (search, summarize, synthesize) decomposed into primitive sequences, and where is that decomposition memoized?

### 8.3 Provenance Discipline

- What is the format of a provenance-atom? (Witness, time, source-medium, confidence — at minimum.)
- How is "confidence" valued? (Discrete categories, continuous score, dual-rail certain/uncertain?)
- What constitutes a sufficient witness for ATTEST? (LLM? Human? Cross-source agreement?)
- How are provenance-atoms themselves attested? (To avoid infinite regress, the specification permits a fixed-point: provenance-atoms whose witness is the engine's own attestation policy.)

### 8.4 Gap Discipline

- What surfaces a gap? (Failed query? Health check? Cross-source contradiction?)
- What format does a gap-atom take?
- How does IMPUTE decide *whether* to chase a gap? (Cost model, priority, dormancy?)

### 8.5 Trust Model

- Who can RATIFY? (Human only? Agent? Quorum?)
- Who can INVALIDATE? (Same as RATIFY? Different?)
- How are conflicts resolved? (Most-recent-wins? Quorum? Surfaced to human?)

### 8.6 Failure Modes

- What happens when CAPTURE fails (network, corruption)?
- What happens when DISSOLVE produces atoms that re-compose into a different composite than the input?
- What happens when IMPUTE returns a candidate that contradicts a RATIFY'd atom? (EE-AX-4 dictates that the existing atom enters re-attestation; the designer must specify the procedure.)
- What happens when the engine is asked to RECUR forever?

### 8.7 Observability

- How does the practitioner perceive the engine's state? (Dashboard, summary, query interface?)
- How is the trajectory of EE-AX-7 (two-bandwidth asymmetry) made visible?
- How is the teleological convergence of §5 made observable over time?

### 8.8 Termination Conditions

The designer must define what it means for an instance of the engine to *complete* a session, an inquiry, a backfill operation. Termination is not given by the specification.

---

## 9. Status, Amendment, and Provenance

This specification is **L1** (metaphysical identity) in the sense of `specs/SPEC-NUMBERING.md`. It does not take a SPEC-NNN number because the `specs/` ladder describes ORGANVM itself; the Epistemic Engine is a product artifact emitted *by* ORGANVM, not a self-description of it. Per `docs/standards/11-specification-driven-development.md`, product/feature specs land in `docs/specs/<feature>/`.

Amendment requires:
1. A successor session producing a new revision under `docs/specs/epistemic-engine/spec.md` with explicit diff against this revision.
2. Justification for any change to the eight primitives or seven axioms, anchored against the falsifiers in §6.
3. Co-signing by the human principal.

Provenance of this revision:
- **Mandate:** IRF-THE-033 (line 2320 of `INST-INDEX-RERUM-FACIENDARUM.md`)
- **Originating session:** `S-2026-05-17-knowledge-base-epistemic-export` (5-node proposal recorded)
- **Authoring session:** `S-2026-05-19-pick-abc-conductor-handoff` (this revision)
- **Triple reference:** IRF-THE-033 + repo `a-organvm/organvm-corpvs-testamentvm` + GH issue #353
- **User directive:** "Produce the theoretical detailed specification for a different take entirely of the artifact so that another agent will design something that is true to the rules set internally of logic but none of the code or physical manifestations in reality."

---

## Appendix A — Reading List for the Designer

A designer beginning from this specification will benefit from prior art:

- **Substrate theory:** Zettelkasten methodology (SPEC-020 in this corpus); Niklas Luhmann's original card-index practice; Andy Matuschak's evergreen notes.
- **Provenance theory:** W3C PROV-O ontology; the Anchored Provenance pattern in academic citation systems.
- **Compositional knowledge:** the Curry-Howard-Lambek correspondence (referenced in SPEC-018 of this corpus) as a deep model of how primitives compose into structure.
- **Gap-driven inquiry:** Heuristic search literature; the *known-unknown / unknown-unknown* taxonomy from Rumsfeld and prior.
- **Self-correcting epistemics:** Karl Popper on falsification; Imre Lakatos on research programmes; the engineering literature on idempotent event-sourced systems.

A designer is not required to read any of these. They are landmarks, not requirements.
