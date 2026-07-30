# Wallet roster

_Auto-generated 2026-07-30T17:43:28Z. 1264 flagged wallets, 17 with enough graded trades to judge, 1 that beat a coin flip._

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
| `0xeb6f0a13ea...` | 14 | +5.29c | 100% | 0.00 | 5 | 25 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x74471a007d...` | 17 | +4.85c | 65% | 0.17 | 13 | 32 | PROMISING (edge, luck not ruled out) |
| `0xe234959595...` | 13 | +1.72c | 54% | 0.50 | 13 | 17 | PROMISING (edge, luck not ruled out) |
| `0x7bc14171cc...` | 14 | +1.32c | 57% | 0.39 | 14 | 18 | PROMISING (edge, luck not ruled out) |
| `0x60a92c8620...` | 19 | +1.00c | 56% | 0.41 | 13 | 33 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xeb6f0a13ea...` | 14 | +5.29c | 100% | 0.00 | 5 | 25 | WATCH (beats luck) |
| `0x74471a007d...` | 17 | +4.85c | 65% | 0.17 | 13 | 32 | PROMISING (edge, luck not ruled out) |
| `0xe234959595...` | 13 | +1.72c | 54% | 0.50 | 13 | 17 | PROMISING (edge, luck not ruled out) |
| `0x7bc14171cc...` | 14 | +1.32c | 57% | 0.39 | 14 | 18 | PROMISING (edge, luck not ruled out) |
| `0x60a92c8620...` | 19 | +1.00c | 56% | 0.41 | 13 | 33 | PROMISING (edge, luck not ruled out) |
| `0xdbd028b4af...` | 12 | +0.87c | 64% | 0.27 | 12 | 14 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 20 | +0.48c | 63% | 0.18 | 16 | 38 | NOISE (busy, not sharp) |
| `0xd218e47477...` | 13 | +0.11c | 50% | 0.62 | 15 | 20 | NOISE (busy, not sharp) |
| `0x8c66e28fbe...` | 15 | +0.07c | 47% | 0.70 | 10 | 18 | NOISE (busy, not sharp) |
| `0x21e25662e5...` | 27 | +0.02c | 56% | 0.41 | 11 | 39 | NOISE (busy, not sharp) |
| `0x1465b79bff...` | 17 | -0.04c | 50% | 0.61 | 6 | 37 | NOISE (busy, not sharp) |
| `0xf705fa0452...` | 16 | -0.73c | 60% | 0.30 | 13 | 37 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 37 | -1.21c | 51% | 0.50 | 14 | 48 | FADE (bets the wrong way) |
| `0x6d9fc316c3...` | 13 | -1.81c | 69% | 0.13 | 15 | 20 | FADE (bets the wrong way) |
| `0x511f9c7714...` | 23 | -2.32c | 52% | 0.50 | 23 | 52 | FADE (bets the wrong way) |
| `0x6916cc00aa...` | 13 | -2.75c | 55% | 0.50 | 11 | 33 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 22 | -6.11c | 50% | 0.58 | 34 | 60 | FADE (bets the wrong way) |

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
