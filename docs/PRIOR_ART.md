# Prior art — who else built this, and what they added

Multi-agent web survey run 2026-07-11 across five beats: the Polymarket
whale-tracking ecosystem, Kalshi tooling, academic work on informed trading
in prediction markets, sports-betting steam/CLV services (the most mature
"follow smart money" industry), and crypto smart-money analytics.

## The landscape

| Tool | What it is |
|---|---|
| [Polymaster](https://github.com/neur0map/polymaster) | Closest open-source analog: dual-platform (Polymarket + Kalshi) whale watcher, per-wallet SQLite memory, repeat-actor and side-flip flags |
| [pselamy/polymarket-insider-tracker](https://github.com/pselamy/polymarket-insider-tracker) | Open-source insider pipeline with concrete published thresholds; near-identical architecture to Tipoff (public APIs, no indexing, Telegram) |
| [Polywhaler](https://polywhaler.com/) | Commercial: insider risk score (big bets at long odds), watchlist-consensus alerts, paper-trading simulator |
| [OrcaLayer Whales](https://orcalayer.com/whales) | Best published smart-money badge: per-resolved-market win rate ≥55% + positive PnL + ≥10 resolved markets, with farmer/bot noise filters |
| [FORCASTR](https://forcastr.market/) | Commercial Kalshi-only intelligence terminal: tiered whale alerts, 60-second cadence |
| [CrossOdds](https://www.crossodds.app/) | Kalshi+Polymarket whale dashboard; admits Kalshi whales stay anonymous (no wallet data) |
| [PolyTerm](https://github.com/NYTEMODEONLY/polyterm) | Open-source terminal: smart-money filter (>70% win rate, 10+ trades), wash-trade detection |
| [Kalshi-smart-money](https://github.com/vortexpixelz/Kalshi-smart-money) | ML library: VPIN/PIN microstructure detectors with ensemble weights learned from graded outcomes |
| [Pikkit](https://pikkit.com/closing-line-value) | Sports bet tracker that auto-grades CLV per bet/tag — the commercial twin of Tipoff's grading loop |
| [Mitts & Ofir 2026](https://corpgov.law.harvard.edu/2026/03/25/from-iran-to-taylor-swift-informed-trading-in-prediction-markets/) | Academic screen over 93k Polymarket markets: five-signal composite flagged $143M in anomalous profits |

Two structural findings worth remembering:

1. **Nobody grades their own alerts.** No surveyed tool — commercial or
   open-source — publishes an audited record of whether following its alerts
   beat the closing line. Tipoff's per-category CLV table is the
   differentiator; everything adopted below extends it rather than copying
   features that lack a feedback loop.
2. **The sports industry already ran this experiment.** Steam-chasing
   (following sharp line moves) worked, got crowded, and died — followers
   were late, alerts moved lines themselves, and books limited winners. The
   survivors pivoted to fair-value pricing. Two lessons transfer: measure
   follower lateness obsessively (CLV, which Tipoff does), and note that
   exchange-model prediction markets *cannot ban winners* — a real
   structural advantage for this niche.

## Adopted into Tipoff (2026-07-11)

| Feature | Borrowed from |
|---|---|
| **Per-trigger CLV table** in REPORT.md — grades every signal type separately; a trigger with negative CLV is a fade signal, whatever its win rate | Sports Insights' per-book steam records; Pikkit tag-level CLV |
| **Price-impact-per-volume signal** — ≥3¢ move on volume the market usually absorbs silently (insider trades measured moving prices 7–12× more per dollar) | Mitts & Ofir 2026 |
| **Within-trader bet size** — a trade ≥5× the wallet's own median is informative even if small in absolute terms | Mitts & Ofir composite; pselamy |
| **Repeat-actor wallet memory** — persistent cross-scan map of flagged wallets; re-flags and side-flips escalate | Polymaster's per-wallet SQLite memory |
| **Signal count in alerts** ("3 signals") — composite evidence beats any single trigger | pselamy's stacked-confidence bonuses; Action Network |
| **Research dataset** (signals.csv with 1h/6h/24h forward prices) — the raw material for the follow-vs-fade table nobody has published | gap identified by the survey |

Already built before the survey, independently validated by it: CLV grading
(unique), the followability gate (academically supported — thin markets
underreact and drift), fresh-wallet flag (matches the documented insider
pattern: six fresh wallets made ~$1.2M on the Oct 2024 Iran-strike market),
cross-platform confirmation, thin-market bonus, paper-trading loop.

## Roadmap (not yet built, in rough priority order)

1. **Lazy wallet grading + smart-money badge** — when a wallet trips a
   signal, pull its history and compute an OrcaLayer-style badge (win rate
   ≥55% per resolved market, positive PnL, ≥10 resolved), gated by the
   sign-randomization luck test from the wallet_screener project. Badged
   wallets boost alerts; ≥2 badged wallets on the same side = consensus
   alert. (medium effort)
2. **Funding-source classification** — label a fresh wallet's first USDC
   inflow via free eth-labels dumps: CEX (KYC'd retail-ish) vs bridge
   (opaque) vs another fresh wallet (Sybil smell). (medium)
3. **Same-funder cluster detection** — ≥2 wallets sharing a funding parent
   entering one market side = the documented Iran-strike pattern, which no
   per-wallet threshold can catch. (medium)
4. **Burst mode** — when a preliminary signal fires, re-poll that market
   every ~60s for the rest of the Actions job before alerting. (medium)
5. **Cross-venue fair-value gate** — for dual-listed markets, alert only if
   the catchable price still deviates from the liquidity-weighted blended
   mid: "price still wrong" instead of "price still catchable". (medium)
6. **Deadline/leak-window weighting** — pre-arm lower thresholds in
   decision-to-announcement windows (the Nobel-prize template). (low)

## Open gaps in the field (what this data could uniquely answer)

- The first audited alert track record in the prediction-market space
  (CLV table + a sign-randomization null over the paper ledger).
- The first published follow-vs-fade table per signal type (is fresh-wallet
  a follow in politics but a fade in sports?).
- The edge-decay curve for an hourly scanner: where is 1-hour latency still
  fast enough? (sports lore says 60 seconds on liquid markets — nobody has
  measured it here)
- Wallet-free informed-flow detection for Kalshi (every wallet technique is
  Polymarket-only; Kalshi traders are anonymous).
- Manipulation-vs-informed labeling: informed moves persist, manipulative
  moves revert — the CLV loop already implicitly measures this.
