# Wallet roster

_Auto-generated 2026-08-24T07:14:43Z. 1196 flagged wallets, 18 with enough graded trades to judge, 0 that beat a coin flip._

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

_None yet._

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xcc500cbcc8...` | 20 | +4.87c | 63% | 0.18 | 19 | 65 | PROMISING (edge, luck not ruled out) |
| `0xf705fa0452...` | 55 | +4.17c | 61% | 0.07 | 52 | 167 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 21 | +2.68c | 68% | 0.08 | 16 | 87 | PROMISING (edge, luck not ruled out) |
| `0x401ee31e9e...` | 12 | +1.29c | 70% | 0.17 | 8 | 19 | PROMISING (edge, luck not ruled out) |
| `0x6d9fc316c3...` | 17 | +1.16c | 64% | 0.27 | 16 | 64 | PROMISING (edge, luck not ruled out) |
| `0xdf17f4a8dd...` | 12 | +1.13c | 44% | 0.75 | 14 | 48 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xcc500cbcc8...` | 20 | +4.87c | 63% | 0.18 | 19 | 65 | PROMISING (edge, luck not ruled out) |
| `0xf705fa0452...` | 55 | +4.17c | 61% | 0.07 | 52 | 167 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 21 | +2.68c | 68% | 0.08 | 16 | 87 | PROMISING (edge, luck not ruled out) |
| `0x401ee31e9e...` | 12 | +1.29c | 70% | 0.17 | 8 | 19 | PROMISING (edge, luck not ruled out) |
| `0x6d9fc316c3...` | 17 | +1.16c | 64% | 0.27 | 16 | 64 | PROMISING (edge, luck not ruled out) |
| `0xdf17f4a8dd...` | 12 | +1.13c | 44% | 0.75 | 14 | 48 | PROMISING (edge, luck not ruled out) |
| `0x56e777a0ac...` | 12 | +0.84c | 67% | 0.19 | 6 | 28 | NOISE (busy, not sharp) |
| `0xcdf82242c9...` | 13 | +0.59c | 89% | 0.02 | 15 | 33 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 28 | +0.51c | 56% | 0.35 | 29 | 125 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 18 | +0.48c | 53% | 0.50 | 20 | 105 | NOISE (busy, not sharp) |
| `0xc2de93c744...` | 12 | +0.08c | 67% | 0.19 | 3 | 25 | NOISE (busy, not sharp) |
| `0xcfee7c48b3...` | 12 | -0.52c | 33% | 0.91 | 4 | 19 | NOISE (busy, not sharp) |
| `0x252d7bae5e...` | 14 | -0.69c | 46% | 0.71 | 22 | 40 | NOISE (busy, not sharp) |
| `0xb10047d6a2...` | 12 | -1.33c | 50% | 0.61 | 11 | 66 | FADE (bets the wrong way) |
| `0xe734e7bf7c...` | 19 | -2.35c | 50% | 0.59 | 8 | 123 | FADE (bets the wrong way) |
| `0x56ad6bd059...` | 12 | -7.07c | 45% | 0.73 | 12 | 31 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 39 | -7.24c | 59% | 0.17 | 58 | 211 | FADE (bets the wrong way) |
| `0x6765c1c000...` | 16 | -13.48c | 8% | 1.00 | 5 | 36 | FADE (bets the wrong way) |

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
