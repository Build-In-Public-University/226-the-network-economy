# Capitalism Argument Analysis

A reproducible, claim-centered analysis of the Stanford Encyclopedia of Philosophy entry:
https://plato.stanford.edu/entries/capitalism/

The repo reconstructs the entry's argumentative architecture rather than pretending to prove or disprove the cited theories. It separates:

- descriptive theories of capitalism
- normative defenses
- normative critiques
- meta-level standards for what counts as a critique
- supports, challenges, assumptions, and proposed falsifiers

The central result is a graph showing two major chains:

- institutional substrate -> markets -> efficiency/welfare/freedom/political liberty
- ownership/commodification/investment/dependence -> exploitation/domination/externalization/crisis/distributive critique

The most important unresolved issue is definitional. The entry compares arguments that do not always target the same object. A claim about free markets is not automatically a claim about capitalism as a whole.

## Quickstart

```bash
cd capitalism-argument-analysis
PYTHONPATH=src python3 -m capitalism_analysis source/sep-capitalism.md --out data
python3 -m unittest discover -s tests -v
```

Outputs:

- `data/claims.json` — curated claim ledger with status, assumptions, links, and falsifiers
- `data/edges.json` — machine-readable support/challenge edges
- `data/argument-map.dot` — Graphviz graph source
- `data/argument-map.svg` — rendered argument graph
- `data/time-violence-alignment.json` — SEP-to-our-framework alignment ledger with falsifiers
- `time-violence-alignment.md` — synthesis of the alignment and proposed instrument
- `data/multi-resource-model.json` — idealized labor-time, money-return, and network-economy comparison
- `data/multi-resource-model.dot` — visual model source
- `multi-resource-model.md` — comparison and test design
- `reviews/pro-review.md` — independent charitable case
- `reviews/con-review.md` — independent skeptical case
- `reviews/HUMAN-JUDGE.md` — human adjudication worksheet
- `PUBLICATION_BOUNDARY.md` — public/private and publication-state boundary
- `data/sections.json` — parsed source heading structure
- `data/report.md` — human-readable report

## Epistemic boundary

This first version analyzes the arguments as presented in the SEP entry. It does not independently verify the empirical or historical claims in the cited literature. `conditional` means the entry presents a claim with explicit or implicit conditions; `contested` means the entry itself records significant objections; `framing` marks scope or methodology rather than a truth claim.

The source snapshot is preserved locally for reproducibility. Check its publication date and contents before treating this as a current analysis.
