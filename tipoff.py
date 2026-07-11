#!/usr/bin/env python3
"""
Tipoff — informed-money scanner for Kalshi + Polymarket.

Single-shot script: one invocation = one scan cycle (designed for an hourly
GitHub Actions cron). It never places orders. It:

  1. Pulls open markets from Kalshi (trade-api/v2) and Polymarket (Gamma +
     on-chain data-api).
  2. Compares each market against its own rolling baseline (winsorized EWMA
     of hourly volume rate + recent price moves, persisted in
     state/baselines.json).
  3. Flags informed-money signals:
        - volume spike vs the market's own baseline (>= ~3x)
        - sudden price jump (>= ~5c) backed by real volume, with a
          scheduled-news proxy (jumps near resolution don't count)
        - (Polymarket, on-chain) unusually large trade — absolute ($) or
          relative (x the market's own median trade size)
        - (Polymarket, on-chain) fresh wallet loading up
        - context bonuses: thin market + on-chain flow ("insider score"),
          and the same story moving on both platforms at once
  4. Runs a FOLLOWABILITY GATE: price still catchable (entry within ~3c of
     the signal), not already fully moved, enough depth for a small size,
     and resolution >24h out so a lag window exists. Gate fail -> WATCH log.
  5. Scores signals; strong + followable -> Telegram alert + paper-ledger
     entry, graded on resolution (win/loss, ROI, closing-line value) per
     category.

Operational extras:
  - CALIBRATION WEEK: the first CALIB_DAYS after deployment run with looser
    alert thresholds and everything logged; those alerts are tagged
    mode=calib and excluded from the pre-registered verdict.
  - DAILY PING: one short Telegram summary a day ("scanned N, X alerts,
    Y watches") so silence never means "maybe it's broken".

Honest framing: paper-testing research tool. It detects/follows informed
money in public market data; it does not place trades and it does not
involve trading on non-public information.

All thresholds live in config.py. Secrets (TELEGRAM_BOT_TOKEN,
TELEGRAM_CHAT_ID) come only from the environment / GitHub Actions secrets.
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

from config import CFG

# ---------------------------------------------------------------------------
# Paths + constants
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent
STATE_FILE = ROOT / "state" / "baselines.json"
LEDGER_FILE = ROOT / "ledger" / "ledger.csv"
WATCH_FILE = ROOT / "ledger" / "watch_log.csv"
REPORT_FILE = ROOT / "ledger" / "REPORT.md"
CALIB_REPORT_FILE = ROOT / "ledger" / "CALIBRATION.md"
RESEARCH_FILE = ROOT / "research" / "signals.csv"

KALSHI_BASE = "https://api.elections.kalshi.com/trade-api/v2"
GAMMA_BASE = "https://gamma-api.polymarket.com"
DATA_API_BASE = "https://data-api.polymarket.com"

CATEGORIES = ("entertainment", "politics", "sports", "crypto", "other")

LEDGER_COLUMNS = [
    "id", "ts", "platform", "market_id", "title", "category", "side",
    "entry_price", "stake_usd", "score", "signals", "triggers",
    "hours_to_close", "mode", "status", "last_price", "resolved_ts",
    "result", "roi", "clv",
    "read",  # informed-flow read on resolution: informed-like /
             # early-but-wrong / late-money / neutral
]

WATCH_COLUMNS = [
    "ts", "platform", "market_id", "title", "category", "score",
    "signals", "mode", "reasons",
]

# Research dataset: EVERY signal candidate (alerted or not) gets a row, and
# later runs fill in where the YES price actually went 1h/6h/24h after the
# signal. The point: after a few weeks this is a labeled dataset that can
# answer "which signals/categories/wallets actually predict moves" — the
# watch pile becomes training data instead of exhaust.
RESEARCH_COLUMNS = [
    "ts", "ts_unix", "platform", "market_id", "title", "category",
    "insiderable", "mode",
    "alerted",  # "0" not alerted, "1" follow alert, "M" monitor alert
    "score", "signals", "triggers", "side", "yes_price",
    "entry_price", "vol24", "depth", "hours_to_close", "gate_reasons",
    "wallet", "p_1h", "p_6h", "p_24h",
]
RESEARCH_HORIZONS = {"p_1h": 1.0, "p_6h": 6.0, "p_24h": 24.0}
RESEARCH_MAX_ROWS = 10000
RESEARCH_GRACE_H = 6.0  # market gone from the universe this long past a
                        # horizon -> mark "na" and stop looking

_RUN_STATS = {"http_errors": 0}  # per-run health counters (reset on start)

# ---------------------------------------------------------------------------
# Small utilities
# ---------------------------------------------------------------------------


def now_ts() -> float:
    return time.time()


def iso_utc(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def utc_hour(ts: float) -> int:
    return datetime.fromtimestamp(ts, tz=timezone.utc).hour


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


def http_get_json(url: str, params=None, retries: int = 2):
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
    _RUN_STATS["http_errors"] += 1
    print(f"  [warn] GET {url} failed after retries: {last_err}")
    return None

# ---------------------------------------------------------------------------
# Market fetch + normalization
# ---------------------------------------------------------------------------
# Normalized market dict:
#   platform, id, event (grouping key for dedup), title, category, close_ts,
#   price        - current YES probability (mid where possible)
#   yes_ask/no_ask - what a taker pays to enter each side
#   vol (cumulative), vol24,
#   depth_yes_usd / depth_no_usd - size at the touch (Kalshi) or
#                                  book-liquidity proxy (Polymarket)
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
    r"|game \d|vs\.?\s|match|playoff|championship"
    r"|esports|league of legends|valorant|dota|counter.?strike|cs2"
    r"|msi \d{4}|lcs\b|lck\b|overwatch)\b", re.I)
ENTERTAINMENT_RE = re.compile(
    r"\b(oscars?|academy award|grammy|emmy|golden globe|box office|movie"
    r"|film|album|billboard|spotify|netflix|tv show|season finale|bachelor"
    r"|survivor|taylor swift|beyonc|kardashian|celebrity|rotten tomatoes)\b", re.I)
POLITICS_RE = re.compile(
    r"\b(election|president|senate|congress|governor|parliament|prime minister"
    r"|nominee|impeach|cabinet|supreme court|tariff|executive order|veto"
    r"|legislation|mayor|referendum|coalition|geopolit|ceasefire|treaty"
    r"|military (?:action|operation)|air ?strikes?|missile|invasion|troops"
    r"|sanctions?|blockade|nuclear (?:deal|program)|strait of hormuz)\b", re.I)


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


# Insiderability: derived from the documented episode history (see
# docs/BACKTEST.md). Every verified insider case resolved on a private
# human decision; game outcomes structurally cannot leak.

GAME_OUTCOME_RE = re.compile(
    r"\bvs\.?\s|\bboth teams\b|\bto score\b|\bmoneyline\b|\bspread\b"
    r"|\bover/under\b|\bo/u\b|\btotal (?:points|goals|runs|sets)\b"
    r"|\b(?:1st|2nd|3rd|4th|first|second) (?:half|quarter|period|set|map)\b"
    r"|\bwin on \d{4}-\d{2}-\d{2}\b|\bwin (?:game|map|set|race) \d\b"
    r"|\bshots on goal\b|\bpoints scored\b|\bmargin of victory\b"
    r"|\breach the (?:final|semi|quarter)|\bmake the playoffs\b"
    r"|\btop (?:goal.?scorer|scorer)\b|\bgolden boot\b|\bqualif(?:y|ies)\b"
    r"|\btop \d+ finish|\bwin the .{0,30}(?:cup|championship|title"
    r"|tournament|open|series|derby|grand prix)\b", re.I)

DECISION_RE = re.compile(
    r"\b(?:announce|resign|step(?:s|ping)? down|fired?|out as|pardon"
    r"|nominat|appoint|confirm(?:ed|ation)|cabinet|laureate|prize|award"
    r"|winner of the|engag(?:ed|ement)|married|divorce|album|release date"
    r"|launch|unveil|ipo|acquisition|acquire|merger|indicted?|arrest"
    r"|charged|convict|verdict|sentenc|strike[sd]?\b|invade|invasion"
    r"|capture|custody|military (?:action|operation)|attend|appear at"
    r"|retire|suspend(?:ed|s|sion)?|trade[sd]? (?:to|for)|sign(?:s|ed)? with|drafted"
    r"|host(?:s|ed)? the|cancel(?:led|ed)|renewed?|meet(?:s|ing)? with"
    r"|visit|summit|ceasefire|treaty|executive order|veto)\b", re.I)


def insiderability(title: str, category: str) -> str:
    """'high' for private-decision markets (where every documented insider
    episode lived), 'none' for play-determined sports outcomes (games,
    tournament runs, scorer races — decided on the field, so no insider can
    exist; zero documented episodes there), else 'normal'. Sports DECISION
    markets — injuries, trades, retirements, suspensions — stay 'high':
    someone in the building always knows first."""
    text = title or ""
    if DECISION_RE.search(text):
        return "high"
    if category == "sports" or GAME_OUTCOME_RE.search(text):
        return "none"
    return "normal"


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
                    "event": ev.get("event_ticker", m["ticker"]),
                    "title": title,
                    "category": categorize(title, ev.get("category", "")),
                    "close_ts": parse_iso(m.get("close_time", "")),
                    "price": price,
                    "yes_ask": yes_ask,
                    "no_ask": no_ask,
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
            except (json.JSONDecodeError, TypeError):
                continue  # TypeError: outcomePrices came back as JSON null
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
                "event": slug or m["conditionId"],
                "event_id": str(ev.get("id") or ""),
                "title": title,
                "category": categorize(f'{title} {ev.get("title", "")}'),
                "close_ts": parse_iso(m.get("endDate") or ""),
                "price": price,
                "yes_ask": best_ask if best_ask > 0 else prices[0],
                "no_ask": (1.0 - best_bid) if best_bid > 0 else prices[1],
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
#   "m":   EWMA of hourly volume rate   "im": EWMA of |price move|/volume
#   "mv":  recent |price moves| (<= MAX_MOVE_WINDOW)
#   "la":  last alert ts (cooldown)     "lg": last grade (F=follow, M=monitor)
# }
# state["wallets"][addr] = {"ts": last flag, "d": direction, "n": flag count}
# state["meta"] holds first_run_ts (calibration clock), last_ping_ts and the
# rolling "day" counters for the daily ping.


def market_key(m: dict) -> str:
    return f'{m["platform"]}:{m["id"]}'


def hours_until_close(m: dict, ts: float) -> float | None:
    """None = clock unknown or stale. Platforms serve stale close dates (a
    gamma endDate was a month in the past on an ACTIVE market in the
    backtest); a broken clock must read as 'unknown', never as 'resolves
    now' — the gate treats unknown as pass-with-flag, not fail."""
    close_ts = m.get("close_ts")
    if not close_ts or close_ts <= ts:
        return None
    return (close_ts - ts) / 3600.0


RETIRED_MARKET_KEYS = ("s2", "c")  # dropped fields — strip from old state


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text())
            state.setdefault("markets", {})
            state.setdefault("meta", {})
            for entry in state["markets"].values():
                for key in RETIRED_MARKET_KEYS:
                    entry.pop(key, None)
            return state
        except json.JSONDecodeError:
            print("  [warn] corrupt state file, starting fresh")
    return {"markets": {}, "meta": {}}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    # One market per line -> git stores hourly updates as small line diffs.
    entries = state["markets"]
    lines = ['{"meta": ' + json.dumps(state.get("meta", {})) + ',',
             '"wallets": ' + json.dumps(state.get("wallets", {})) + ',',
             '"markets": {']
    for i, key in enumerate(sorted(entries)):
        comma = "," if i < len(entries) - 1 else ""
        lines.append(f'{json.dumps(key)}: {json.dumps(entries[key])}{comma}')
    lines.append("}}")
    STATE_FILE.write_text("\n".join(lines))


def observe_market(entry: dict | None, m: dict, ts: float,
                   cfg: dict = CFG) -> tuple[dict, dict]:
    """Fold the new snapshot into the baseline.

    Returns (updated_entry, obs) where obs holds the pre-update measurements
    the detectors need: dt_hours, vol_rate (per hour), price_move, plus the
    baseline stats as they stood BEFORE this observation.

    Anti-contamination: once warmed up, the rate folded INTO the EWMA is
    winsorized at BASELINE_WINSOR_MULT x the current mean, so a one-hour
    burst can't inflate the baseline and mask the follow-through hours —
    exactly the hours where informed money keeps accumulating.
    """
    if entry is None:
        entry = {"ts": ts, "v": m["vol"], "p": round(m["price"], 4), "n": 0,
                 "m": 0.0, "mv": [], "la": 0}
        return entry, {"dt_h": None}

    dt_h = (ts - entry["ts"]) / 3600.0
    if dt_h <= 0.01:
        return entry, {"dt_h": None}

    dv = max(0.0, m["vol"] - entry["v"])  # cumulative volume never decreases
    rate = dv / dt_h
    dp = m["price"] - entry["p"]
    impact = abs(dp) / dv if dv > 0 else None  # price move per unit traded
    # dollar volume: poly volume is already USD; kalshi is contracts, and a
    # contract's notional is roughly its price
    dv_usd = dv if m.get("platform") == "poly" else dv * max(m["price"], 0.01)
    obs = {
        "dt_h": dt_h, "rate": rate, "dp": dp, "dv": dv, "dv_usd": dv_usd,
        "p_prev": entry["p"],
        "impact": impact, "base_impact": entry.get("im", 0.0),
        "base_mean": entry["m"], "n": entry["n"],
        "recent_moves": list(entry["mv"]),
    }

    rate_upd = rate
    if entry["n"] >= cfg["MIN_OBS"] and entry["m"] > 0:
        rate_upd = min(rate, entry["m"] * cfg["BASELINE_WINSOR_MULT"])

    alpha = cfg["EWMA_ALPHA"]
    if entry["n"] == 0:
        entry["m"] = rate_upd
    else:
        entry["m"] += alpha * (rate_upd - entry["m"])
    if impact is not None:
        base_im = entry.get("im", 0.0)
        if base_im <= 0:
            entry["im"] = round(impact, 6)
        else:  # winsorized, same anti-contamination logic as the volume EWMA
            capped = min(impact, base_im * cfg["BASELINE_WINSOR_MULT"])
            entry["im"] = round(base_im + alpha * (capped - base_im), 6)
    entry["n"] += 1
    entry["mv"] = (entry["mv"] + [round(abs(dp), 4)])[-cfg["MAX_MOVE_WINDOW"]:]
    entry["ts"], entry["v"], entry["p"] = ts, m["vol"], round(m["price"], 4)
    return entry, obs


def prune_state(state: dict, ts: float) -> int:
    stale = [k for k, e in state["markets"].items()
             if ts - e.get("ts", 0) > CFG["STALE_PRUNE_HOURS"] * 3600]
    for k in stale:
        del state["markets"][k]
    wallets = state.get("wallets", {})
    for w in [w for w, rec in wallets.items()
              if ts - safe_float(rec.get("ts")) > CFG["WALLET_MEMORY_PRUNE_D"] * 86400]:
        del wallets[w]
    return len(stale)

# ---------------------------------------------------------------------------
# Signal detection (pure functions — unit-tested)
# ---------------------------------------------------------------------------


def detect_volume_spike(obs: dict, cfg: dict = CFG) -> dict | None:
    """Hourly volume rate >= VOL_SPIKE_MULT x the market's own baseline."""
    if obs.get("dt_h") is None or obs["dt_h"] > cfg["MAX_GAP_HOURS"]:
        return None
    if obs["n"] < cfg["MIN_OBS"]:
        return None  # warm-up: not enough history to call anything a spike
    if obs.get("dv_usd", obs["rate"] * obs["dt_h"]) < cfg["VOL_SPIKE_MIN_USD"]:
        return None  # dollar dust guard: multiples of pennies are noise
    mean = obs["base_mean"]
    if mean <= 0:
        return None  # dead market waking up is handled by the abs floor +
                     # jump/trade signals, not a divide-by-zero multiple
    mult = obs["rate"] / mean
    if mult < cfg["VOL_SPIKE_MULT"]:
        return None
    return {
        "type": "volume_spike",
        "desc": f"volume spike ({mult:.0f}x baseline)",
        "points": min(35, round(6 * mult)),
    }


def detect_price_jump(obs: dict, hours_to_close: float | None,
                      cfg: dict = CFG) -> dict | None:
    """Sudden price move vs the market's own recent-move baseline.

    Guards:
      - scheduled-news proxy: a jump within SCHEDULED_NEWS_MIN_H of
        resolution is presumed to be the event itself happening — UNLESS
        the repricing is extreme (>=15c or >=5x odds change): the Nobel
        leak was a 3.7c->39c longshot repricing that no scheduled-drift
        story explains, and the backtest showed the proxy killing it;
      - phantom guard: a "jump" with almost no volume behind it is a
        re-quoted book (one MM moving), not news.
    hours_to_close=None means the close timestamp is unknown/stale — an
    unknown clock must not suppress detection (backtest: a stale endDate
    silently zeroed a market that contained three documented insiders).
    """
    if obs.get("dt_h") is None or obs["dt_h"] > cfg["PRICE_JUMP_MAX_AGE_H"]:
        return None
    if obs["rate"] * obs["dt_h"] < cfg["JUMP_MIN_VOL_DELTA"]:
        return None
    dp = obs["dp"]
    if abs(dp) < cfg["PRICE_JUMP_MIN"]:
        return None
    extreme = abs(dp) >= cfg["JUMP_EXTREME_DP"]
    p_prev = obs.get("p_prev")
    if not extreme and p_prev and p_prev > 0:
        p_now = max(p_prev + dp, 0.001)
        odds_ratio = max(p_now / p_prev, p_prev / p_now)
        extreme = odds_ratio >= cfg["JUMP_EXTREME_RATIO"]
    if hours_to_close is not None \
            and hours_to_close < cfg["SCHEDULED_NEWS_MIN_H"] and not extreme:
        return None
    moves = sorted(obs.get("recent_moves", []))
    if len(moves) >= 4:
        median = moves[len(moves) // 2]
        if median > 0 and abs(dp) < cfg["PRICE_JUMP_MED_MULT"] * median:
            return None  # normal chop for this market, not a jump
    return {
        "type": "price_jump",
        "desc": f"price jump {dp * 100:+.0f}c in {obs['dt_h']:.1f}h",
        "points": min(35, round(320 * abs(dp))),
        "direction": 1 if dp > 0 else -1,
    }


def detect_price_impact(obs: dict, cfg: dict = CFG) -> dict | None:
    """Outsized price impact per unit of volume — this hour's |move|/volume
    vs the market's own baseline. Research-backed: insider trades move
    prices several times more per dollar than ordinary skilled flow, so a
    3c+ move on very little volume in a market that usually absorbs that
    volume without budging is informative even below the jump threshold."""
    if obs.get("dt_h") is None or obs["dt_h"] > cfg["MAX_GAP_HOURS"]:
        return None
    if obs["n"] < cfg["MIN_OBS"] or obs.get("impact") is None:
        return None
    if obs["dv"] < cfg["JUMP_MIN_VOL_DELTA"]:
        return None  # same phantom guard as the jump signal
    if abs(obs["dp"]) < cfg["IMPACT_MIN_MOVE"]:
        return None
    base = obs.get("base_impact", 0.0)
    if base <= 0:
        return None
    ratio = obs["impact"] / base
    if ratio < cfg["IMPACT_MULT"]:
        return None
    return {
        "type": "price_impact",
        "desc": f"outsized impact ({ratio:.0f}x baseline move-per-volume)",
        "points": min(15, round(5 + ratio)),
        "direction": 1 if obs["dp"] > 0 else -1,
    }


def repeat_actor_signal(record: dict | None, direction: int, ts: float,
                        cfg: dict = CFG) -> dict | None:
    """The same wallet flagged again on a LATER scan. Persistent per-wallet
    memory is what the best open-source trackers add over raw thresholds:
    one whale print is noise, the same wallet pressing across hours is a
    position being built (or flipped)."""
    if not record:
        return None
    if ts - safe_float(record.get("ts")) > cfg["REPEAT_ACTOR_WINDOW_D"] * 86400:
        return None
    flip = record.get("d") not in (None, direction)
    return {
        "type": "repeat_actor",
        "desc": ("repeat actor — same wallet flipped sides" if flip
                 else f"repeat actor ({record.get('n', 1) + 1} flags)"),
        "points": 10,
    }


def within_trader_signal(activity_rows: list[dict], notional: float,
                         cfg: dict = CFG) -> dict | None:
    """A trade that is huge relative to THIS wallet's own history is
    informative even when it's small in absolute terms (the within-trader
    bet-size signal from the Mitts & Ofir composite). Reuses the activity
    rows already fetched for the fresh-wallet check."""
    sizes = sorted(safe_float(r.get("usdcSize")) for r in activity_rows
                   if r.get("type") == "TRADE" and safe_float(r.get("usdcSize")) > 0)
    if len(sizes) < cfg["WITHIN_TRADER_MIN_ROWS"]:
        return None
    median = sizes[len(sizes) // 2]
    if median <= 0 or notional < cfg["WITHIN_TRADER_MULT"] * median:
        return None
    return {
        "type": "within_trader",
        "desc": f"out of character ({notional / median:.0f}x this wallet's"
                f" typical size)",
        "points": 8,
    }


def detect_large_trades(trades: list[dict], since_ts: float,
                        cfg: dict = CFG) -> dict | None:
    """Largest single on-chain trade since the last snapshot (Polymarket).

    Fires on either path:
      absolute — notional >= LARGE_TRADE_USD;
      relative — notional >= LARGE_TRADE_MED_MULT x this market's own median
                 trade size (with a floor: 5x of dust is still dust).
    The median comes from the whole fetched trade window, so a market where
    everyone bets $50 flags a $600 order that an absolute floor would miss.
    """
    notionals = [safe_float(t.get("size")) * safe_float(t.get("price"))
                 for t in trades]
    median = sorted(notionals)[len(notionals) // 2] if notionals else 0.0

    best = None
    for t, notional in zip(trades, notionals):
        if safe_float(t.get("timestamp")) <= since_ts:
            continue
        if best is None or notional > best[0]:
            best = (notional, t)
    if best is None:
        return None
    notional, t = best

    absolute = notional >= cfg["LARGE_TRADE_USD"]
    relative = (median > 0
                and notional >= cfg["LARGE_TRADE_MED_MULT"] * median
                and notional >= cfg["LARGE_TRADE_MIN_USD"])
    if not (absolute or relative):
        return None

    mult_txt = f", {notional / median:.0f}x typical" if median > 0 else ""
    # net long YES when buying the Yes leg (outcomeIndex 0) OR selling the
    # No leg — both push toward YES. The XNOR captures that equivalence.
    is_buy = t.get("side") == "BUY"
    is_yes_leg = t.get("outcomeIndex") == 0
    buys_yes = is_buy == is_yes_leg
    points = round(6 + notional / 500)
    if relative:
        points += 5  # out-of-character for THIS market is extra information
    return {
        "type": "large_trade",
        "desc": f"${notional:,.0f} single trade"
                f" ({'into' if buys_yes else 'against'} YES{mult_txt})",
        "points": min(30, points),
        "direction": 1 if buys_yes else -1,
        "wallet": t.get("proxyWallet", ""),
        "trader_name": t.get("name") or t.get("pseudonym") or "",
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


PSEUDONYM_EPOCH_RE = re.compile(r"^0x[0-9a-fA-F]{6,}-(\d{13})$")


def wallet_age_from_name(name: str, ts: float) -> float | None:
    """Polymarket's default account name encodes creation time as
    '0xADDR-<epoch-ms>'. When present it gives exact wallet age for free —
    no /activity call, no history-cap problems. Renamed wallets fall back
    to the activity check."""
    match = PSEUDONYM_EPOCH_RE.match((name or "").strip())
    if not match:
        return None
    created = int(match.group(1)) / 1000.0
    age = ts - created
    return age if 0 <= age < 20 * 365 * 86400 else None


def fresh_wallet_signal(notional: float, direction: int = 0) -> dict:
    """Direction rides along: the backtest showed followers must copy the
    FRESH WALLET's side — on the Iran replay every insider hour's largest
    print was a wrong-side whale, and following it loses 100%."""
    points = 15 + (10 if notional >= 5000 else 0)
    sig = {"type": "fresh_wallet",
           "desc": f"fresh wallet (<{CFG['FRESH_WALLET_MAX_AGE_D']:.0f}d old)"
                   f" loading up",
           "points": points}
    if direction:
        sig["direction"] = direction
    return sig


def is_insider_archetype(signals: list[dict]) -> bool:
    """Fresh wallet + large same-wallet trade = the documented insider
    archetype. On the Iran replay this conjunction ALONE flagged exactly
    the six documented insider wallets; in three other episodes it scored
    40-45 and died under the 55 threshold (bigwinner01, Mikeymike53,
    romanticpaul). It bypasses the aggregate score — but NOT the gate."""
    types = {s["type"] for s in signals}
    return "fresh_wallet" in types and "large_trade" in types


# --- news check: is there PUBLIC news explaining this move? ---------------
# An insider move is, by definition, a move BEFORE the news. A strong
# anomaly with zero recent press coverage is the suspicious shape; the same
# anomaly with a wall of headlines is just the market reading the paper.

NEWS_STOP = frozenset(
    "will the a an in on at by of to be for vs and or before after over"
    " under than with is are does 2025 2026 2027".split())


def news_query(title: str) -> str:
    """First few substantive words of the market title, for a news search."""
    words = re.findall(r"[a-zA-Z][a-zA-Z'-]+", title or "")
    picked = [w for w in words if w.lower() not in NEWS_STOP][:6]
    return " ".join(picked)


def count_recent_news(rss_text: str, ts: float, window_h: float) -> int:
    """Count RSS items published within the window. Pure parse — tested."""
    from email.utils import parsedate_to_datetime
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(rss_text)
    except ET.ParseError:
        return 0
    cutoff = ts - window_h * 3600
    count = 0
    for item in root.iter("item"):
        pub = item.findtext("pubDate") or ""
        try:
            when = parsedate_to_datetime(pub).timestamp()
        except (ValueError, TypeError):
            continue
        if when >= cutoff:
            count += 1
    return count


def fetch_news_count(query: str, ts: float) -> int | None:
    """Google News RSS — keyless, serverless-friendly. None on failure
    (failure must never be mistaken for 'no news')."""
    if not query:
        return None
    try:
        resp = _session.get(
            "https://news.google.com/rss/search",
            params={"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"},
            timeout=CFG["HTTP_TIMEOUT"])
        resp.raise_for_status()
        return count_recent_news(resp.text, ts, CFG["NEWS_WINDOW_H"])
    except requests.RequestException:
        return None


def apply_news_check(candidates: list[dict], ts: float,
                     cfg: dict = CFG) -> None:
    """Press-sweep the strongest alerts (in place, budgeted). Zero coverage
    -> an 'unexplained move' marker joins the signals (0 points — it's a
    verification tag, not a detector, but it lands in the ledger's trigger
    column so its CLV gets graded like everything else). Heavy coverage ->
    a 'likely public-news reaction' note on the alert."""
    budget = cfg["MAX_NEWS_CHECKS"]
    for a in candidates:
        if budget <= 0:
            break
        budget -= 1
        n = fetch_news_count(news_query(a["title"]), ts)
        if n is None:
            continue
        if n == 0:
            a["signals"].append({
                "type": "no_public_news",
                "desc": "no public news found — unexplained move",
                "points": 0})
        elif n >= cfg["NEWS_EXPLAINED_MIN"]:
            a["news_note"] = (f"{n} recent articles — likely reacting to"
                              f" public news, not leading it")


CHATTER_RE = re.compile(
    r"insider|inside\s+info|leak(?:ed|s)?\b|front.?run|knows?\s+something"
    r"|someone\s+knows|smart\s+money|suspicious\s+(?:volume|buy|bet)"
    r"|sus\s+(?:volume|buy|bet)|whale.{0,25}know|who(?:'s| is)\s+buying",
    re.I)


def detect_chatter(comments: list[dict], ts: float,
                   cfg: dict = CFG) -> dict | None:
    """Crowd chatter: multiple DISTINCT commenters raising insider suspicion
    on this market recently. The comment section notices anomalies before
    journalists do — but it's full of spam bots, so mentions are counted per
    unique wallet, and one lone voice never fires."""
    cutoff = ts - cfg["CHATTER_WINDOW_H"] * 3600
    voices = set()
    for c in comments:
        created = parse_iso(c.get("createdAt") or "")
        if created is None or created < cutoff:
            continue
        if CHATTER_RE.search(c.get("body") or ""):
            voices.add(c.get("userAddress") or c.get("id"))
    if len(voices) < cfg["CHATTER_MIN_VOICES"]:
        return None
    return {
        "type": "chatter",
        "desc": f"crowd chatter ({len(voices)} commenters crying insider)",
        "points": min(12, 4 + 2 * len(voices)),
    }


def thin_market_signal(vol24: float, cfg: dict = CFG) -> dict | None:
    """Insider-context bonus: big on-chain flow in a thin, obscure market is
    far more informative than the same flow in a liquid one. Only added when
    an on-chain signal already fired."""
    if vol24 >= cfg["THIN_MARKET_VOL24"]:
        return None
    return {"type": "thin_market",
            "desc": f"thin market (${vol24:,.0f}/24h)",
            "points": 10}

# ---------------------------------------------------------------------------
# Cross-platform confirmation + dedup (pure functions — unit-tested)
# ---------------------------------------------------------------------------

_STOPWORDS = frozenset(
    "will the a an in on at by of to be for vs and or before after over under"
    " than with is are does do next who what when how much many".split())


def title_tokens(title: str) -> frozenset:
    words = re.findall(r"[a-z0-9]+", (title or "").lower())
    return frozenset(w for w in words if w not in _STOPWORDS)


def title_similarity(a: str, b: str) -> float:
    """Jaccard on stopword-stripped tokens, with a hard veto: if both titles
    carry numbers and the number sets differ at all, they're different
    strikes of the same family ('BTC > 150k by Dec 31' vs 'BTC > 200k by
    Dec 31'), similarity 0."""
    ta, tb = title_tokens(a), title_tokens(b)
    if not ta or not tb:
        return 0.0
    # any token containing a digit is a number — including unit-suffixed
    # strikes like "150k"/"200k" that a pure-isdigit test would miss and
    # then wrongly merge as the same story
    na = {t for t in ta if any(ch.isdigit() for ch in t)}
    nb = {t for t in tb if any(ch.isdigit() for ch in t)}
    if na and nb and na != nb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def cross_platform_confirm(cands: list[dict], cfg: dict = CFG) -> None:
    """Same story moving on BOTH venues at once is much less likely to be
    noise. Adds a confirmation signal (in place) to every candidate whose
    title matches a candidate on the other platform."""
    for i, a in enumerate(cands):
        for b in cands[i + 1:]:
            if a["platform"] == b["platform"]:
                continue
            if title_similarity(a["title"], b["title"]) < cfg["CROSS_CONFIRM_JACCARD"]:
                continue
            for c, other in ((a, b), (b, a)):
                if any(s["type"] == "cross_platform" for s in c["signals"]):
                    continue
                c["signals"].append({
                    "type": "cross_platform",
                    "desc": f"confirmed on {other['platform']} too",
                    "points": cfg["CROSS_CONFIRM_POINTS"],
                })


def dedup_alerts(cands: list[dict], cfg: dict = CFG
                 ) -> tuple[list[dict], list[tuple[dict, str]]]:
    """One alert per story. Multiple legs of the same event spiking together
    (one news item) keep only the top scorer; a cross-platform twin of an
    already-kept alert is dropped (its info is on the kept one). Returns
    (kept, [(dropped, reason), ...])."""
    kept: list[dict] = []
    dropped: list[tuple[dict, str]] = []
    seen_events: dict = {}
    for c in sorted(cands, key=lambda x: x.get("sort_key", x["score"]),
                    reverse=True):
        ekey = (c["platform"], c.get("event") or c["market_id"])
        if ekey in seen_events:
            dropped.append((c, f"duplicate leg of alerted event: "
                               f"{seen_events[ekey]['title'][:50]}"))
            continue
        twin = next(
            (k for k in kept if k["platform"] != c["platform"]
             and title_similarity(k["title"], c["title"])
             >= cfg["CROSS_CONFIRM_JACCARD"]), None)
        if twin:
            dropped.append((c, f"same story alerted on {twin['platform']}"))
            continue
        seen_events[ekey] = c
        kept.append(c)
    return kept, dropped

# ---------------------------------------------------------------------------
# Scoring, direction, followability gate (pure functions — unit-tested)
# ---------------------------------------------------------------------------


def score_signals(signals: list[dict]) -> int:
    return min(100, sum(s["points"] for s in signals))


def choose_side(signals: list[dict], price_drift: float) -> str:
    """'yes' or 'no'. Priority order matters (backtest-proven): the fresh
    wallet's side beats everything (it IS the informed trader), then the
    flagged large trade, then the majority of other directional signals,
    then raw price drift."""
    for wanted in ("fresh_wallet", "large_trade"):
        for s in signals:
            if s.get("type") == wanted and s.get("direction"):
                return "yes" if s["direction"] > 0 else "no"
    directional = [s["direction"] for s in signals if s.get("direction")]
    if directional:
        return "yes" if sum(directional) >= 0 else "no"
    return "yes" if price_drift >= 0 else "no"


def followability_gate(entry_price: float, signal_price: float,
                       depth_usd: float, hours_to_close: float | None,
                       cfg: dict = CFG, min_depth: float | None = None,
                       fresh_exempt: bool = False) -> tuple[bool, list[str]]:
    """Can this signal still be followed at a fair price, in size, in time?

    Returns (passes, reasons_it_failed). Every check is a reason the follow
    would lose even if the signal itself is real:
      - entry already past GATE_MAX_PRICE -> the move happened, we're late
      - entry below GATE_MIN_PRICE -> longshot churn, not an information lag
      - entry > signal price + GATE_MAX_SLIP -> not catchable: the fill
        won't resemble the price the signal fired at
      - no depth -> can't put even a small size on
      - resolves too soon -> no lag window, the event IS the resolution
      - resolves too far out -> capital locked, CLV meaningless for months

    hours_to_close=None = clock unknown/stale (a stale endDate once computed
    NEGATIVE hours and silently zeroed a market with three documented
    insiders) -> time checks are skipped, never failed.
    fresh_exempt skips the max-days cap: fresh-wallet insider markets carry
    backstop close dates ("...by Dec 31") but resolve on the event — the
    backtest showed the cap blocking a true insider alert at 94 days out
    on a market that resolved within weeks.
    """
    reasons = []
    if entry_price > cfg["GATE_MAX_PRICE"]:
        reasons.append(f"too late: entry {entry_price:.2f} > {cfg['GATE_MAX_PRICE']}")
    if entry_price < cfg["GATE_MIN_PRICE"]:
        reasons.append(f"longshot: entry {entry_price:.2f} < {cfg['GATE_MIN_PRICE']}")
    slip = entry_price - signal_price
    if slip > cfg["GATE_MAX_SLIP"] + 1e-9:
        reasons.append(f"not catchable: entry {slip * 100:.0f}c above signal")
    floor = cfg["GATE_MIN_DEPTH_USD"] if min_depth is None else min_depth
    if depth_usd < floor:
        reasons.append(f"thin: ${depth_usd:,.0f} depth < ${floor:,.0f}")
    if hours_to_close is not None:
        if hours_to_close < cfg["GATE_MIN_HOURS_TO_CLOSE"]:
            reasons.append(f"resolves in {hours_to_close:.0f}h — no lag window")
        if hours_to_close > cfg["GATE_MAX_DAYS_TO_CLOSE"] * 24 \
                and not fresh_exempt:
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
# Calibration week (pure helpers — unit-tested)
# ---------------------------------------------------------------------------


def calibration_status(first_run_ts: float, ts: float,
                       cfg: dict = CFG) -> tuple[bool, int]:
    """(active, day_number). Day 1 starts at first_run_ts."""
    day = int((ts - first_run_ts) // 86400) + 1
    return (ts - first_run_ts < cfg["CALIB_DAYS"] * 86400, max(1, day))


def run_mode(calib_active: bool) -> str:
    return "calib" if calib_active else "normal"

# ---------------------------------------------------------------------------
# Telegram (formatters are pure — unit-tested; sender does I/O)
# ---------------------------------------------------------------------------

ALERT_HEADER = "🚨🚨 ALERT!!! INSIDER TRADING SCOOP 🚨🚨"
MONITOR_HEADER = "👀 TIPOFF MONITOR — strong signal, gated"


def format_alert(alert: dict) -> str:
    """Phone-skimmable alert. `alert` needs: title, platform, market_id,
    signals (list of desc strings), side, entry_price, category, stake_usd,
    hours_to_close (may be None), score, url; optionally calib (bool) and
    grade ('follow' default, or 'monitor' with gate_reasons).

    MONITOR grade exists because of the backtest: the Nobel-leak replay
    scored 125 for ten straight hours and the user never saw a thing — a
    strong signal the gate rejects is still intelligence, it just must not
    be dressed up as a trade."""
    side = alert["side"].upper()
    price_c = alert["entry_price"] * 100
    window = alert.get("hours_to_close")
    window_txt = ("unknown" if window is None
                  else f"{window:.0f}h" if window < 72
                  else f"{window / 24:.0f}d")
    monitor = alert.get("grade") == "monitor"
    lines = [
        MONITOR_HEADER if monitor else ALERT_HEADER,
        "",
        f"📍 {alert['title']}",
        f"   [{alert['platform']} · {alert['market_id']}]",
        f"🔔 Signal: {' + '.join(alert['signals'])}",
        f"💵 Price: {price_c:.0f}c — {'informed side is' if monitor else 'buy'}"
        f" {side}",
        f"🏷 Category: {alert['category']}",
    ]
    if monitor:
        lines += [
            f"⚡ Score {alert['score']}/100 · {len(alert['signals'])}"
            f" signals · resolves in {window_txt}",
            f"🚧 Gated: {alert.get('gate_reasons', 'followability failed')}",
            "👀 Watch it — don't chase. Not a paper trade.",
        ]
    else:
        lines += [
            f"📐 Suggested size: ${alert['stake_usd']:.0f} (paper)",
            f"⚡ Score {alert['score']}/100 · {len(alert['signals'])}"
            f" signals · resolves in {window_txt}",
            "⏳ Window open — verify + move.",
        ]
    if alert.get("news_note"):
        lines.append(f"📰 {alert['news_note']}")
    if alert.get("url"):
        lines.append(f"🔗 {alert['url']}")
    if alert.get("calib"):
        lines.append("📏 calibration week — thresholds loose")
    return "\n".join(lines)


def format_daily_ping(stats: dict) -> str:
    """Still-alive summary. `stats`: runs, markets, alerts, watches,
    open_positions, graded, wins, losses, avg_clv, calib_day (0 = normal)."""
    lines = [
        "🟢 Tipoff daily check-in — running fine",
        f"Last 24h: {stats['runs']} scans · {stats['markets']:,} markets"
        f" · {stats['alerts']} alerts · {stats['watches']} watches",
    ]
    if stats["graded"]:
        lines.append(
            f"Paper book: {stats['open_positions']} open · {stats['graded']}"
            f" graded ({stats['wins']}W–{stats['losses']}L, avg CLV"
            f" {stats['avg_clv'] * 100:+.1f}c)")
    elif stats["open_positions"]:
        lines.append(f"Paper book: {stats['open_positions']} open, none"
                     f" resolved yet")
    if stats["alerts"] == 0:
        lines.append("All quiet — nothing strong + followable fired.")
    if stats.get("health"):
        h = stats["health"]

        def mark(n):
            return f"{n:,} ✓" if n else "0 ⚠️"
        lines.append(
            f"🩺 kalshi {mark(h['kalshi'])} · poly {mark(h['poly'])}"
            f" · {h['warm']:,} baselines warm"
            f" · {stats.get('errors', 0)} fetch errors (24h)")
    if stats.get("minutes_used") is not None:
        lines.append(
            f"⛽ {stats['minutes_used']:,.0f}/{stats['minutes_budget']:,.0f}"
            f" Actions min ({stats['minutes_pct'] * 100:.0f}%)"
            f" · {stats['cadence']}")
    if stats.get("calib_day"):
        lines.append(f"📏 calibration week: day {stats['calib_day']:.0f}/"
                     f"{CFG['CALIB_DAYS']:.0f} — running loose, review the"
                     f" watch log")
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


def should_ping(meta: dict, ts: float, cfg: dict = CFG) -> bool:
    """Once a day: prefer the run in PING_UTC_HOUR; a >PING_MAX_GAP_H gap
    forces one regardless (also fires the hello ping on the very first run)."""
    last = safe_float(meta.get("last_ping_ts"))
    if ts - last >= cfg["PING_MAX_GAP_H"] * 3600:
        return True
    return (utc_hour(ts) == cfg["PING_UTC_HOUR"]
            and ts - last >= cfg["PING_MIN_GAP_H"] * 3600)

# ---------------------------------------------------------------------------
# GitHub Actions minutes guard + self-throttling
# ---------------------------------------------------------------------------
# Running out of Actions minutes is the one failure the daily ping can't
# warn about: no minutes = no ping = looks exactly like "all quiet". So every
# run measures this month's billable minutes from the repo's own workflow-run
# history (the built-in GITHUB_TOKEN can read that; no billing scope needed),
# projects month-end usage, and throttles BEFORE the tank is empty:
#
#   - with a WORKFLOW_EDIT_TOKEN secret (PAT that may edit workflows), Tipoff
#     rewrites the cron line in its own workflow file via the GitHub API —
#     real self-modification, real savings;
#   - without it, it flips to skip-mode: the cron still fires hourly but the
#     scanner exits immediately off-cadence (each skipped run still bills
#     the 1-minute floor, so this only saves about half).
#
# The throttle only ever tightens within a month and resets on the 1st.

WORKFLOW_PATH = ".github/workflows/tipoff.yml"
# eco_n=1 is the researched volume-matched schedule (see README "Scan
# cadence"): hourly through the 18h block carrying ~89% of traded volume,
# two touch-runs across the 07-12 UTC dead zone. 20 runs/day. Throttled
# tiers fall back to plain every-Nh crons.
CADENCE_CRONS = {
    1: ["7 0-6,13-23 * * *", "7 8,11 * * *"],
    2: ["7 */2 * * *"],
    3: ["7 */3 * * *"],
    6: ["7 */6 * * *"],
}
CADENCE_NAME = {1: "volume-matched schedule", 2: "every 2h",
                3: "every 3h", 6: "every 6h"}


def month_context(ts: float) -> tuple[str, str, float]:
    """(year-month string, month start ISO date, fraction of month elapsed)."""
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    start = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if start.month == 12:
        nxt = start.replace(year=start.year + 1, month=1)
    else:
        nxt = start.replace(month=start.month + 1)
    frac = (ts - start.timestamp()) / (nxt.timestamp() - start.timestamp())
    return dt.strftime("%Y-%m"), start.strftime("%Y-%m-%d"), frac


def estimate_billable_minutes(runs: list[dict]) -> float:
    """Billable minutes from workflow-run records: per-run wall time rounded
    UP to whole minutes (GitHub bills a 1-minute floor per job)."""
    total = 0.0
    for r in runs:
        started = parse_iso(r.get("run_started_at") or "")
        updated = parse_iso(r.get("updated_at") or "")
        if started is None or updated is None:
            continue
        total += max(1.0, math.ceil(max(0.0, updated - started) / 60.0))
    return total


def fetch_actions_minutes(repo: str, token: str, month_start: str) -> float | None:
    """Sum this month's billable minutes across the repo's workflow runs."""
    runs: list[dict] = []
    headers = {"Authorization": f"Bearer {token}",
               "Accept": "application/vnd.github+json"}
    for page in range(1, 11):  # 1000 runs covers a full hourly month
        try:
            resp = _session.get(
                f"https://api.github.com/repos/{repo}/actions/runs",
                params={"created": f">={month_start}", "per_page": 100,
                        "page": page},
                headers=headers, timeout=CFG["HTTP_TIMEOUT"])
            resp.raise_for_status()
            batch = resp.json().get("workflow_runs", [])
        except (requests.RequestException, ValueError) as err:
            print(f"  [warn] actions usage fetch failed: {err}")
            return None
        runs.extend(batch)
        if len(batch) < 100:
            break
    return estimate_billable_minutes(runs)


def budget_outlook(used: float, budget: float, month_frac: float,
                   cfg: dict = CFG) -> dict:
    """used_pct + straight-line month-end projection (damped early in the
    month so day-one noise can't trigger a panic downshift)."""
    frac = max(month_frac, cfg["BUDGET_MIN_ELAPSED_DAYS"] / 31.0)
    projected = used / frac
    return {"used": used, "budget": budget,
            "used_pct": used / budget if budget else 0.0,
            "projected": projected,
            "projected_pct": projected / budget if budget else 0.0}


def decide_eco_n(outlook: dict, current_n: int = 1, cfg: dict = CFG) -> int:
    """Cadence divisor (1=hourly, 2/3/6 = every Nh). Monotonic within a
    month — only ever slows down; the monthly rollover resets it."""
    if outlook["used_pct"] >= cfg["BUDGET_CRIT_USED_PCT"] \
            or outlook["projected_pct"] >= cfg["BUDGET_6H_PROJ_PCT"]:
        n = 6
    elif outlook["projected_pct"] >= cfg["BUDGET_3H_PROJ_PCT"]:
        n = 3
    elif outlook["projected_pct"] >= cfg["BUDGET_2H_PROJ_PCT"]:
        n = 2
    else:
        n = 1
    return max(n, current_n)


def should_skip_run(eco_n: int, hour: int, cfg: dict = CFG) -> bool:
    """Skip-mode cadence, anchored so the PING_UTC_HOUR run always scans
    (the daily ping must survive throttling)."""
    if eco_n <= 1:
        return False
    return hour % eco_n != cfg["PING_UTC_HOUR"] % eco_n


def set_cron_cadence(workflow_text: str, eco_n: int) -> str:
    """Replace the whole `schedule:` block (all cron lines and any comments
    inside it) with the cadence for eco_n. Line-based on purpose — regex
    over multi-line YAML blocks is where bugs live."""
    out, in_sched = [], False
    for line in workflow_text.splitlines():
        stripped = line.strip()
        if stripped == "schedule:":
            in_sched = True
            out.append(line)
            out.extend(f'    - cron: "{c}"' for c in CADENCE_CRONS[eco_n])
            continue
        if in_sched:
            if stripped.startswith("- cron:") or stripped.startswith("#"):
                continue  # old schedule content
            in_sched = False
        out.append(line)
    return "\n".join(out) + "\n"


def apply_cron_change(eco_n: int, token: str) -> bool:
    """Rewrite this workflow's cron line on the default branch via the
    GitHub contents API (needs a PAT allowed to edit workflow files)."""
    import base64
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    if not (repo and token):
        return False
    url = f"https://api.github.com/repos/{repo}/contents/{WORKFLOW_PATH}"
    headers = {"Authorization": f"Bearer {token}",
               "Accept": "application/vnd.github+json"}
    try:
        resp = _session.get(url, params={"ref": branch}, headers=headers,
                            timeout=CFG["HTTP_TIMEOUT"])
        resp.raise_for_status()
        payload = resp.json()
        text = base64.b64decode(payload["content"]).decode()
        new_text = set_cron_cadence(text, eco_n)
        if new_text == text:
            return True
        resp = _session.put(url, headers=headers, timeout=CFG["HTTP_TIMEOUT"],
                            json={
            "message": f"tipoff: self-throttle cron to "
                       f"{CADENCE_NAME[eco_n]} (minutes budget)",
            "content": base64.b64encode(new_text.encode()).decode(),
            "sha": payload["sha"], "branch": branch,
        })
        resp.raise_for_status()
        return True
    except (requests.RequestException, KeyError, ValueError) as err:
        print(f"  [warn] cron self-edit failed: {err}")
        return False


def format_budget_alert(outlook: dict, eco_n: int, method: str) -> str:
    """method: 'cron' (workflow rewritten), 'skip' (in-place), 'warn'
    (no throttle change, just a heads-up)."""
    lines = [
        "⛽ Tipoff minutes check",
        f"Used {outlook['used']:,.0f}/{outlook['budget']:,.0f} GitHub Actions"
        f" min this month ({outlook['used_pct'] * 100:.0f}%) — projected"
        f" ~{outlook['projected']:,.0f} by month-end.",
    ]
    if method == "cron":
        lines.append(f"🔧 Self-throttled: rewrote my own cron to"
                     f" {CADENCE_NAME[eco_n]}. Resets to hourly on the 1st.")
    elif method == "skip":
        lines.append(f"🔧 Throttled to {CADENCE_NAME[eco_n]} by skipping"
                     f" scans in place (skipped runs still bill ~1 min).")
        lines.append("For real savings add a WORKFLOW_EDIT_TOKEN secret so I"
                     " can rewrite my own cron — see README.")
    else:
        lines.append("No throttle change yet — watching the projection.")
    return "\n".join(lines)


def check_actions_budget(meta: dict, ts: float) -> dict | None:
    """Measure usage, warn, and self-throttle. Mutates meta['budget'].
    Returns the outlook (for the daily ping) or None when unmeasurable
    (e.g. local runs outside Actions)."""
    token_edit = os.environ.get("WORKFLOW_EDIT_TOKEN", "")
    token_read = token_edit or os.environ.get("GH_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    ym, month_start, month_frac = month_context(ts)
    b = meta.setdefault("budget", {})

    if b.get("month") != ym:  # monthly rollover: restore full speed
        old_n = b.get("eco_n", 1)
        if old_n > 1:
            restored = b.get("method") != "cron" or \
                apply_cron_change(1, token_edit)
            if restored:
                send_telegram("⛽ New month — Tipoff back to the full"
                              " volume-matched schedule.")
        b.clear()
        b.update({"month": ym, "eco_n": 1, "method": "none", "warned": 0.0})

    if not (token_read and repo):
        return None
    used = fetch_actions_minutes(repo, token_read, month_start)
    if used is None:
        return None
    outlook = budget_outlook(used, CFG["ACTIONS_BUDGET_MIN"], month_frac)
    b["used"] = round(used)

    n = decide_eco_n(outlook, b.get("eco_n", 1))
    if n > b.get("eco_n", 1):
        if token_edit and apply_cron_change(n, token_edit):
            method = "cron"
        else:
            method = "skip"
        b.update({"eco_n": n, "method": method})
        send_telegram(format_budget_alert(outlook, n, method))
        print(f"  minutes budget: throttled to {CADENCE_NAME[n]} ({method})")
    elif outlook["used_pct"] >= CFG["BUDGET_WARN_USED_PCT"] \
            and b.get("warned", 0.0) < CFG["BUDGET_WARN_USED_PCT"]:
        b["warned"] = outlook["used_pct"]
        send_telegram(format_budget_alert(outlook, n, "warn"))
    return outlook

# ---------------------------------------------------------------------------
# Paper ledger + CLV grading
# ---------------------------------------------------------------------------


def read_ledger() -> list[dict]:
    if not LEDGER_FILE.exists():
        return []
    with LEDGER_FILE.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:  # schema migration for rows written before newer columns
        r.setdefault("mode", "normal")
        r.setdefault("triggers", "")
        r.setdefault("read", "")
    return rows


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
        row["read"] = ""
        return
    won = (result == row["side"])
    row["status"] = "won" if won else "lost"
    row["roi"] = f"{((1.0 - entry) / entry) if won else -1.0:.4f}"
    last = safe_float(row.get("last_price"), entry)
    clv = last - entry
    row["clv"] = f"{clv:.4f}"
    row["read"] = informed_read(won, clv)


def informed_read(won: bool, clv: float) -> str:
    """Was the alert actually informed money, judged in hindsight?

    Outcome and information are different axes: a bet can WIN by luck while
    the line said you were late, and can LOSE while the line proves the
    signal was real. CLV is the information axis:
      informed-like    won  AND the line kept moving our way (clv >= +5c)
      early-but-wrong  lost BUT the line moved our way — real signal,
                       unlucky outcome (still evidence of informed flow)
      late-money       the line moved against us after entry (clv <= -2c) —
                       we were the exit liquidity, whatever the outcome
      neutral          everything else (no informational verdict)
    """
    if clv >= 0.05:
        return "informed-like" if won else "early-but-wrong"
    if clv <= -0.02:
        return "late-money"
    return "neutral"


def verdict_rows(rows: list[dict]) -> list[dict]:
    """Calibration-week alerts used looser thresholds; mixing them into the
    verdict would bias it. They stay in the ledger for review only."""
    return [r for r in rows if r.get("mode") != "calib"]


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


def compute_trigger_report(rows: list[dict]) -> dict:
    """Per-signal-type stats — the follow-vs-fade table nobody in the space
    publishes. A graded alert counts toward EVERY trigger it contained, so
    the cells answer 'when this signal was part of an alert, did the line
    keep moving our way?'"""
    stats: dict[str, dict] = {}
    for row in rows:
        if row["status"] not in ("won", "lost"):
            continue
        for trig in (row.get("triggers") or "").split("+"):
            trig = trig.strip()
            if not trig:
                continue
            b = stats.setdefault(trig, {"graded": 0, "wins": 0,
                                        "roi_sum": 0.0, "clv_sum": 0.0})
            b["graded"] += 1
            b["wins"] += row["status"] == "won"
            b["roi_sum"] += safe_float(row["roi"])
            b["clv_sum"] += safe_float(row["clv"])
    for b in stats.values():
        n = b["graded"]
        b["win_rate"] = b["wins"] / n
        b["avg_roi"] = b["roi_sum"] / n
        b["avg_clv"] = b["clv_sum"] / n
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
    scored = verdict_rows(rows)
    n_calib = len(rows) - len(scored)
    stats = compute_report(scored)
    lines = [
        "# Tipoff — paper-trading report",
        "",
        f"_Auto-generated {iso_utc(ts)}. {len(rows)} alerts ledgered"
        + (f" ({n_calib} from calibration week, excluded from the verdict"
           f" stats below)." if n_calib else "."),
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
    graded_rows = [r for r in scored if r["status"] in ("won", "lost")]
    if graded_rows:
        reads = read_counts(graded_rows)
        lines += [
            "",
            f"**Informed-flow reads** (was the alert actually informed money,"
            f" judged by where the line went): {reads['informed-like']}"
            f" informed-like · {reads['early-but-wrong']} early-but-wrong"
            f" (real signal, unlucky outcome) · {reads['late-money']}"
            f" late-money · {reads['neutral']} neutral",
        ]
    triggers = compute_trigger_report(scored)
    if triggers:
        lines += [
            "",
            "## By trigger",
            "",
            "A graded alert counts toward every signal it contained — this is",
            "the follow-vs-fade table: a trigger with negative CLV is one to",
            "fade or drop, whatever its win rate says.",
            "",
            "| Trigger | Graded | Win% | Avg ROI | Avg CLV | Verdict |",
            "|---|---|---|---|---|---|",
        ]
        for trig in sorted(triggers, key=lambda t: -triggers[t]["graded"]):
            b = triggers[trig]
            lines.append(
                f"| {trig} | {b['graded']} | {b['win_rate'] * 100:.0f}% "
                f"| {b['avg_roi'] * 100:+.1f}% | {b['avg_clv'] * 100:+.1f}c "
                f"| {b['verdict']} |")
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(lines) + "\n")


def watch_reason_histogram(watch_rows: list[dict]) -> list[tuple[str, int]]:
    """Top filter reasons across the watch log — the tuning signal: what is
    the net actually rejecting, and does that match intent?"""
    counts: dict[str, int] = {}
    for w in watch_rows:
        for reason in (w.get("reasons") or "").split(";"):
            key = reason.strip().split(":")[0].strip()
            if key:
                counts[key] = counts.get(key, 0) + 1
    return sorted(counts.items(), key=lambda kv: -kv[1])


def read_counts(rows: list[dict]) -> dict:
    counts = {"informed-like": 0, "early-but-wrong": 0,
              "late-money": 0, "neutral": 0}
    for r in rows:
        if r.get("read") in counts:
            counts[r["read"]] += 1
    return counts


def write_calibration_report(ledger: list[dict], watch_rows: list[dict],
                             research_rows: list[dict], meta: dict,
                             ts: float) -> str:
    """One-time review written when calibration week ends. Everything here
    INCLUDES calibration-mode alerts (that's the point — reviewing what the
    loose week caught) unlike REPORT.md, which excludes them. Returns a
    short Telegram summary."""
    follows = [r for r in ledger]
    graded = [r for r in ledger if r["status"] in ("won", "lost")]
    wins = sum(r["status"] == "won" for r in graded)
    monitors = sum(1 for r in research_rows if r.get("alerted") == "M")
    avg_clv = (sum(safe_float(r["clv"]) for r in graded) / len(graded)
               if graded else 0.0)
    avg_roi = (sum(safe_float(r["roi"]) for r in graded) / len(graded)
               if graded else 0.0)
    reads = read_counts(graded)
    histogram = watch_reason_histogram(watch_rows)
    start = meta.get("first_run_ts")

    lines = [
        "# Calibration week review",
        "",
        f"_Auto-generated {iso_utc(ts)}. Covers"
        f" {iso_utc(start) if start else '?'} → {iso_utc(ts)}. Unlike"
        f" REPORT.md, calibration-mode alerts ARE included here — this is"
        f" the tuning review, not the pre-registered verdict._",
        "",
        "## Totals",
        "",
        f"- **{len(follows)} paper positions** ({monitors} additional"
        f" MONITOR-grade alerts, never traded)",
        f"- **Graded: {len(graded)}** — {wins}W–{len(graded) - wins}L,"
        f" avg ROI {avg_roi * 100:+.1f}%, avg CLV {avg_clv * 100:+.1f}c",
        f"- Informed-flow reads: {reads['informed-like']} informed-like ·"
        f" {reads['early-but-wrong']} early-but-wrong ·"
        f" {reads['late-money']} late-money · {reads['neutral']} neutral",
        f"- {len(research_rows)} research candidates logged;"
        f" {len(watch_rows)} watch entries",
        "",
        "## What the filters rejected (top reasons)",
        "",
        "| Reason | Count |",
        "|---|---|",
    ]
    lines += [f"| {k} | {v} |" for k, v in histogram[:12]]
    lines += [
        "",
        "## Per-category (calibration included)",
        "",
        "| Category | Alerts | Graded | Win% | Avg ROI | Avg CLV |",
        "|---|---|---|---|---|---|",
    ]
    stats = compute_report(ledger)
    for cat in list(CATEGORIES) + ["ALL"]:
        b = stats[cat]
        lines.append(
            f"| {cat} | {b['alerts']} | {b['graded']}"
            f" | {b['win_rate'] * 100:.0f}% | {b['avg_roi'] * 100:+.1f}%"
            f" | {b['avg_clv'] * 100:+.1f}c |")
    triggers = compute_trigger_report(ledger)
    if triggers:
        lines += ["", "## Per-trigger (calibration included)", "",
                  "| Trigger | Graded | Win% | Avg CLV |", "|---|---|---|---|"]
        for trig in sorted(triggers, key=lambda t: -triggers[t]["graded"]):
            b = triggers[trig]
            lines.append(f"| {trig} | {b['graded']}"
                         f" | {b['win_rate'] * 100:.0f}%"
                         f" | {b['avg_clv'] * 100:+.1f}c |")
    lines += [
        "",
        "## How to use this",
        "",
        "1. Sort the ledger by `read`: `early-but-wrong` rows are real",
        "   signals with unlucky outcomes — the archetype to protect.",
        "   `late-money` rows are what to filter harder.",
        "2. If good alerts died in the top filter reasons above, loosen",
        "   that one gate value in config.py; if junk alerted, raise the",
        "   relevant signal threshold.",
        "3. Normal mode (score >= 55) is now live; the pre-registered",
        "   verdict accumulates in REPORT.md from here on.",
    ]
    CALIB_REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    CALIB_REPORT_FILE.write_text("\n".join(lines) + "\n")

    top = ", ".join(f"{k} ({v})" for k, v in histogram[:3])
    return (f"📏 Calibration week complete!\n"
            f"{len(follows)} paper alerts + {monitors} monitors ·"
            f" graded {wins}W–{len(graded) - wins}L ·"
            f" avg CLV {avg_clv * 100:+.1f}c\n"
            f"Reads: {reads['informed-like']} informed-like ·"
            f" {reads['early-but-wrong']} early-but-wrong ·"
            f" {reads['late-money']} late-money\n"
            f"Top filters: {top}\n"
            f"Full review: ledger/CALIBRATION.md — normal mode is live.")


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
        writer = csv.DictWriter(fh, fieldnames=WATCH_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

# ---------------------------------------------------------------------------
# Research dataset — forward returns for every signal candidate
# ---------------------------------------------------------------------------


def fill_forward_returns(rows: list[dict], prices: dict, ts: float) -> int:
    """Fill due forward-price columns in place. `prices` maps
    'platform:market_id' -> current YES price. A horizon whose market has
    left the universe gets 'na' once RESEARCH_GRACE_H past due. Returns the
    number of cells filled."""
    filled = 0
    for row in rows:
        key = f'{row["platform"]}:{row["market_id"]}'
        born = safe_float(row.get("ts_unix"))
        for col, hours in RESEARCH_HORIZONS.items():
            if row.get(col):
                continue
            due = born + hours * 3600
            if ts < due:
                continue
            price = prices.get(key)
            if price is not None:
                row[col] = f"{price:.4f}"
                filled += 1
            elif ts >= due + RESEARCH_GRACE_H * 3600:
                row[col] = "na"
                filled += 1
    return filled


def update_research_log(new_rows: list[dict], prices: dict, ts: float) -> int:
    """Append this run's candidates and fill due forward returns on the
    whole file. Oldest rows fall off past RESEARCH_MAX_ROWS."""
    rows = []
    if RESEARCH_FILE.exists():
        with RESEARCH_FILE.open(newline="") as fh:
            rows = list(csv.DictReader(fh))
    filled = fill_forward_returns(rows, prices, ts)
    rows.extend(new_rows)
    rows = rows[-RESEARCH_MAX_ROWS:]
    RESEARCH_FILE.parent.mkdir(parents=True, exist_ok=True)
    with RESEARCH_FILE.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=RESEARCH_COLUMNS,
                                extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return filled


def research_row(c: dict, ts: float, mode: str, alerted: bool, score: int,
                 side: str, entry_price: float, depth: float,
                 hours_to_close: float | None,
                 gate_reasons: list[str]) -> dict:
    wallet = next((s.get("wallet", "") for s in c["signals"]
                   if s["type"] == "large_trade"), "")
    return {
        "ts": iso_utc(ts), "ts_unix": f"{ts:.0f}", "platform": c["platform"],
        "market_id": c["id"], "title": c["title"], "category": c["category"],
        "insiderable": insiderability(c["title"], c["category"]),
        "mode": mode, "alerted": "1" if alerted else "0", "score": str(score),
        "signals": " + ".join(s["desc"] for s in c["signals"]),
        "triggers": "+".join(sorted({s["type"] for s in c["signals"]})),
        "side": side,
        "yes_price": f"{c['price']:.4f}", "entry_price": f"{entry_price:.4f}",
        "vol24": f"{c['vol24']:.0f}", "depth": f"{depth:.0f}",
        "hours_to_close": ("" if hours_to_close is None
                           else f"{hours_to_close:.1f}"),
        "gate_reasons": "; ".join(gate_reasons), "wallet": wallet,
        "p_1h": "", "p_6h": "", "p_24h": "",
    }

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
            except (json.JSONDecodeError, TypeError):
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


def scan_market(m: dict, entry: dict | None, ts: float, trade_budget: dict,
                wallet_memory: dict) -> tuple[dict, list[dict], dict]:
    """Update one market's baseline and return (entry, signals, obs)."""
    entry, obs = observe_market(entry, m, ts)
    tier = insiderability(m["title"], m["category"])
    if tier == "none":
        # game-outcome market: the move IS the game; no insider can exist.
        # Baseline still updates (cheap) but no signals, no API spend.
        return entry, [], obs
    signals = []
    hours_to_close = hours_until_close(m, ts)

    spike = detect_volume_spike(obs)
    if spike:
        signals.append(spike)
    jump = detect_price_jump(obs, hours_to_close)
    if jump:
        signals.append(jump)
    impact = detect_price_impact(obs)
    if impact:
        signals.append(impact)

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
            wallet = big.get("wallet", "")
            repeat = repeat_actor_signal(wallet_memory.get(wallet),
                                         big["direction"], ts)
            if repeat:
                signals.append(repeat)
            if wallet:  # remember every flagged wallet across scans
                prior = wallet_memory.get(wallet, {})
                wallet_memory[wallet] = {"ts": ts, "d": big["direction"],
                                         "n": prior.get("n", 0) + 1}
            if big["notional"] >= CFG["FRESH_WALLET_TRADE_USD"] and wallet \
                    and trade_budget["wallets"] < CFG["MAX_WALLET_LOOKUPS"]:
                trade_budget["wallets"] += 1
                limit = CFG["FRESH_WALLET_ACTIVITY_LIMIT"]
                activity = http_get_json(f"{DATA_API_BASE}/activity", {
                    "user": wallet, "limit": limit}) or []
                # two freshness sources: the activity feed, plus the exact
                # creation time hidden in unrenamed default account names
                # (the activity feed prunes history and misses some)
                pseudo_age = wallet_age_from_name(big.get("trader_name", ""), ts)
                fresh = is_fresh_wallet(activity, limit, ts) or (
                    pseudo_age is not None
                    and pseudo_age <= CFG["FRESH_WALLET_MAX_AGE_D"] * 86400)
                if fresh:
                    signals.append(fresh_wallet_signal(big["notional"],
                                                       big["direction"]))
                within = within_trader_signal(activity, big["notional"])
                if within:
                    signals.append(within)
            thin = thin_market_signal(m["vol24"])
            if thin:
                signals.append(thin)
        # crowd chatter: are commenters already crying insider on this one?
        if m.get("event_id") \
                and trade_budget["comments"] < CFG["MAX_COMMENT_FETCHES"]:
            trade_budget["comments"] += 1
            comments = http_get_json(f"{GAMMA_BASE}/comments", {
                "parent_entity_type": "Event",
                "parent_entity_id": m["event_id"], "limit": 40,
                "order": "createdAt", "ascending": "false"}) or []
            chatter = detect_chatter(comments, ts)
            if chatter:
                signals.append(chatter)
    if signals and tier == "high":
        # every documented insider episode lived in a decision market —
        # anomalies here deserve more weight than the same anomaly elsewhere
        signals.append({"type": "insiderable",
                        "desc": "decision market — insider possible",
                        "points": CFG["INSIDERABLE_POINTS"]})
    return entry, signals, obs


def build_day_stats(meta: dict, ledger: list[dict], calib_active: bool,
                    calib_day: int, health: dict | None = None) -> dict:
    day = meta.get("day", {})
    graded_rows = [r for r in ledger if r["status"] in ("won", "lost")]
    return {
        "runs": day.get("runs", 0),
        "markets": day.get("markets", 0),
        "alerts": day.get("alerts", 0),
        "watches": day.get("watches", 0),
        "errors": day.get("errors", 0),
        "health": health,
        "open_positions": sum(r["status"] == "open" for r in ledger),
        "graded": len(graded_rows),
        "wins": sum(r["status"] == "won" for r in graded_rows),
        "losses": sum(r["status"] == "lost" for r in graded_rows),
        "avg_clv": (sum(safe_float(r["clv"]) for r in graded_rows)
                    / len(graded_rows)) if graded_rows else 0.0,
        "calib_day": calib_day if calib_active else 0,
    }


def main() -> int:
    load_dotenv(ROOT / ".env")
    _RUN_STATS["http_errors"] = 0
    ts = now_ts()
    print(f"tipoff scan @ {iso_utc(ts)}")

    state = load_state()
    meta = state["meta"]

    # eco skip-mode (no-PAT throttle): bail before any market fetch. The
    # cron still fired, but this cycle is deliberately cheap.
    b = meta.get("budget") or {}
    if b.get("method") == "skip" and should_skip_run(b.get("eco_n", 1),
                                                     utc_hour(ts)):
        print(f"  eco mode ({CADENCE_NAME[b['eco_n']]}): skipping this cycle"
              f" — over the minutes budget")
        return 0

    meta.setdefault("first_run_ts", ts)
    day = meta.setdefault("day", {"runs": 0, "alerts": 0, "watches": 0,
                                  "markets": 0, "errors": 0})
    calib_active, calib_day = calibration_status(meta["first_run_ts"], ts)
    mode = run_mode(calib_active)
    if calib_active:
        print(f"  calibration week: day {calib_day}/{CFG['CALIB_DAYS']:.0f}"
              f" (alert score >= {CFG['CALIB_ALERT_SCORE']})")
    alert_score = CFG["CALIB_ALERT_SCORE"] if calib_active else CFG["ALERT_SCORE"]
    max_alerts = (CFG["CALIB_MAX_ALERTS_PER_RUN"] if calib_active
                  else CFG["MAX_ALERTS_PER_RUN"])
    cooldown_h = CFG["CALIB_COOLDOWN_H"] if calib_active else CFG["REALERT_COOLDOWN_H"]

    ledger = read_ledger()

    # one-time calibration-week review: fires on the first run AFTER the
    # loose week ends, then never again
    if not calib_active and meta.get("first_run_ts") \
            and not meta.get("calib_reported"):
        watch_rows = []
        if WATCH_FILE.exists():
            with WATCH_FILE.open(newline="") as fh:
                watch_rows = list(csv.DictReader(fh))
        research_rows = []
        if RESEARCH_FILE.exists():
            with RESEARCH_FILE.open(newline="") as fh:
                research_rows = list(csv.DictReader(fh))
        summary = write_calibration_report(ledger, watch_rows,
                                           research_rows, meta, ts)
        send_telegram(summary)
        meta["calib_reported"] = iso_utc(ts)
        print("  calibration week review written to ledger/CALIBRATION.md")

    # --- 1. grade yesterday's calls before making today's ---
    graded = resolve_open_positions(ledger, ts)
    if graded:
        print(f"  graded {graded} resolved position(s)")

    # --- 2. pull the market universe ---
    kalshi = select_universe(fetch_kalshi_markets(), CFG["KALSHI_MIN_VOL24"])
    poly = select_universe(fetch_polymarket_markets(), CFG["POLY_MIN_VOL24"])
    print(f"  tracking {len(kalshi)} kalshi + {len(poly)} polymarket markets")
    for name, n in (("kalshi", len(kalshi)), ("polymarket", len(poly))):
        # a platform going dark is a health event, not just a log line
        if n == 0 and ts - safe_float(meta.get(f"down_warned_{name}")) > 86400:
            meta[f"down_warned_{name}"] = ts
            send_telegram(f"⚠️ Tipoff health: {name} returned no markets this"
                          f" run. Scanning continues on the other platform;"
                          f" this warning repeats at most daily.")
    if not kalshi and not poly:
        print("  [warn] both platforms returned nothing; keeping state as-is")
        write_ledger(ledger)
        write_report(ledger, ts)
        return 0

    # --- 3. scan every market, collect signal-bearing candidates ---
    trade_budget = {"trades": 0, "wallets": 0, "comments": 0}
    candidates = []
    state.setdefault("wallets", {})
    for m in kalshi + poly:
        key = market_key(m)
        entry, signals, obs = scan_market(m, state["markets"].get(key), ts,
                                          trade_budget, state["wallets"])
        state["markets"][key] = entry
        if signals:
            candidates.append({**m, "signals": signals, "obs": obs,
                               "state_key": key})

    # --- 4. cross-platform confirmation, then score/gate/dedup ---
    cross_platform_confirm(candidates)

    alertable, watches = [], []
    holding = {r["market_id"] for r in ledger if r["status"] == "open"}

    def to_watch(c, score, reasons):
        watches.append({
            "ts": iso_utc(ts), "platform": c["platform"],
            "market_id": c["id"], "title": c["title"],
            "category": c["category"], "score": score,
            "signals": " + ".join(s["desc"] for s in c["signals"]),
            "mode": mode, "reasons": "; ".join(reasons),
        })

    research_rows: dict[str, dict] = {}
    monitorable = []
    for c in candidates:
        score = score_signals(c["signals"])
        side = choose_side(c["signals"], c["obs"].get("dp", 0.0))
        entry_price = c["yes_ask"] if side == "yes" else c["no_ask"]
        signal_price = side_price(side, c["price"])
        depth = c["depth_yes_usd"] if side == "yes" else c["depth_no_usd"]
        hours_to_close = hours_until_close(c, ts)
        fresh_fired = any(s["type"] == "fresh_wallet" for s in c["signals"])
        archetype = is_insider_archetype(c["signals"])
        min_depth = (CFG["GATE_MIN_LIQUIDITY_USD"] if c["platform"] == "poly"
                     else CFG["GATE_MIN_DEPTH_USD"])
        passes, gate_reasons = followability_gate(
            entry_price, signal_price, depth, hours_to_close,
            min_depth=min_depth, fresh_exempt=fresh_fired)
        research_rows[c["id"]] = research_row(
            c, ts, mode, False, score, side, entry_price, depth,
            hours_to_close, gate_reasons)

        # strong = aggregate score, OR the insider archetype (fresh wallet
        # + large same-wallet trade), which the backtest showed flagging
        # exactly the documented insider wallets while scoring under 55
        strong = score >= alert_score or archetype
        entry_state = state["markets"][c["state_key"]]
        cooling = ts - safe_float(entry_state.get("la")) < cooldown_h * 3600
        may_escalate = entry_state.get("lg") == "M"  # monitor -> follow

        if c["id"] in holding:
            to_watch(c, score, gate_reasons + ["already holding (open ledger row)"])
        elif not strong:
            to_watch(c, score, gate_reasons + [f"score {score} < {alert_score}"])
        elif passes:
            if cooling and not may_escalate:
                to_watch(c, score, ["re-alert cooldown"])
            else:
                alertable.append({**c, "score": score, "side": side,
                                  "entry_price": entry_price, "depth": depth,
                                  "hours_to_close": hours_to_close,
                                  "grade": "follow", "sort_key": score + 1000})
        else:  # strong but gated -> MONITOR-grade intel, never a paper trade
            if cooling:
                to_watch(c, score, ["re-alert cooldown (monitor)"])
            else:
                monitorable.append({**c, "score": score, "side": side,
                                    "entry_price": entry_price, "depth": depth,
                                    "hours_to_close": hours_to_close,
                                    "grade": "monitor", "sort_key": score,
                                    "gate_reasons": "; ".join(gate_reasons)})

    kept, duplicates = dedup_alerts(alertable + monitorable)
    for c, reason in duplicates:
        to_watch(c, c["score"], [reason])
    follows = [c for c in kept if c["grade"] == "follow"]
    monitors = [c for c in kept if c["grade"] == "monitor"]
    for c in follows[max_alerts:]:
        to_watch(c, c["score"], ["alert cap for this run"])
    for c in monitors[CFG["MONITOR_MAX_PER_RUN"]:]:
        to_watch(c, c["score"], ["monitor cap for this run"])
    alerts = follows[:max_alerts]
    monitors = monitors[: CFG["MONITOR_MAX_PER_RUN"]]

    # investigator step: is there PUBLIC news explaining these moves?
    apply_news_check(alerts + monitors, ts)

    for w in watches:
        print(f"  WATCH [{w['score']:>3}] {w['title'][:55]} ::"
              f" {w['signals']} :: {w['reasons']}")

    # --- 5. send alerts, append to the paper ledger ---
    next_id = 1 + max((int(r["id"]) for r in ledger if r["id"].isdigit()),
                      default=0)
    for a in alerts:
        stake = suggested_stake(a["score"], a["depth"])
        desc_list = [s["desc"] for s in a["signals"]]
        msg = format_alert({
            "title": a["title"], "platform": a["platform"],
            "market_id": a["id"], "signals": desc_list, "side": a["side"],
            "entry_price": a["entry_price"], "category": a["category"],
            "stake_usd": stake, "hours_to_close": a["hours_to_close"],
            "score": a["score"], "url": a["url"], "calib": calib_active,
            "news_note": a.get("news_note"),
        })
        sent = send_telegram(msg)
        print(f"  ALERT [{a['score']:>3}] {'sent' if sent else 'dry'} :: "
              f"{a['title'][:55]} ({a['side']} @ {a['entry_price']:.2f})")
        state["markets"][a["state_key"]].update({"la": ts, "lg": "F"})
        if a["id"] in research_rows:
            research_rows[a["id"]]["alerted"] = "1"
        ledger.append({
            "id": str(next_id), "ts": iso_utc(ts), "platform": a["platform"],
            "market_id": a["id"], "title": a["title"],
            "category": a["category"], "side": a["side"],
            "entry_price": f"{a['entry_price']:.4f}",
            "stake_usd": f"{stake:.0f}", "score": str(a["score"]),
            "signals": " + ".join(desc_list),
            "triggers": "+".join(sorted({s["type"] for s in a["signals"]})),
            "hours_to_close": ("" if a["hours_to_close"] is None
                               else f"{a['hours_to_close']:.1f}"),
            "mode": mode,
            "status": "open", "last_price": f"{a['entry_price']:.4f}",
            "resolved_ts": "", "result": "", "roi": "", "clv": "",
        })
        next_id += 1

    # MONITOR-grade: strong-but-gated intel. Telegram + research log only —
    # never a paper trade (the gate said a follow would lose; grading it
    # as one would poison the CLV verdict).
    for a in monitors:
        desc_list = [s["desc"] for s in a["signals"]]
        msg = format_alert({
            "title": a["title"], "platform": a["platform"],
            "market_id": a["id"], "signals": desc_list, "side": a["side"],
            "entry_price": a["entry_price"], "category": a["category"],
            "stake_usd": 0, "hours_to_close": a["hours_to_close"],
            "score": a["score"], "url": a["url"], "calib": calib_active,
            "grade": "monitor", "gate_reasons": a["gate_reasons"],
            "news_note": a.get("news_note"),
        })
        sent = send_telegram(msg)
        print(f"  MONITOR [{a['score']:>3}] {'sent' if sent else 'dry'} :: "
              f"{a['title'][:55]} :: gated: {a['gate_reasons']}")
        state["markets"][a["state_key"]].update({"la": ts, "lg": "M"})
        if a["id"] in research_rows:
            research_rows[a["id"]]["alerted"] = "M"
        to_watch(a, a["score"],
                 [f"MONITOR alert sent; gated: {a['gate_reasons']}"])

    # --- 6. minutes guard (may warn or self-throttle) ---
    outlook = check_actions_budget(meta, ts)

    # --- 7. daily still-alive ping (with health line) ---
    day["runs"] += 1
    day["alerts"] += len(alerts)
    day["watches"] += len(watches)
    day["markets"] = len(kalshi) + len(poly)
    day["errors"] = day.get("errors", 0) + _RUN_STATS["http_errors"]
    if should_ping(meta, ts):
        health = {
            "kalshi": len(kalshi), "poly": len(poly),
            "warm": sum(1 for e in state["markets"].values()
                        if e.get("n", 0) >= CFG["MIN_OBS"]),
        }
        stats = build_day_stats(meta, ledger, calib_active, calib_day, health)
        if outlook:
            stats.update({
                "minutes_used": outlook["used"],
                "minutes_budget": outlook["budget"],
                "minutes_pct": outlook["used_pct"],
                "cadence": CADENCE_NAME[meta["budget"].get("eco_n", 1)],
            })
        ping = format_daily_ping(stats)
        send_telegram(ping)
        print("  daily ping sent")
        meta["last_ping_ts"] = ts
        meta["day"] = {"runs": 0, "alerts": 0, "watches": 0,
                       "markets": day["markets"], "errors": 0}

    # --- 8. persist everything ---
    pruned = prune_state(state, ts)
    meta.update({"last_run_ts": ts, "last_run": iso_utc(ts),
                 "tracked": len(state["markets"]), "mode": mode})
    save_state(state)
    write_ledger(ledger)
    write_report(ledger, ts)
    append_watch_log(watches)
    prices = {market_key(m): m["price"] for m in kalshi + poly}
    filled = update_research_log(list(research_rows.values()), prices, ts)
    print(f"  done: {len(alerts)} alert(s), {len(watches)} watch(es), "
          f"{graded} graded, {pruned} stale market(s) pruned, "
          f"{trade_budget['trades']} trade fetches, "
          f"{len(research_rows)} research row(s) + {filled} forward fill(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
