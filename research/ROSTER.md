# Wallet roster

_Auto-generated 2026-08-23T23:30:25Z. 1206 flagged wallets, 14 with enough graded trades to judge, 1 that beat a coin flip._

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
| `0xcc500cbcc8...` | 17 | +7.00c | 75% | 0.04 | 19 | 65 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xf705fa0452...` | 48 | +4.43c | 60% | 0.12 | 52 | 165 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 21 | +2.68c | 68% | 0.08 | 16 | 87 | PROMISING (edge, luck not ruled out) |
| `0x6d9fc316c3...` | 14 | +1.55c | 70% | 0.17 | 16 | 64 | PROMISING (edge, luck not ruled out) |
| `0xdf17f4a8dd...` | 12 | +1.13c | 44% | 0.75 | 14 | 48 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xcc500cbcc8...` | 17 | +7.00c | 75% | 0.04 | 19 | 65 | WATCH (beats luck) |
| `0xf705fa0452...` | 48 | +4.43c | 60% | 0.12 | 52 | 165 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 21 | +2.68c | 68% | 0.08 | 16 | 87 | PROMISING (edge, luck not ruled out) |
| `0x6d9fc316c3...` | 14 | +1.55c | 70% | 0.17 | 16 | 64 | PROMISING (edge, luck not ruled out) |
| `0xdf17f4a8dd...` | 12 | +1.13c | 44% | 0.75 | 14 | 48 | PROMISING (edge, luck not ruled out) |
| `0x252d7bae5e...` | 13 | +0.80c | 50% | 0.61 | 22 | 40 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 28 | +0.51c | 56% | 0.35 | 29 | 125 | NOISE (busy, not sharp) |
| `0x511f9c7714...` | 18 | +0.48c | 53% | 0.50 | 19 | 104 | NOISE (busy, not sharp) |
| `0xcfee7c48b3...` | 13 | -0.46c | 40% | 0.83 | 4 | 19 | NOISE (busy, not sharp) |
| `0xb10047d6a2...` | 12 | -1.29c | 55% | 0.50 | 12 | 66 | FADE (bets the wrong way) |
| `0xe734e7bf7c...` | 19 | -2.82c | 44% | 0.76 | 7 | 121 | FADE (bets the wrong way) |
| `0x56ad6bd059...` | 12 | -7.07c | 45% | 0.73 | 12 | 31 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 36 | -7.78c | 58% | 0.20 | 58 | 208 | FADE (bets the wrong way) |
| `0x6765c1c000...` | 16 | -13.48c | 8% | 1.00 | 5 | 36 | FADE (bets the wrong way) |

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
