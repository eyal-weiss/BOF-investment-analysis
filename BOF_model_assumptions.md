# BranchOut Food (NASDAQ: BOF) — Scenario Valuation Model Assumptions

**Approach:** Probabilistic scenario / Monte Carlo valuation, *not* a false-precision multi-year 3-statement model.
For a sub-scale company whose future is a few discrete development paths, we model each path's
*consequence* for the per-share value and weight by its *probability*, producing an expected value
**and a full distribution** of per-share outcomes.

Last updated: 2026-06 (research date). Currency in USD; financials in $ millions unless noted.

---

## 1. Current state (anchor, ~mid-2026)

| Item | Value | Source |
|---|---|---|
| Share price | $4.28 | market, Jun 2026 |
| Basic shares out | 15.32M | 10-Q / cover, Jun 18 2026 |
| Market cap | ~$66M | derived |
| Cash | $0.9M | 10-Q, Mar 31 2026 |
| Total debt | ~$7.6M | 10-Q (Kaufman convert $2.9M @ $0.7582; Kaufman senior secured $1.5M; EnWave equip loan $1.5M; Peru finance lease $1.7M; EIDL) |
| Net debt | ~$6.7M | derived |
| Enterprise value | ~$72M | derived |
| FY2025 revenue | $13.7M (+113% YoY) | press release / 10-K |
| FY2026 revenue guide | "$20M+" | mgmt, Q4'25 call |
| Reported GM (FY25) | ~16% (depressed by air freight + tariff) | 10-K |
| **Normalized GM (ex air-freight & tariff)** | **~25%** (printed 27% in a record month, Jun'25) | mgmt |
| Going concern | Yes (accum. deficit $25.5M) | 10-Q |
| Key backer | Kaufman Capital — 34.5% fully diluted | filings |
| CEO / CFO | Eric Healy (founder, ~20%) / John Dalfonsi (banking background) | filings |

## 2. Business & moat (analyst diligence + filings)

- **Tech/process:** GentleDry / EnWave REV dehydration; 4 production lines in a 50k sqft Peru facility.
- **Moat:** Peru cost base ($1.5/hr labor, exclusive access to cosmetically-imperfect produce),
  ~4-year head start, customer relationships hard to win. Demand is **not** the constraint —
  **scaling throughput is** (filings + analyst diligence). This is the binding risk.
- **Customers (verified):** Costco (multi-region), Sam's Club (nationwide May'26), Target (~2,000 stores Sep'26),
  Walmart (slipped to 2027), MicroDried ingredient channel ($5–6M), a large tolling partner, a chocolate CPG.
- **Maturity mix (analyst assumption):** brand 40% / private label 40% / ingredient 20%.
- **Margins (analyst assumption):** 35% GM realistic at scale (in line with best scaled branded-snack peers; Peru cost base supports it).

## 3. The two temporary margin drags (model them out)

- **Air freight (~8% of COGS):** deliberate ramp/credibility choice; removed as ocean freight takes over
  (mgmt: +3–4% GM uplift). **Modeled as fully removed.**
- **Tariff:** Peru lost duty-free (TPA) under the Apr-2025 10% reciprocal tariff (EO 14257); a Nov-2025
  exemption restored duty-free for 100+ ag products **including mangoes** (avocado, coffee, cocoa, citrus, juices),
  but **pineapple/banana not explicitly named, blueberries excluded**, and processed/dried HS classification unresolved.
  → **Modeled as a small 0–2% residual drag (default ~1%), tweakable.**

## 4. Scenario tree (4 paths) — the decomposition

Winning = **scaling works**. `P(acquired) = P(scaling works) × P(sell | scaled)`.
The 3-vs-4 split is immaterial to the thesis (both are wins); reported separately for the distribution's right tail.

| # | Path | Definition | Base prob |
|---|---|---|---|
| 1 | **Failure** | Going concern fails / dilution spiral; equity ≈ $0 | 12% |
| 2 | **Muddle** | Survives sub-scale, chronic dilution, barely profitable | 30% |
| 3 | **Scale & public** | Operational scaling works; profitable growth co., stays public (Simply Good Foods / BellRing template) | 26% |
| 4 | **Scale & acquired** | Scaling works AND a strategic buys it (PepsiCo/Hershey/Mondelez) | 32% |

*Notes:* Probabilities are tweakable. User priors were 10/30/15/45; analyst counter 13/30/24/33; base case ≈ midpoint.
**Kaufman Heinz correction:** Kraft Heinz is a *divester*; natural acquirers are PepsiCo/Frito-Lay (Bare precedent), Hershey, Mondelez.

## 5. Per-path value drivers (Monte Carlo distributions; triangular = min/mode/max)

| Driver | Failure | Muddle | Scale & public | Scale & acquired |
|---|---|---|---|---|
| Exit revenue ($M) | — | (22 / 27 / 32) | (55 / 85 / 160) | (75 / 115 / 220) |
| Exit basis | residual | EV/Rev | EV/Rev (no control premium) | EV/Rev (M&A) |
| Exit multiple (EV/Rev) | — | (1.0 / 1.8 / 2.5) | (2.0 / 2.8 / 3.5) | (3.5 / 4.0 / 5.0) |
| **Exit shares (M)** | n/a | (28 / 30 / 40) | correlated w/ revenue | correlated w/ revenue |
| Net debt at exit ($M) | — | ~8 | ~9 + 0.04·(rev−90) | ~9 + 0.04·(rev−90) |
| Years to exit | — | ~5 | ~5 | correlated w/ revenue (4→7.5) |
| Equity value/share | (0 / 0.10 / 0.50) | derived | derived | derived |

**Correlations (scaling paths):** exit **shares rise with revenue** — `shares = 20 + 0.075·(rev−60) + noise`
(@ $115M → ~24M; @ $200M → ~30.5M); for the **acquired** path **time-to-exit rises with revenue**
(`4 + 0.0241·(rev−75)`: @ $115M → 5yr, @ $200M → 7yr). This prices the "$200M-then-sell" **super-bull as the
right tail of path 4 — no fifth scenario** — with honest time-and-dilution drag (~$12 PV ≈ 2.9x, vs naive ~$56).

**Dilution logic:** BOF is ~EBITDA breakeven already, so equity need funds working capital + growth capex,
not years of losses — and machines are debt-financeable. Management minimizes dilution by (1) debt-financing
hard assets, (2) trade/AR financing for WC, (3) equity only for the gap. A near-term ~$5M equity raise at ~$4
is forced (cash is $0.9M). Scaling paths dilute *moderately* (~24M @ base), driven largely by the near-certain
Kaufman convert (~3.8M) + warrants (~0.5M). Muddle dilutes brutally (low prices) to ~30M+.
**Dilution risk and operational-scaling risk are the same risk** → no separate dilution probability needed.

## 6. M&A exit multiple support (BFY snack deals)

Clean better-for-you snack transactions cluster at **~3.6–4.4x EV/Revenue**, ~15–17x EV/EBITDA:
Kraft Heinz/Primal Kitchen ~4.0x; Hershey/Amplify (SkinnyPop) ~4.2–4.3x; Hershey/Dot's ~4.4–5.6x;
Mondelez/Clif ~3.6x. Direct analog: **PepsiCo/Bare Foods (2018, <$200M)** — same dried fruit/veg category.
Strategic interest threshold ~$50–100M revenue for a category-defining BFY brand.

## 7. Discounting

Cost of equity **~12%** (idiosyncratic/survival risk carried in the path probabilities, not the rate). Tweakable.

## 7b. Current base-case result (refined)

Expected value **$5.61 (+31% vs $4.28)** | median $5.79 | P(≥2x) 34% | P(loss) 43% | P(near-total loss) 16%.
Per-path conditional means: failure $0.20, muddle $0.69, scale&public $6.55, scale&acquired $11.49.
Bimodal: ~42% mass → ~$0 (failure+muddle), ~58% → win cluster ($6–14). The case rests on P(scaling works).

## 8. Outputs

- Full Monte Carlo distribution of PV/share; expected value vs $4.28; median; percentiles.
- P(total loss), P(loss vs today), P(>2x), P(>5x).
- Per-path expected value & contribution.
- **Dilution sensitivity table** (expected value & upside across exit-share-count variations).
- Sensitivity to probabilities, exit multiple, discount rate.
