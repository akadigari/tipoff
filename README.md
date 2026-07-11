# Tipoff

**A cloud-run scanner that watches Kalshi and Polymarket for informed-money
footprints, alerts on Telegram when a signal is still followable, and
paper-tracks every alert so the data — not vibes — decides whether any market
niche is worth following.**

Runs entirely on GitHub Actions (hourly cron, no server, laptop off). It never
places an order.

## Honest framing — read this first

Tipoff is a **paper-testing research tool**. The question it exists to answer:

> When smart/informed money shows up in public prediction-market data, is
> there still edge left by the time an outside observer could react — and in
> which category?

It **detects and follows informed money in public data** (prices, volumes,
on-chain trades). It does not place trades, live or otherwise, and it has
nothing to do with trading on non-public information — "insider trading scoop"
in the alert header is the joke, not the method. Every alert goes into a paper
ledger and gets graded on resolution, with **closing-line value (CLV)** as the
primary metric. If a category's CLV says "you were always late," the honest
answer is that niche is not followable, and Tipoff will tell you so.

## What it scans

| Source | Endpoint | What it's used for |
|---|---|---|
| Kalshi | `api.elections.kalshi.com/trade-api/v2/events` (nested markets) | open binary markets + category, price/volume/depth-at-touch |
| Polymarket | `gamma-api.polymarket.com/markets` | top markets by 24h volume, price/volume/liquidity |
| Polymarket (on-chain) | `data-api.polymarket.com/trades`, `/activity` | individual trades and wallet freshness |

Each hourly run snapshots every tracked market (≥1,000 units of 24h volume,
top 1,200 per platform) and folds the snapshot into a compact online baseline
(EWMA of hourly volume rate + a window of recent price moves) stored in
`state/baselines.json`. A market needs **8 observations (~8 hours) of warm-up**
before spike detection goes live on it, so the first day is quiet by design.

## Signals

All thresholds are pre-registered in the `CFG` block at the top of
[tipoff.py](tipoff.py) — no tuning after the fact.

1. **Volume spike** — this hour's volume rate is ≥3 standard deviations above
   the market's *own* baseline (and the absolute delta is big enough to
   matter; a 50× spike on a dust market is noise).
2. **Price jump** — a move of ≥8¢ within ≤3h that's also ≥3× the market's
   median recent move. *Scheduled-news proxy:* jumps within 12h of resolution
   don't count — that close to the end, a move is usually the event itself
   happening, not informed money arriving early.
3. **Large on-chain trade** (Polymarket) — a single trade ≥$5,000 notional
   since the last snapshot.
4. **Fresh wallet loading up** (Polymarket) — the large trade came from a
   wallet whose entire visible history is less than a week old. Classic
   "new wallet funded for one opinion" pattern.

Signal points sum to a 0–100 score; alerts require **score ≥60**. No single
signal can reach 60 alone — an alert always means at least two independent
things fired (e.g. volume spike + price jump, or price jump + large trade).
On-chain checks only run on markets that already look anomalous, keeping the
API budget to roughly 75 requests per cycle.

## The followability gate — why it exists

A real signal you can't act on at a fair price is trivia, not edge. The core
failure mode of "follow the smart money" is **being the exit liquidity**: by
the time the anomaly is visible, the price has already absorbed the
information. So every scored signal must pass ALL of these before it may
alert:

| Check | Threshold | Why it matters |
|---|---|---|
| Price not fully moved | entry ≤ 85¢ | above this, the move already happened — you're late |
| Not a longshot | entry ≥ 5¢ | sub-5¢ churn is lottery-ticket noise, not an information lag |
| Spread | ≤ 5¢ | wide spread = your fill won't resemble the signal price |
| Depth | ≥ $500 at the touch (Kalshi) / ≥ $2,000 book liquidity (Polymarket, proxy) | must be able to fill a small size |
| Resolves slow enough | ≥ 6h out | if it resolves now, there is no lag window to exploit |
| Resolves fast enough | ≤ 90 days | capital dead for months makes CLV meaningless |

Signals that score high but fail the gate are logged to
[ledger/watch_log.csv](ledger/watch_log.csv) as `WATCH` with the exact reasons
— useful for later analysis of what the gate is costing.

Extra alert hygiene: max 5 alerts per run (overflow → watch log), a 48h
per-market re-alert cooldown, and no re-alerting a market you already "hold"
in the paper ledger.

## Telegram alerts

On a strong + followable signal you get one message, built to be skimmed on a
phone:

```
🚨🚨 ALERT!!! INSIDER TRADING SCOOP 🚨🚨

📍 Will the Fed cut rates in September?
   [kalshi · KXFED-25SEP-C]
🔔 Signal: volume spike (12x baseline, z=4.1) + price jump +9c in 1.0h
💵 Price: 62c — buy YES
🏷 Category: politics
📐 Suggested size: $50 (paper)
⚡ Score 72/100 · resolves in 30h
⏳ Window open — verify + move.
```

Silence means nothing fired — the bot does not send heartbeats.

## Paper ledger + CLV grading

Every alert is appended to [ledger/ledger.csv](ledger/ledger.csv) with the
price you'd have paid (the ask for the alerted side). Each later run refreshes
the market's current price (`last_price`) while the position is open; when the
market resolves, the row is graded:

- **ROI** — per dollar staked: `(1 − entry)/entry` on a win, `−1` on a loss.
- **CLV (closing-line value)** — `final observed price − entry price`, in
  probability points. **This is the primary metric.** Positive CLV means the
  market kept moving your way after the alert — the signal led the market and
  following it was early money. Negative CLV means you were the exit
  liquidity. CLV is outcome-independent (a lost bet can still have positive
  CLV) and converges far faster than ROI, which is dominated by variance at
  small sample sizes.

### How to read the per-category verdict

[ledger/REPORT.md](ledger/REPORT.md) is regenerated every run — one row per
category (entertainment / politics / sports / crypto / other) plus `ALL`:

| Verdict | Pre-registered rule | Meaning |
|---|---|---|
| `INSUFFICIENT DATA` | < 20 graded alerts | keep collecting; ignore ROI/win% until then |
| `FOLLOWABLE` | avg CLV > +2¢ **and** avg ROI > 0 | signals in this niche lead the market by enough to act on |
| `MARGINAL` | avg CLV > 0 but thin or ROI ≤ 0 | edge exists but likely eaten by spread/fees |
| `NOT FOLLOWABLE` | avg CLV ≤ 0 | by alert time you're late; following is donating |

The interesting outcome is the *split*: e.g. entertainment markets (few
professionals, real information leaks) grading `FOLLOWABLE` while sports
grades `NOT FOLLOWABLE` (sharps are faster than any hourly cron) would itself
be a publishable finding — and exactly what this tool is for.

## Running it

### Locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt pytest
pytest                          # 60+ unit tests, no network needed

cp .env.example .env            # then edit; .env is gitignored
python tipoff.py                # one scan cycle
```

With `TIPOFF_DRY_RUN=1` (default in `.env.example`), alerts are printed
instead of sent. Note the warm-up: signals only fire after a market has ~8
snapshots of history, so single local runs will mostly just build baseline.

### On GitHub Actions

[.github/workflows/tipoff.yml](.github/workflows/tipoff.yml) runs the scanner
**hourly** (at :07 — GitHub delays top-of-hour crons) and commits the updated
`state/` + `ledger/` back to the repo, so the repo itself is the database.

Setup:

1. Push this repo to GitHub as a **private** repository.
2. Add the secrets (below).
3. Actions tab → *Tipoff scanner* → *Run workflow* to test immediately;
   the hourly cron takes over from there.

Budget note: ~1–2 min/run × 24 runs/day ≈ 900–1,500 Actions minutes/month,
inside the 2,000 free minutes for private repos but not by miles. If you get
tight, change the cron to `7 */2 * * *` (every 2h) — the baseline math handles
irregular gaps.

### Secrets

| Secret | What it is |
|---|---|
| `TELEGRAM_BOT_TOKEN` | from [@BotFather](https://t.me/BotFather) → `/newbot` |
| `TELEGRAM_CHAT_ID` | your chat's id — DM the bot once, then check `https://api.telegram.org/bot<TOKEN>/getUpdates` |

Add them in GitHub → repo → **Settings → Secrets and variables → Actions →
New repository secret**. No other API keys are needed: all market-data
endpoints used are public and unauthenticated.

**Never** put keys in code or commits. Locally they live in `.env`
(gitignored); in the cloud they exist only as GitHub Secrets injected into the
workflow environment.

## Repo layout

```
tipoff.py                    the scanner — one invocation = one cycle
tests/                       signal, gate, telegram, ledger/CLV tests
.github/workflows/tipoff.yml hourly cron + ledger commit-back
state/baselines.json         per-market EWMA baselines (bot-committed)
ledger/ledger.csv            every alert, graded on resolution
ledger/watch_log.csv         signals that fired but failed the gate
ledger/REPORT.md             per-category CLV verdict (regenerated each run)
```

## Known limitations (by design, documented up front)

- **Hourly cadence is the floor on speed.** Anything where informed money is
  faster than ~1h (in-game sports, breaking crypto news) should grade NOT
  FOLLOWABLE — that's a finding, not a bug.
- **Polymarket depth is a proxy** (Gamma book liquidity, not touch size).
  Kalshi depth is the real size at the inside quote.
- **Scheduled-news detection is a heuristic** (time-to-resolution window). A
  jump on a pre-announced poll release >12h before close can still fire.
- **Paper fills are optimistic**: entry at the displayed ask, no fees, no
  slippage beyond the spread. Real following would do somewhat worse — so a
  verdict that's only barely FOLLOWABLE should be treated as MARGINAL.
- **No live orders, ever.** If the verdict ever justifies real money, that's
  a separate, deliberate step with its own risk controls.
