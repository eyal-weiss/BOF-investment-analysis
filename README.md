# BranchOut Food, Inc. (NASDAQ: BOF) — Investment Analysis

Independent investment analysis of BranchOut Food, Inc. (NASDAQ: BOF), a micro-cap better-for-you snack company that dries fruit and vegetables using EnWave "GentleDry" REV dehydration technology at a company-owned facility in Peru.

Unlike a conventional DCF, BOF is valued with a **probabilistic scenario / Monte Carlo model**, because its future resolves into a few discrete development paths whose values differ by more than 10x. The model defines those paths, assigns each a probability, models the per-share consequence within each as a distribution, and rolls up into an expected value *and* a full distribution of outcomes.

## Valuation summary

*200,000-draw Monte Carlo · 12% cost of equity · price $4.28 (anchor; ≈$4.30 spot Jul 1, 2026)*
*Updated 2026-06-30 for the Sam's Club everyday-placement catalyst (see below).*

| Path | Probability | Conditional value/share | Contribution to E[value] |
|------|------------|------------------------|--------------------------|
| Failure (going concern / dilution spiral) | 9% | ~$0.16 | $0.01 |
| Muddle (survives sub-scale) | 27% | ~$0.69 | $0.19 |
| Scale & stay public | 29% | ~$6.53 | $1.90 |
| Scale & acquired by a strategic | 35% | ~$11.47 | $4.01 |
| **Probability-weighted expected value** | **100%** | **$6.10 (+43%)** | **$6.10** |

Median $6.37 · P(≥2x) 37% · P(near-total loss) 13%. The thesis is a **~64/36 binary on operational scaling** of the Peru REV throughput. At $4.28 the price capitalizes only a **~43% chance of scaling at face value** (≈59–64% once the usual micro-cap margin of safety is applied), versus a **~64% base case** — implying ~43% upside. Winning exits compound at a **~30–34% CAGR**; the bull tail — scale to ~$200M revenue, then a strategic exit (PepsiCo/Hershey/Mondelez) at ~4x revenue — is worth ~$12/share after honest time-and-dilution drag.

**2026-06-30 catalyst.** BranchOut converted its Sam's Club (nation's #2 warehouse club) placement to **everyday recurring** in **309 clubs** at an estimated **$8M annual revenue** (shipments Sep 2026), with management guiding to **positive operating cash flow** and better factory utilisation / gross margin. This is the first hard, dated evidence that the model's central "does scaling work?" binary is resolving favourably, so it is expressed as a **path-probability shift** (P(scaling) 58% → 64%; failure 12% → 9%) rather than as changed exit distributions. E[value] moves $5.61 → $6.10. Notably, the tape barely reacted — the price still implies only ~43% at face value.

## Contents

- `BOF_investment_thesis.md` — full written thesis
- `bof_financial_model.ipynb` — the probabilistic scenario / Monte Carlo model (control panel + sensitivities)
- `build_notebook.py` — generator script that builds the notebook
- `BOF_model_assumptions.md` — documented assumptions, correlations, and sources

## Methodology & data sources

- **Financials & capital structure:** SEC EDGAR filings (10-K, 10-Q, 8-K), company press releases.
- **Commercial traction & guidance:** company releases and investor-event summaries.
- **M&A comparables:** confirmed better-for-you snack transactions (Primal Kitchen, SkinnyPop/Amplify, Dot's, Clif, Bare/PepsiCo) — clustering at ~3.6–4.4x EV/Revenue.
- **Model:** Python (NumPy/pandas/matplotlib); triangular input distributions; correlations linking exit scale to dilution and time-to-exit.

## Disclaimer

This is independent analysis for informational purposes only and is **not investment advice**. Figures are estimates and modeling assumptions, not company guidance. Do your own research.
