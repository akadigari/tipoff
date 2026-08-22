# Wallet roster

_Auto-generated 2026-08-22T06:54:49Z. 1159 flagged wallets, 10 with enough graded trades to judge, 3 that beat a coin flip._

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
| `0xcc500cbcc8...` | 14 | +12.53c | 100% | 0.00 | 16 | 58 | WATCH (beats luck) |
| `0x1465b79bff...` | 20 | +3.09c | 83% | 0.00 | 12 | 67 | WATCH (beats luck) |
| `0x879247bf75...` | 12 | +2.50c | 92% | 0.00 | 7 | 21 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xf705fa0452...` | 23 | +7.18c | 68% | 0.07 | 48 | 143 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xcc500cbcc8...` | 14 | +12.53c | 100% | 0.00 | 16 | 58 | WATCH (beats luck) |
| `0xf705fa0452...` | 23 | +7.18c | 68% | 0.07 | 48 | 143 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 20 | +3.09c | 83% | 0.00 | 12 | 67 | WATCH (beats luck) |
| `0x879247bf75...` | 12 | +2.50c | 92% | 0.00 | 7 | 21 | WATCH (beats luck) |
| `0x511f9c7714...` | 16 | +0.52c | 50% | 0.61 | 20 | 104 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 29 | +0.47c | 54% | 0.43 | 31 | 118 | NOISE (busy, not sharp) |
| `0xcfee7c48b3...` | 14 | -0.46c | 36% | 0.89 | 5 | 19 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 14 | -2.40c | 50% | 0.61 | 6 | 116 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 28 | -5.59c | 57% | 0.29 | 51 | 193 | FADE (bets the wrong way) |
| `0x6765c1c000...` | 15 | -13.04c | 8% | 1.00 | 5 | 36 | FADE (bets the wrong way) |

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
