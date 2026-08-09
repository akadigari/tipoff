# Wallet roster

_Auto-generated 2026-08-09T08:55:59Z. 1244 flagged wallets, 16 with enough graded trades to judge, 2 that beat a coin flip._

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
| `0xeb6f0a13ea...` | 13 | +5.19c | 100% | 0.00 | 6 | 31 | WATCH (beats luck) |
| `0xbaa2bcb543...` | 17 | +4.22c | 80% | 0.02 | 15 | 25 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x162f6fff88...` | 18 | +4.90c | 62% | 0.23 | 13 | 22 | PROMISING (edge, luck not ruled out) |
| `0xeb490d0534...` | 14 | +2.62c | 69% | 0.13 | 12 | 17 | PROMISING (edge, luck not ruled out) |
| `0xc7e53ac4a7...` | 12 | +2.30c | 50% | 0.61 | 9 | 14 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 21 | +1.74c | 55% | 0.41 | 19 | 56 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xeb6f0a13ea...` | 13 | +5.19c | 100% | 0.00 | 6 | 31 | WATCH (beats luck) |
| `0x162f6fff88...` | 18 | +4.90c | 62% | 0.23 | 13 | 22 | PROMISING (edge, luck not ruled out) |
| `0xbaa2bcb543...` | 17 | +4.22c | 80% | 0.02 | 15 | 25 | WATCH (beats luck) |
| `0xeb490d0534...` | 14 | +2.62c | 69% | 0.13 | 12 | 17 | PROMISING (edge, luck not ruled out) |
| `0xc7e53ac4a7...` | 12 | +2.30c | 50% | 0.61 | 9 | 14 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 21 | +1.74c | 55% | 0.41 | 19 | 56 | PROMISING (edge, luck not ruled out) |
| `0x60a92c8620...` | 13 | +0.90c | 69% | 0.13 | 10 | 43 | NOISE (busy, not sharp) |
| `0x3eae57986b...` | 14 | +0.79c | 67% | 0.19 | 17 | 35 | NOISE (busy, not sharp) |
| `0xf705fa0452...` | 18 | +0.27c | 53% | 0.50 | 20 | 55 | NOISE (busy, not sharp) |
| `0x6d9fc316c3...` | 15 | +0.17c | 54% | 0.50 | 17 | 33 | NOISE (busy, not sharp) |
| `0xe234959595...` | 22 | +0.16c | 55% | 0.41 | 20 | 30 | NOISE (busy, not sharp) |
| `0x0c0e270cf8...` | 13 | -0.12c | 73% | 0.11 | 8 | 25 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 38 | -0.30c | 51% | 0.50 | 21 | 76 | NOISE (busy, not sharp) |
| `0x06dc51826b...` | 27 | -0.84c | 65% | 0.08 | 44 | 91 | NOISE (busy, not sharp) |
| `0xbd0477e08d...` | 17 | -1.08c | 59% | 0.31 | 10 | 27 | FADE (bets the wrong way) |
| `0x511f9c7714...` | 18 | -2.22c | 60% | 0.30 | 21 | 70 | FADE (bets the wrong way) |

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
