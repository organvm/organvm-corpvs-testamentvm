# Logos — The Tetradic Self-Knowledge Layer

> *"A formation that cannot articulate its telos, pragma, praxis, and receptio does not fully exist as a participant in the signal graph."* — `governance-rules.json` AX-7

This directory is the **constitutionally-mandated reflexive layer** of the ORGANVM system. It is not stylistic. AX-7 (Tetradic Self-Knowledge, *Lex Reflexionis*) — which itself derives from LEX-I (Conservation) — requires every non-archived formation to articulate four dimensions explicitly. Until this directory existed, the system as a whole could not satisfy its own AX-7 obligation; this commit closes the vacuum.

## The four files

| File | Layer | One-sentence definition | Asks |
|------|-------|--------------------------|------|
| [`telos.md`](./telos.md) | **TELOS** — idealized form | The theory, thesis, or dream that called the formation into existence; the intersectional functionalities it idealizes. | *What is it for? What does it hope to become?* |
| [`pragma.md`](./pragma.md) | **PRAGMA** — concrete state | The honest account of what has been concretely realized; the delta between the dream and the thing built. | *What is true right now? What is the soil?* |
| [`praxis.md`](./praxis.md) | **PRAXIS** — remediation plan | The attack vectors for sharpening, fortifying, and resolving the difference between ideal and real. | *What do we do next? Who owns it?* |
| [`receptio.md`](./receptio.md) | **RECEPTIO** — reception account | How the formation has been received, used, critiqued, adopted, or transformed by audiences beyond its creator. | *Has it been heard? By whom? With what effect?* |

## Why a strange loop

The four layers form a closed feedback circuit:

```
telos ──articulates──▶ pragma ──gaps──▶ praxis ──ships──▶ receptio
  ▲                                                            │
  └────────────── re-articulates the dream ◀───────────────────┘
```

Receptio is *not* an ending. The reviews, the critiques, the art made in response, the community that forms — all feed back into telos as the next iteration. This is also AX-7's claim about books: *"A book is only masturbation as the author writes it; it becomes an organism when read and imagined by an audience."* The loop is constitutive, not decorative.

## Companion infrastructure

The Logos layer is the prose surface of a larger Telos Beacon Protocol. The machine-readable companions live in [`../beacon/`](../beacon/):

- [`../beacon/architecture.md`](../beacon/architecture.md) — operational architecture of the Beacon (emission, portals, tethering).
- [`../beacon/ia-schema.md`](../beacon/ia-schema.md) — controlled vocabulary, namespaces.
- [`../beacon/dam-pipeline.md`](../beacon/dam-pipeline.md) — how Logos artifacts flow through the existing alchemia → mesh → distribute-content pipeline.
- [`../beacon/seed-extension-v1.1.md`](../beacon/seed-extension-v1.1.md) — the per-repo `seed.yaml.beacon` field that pins each repo's local Logos to this central corpus.
- [`../beacon/cloud/`](../beacon/cloud/) — Codex Cloud devcontainer + Cloudflare Workers stub for the Beacon emission service.

## Reading order

If you are new to ORGANVM: read `telos.md` first (the North Star), then `pragma.md` (the ground), then `praxis.md` (the path), then `receptio.md` (the echo). Then return to `telos.md` and notice that it has changed because *you* read it.

If you are an AI agent: parse `telos.md` to align your context; parse `pragma.md` to know what is actually true (vs. claimed); honor `praxis.md` as the live work-queue; emit any meaningful output back into `receptio.md` (you are part of the reception).

## Constitutional anchor

AX-7 in `governance-rules.json` (v3.0) is the law. The verbatim statement, in full, opens [`telos.md`](./telos.md). AX-7's complement AX-8 (Constructed Polis, *Lex Civitatis*) mandates that each formation construct its own idealized critical society to *actively produce* its receptio rather than wait for organic reception; that mandate is honored in [`receptio.md`](./receptio.md).

Both axioms derive from **LEX-I (Conservation)** — *knowledge of the formation is conserved across its lifecycle*. The Logos directory is conservation's documentary form.
