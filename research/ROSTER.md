# Wallet roster

_Auto-generated 2026-07-29T21:08:22Z. 1250 flagged wallets, 16 with enough graded trades to judge, 1 that beat a coin flip._

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
| `0xeb6f0a13ea...` | 14 | +5.29c | 100% | 0.00 | 4 | 22 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x74471a007d...` | 18 | +5.35c | 67% | 0.12 | 13 | 32 | PROMISING (edge, luck not ruled out) |
| `0x7bc14171cc...` | 12 | +1.38c | 58% | 0.39 | 14 | 17 | PROMISING (edge, luck not ruled out) |
| `0x60a92c8620...` | 17 | +1.01c | 56% | 0.40 | 13 | 33 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x74471a007d...` | 18 | +5.35c | 67% | 0.12 | 13 | 32 | PROMISING (edge, luck not ruled out) |
| `0xeb6f0a13ea...` | 14 | +5.29c | 100% | 0.00 | 4 | 22 | WATCH (beats luck) |
| `0x7bc14171cc...` | 12 | +1.38c | 58% | 0.39 | 14 | 17 | PROMISING (edge, luck not ruled out) |
| `0x60a92c8620...` | 17 | +1.01c | 56% | 0.40 | 13 | 33 | PROMISING (edge, luck not ruled out) |
| `0xdbd028b4af...` | 12 | +0.87c | 64% | 0.27 | 12 | 14 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 19 | +0.48c | 61% | 0.24 | 16 | 38 | NOISE (busy, not sharp) |
| `0x8c66e28fbe...` | 15 | +0.07c | 47% | 0.70 | 10 | 18 | NOISE (busy, not sharp) |
| `0xd218e47477...` | 12 | +0.03c | 44% | 0.75 | 15 | 20 | NOISE (busy, not sharp) |
| `0x21e25662e5...` | 27 | +0.02c | 56% | 0.41 | 10 | 35 | NOISE (busy, not sharp) |
| `0x1465b79bff...` | 17 | -0.04c | 50% | 0.61 | 6 | 37 | NOISE (busy, not sharp) |
| `0xf705fa0452...` | 16 | -0.50c | 67% | 0.15 | 14 | 37 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 34 | -1.20c | 50% | 0.57 | 14 | 48 | FADE (bets the wrong way) |
| `0x511f9c7714...` | 24 | -2.22c | 55% | 0.42 | 23 | 52 | FADE (bets the wrong way) |
| `0x6d9fc316c3...` | 12 | -2.75c | 67% | 0.19 | 15 | 19 | FADE (bets the wrong way) |
| `0x6916cc00aa...` | 13 | -2.75c | 55% | 0.50 | 11 | 33 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 21 | -6.47c | 48% | 0.67 | 33 | 55 | FADE (bets the wrong way) |

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
