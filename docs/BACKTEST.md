# Backtest: replaying documented insider episodes

Run 2026-07-11: a multi-agent forensic replay of Tipoff's detectors against
**documented, sourced insider-trading episodes** on prediction markets,
using real historical data (Gamma market records, CLOB hourly price
history, on-chain trade tapes, wallet activity). Full detector spec was
simulated hour-by-hour with proper warm-up.

## Episodes and scoreboard

| Episode | Evidence quality | Verdict |
|---|---|---|
| **Nobel Peace Prize 2025 leak** (Machado, 3.7¢→39¢→71¢ ~10h pre-announcement; Nobel Institute confirmed a system breach) | high: institutional leak probe | CAUGHT_BUT_GATED: score 125 for ten straight hours, every alert killed by the 24h-to-close gate |
| **US strike on Iran, Feb 2026** (six fresh wallets, ~$1.2M; Bubblemaps/Forbes/Mitts & Ofir) | high | CAUGHT: fresh-wallet+large-trade fired on the documented wallets at T-57h/T-32h/T-7h, gate passed |
| **IAF reservist leak, June 2025** (criminal indictment, classified strike date → Polymarket bets) | highest: criminal charges | CAUGHT: score 96 at T-12h, entry 0.11, +809% if followed |
| **Trump pardons CZ, Oct 2025** (bigwinner01, ~$28k hours early) | medium | CAUGHT_BUT_GATED: archetype scored 40 (<55) and the 90-day cap blocked the window anyway |
| **Taylor Swift engagement, Aug 2025** (buys minutes before a privately-scheduled announcement) | medium | CAUGHT_BUT_GATED: scored 45; 90-day cap blocked the market its entire life (Dec-31 backstop date, resolved in Aug) |
| **Astronomer CEO resignation, July 2025** | low (public scandal, momentum not MNPI) | CAUGHT, but validates recall, not insider precision |
| George Santos Kalshi self-bet (Feb 2026, DOJ probe) / Maduro capture (Burdensome-Mix) | high / medium | NOT_TESTED: Kalshi ticker unpublished / market ambiguous. Open replay targets. |

**Headline: detectors fired before the news in 6 of 6 reconstructed
episodes. The failures were self-inflicted: the followability gate and the
aggregate score threshold, not detection.**

## Fixes adopted (2026-07-11), each tied to an episode

1. **Stale-clock handling**: a Gamma `endDate` was a *month in the past*
   on an active market (Iran), making hours-to-close negative and silently
   suppressing everything. Unknown/stale clocks now read as "unknown" and
   skip time checks instead of failing them.
2. **MONITOR-grade alerts**: the gate is now advisory, not silencing:
   strong-but-gated signals send a distinct "👀 MONITOR: strong signal,
   gated" Telegram alert with the gate reasons attached. They are never
   logged to the ledger (that would poison the CLV verdict). A score-125 signal the
   user never sees is a system failure; the Nobel leak now reaches your
   phone as intel.
3. **Insider-archetype bypass**: fresh wallet + large same-wallet trade
   alerts regardless of aggregate score. On the Iran replay this conjunction
   alone flagged exactly the six documented insider wallets; in three other
   episodes it scored 40-45 and died under the 55 bar.
4. **Direction from the informed wallet**: on the Iran replay, every
   insider hour's *largest* print was a wrong-side whale; copying the
   biggest trade loses 100%, copying the fresh wallet's side makes +890%.
   Side selection now prioritizes: fresh wallet > flagged large trade >
   other signals > drift, and alerts state whose side it is.
5. **Extreme-repricing exemption**: a ≥15¢ move or ≥5× odds change is
   never "scheduled news drift"; the proxy no longer suppresses it (the
   Nobel bar survived by 71 minutes on one clock and died on the other).
6. **Dollar volume floor**: the 300-*share* spike floor was $2 on a penny
   market and noise-fired 18 times in 3.75 days on the Nobel replay; now
   $500 of actual dollars.
7. **Fresh-wallet exemption from the 90-day cap**: event-triggered markets
   carry backstop close dates ("…by Dec 31") but resolve on announcement;
   the cap had blocked the only true insider alert of the CZ episode and
   the Swift market for its entire life.
8. **Pseudonym-epoch wallet age**: unrenamed Polymarket accounts encode
   creation time in their default name (`0xADDR-<epoch-ms>`); used as a
   second freshness source since `/activity` prunes history.

## Known gaps, deliberately not yet built (need out-of-sample validation)

- **Coordination detector** (≥3 wallets, same second, same side, the Iran
  Feb 27 signature: eight wallets at 23:41:57/59). Single-episode evidence;
  measure the base rate on ordinary markets first.
- **Cumulative quiet accumulation** (passive limit-fill buildup never
  triggers per-trade thresholds, bigwinner01's $15k of 33¢ fills; rolling
  2-3h scoring windows).
- **ADV-normalized thresholds** (fixed floors alert 33% of all hours on a
  $90M market and are dust on penny markets).
- **12h gate floor / realized-liquidity gate**, graded 14-day freshness,
  market-age labels: see the synthesis in the session notes.

## Honest caveats (read before trusting the scoreboard)

- **Survivorship bias**: episodes were chosen because insiders got caught.
  This measures recall on known positives; precision claims are anecdotal
  (fragments are alarming: 33% of hours alerted on the Iran market).
- **Overfitting risk**: 13 recommended changes derived from 6 episodes and
  evaluated on the same 6. The adopted set is the conservative subset; the
  held-out episodes (Santos, Maduro) and the calibration-week live data are
  the out-of-sample check.
- **Hindsight**: analysts knew which market and window to examine. A live
  scanner must find these markets without a Forbes article pointing at them,
  and several weren't findable via the primary API path at all.
- **Maker-side accumulation is invisible** in taker-only tapes: the quiet
  insiders (dirtycup ~$70k, Swift's $12k→$52k trader) left no footprint the
  scanner can see. Some "CAUGHT" verdicts credit us for the *noisy* insider
  while the quiet one walked past.
- **All profit figures assume printed-price fills** with zero slippage:
  upper bounds, not expectations.
