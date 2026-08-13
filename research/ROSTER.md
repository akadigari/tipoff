# Wallet roster

_Auto-generated 2026-08-13T14:25:19Z. 1225 flagged wallets, 18 with enough graded trades to judge, 3 that beat a coin flip._

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
| `0x23d81ba937...` | 17 | +7.76c | 81% | 0.01 | 12 | 28 | WATCH (beats luck) |
| `0xfc2f4f50ce...` | 14 | +7.29c | 92% | 0.00 | 12 | 40 | WATCH (beats luck) |
| `0xbaa2bcb543...` | 15 | +6.15c | 79% | 0.03 | 13 | 27 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x162f6fff88...` | 16 | +4.28c | 53% | 0.50 | 14 | 25 | PROMISING (edge, luck not ruled out) |
| `0xbd0477e08d...` | 15 | +3.02c | 67% | 0.15 | 11 | 33 | PROMISING (edge, luck not ruled out) |
| `0xeb490d0534...` | 17 | +1.57c | 69% | 0.11 | 13 | 34 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x23d81ba937...` | 17 | +7.76c | 81% | 0.01 | 12 | 28 | WATCH (beats luck) |
| `0xfc2f4f50ce...` | 14 | +7.29c | 92% | 0.00 | 12 | 40 | WATCH (beats luck) |
| `0xbaa2bcb543...` | 15 | +6.15c | 79% | 0.03 | 13 | 27 | WATCH (beats luck) |
| `0x162f6fff88...` | 16 | +4.28c | 53% | 0.50 | 14 | 25 | PROMISING (edge, luck not ruled out) |
| `0xbd0477e08d...` | 15 | +3.02c | 67% | 0.15 | 11 | 33 | PROMISING (edge, luck not ruled out) |
| `0xeb490d0534...` | 17 | +1.57c | 69% | 0.11 | 13 | 34 | PROMISING (edge, luck not ruled out) |
| `0x06dc51826b...` | 29 | +0.87c | 78% | 0.00 | 38 | 116 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 21 | +0.80c | 50% | 0.59 | 22 | 72 | NOISE (busy, not sharp) |
| `0x3eae57986b...` | 17 | +0.69c | 64% | 0.21 | 19 | 37 | NOISE (busy, not sharp) |
| `0x000d257d2d...` | 17 | +0.11c | 44% | 0.77 | 15 | 23 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 18 | +0.10c | 53% | 0.50 | 20 | 76 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 40 | +0.07c | 62% | 0.10 | 13 | 93 | NOISE (busy, not sharp) |
| `0xe234959595...` | 20 | -0.05c | 47% | 0.68 | 17 | 38 | NOISE (busy, not sharp) |
| `0x74471a007d...` | 17 | -1.10c | 47% | 0.69 | 13 | 51 | FADE (bets the wrong way) |
| `0x35bbbad241...` | 12 | -1.63c | 42% | 0.81 | 7 | 30 | FADE (bets the wrong way) |
| `0x6d9fc316c3...` | 16 | -1.81c | 27% | 0.98 | 11 | 40 | FADE (bets the wrong way) |
| `0xb10047d6a2...` | 19 | -3.92c | 44% | 0.76 | 20 | 51 | FADE (bets the wrong way) |
| `0xdf17f4a8dd...` | 15 | -4.16c | 64% | 0.21 | 14 | 27 | FADE (bets the wrong way) |

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
