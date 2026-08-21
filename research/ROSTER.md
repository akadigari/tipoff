# Wallet roster

_Auto-generated 2026-08-21T15:42:37Z. 1177 flagged wallets, 9 with enough graded trades to judge, 2 that beat a coin flip._

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
| `0xcc500cbcc8...` | 13 | +13.04c | 100% | 0.00 | 14 | 54 | WATCH (beats luck) |
| `0x1465b79bff...` | 16 | +2.99c | 79% | 0.03 | 12 | 65 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xf705fa0452...` | 19 | +6.83c | 67% | 0.12 | 42 | 128 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xcc500cbcc8...` | 13 | +13.04c | 100% | 0.00 | 14 | 54 | WATCH (beats luck) |
| `0xf705fa0452...` | 19 | +6.83c | 67% | 0.12 | 42 | 128 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 16 | +2.99c | 79% | 0.03 | 12 | 65 | WATCH (beats luck) |
| `0x511f9c7714...` | 12 | +0.78c | 58% | 0.39 | 20 | 102 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 31 | +0.46c | 55% | 0.36 | 37 | 117 | NOISE (busy, not sharp) |
| `0xcfee7c48b3...` | 14 | -0.46c | 36% | 0.89 | 5 | 19 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 16 | -2.45c | 50% | 0.60 | 5 | 114 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 29 | -4.52c | 59% | 0.23 | 46 | 184 | FADE (bets the wrong way) |
| `0x6765c1c000...` | 19 | -10.16c | 27% | 0.98 | 5 | 36 | FADE (bets the wrong way) |

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
