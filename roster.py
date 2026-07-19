#!/usr/bin/env python3
"""
Tipoff wallet roster: grade the wallets the scanner keeps flagging, so we
can flip from market-first to wallet-first.

Market-first (what tipoff.py does) has to wait for a market to move before
it looks, which is late by construction. Wallet-first watches people who
have shown the fingerprint and follows THEIR new bets, so the move comes to
us. But a wallet is only worth watching if it is actually good, and the
roster we have was collected by detectors our own self-audit called noise,
so it is enriched for market makers and busy whales, not quiet insiders.

This module sorts that out, and it does the honest thing: it grades every
flagged wallet against data we already own. For each wallet we pull every
research row where that wallet drove the flagged trade, and score it on the
price move that followed, in the wallet's direction. That is not a proxy
for "would following this wallet have paid" — it is exactly that question,
measured on our own collected data with no new API calls.

Two guards make a wallet worth watching:
  - sample size: fewer than MIN_TRADES graded moves and it gets no verdict.
  - luck test: the share of moves that went the wallet's way must beat a
    coin flip by enough that chance is an unlikely explanation. A wallet
    that went 8 for 12 on coin-flip markets has not earned anything.

Nothing here changes live alerting. It reads, ranks, and writes
research/ROSTER.md. Deciding whether to watch the top of the roster live is
a separate, deliberate step.

    python roster.py
"""

from __future__ import annotations

import json
import math
import statistics
import sys
from pathlib import Path

from learn import forward_move, load_rows

ROOT = Path(__file__).resolve().parent
STATE_FILE = ROOT / "state" / "baselines.json"
ROSTER_FILE = ROOT / "research" / "ROSTER.md"

MIN_TRADES = 12         # graded moves before a wallet gets a verdict
FOLLOW_EDGE = 0.010     # avg forward move >= +1.0c to read as followable
LUCK_ALPHA = 0.05       # hit rate must beat a coin flip at this level

# Documented, publicly-reported insider wallets from the backtest episodes
# (docs/BACKTEST.md). Recorded by the pseudonym the reporting used. Most are
# probably burned (insiders rotate addresses; the IAF pair renamed theirs
# when investigators closed in), so these are tripwires, not a strategy, and
# their on-chain addresses still need resolving before they can be watched.
KNOWN_INSIDERS = [
    ("6741", "Nobel Peace Prize 2025 leak (Machado)"),
    ("dirtycup", "Nobel Peace Prize 2025 leak (Machado)"),
    ("Magamyman", "US strike on Iran, Feb 2026 (six fresh wallets)"),
    ("Planktonbets", "US strike on Iran, Feb 2026"),
    ("bigwinner01", "Trump pardons CZ, Oct 2025"),
    ("romanticpaul", "Taylor Swift engagement, Aug 2025"),
    ("ricosuave666", "IAF reservist / Rising Lion, June 2025 (indicted)"),
]


def binomial_luck_p(moved_our_way: int, moved_total: int) -> float:
    """One-sided probability that a coin flip would do this well or better.
    Normal approximation with a continuity correction, which is plenty for a
    screening filter. Returns 1.0 when nothing moved (no evidence either
    way)."""
    if moved_total == 0:
        return 1.0
    mean = moved_total * 0.5
    sd = math.sqrt(moved_total * 0.25)
    if sd == 0:
        return 1.0
    z = (moved_our_way - mean - 0.5) / sd
    return 0.5 * math.erfc(z / math.sqrt(2))


def flag_counts(state_path: Path = STATE_FILE) -> dict:
    """How many times, and which direction, tipoff.py has flagged each
    wallet across scans (from persistent wallet memory)."""
    if not state_path.exists():
        return {}
    try:
        wallets = json.loads(state_path.read_text()).get("wallets", {})
    except json.JSONDecodeError:
        return {}
    return {addr: {"flags": rec.get("n", 1), "dir": rec.get("d")}
            for addr, rec in wallets.items()}


def grade_wallets(rows: list[dict], state: dict) -> list[dict]:
    """One graded record per wallet that ever drove a flagged trade."""
    moves: dict[str, list[float]] = {}
    markets: dict[str, set] = {}
    for row in rows:
        wallet = row.get("wallet")
        if not wallet:
            continue
        markets.setdefault(wallet, set()).add(row.get("market_id"))
        move = forward_move(row)
        if move is not None:
            moves.setdefault(wallet, []).append(move)

    graded = []
    for wallet, vals in moves.items():
        n = len(vals)
        up = sum(1 for v in vals if v > 0.0005)
        down = sum(1 for v in vals if v < -0.0005)
        moved = up + down
        avg = statistics.mean(vals)
        luck_p = binomial_luck_p(up, moved)
        graded.append({
            "wallet": wallet,
            "n": n,
            "avg": avg,
            "median": statistics.median(vals),
            "hit_rate": (up / moved) if moved else 0.0,
            "luck_p": luck_p,
            "markets": len(markets.get(wallet, set())),
            "flags": state.get(wallet, {}).get("flags", 0),
            "verdict": wallet_verdict(n, avg, luck_p),
        })
    # wallets flagged but with no filled forward data yet still deserve a row
    for wallet in markets:
        if wallet not in moves:
            graded.append({
                "wallet": wallet, "n": 0, "avg": 0.0, "median": 0.0,
                "hit_rate": 0.0, "luck_p": 1.0,
                "markets": len(markets[wallet]),
                "flags": state.get(wallet, {}).get("flags", 0),
                "verdict": "INSUFFICIENT DATA",
            })
    graded.sort(key=lambda g: (-g["avg"], -g["n"]))
    return graded


def wallet_verdict(n: int, avg: float, luck_p: float) -> str:
    """A wallet is only WATCH-worthy if it has enough graded moves, a
    positive average, AND a hit rate that beats a coin flip. All three, or
    it is noise."""
    if n < MIN_TRADES:
        return "INSUFFICIENT DATA"
    if avg >= FOLLOW_EDGE and luck_p < LUCK_ALPHA:
        return "WATCH (beats luck)"
    if avg >= FOLLOW_EDGE:
        return "PROMISING (edge, luck not ruled out)"
    if avg <= -FOLLOW_EDGE:
        return "FADE (bets the wrong way)"
    return "NOISE (busy, not sharp)"


def build_roster(graded: list[dict], generated_at: str) -> str:
    watch = [g for g in graded if g["verdict"].startswith("WATCH")]
    promising = [g for g in graded if g["verdict"].startswith("PROMISING")]
    graded_n = [g for g in graded if g["n"] >= MIN_TRADES]

    lines = [
        "# Wallet roster",
        "",
        f"_Auto-generated {generated_at}. {len(graded)} flagged wallets,"
        f" {len(graded_n)} with enough graded trades to judge,"
        f" {len(watch)} that beat a coin flip._",
        "",
        "Each wallet is graded on the price move that followed its flagged",
        "trades, in the wallet's own direction, using data the scanner",
        "already collected. A wallet earns WATCH only with at least",
        f"{MIN_TRADES} graded moves, a positive average, and a hit rate that",
        "beats a coin flip (p < 0.05). Averages are in cents of probability.",
        "",
        "**Read this before trusting the list.** These wallets were surfaced",
        "by detectors the self-audit (LEARNING.md) calls noise, so the pool",
        "leans toward market makers and busy whales, not quiet insiders. A",
        "high flag count is a reason for suspicion, not trust: real insiders",
        "in the documented cases traded once, in one market, then vanished.",
        "The grading below is exactly what separates the two.",
        "",
    ]

    def table(title, rows_):
        out = [f"## {title}", ""]
        if not rows_:
            out += ["_None yet._", ""]
            return out
        out += ["| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |",
                "|---|---|---|---|---|---|---|---|"]
        for g in rows_:
            out.append(
                f"| `{g['wallet'][:12]}...` | {g['n']} | {g['avg'] * 100:+.2f}c"
                f" | {g['hit_rate'] * 100:.0f}% | {g['luck_p']:.2f}"
                f" | {g['markets']} | {g['flags']} | {g['verdict']} |")
        out.append("")
        return out

    lines += table("Watch list (earned it)", watch)
    lines += table("Promising (edge, needs more data to rule out luck)",
                   promising[:15])
    lines += table("Top of the pack by average (all verdicts)", graded_n[:20])

    lines += [
        "## Documented known insiders (Phase B watch targets)",
        "",
        "Publicly-reported insider wallets from the backtest episodes,"
        " by the pseudonym the reporting used. On-chain addresses still need"
        " resolving before they can be watched live, and most are likely"
        " burned (insiders rotate addresses). Tripwires, not a strategy.",
        "",
        "| Pseudonym | Episode |",
        "|---|---|",
    ]
    lines += [f"| {name} | {episode} |" for name, episode in KNOWN_INSIDERS]
    lines += [
        "",
        "## Next step",
        "",
        "If the watch list stays empty or tiny once normal mode fills the",
        "data, wallet-first is not worth the API budget and we do not build",
        "Phase B. If real names keep earning WATCH, Phase B polls those",
        "wallets every run and alerts the moment they open a new position,",
        "before the market is anomalous.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    from datetime import datetime, timezone
    rows = load_rows()
    if not rows:
        print("no research data yet, nothing to grade")
        return 0
    graded = grade_wallets(rows, flag_counts())
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ROSTER_FILE.parent.mkdir(parents=True, exist_ok=True)
    ROSTER_FILE.write_text(build_roster(graded, stamp))
    watch = sum(1 for g in graded if g["verdict"].startswith("WATCH"))
    print(f"roster written to {ROSTER_FILE.name}"
          f" ({len(graded)} wallets, {watch} on the watch list)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
