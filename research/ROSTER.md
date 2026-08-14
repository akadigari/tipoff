# Wallet roster

_Auto-generated 2026-08-14T22:33:45Z. 1190 flagged wallets, 17 with enough graded trades to judge, 4 that beat a coin flip._

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
| `0x7e5972bfc2...` | 12 | +8.60c | 83% | 0.02 | 9 | 22 | WATCH (beats luck) |
| `0x23d81ba937...` | 15 | +8.53c | 79% | 0.03 | 11 | 28 | WATCH (beats luck) |
| `0xfc2f4f50ce...` | 18 | +5.98c | 93% | 0.00 | 11 | 45 | WATCH (beats luck) |
| `0x06dc51826b...` | 26 | +1.64c | 79% | 0.00 | 30 | 123 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xdf44c3e8ce...` | 13 | +4.82c | 64% | 0.27 | 12 | 18 | PROMISING (edge, luck not ruled out) |
| `0xbd0477e08d...` | 16 | +2.02c | 56% | 0.40 | 11 | 33 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x7e5972bfc2...` | 12 | +8.60c | 83% | 0.02 | 9 | 22 | WATCH (beats luck) |
| `0x23d81ba937...` | 15 | +8.53c | 79% | 0.03 | 11 | 28 | WATCH (beats luck) |
| `0xfc2f4f50ce...` | 18 | +5.98c | 93% | 0.00 | 11 | 45 | WATCH (beats luck) |
| `0xdf44c3e8ce...` | 13 | +4.82c | 64% | 0.27 | 12 | 18 | PROMISING (edge, luck not ruled out) |
| `0xbd0477e08d...` | 16 | +2.02c | 56% | 0.40 | 11 | 33 | PROMISING (edge, luck not ruled out) |
| `0x06dc51826b...` | 26 | +1.64c | 79% | 0.00 | 30 | 123 | WATCH (beats luck) |
| `0xeb490d0534...` | 22 | +0.45c | 50% | 0.59 | 12 | 35 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 21 | +0.32c | 50% | 0.59 | 25 | 80 | NOISE (busy, not sharp) |
| `0x000d257d2d...` | 15 | +0.23c | 50% | 0.61 | 13 | 23 | NOISE (busy, not sharp) |
| `0x3eae57986b...` | 15 | +0.17c | 58% | 0.39 | 18 | 38 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 12 | -0.03c | 45% | 0.73 | 17 | 76 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 33 | -0.23c | 64% | 0.08 | 12 | 96 | NOISE (busy, not sharp) |
| `0x74471a007d...` | 16 | -0.86c | 56% | 0.40 | 13 | 53 | NOISE (busy, not sharp) |
| `0x162f6fff88...` | 13 | -0.88c | 36% | 0.89 | 11 | 26 | NOISE (busy, not sharp) |
| `0x6d9fc316c3...` | 12 | -3.21c | 25% | 0.98 | 10 | 41 | FADE (bets the wrong way) |
| `0xb10047d6a2...` | 21 | -3.82c | 40% | 0.87 | 19 | 52 | FADE (bets the wrong way) |
| `0xdf17f4a8dd...` | 15 | -4.16c | 64% | 0.21 | 15 | 28 | FADE (bets the wrong way) |

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
