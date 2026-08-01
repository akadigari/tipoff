# Wallet roster

_Auto-generated 2026-08-01T03:43:53Z. 1276 flagged wallets, 18 with enough graded trades to judge, 1 that beat a coin flip._

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
| `0xeb6f0a13ea...` | 15 | +5.74c | 100% | 0.00 | 5 | 25 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x74471a007d...` | 13 | +3.38c | 62% | 0.29 | 12 | 33 | PROMISING (edge, luck not ruled out) |
| `0xe234959595...` | 15 | +1.49c | 54% | 0.50 | 13 | 17 | PROMISING (edge, luck not ruled out) |
| `0x7bc14171cc...` | 15 | +1.09c | 53% | 0.50 | 13 | 18 | PROMISING (edge, luck not ruled out) |
| `0x60a92c8620...` | 22 | +1.01c | 62% | 0.19 | 14 | 37 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xeb6f0a13ea...` | 15 | +5.74c | 100% | 0.00 | 5 | 25 | WATCH (beats luck) |
| `0x74471a007d...` | 13 | +3.38c | 62% | 0.29 | 12 | 33 | PROMISING (edge, luck not ruled out) |
| `0xe234959595...` | 15 | +1.49c | 54% | 0.50 | 13 | 17 | PROMISING (edge, luck not ruled out) |
| `0x7bc14171cc...` | 15 | +1.09c | 53% | 0.50 | 13 | 18 | PROMISING (edge, luck not ruled out) |
| `0x60a92c8620...` | 22 | +1.01c | 62% | 0.19 | 14 | 37 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 19 | +0.53c | 67% | 0.12 | 18 | 40 | NOISE (busy, not sharp) |
| `0x8c66e28fbe...` | 14 | +0.31c | 54% | 0.50 | 9 | 18 | NOISE (busy, not sharp) |
| `0xd218e47477...` | 16 | +0.14c | 50% | 0.61 | 15 | 20 | NOISE (busy, not sharp) |
| `0x21e25662e5...` | 27 | +0.02c | 56% | 0.41 | 11 | 39 | NOISE (busy, not sharp) |
| `0x1465b79bff...` | 17 | -0.04c | 50% | 0.61 | 6 | 37 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 35 | -0.85c | 51% | 0.50 | 14 | 49 | NOISE (busy, not sharp) |
| `0xf705fa0452...` | 17 | -0.89c | 56% | 0.40 | 14 | 42 | NOISE (busy, not sharp) |
| `0x6d9fc316c3...` | 12 | -1.71c | 67% | 0.19 | 16 | 24 | FADE (bets the wrong way) |
| `0x6916cc00aa...` | 13 | -2.75c | 55% | 0.50 | 9 | 33 | FADE (bets the wrong way) |
| `0x511f9c7714...` | 19 | -2.98c | 47% | 0.68 | 22 | 53 | FADE (bets the wrong way) |
| `0xa8c63f775d...` | 12 | -4.38c | 60% | 0.38 | 13 | 15 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 28 | -4.64c | 50% | 0.57 | 38 | 65 | FADE (bets the wrong way) |
| `0xfc2f4f50ce...` | 12 | -9.75c | 25% | 0.98 | 12 | 24 | FADE (bets the wrong way) |

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
