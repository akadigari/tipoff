# Wallet-first pivot: prior art and the honest edge picture

Multi-agent web survey run 2026-07-19 (GitHub, Reddit/forums, commercial
products, academic papers) to answer one question before building further:
has anyone built the "watch a graded roster of known insider wallets and
follow their new bets" loop, and does following insiders actually pay?

## Are we original? Partial, and precisely so

**The bare wallet-follow loop is fully commoditized.** A dozen-plus tools
already let you follow a specific wallet and get pinged on its new bets:
Polywhaler, Stand.Trade/Copycat, Poly Syncer, Polycopy, PolyTradeAlerts,
OddAlerts, the open-source `braedonsaunders/homerun`, and most directly
**polyloly**, which even tail-backtests the strategy on a live cron and
publishes a `/insider-picks` endpoint. We are not first to wallet-following.

**But every one of them selects wallets by raw win-rate, PnL, or Sharpe** —
exactly the luck-contaminated selection the academic work warns against. The
full-universe Polymarket studies (Gomez-Cram et al.; Nechepurenko, arXiv
2605.02287) find only ~3.14% of profitable wallets are genuinely skilled;
~29% are lucky. The sign-randomization luck test that separates them exists
**only in papers, never wired into a live follow loop.** roster.py sits in
that open slice.

**Two things appear genuinely unbuilt anywhere, commercial or academic:**

1. **A luck-test gate on a live wallet roster** — only follow wallets whose
   hit rate beats a coin-flip null. polyloly rosters by raw win-rate; the
   academics luck-test offline and stop. Nobody joins the two.
2. **Per-trigger + per-category CLV self-audit of the tool's own alerts**
   (learn.py), with the falsifiable "alerted vs filtered-out" control at
   fixed horizons. Three independent ecosystem surveys and the arXiv
   taxonomy explicitly document this as missing field-wide. One signal bot
   (`mmoore07129/mlb-kalshi-bot`) does CLV self-grading, but it has no
   wallet/insider dimension. Nobody grades their own *insider-money* alerts
   by closing-line value.

Plus: excluding play-determined sports as a first-class taxonomy (not just
noise-filtering), and the whole synthesis in one serverless paper-first
tool, are not combined anywhere.

**Verdict: not original on wallet-following; original on the rigor.** The
hardest-to-copy piece is the CLV alert self-audit. The luck-tested roster is
the second.

## The honest reality check (read before dreaming of money)

The informed-money *signal* is real and academically validated (skilled
order flow predicts next-period price; flagged traders hit 69.9% win rate at
>60 standard deviations; the lifecycle heuristic pinned the indicted
Venezuela wallet to the dollar). **But a tradeable forward "follow known
insiders for profit" edge is unproven and shows multiple decay signals:**

1. Only ~44% of "skilled" labels persist out-of-sample. More than half of
   any proven roster stops being skilled.
2. The biggest edge comes from **one-shot insiders who bet once and vanish**
   — unfollowable by construction, and **the luck test itself excludes
   them.** This is the core tension: the luck test protects you from
   market-makers but filters out the juiciest insiders. A luck-tested roster
   is the safe repeatable players, not the leak-of-the-week.
3. polyloly's headline +46.7% ROI is a zero-slippage upper bound, cut to
   +15-25% on realistic fills, and even that forward number is unaudited.
4. Naive backtests overstate returns 30-100%; latency is nonzero; last
   quarter's edge gets arbitraged out.
5. Sharps actively evade copiers (secondary accounts, iceberging, merging).
6. **Kalshi has no wallets** — wallet-first is Polymarket-only; Kalshi must
   fall back to order-flow microstructure.

**Bottom line: Tipoff is an instrument that measures whether the edge
survives, not a money printer.** That measurement honesty — the CLV
self-audit, the luck-tested roster, and the built-in falsifier ("empty watch
list => don't build Phase B") — is the genuinely defensible, interview-ready
contribution.

## What to steal (ranked backlog, do not build all at once)

1. **True CLV, both spaces** (from mmoore07129): snapshot the sharp/fair
   close for every analyzed market and report CLV in probability-space AND
   ROI-space, upgrading learn.py's fixed-horizon forward-move proxy into
   real closing-line value. Highest value: makes the audit interview-solid.
2. **Slippage haircut in the gate** (from polyloly): bake a ~3c lag/slippage
   cut directly into the followability gate so paper numbers stop being
   upper bounds.
3. **Farmer filter + NegRisk correction** (from OrcaLayer): strip
   airdrop-farmer wallets (~16% of the raw leaderboard) and neg-risk
   arbitrage before the luck test, so the roster is not pre-polluted.
4. **Brier / calibration as a second skill lens** (from runesleo, Convexly)
   beside the coin-flip test: separates skilled predictors from
   market-makers.
5. **Actionable FADE verdicts** (from OpenThomas): a trigger that reads FADE
   should auto-propose an invert/drop as a tracked action, not just prose.
6. **Encode sharp-evasion as followability failures**: secondary accounts,
   iceberging, position merging.
7. **Resolve KNOWN_INSIDERS pseudonyms to on-chain addresses** to turn the
   documented episodes into live tripwires.

## Closest competitors (for the record)

- **polyloly** — the wallet-first tail loop, live cron, paper-first, public;
  selects by raw win-rate (luck-contaminated), self-audit admitted-not-run.
- **mmoore07129/mlb-kalshi-bot** — real CLV self-grading, universe-wide
  close snapshots; signal-first, zero wallet/insider dimension.
- **braedonsaunders/homerun** — bundles nearly every Tipoff block (whale
  discovery, copy-trading, 27-point anomaly score, backtester, serverless)
  except the two rigor layers.
- **Polywhaler + Orca** — closest commercial: dual-venue, watchlist-follow,
  per-trade insider score, coordination detector, paper-then-live; no CLV
  audit, no luck test.
- **Gomez-Cram et al. / Nechepurenko** — the peer-reviewed twin of the luck
  test; offline classification only, never a live follow loop, and
  explicitly measures no CLV.
