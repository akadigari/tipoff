# Wallet roster

_Auto-generated 2026-08-09T16:48:23Z. 1249 flagged wallets, 17 with enough graded trades to judge, 3 that beat a coin flip._

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
| `0x23d81ba937...` | 13 | +5.65c | 92% | 0.00 | 13 | 20 | WATCH (beats luck) |
| `0xeb6f0a13ea...` | 12 | +5.13c | 100% | 0.00 | 6 | 31 | WATCH (beats luck) |
| `0xbaa2bcb543...` | 15 | +4.22c | 77% | 0.05 | 14 | 26 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x162f6fff88...` | 15 | +4.84c | 57% | 0.39 | 12 | 22 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 22 | +2.66c | 62% | 0.19 | 19 | 58 | PROMISING (edge, luck not ruled out) |
| `0xc7e53ac4a7...` | 12 | +2.30c | 50% | 0.61 | 9 | 14 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x23d81ba937...` | 13 | +5.65c | 92% | 0.00 | 13 | 20 | WATCH (beats luck) |
| `0xeb6f0a13ea...` | 12 | +5.13c | 100% | 0.00 | 6 | 31 | WATCH (beats luck) |
| `0x162f6fff88...` | 15 | +4.84c | 57% | 0.39 | 12 | 22 | PROMISING (edge, luck not ruled out) |
| `0xbaa2bcb543...` | 15 | +4.22c | 77% | 0.05 | 14 | 26 | WATCH (beats luck) |
| `0x122cb94c43...` | 22 | +2.66c | 62% | 0.19 | 19 | 58 | PROMISING (edge, luck not ruled out) |
| `0xc7e53ac4a7...` | 12 | +2.30c | 50% | 0.61 | 9 | 14 | PROMISING (edge, luck not ruled out) |
| `0x60a92c8620...` | 13 | +0.90c | 69% | 0.13 | 10 | 43 | NOISE (busy, not sharp) |
| `0x3eae57986b...` | 14 | +0.79c | 67% | 0.19 | 17 | 35 | NOISE (busy, not sharp) |
| `0xe234959595...` | 20 | +0.55c | 56% | 0.41 | 18 | 30 | NOISE (busy, not sharp) |
| `0xf705fa0452...` | 18 | +0.27c | 53% | 0.50 | 20 | 55 | NOISE (busy, not sharp) |
| `0x6d9fc316c3...` | 12 | -0.03c | 60% | 0.38 | 15 | 33 | NOISE (busy, not sharp) |
| `0x0c0e270cf8...` | 13 | -0.12c | 73% | 0.11 | 8 | 25 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 37 | -0.31c | 50% | 0.57 | 21 | 77 | NOISE (busy, not sharp) |
| `0x06dc51826b...` | 28 | -0.51c | 67% | 0.06 | 44 | 91 | NOISE (busy, not sharp) |
| `0xbd0477e08d...` | 16 | -0.65c | 62% | 0.23 | 10 | 27 | NOISE (busy, not sharp) |
| `0x0f7f9903f4...` | 14 | -2.23c | 43% | 0.79 | 12 | 16 | FADE (bets the wrong way) |
| `0x511f9c7714...` | 17 | -2.24c | 64% | 0.21 | 21 | 70 | FADE (bets the wrong way) |

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
