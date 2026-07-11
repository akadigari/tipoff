#!/usr/bin/env python3
"""
Tipoff — informed-money scanner for Kalshi + Polymarket.

Single-shot script: one invocation = one scan cycle (designed for an hourly
GitHub Actions cron). It never places orders. It:

  1. Pulls open markets from Kalshi (trade-api/v2) and Polymarket (Gamma +
     on-chain data-api).
  2. Compares each market against its own rolling baseline (EWMA of hourly
     volume rate + recent price moves, persisted in state/baselines.json).
  3. Flags informed-money signals:
        - volume spike vs the market's own baseline
        - sudden price jump (with a scheduled-news proxy: ignore jumps close
          to resolution, when moves are usually just the event happening)
        - (Polymarket, on-chain) unusually large trade
        - (Polymarket, on-chain) fresh wallet loading up
  4. Runs a FOLLOWABILITY GATE: price not already fully moved, enough depth
     to fill a small size, spread tight enough, and a slow-enough-resolving
     market that a lag window matters. Gate fail -> logged as WATCH, no alert.
  5. Scores signals; strong + followable -> Telegram alert + paper-ledger
     entry. The ledger is graded on resolution (win/loss, ROI, and
     closing-line value) per category, so the data answers: "is any niche
     actually followable, or am I always late?"

Honest framing: this is a paper-testing research tool. It detects/follows
informed money in public market data; it does not place trades and it does
not involve trading on non-public information.

Secrets: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID come from the environment
(GitHub Actions secrets, or a local .env which is gitignored). Nothing is
ever hard-coded here.
"""

from __future__ import annotations

import csv
import json
import math
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Configuration (every threshold is pre-registered here, env-overridable)
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent
STATE_FILE = ROOT / "state" / "baselines.json"
LEDGER_FILE = ROOT / "ledger" / "ledger.csv"
WATCH_FILE = ROOT / "ledger" / "watch_log.csv"
REPORT_FILE = ROOT / "ledger" / "REPORT.md"

KALSHI_BASE = "https://api.elections.kalshi.com/trade-api/v2"
GAMMA_BASE = "https://gamma-api.polymarket.com"
DATA_API_BASE = "https://data-api.polymarket.com"


def _env_num(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, default))
    except ValueError:
        return default


CFG = {
    # --- universe filters (what gets baseline-tracked) ---
    "KALSHI_MIN_VOL24": _env_num("TIPOFF_KALSHI_MIN_VOL24", 1000),   # contracts/24h
    "POLY_MIN_VOL24": _env_num("TIPOFF_POLY_MIN_VOL24", 1000),       # USD/24h
    "MAX_TRACKED_PER_PLATFORM": int(_env_num("TIPOFF_MAX_TRACKED", 1200)),
    "KALSHI_MAX_PAGES": int(_env_num("TIPOFF_KALSHI_PAGES", 25)),
    "POLY_PAGES": int(_env_num("TIPOFF_POLY_PAGES", 8)),  # x100 markets (Gamma
                                                          # caps limit at 100)

    # --- baseline (EWMA) ---
    "EWMA_ALPHA": 0.15,          # weight of the newest observation
    "MIN_OBS": 8,                # observations before spike detection is live
    "MAX_MOVE_WINDOW": 12,       # recent |price moves| kept for jump baseline
    "MAX_GAP_HOURS": 6.0,        # snapshot gap beyond which signals are skipped
    "STALE_PRUNE_HOURS": 72.0,   # drop markets not seen for this long

    # --- signal thresholds ---
    "VOL_SPIKE_Z": 3.0,          # hourly volume rate z-score to fire
    "VOL_SPIKE_MIN_ABS": 500.0,  # min volume delta (contracts/USD) to fire
    "PRICE_JUMP_MIN": 0.08,      # min |move| since last snapshot (8 cents)
    "PRICE_JUMP_MED_MULT": 3.0,  # and >= this multiple of median recent move
    "PRICE_JUMP_MAX_AGE_H": 3.0, # jump must be measured over <= this window
    "SCHEDULED_NEWS_MIN_H": 12.0,# jump within this many hours of close is
                                 # presumed scheduled-news / event-driven
    "LARGE_TRADE_USD": 5000.0,   # single on-chain trade notional to flag
    "FRESH_WALLET_TRADE_USD": 2000.0,  # min trade size to bother profiling
    "FRESH_WALLET_MAX_AGE_D": 7.0,     # wallet first seen within N days
    "FRESH_WALLET_ACTIVITY_LIMIT": 50, # rows fetched; fewer => whole history

    # --- API budget per run ---
    "MAX_TRADE_FETCHES": 40,
    "MAX_WALLET_LOOKUPS": 10,

    # --- followability gate ---
    "GATE_MAX_PRICE": 0.85,      # entry above this = move already happened
    "GATE_MIN_PRICE": 0.05,      # below this = longshot noise, not a lag play
    "GATE_MAX_SPREAD": 0.05,     # wider than 5c = can't fill near the signal
    "GATE_MIN_DEPTH_USD": 500.0, # visible size at the touch (Kalshi)
    "GATE_MIN_LIQUIDITY_USD": 2000.0,  # book liquidity proxy (Polymarket)
    "GATE_MIN_HOURS_TO_CLOSE": 6.0,    # resolves sooner = no lag window
    "GATE_MAX_DAYS_TO_CLOSE": 90.0,    # resolves later = capital dead too long

    # --- alerting ---
    "ALERT_SCORE": 60,           # min combined score to alert
    "REALERT_COOLDOWN_H": 48.0,  # per-market cooldown between alerts
    "MAX_ALERTS_PER_RUN": 5,     # excess goes to the watch log
    "PAPER_STAKE_BASE": 25.0,    # suggested paper size ($)

    # --- misc ---
    "HTTP_TIMEOUT": 20,
    "WATCH_LOG_MAX_ROWS": 5000,
}

CATEGORIES = ("entertainment", "politics", "sports", "crypto", "other")

LEDGER_COLUMNS = [
    "id", "ts", "platform", "market_id", "title", "category", "side",
    "entry_price", "stake_usd", "score", "signals", "hours_to_close",
    "status", "last_price", "resolved_ts", "result", "roi", "clv",
]

WATCH_COLUMNS = [
    "ts", "platform", "market_id", "title", "category", "score",
    "signals", "reasons",
]

# ---------------------------------------------------------------------------
# Small utilities
# ---------------------------------------------------------------------------


def now_ts() -> float:
    return time.time()


def iso_utc(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(s: str) -> float | None:
    """ISO-8601 (with or without trailing Z) -> unix timestamp, or None."""
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def safe_float(v, default: float = 0.0) -> float:
    """Both APIs return numbers as strings ('0.0030', '39637817.99')."""
    try:
        f = float(v)
        return f if math.isfinite(f) else default
    except (TypeError, ValueError):
        return default


def load_dotenv(path: Path) -> None:
    """Tiny .env loader for local runs (KEY=VALUE lines). Never committed."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip().strip("'\""))


_session = requests.Session()
_session.headers["User-Agent"] = "tipoff-scanner/1.0 (paper research; no orders)"


def http_get_json(url: str, params: dict | None = None, retries: int = 2):
    """GET with retry. Kalshi payloads can contain raw control characters,
    so parse leniently (strict=False) instead of resp.json()."""
    last_err = None
    for attempt in range(retries + 1):
        try:
            resp = _session.get(url, params=params, timeout=CFG["HTTP_TIMEOUT"])
            if resp.status_code == 429:
                time.sleep(2.0 * (attempt + 1))
                continue
            resp.raise_for_status()
            return json.loads(resp.text, strict=False)
        except (requests.RequestException, json.JSONDecodeError) as err:
            last_err = err
            time.sleep(1.0 * (attempt + 1))
    print(f"  [warn] GET {url} failed after retries: {last_err}")
    return None

# ---------------------------------------------------------------------------
# Market fetch + normalization
# ---------------------------------------------------------------------------
# Normalized market dict:
#   platform, id, title, category, close_ts,
#   price        - current YES probability (mid where possible)
#   yes_ask/no_ask - what a taker pays to enter each side
#   spread, vol (cumulative), vol24,
#   depth_yes_usd / depth_no_usd  - visible size at the touch (Kalshi) or
#                                   book-liquidity proxy (Polymarket)
#   url          - human link for the alert (may be "")


KALSHI_CATEGORY_MAP = {
    "sports": "sports",
    "politics": "politics",
    "elections": "politics",
    "world": "politics",
    "entertainment": "entertainment",
    "social": "entertainment",
}

CRYPTO_RE = re.compile(
    r"\b(bitcoin|btc|ethereum|eth\b|solana|sol\b|xrp|dogecoin|doge|crypto"
    r"|stablecoin|binance|coinbase|memecoin|altcoin|blockchain|nft)\b", re.I)
SPORTS_RE = re.compile(
    r"\b(nfl|nba|mlb|nhl|ncaa|uefa|fifa|premier league|la liga|serie a"
    r"|grand slam|wimbledon|us open|super bowl|world series|stanley cup"
    r"|f1|formula 1|ufc|boxing|golf|pga|olympic|world cup|touchdown"
    r"|game \d|vs\.?\s|match|playoff|championship)\b", re.I)
ENTERTAINMENT_RE = re.compile(
    r"\b(oscars?|academy award|grammy|emmy|golden globe|box office|movie"
    r"|film|album|billboard|spotify|netflix|tv show|season finale|bachelor"
    r"|survivor|taylor swift|beyonc|kardashian|celebrity|rotten tomatoes)\b", re.I)
POLITICS_RE = re.compile(
    r"\b(election|president|senate|congress|governor|parliament|prime minister"
    r"|nominee|impeach|cabinet|supreme court|tariff|executive order|veto"
    r"|legislation|mayor|referendum|coalition|geopolit|ceasefire|treaty)\b", re.I)


def categorize(title: str, platform_category: str = "") -> str:
    """Tag a market entertainment/politics/sports/crypto/other.

    Crypto keywords win first because platforms file crypto price markets
    under 'Financials'/'Economics'; then trust the platform category; then
    fall back to keywords.
    """
    text = title or ""
    if CRYPTO_RE.search(text):
        return "crypto"
    mapped = KALSHI_CATEGORY_MAP.get((platform_category or "").strip().lower())
    if mapped:
        return mapped
    if SPORTS_RE.search(text):
        return "sports"
    if ENTERTAINMENT_RE.search(text):
        return "entertainment"
    if POLITICS_RE.search(text):
        return "politics"
    return "other"


def fetch_kalshi_markets() -> list[dict]:
    """Open Kalshi markets via /events?with_nested_markets=true.

    The raw /markets endpoint is dominated by thousands of auto-generated
    multivariate parlays (KXMVE...); the events endpoint skips them and
    carries the category we need.
    """
    out: list[dict] = []
    cursor = ""
    for _ in range(CFG["KALSHI_MAX_PAGES"]):
        params = {"status": "open", "limit": 200, "with_nested_markets": "true"}
        if cursor:
            params["cursor"] = cursor
        data = http_get_json(f"{KALSHI_BASE}/events", params)
        if not data:
            break
        events = data.get("events", [])
        for ev in events:
            markets = ev.get("markets") or []
            for m in markets:
                if m.get("status") != "active" or m.get("market_type") != "binary":
                    continue
                if m.get("mve_collection_ticker"):
                    continue
                yes_bid = safe_float(m.get("yes_bid_dollars"))
                yes_ask = safe_float(m.get("yes_ask_dollars"))
                no_ask = safe_float(m.get("no_ask_dollars"), 1.0 - yes_bid)
                price = (yes_bid + yes_ask) / 2 if yes_ask > 0 else safe_float(
                    m.get("last_price_dollars"))
                title = ev.get("title") or m.get("title") or m["ticker"]
                sub = (m.get("yes_sub_title") or "").strip()
                if len(markets) > 1 and sub and sub.lower() not in title.lower():
                    title = f"{title} — {sub}"
                out.append({
                    "platform": "kalshi",
                    "id": m["ticker"],
                    "title": title,
                    "category": categorize(title, ev.get("category", "")),
                    "close_ts": parse_iso(m.get("close_time", "")),
                    "price": price,
                    "yes_ask": yes_ask,
                    "no_ask": no_ask,
                    "spread": max(0.0, yes_ask - yes_bid) if yes_ask > 0 else 1.0,
                    "vol": safe_float(m.get("volume_fp")),
                    "vol24": safe_float(m.get("volume_24h_fp")),
                    # buying YES lifts the yes ask; buying NO crosses the yes bid
                    "depth_yes_usd": safe_float(m.get("yes_ask_size_fp")) * yes_ask,
                    "depth_no_usd": safe_float(m.get("yes_bid_size_fp")) * no_ask,
                    "url": "",
                })
        cursor = data.get("cursor") or ""
        if not cursor or not events:
            break
    return out


def fetch_polymarket_markets() -> list[dict]:
    """Top Polymarket binary markets by 24h volume via the Gamma API.
    Gamma silently caps limit at 100, so page in steps of 100."""
    out: list[dict] = []
    for page in range(CFG["POLY_PAGES"]):
        data = http_get_json(f"{GAMMA_BASE}/markets", {
            "active": "true", "closed": "false", "limit": 100,
            "offset": page * 100, "order": "volume24hr", "ascending": "false",
        })
        if not data:
            break
        for m in data:
            try:
                outcomes = json.loads(m.get("outcomes") or "[]")
                prices = [safe_float(p) for p in
                          json.loads(m.get("outcomePrices") or "[]")]
            except json.JSONDecodeError:
                continue
            if outcomes != ["Yes", "No"] or len(prices) != 2:
                continue  # keep semantics simple: binary Yes/No legs only
            if not (m.get("enableOrderBook") and m.get("acceptingOrders")):
                continue
            best_bid = safe_float(m.get("bestBid"))
            best_ask = safe_float(m.get("bestAsk"))
            price = (best_bid + best_ask) / 2 if best_ask > 0 else prices[0]
            liquidity = safe_float(m.get("liquidityNum"))
            ev = (m.get("events") or [{}])[0]
            title = m.get("question") or m.get("slug") or m["conditionId"]
            slug = ev.get("slug") or m.get("slug") or ""
            out.append({
                "platform": "poly",
                "id": m["conditionId"],
                "title": title,
                "category": categorize(f'{title} {ev.get("title", "")}'),
                "close_ts": parse_iso(m.get("endDate") or ""),
                "price": price,
                "yes_ask": best_ask if best_ask > 0 else prices[0],
                "no_ask": (1.0 - best_bid) if best_bid > 0 else prices[1],
                "spread": max(0.0, best_ask - best_bid) if best_ask > 0 else 1.0,
                "vol": safe_float(m.get("volumeNum")),
                "vol24": safe_float(m.get("volume24hr")),
                # Gamma exposes total book liquidity, not touch size; the gate
                # applies GATE_MIN_LIQUIDITY_USD to this proxy instead.
                "depth_yes_usd": liquidity,
                "depth_no_usd": liquidity,
                "url": f"https://polymarket.com/event/{slug}" if slug else "",
            })
    return out


def select_universe(markets: list[dict], min_vol24: float) -> list[dict]:
    """Keep active-enough markets, capped per platform by 24h volume."""
    live = [m for m in markets
            if m["vol24"] >= min_vol24 and m["close_ts"]
            and 0.005 < m["price"] < 0.995]
    live.sort(key=lambda m: m["vol24"], reverse=True)
    return live[: CFG["MAX_TRACKED_PER_PLATFORM"]]

# ---------------------------------------------------------------------------
# Baseline state (online EWMA — compact enough to commit every hour)
# ---------------------------------------------------------------------------
# state["markets"][key] = {
#   "ts":  last snapshot unix ts        "v":  last cumulative volume
#   "p":   last YES price               "n":  observations so far
#   "m":   EWMA of hourly volume rate   "s2": EWMA variance of that rate
#   "mv":  recent |price moves| (<= MAX_MOVE_WINDOW)
#   "la":  last alert ts (cooldown)     "c":  category
# }


def market_key(m: dict) -> str:
    return f'{m["platform"]}:{m["id"]}'


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except json.JSONDecodeError:
            print("  [warn] corrupt state file, starting fresh")
    return {"markets": {}, "meta": {}}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    # One market per line -> git stores hourly updates as small line diffs.
    entries = state["markets"]
    lines = ['{"meta": ' + json.dumps(state.get("meta", {})) + ', "markets": {']
    for i, key in enumerate(sorted(entries)):
        comma = "," if i < len(entries) - 1 else ""
        lines.append(f'{json.dumps(key)}: {json.dumps(entries[key])}{comma}')
    lines.append("}}")
    STATE_FILE.write_text("\n".join(lines))


def observe_market(entry: dict | None, m: dict, ts: float) -> tuple[dict, dict]:
    """Fold the new snapshot into the baseline.

    Returns (updated_entry, obs) where obs holds the pre-update measurements
    the detectors need: dt_hours, vol_rate (per hour), price_move, plus the
    baseline stats as they stood BEFORE this observation.
    """
    if entry is None:
        entry = {"ts": ts, "v": m["vol"], "p": round(m["price"], 4), "n": 0,
                 "m": 0.0, "s2": 0.0, "mv": [], "la": 0, "c": m["category"]}
        return entry, {"dt_h": None}

    dt_h = (ts - entry["ts"]) / 3600.0
    if dt_h <= 0.01:
        return entry, {"dt_h": None}

    dv = max(0.0, m["vol"] - entry["v"])  # cumulative volume never decreases
    rate = dv / dt_h
    dp = m["price"] - entry["p"]
    obs = {
        "dt_h": dt_h, "rate": rate, "dp": dp,
        "base_mean": entry["m"], "base_var": entry["s2"], "n": entry["n"],
        "recent_moves": list(entry["mv"]),
    }

    alpha = CFG["EWMA_ALPHA"]
    if entry["n"] == 0:
        entry["m"], entry["s2"] = rate, 0.0
    else:
        delta = rate - entry["m"]
        entry["m"] += alpha * delta
        entry["s2"] = (1 - alpha) * (entry["s2"] + alpha * delta * delta)
    entry["n"] += 1
    entry["mv"] = (entry["mv"] + [round(abs(dp), 4)])[-CFG["MAX_MOVE_WINDOW"]:]
    entry["ts"], entry["v"], entry["p"] = ts, m["vol"], round(m["price"], 4)
    entry["c"] = m["category"]
    return entry, obs


def prune_state(state: dict, ts: float) -> int:
    stale = [k for k, e in state["markets"].items()
             if ts - e.get("ts", 0) > CFG["STALE_PRUNE_HOURS"] * 3600]
    for k in stale:
        del state["markets"][k]
    return len(stale)

# ---------------------------------------------------------------------------
# Signal detection (pure functions — unit-tested)
# ---------------------------------------------------------------------------


def detect_volume_spike(obs: dict, cfg: dict = CFG) -> dict | None:
    """Hourly volume rate vs the market's own EWMA baseline (z-score)."""
    if obs.get("dt_h") is None or obs["dt_h"] > cfg["MAX_GAP_HOURS"]:
        return None
    if obs["n"] < cfg["MIN_OBS"]:
        return None  # warm-up: not enough history to call anything a spike
    rate, mean, var = obs["rate"], obs["base_mean"], obs["base_var"]
    if rate * obs["dt_h"] < cfg["VOL_SPIKE_MIN_ABS"]:
        return None  # tiny absolute delta; z-scores on dust are noise
    std = math.sqrt(var) if var > 0 else max(1.0, mean * 0.5)
    z = (rate - mean) / std if std > 0 else 0.0
    if z < cfg["VOL_SPIKE_Z"]:
        return None
    mult = rate / mean if mean > 0 else float("inf")
    mult_txt = f"{mult:.0f}x" if math.isfinite(mult) else "new"
    return {
        "type": "volume_spike",
        "desc": f"volume spike ({mult_txt} baseline, z={z:.1f})",
        "points": min(40, round(10 + 5 * min(z, 8.0))),
    }


def detect_price_jump(obs: dict, hours_to_close: float,
                      cfg: dict = CFG) -> dict | None:
    """Sudden price move vs the market's own recent-move baseline.

    Scheduled-news proxy: a jump within SCHEDULED_NEWS_MIN_H of resolution is
    presumed to be the event itself happening (game ending, announcement
    landing) rather than informed money arriving early, so it does not fire.
    """
    if obs.get("dt_h") is None or obs["dt_h"] > cfg["PRICE_JUMP_MAX_AGE_H"]:
        return None
    if hours_to_close < cfg["SCHEDULED_NEWS_MIN_H"]:
        return None
    dp = obs["dp"]
    if abs(dp) < cfg["PRICE_JUMP_MIN"]:
        return None
    moves = sorted(obs.get("recent_moves", []))
    if len(moves) >= 4:
        median = moves[len(moves) // 2]
        if median > 0 and abs(dp) < cfg["PRICE_JUMP_MED_MULT"] * median:
            return None  # normal chop for this market, not a jump
    return {
        "type": "price_jump",
        "desc": f"price jump {dp * 100:+.0f}c in {obs['dt_h']:.1f}h",
        "points": min(35, round(250 * abs(dp))),
        "direction": 1 if dp > 0 else -1,
    }


def detect_large_trades(trades: list[dict], since_ts: float,
                        cfg: dict = CFG) -> dict | None:
    """Largest single on-chain trade since the last snapshot (Polymarket).

    `trades` are data-api rows: side BUY/SELL, outcomeIndex 0=Yes 1=No,
    size (shares), price (USDC). Direction is toward YES if someone bought
    Yes or dumped No.
    """
    best = None
    for t in trades:
        if safe_float(t.get("timestamp")) <= since_ts:
            continue
        notional = safe_float(t.get("size")) * safe_float(t.get("price"))
        if notional < cfg["LARGE_TRADE_USD"]:
            continue
        if best is None or notional > best[0]:
            best = (notional, t)
    if best is None:
        return None
    notional, t = best
    buys_yes = (t.get("side") == "BUY") == (t.get("outcomeIndex") == 0)
    return {
        "type": "large_trade",
        "desc": f"${notional:,.0f} single trade "
                f"({'into' if buys_yes else 'against'} YES)",
        "points": min(30, round(10 + notional / 1000)),
        "direction": 1 if buys_yes else -1,
        "wallet": t.get("proxyWallet", ""),
        "notional": notional,
    }


def is_fresh_wallet(activity_rows: list[dict], fetch_limit: int,
                    ts: float, cfg: dict = CFG) -> bool:
    """A wallet is 'fresh' when we can see its ENTIRE history (fewer rows than
    the fetch limit came back) and the earliest row is recent."""
    if not activity_rows or len(activity_rows) >= fetch_limit:
        return False  # long history (or unknown) -> not fresh
    earliest = min(safe_float(r.get("timestamp"), ts) for r in activity_rows)
    return (ts - earliest) <= cfg["FRESH_WALLET_MAX_AGE_D"] * 86400


FRESH_WALLET_SIGNAL = {
    "type": "fresh_wallet",
    "desc": "fresh wallet loading up",
    "points": 20,
}

# ---------------------------------------------------------------------------
# Scoring, direction, followability gate (pure functions — unit-tested)
# ---------------------------------------------------------------------------


def score_signals(signals: list[dict]) -> int:
    return min(100, sum(s["points"] for s in signals))


def choose_side(signals: list[dict], price_drift: float) -> str:
    """'yes' or 'no' — trust directional signals, fall back to price drift."""
    directional = [s["direction"] for s in signals if "direction" in s]
    if directional:
        return "yes" if sum(directional) >= 0 else "no"
    return "yes" if price_drift >= 0 else "no"


def followability_gate(entry_price: float, depth_usd: float, spread: float,
                       hours_to_close: float, cfg: dict = CFG,
                       min_depth: float | None = None) -> tuple[bool, list[str]]:
    """Can this signal still be followed at a fair price, in size, in time?

    Returns (passes, reasons_it_failed). Every check is a reason the follow
    would lose even if the signal itself is real:
      - price already moved past GATE_MAX_PRICE -> we're late, edge consumed
      - price below GATE_MIN_PRICE -> longshot churn, not an information lag
      - spread too wide / no depth -> fill price won't resemble signal price
      - resolves too soon -> no lag window, the event IS the resolution
      - resolves too far out -> capital locked, CLV meaningless for months
    """
    reasons = []
    if entry_price > cfg["GATE_MAX_PRICE"]:
        reasons.append(f"too late: entry {entry_price:.2f} > {cfg['GATE_MAX_PRICE']}")
    if entry_price < cfg["GATE_MIN_PRICE"]:
        reasons.append(f"longshot: entry {entry_price:.2f} < {cfg['GATE_MIN_PRICE']}")
    if spread > cfg["GATE_MAX_SPREAD"]:
        reasons.append(f"spread {spread * 100:.0f}c too wide")
    floor = cfg["GATE_MIN_DEPTH_USD"] if min_depth is None else min_depth
    if depth_usd < floor:
        reasons.append(f"thin: ${depth_usd:,.0f} depth < ${floor:,.0f}")
    if hours_to_close < cfg["GATE_MIN_HOURS_TO_CLOSE"]:
        reasons.append(f"resolves in {hours_to_close:.0f}h — no lag window")
    if hours_to_close > cfg["GATE_MAX_DAYS_TO_CLOSE"] * 24:
        reasons.append(f"resolves in {hours_to_close / 24:.0f}d — too slow")
    return (not reasons, reasons)


def suggested_stake(score: int, depth_usd: float, cfg: dict = CFG) -> float:
    stake = cfg["PAPER_STAKE_BASE"]
    if score >= 75:
        stake *= 2
    if score >= 90:
        stake *= 2
    stake = min(stake, depth_usd * 0.10)  # never suggest > 10% of visible size
    return max(10.0, 5 * round(stake / 5))

# ---------------------------------------------------------------------------
# Telegram (formatter is pure — unit-tested; sender does I/O)
# ---------------------------------------------------------------------------

ALERT_HEADER = "🚨🚨 ALERT!!! INSIDER TRADING SCOOP 🚨🚨"


def format_alert(alert: dict) -> str:
    """Phone-skimmable alert. `alert` needs: title, platform, market_id,
    signals (list of desc strings), side, entry_price, category, stake_usd,
    hours_to_close, score, url."""
    side = alert["side"].upper()
    price_c = alert["entry_price"] * 100
    window = alert["hours_to_close"]
    window_txt = (f"{window:.0f}h" if window < 72 else f"{window / 24:.0f}d")
    lines = [
        ALERT_HEADER,
        "",
        f"📍 {alert['title']}",
        f"   [{alert['platform']} · {alert['market_id']}]",
        f"🔔 Signal: {' + '.join(alert['signals'])}",
        f"💵 Price: {price_c:.0f}c — buy {side}",
        f"🏷 Category: {alert['category']}",
        f"📐 Suggested size: ${alert['stake_usd']:.0f} (paper)",
        f"⚡ Score {alert['score']}/100 · resolves in {window_txt}",
        "⏳ Window open — verify + move.",
    ]
    if alert.get("url"):
        lines.append(f"🔗 {alert['url']}")
    return "\n".join(lines)


def send_telegram(text: str) -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if os.environ.get("TIPOFF_DRY_RUN") or not token or not chat_id:
        print("  [dry-run] telegram message suppressed:")
        print("  " + text.replace("\n", "\n  "))
        return False
    try:
        resp = _session.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text,
                  "disable_web_page_preview": True},
            timeout=CFG["HTTP_TIMEOUT"])
        ok = resp.status_code == 200 and resp.json().get("ok")
        if not ok:
            print(f"  [warn] telegram send failed: {resp.text[:200]}")
        return bool(ok)
    except requests.RequestException as err:
        print(f"  [warn] telegram send error: {err}")
        return False

# ---------------------------------------------------------------------------
# Paper ledger + CLV grading
# ---------------------------------------------------------------------------


def read_ledger() -> list[dict]:
    if not LEDGER_FILE.exists():
        return []
    with LEDGER_FILE.open(newline="") as fh:
        return list(csv.DictReader(fh))


def write_ledger(rows: list[dict]) -> None:
    LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER_FILE.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=LEDGER_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def grade_row(row: dict, result: str, ts: float) -> None:
    """Grade a resolved position in place.

    ROI is per-dollar-staked at entry. CLV (closing-line value) is the final
    observed market price for our side minus our entry price: positive means
    the line kept moving our way after the alert (the signal led the market —
    followable even when the outcome loses); negative means we were the exit
    liquidity.
    """
    entry = safe_float(row["entry_price"])
    row["resolved_ts"] = iso_utc(ts)
    row["result"] = result
    if result == "void":
        row["status"], row["roi"], row["clv"] = "void", "0.0", "0.0"
        return
    won = (result == row["side"])
    row["status"] = "won" if won else "lost"
    row["roi"] = f"{((1.0 - entry) / entry) if won else -1.0:.4f}"
    last = safe_float(row.get("last_price"), entry)
    row["clv"] = f"{last - entry:.4f}"


def compute_report(rows: list[dict]) -> dict:
    """Per-category (and overall) stats + a pre-registered verdict."""
    def bucket():
        return {"alerts": 0, "open": 0, "graded": 0, "wins": 0,
                "roi_sum": 0.0, "clv_sum": 0.0}

    stats = {c: bucket() for c in CATEGORIES}
    stats["ALL"] = bucket()
    for row in rows:
        cat = row["category"] if row["category"] in stats else "other"
        for b in (stats[cat], stats["ALL"]):
            b["alerts"] += 1
            if row["status"] == "open":
                b["open"] += 1
            elif row["status"] in ("won", "lost"):
                b["graded"] += 1
                b["wins"] += row["status"] == "won"
                b["roi_sum"] += safe_float(row["roi"])
                b["clv_sum"] += safe_float(row["clv"])
    for b in stats.values():
        n = b["graded"]
        b["win_rate"] = b["wins"] / n if n else 0.0
        b["avg_roi"] = b["roi_sum"] / n if n else 0.0
        b["avg_clv"] = b["clv_sum"] / n if n else 0.0
        b["verdict"] = verdict(n, b["avg_clv"], b["avg_roi"])
    return stats


def verdict(n_graded: int, avg_clv: float, avg_roi: float) -> str:
    """Pre-registered read of a category. CLV is primary: it converges much
    faster than ROI and measures the only thing that matters for a follower —
    does the price keep moving our way after we alert, or are we late?"""
    if n_graded < 20:
        return "INSUFFICIENT DATA"
    if avg_clv > 0.02 and avg_roi > 0:
        return "FOLLOWABLE"
    if avg_clv > 0:
        return "MARGINAL — edge exists but thin"
    return "NOT FOLLOWABLE — following is late money"


def write_report(rows: list[dict], ts: float) -> None:
    stats = compute_report(rows)
    lines = [
        "# Tipoff — paper-trading report",
        "",
        f"_Auto-generated {iso_utc(ts)}. {len(rows)} alerts ledgered._",
        "",
        "CLV = final observed price for our side minus entry price, in probability",
        "points. Positive CLV means the market kept moving our way after the alert.",
        "A category is only called FOLLOWABLE with >= 20 graded alerts, avg CLV",
        "> +0.02 and positive avg ROI. See README for how to read this.",
        "",
        "| Category | Alerts | Open | Graded | Win% | Avg ROI | Avg CLV | Verdict |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for cat in list(CATEGORIES) + ["ALL"]:
        b = stats[cat]
        lines.append(
            f"| {cat} | {b['alerts']} | {b['open']} | {b['graded']} "
            f"| {b['win_rate'] * 100:.0f}% | {b['avg_roi'] * 100:+.1f}% "
            f"| {b['avg_clv'] * 100:+.1f}c | {b['verdict']} |")
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(lines) + "\n")


def append_watch_log(entries: list[dict]) -> None:
    if not entries:
        return
    WATCH_FILE.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    if WATCH_FILE.exists():
        with WATCH_FILE.open(newline="") as fh:
            rows = list(csv.DictReader(fh))
    rows.extend(entries)
    rows = rows[-CFG["WATCH_LOG_MAX_ROWS"]:]
    with WATCH_FILE.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=WATCH_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

# ---------------------------------------------------------------------------
# Resolution pass — update open positions, grade what resolved
# ---------------------------------------------------------------------------


def side_price(side: str, yes_price: float) -> float:
    return yes_price if side == "yes" else 1.0 - yes_price


def resolve_open_positions(rows: list[dict], ts: float) -> int:
    """For every open ledger row: refresh last_price (the running closing
    line) and grade it if the market resolved. Returns count graded."""
    open_rows = [r for r in rows if r["status"] == "open"]
    if not open_rows:
        return 0
    graded = 0

    kalshi_rows = [r for r in open_rows if r["platform"] == "kalshi"]
    for i in range(0, len(kalshi_rows), 40):
        chunk = kalshi_rows[i:i + 40]
        data = http_get_json(f"{KALSHI_BASE}/markets", {
            "tickers": ",".join(r["market_id"] for r in chunk)})
        markets = {m["ticker"]: m for m in (data or {}).get("markets", [])}
        for row in chunk:
            m = markets.get(row["market_id"])
            if not m:
                continue
            yes = safe_float(m.get("last_price_dollars"))
            if 0 < yes < 1:
                row["last_price"] = f"{side_price(row['side'], yes):.4f}"
            result = (m.get("result") or "").lower()
            status = (m.get("status") or "").lower()
            if result in ("yes", "no"):
                grade_row(row, result, ts)
                graded += 1
            elif status in ("finalized", "settled"):
                grade_row(row, "void", ts)
                graded += 1

    poly_rows = [r for r in open_rows if r["platform"] == "poly"]
    for i in range(0, len(poly_rows), 20):
        chunk = poly_rows[i:i + 20]
        data = http_get_json(f"{GAMMA_BASE}/markets", [
            ("condition_ids", r["market_id"]) for r in chunk])
        markets = {m.get("conditionId"): m for m in (data or [])}
        for row in chunk:
            m = markets.get(row["market_id"])
            if not m:
                continue
            try:
                prices = [safe_float(p) for p in
                          json.loads(m.get("outcomePrices") or "[]")]
            except json.JSONDecodeError:
                prices = []
            if len(prices) == 2 and 0 < prices[0] < 1:
                row["last_price"] = f"{side_price(row['side'], prices[0]):.4f}"
            if m.get("closed") and m.get("umaResolutionStatus") == "resolved" \
                    and len(prices) == 2:
                if prices[0] >= 0.99:
                    grade_row(row, "yes", ts)
                elif prices[0] <= 0.01:
                    grade_row(row, "no", ts)
                else:
                    grade_row(row, "void", ts)  # non-binary settlement
                graded += 1
    return graded

# ---------------------------------------------------------------------------
# Main scan cycle
# ---------------------------------------------------------------------------


def scan_market(m: dict, entry: dict | None, ts: float,
                trade_budget: dict) -> tuple[dict, list[dict], dict]:
    """Update one market's baseline and return (entry, signals, obs)."""
    entry, obs = observe_market(entry, m, ts)
    signals = []
    hours_to_close = ((m["close_ts"] or ts) - ts) / 3600.0

    spike = detect_volume_spike(obs)
    if spike:
        signals.append(spike)
    jump = detect_price_jump(obs, hours_to_close)
    if jump:
        signals.append(jump)

    # On-chain corroboration (Polymarket only), budgeted per run: only spend
    # trade fetches on markets that already look anomalous.
    if signals and m["platform"] == "poly" \
            and trade_budget["trades"] < CFG["MAX_TRADE_FETCHES"]:
        trade_budget["trades"] += 1
        trades = http_get_json(f"{DATA_API_BASE}/trades", {
            "market": m["id"], "limit": 100}) or []
        since = entry["ts"] - (obs["dt_h"] or 1.0) * 3600 if obs.get("dt_h") else ts - 3600
        big = detect_large_trades(trades, since)
        if big:
            signals.append(big)
            if big["notional"] >= CFG["FRESH_WALLET_TRADE_USD"] \
                    and big.get("wallet") \
                    and trade_budget["wallets"] < CFG["MAX_WALLET_LOOKUPS"]:
                trade_budget["wallets"] += 1
                limit = CFG["FRESH_WALLET_ACTIVITY_LIMIT"]
                activity = http_get_json(f"{DATA_API_BASE}/activity", {
                    "user": big["wallet"], "limit": limit}) or []
                if is_fresh_wallet(activity, limit, ts):
                    signals.append(dict(FRESH_WALLET_SIGNAL))
    return entry, signals, obs


def main() -> int:
    load_dotenv(ROOT / ".env")
    ts = now_ts()
    print(f"tipoff scan @ {iso_utc(ts)}")

    state = load_state()
    ledger = read_ledger()

    # --- 1. grade yesterday's calls before making today's ---
    graded = resolve_open_positions(ledger, ts)
    if graded:
        print(f"  graded {graded} resolved position(s)")

    # --- 2. pull the market universe ---
    kalshi = select_universe(fetch_kalshi_markets(), CFG["KALSHI_MIN_VOL24"])
    poly = select_universe(fetch_polymarket_markets(), CFG["POLY_MIN_VOL24"])
    print(f"  tracking {len(kalshi)} kalshi + {len(poly)} polymarket markets")
    if not kalshi and not poly:
        print("  [warn] both platforms returned nothing; keeping state as-is")
        write_ledger(ledger)
        write_report(ledger, ts)
        return 0

    # --- 3. scan for signals ---
    trade_budget = {"trades": 0, "wallets": 0}
    alerts, watches = [], []
    alerted_ids = {r["market_id"] for r in ledger if r["status"] == "open"}

    for m in kalshi + poly:
        key = market_key(m)
        entry, signals, obs = scan_market(m, state["markets"].get(key), ts,
                                          trade_budget)
        state["markets"][key] = entry
        if not signals:
            continue

        score = score_signals(signals)
        side = choose_side(signals, obs.get("dp", 0.0))
        entry_price = m["yes_ask"] if side == "yes" else m["no_ask"]
        depth = m["depth_yes_usd"] if side == "yes" else m["depth_no_usd"]
        hours_to_close = ((m["close_ts"] or ts) - ts) / 3600.0
        min_depth = (CFG["GATE_MIN_LIQUIDITY_USD"] if m["platform"] == "poly"
                     else CFG["GATE_MIN_DEPTH_USD"])
        passes, reasons = followability_gate(
            entry_price, depth, m["spread"], hours_to_close,
            min_depth=min_depth)

        if score < CFG["ALERT_SCORE"]:
            passes, reasons = False, reasons + [f"score {score} < {CFG['ALERT_SCORE']}"]
        if m["id"] in alerted_ids:
            passes, reasons = False, reasons + ["already holding (open ledger row)"]
        cooldown = ts - safe_float(entry.get("la")) < CFG["REALERT_COOLDOWN_H"] * 3600
        if passes and cooldown:
            passes, reasons = False, ["re-alert cooldown"]

        record = {
            "ts": iso_utc(ts), "platform": m["platform"], "market_id": m["id"],
            "title": m["title"], "category": m["category"], "score": score,
            "signals": " + ".join(s["desc"] for s in signals),
        }
        if passes:
            alerts.append({**record, "side": side, "entry_price": entry_price,
                           "depth": depth, "hours_to_close": hours_to_close,
                           "url": m["url"], "state_key": key})
        else:
            watches.append({**record, "reasons": "; ".join(reasons)})
            print(f"  WATCH [{score:>3}] {m['title'][:60]} :: {record['signals']}"
                  f" :: {'; '.join(reasons)}")

    # --- 4. alert the strongest, ledger them ---
    alerts.sort(key=lambda a: a["score"], reverse=True)
    overflow = alerts[CFG["MAX_ALERTS_PER_RUN"]:]
    for a in overflow:
        watches.append({k: a[k] for k in WATCH_COLUMNS if k in a}
                       | {"reasons": "alert cap for this run"})
    alerts = alerts[: CFG["MAX_ALERTS_PER_RUN"]]

    next_id = 1 + max((int(r["id"]) for r in ledger if r["id"].isdigit()),
                      default=0)
    for a in alerts:
        stake = suggested_stake(a["score"], a["depth"])
        msg = format_alert({**a, "stake_usd": stake,
                            "signals": a["signals"].split(" + ")})
        sent = send_telegram(msg)
        print(f"  ALERT [{a['score']:>3}] {'sent' if sent else 'dry'} :: "
              f"{a['title'][:60]} ({a['side']} @ {a['entry_price']:.2f})")
        state["markets"][a["state_key"]]["la"] = ts
        ledger.append({
            "id": str(next_id), "ts": a["ts"], "platform": a["platform"],
            "market_id": a["market_id"], "title": a["title"],
            "category": a["category"], "side": a["side"],
            "entry_price": f"{a['entry_price']:.4f}",
            "stake_usd": f"{stake:.0f}", "score": str(a["score"]),
            "signals": a["signals"],
            "hours_to_close": f"{a['hours_to_close']:.1f}", "status": "open",
            "last_price": f"{a['entry_price']:.4f}", "resolved_ts": "",
            "result": "", "roi": "", "clv": "",
        })
        next_id += 1

    # --- 5. persist everything ---
    pruned = prune_state(state, ts)
    state["meta"] = {"last_run_ts": ts, "last_run": iso_utc(ts),
                     "tracked": len(state["markets"])}
    save_state(state)
    write_ledger(ledger)
    write_report(ledger, ts)
    append_watch_log(watches)
    print(f"  done: {len(alerts)} alert(s), {len(watches)} watch(es), "
          f"{graded} graded, {pruned} stale market(s) pruned, "
          f"{trade_budget['trades']} trade fetches")
    return 0


if __name__ == "__main__":
    sys.exit(main())
