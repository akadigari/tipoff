# Wallet roster

_Auto-generated 2026-08-24T18:53:34Z. 1208 flagged wallets, 17 with enough graded trades to judge, 1 that beat a coin flip._

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
| `0xf705fa0452...` | 58 | +4.00c | 62% | 0.04 | 54 | 172 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xcc500cbcc8...` | 23 | +4.34c | 64% | 0.14 | 22 | 71 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 31 | +1.84c | 61% | 0.17 | 17 | 93 | PROMISING (edge, luck not ruled out) |
| `0x401ee31e9e...` | 12 | +1.29c | 70% | 0.17 | 8 | 20 | PROMISING (edge, luck not ruled out) |
| `0x6d9fc316c3...` | 17 | +1.16c | 64% | 0.27 | 16 | 65 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xcc500cbcc8...` | 23 | +4.34c | 64% | 0.14 | 22 | 71 | PROMISING (edge, luck not ruled out) |
| `0xf705fa0452...` | 58 | +4.00c | 62% | 0.04 | 54 | 172 | WATCH (beats luck) |
| `0x1465b79bff...` | 31 | +1.84c | 61% | 0.17 | 17 | 93 | PROMISING (edge, luck not ruled out) |
| `0x401ee31e9e...` | 12 | +1.29c | 70% | 0.17 | 8 | 20 | PROMISING (edge, luck not ruled out) |
| `0x6d9fc316c3...` | 17 | +1.16c | 64% | 0.27 | 16 | 65 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 28 | +0.80c | 59% | 0.22 | 26 | 127 | NOISE (busy, not sharp) |
| `0xcdf82242c9...` | 13 | +0.59c | 89% | 0.02 | 15 | 33 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 17 | +0.42c | 50% | 0.61 | 17 | 107 | NOISE (busy, not sharp) |
| `0x6e2c3937e6...` | 12 | +0.19c | 80% | 0.06 | 10 | 33 | NOISE (busy, not sharp) |
| `0xc2de93c744...` | 12 | +0.08c | 67% | 0.19 | 3 | 25 | NOISE (busy, not sharp) |
| `0xcfee7c48b3...` | 12 | -0.52c | 33% | 0.91 | 4 | 19 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 21 | -1.19c | 50% | 0.59 | 8 | 124 | FADE (bets the wrong way) |
| `0x252d7bae5e...` | 17 | -1.63c | 38% | 0.89 | 22 | 41 | FADE (bets the wrong way) |
| `0x56e777a0ac...` | 15 | -3.40c | 53% | 0.50 | 6 | 28 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 41 | -6.62c | 61% | 0.11 | 60 | 214 | FADE (bets the wrong way) |
| `0x56ad6bd059...` | 12 | -7.07c | 45% | 0.73 | 12 | 31 | FADE (bets the wrong way) |
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
