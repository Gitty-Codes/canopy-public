# Voices

The ten voices of The Canopy. Each corresponds to a named agent in the
Agent Architecture: dispositions held in tension, not personas in dialogue.

## Variant scheme

A variant is a complete set of ten voices representing one hypothesis
about how the substrate should be expressed. The harness loads one
variant at a time as the unconscious layer of the system prompt.

| Variant | Hypothesis | Notes |
|---|---|---|
| `v1_original` | Each voice runs as its own agent process with a full standalone prompt. | The founding prompts. Extracted verbatim from `agents/*.py` and `constitution/load.py`. Locked — preserved as the baseline against which later variants are benchmarked. Do not edit. |
| `v2_compressed` | Voices held simultaneously in one harness; tighter dispositions, no per-voice operational instructions. | Step 1 of the harness rebuild. ~17 lines per voice. Drops Elder-in-Training boilerplate (lives in the Cultural Constitution and Agent Architecture, loaded alongside) and structured-output scaffolding (added back when council mode is invoked). |

## Backtest discipline

When a new variant is added, existing variants stay as-is. Edits to
the active variant are made by creating a new variant, not by
modifying an old one. The decisions log records which variant won
which benchmark and why.

We do not rewrite the past.
