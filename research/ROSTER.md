# Wallet roster

_Auto-generated 2026-08-19T22:35:29Z. 1147 flagged wallets, 13 with enough graded trades to judge, 2 that beat a coin flip._

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
| `0x06dc51826b...` | 29 | +1.59c | 72% | 0.01 | 35 | 156 | WATCH (beats luck) |
| `0xe734e7bf7c...` | 19 | +1.47c | 74% | 0.03 | 6 | 105 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xfc2f4f50ce...` | 13 | +1.12c | 64% | 0.27 | 8 | 49 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x06dc51826b...` | 29 | +1.59c | 72% | 0.01 | 35 | 156 | WATCH (beats luck) |
| `0xe734e7bf7c...` | 19 | +1.47c | 74% | 0.03 | 6 | 105 | WATCH (beats luck) |
| `0xfc2f4f50ce...` | 13 | +1.12c | 64% | 0.27 | 8 | 49 | PROMISING (edge, luck not ruled out) |
| `0xeb490d0534...` | 18 | +0.86c | 59% | 0.31 | 10 | 43 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 14 | +0.63c | 50% | 0.61 | 25 | 98 | NOISE (busy, not sharp) |
| `0xc2de93c744...` | 12 | +0.14c | 67% | 0.19 | 3 | 17 | NOISE (busy, not sharp) |
| `0x35bbbad241...` | 12 | +0.02c | 33% | 0.93 | 12 | 39 | NOISE (busy, not sharp) |
| `0xcfee7c48b3...` | 14 | -0.36c | 33% | 0.91 | 6 | 19 | NOISE (busy, not sharp) |
| `0x6765c1c000...` | 19 | -0.37c | 53% | 0.50 | 6 | 35 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 28 | -0.48c | 50% | 0.58 | 35 | 108 | NOISE (busy, not sharp) |
| `0x6d9fc316c3...` | 16 | -0.55c | 33% | 0.94 | 9 | 50 | NOISE (busy, not sharp) |
| `0xe234959595...` | 13 | -2.03c | 27% | 0.96 | 11 | 47 | FADE (bets the wrong way) |
| `0xb10047d6a2...` | 16 | -4.17c | 50% | 0.61 | 16 | 58 | FADE (bets the wrong way) |

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
