# Wallet roster

_Auto-generated 2026-08-08T14:41:51Z. 1248 flagged wallets, 17 with enough graded trades to judge, 5 that beat a coin flip._

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
| `0xeb6f0a13ea...` | 13 | +5.19c | 100% | 0.00 | 6 | 31 | WATCH (beats luck) |
| `0xbaa2bcb543...` | 18 | +4.13c | 81% | 0.01 | 16 | 25 | WATCH (beats luck) |
| `0xeb490d0534...` | 12 | +3.20c | 82% | 0.04 | 12 | 17 | WATCH (beats luck) |
| `0x30e443872d...` | 12 | +3.02c | 100% | 0.00 | 7 | 15 | WATCH (beats luck) |
| `0x60a92c8620...` | 16 | +2.52c | 75% | 0.04 | 11 | 43 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x162f6fff88...` | 16 | +5.83c | 71% | 0.09 | 13 | 22 | PROMISING (edge, luck not ruled out) |
| `0xa65c87d5fa...` | 13 | +3.15c | 62% | 0.29 | 10 | 17 | PROMISING (edge, luck not ruled out) |
| `0xfc2f4f50ce...` | 12 | +3.12c | 50% | 0.61 | 13 | 29 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 21 | +1.79c | 55% | 0.41 | 19 | 55 | PROMISING (edge, luck not ruled out) |
| `0xe234959595...` | 26 | +1.50c | 58% | 0.27 | 22 | 30 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x162f6fff88...` | 16 | +5.83c | 71% | 0.09 | 13 | 22 | PROMISING (edge, luck not ruled out) |
| `0xeb6f0a13ea...` | 13 | +5.19c | 100% | 0.00 | 6 | 31 | WATCH (beats luck) |
| `0xbaa2bcb543...` | 18 | +4.13c | 81% | 0.01 | 16 | 25 | WATCH (beats luck) |
| `0xeb490d0534...` | 12 | +3.20c | 82% | 0.04 | 12 | 17 | WATCH (beats luck) |
| `0xa65c87d5fa...` | 13 | +3.15c | 62% | 0.29 | 10 | 17 | PROMISING (edge, luck not ruled out) |
| `0xfc2f4f50ce...` | 12 | +3.12c | 50% | 0.61 | 13 | 29 | PROMISING (edge, luck not ruled out) |
| `0x30e443872d...` | 12 | +3.02c | 100% | 0.00 | 7 | 15 | WATCH (beats luck) |
| `0x60a92c8620...` | 16 | +2.52c | 75% | 0.04 | 11 | 43 | WATCH (beats luck) |
| `0x122cb94c43...` | 21 | +1.79c | 55% | 0.41 | 19 | 55 | PROMISING (edge, luck not ruled out) |
| `0xe234959595...` | 26 | +1.50c | 58% | 0.27 | 22 | 30 | PROMISING (edge, luck not ruled out) |
| `0x6d9fc316c3...` | 15 | +0.57c | 54% | 0.50 | 17 | 31 | NOISE (busy, not sharp) |
| `0xf705fa0452...` | 20 | +0.25c | 58% | 0.32 | 20 | 54 | NOISE (busy, not sharp) |
| `0x0c0e270cf8...` | 13 | -0.12c | 73% | 0.11 | 8 | 25 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 41 | -0.34c | 52% | 0.44 | 20 | 74 | NOISE (busy, not sharp) |
| `0xbd0477e08d...` | 15 | -0.50c | 53% | 0.50 | 11 | 26 | NOISE (busy, not sharp) |
| `0x06dc51826b...` | 29 | -0.73c | 68% | 0.04 | 46 | 90 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 17 | -2.35c | 64% | 0.21 | 22 | 69 | FADE (bets the wrong way) |

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
