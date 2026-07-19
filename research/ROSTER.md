# Wallet roster

_Auto-generated 2026-07-19T14:26:20Z. 935 flagged wallets, 7 with enough graded trades to judge, 0 that beat a coin flip._

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
| `0x74471a007d...` | 18 | +2.19c | 59% | 0.31 | 13 | 19 | PROMISING (edge, luck not ruled out) |
| `0x0f47682c24...` | 12 | +1.43c | 58% | 0.39 | 10 | 13 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 15 | +1.25c | 40% | 0.85 | 13 | 16 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x74471a007d...` | 18 | +2.19c | 59% | 0.31 | 13 | 19 | PROMISING (edge, luck not ruled out) |
| `0x0f47682c24...` | 12 | +1.43c | 58% | 0.39 | 10 | 13 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 15 | +1.25c | 40% | 0.85 | 13 | 16 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 17 | +0.36c | 41% | 0.83 | 9 | 21 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 21 | -0.11c | 50% | 0.59 | 12 | 26 | NOISE (busy, not sharp) |
| `0x6916cc00aa...` | 17 | -1.81c | 43% | 0.79 | 15 | 22 | FADE (bets the wrong way) |
| `0x7f9e2d1df7...` | 13 | -2.70c | 45% | 0.73 | 9 | 14 | FADE (bets the wrong way) |

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
