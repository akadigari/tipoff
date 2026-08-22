# Wallet roster

_Auto-generated 2026-08-22T21:30:37Z. 1196 flagged wallets, 11 with enough graded trades to judge, 3 that beat a coin flip._

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
| `0xcc500cbcc8...` | 15 | +12.13c | 100% | 0.00 | 16 | 58 | WATCH (beats luck) |
| `0x1465b79bff...` | 21 | +3.14c | 79% | 0.01 | 10 | 67 | WATCH (beats luck) |
| `0x879247bf75...` | 12 | +2.50c | 92% | 0.00 | 8 | 22 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xf705fa0452...` | 29 | +5.18c | 61% | 0.17 | 48 | 149 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xcc500cbcc8...` | 15 | +12.13c | 100% | 0.00 | 16 | 58 | WATCH (beats luck) |
| `0xf705fa0452...` | 29 | +5.18c | 61% | 0.17 | 48 | 149 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 21 | +3.14c | 79% | 0.01 | 10 | 67 | WATCH (beats luck) |
| `0x879247bf75...` | 12 | +2.50c | 92% | 0.00 | 8 | 22 | WATCH (beats luck) |
| `0x122cb94c43...` | 28 | +0.79c | 59% | 0.22 | 31 | 121 | NOISE (busy, not sharp) |
| `0x6d9fc316c3...` | 13 | +0.56c | 56% | 0.50 | 12 | 59 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 16 | +0.52c | 50% | 0.61 | 20 | 104 | NOISE (busy, not sharp) |
| `0xcfee7c48b3...` | 13 | -0.46c | 40% | 0.83 | 4 | 19 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 18 | -2.20c | 47% | 0.69 | 6 | 117 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 29 | -5.35c | 62% | 0.13 | 54 | 197 | FADE (bets the wrong way) |
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
