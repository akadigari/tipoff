# Wallet roster

_Auto-generated 2026-08-23T04:47:43Z. 1196 flagged wallets, 12 with enough graded trades to judge, 3 that beat a coin flip._

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
| `0xcc500cbcc8...` | 15 | +11.53c | 86% | 0.01 | 17 | 59 | WATCH (beats luck) |
| `0x1465b79bff...` | 23 | +2.57c | 71% | 0.04 | 10 | 67 | WATCH (beats luck) |
| `0x879247bf75...` | 12 | +2.50c | 92% | 0.00 | 8 | 22 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xf705fa0452...` | 39 | +5.05c | 61% | 0.13 | 49 | 154 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xcc500cbcc8...` | 15 | +11.53c | 86% | 0.01 | 17 | 59 | WATCH (beats luck) |
| `0xf705fa0452...` | 39 | +5.05c | 61% | 0.13 | 49 | 154 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 23 | +2.57c | 71% | 0.04 | 10 | 67 | WATCH (beats luck) |
| `0x879247bf75...` | 12 | +2.50c | 92% | 0.00 | 8 | 22 | WATCH (beats luck) |
| `0x122cb94c43...` | 29 | +0.82c | 61% | 0.17 | 30 | 122 | NOISE (busy, not sharp) |
| `0x6d9fc316c3...` | 14 | +0.59c | 60% | 0.38 | 13 | 61 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 18 | +0.48c | 53% | 0.50 | 20 | 104 | NOISE (busy, not sharp) |
| `0xcfee7c48b3...` | 13 | -0.46c | 40% | 0.83 | 4 | 19 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 16 | -3.07c | 40% | 0.85 | 6 | 118 | FADE (bets the wrong way) |
| `0x56ad6bd059...` | 13 | -6.45c | 50% | 0.61 | 13 | 31 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 34 | -8.00c | 56% | 0.30 | 58 | 201 | FADE (bets the wrong way) |
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
