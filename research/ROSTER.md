# Wallet roster

_Auto-generated 2026-07-22T23:12:52Z. 1186 flagged wallets, 14 with enough graded trades to judge, 1 that beat a coin flip._

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
| `0xeb6f0a13ea...` | 15 | +2.66c | 79% | 0.03 | 8 | 17 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x0f47682c24...` | 16 | +2.12c | 62% | 0.23 | 14 | 17 | PROMISING (edge, luck not ruled out) |
| `0x74471a007d...` | 23 | +1.85c | 55% | 0.42 | 18 | 30 | PROMISING (edge, luck not ruled out) |
| `0x60a92c8620...` | 15 | +1.59c | 67% | 0.19 | 15 | 23 | PROMISING (edge, luck not ruled out) |
| `0xdbd028b4af...` | 13 | +1.15c | 67% | 0.19 | 13 | 14 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xeb6f0a13ea...` | 15 | +2.66c | 79% | 0.03 | 8 | 17 | WATCH (beats luck) |
| `0x0f47682c24...` | 16 | +2.12c | 62% | 0.23 | 14 | 17 | PROMISING (edge, luck not ruled out) |
| `0x74471a007d...` | 23 | +1.85c | 55% | 0.42 | 18 | 30 | PROMISING (edge, luck not ruled out) |
| `0x60a92c8620...` | 15 | +1.59c | 67% | 0.19 | 15 | 23 | PROMISING (edge, luck not ruled out) |
| `0xdbd028b4af...` | 13 | +1.15c | 67% | 0.19 | 13 | 14 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 29 | +0.58c | 50% | 0.58 | 9 | 35 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 20 | +0.54c | 45% | 0.75 | 17 | 22 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 15 | +0.15c | 53% | 0.50 | 8 | 21 | NOISE (busy, not sharp) |
| `0x7449904c4f...` | 12 | +0.03c | 67% | 0.50 | 12 | 14 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 28 | -0.22c | 48% | 0.66 | 20 | 42 | NOISE (busy, not sharp) |
| `0x6916cc00aa...` | 25 | -1.32c | 50% | 0.59 | 17 | 29 | FADE (bets the wrong way) |
| `0xb10047d6a2...` | 13 | -1.89c | 36% | 0.89 | 12 | 15 | FADE (bets the wrong way) |
| `0x7f9e2d1df7...` | 14 | -2.51c | 45% | 0.73 | 11 | 16 | FADE (bets the wrong way) |
| `0xfc2f4f50ce...` | 13 | -3.51c | 46% | 0.71 | 12 | 14 | FADE (bets the wrong way) |

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
