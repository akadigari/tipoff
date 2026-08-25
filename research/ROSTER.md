# Wallet roster

_Auto-generated 2026-08-25T16:49:22Z. 1167 flagged wallets, 17 with enough graded trades to judge, 2 that beat a coin flip._

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
| `0xf705fa0452...` | 63 | +4.03c | 64% | 0.02 | 58 | 178 | WATCH (beats luck) |
| `0x1465b79bff...` | 38 | +1.47c | 66% | 0.05 | 18 | 101 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xa19cbababc...` | 12 | +4.13c | 73% | 0.11 | 10 | 20 | PROMISING (edge, luck not ruled out) |
| `0xcc500cbcc8...` | 26 | +4.12c | 64% | 0.12 | 24 | 82 | PROMISING (edge, luck not ruled out) |
| `0x6db983ff1c...` | 12 | +2.95c | 56% | 0.50 | 11 | 25 | PROMISING (edge, luck not ruled out) |
| `0x6d9fc316c3...` | 18 | +1.04c | 58% | 0.39 | 16 | 67 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 22 | +1.00c | 67% | 0.10 | 25 | 130 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xa19cbababc...` | 12 | +4.13c | 73% | 0.11 | 10 | 20 | PROMISING (edge, luck not ruled out) |
| `0xcc500cbcc8...` | 26 | +4.12c | 64% | 0.12 | 24 | 82 | PROMISING (edge, luck not ruled out) |
| `0xf705fa0452...` | 63 | +4.03c | 64% | 0.02 | 58 | 178 | WATCH (beats luck) |
| `0x6db983ff1c...` | 12 | +2.95c | 56% | 0.50 | 11 | 25 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 38 | +1.47c | 66% | 0.05 | 18 | 101 | WATCH (beats luck) |
| `0x6d9fc316c3...` | 18 | +1.04c | 58% | 0.39 | 16 | 67 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 22 | +1.00c | 67% | 0.10 | 25 | 130 | PROMISING (edge, luck not ruled out) |
| `0x511f9c7714...` | 15 | +0.75c | 50% | 0.61 | 10 | 107 | NOISE (busy, not sharp) |
| `0x401ee31e9e...` | 15 | +0.73c | 58% | 0.39 | 8 | 22 | NOISE (busy, not sharp) |
| `0x000d257d2d...` | 12 | +0.69c | 70% | 0.17 | 12 | 40 | NOISE (busy, not sharp) |
| `0xcdf82242c9...` | 12 | +0.62c | 88% | 0.04 | 14 | 33 | NOISE (busy, not sharp) |
| `0x252d7bae5e...` | 16 | +0.29c | 53% | 0.50 | 21 | 41 | NOISE (busy, not sharp) |
| `0xc2de93c744...` | 12 | +0.08c | 67% | 0.19 | 3 | 25 | NOISE (busy, not sharp) |
| `0x6e2c3937e6...` | 12 | -0.31c | 64% | 0.27 | 11 | 36 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 23 | -0.96c | 48% | 0.67 | 11 | 130 | NOISE (busy, not sharp) |
| `0x56e777a0ac...` | 14 | -3.68c | 50% | 0.61 | 6 | 32 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 44 | -6.44c | 61% | 0.09 | 69 | 228 | FADE (bets the wrong way) |

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
