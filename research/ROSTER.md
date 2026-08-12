# Wallet roster

_Auto-generated 2026-08-12T06:22:44Z. 1244 flagged wallets, 17 with enough graded trades to judge, 3 that beat a coin flip._

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
| `0xfc2f4f50ce...` | 14 | +10.01c | 92% | 0.00 | 13 | 38 | WATCH (beats luck) |
| `0x23d81ba937...` | 18 | +6.61c | 76% | 0.03 | 12 | 27 | WATCH (beats luck) |
| `0xbaa2bcb543...` | 14 | +4.56c | 77% | 0.05 | 13 | 27 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x162f6fff88...` | 14 | +5.03c | 54% | 0.50 | 12 | 23 | PROMISING (edge, luck not ruled out) |
| `0xbd0477e08d...` | 15 | +3.44c | 73% | 0.06 | 11 | 31 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 21 | +2.22c | 55% | 0.41 | 19 | 65 | PROMISING (edge, luck not ruled out) |
| `0xe234959595...` | 15 | +1.60c | 64% | 0.21 | 17 | 38 | PROMISING (edge, luck not ruled out) |
| `0xeb490d0534...` | 16 | +1.47c | 67% | 0.15 | 11 | 26 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xfc2f4f50ce...` | 14 | +10.01c | 92% | 0.00 | 13 | 38 | WATCH (beats luck) |
| `0x23d81ba937...` | 18 | +6.61c | 76% | 0.03 | 12 | 27 | WATCH (beats luck) |
| `0x162f6fff88...` | 14 | +5.03c | 54% | 0.50 | 12 | 23 | PROMISING (edge, luck not ruled out) |
| `0xbaa2bcb543...` | 14 | +4.56c | 77% | 0.05 | 13 | 27 | WATCH (beats luck) |
| `0xbd0477e08d...` | 15 | +3.44c | 73% | 0.06 | 11 | 31 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 21 | +2.22c | 55% | 0.41 | 19 | 65 | PROMISING (edge, luck not ruled out) |
| `0xe234959595...` | 15 | +1.60c | 64% | 0.21 | 17 | 38 | PROMISING (edge, luck not ruled out) |
| `0xeb490d0534...` | 16 | +1.47c | 67% | 0.15 | 11 | 26 | PROMISING (edge, luck not ruled out) |
| `0x06dc51826b...` | 24 | +0.80c | 73% | 0.03 | 41 | 107 | NOISE (busy, not sharp) |
| `0x3eae57986b...` | 17 | +0.69c | 64% | 0.21 | 18 | 36 | NOISE (busy, not sharp) |
| `0x000d257d2d...` | 15 | +0.65c | 50% | 0.61 | 15 | 23 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 16 | +0.15c | 62% | 0.29 | 20 | 74 | NOISE (busy, not sharp) |
| `0xb10047d6a2...` | 13 | -0.08c | 54% | 0.50 | 18 | 42 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 32 | -0.13c | 58% | 0.24 | 14 | 90 | NOISE (busy, not sharp) |
| `0x74471a007d...` | 15 | -0.98c | 53% | 0.50 | 14 | 50 | NOISE (busy, not sharp) |
| `0x6d9fc316c3...` | 12 | -2.95c | 40% | 0.83 | 12 | 40 | FADE (bets the wrong way) |
| `0xdf17f4a8dd...` | 14 | -4.60c | 62% | 0.29 | 14 | 26 | FADE (bets the wrong way) |

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
