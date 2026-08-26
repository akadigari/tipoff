# Wallet roster

_Auto-generated 2026-08-26T19:14:52Z. 1176 flagged wallets, 19 with enough graded trades to judge, 1 that beat a coin flip._

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
| `0xf705fa0452...` | 68 | +3.70c | 62% | 0.03 | 59 | 185 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x6db983ff1c...` | 13 | +4.15c | 60% | 0.38 | 12 | 27 | PROMISING (edge, luck not ruled out) |
| `0xcc500cbcc8...` | 37 | +3.02c | 63% | 0.09 | 23 | 87 | PROMISING (edge, luck not ruled out) |
| `0x401ee31e9e...` | 18 | +1.03c | 60% | 0.30 | 8 | 22 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x6db983ff1c...` | 13 | +4.15c | 60% | 0.38 | 12 | 27 | PROMISING (edge, luck not ruled out) |
| `0xf705fa0452...` | 68 | +3.70c | 62% | 0.03 | 59 | 185 | WATCH (beats luck) |
| `0xcc500cbcc8...` | 37 | +3.02c | 63% | 0.09 | 23 | 87 | PROMISING (edge, luck not ruled out) |
| `0x401ee31e9e...` | 18 | +1.03c | 60% | 0.30 | 8 | 22 | PROMISING (edge, luck not ruled out) |
| `0xa19cbababc...` | 14 | +0.83c | 58% | 0.39 | 9 | 20 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 23 | +0.79c | 59% | 0.26 | 26 | 134 | NOISE (busy, not sharp) |
| `0x252d7bae5e...` | 15 | +0.64c | 57% | 0.39 | 21 | 42 | NOISE (busy, not sharp) |
| `0x1465b79bff...` | 45 | +0.56c | 59% | 0.17 | 18 | 101 | NOISE (busy, not sharp) |
| `0x3a8aa345d5...` | 14 | +0.43c | 62% | 0.29 | 4 | 31 | NOISE (busy, not sharp) |
| `0x000d257d2d...` | 13 | +0.21c | 64% | 0.27 | 12 | 40 | NOISE (busy, not sharp) |
| `0x6d9fc316c3...` | 16 | +0.21c | 45% | 0.73 | 14 | 67 | NOISE (busy, not sharp) |
| `0xc2de93c744...` | 12 | +0.08c | 67% | 0.19 | 3 | 26 | NOISE (busy, not sharp) |
| `0x35bbbad241...` | 23 | -0.20c | 50% | 0.58 | 12 | 68 | NOISE (busy, not sharp) |
| `0x6e2c3937e6...` | 16 | -0.21c | 67% | 0.15 | 11 | 38 | NOISE (busy, not sharp) |
| `0x03805a13a0...` | 14 | -0.60c | 46% | 0.71 | 11 | 20 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 26 | -0.75c | 43% | 0.80 | 11 | 133 | NOISE (busy, not sharp) |
| `0x56e777a0ac...` | 16 | -2.83c | 56% | 0.40 | 6 | 32 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 51 | -5.30c | 62% | 0.06 | 69 | 234 | FADE (bets the wrong way) |
| `0x56ad6bd059...` | 12 | -7.21c | 30% | 0.94 | 11 | 34 | FADE (bets the wrong way) |

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
