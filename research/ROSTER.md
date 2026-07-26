# Wallet roster

_Auto-generated 2026-07-26T20:15:42Z. 1228 flagged wallets, 16 with enough graded trades to judge, 2 that beat a coin flip._

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
| `0xcc500cbcc8...` | 13 | +3.61c | 92% | 0.00 | 11 | 22 | WATCH (beats luck) |
| `0xeb6f0a13ea...` | 12 | +3.40c | 91% | 0.01 | 5 | 18 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x74471a007d...` | 20 | +3.75c | 60% | 0.25 | 14 | 32 | PROMISING (edge, luck not ruled out) |
| `0x60a92c8620...` | 17 | +1.61c | 67% | 0.15 | 13 | 29 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 21 | +1.19c | 62% | 0.19 | 18 | 34 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x74471a007d...` | 20 | +3.75c | 60% | 0.25 | 14 | 32 | PROMISING (edge, luck not ruled out) |
| `0xcc500cbcc8...` | 13 | +3.61c | 92% | 0.00 | 11 | 22 | WATCH (beats luck) |
| `0xeb6f0a13ea...` | 12 | +3.40c | 91% | 0.01 | 5 | 18 | WATCH (beats luck) |
| `0x60a92c8620...` | 17 | +1.61c | 67% | 0.15 | 13 | 29 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 21 | +1.19c | 62% | 0.19 | 18 | 34 | PROMISING (edge, luck not ruled out) |
| `0xdbd028b4af...` | 12 | +0.87c | 64% | 0.27 | 12 | 14 | NOISE (busy, not sharp) |
| `0xf705fa0452...` | 12 | +0.23c | 67% | 0.19 | 14 | 26 | NOISE (busy, not sharp) |
| `0x1465b79bff...` | 31 | +0.10c | 46% | 0.72 | 9 | 37 | NOISE (busy, not sharp) |
| `0xd218e47477...` | 12 | +0.04c | 50% | 0.62 | 10 | 13 | NOISE (busy, not sharp) |
| `0x7449904c4f...` | 13 | +0.02c | 67% | 0.50 | 13 | 16 | NOISE (busy, not sharp) |
| `0x21e25662e5...` | 27 | +0.02c | 56% | 0.41 | 10 | 35 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 37 | -0.36c | 50% | 0.57 | 25 | 48 | NOISE (busy, not sharp) |
| `0x8b4bca1d79...` | 12 | -1.51c | 50% | 0.62 | 12 | 15 | FADE (bets the wrong way) |
| `0x6916cc00aa...` | 18 | -2.12c | 53% | 0.50 | 15 | 33 | FADE (bets the wrong way) |
| `0xe734e7bf7c...` | 28 | -3.51c | 43% | 0.83 | 13 | 38 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 19 | -6.50c | 42% | 0.82 | 28 | 36 | FADE (bets the wrong way) |

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
