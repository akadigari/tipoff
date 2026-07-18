# Calibration week review

_Auto-generated 2026-07-18T06:13:42Z. Covers 2026-07-11T05:10:28Z → 2026-07-18T06:13:42Z. Unlike REPORT.md, calibration-mode alerts ARE included here — this is the tuning review, not the pre-registered verdict._

## Totals

- **172 paper positions** (216 additional MONITOR-grade alerts, never traded)
- **Graded: 8** — 5W–3L, avg ROI -8.3%, avg CLV +6.2c
- Informed-flow reads: 5 informed-like · 0 early-but-wrong · 3 late-money · 0 neutral
- 6274 research candidates logged; 5000 watch entries

## What the filters rejected (top reasons)

| Reason | Count |
|---|---|
| score 35 < 40 | 1613 |
| thin | 1516 |
| too late | 884 |
| already holding (open ledger row) | 758 |
| monitor cap for this run | 591 |
| longshot | 458 |
| not catchable | 246 |
| MONITOR alert sent | 195 |
| gated | 195 |
| duplicate leg of alerted event | 187 |
| re-alert cooldown (monitor) | 162 |
| score 19 < 40 | 126 |

## Per-category (calibration included)

| Category | Alerts | Graded | Win% | Avg ROI | Avg CLV |
|---|---|---|---|---|---|
| entertainment | 2 | 0 | 0% | +0.0% | +0.0c |
| politics | 24 | 0 | 0% | +0.0% | +0.0c |
| sports | 31 | 4 | 25% | -62.1% | -15.0c |
| crypto | 22 | 1 | 100% | +17.6% | +12.0c |
| other | 93 | 3 | 100% | +54.8% | +32.7c |
| ALL | 172 | 8 | 62% | -8.3% | +6.2c |

## Per-trigger (calibration included)

| Trigger | Graded | Win% | Avg CLV |
|---|---|---|---|
| price_jump | 7 | 71% | +8.1c |
| volume_spike | 7 | 71% | +14.0c |
| cross_platform | 1 | 0% | -7.0c |
| price_impact | 1 | 0% | -48.0c |

## How to use this

1. Sort the ledger by `read`: `early-but-wrong` rows are real
   signals with unlucky outcomes — the archetype to protect.
   `late-money` rows are what to filter harder.
2. If good alerts died in the top filter reasons above, loosen
   that one gate value in config.py; if junk alerted, raise the
   relevant signal threshold.
3. Normal mode (score >= 55) is now live; the pre-registered
   verdict accumulates in REPORT.md from here on.
