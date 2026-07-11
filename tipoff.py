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

KALSHI_BASE = "https://api.elections.kalshi.com/trade-api/v2"
GAMMA_BASE = "https://gamma-api.polymarket.com"
DATA_API_BASE = "https://data-api.polymarket.com"

CATEGORIES = ("entertainment", "politics", "sports", "crypto", "other")

LEDGER_COLUMNS = [
    "id", "ts", "platform", "market_id", "title", "category", "side",
    "entry_price", "stake_usd", "score", "signals", "hours_to_close",
    "mode", "status", "last_price", "resolved_ts", "result", "roi", "clv",
]

WATCH_COLUMNS = [
    "ts", "platform", "market_id", "title", "category", "score",
    "signals", "mode", "reasons",
]

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
                "event": slug or m["conditionId"],
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
#   "m":   EWMA of hourly volume rate   "s2": EWMA variance of that rate
#   "mv":  recent |price moves| (<= MAX_MOVE_WINDOW)
#   "la":  last alert ts (cooldown)     "c":  category
# }
# state["meta"] holds first_run_ts (calibration clock), last_ping_ts and the
# rolling "day" counters for the daily ping.


def market_key(m: dict) -> str:
    return f'{m["platform"]}:{m["id"]}'


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text())
            state.setdefault("markets", {})
            state.setdefault("meta", {})
            return state
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

    rate_upd = rate
    if entry["n"] >= cfg["MIN_OBS"] and entry["m"] > 0:
        rate_upd = min(rate, entry["m"] * cfg["BASELINE_WINSOR_MULT"])

    alpha = cfg["EWMA_ALPHA"]
    if entry["n"] == 0:
        entry["m"], entry["s2"] = rate_upd, 0.0
    else:
        delta = rate_upd - entry["m"]
        entry["m"] += alpha * delta
        entry["s2"] = (1 - alpha) * (entry["s2"] + alpha * delta * delta)
    entry["n"] += 1
    entry["mv"] = (entry["mv"] + [round(abs(dp), 4)])[-cfg["MAX_MOVE_WINDOW"]:]
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
    """Hourly volume rate >= VOL_SPIKE_MULT x the market's own baseline."""
    if obs.get("dt_h") is None or obs["dt_h"] > cfg["MAX_GAP_HOURS"]:
        return None
    if obs["n"] < cfg["MIN_OBS"]:
        return None  # warm-up: not enough history to call anything a spike
    if obs["rate"] * obs["dt_h"] < cfg["VOL_SPIKE_MIN_ABS"]:
        return None  # tiny absolute delta; multiples of dust are noise
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


def detect_price_jump(obs: dict, hours_to_close: float,
                      cfg: dict = CFG) -> dict | None:
    """Sudden price move vs the market's own recent-move baseline.

    Guards:
      - scheduled-news proxy: a jump within SCHEDULED_NEWS_MIN_H of
        resolution is presumed to be the event itself happening, not
        informed money arriving early;
      - phantom guard: a "jump" with almost no volume behind it is a
        re-quoted book (one MM moving), not news.
    """
    if obs.get("dt_h") is None or obs["dt_h"] > cfg["PRICE_JUMP_MAX_AGE_H"]:
        return None
    if hours_to_close < cfg["SCHEDULED_NEWS_MIN_H"]:
        return None
    if obs["rate"] * obs["dt_h"] < cfg["JUMP_MIN_VOL_DELTA"]:
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
        "points": min(35, round(320 * abs(dp))),
        "direction": 1 if dp > 0 else -1,
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
    buys_yes = (t.get("side") == "BUY") == (t.get("outcomeIndex") == 0)
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


def fresh_wallet_signal(notional: float) -> dict:
    points = 15 + (10 if notional >= 5000 else 0)
    return {"type": "fresh_wallet",
            "desc": f"fresh wallet (<{CFG['FRESH_WALLET_MAX_AGE_D']:.0f}d old)"
                    f" loading up",
            "points": points}


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
    na = {t for t in ta if t.isdigit()}
    nb = {t for t in tb if t.isdigit()}
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
    for c in sorted(cands, key=lambda x: x["score"], reverse=True):
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
    """'yes' or 'no' — trust directional signals, fall back to price drift."""
    directional = [s["direction"] for s in signals if "direction" in s]
    if directional:
        return "yes" if sum(directional) >= 0 else "no"
    return "yes" if price_drift >= 0 else "no"


def followability_gate(entry_price: float, signal_price: float,
                       depth_usd: float, hours_to_close: float,
                       cfg: dict = CFG,
                       min_depth: float | None = None) -> tuple[bool, list[str]]:
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


def format_alert(alert: dict) -> str:
    """Phone-skimmable alert. `alert` needs: title, platform, market_id,
    signals (list of desc strings), side, entry_price, category, stake_usd,
    hours_to_close, score, url, and optionally calib (bool)."""
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
CADENCE_CRON = {1: "7 * * * *", 2: "7 */2 * * *",
                3: "7 */3 * * *", 6: "7 */6 * * *"}
CADENCE_NAME = {1: "hourly", 2: "every 2h", 3: "every 3h", 6: "every 6h"}


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
    return re.sub(r'- cron: "[^"]*"',
                  f'- cron: "{CADENCE_CRON[eco_n]}"', workflow_text, count=1)


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
                send_telegram("⛽ New month — Tipoff back to hourly scans.")
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
    for r in rows:  # schema migration: rows written before the mode column
        r.setdefault("mode", "normal")
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
        return
    won = (result == row["side"])
    row["status"] = "won" if won else "lost"
    row["roi"] = f"{((1.0 - entry) / entry) if won else -1.0:.4f}"
    last = safe_float(row.get("last_price"), entry)
    row["clv"] = f"{last - entry:.4f}"


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
        writer = csv.DictWriter(fh, fieldnames=WATCH_COLUMNS, extrasaction="ignore")
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
                    signals.append(fresh_wallet_signal(big["notional"]))
            thin = thin_market_signal(m["vol24"])
            if thin:
                signals.append(thin)
    return entry, signals, obs


def build_day_stats(meta: dict, ledger: list[dict], calib_active: bool,
                    calib_day: int) -> dict:
    day = meta.get("day", {})
    graded_rows = [r for r in ledger if r["status"] in ("won", "lost")]
    return {
        "runs": day.get("runs", 0),
        "markets": day.get("markets", 0),
        "alerts": day.get("alerts", 0),
        "watches": day.get("watches", 0),
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
                                  "markets": 0})
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

    # --- 3. scan every market, collect signal-bearing candidates ---
    trade_budget = {"trades": 0, "wallets": 0}
    candidates = []
    for m in kalshi + poly:
        key = market_key(m)
        entry, signals, obs = scan_market(m, state["markets"].get(key), ts,
                                          trade_budget)
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

    for c in candidates:
        score = score_signals(c["signals"])
        side = choose_side(c["signals"], c["obs"].get("dp", 0.0))
        entry_price = c["yes_ask"] if side == "yes" else c["no_ask"]
        signal_price = side_price(side, c["price"])
        depth = c["depth_yes_usd"] if side == "yes" else c["depth_no_usd"]
        hours_to_close = ((c["close_ts"] or ts) - ts) / 3600.0
        min_depth = (CFG["GATE_MIN_LIQUIDITY_USD"] if c["platform"] == "poly"
                     else CFG["GATE_MIN_DEPTH_USD"])
        passes, reasons = followability_gate(
            entry_price, signal_price, depth, hours_to_close,
            min_depth=min_depth)

        if score < alert_score:
            passes = False
            reasons = reasons + [f"score {score} < {alert_score}"]
        if c["id"] in holding:
            passes = False
            reasons = reasons + ["already holding (open ledger row)"]
        last_alert = safe_float(state["markets"][c["state_key"]].get("la"))
        if passes and ts - last_alert < cooldown_h * 3600:
            passes, reasons = False, ["re-alert cooldown"]

        if passes:
            alertable.append({**c, "score": score, "side": side,
                              "entry_price": entry_price, "depth": depth,
                              "hours_to_close": hours_to_close})
        else:
            to_watch(c, score, reasons)

    kept, duplicates = dedup_alerts(alertable)
    for c, reason in duplicates:
        to_watch(c, c["score"], [reason])
    for c in kept[max_alerts:]:
        to_watch(c, c["score"], ["alert cap for this run"])
    alerts = kept[:max_alerts]

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
        })
        sent = send_telegram(msg)
        print(f"  ALERT [{a['score']:>3}] {'sent' if sent else 'dry'} :: "
              f"{a['title'][:55]} ({a['side']} @ {a['entry_price']:.2f})")
        state["markets"][a["state_key"]]["la"] = ts
        ledger.append({
            "id": str(next_id), "ts": iso_utc(ts), "platform": a["platform"],
            "market_id": a["id"], "title": a["title"],
            "category": a["category"], "side": a["side"],
            "entry_price": f"{a['entry_price']:.4f}",
            "stake_usd": f"{stake:.0f}", "score": str(a["score"]),
            "signals": " + ".join(desc_list),
            "hours_to_close": f"{a['hours_to_close']:.1f}", "mode": mode,
            "status": "open", "last_price": f"{a['entry_price']:.4f}",
            "resolved_ts": "", "result": "", "roi": "", "clv": "",
        })
        next_id += 1

    # --- 6. minutes guard (may warn or self-throttle) ---
    outlook = check_actions_budget(meta, ts)

    # --- 7. daily still-alive ping ---
    day["runs"] += 1
    day["alerts"] += len(alerts)
    day["watches"] += len(watches)
    day["markets"] = len(kalshi) + len(poly)
    if should_ping(meta, ts):
        stats = build_day_stats(meta, ledger, calib_active, calib_day)
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
                       "markets": day["markets"]}

    # --- 8. persist everything ---
    pruned = prune_state(state, ts)
    meta.update({"last_run_ts": ts, "last_run": iso_utc(ts),
                 "tracked": len(state["markets"]), "mode": mode})
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
