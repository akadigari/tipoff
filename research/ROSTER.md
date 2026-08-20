# Wallet roster

_Auto-generated 2026-08-20T18:54:00Z. 1147 flagged wallets, 8 with enough graded trades to judge, 0 that beat a coin flip._

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

_None yet._

## Promising (edge, needs more data to rule out luck)

_None yet._

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xeb490d0534...` | 15 | +0.87c | 64% | 0.21 | 10 | 46 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 14 | +0.63c | 50% | 0.61 | 25 | 98 | NOISE (busy, not sharp) |
| `0xc2de93c744...` | 13 | -0.09c | 62% | 0.29 | 3 | 17 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 29 | -0.19c | 56% | 0.35 | 36 | 113 | NOISE (busy, not sharp) |
| `0x06dc51826b...` | 27 | -0.29c | 67% | 0.06 | 42 | 172 | NOISE (busy, not sharp) |
| `0xcfee7c48b3...` | 16 | -0.41c | 33% | 0.93 | 5 | 19 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 15 | -3.24c | 53% | 0.50 | 6 | 109 | FADE (bets the wrong way) |
| `0x6765c1c000...` | 21 | -9.17c | 35% | 0.93 | 6 | 35 | FADE (bets the wrong way) |

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
