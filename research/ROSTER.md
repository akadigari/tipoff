# Wallet roster

_Auto-generated 2026-08-26T11:38:45Z. 1186 flagged wallets, 19 with enough graded trades to judge, 2 that beat a coin flip._

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
| `0xf705fa0452...` | 65 | +4.23c | 65% | 0.01 | 58 | 182 | WATCH (beats luck) |
| `0x1465b79bff...` | 38 | +1.24c | 66% | 0.05 | 18 | 101 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0x6db983ff1c...` | 13 | +4.15c | 60% | 0.38 | 12 | 27 | PROMISING (edge, luck not ruled out) |
| `0xcc500cbcc8...` | 37 | +3.02c | 63% | 0.09 | 23 | 84 | PROMISING (edge, luck not ruled out) |
| `0x401ee31e9e...` | 18 | +1.03c | 60% | 0.30 | 8 | 22 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 23 | +1.02c | 64% | 0.14 | 24 | 132 | PROMISING (edge, luck not ruled out) |

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xf705fa0452...` | 65 | +4.23c | 65% | 0.01 | 58 | 182 | WATCH (beats luck) |
| `0x6db983ff1c...` | 13 | +4.15c | 60% | 0.38 | 12 | 27 | PROMISING (edge, luck not ruled out) |
| `0xcc500cbcc8...` | 37 | +3.02c | 63% | 0.09 | 23 | 84 | PROMISING (edge, luck not ruled out) |
| `0x1465b79bff...` | 38 | +1.24c | 66% | 0.05 | 18 | 101 | WATCH (beats luck) |
| `0x401ee31e9e...` | 18 | +1.03c | 60% | 0.30 | 8 | 22 | PROMISING (edge, luck not ruled out) |
| `0x122cb94c43...` | 23 | +1.02c | 64% | 0.14 | 24 | 132 | PROMISING (edge, luck not ruled out) |
| `0x35bbbad241...` | 21 | +0.88c | 57% | 0.33 | 12 | 65 | NOISE (busy, not sharp) |
| `0xa19cbababc...` | 14 | +0.83c | 58% | 0.39 | 9 | 20 | NOISE (busy, not sharp) |
| `0x252d7bae5e...` | 15 | +0.64c | 57% | 0.39 | 21 | 41 | NOISE (busy, not sharp) |
| `0xcdf82242c9...` | 12 | +0.62c | 88% | 0.04 | 14 | 33 | NOISE (busy, not sharp) |
| `0x000d257d2d...` | 13 | +0.21c | 64% | 0.27 | 12 | 40 | NOISE (busy, not sharp) |
| `0x6d9fc316c3...` | 17 | +0.18c | 42% | 0.81 | 14 | 67 | NOISE (busy, not sharp) |
| `0xc2de93c744...` | 12 | +0.08c | 67% | 0.19 | 3 | 25 | NOISE (busy, not sharp) |
| `0x6e2c3937e6...` | 14 | -0.25c | 62% | 0.29 | 11 | 38 | NOISE (busy, not sharp) |
| `0x03805a13a0...` | 12 | -0.71c | 42% | 0.81 | 11 | 20 | NOISE (busy, not sharp) |
| `0xe734e7bf7c...` | 27 | -0.74c | 42% | 0.85 | 11 | 132 | NOISE (busy, not sharp) |
| `0x56e777a0ac...` | 17 | -2.62c | 59% | 0.31 | 6 | 32 | FADE (bets the wrong way) |
| `0x06dc51826b...` | 51 | -5.75c | 60% | 0.10 | 69 | 233 | FADE (bets the wrong way) |
| `0x56ad6bd059...` | 12 | -7.21c | 30% | 0.94 | 11 | 34 | FADE (bets the wrong way) |

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
