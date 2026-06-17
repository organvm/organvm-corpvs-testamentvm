# SPEC-002 Source Archive

```
Date:      2026-06-15
Status:    COMPLETE
Resolves:  GH#134
Phase:     R (Research) — gate G0 for SPEC-002 Phase F
Spec:      SPEC-002 (Primitive Register)
Scope:     Annotated bibliography of all sources grounding the seven primitives
           and the §2 composition framework.
```

> **Network note.** This archive was assembled from SPEC-002's own citations and the
> repository bibliography. No downloads were attempted — the working environment has
> restricted network access. "Open access" notes below record publicly known availability
> from prior knowledge; they should be spot-verified during Phase F before a reviewer relies
> on a link.
>
> **BibTeX cross-reference.** Keys in `specs/bibliography.bib` today that bear on SPEC-002:
> `MartinLof1984`, `MartinLof1982`, `CrawfordOstrom1995`, `WhiteheadRussell1910`, `Curry1934`,
> `Howard1980`, `Wadler2015`. All other keys below are **[in bibliography.bib]** — cited by SPEC-002 but
> not yet present in the canonical bib. Adding them is a Phase-F gate item.

---

## 1. Mereology — Composition Framework (§2)

### Simons (1987) — `Simons1987` **[in bibliography.bib]**
Simons, Peter. *Parts: A Study in Ontology.* Oxford: Clarendon Press, 1987.

The standard modern treatment of formal mereology. Simons surveys Classical Extensional
Mereology and argues against its extensionality and unrestricted-composition axioms, proposing
**Minimal Mereology (MM)** as the defensible core. SPEC-002 borrows MM's axiom set verbatim
(§2.1) and Simons' notion of the *integral whole* — a composite individuated by the
structure-determining relations among its parts — to justify non-extensional composition of
organs and repos. Chapter 8's essential/non-essential part distinction grounds SPEC-002 §2.3
(essential vs. generic vs. rigid dependence). *Open access:* No; monograph, library/purchase.

---

## 2. Type Theory — Primitive Signatures and Dependent Records (§1, §2.2, §4)

### Martin-Löf (1984) — `MartinLof1984` (in bib)
Martin-Löf, Per. *Intuitionistic Type Theory.* Naples: Bibliopolis, 1984. (Padua lectures,
notes by Giovanni Sambin.)

The foundational text for dependent type theory. Introduces the universe hierarchy, dependent
function types (Π) and dependent pair types (Σ), judgments, and the propositions-as-types
interpretation. SPEC-002 uses it for every primitive's type signature, for State as a Π-type
over dimensions, and for Constraint-as-`Prop` (a satisfying State is a proof term). *Open
access:* Yes — the Sambin lecture notes circulate freely online (commonly hosted PDF).

### Martin-Löf (1982) — `MartinLof1982` (in bib)
Martin-Löf, Per. "Constructive Mathematics and Computer Programming." In *Logic, Methodology
and Philosophy of Science VI*, 153–175. Amsterdam: North-Holland, 1982.

The programming-facing companion to the 1984 monograph; connects dependent types to executable
construction. Supports SPEC-002's claim that the primitives are FORMALIZABLE — specifiable as
machine-checkable types. *Open access:* Partial — widely reprinted; preprints circulate.

### Pierce (2002) — `Pierce2002` **[in bibliography.bib]**
Pierce, Benjamin C. *Types and Programming Languages.* Cambridge, MA: MIT Press, 2002.

The reference textbook for practical type systems: records, variants, subtyping, references,
recursive types, and their metatheory. SPEC-002 leans on Pierce for the *engineering
tractability* of its dependent record types (§2.2) and the §3 domain compositions — the bridge
from Martin-Löf's semantics to an implementable static discipline. Note: TAPL's core records are
non-dependent, so SPEC-002 combines Pierce (records) with Martin-Löf (dependency). *Open access:*
No; textbook. Errata and supplementary material are public on the author's site.

### Curry (1934) / Howard (1980) — `Curry1934`, `Howard1980` (in bib)
Curry, H.B. "Functionality in Combinatory Logic," *PNAS* 20(11):584–590, 1934; Howard, W.A.
"The Formulae-as-Types Notion of Construction," in *To H.B. Curry*, 479–490, Academic Press, 1980
(ms. 1969).

The Curry–Howard correspondence (propositions-as-types). SPEC-002 invokes it specifically for
Constraint (PRIM-006): a Constraint is a type, its proofs are terms, an uninhabited Constraint
type is an unsatisfiable rule. *Open access:* Curry yes (PNAS archive); Howard typically behind
publisher access; Wadler (2015, `Wadler2015`, in bib) is an open survey covering both.

---

## 3. Foundational Ontologies — Alignment Columns (§1, §3 of grounding)

### Guarino & Welty (2002) — `GuarinoWelty2002` **[in bibliography.bib]**
Guarino, Nicola, and Christopher Welty. "Evaluating Ontological Decisions with OntoClean."
*Communications of the ACM* 45(2):61–65, 2002. (See also their *Data & Knowledge Engineering*
treatment, 2009.)

Defines the OntoClean meta-properties — Rigidity, Identity, Unity, Dependence — and the
constraints they impose on subsumption. SPEC-002 attaches an OntoClean profile to each of the
seven primitives and uses the meta-properties as the consistency discipline of `grounding.md`
§(a). *Open access:* Yes — the CACM article and OntoClean overviews are publicly available.

### Masolo et al. (2003) — `MasoloEtAl2003` **[in bibliography.bib]**
Masolo, Claudio, Stefano Borgo, Aldo Gangemi, Nicola Guarino, and Alessandro Oltramari.
*Ontology Library (WonderWeb Deliverable D18) — DOLCE.* ISTC-CNR, 2003.

The DOLCE specification: a Descriptive Ontology for Linguistic and Cognitive Engineering,
partitioning reality into Endurants, Perdurants, Qualities, and Abstracts. SPEC-002's DOLCE
alignment column derives from it — notably the single point of credit for State (DOLCE's
homeomeric-perdurant State, 0.5/1) and the Quality/qualia treatment grounding Value. *Open
access:* Yes — the WonderWeb D18 deliverable PDF is publicly distributed.

### Arp, Smith & Spear (2015) — `ArpSmithSpear2015` **[in bibliography.bib]**
Arp, Robert, Barry Smith, and Andrew D. Spear. *Building Ontologies with Basic Formal Ontology.*
Cambridge, MA: MIT Press, 2015.

The canonical BFO 2.0 reference: the Continuant/Occurrent partition, Independent/Specifically-
Dependent/Generically-Dependent continuants, Process/Process Boundary occurrents, and the
Disposition/Role/Function trichotomy for realizables. SPEC-002's BFO alignment column derives
from it, including the PRIM-007 trichotomy table and the BFO non-recognition of State and
Constraint. *Open access:* The book is purchase/library; BFO 2.0 the ISO/IEC 21838-2 standard
and the BFO documentation/specification are publicly available online.

---

## 4. Normative / Institutional Grounding — Constraint (PRIM-006)

### von Wright (1951) — `vonWright1951` **[in bibliography.bib]**
von Wright, Georg Henrik. "Deontic Logic." *Mind* 60(237):1–15, 1951.

The founding paper of modern deontic logic, introducing obligation (O), permission (P), and
prohibition (F) as modal operators with interdefinability. SPEC-002's `Deontic = MUST | SHOULD |
MAY` parameter and the MUST↔O / MAY↔P / ¬MAY↔F mapping derive directly. *Open access:* Behind
*Mind* (OUP) access, though widely anthologized.

### Crawford & Ostrom (1995) — `CrawfordOstrom1995` (in bib)
Crawford, Sue E.S., and Elinor Ostrom. "A Grammar of Institutions." *American Political Science
Review* 89(3):582–600, 1995.

Introduces the **ADICO** syntax (Attributes, Deontic, aIm, Conditions, Or-else) for decomposing
institutional statements into rules, norms, and strategies. SPEC-002 carries only the Deontic
component at the primitive layer and defers full ADICO structuring to SPEC-003/SPEC-005. *Open
access:* Behind *APSR* (Cambridge/JSTOR), widely cited and summarized.

### Ostrom (2005) — `Ostrom2005` **[in bibliography.bib]**
Ostrom, Elinor. *Understanding Institutional Diversity.* Princeton: Princeton University Press,
2005.

Develops rules-in-use vs. rules-in-form and the layered (operational / collective-choice /
constitutional) view of institutions. Grounds SPEC-002's distinction between Constraints-as-
declared (`governance-rules.json`) and Constraints-as-enforced (engine validators), and motivates
the DRIFT classification in §7.3. *Open access:* No; monograph.

### Searle (1995) — `Searle1995` **[in bibliography.bib]**
Searle, John R. *The Construction of Social Reality.* New York: Free Press, 1995.

Theory of constitutive rules ("X counts as Y in context C") and institutional facts. Backstops the
Contestation Disclosure for Constraint (§5.2): governance Constraints are constitutive rules,
which licenses importing normativity into the register. SPEC-002 adopts the constitutive-rule
schema only, not Searle's full collective-intentionality apparatus. *Open access:* No; monograph.

---

## 5. Disposition / Capability Grounding — Capability (PRIM-007)

### Johansson (2004) — `Johansson2004` **[in bibliography.bib]**
Johansson, Ingvar. *Ontological Investigations: An Inquiry into the Categories of Nature, Man and
Society.* 2nd ed. Frankfurt: Ontos Verlag, 2004 (1st ed. Routledge, 1989).

Argues (Ch. 11) that dispositions/tendencies are irreducible to their manifestations — a sugar
cube is soluble even when dry. SPEC-002 uses this as the independent (non-BFO) validation that
Capability (a power that exists unexercised) is first-class, supporting retention of the unified
primitive against the reduction-to-function objection. *Open access:* No; monograph.

---

## 6. Quality / State Grounding (secondary)

### Armstrong (1978) — `Armstrong1978` **[in bibliography.bib]**
Armstrong, David M. *A Theory of Universals: Universals and Scientific Realism, Vol. II.*
Cambridge: Cambridge University Press, 1978.

Immanent realism about universals and the theory of states of affairs as truthmakers. Provides
secondary grounding for Value (qualities first-class, PRIM-002) and for the respectability of
State as a "states of affairs"-style category (PRIM-005), supplementing the primary DOLCE
grounding. *Open access:* No; monograph.

---

## 7. Methodological Principle — Reductions (§3.5–3.6, §5.4–5.5)

### Gruber (1993) — `Gruber1993` **[in bibliography.bib]**
Gruber, Thomas R. "Toward Principles for the Design of Ontologies Used for Knowledge Sharing."
*International Journal of Human-Computer Studies* (also Knowledge Systems Lab tech report
KSL-93-04), 1993/1995.

States the **minimal ontological commitment** principle (commit only to what the application
domain requires) alongside clarity, coherence, and extendability. This is the decisive principle
for *excluding* Process and Evidence from the register (they are reducible) while *admitting*
Constraint (the governance domain requires normativity). *Open access:* Yes — the KSL tech report
PDF circulates freely.

---

## 8. Phase-F Action Items

1. Add the 11 `[in bibliography.bib]` BibTeX keys to `specs/bibliography.bib`: `Simons1987`,
   `GuarinoWelty2002`, `MasoloEtAl2003`, `ArpSmithSpear2015`, `Pierce2002`, `vonWright1951`,
   `Ostrom2005`, `Searle1995`, `Johansson2004`, `Armstrong1978`, `Gruber1993`. Tag each with
   keyword `SPEC-002`.
2. Spot-verify the "open access" notes against live sources before any reviewer-facing link is
   published (network was restricted during research).
3. Confirm `SPEC-002.md` §7.4 Academic Lineage cites only keys that exist post-addition.
