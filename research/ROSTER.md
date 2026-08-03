# Wallet roster

_Auto-generated 2026-08-03T15:49:53Z. 1298 flagged wallets, 19 with enough graded trades to judge, 2 that beat a coin flip._

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
| `0xeb6f0a13ea...` | 14 | +5.83c | 100% | 0.00 | 5 | 26 | WATCH (beats luck) |
| `0x122cb94c43...` | 24 | +2.37c | 70% | 0.05 | 22 | 46 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xe234959595...` | 23 | +3.39c | 62% | 0.19 | 22 | 27 | PROMISING (edge, luck not ruled out) |
| `0xcc500cbcc8...` | 12 | +3.10c | 67% | 0.19 | 10 | 29 | PROMISING (edge, luck not ruled out) |
| `0x74471a007d...` | 15 | +2.57c | 53% | 0.50 | 13 | 35 | PROMISING (edge, luck not ruled out) |
| `0x8c66e28fbe...` | 13 | +1.42c | 58% | 0.39 | 8 | 20 | PROMISING (edge, luck not ruled out) |
| `0x60a92c8620...` | 19 | +1.33c | 63% | 0.18 | 14 | 38 | PROMISING (edge, luck not ruled out) |
| `0x7bc14171cc...` | 15 | +1.09c | 53% | 0.50 | 13 | 18 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xeb6f0a13ea...` | 14 | +5.83c | 100% | 0.00 | 5 | 26 | WATCH (beats luck) |
| `0xe234959595...` | 23 | +3.39c | 62% | 0.19 | 22 | 27 | PROMISING (edge, luck not ruled out) |
| `0xcc500cbcc8...` | 12 | +3.10c | 67% | 0.19 | 10 | 29 | PROMISING (edge, luck not ruled out) |
| `0x74471a007d...` | 15 | +2.57c | 53% | 0.50 | 13 | 35 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 24 | +2.37c | 70% | 0.05 | 22 | 46 | WATCH (beats luck) |
| `0x8c66e28fbe...` | 13 | +1.42c | 58% | 0.39 | 8 | 20 | PROMISING (edge, luck not ruled out) |
| `0x60a92c8620...` | 19 | +1.33c | 63% | 0.18 | 14 | 38 | PROMISING (edge, luck not ruled out) |
| `0x7bc14171cc...` | 15 | +1.09c | 53% | 0.50 | 13 | 18 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 12 | +0.24c | 60% | 0.38 | 6 | 37 | NOISE (busy, not sharp) |
| `0xf705fa0452...` | 18 | +0.16c | 59% | 0.31 | 17 | 46 | NOISE (busy, not sharp) |
| `0xd218e47477...` | 16 | +0.14c | 50% | 0.61 | 15 | 20 | NOISE (busy, not sharp) |
| `0x21e25662e5...` | 27 | +0.02c | 56% | 0.41 | 11 | 39 | NOISE (busy, not sharp) |
| `0x0c0e270cf8...` | 13 | -0.34c | 73% | 0.11 | 9 | 24 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 37 | -0.45c | 54% | 0.37 | 22 | 58 | NOISE (busy, not sharp) |
| `0xfc2f4f50ce...` | 13 | -1.68c | 46% | 0.71 | 11 | 26 | FADE (bets the wrong way) |
| `0x6d9fc316c3...` | 19 | -1.71c | 59% | 0.31 | 17 | 27 | FADE (bets the wrong way) |
| `0xa8c63f775d...` | 14 | -2.59c | 58% | 0.39 | 14 | 16 | FADE (bets the wrong way) |
| `0x511f9c7714...` | 18 | -2.98c | 47% | 0.69 | 20 | 59 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 30 | -3.55c | 57% | 0.29 | 49 | 80 | FADE (bets the wrong way) |

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
