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
before spike detection goes live on it, so the first hours are quiet by design.

The baseline is **winsorized**: a one-hour burst is folded into the EWMA
capped at 4× the current mean, so a spike can't inflate its own baseline and
mask the follow-through hours — exactly the hours where informed money keeps
accumulating.

## Configuration

**Every threshold lives in [config.py](config.py)** — one file, commented,
grouped by purpose. Any value can also be overridden per-run with a
`TIPOFF_`-prefixed env var (e.g. `TIPOFF_ALERT_SCORE=50`). Tune after
reviewing the calibration-week logs, not after a single bad beat.

## Signals (balanced middle-ground defaults)

| Signal | Fires when | Max points |
|---|---|---|
| Volume spike | this hour's rate ≥ **3× the market's own baseline**, and the absolute delta is big enough to matter (dust guard) | 35 |
| Price jump | move ≥ **5¢** within ≤3h, ≥3× this market's median recent move, **backed by real volume** (phantom guard: a re-quoted book with no trades behind it doesn't count) | 35 |
| Large on-chain trade (Polymarket) | single trade ≥ **$2k**, *or* ≥ **5× this market's own median trade size** (floor $500 — 5× of dust is still dust) | 30 |
| Fresh wallet (Polymarket) | the big trade came from a wallet whose entire visible history is **< 3 days old**, betting ≥ $1k (+bonus ≥ $5k) | 25 |
| Thin-market bonus | on-chain flow in a market doing < $10k/24h — big bets in obscure markets are the classic insider footprint | 10 |
| Cross-platform confirmation | the same story is moving on *both* venues this cycle (title-matched, with a number veto so different strikes never merge) | 10 |
| Price impact (research-backed) | a ≥3¢ move on volume this market usually absorbs silently — insider trades move prices several times more per dollar than ordinary flow | 15 |
| Repeat actor | the same wallet flagged again on a later scan (side-flips called out) — one print is noise, pressing is a position | 10 |
| Within-trader size | the trade is ≥5× that wallet's own median — out of character even if small in absolute terms | 8 |
| Crowd chatter (Polymarket) | ≥2 distinct commenters crying "insider"/"leak"/"who is buying" on this market in the last 48h while it's moving — the comment section notices before journalists do (deduped per wallet; spam bots don't count twice) | 12 |

Guards that keep the jump signal honest: a **scheduled-news proxy** (jumps
within 12h of resolution are presumed to be the event itself happening, not
early money) and the phantom-volume guard above.

Points sum to a 0–100 score. **No single signal can reach the alert threshold
alone** — even in calibration mode an alert always means at least two
independent things fired. On-chain checks only run on markets that already
look anomalous, keeping the API budget to ~75 requests per cycle.

## The followability gate — why it exists

A real signal you can't act on at a fair price is trivia, not edge. The core
failure mode of "follow the smart money" is **being the exit liquidity**. So
every scored signal must pass ALL of these before it may alert:

| Check | Threshold | Why it matters |
|---|---|---|
| Still catchable | entry ≤ **3¢ above the signal price** | if the ask has already run away, your fill won't resemble what fired |
| Price not fully moved | entry ≤ 85¢ | above this, the move already happened — you're late |
| Not a longshot | entry ≥ 5¢ | sub-5¢ churn is lottery-ticket noise |
| Depth | ≥ $500 at the touch (Kalshi) / ≥ $2,000 book liquidity (Polymarket, proxy) | must be able to fill a small size |
| Resolves slow enough | **> 24h out** | if it resolves now, there is no lag window to exploit |
| Resolves fast enough | ≤ 90 days | capital dead for months makes CLV meaningless |

Signals that fire but fail the gate are logged to
[ledger/watch_log.csv](ledger/watch_log.csv) as `WATCH` **with the exact
reasons** — the raw material for tuning.

One alert per story: multiple legs of the same event spiking on one news item
are deduped to the top scorer, and a cross-platform twin of an already-sent
alert is dropped (its confirmation is already priced into the kept one's
score). Plus: max alerts per run, a per-market re-alert cooldown, and no
re-alerting a market already "held" in the paper ledger.

## Calibration week

For the **first 7 days after deployment** Tipoff runs looser on purpose:

- alert threshold drops (40 vs 55), more alerts allowed per run, shorter
  cooldown — you *want* borderline stuff hitting your phone this week;
- every alert is tagged `mode=calib` in the ledger and **excluded from the
  pre-registered verdict stats** (they were caught with different thresholds;
  mixing them in would bias the experiment);
- the watch log records everything that fired-but-filtered, with reasons.

At the end of the week, skim `ledger/watch_log.csv` and the calib alerts:
if good stuff died at the gate, loosen that gate value in config.py; if junk
alerted, raise the relevant signal threshold. Then let normal mode run.

## Telegram

### Alerts

```
🚨🚨 ALERT!!! INSIDER TRADING SCOOP 🚨🚨

📍 Will the Fed cut rates in September?
   [kalshi · KXFED-25SEP-C]
🔔 Signal: volume spike (12x baseline) + price jump +9c in 1.0h
💵 Price: 62c — buy YES
🏷 Category: politics
📐 Suggested size: $50 (paper)
⚡ Score 72/100 · resolves in 30h
⏳ Window open — verify + move.
```

### Daily still-alive ping (the health bar)

Once a day (targeting 13:00 UTC ≈ 9am ET) you get one short summary even when
nothing fired, so silence never means "maybe it's broken":

```
🟢 Tipoff daily check-in — running fine
Last 24h: 24 scans · 1,654 markets · 0 alerts · 7 watches
All quiet — nothing strong + followable fired.
🩺 kalshi 1,175 ✓ · poly 476 ✓ · 1,540 baselines warm · 0 fetch errors (24h)
⛽ 412/1,800 Actions min (23%) · volume-matched schedule
📏 calibration week: day 3/7 — running loose, review the watch log
```

The 🩺 line is the health bar: markets per platform (⚠️ if one went dark),
how many baselines are past warm-up, and API errors over the last day. The
⛽ line is the minutes fuel gauge.

### When something actually breaks, it tells you — three layers

1. **🔴 Crash alert** — if a run *fails outright*, a workflow-level step
   (independent of the Python code that just crashed) sends a red Telegram
   alert with a direct link to the failing run's logs.
2. **⚠️ Platform-down warning** — if Kalshi or Polymarket returns zero
   markets while the other still works, you get a warning (at most one per
   day per platform) and scanning continues one-legged.
3. **Silence rule** — the only failure that can't message you is GitHub
   itself not running the workflow. That's why the daily ping exists: **no
   ping for two days = go look at the Actions tab.**

## Paper ledger + CLV grading

Every alert is appended to [ledger/ledger.csv](ledger/ledger.csv) with the
price you'd have paid (the ask for the alerted side). Each later run refreshes
the market's current price while the position is open; when the market
resolves, the row is graded:

- **ROI** — per dollar staked: `(1 − entry)/entry` on a win, `−1` on a loss.
- **CLV (closing-line value)** — `final observed price − entry price`, in
  probability points. **This is the primary metric.** Positive CLV means the
  market kept moving your way after the alert — the signal led the market and
  following it was early money. Negative CLV means you were the exit
  liquidity. CLV is outcome-independent (a lost bet can still have positive
  CLV) and converges far faster than ROI, which is dominated by variance at
  small sample sizes.

### The research dataset — signals.csv

The paper ledger only grades what *alerted*. [research/signals.csv](research/signals.csv)
goes further: **every signal candidate** — alerted or filtered — gets a row
with its full context (signal types, score, side, YES price, 24h volume,
depth, time to resolution, the exact gate reasons, and the whale wallet
address when an on-chain trade fired). Then later runs fill in where the
YES price actually went **1h, 6h, and 24h after the signal** (`p_1h`,
`p_6h`, `p_24h`; `na` if the market left the universe first).

After a few weeks this becomes a labeled dataset that can answer questions
the ledger can't:

- Do volume spikes *without* a price jump predict moves (early money we're
  filtering out), or are they noise?
- Which category's whales actually move markets — and does the fresh-wallet
  flag add anything on top of trade size?
- Is the gate throwing away winners? (compare forward moves of gate-failed
  vs gate-passed candidates)
- Do specific wallet addresses show up repeatedly *before* moves? (group by
  the `wallet` column — a personal smart-money list falls out of the data)

The file is capped at 10,000 rows (oldest fall off) and committed back by
the bot like everything else, so it accumulates history with zero effort.

### How to read the per-category verdict

[ledger/REPORT.md](ledger/REPORT.md) is regenerated every run — one row per
category (entertainment / politics / sports / crypto / other) plus `ALL`.
Calibration-week alerts are excluded from these stats.

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
pytest                          # 100+ unit tests, no network needed

cp .env.example .env            # then edit; .env is gitignored
python tipoff.py                # one scan cycle
```

With `TIPOFF_DRY_RUN=1` (default in `.env.example`), alerts are printed
instead of sent.

### On GitHub Actions

[.github/workflows/tipoff.yml](.github/workflows/tipoff.yml) runs the scanner
on the volume-matched schedule below and commits the updated `state/` +
`ledger/` back to the repo, so the repo itself is the database.

## Scan cadence — measured, not guessed

Scanning hourly around the clock spends ~25% of the minutes budget on hours
where nothing trades. To size the schedule, hour-of-day volume was measured
(2026-07) across both platforms: 30 top Kalshi markets × 7 days of hourly
candlesticks, and 29 top Polymarket markets × 72h of on-chain trades — each
market's distribution normalized before averaging, so no single whale market
dominates.

| UTC window | Share of traded volume | Cadence |
|---|---|---|
| 13:00–06:59 (US morning → late night) | **~89%** | hourly (`7 0-6,13-23 * * *`) |
| 07:00–12:59 (~3–9am ET dead zone) | ~11% (<2%/hour) | touch-runs at 08:07 + 11:07 |

That's **20 runs/day ≈ 620/month ≈ 700–1,300 billed minutes** (runs bill
1–2 min each), comfortably inside the 1,800 budget with headroom for cron
jitter and other repos. The dead-zone gaps never exceed 3h, so the
price-jump detector (window ≤ 3.5h) stays live around the clock — a jump at
4am ET is caught by the 08:07 run, usually still inside the catchable gate
because nothing else is trading either.

Deliberately NOT implemented yet: 30-minute scanning during the hottest
hours (21:00–03:59 UTC carries ~53% of volume). It would plausibly convert
some "not catchable" watches into alerts, but it costs ~40% more minutes on
a hunch. The calibration-week watch log records exactly how often signals
die at the catchable gate during those hours — if that number turns out
big, add `- cron: "37 0-3,21-23 * * *"` to the schedule and it's done.

Setup:

1. Push this repo to GitHub as a **private** repository.
2. Add the secrets (below).
3. Actions tab → *Tipoff scanner* → *Run workflow* to test immediately;
   the hourly cron takes over from there.

## Minutes guard + self-throttling

Running out of Actions minutes is the one failure the daily ping can't warn
about —
no minutes means no ping, which looks exactly like "all quiet". So every run
audits the month's usage and acts before the tank is empty:

- **Measurement** — billable minutes are computed from this repo's own
  workflow-run history via the built-in `GITHUB_TOKEN` (no extra secret, no
  billing scope). The budget defaults to 1,800 (`ACTIONS_BUDGET_MIN` in
  config.py), leaving headroom for your other repos.
- **Warning** — one Telegram alert when usage crosses 80%, with the
  month-end projection.
- **Self-throttling** — when the projection exceeds budget (or usage hits
  95%), Tipoff slows itself down to every 2h / 3h / 6h:
  - **With the optional `WORKFLOW_EDIT_TOKEN` secret** it literally rewrites
    the cron line in its own workflow file via the GitHub API and tells you
    it did — full proportional savings.
  - **Without it** it falls back to skip-mode: the cron still fires hourly
    but off-cadence runs exit in seconds. Skipped runs still bill GitHub's
    1-minute floor, so this only saves about half — the alert nags you about
    the PAT for a reason.
- The throttle only ever tightens within a month; on the 1st it resets to
  hourly and tells you. The daily ping always carries a fuel gauge line
  (`⛽ 412/1,800 Actions min (23%) · hourly`), and the skip cadence is
  anchored so the ping-hour run always executes.

To enable true self-modification, create a **fine-grained PAT**: GitHub →
Settings → Developer settings → Fine-grained tokens → generate one scoped to
**only the tipoff repo** with repository permissions **Contents: read/write**
and **Workflows: read/write**, then add it as the `WORKFLOW_EDIT_TOKEN`
Actions secret. Optional but recommended.

### Secrets

| Secret | Required | What it is |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | yes | from [@BotFather](https://t.me/BotFather) → `/newbot` |
| `TELEGRAM_CHAT_ID` | yes | your chat's id — DM the bot once, then check `https://api.telegram.org/bot<TOKEN>/getUpdates` |
| `WORKFLOW_EDIT_TOKEN` | optional | fine-grained PAT (this repo only; Contents + Workflows read/write) that lets Tipoff rewrite its own cron when minutes run low |

Add them in GitHub → repo → **Settings → Secrets and variables → Actions →
New repository secret**. No other API keys are needed: all market-data
endpoints used are public and unauthenticated.

**Never** put keys in code or commits. Locally they live in `.env`
(gitignored); in the cloud they exist only as GitHub Secrets injected into the
workflow environment.

## Repo layout

```
tipoff.py                    the scanner — one invocation = one cycle
config.py                    ALL thresholds, commented — the only file to tune
tests/                       signal, gate, dedup, telegram, ledger/CLV tests
.github/workflows/tipoff.yml hourly cron + ledger commit-back
state/baselines.json         per-market EWMA baselines (bot-committed)
ledger/ledger.csv            every alert, graded on resolution
ledger/watch_log.csv         signals that fired but were filtered, with reasons
ledger/REPORT.md             per-category CLV verdict (regenerated each run)
research/signals.csv         every candidate + 1h/6h/24h forward prices
docs/PRIOR_ART.md            survey of similar tools + feature roadmap
```

## Known limitations (by design, documented up front)

- **Hourly cadence is the floor on speed.** Anything where informed money is
  faster than ~1h (in-game sports, breaking crypto news) should grade NOT
  FOLLOWABLE — that's a finding, not a bug.
- **Polymarket depth is a proxy** (Gamma book liquidity, not touch size).
  Kalshi depth is the real size at the inside quote.
- **Scheduled-news detection is a heuristic** (time-to-resolution window). A
  jump on a pre-announced poll release >12h before close can still fire.
- **Cross-platform matching is conservative** (token similarity + number
  veto); it will miss some twins rather than merge different markets.
- **Paper fills are optimistic**: entry at the displayed ask, no fees, no
  slippage beyond the spread. Real following would do somewhat worse — so a
  verdict that's only barely FOLLOWABLE should be treated as MARGINAL.
- **No live orders, ever.** If the verdict ever justifies real money, that's
  a separate, deliberate step with its own risk controls.
