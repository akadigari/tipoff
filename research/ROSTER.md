# Wallet roster

_Auto-generated 2026-08-15T13:37:36Z. 1173 flagged wallets, 15 with enough graded trades to judge, 4 that beat a coin flip._

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
| `0x23d81ba937...` | 13 | +9.35c | 77% | 0.05 | 10 | 28 | WATCH (beats luck) |
| `0x7e5972bfc2...` | 12 | +8.60c | 83% | 0.02 | 9 | 22 | WATCH (beats luck) |
| `0xfc2f4f50ce...` | 19 | +4.98c | 88% | 0.00 | 11 | 46 | WATCH (beats luck) |
| `0x06dc51826b...` | 27 | +1.72c | 80% | 0.00 | 28 | 124 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xbd0477e08d...` | 13 | +2.95c | 54% | 0.50 | 11 | 33 | PROMISING (edge, luck not ruled out) |
| `0xdf44c3e8ce...` | 15 | +2.33c | 54% | 0.50 | 12 | 18 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x23d81ba937...` | 13 | +9.35c | 77% | 0.05 | 10 | 28 | WATCH (beats luck) |
| `0x7e5972bfc2...` | 12 | +8.60c | 83% | 0.02 | 9 | 22 | WATCH (beats luck) |
| `0xfc2f4f50ce...` | 19 | +4.98c | 88% | 0.00 | 11 | 46 | WATCH (beats luck) |
| `0xbd0477e08d...` | 13 | +2.95c | 54% | 0.50 | 11 | 33 | PROMISING (edge, luck not ruled out) |
| `0xdf44c3e8ce...` | 15 | +2.33c | 54% | 0.50 | 12 | 18 | PROMISING (edge, luck not ruled out) |
| `0x06dc51826b...` | 27 | +1.72c | 80% | 0.00 | 28 | 124 | WATCH (beats luck) |
| `0xeb490d0534...` | 21 | +0.68c | 53% | 0.50 | 12 | 35 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 22 | +0.26c | 47% | 0.68 | 27 | 82 | NOISE (busy, not sharp) |
| `0x000d257d2d...` | 15 | +0.23c | 50% | 0.61 | 13 | 23 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 35 | +0.05c | 66% | 0.05 | 12 | 97 | NOISE (busy, not sharp) |
| `0x3eae57986b...` | 15 | +0.04c | 50% | 0.61 | 20 | 41 | NOISE (busy, not sharp) |
| `0x74471a007d...` | 17 | -0.02c | 53% | 0.50 | 12 | 53 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 12 | -0.03c | 45% | 0.73 | 18 | 77 | NOISE (busy, not sharp) |
| `0xb10047d6a2...` | 22 | -3.63c | 43% | 0.81 | 19 | 53 | FADE (bets the wrong way) |
| `0xdf17f4a8dd...` | 15 | -4.16c | 64% | 0.21 | 17 | 30 | FADE (bets the wrong way) |

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
