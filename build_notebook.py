"""Generate bof_financial_model.ipynb — a probabilistic scenario / Monte Carlo valuation."""
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

cells = []
def md(s): cells.append(new_markdown_cell(s))
def code(s): cells.append(new_code_cell(s))

# ---------------------------------------------------------------- title
md(r"""# BranchOut Food (NASDAQ: BOF) — Probabilistic Scenario Valuation

**Why this model, not a 5-year DCF:** BOF is a sub-scale company whose future is a handful of
*discrete development paths*. Forecasting one precise income statement to 2030 would be false precision.
Instead we define the plausible paths, attach a probability to each, model the *consequence* for the
per-share value within each (as distributions, not points), and roll up via **Monte Carlo** into an
**expected value** *and* a **full probability distribution** of per-share outcomes.

The model is fully parametric — **edit the control panel in the next cell and re-run** to test any view.

Scenario tree (winning = *scaling works*) — deliberately **4 paths, no "super-bull" node**:

| # | Path | Definition |
|---|---|---|
| 1 | Failure | Going concern fails / dilution spiral → equity ≈ \$0 |
| 2 | Muddle | Survives sub-scale, chronic dilution, barely profitable |
| 3 | Scale & public | Scaling works; profitable growth co., stays public |
| 4 | Scale & acquired | Scaling works **and** a strategic buys it (PepsiCo/Hershey/Mondelez) |

The **\$200M "scale-further-then-sell" super-bull is the right tail of path 4**, not a separate scenario:
adding a discrete node would not change the expected value (the mean is linear) and would force an
invented probability. Instead, path 4 carries two correlations so the tail is *honest*:
**bigger exits take longer** (more discounting) and **take more dilution** (more shares).
`P(acquired) = P(scaling works) × P(sell | scaled)`; dilution risk = operational-scaling risk.""")

# ---------------------------------------------------------------- setup
md(r"""## 1. Setup & Control Panel

All assumptions live here. Triangular distributions are `(min, mode, max)`.

**Update 2026-06-30 — de-risking catalyst baked in.** BranchOut converted its Sam's Club
(the nation's #2 warehouse club) placement to **everyday recurring** in **309 clubs** at an
estimated **\$8M annual revenue**, and management expects the program to drive **positive
operating cash flow** and better factory utilisation / gross margin. Because this bears directly
on the model's central binary — *does operational scaling work?* — it is expressed as a shift in
the **path probabilities** (failure 12→9, muddle 30→27, scaling 58→**64%**), with a +\$0.5M
net-debt nudge for the new \$1.0M working-capital loan. Exit-revenue/multiple distributions are
unchanged (their modes are years out).""")
code(r"""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.float_format', lambda x: f'{x:,.2f}')   # all randomness flows through run_mc's seeded rng

N_SIMS   = 200_000      # Monte Carlo draws
DISCOUNT = 0.12         # cost of equity (survival risk is in the probabilities, not the rate)

# ---- Current state (anchor, mid-2026) -------------------------------------
PRICE_NOW   = 4.28
SHARES_NOW  = 15.32     # million, basic

# ---- Path probabilities (must sum to 1.0) ---------------------------------
#   user priors 10/30/15/45 ; analyst counter 13/30/24/33 ; prior base 12/30/26/32
#   UPDATED 2026-06-30: Sam's Club (nation's #2 warehouse club) converts to EVERYDAY
#   placement in 309 clubs (~$8M/yr est.) + mgmt guides to POSITIVE OPERATING CASH FLOW.
#   This is direct evidence the scaling binary is resolving favourably: cut failure
#   (going-concern risk falls with positive OCF), trim muddle, add ~6pts to scaling.
#   P(scaling) 58% -> 64%, in line with the ~59-64% the tape implies after a micro-cap MoS.
P = {
    'failure'       : 0.09,
    'muddle'        : 0.27,
    'scale_public'  : 0.29,
    'scale_acquired': 0.35,
}
assert abs(sum(P.values()) - 1.0) < 1e-9, "probabilities must sum to 1"

# ---- Exit revenue ($M), triangular (min, mode, max) -----------------------
#   acquired tail reaches ~$220M to carry the "scale-further-then-sell" super-bull
REV = {
    'muddle'        : (22,  27,  32),
    'scale_public'  : (55,  85,  160),
    'scale_acquired': (75, 115,  220),
}
# ---- Exit valuation multiple (EV / Revenue), triangular -------------------
MULT = {
    'muddle'        : (1.0, 1.8, 2.5),   # weak small-cap
    'scale_public'  : (2.0, 2.8, 3.5),   # profitable public grower, no control premium
    'scale_acquired': (3.5, 4.0, 5.0),   # BFY-snack M&A cluster (3.6-4.4x); high-growth tail to 5.0x
}

# ---- DILUTION correlated with exit revenue (scaling paths) ----------------
#   shares = base + slope*(rev - ref) + noise   -> more capacity => more capital => more shares
DIL = {'ref_rev': 60, 'base_shares': 20.0, 'slope': 0.075, 'noise': 1.2}
#   e.g. @ $115M rev -> ~24M shares ; @ $200M -> ~30.5M shares
MUDDLE_SHARES = (28, 30, 40)             # muddle dilutes brutally (low prices)

# ---- Net debt at exit ($M): mild rise with revenue (scaling), flat (muddle)
#   +$0.5M vs prior anchors for the Jun-2026 $1.0M working-capital loan (Kaufman, 8%)
#   funding the Sam's Club everyday-placement production ramp.
NDV          = {'base': 9.5, 'slope': 0.04, 'ref_rev': 90}   # @ $200M -> ~$13.9M
NETDEBT_MUD  = 8.5

# ---- TIME to exit (years) -------------------------------------------------
#   acquired: correlated with revenue (bigger exit => longer): @75->4, @115->~5, @220->~7.5
TCORR        = {'ref_rev': 75, 'base_years': 4.0, 'slope': 0.0241, 'noise': 0.7}
YEARS_PUBLIC = (4, 5, 6)
YEARS_MUDDLE = (4, 5, 6)

# ---- Failure residual equity value per share (triangular) -----------------
FAIL_VPS   = (0.0, 0.10, 0.50)
FAIL_YEARS = (1, 2, 3)                    # residual realised over a short wind-down, then discounted

print("Control panel loaded.")
print(f"  Sims {N_SIMS:,} | Discount {DISCOUNT:.0%} | Price ${PRICE_NOW:.2f} | Shares now {SHARES_NOW:.2f}M")
print(f"  P(scaling works) = {P['scale_public']+P['scale_acquired']:.0%}  "
      f"[public {P['scale_public']:.0%} + acquired {P['scale_acquired']:.0%}]  |  "
      f"muddle {P['muddle']:.0%} | failure {P['failure']:.0%}")
print(f"  Acquired revenue tail reaches ${REV['scale_acquired'][2]:.0f}M (super-bull lives here)")""")

# ---------------------------------------------------------------- engine
md(r"""## 2. Monte Carlo Engine

Each draw picks a path by probability, then within the path:
`EV = revenue × multiple → equity = EV − net debt → per-share → discount to today`.

**Correlations in the scaling paths** (the new physics): exit **shares rise with revenue**
(more capacity ⇒ more capital ⇒ more dilution), and for the **acquired** path **time-to-exit rises
with revenue** (a \$200M exit lands ~7–8 yr out, not 5). This is what keeps the super-bull tail honest
instead of rewarding big revenue with no cost.""")
code(r"""def tri(rng, p, k): return rng.triangular(p[0], p[1], p[2], k)

def run_mc(probs=P, rev=REV, mult=MULT, dil=None, dil_base=None, muddle_shares=MUDDLE_SHARES,
           ndv=NDV, netdebt_mud=NETDEBT_MUD, tcorr=TCORR, years_public=YEARS_PUBLIC,
           years_muddle=YEARS_MUDDLE, fail_vps=FAIL_VPS, fail_years=FAIL_YEARS,
           discount=DISCOUNT, n=N_SIMS, seed=42):
    # Returns DataFrame: path label, present value per share, and exit (undiscounted) price.
    # Every random draw flows through this single rng, so `seed` fully controls reproducibility.
    dil = dict(DIL) if dil is None else dil
    if dil_base is not None: dil = {**dil, 'base_shares': dil_base}
    rng = np.random.default_rng(seed)
    names = list(probs.keys())
    paths = rng.choice(len(names), size=n, p=np.array([probs[k] for k in names]))
    pv = np.empty(n); exitp = np.full(n, np.nan)

    for i, name in enumerate(names):
        mask = paths == i; k = int(mask.sum())
        if k == 0: continue
        if name == 'failure':
            yrs = tri(rng, fail_years, k)                                       # residual discounted, like every path
            pv[mask] = tri(rng, fail_vps, k) / (1 + discount) ** yrs; continue
        if name == 'muddle':
            ev  = tri(rng, rev['muddle'], k) * tri(rng, mult['muddle'], k)
            sh  = tri(rng, muddle_shares, k); yrs = tri(rng, years_muddle, k)
            ep  = np.maximum(ev - netdebt_mud, 0) / sh
            exitp[mask] = ep; pv[mask] = ep / (1 + discount) ** yrs; continue
        # ---- scaling paths: correlated drivers ----
        r   = tri(rng, rev[name], k); m = tri(rng, mult[name], k)
        sh  = np.clip(dil['base_shares'] + dil['slope'] * (r - dil['ref_rev'])
                      + rng.normal(0, dil['noise'], k), 17, None)               # dilution ~ revenue
        nd  = np.maximum(ndv['base'] + ndv['slope'] * (r - ndv['ref_rev']), 0)  # net debt ~ revenue
        if name == 'scale_acquired':
            yrs = np.clip(tcorr['base_years'] + tcorr['slope'] * (r - tcorr['ref_rev'])
                          + rng.normal(0, tcorr['noise'], k), 2.5, 9)           # time ~ revenue
        else:
            yrs = tri(rng, years_public, k)
        ep  = np.maximum(r * m - nd, 0) / sh
        exitp[mask] = ep; pv[mask] = ep / (1 + discount) ** yrs

    return pd.DataFrame({'path': [names[p] for p in paths], 'pv': pv, 'exit_price': exitp})

sim = run_mc()
print(f"Ran {len(sim):,} simulations. Mean implied exit shares (acquired) "
      f"≈ {(DIL['base_shares']+DIL['slope']*(115-DIL['ref_rev'])):.1f}M at $115M revenue.")
sim.head()""")

# ---------------------------------------------------------------- results
md("## 3. Headline Result — Expected Value & Distribution")
code(r"""pv = sim['pv'].values
exp_val = pv.mean(); median = np.median(pv); upside = exp_val / PRICE_NOW - 1
pctiles = {p: np.percentile(pv, p) for p in [5, 10, 25, 50, 75, 90, 95]}

print("="*60)
print(f"  Current price ...................... ${PRICE_NOW:>7.2f}")
print(f"  Probability-weighted EXPECTED value  ${exp_val:>7.2f}   ({upside:+.0%} vs price)")
print(f"  Median outcome ..................... ${median:>7.2f}")
print(f"  Expected return multiple ........... {exp_val/PRICE_NOW:>7.2f}x")
print("-"*60); print("  Percentiles of per-share PV:")
for p, v in pctiles.items(): print(f"    P{p:<2} .......... ${v:>7.2f}")
print("-"*60)
P_total_loss = (pv < 0.50).mean(); P_loss = (pv < PRICE_NOW).mean()
P_2x = (pv >= 2*PRICE_NOW).mean(); P_3x = (pv >= 3*PRICE_NOW).mean(); P_5x = (pv >= 5*PRICE_NOW).mean()
print("  Outcome probabilities (PV vs today's price):")
print(f"    Near-total loss (<$0.50) .. {P_total_loss:>5.1%}")
print(f"    Below today's price ....... {P_loss:>5.1%}")
print(f"    >= 2x ..................... {P_2x:>5.1%}")
print(f"    >= 3x ..................... {P_3x:>5.1%}")
print(f"    >= 5x ..................... {P_5x:>5.1%}")""")

code(r"""fig, ax = plt.subplots(1, 2, figsize=(14, 5))
clip = np.percentile(pv, 99)
ax[0].hist(np.clip(pv, 0, clip), bins=80, color='#3d5a6e', edgecolor='white', linewidth=0.3)
ax[0].axvline(PRICE_NOW, color='#c0392b', lw=2, ls='--', label=f'Price ${PRICE_NOW:.2f}')
ax[0].axvline(exp_val, color='#27ae60', lw=2, label=f'E[value] ${exp_val:.2f}')
ax[0].axvline(median, color='#f39c12', lw=2, ls=':', label=f'Median ${median:.2f}')
ax[0].set_title('Distribution of per-share present value', fontweight='bold')
ax[0].set_xlabel('PV per share ($)'); ax[0].set_ylabel('Frequency'); ax[0].legend()

order = ['failure', 'muddle', 'scale_public', 'scale_acquired']
contrib = sim.groupby('path')['pv'].agg(['mean', 'count'])
contrib['prob'] = contrib['count'] / len(sim)
contrib['contribution'] = contrib['mean'] * contrib['prob']
contrib = contrib.loc[order]
colors = ['#c0392b', '#e67e22', '#2980b9', '#27ae60']
ax[1].bar(contrib.index, contrib['contribution'], color=colors, edgecolor='white')
ax[1].set_title('Contribution to expected value by path', fontweight='bold')
ax[1].set_ylabel('Prob-weighted $/share'); ax[1].tick_params(axis='x', rotation=20)
for x, v in zip(range(len(contrib)), contrib['contribution']):
    ax[1].text(x, v, f'${v:.2f}', ha='center', va='bottom', fontweight='bold')
plt.tight_layout(); plt.show()""")

# ---------------------------------------------------------------- per-path
md("## 4. Per-Path Breakdown")
code(r"""tbl = sim.groupby('path')['pv'].agg(
    prob=lambda s: len(s)/len(sim), mean_value='mean', median_value='median',
    p10=lambda s: s.quantile(.10), p90=lambda s: s.quantile(.90))
tbl['contribution'] = tbl['prob'] * tbl['mean_value']; tbl = tbl.loc[order]
tbl.loc['— BLENDED —'] = [1.0, exp_val, median, np.percentile(pv,10),
                          np.percentile(pv,90), tbl['contribution'].sum()]
disp = tbl.copy(); disp['prob'] = (disp['prob']*100).round(1).astype(str)+'%'
for c in ['mean_value','median_value','p10','p90','contribution']:
    disp[c] = '$'+disp[c].round(2).astype(str)
disp""")

# ---------------------------------------------------------------- super-bull readout
md(r"""## 5. Super-Bull Readout — the \$200M tail of the acquired path

The "scale further to ~\$200M, then sell" outcome is **not a separate scenario** — it's the upper tail
of path 4. Below: the acquired-path distribution (so you can *see* the tail), plus the deterministic
\$200M case worked through with its honest time-and-dilution drag.""")
code(r"""acq = sim[sim.path=='scale_acquired']
print("Acquired-path distribution (conditional on the path happening):")
for p in [50, 75, 90, 95, 99]:
    print(f"   P{p:<2}: exit ${np.percentile(acq.exit_price,p):>6.2f}  -> PV today ${np.percentile(acq.pv,p):>6.2f}")
print(f"   P(acquired exit price > $20) = {(acq.exit_price>20).mean():.0%} | > $30 = {(acq.exit_price>30).mean():.0%}")
print()
# Deterministic $200M super-bull, fully costed
def costed(rev_exit, mult_exit):
    sh  = DIL['base_shares'] + DIL['slope']*(rev_exit-DIL['ref_rev'])
    nd  = NDV['base'] + NDV['slope']*(rev_exit-NDV['ref_rev'])
    yrs = TCORR['base_years'] + TCORR['slope']*(rev_exit-TCORR['ref_rev'])
    ev  = rev_exit*mult_exit; eq = ev-nd; exitp = eq/sh; pvv = exitp/(1+DISCOUNT)**yrs
    return sh, nd, yrs, ev, exitp, pvv
print("Deterministic 'scale-further-then-sell' cases (mode path):")
print(f"{'Revenue':>9}{'Mult':>6}{'Shares':>8}{'NetDebt':>9}{'Years':>7}{'EV $M':>8}{'Exit $':>9}{'PV $':>8}{'x price':>9}")
for r_, m_ in [(115,4.0),(150,4.25),(200,4.25),(220,4.5)]:
    sh,nd,yr,ev,exq,pvv = costed(r_,m_)
    print(f"{r_:>9.0f}{m_:>6.2f}{sh:>8.1f}{nd:>9.1f}{yr:>7.1f}{ev:>8.0f}{exq:>9.2f}{pvv:>8.2f}{pvv/PRICE_NOW:>8.1f}x")""")

# ---------------------------------------------------------------- dilution table
md(r"""## 6. Dilution Sensitivity Table  ⬅ *requested*

Vary the **dilution intercept** (`base_shares`) — i.e. how share-heavy the scaling journey is.
Shown as the implied diluted share count at the ~\$115M revenue mode, with the resulting blended
expected value, upside, and acquired-path value. Second axis: the acquisition EV/Revenue multiple.""")
code(r"""dil_bases = [16, 18, 20, 23, 26]      # intercept; implied shares @ $115M = base + 0.075*55 = base+4.1
rows = []
for b in dil_bases:
    s = run_mc(dil_base=b, seed=7); pvd = s['pv'].values
    acqv = s.loc[s.path=='scale_acquired','pv'].values
    sh115 = b + DIL['slope']*(115-DIL['ref_rev'])
    rows.append({'Shares @ $115M (M)': round(sh115,1),
                 'Dilution vs today': f"{sh115/SHARES_NOW-1:+.0%}",
                 'Blended E[value]': pvd.mean(),
                 'Upside vs $4.28': f"{pvd.mean()/PRICE_NOW-1:+.0%}",
                 'Acquired-path E[value]': acqv.mean(),
                 'P(>=2x)': f"{(pvd>=2*PRICE_NOW).mean():.0%}"})
dil1d = pd.DataFrame(rows)
for c in ['Blended E[value]','Acquired-path E[value]']:
    dil1d[c] = '$'+dil1d[c].round(2).astype(str)
print("Dilution sensitivity — blended expected value & upside:")
dil1d""")

code(r"""mult_modes = [3.5, 4.0, 4.5]
grid = np.zeros((len(dil_bases), len(mult_modes)))
for r_, b in enumerate(dil_bases):
    for c_, m in enumerate(mult_modes):
        mu = dict(MULT); mu['scale_acquired'] = (m-0.5, m, m+1.0)
        s = run_mc(dil_base=b, mult=mu, seed=11)
        grid[r_, c_] = s.loc[s.path=='scale_acquired','pv'].mean()
idx = [f"{b+DIL['slope']*(115-DIL['ref_rev']):.0f}M ({(b+DIL['slope']*55)/SHARES_NOW-1:+.0%})" for b in dil_bases]
grid2d = pd.DataFrame(grid, index=idx, columns=[f"{m:.1f}x" for m in mult_modes])
grid2d.index.name = 'Exit shares (dilution)'

fig, ax = plt.subplots(figsize=(9, 5))
im = ax.imshow(grid2d.values, cmap='RdYlGn', aspect='auto')
ax.set_xticks(range(len(mult_modes))); ax.set_xticklabels([f"{m:.1f}x EV/Rev" for m in mult_modes])
ax.set_yticks(range(len(dil_bases))); ax.set_yticklabels(grid2d.index)
ax.set_title('Acquired-path PV/share — dilution vs exit multiple', fontweight='bold')
ax.set_xlabel('Acquisition EV/Revenue (mode)'); ax.set_ylabel('Implied exit shares (dilution vs today)')
for r_ in range(len(dil_bases)):
    for c_ in range(len(mult_modes)):
        ax.text(c_, r_, f'${grid2d.values[r_,c_]:.2f}', ha='center', va='center', fontweight='bold')
plt.colorbar(im, label='PV/share ($)'); plt.tight_layout(); plt.show()
grid2d.round(2)""")

# ---------------------------------------------------------------- other sensitivities
md("## 7. Other Sensitivities — Probability of Scaling & Discount Rate")
code(r"""scaling_probs = [0.40, 0.50, 0.58, 0.66, 0.75]
acq_share = P['scale_acquired'] / (P['scale_public'] + P['scale_acquired'])
rows = []
for sp in scaling_probs:
    pp = {'failure': P['failure'], 'muddle': 1 - P['failure'] - sp,
          'scale_acquired': sp*acq_share, 'scale_public': sp*(1-acq_share)}
    v = run_mc(probs=pp, seed=5)['pv'].values
    rows.append({'P(scaling works)': f"{sp:.0%}", 'P(muddle)': f"{pp['muddle']:.0%}",
                 'E[value]': f"${v.mean():.2f}", 'Upside': f"{v.mean()/PRICE_NOW-1:+.0%}",
                 'P(>=2x)': f"{(v>=2*PRICE_NOW).mean():.0%}", 'P(loss)': f"{(v<PRICE_NOW).mean():.0%}"})
print("Sensitivity to P(scaling works):")
print(pd.DataFrame(rows).to_string(index=False))
print("\nSensitivity to discount rate:")
rows = []
for dr in [0.10, 0.12, 0.15, 0.175, 0.20]:
    ev = run_mc(discount=dr, seed=3)['pv'].mean()    # run once; E[value] and Upside from the same sample
    rows.append({'Discount': f"{dr:.1%}", 'E[value]': f"${ev:.2f}", 'Upside': f"{ev/PRICE_NOW-1:+.0%}"})
print(pd.DataFrame(rows).to_string(index=False))""")

# ---------------------------------------------------------------- implied prob & CAGR
md(r"""## 8. What the Market Price Implies & Return CAGR by Exit Scenario

Two reads investors actually want: (a) what probability of scaling the **current price** is paying for —
both at face value *and* after the margin of safety micro-cap, not-yet-profitable names warrant — and
(b) the **annualized return (CAGR)** an investor earns from today's price in each constructive exit.""")
code(r"""# (1) Market-implied probability of successful scaling
Pgrid = np.linspace(0.40, 0.75, 8)
acq_share = P['scale_acquired'] / (P['scale_public'] + P['scale_acquired'])
evs = []
for sp in Pgrid:
    pp = {'failure': P['failure'], 'muddle': 1 - P['failure'] - sp,
          'scale_acquired': sp*acq_share, 'scale_public': sp*(1-acq_share)}
    evs.append(run_mc(probs=pp, seed=5)['pv'].mean())
a_fit, b_fit = np.polyfit(Pgrid, evs, 1)
P_for = lambda ev: (ev - b_fit) / a_fit
print("MARKET-IMPLIED PROBABILITY OF SCALING (price ${:.2f})".format(PRICE_NOW))
print(f"  Break-even (price = model fair value): {P_for(PRICE_NOW):.0%}")
print("  Adjusted for a typical micro-cap margin of safety (price = fair value x (1-MoS)):")
for mos in [0.20, 0.25, 0.30, 0.35]:
    fv = PRICE_NOW / (1 - mos)
    print(f"    MoS {mos:.0%}: implied fair value ${fv:.2f}  ->  implied P(scaling) {P_for(fv):.0%}")

# (2) Return CAGR by exit scenario (model-consistent shares, net debt, timing)
shares = lambda rev: DIL['base_shares'] + DIL['slope']*(rev - DIL['ref_rev'])
ndebt  = lambda rev: NDV['base'] + NDV['slope']*(rev - NDV['ref_rev'])
def row(name, rev, mult, yrs):
    ep = (rev*mult - ndebt(rev)) / shares(rev)
    return name, rev, mult, yrs, ep, ep/PRICE_NOW, (ep/PRICE_NOW)**(1/yrs) - 1
scen = [row("Scale & public", 85, 2.80, 5.0), row("Acquired base", 115, 4.00, 5.0),
        row("Acquired", 150, 4.25, 5.8), row("Super-bull $200M", 200, 4.25, 7.0),
        row("Super-bull $220M", 220, 4.50, 7.5)]
print(f"\nRETURN CAGR BY EXIT SCENARIO (entry ${PRICE_NOW:.2f}):")
for name, rev, mult, yrs, ep, x, c in scen:
    print(f"  {name:18s} ${rev:>3.0f}M {mult:.2f}x  {yrs:.1f}yr  exit ${ep:6.2f}  {x:4.1f}x  CAGR {c*100:+5.1f}%")
print(f"  {'Muddle':18s}  (sub-scale)        ~5yr  exit ~$1.22   0.3x  CAGR  -22%")
print(f"  {'Failure':18s}  (equity impaired)               ~ -100% (near-total loss)")""")

# ---------------------------------------------------------------- summary
md("""## 9. Summary

The model returns an **expected value** and a **full distribution**: the central estimate vs the $4.28 price,
*and* the shape of the bet (fat left tail from failure/muddle, fat right tail from a strategic exit).
Re-run with your own probabilities/assumptions in the control panel to make it yours.

Structural findings baked in:
- **Bimodal bet:** ~42% mass collapses toward $0 (failure+muddle); ~58% lands in the win cluster. The case rests on `P(scaling works)`.
- **Dilution risk = operational-scaling risk** — one uncertainty, not two.
- **The exit door (acquired vs stay-public) is immaterial** to the expected value; the super-bull is the *tail* of the acquired path, not a separate scenario.
- **Bigger exits cost time and dilution** — the $200M super-bull is ~2.7x today, not the naive ~13x.
- **Kraft Heinz is a divester** — real acquirers are PepsiCo/Hershey/Mondelez; BFY-snack M&A clusters at 3.6–4.4x EV/Revenue.""")
code(r"""print(f"BOF probabilistic valuation — summary @ price ${PRICE_NOW:.2f}")
print(f"  Expected value : ${exp_val:.2f}  ({upside:+.0%})")
print(f"  Median         : ${median:.2f}")
print(f"  P(>=2x) {P_2x:.0%} | P(loss) {P_loss:.0%} | P(near-total loss) {P_total_loss:.0%}")""")

nb = new_notebook(cells=cells)
nb.metadata = {"kernelspec": {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"},
               "language_info": {"name": "python"}}
with open("bof_financial_model.ipynb", "w") as f:
    nbf.write(nb, f)
print("Wrote bof_financial_model.ipynb with", len(cells), "cells")
