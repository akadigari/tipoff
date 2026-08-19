# Wallet roster

_Auto-generated 2026-08-19T01:47:37Z. 1178 flagged wallets, 13 with enough graded trades to judge, 2 that beat a coin flip._

Each wallet is graded on the price move that followed its flagged
trades, in the wallet's own direction, using data the scanner
already collected. A wallet earns WATCH only with at least
12 graded moves, a positive average, and a hit rate that
beats a coin flip (p < 0.05). Averages are in cents of probability.

**Read this before trusting the list.** These wallets were surfaced
by detectors the self-audit (LEARNING.md) calls noise, so the pool
leans toward market makers and busy whales, not quiet insiders. A
high flag count is a reason for suspicion, not trust: real insiders
in the documented cases traded once, in one market, then vanished.
The grading below is exactly what separates the two.

## Watch list (earned it)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xfc2f4f50ce...` | 20 | +3.55c | 72% | 0.05 | 11 | 49 | WATCH (beats luck) |
| `0xe734e7bf7c...` | 23 | +2.74c | 83% | 0.00 | 8 | 103 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

_None yet._

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xfc2f4f50ce...` | 20 | +3.55c | 72% | 0.05 | 11 | 49 | WATCH (beats luck) |
| `0xe734e7bf7c...` | 23 | +2.74c | 83% | 0.00 | 8 | 103 | WATCH (beats luck) |
| `0xeb490d0534...` | 24 | +0.99c | 68% | 0.07 | 13 | 43 | NOISE (busy, not sharp) |
| `0x06dc51826b...` | 31 | +0.90c | 70% | 0.02 | 28 | 138 | NOISE (busy, not sharp) |
| `0x88c4919de7...` | 12 | +0.48c | 50% | 0.62 | 12 | 24 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 14 | +0.40c | 50% | 0.61 | 25 | 98 | NOISE (busy, not sharp) |
| `0x35bbbad241...` | 12 | -0.25c | 25% | 0.98 | 10 | 37 | NOISE (busy, not sharp) |
| `0x6765c1c000...` | 18 | -0.31c | 57% | 0.39 | 6 | 31 | NOISE (busy, not sharp) |
| `0x000d257d2d...` | 13 | -0.58c | 46% | 0.71 | 12 | 27 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 27 | -0.63c | 46% | 0.73 | 36 | 104 | NOISE (busy, not sharp) |
| `0x6d9fc316c3...` | 13 | -0.81c | 33% | 0.93 | 9 | 50 | NOISE (busy, not sharp) |
| `0xe234959595...` | 15 | -1.56c | 33% | 0.93 | 12 | 46 | FADE (bets the wrong way) |
| `0xb10047d6a2...` | 23 | -3.64c | 48% | 0.67 | 21 | 58 | FADE (bets the wrong way) |

## Documented known insiders (Phase B watch targets)

Publicly-reported insider wallets from the backtest episodes, by the pseudonym the reporting used. On-chain addresses still need resolving before they can be watched live, and most are likely burned (insiders rotate addresses). Tripwires, not a strategy.

| Pseudonym | Episode |
|---|---|
| 6741 | Nobel Peace Prize 2025 leak (Machado) |
| dirtycup | Nobel Peace Prize 2025 leak (Machado) |
| Magamyman | US strike on Iran, Feb 2026 (six fresh wallets) |
| Planktonbets | US strike on Iran, Feb 2026 |
| bigwinner01 | Trump pardons CZ, Oct 2025 |
| romanticpaul | Taylor Swift engagement, Aug 2025 |
| ricosuave666 | IAF reservist / Rising Lion, June 2025 (indicted) |

## Next step

If the watch list stays empty or tiny once normal mode fills the
data, wallet-first is not worth the API budget and we do not build
Phase B. If real names keep earning WATCH, Phase B polls those
wallets every run and alerts the moment they open a new position,
before the market is anomalous.
