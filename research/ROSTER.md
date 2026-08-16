# Wallet roster

_Auto-generated 2026-08-16T19:28:13Z. 1207 flagged wallets, 15 with enough graded trades to judge, 4 that beat a coin flip._

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
| `0xfc2f4f50ce...` | 20 | +4.80c | 88% | 0.00 | 12 | 49 | WATCH (beats luck) |
| `0xe734e7bf7c...` | 31 | +1.46c | 71% | 0.02 | 11 | 98 | WATCH (beats luck) |
| `0x06dc51826b...` | 30 | +1.44c | 71% | 0.02 | 25 | 124 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xdf44c3e8ce...` | 15 | +2.33c | 54% | 0.50 | 12 | 18 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x7e5972bfc2...` | 12 | +8.60c | 83% | 0.02 | 9 | 22 | WATCH (beats luck) |
| `0xfc2f4f50ce...` | 20 | +4.80c | 88% | 0.00 | 12 | 49 | WATCH (beats luck) |
| `0xdf44c3e8ce...` | 15 | +2.33c | 54% | 0.50 | 12 | 18 | PROMISING (edge, luck not ruled out) |
| `0xe734e7bf7c...` | 31 | +1.46c | 71% | 0.02 | 11 | 98 | WATCH (beats luck) |
| `0x06dc51826b...` | 30 | +1.44c | 71% | 0.02 | 25 | 124 | WATCH (beats luck) |
| `0xeb490d0534...` | 21 | +0.61c | 53% | 0.50 | 15 | 42 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 21 | +0.25c | 56% | 0.41 | 28 | 87 | NOISE (busy, not sharp) |
| `0x000d257d2d...` | 14 | +0.22c | 46% | 0.71 | 12 | 23 | NOISE (busy, not sharp) |
| `0x3eae57986b...` | 14 | +0.18c | 55% | 0.50 | 20 | 45 | NOISE (busy, not sharp) |
| `0x74471a007d...` | 17 | -0.02c | 53% | 0.50 | 12 | 54 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 12 | -0.30c | 45% | 0.73 | 25 | 87 | NOISE (busy, not sharp) |
| `0xdf17f4a8dd...` | 14 | -0.60c | 77% | 0.05 | 15 | 32 | NOISE (busy, not sharp) |
| `0x6d9fc316c3...` | 14 | -2.21c | 29% | 0.97 | 10 | 43 | FADE (bets the wrong way) |
| `0x35bbbad241...` | 13 | -2.88c | 23% | 0.99 | 10 | 35 | FADE (bets the wrong way) |
| `0xb10047d6a2...` | 25 | -3.23c | 43% | 0.80 | 20 | 55 | FADE (bets the wrong way) |

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
