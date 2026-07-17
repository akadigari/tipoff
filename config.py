"""Tipoff configuration: every knob in one place.

Change values here (or override any of them with an env var of the same name
prefixed TIPOFF_, e.g. TIPOFF_ALERT_SCORE=50). All thresholds are
pre-registered: tune them deliberately, ideally after reviewing a calibration
week of ledger/watch_log.csv, not after a bad beat.
"""

import os


def _num(name: str, default: float) -> float:
    try:
        return float(os.environ.get(f"TIPOFF_{name}", default))
    except ValueError:
        return default


CFG = {
    # ------------------------------------------------------------------
    # Universe: which markets get baseline-tracked at all
    # ------------------------------------------------------------------
    "KALSHI_MIN_VOL24": _num("KALSHI_MIN_VOL24", 1000),   # contracts / 24h
    "POLY_MIN_VOL24": _num("POLY_MIN_VOL24", 1000),       # USD / 24h
    "MAX_TRACKED_PER_PLATFORM": int(_num("MAX_TRACKED", 1200)),
    "KALSHI_MAX_PAGES": int(_num("KALSHI_PAGES", 25)),    # x200 events
    "POLY_PAGES": int(_num("POLY_PAGES", 8)),             # x100 markets (Gamma
                                                          # caps limit at 100)

    # ------------------------------------------------------------------
    # Baseline (online EWMA per market)
    # ------------------------------------------------------------------
    "EWMA_ALPHA": 0.15,           # weight of newest observation
    "MIN_OBS": 8,                 # warm-up observations before signals fire
    "MAX_MOVE_WINDOW": 12,        # recent |price moves| kept for jump baseline
    "MAX_GAP_HOURS": 6.5,         # snapshot gap beyond which signals skip
                                  # (6.5 so a 6h throttled cadence still works)
    "STALE_PRUNE_HOURS": 72.0,    # drop markets unseen for this long
    "BASELINE_WINSOR_MULT": 4.0,  # cap a spike at Nx baseline before folding
                                  # it into the EWMA, so one burst can't poison
                                  # the baseline and mask follow-through

    # ------------------------------------------------------------------
    # Signals (balanced middle-ground defaults)
    # ------------------------------------------------------------------
    # volume spike: this hour's rate vs the market's own baseline
    "VOL_SPIKE_MULT": 3.0,        # fire at >= 3x trailing baseline
    "VOL_SPIKE_MIN_USD": 500.0,   # ...and >= this DOLLAR delta (backtest:
                                  # a share floor is $2 on a penny market
                                  # and noise-fired 18x on the Nobel replay)

    # price jump: move since last snapshot
    "PRICE_JUMP_MIN": 0.05,       # >= 5 cents
    "PRICE_JUMP_MED_MULT": 3.0,   # and >= 3x this market's median recent move
    "PRICE_JUMP_MAX_AGE_H": 3.5,  # measured over a window <= 3.5h (the
                                  # dead-zone cadence gaps 3h; +0.5 absorbs
                                  # GitHub cron jitter)
    "JUMP_MIN_VOL_DELTA": 20.0,   # phantom guard: a "jump" with no volume
                                  # behind it is a re-quoted book, not news
    "SCHEDULED_NEWS_MIN_H": 12.0, # jump within 12h of close = presumed the
                                  # event itself happening, not early money
    "JUMP_EXTREME_DP": 0.15,      # ...UNLESS the repricing is extreme: a
    "JUMP_EXTREME_RATIO": 5.0,    # >=15c move or >=5x odds change is never
                                  # scheduled drift (Nobel leak: 3.7c->39c)

    # large on-chain trade (Polymarket)
    "LARGE_TRADE_USD": 2000.0,    # absolute path: single trade >= $2k
    "LARGE_TRADE_MED_MULT": 5.0,  # relative path: >= 5x market's median trade
    "LARGE_TRADE_MIN_USD": 500.0, # floor for the relative path (5x of dust
                                  # is still dust)

    # fresh wallet (Polymarket)
    "FRESH_WALLET_TRADE_USD": 1000.0,  # bet size worth profiling the wallet
    "FRESH_WALLET_MAX_AGE_D": 3.0,     # whole history younger than ~3 days
    "FRESH_WALLET_ACTIVITY_LIMIT": 50, # rows fetched; a full page = veteran

    # insider-context bonus: informed flow means more in thin markets
    "THIN_MARKET_VOL24": 10000.0, # 24h volume below this + on-chain signal
                                  # -> extra points (obscure market, big bet)

    # price impact per unit of volume (research-backed: insider trades move
    # prices ~7-12x more per dollar than skilled-trader flow, Mitts & Ofir)
    "IMPACT_MULT": 5.0,           # this hour's |move|/volume >= 5x baseline
    "IMPACT_MIN_MOVE": 0.03,      # and the move itself >= 3 cents

    # wallet behavior (Polymarket): same wallet flagged across scans, and
    # trades out of character for THAT wallet's own history
    "REPEAT_ACTOR_WINDOW_D": 14.0,   # repeat flag within this window
    "WALLET_MEMORY_PRUNE_D": 30.0,   # forget flagged wallets after this
    "WITHIN_TRADER_MULT": 5.0,       # trade >= 5x wallet's own median size
    "WITHIN_TRADER_MIN_ROWS": 5,     # need this much history to say so

    # coordination (Polymarket): N distinct wallets buying the SAME side
    # within a tight window: the documented insider signature (Iran Feb 27:
    # 8 wallets bought YES within 2 seconds). Invisible to per-wallet
    # thresholds. Conservative: single-episode evidence, so it corroborates,
    # never alerts alone; calibration measures its real base rate.
    "COORD_WINDOW_S": 3.0,           # "same time" window, seconds
    "COORD_MIN_WALLETS": 3,          # distinct wallets to call it coordinated
    "COORD_MIN_TRADE_USD": 500.0,    # ignore dust in the cluster

    # cross-platform confirmation: same story moving on both venues
    "CROSS_CONFIRM_POINTS": 10,
    "CROSS_CONFIRM_JACCARD": 0.5, # title-token similarity to call it a twin

    # crowd chatter (Polymarket): commenters accusing a market of insider
    # activity while its price/volume is anomalous
    "CHATTER_WINDOW_H": 48.0,     # comments this recent count
    "CHATTER_MIN_VOICES": 2,      # distinct commenters (spam bots repeat)

    # insiderability: every documented episode happened in a market that
    # resolves on a PRIVATE HUMAN DECISION (committee, government, board,
    # celebrity, the subject themselves); ZERO happened in play-determined
    # sports outcomes: games, tournament runs, top-scorer races. Decision
    # markets get a score bonus; play-determined markets aren't scanned.
    "INSIDERABLE_POINTS": 8,

    # news check (Google News RSS, keyless): an insider move is a move
    # WITHOUT public news to explain it. Strong alerts get a press sweep:
    # zero recent coverage marks the move unexplained; heavy coverage
    # labels it a likely public-news reaction.
    "MAX_NEWS_CHECKS": 8,         # per run, alerts+monitors only
    "NEWS_WINDOW_H": 24.0,        # articles this recent count
    "NEWS_EXPLAINED_MIN": 3,      # >= this many -> 'explained by news'

    # ------------------------------------------------------------------
    # API budget per run
    # ------------------------------------------------------------------
    "MAX_TRADE_FETCHES": 40,
    "MAX_WALLET_LOOKUPS": 10,
    "MAX_COMMENT_FETCHES": 15,

    # ------------------------------------------------------------------
    # Followability gate
    # ------------------------------------------------------------------
    "GATE_MAX_PRICE": 0.85,       # entry above this = move already happened
    "GATE_MIN_PRICE": 0.05,       # below this = longshot churn
    "GATE_MAX_SLIP": 0.03,        # entry must be within 3c of the signal
                                  # price (catchable), else fills won't
                                  # resemble what fired
    "GATE_MIN_DEPTH_USD": 500.0,  # size at the touch (Kalshi)
    "GATE_MIN_LIQUIDITY_USD": 2000.0,  # book-liquidity proxy (Polymarket)
    "GATE_MIN_HOURS_TO_CLOSE": 24.0,   # resolves sooner = no lag window
    "GATE_MAX_DAYS_TO_CLOSE": 90.0,    # slower = dead capital

    # ------------------------------------------------------------------
    # Alerting
    # ------------------------------------------------------------------
    "ALERT_SCORE": 55,            # normal mode: min score to alert
    "REALERT_COOLDOWN_H": 48.0,   # per-market cooldown
    "MAX_ALERTS_PER_RUN": 5,
    "MONITOR_MAX_PER_RUN": 3,     # gate-failed-but-strong 👀 alerts per run
    "PAPER_STAKE_BASE": 25.0,     # suggested paper size ($)

    # ------------------------------------------------------------------
    # Calibration week: first N days after deployment run looser so the
    # watch log + ledger show what the net catches; those alerts are
    # tagged mode=calib and EXCLUDED from the pre-registered verdict.
    # ------------------------------------------------------------------
    "CALIB_DAYS": 7.0,
    "CALIB_ALERT_SCORE": 40,
    "CALIB_MAX_ALERTS_PER_RUN": 8,
    "CALIB_COOLDOWN_H": 24.0,

    # ------------------------------------------------------------------
    # Daily still-alive ping
    # ------------------------------------------------------------------
    "PING_UTC_HOUR": 13,          # aim for the run in this UTC hour (~9am ET)
    "PING_MIN_GAP_H": 20.0,       # don't ping twice in a day
    "PING_MAX_GAP_H": 26.0,       # fallback if the target-hour run was missed

    # ------------------------------------------------------------------
    # GitHub Actions minutes guard + self-throttling.
    # Usage is measured from this repo's own workflow runs (built-in token,
    # no extra secret). When the month projects over budget, Tipoff slows
    # itself down: with a WORKFLOW_EDIT_TOKEN secret it rewrites its own
    # cron (real savings); without one it skips scans in place (~half).
    # Throttle only tightens within a month; it resets on the 1st.
    # ------------------------------------------------------------------
    "ACTIONS_BUDGET_MIN": _num("ACTIONS_BUDGET_MIN", 1800),  # of the 2000
                                  # free private-repo minutes; headroom left
                                  # for your other repos
    "BUDGET_MIN_ELAPSED_DAYS": 2.0,   # damp wild projections on day 1
    "BUDGET_WARN_USED_PCT": 0.80,     # heads-up alert at 80% used
    "BUDGET_CRIT_USED_PCT": 0.95,     # hard-brake at 95% used -> every 6h
    "BUDGET_2H_PROJ_PCT": 0.95,       # projected >= 95% of budget -> every 2h
    "BUDGET_3H_PROJ_PCT": 1.30,       # projected >= 130% -> every 3h
    "BUDGET_6H_PROJ_PCT": 2.00,       # projected >= 200% -> every 6h

    # ------------------------------------------------------------------
    # Misc
    # ------------------------------------------------------------------
    "HTTP_TIMEOUT": 20,
    "WATCH_LOG_MAX_ROWS": 5000,
}
