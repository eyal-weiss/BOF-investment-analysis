# BranchOut Food, Inc. (NASDAQ: BOF) — Investment Analysis

Independent investment analysis of BranchOut Food, Inc. (NASDAQ: BOF), a micro-cap better-for-you snack company that dries fruit and vegetables using EnWave "GentleDry" REV dehydration technology at a company-owned facility in Peru.

Unlike a conventional DCF, BOF is valued with a **probabilistic scenario / Monte Carlo model**, because its future resolves into a few discrete development paths whose values differ by more than 10x. The model defines those paths, assigns each a probability, models the per-share consequence within each as a distribution, and rolls up into an expected value *and* a full distribution of outcomes.

## Valuation summary

*200,000-draw Monte Carlo · 12% cost of equity · price $4.28 (June 21, 2026)*

| Path | Probability | Conditional value/share | Contribution to E[value] |
|------|------------|------------------------|--------------------------|
| Failure (going concern / dilution spiral) | 12% | ~$0.20 | $0.02 |
| Muddle (survives sub-scale) | 30% | ~$0.69 | $0.21 |
| Scale & stay public | 26% | ~$6.55 | $1.71 |
| Scale & acquired by a strategic | 32% | ~$11.49 | $3.67 |
| **Probability-weighted expected value** | **100%** | **$5.61 (+31%)** | **$5.61** |

Median $5.79 · P(≥2x) 34% · P(near-total loss) 16%. The thesis is a **~58/42 binary on operational scaling** of the Peru REV throughput. At $4.28 the price capitalizes only a **~43% chance of scaling at face value** (≈59–64% once the usual micro-cap margin of safety is applied), versus a ~58% base case — implying ~31% upside. Winning exits compound at a **~30–34% CAGR**; the bull tail — scale to ~$200M revenue, then a strategic exit (PepsiCo/Hershey/Mondelez) at ~4x revenue — is worth ~$12/share after honest time-and-dilution drag.

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
