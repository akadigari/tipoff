# Wallet roster

_Auto-generated 2026-08-19T04:46:28Z. 1167 flagged wallets, 13 with enough graded trades to judge, 1 that beat a coin flip._

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
| `0xe734e7bf7c...` | 24 | +2.60c | 79% | 0.00 | 8 | 103 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xfc2f4f50ce...` | 16 | +2.78c | 64% | 0.21 | 10 | 49 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xfc2f4f50ce...` | 16 | +2.78c | 64% | 0.21 | 10 | 49 | PROMISING (edge, luck not ruled out) |
| `0xe734e7bf7c...` | 24 | +2.60c | 79% | 0.00 | 8 | 103 | WATCH (beats luck) |
| `0x06dc51826b...` | 31 | +0.90c | 70% | 0.02 | 28 | 138 | NOISE (busy, not sharp) |
| `0xeb490d0534...` | 22 | +0.83c | 65% | 0.13 | 13 | 43 | NOISE (busy, not sharp) |
| `0x88c4919de7...` | 12 | +0.48c | 50% | 0.62 | 12 | 24 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 14 | +0.40c | 50% | 0.61 | 25 | 98 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 27 | -0.18c | 50% | 0.58 | 35 | 104 | NOISE (busy, not sharp) |
| `0x35bbbad241...` | 12 | -0.25c | 25% | 0.98 | 10 | 37 | NOISE (busy, not sharp) |
| `0x6765c1c000...` | 18 | -0.31c | 57% | 0.39 | 6 | 31 | NOISE (busy, not sharp) |
| `0xcfee7c48b3...` | 12 | -0.32c | 29% | 0.93 | 6 | 19 | NOISE (busy, not sharp) |
| `0x6d9fc316c3...` | 13 | -0.81c | 33% | 0.93 | 9 | 50 | NOISE (busy, not sharp) |
| `0xe234959595...` | 15 | -1.56c | 33% | 0.93 | 12 | 46 | FADE (bets the wrong way) |
| `0xb10047d6a2...` | 21 | -4.28c | 42% | 0.82 | 19 | 58 | FADE (bets the wrong way) |

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
