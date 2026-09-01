# Wallet roster

_Auto-generated 2026-09-01T23:14:36Z. 1277 flagged wallets, 23 with enough graded trades to judge, 1 that beat a coin flip._

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
| `0xf705fa0452...` | 74 | +2.82c | 61% | 0.04 | 61 | 191 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x6db983ff1c...` | 15 | +3.82c | 67% | 0.19 | 12 | 28 | PROMISING (edge, luck not ruled out) |
| `0xcc500cbcc8...` | 39 | +2.84c | 62% | 0.09 | 22 | 91 | PROMISING (edge, luck not ruled out) |
| `0x58b3380f71...` | 13 | +2.30c | 60% | 0.38 | 4 | 23 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 48 | +1.18c | 59% | 0.15 | 20 | 103 | PROMISING (edge, luck not ruled out) |
| `0x401ee31e9e...` | 18 | +1.03c | 60% | 0.30 | 9 | 23 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x6db983ff1c...` | 15 | +3.82c | 67% | 0.19 | 12 | 28 | PROMISING (edge, luck not ruled out) |
| `0xcc500cbcc8...` | 39 | +2.84c | 62% | 0.09 | 22 | 91 | PROMISING (edge, luck not ruled out) |
| `0xf705fa0452...` | 74 | +2.82c | 61% | 0.04 | 61 | 191 | WATCH (beats luck) |
| `0x58b3380f71...` | 13 | +2.30c | 60% | 0.38 | 4 | 23 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 48 | +1.18c | 59% | 0.15 | 20 | 103 | PROMISING (edge, luck not ruled out) |
| `0x401ee31e9e...` | 18 | +1.03c | 60% | 0.30 | 9 | 23 | PROMISING (edge, luck not ruled out) |
| `0xa19cbababc...` | 13 | +0.89c | 58% | 0.39 | 10 | 21 | NOISE (busy, not sharp) |
| `0xeb490d0534...` | 13 | +0.67c | 62% | 0.29 | 14 | 65 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 25 | +0.60c | 61% | 0.20 | 29 | 141 | NOISE (busy, not sharp) |
| `0xe234959595...` | 13 | +0.55c | 50% | 0.62 | 11 | 63 | NOISE (busy, not sharp) |
| `0xc2de93c744...` | 14 | +0.24c | 69% | 0.13 | 3 | 30 | NOISE (busy, not sharp) |
| `0x3a8aa345d5...` | 15 | +0.00c | 57% | 0.39 | 4 | 32 | NOISE (busy, not sharp) |
| `0x35bbbad241...` | 30 | -0.07c | 52% | 0.50 | 13 | 69 | NOISE (busy, not sharp) |
| `0x6d9fc316c3...` | 17 | -0.33c | 42% | 0.81 | 15 | 71 | NOISE (busy, not sharp) |
| `0x6e2c3937e6...` | 18 | -0.33c | 65% | 0.17 | 13 | 40 | NOISE (busy, not sharp) |
| `0x03805a13a0...` | 18 | -0.46c | 47% | 0.70 | 11 | 21 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 29 | -0.92c | 42% | 0.84 | 12 | 136 | NOISE (busy, not sharp) |
| `0xb10047d6a2...` | 14 | -1.20c | 50% | 0.61 | 13 | 76 | FADE (bets the wrong way) |
| `0x252d7bae5e...` | 17 | -1.34c | 50% | 0.60 | 22 | 45 | FADE (bets the wrong way) |
| `0xbf961d0c79...` | 12 | -2.38c | 36% | 0.89 | 11 | 30 | FADE (bets the wrong way) |

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
