"""Resolution pass vs the 2026-08 Gamma API listing behavior.

Around early August 2026, gamma-api.polymarket.com/markets stopped
returning closed markets in list responses unless the query carries
closed=true (verified live 2026-08-25: the exact production query for a
resolved July market returned [], and the same query plus closed=true
returned it with umaResolutionStatus=resolved). The old resolution pass
sent no closed param, so every resolved Polymarket position fell into
the `if not m: continue` branch and stayed open forever: 480 open rows,
3 graded, by 2026-08-25.

These tests pin the fixed contract: resolved markets are still found
and graded, and still-open markets keep getting their closing-line
refresh from the default listing.
"""

import tipoff

TS = 1_764_000_000.0

# One resolved market (hidden by the default filter) and one still open.
GAMMA_MARKETS = [
    {
        "conditionId": "0xresolved",
        "closed": True,
        "umaResolutionStatus": "resolved",
        "outcomePrices": '["1", "0"]',
    },
    {
        "conditionId": "0xopen",
        "closed": False,
        "umaResolutionStatus": "",
        "outcomePrices": '["0.43", "0.57"]',
    },
]


def fake_gamma(url, params=None, retries=2):
    """Behave exactly like the post-change Gamma listing: closed markets
    only appear when the query says closed=true."""
    assert "gamma" in url
    pairs = list(params) if isinstance(params, list) else list((params or {}).items())
    ids = [v for k, v in pairs if k == "condition_ids"]
    closed = next((str(v).lower() for k, v in pairs if k == "closed"), None)
    out = []
    for m in GAMMA_MARKETS:
        if m["conditionId"] not in ids:
            continue
        if closed == "true" and not m["closed"]:
            continue
        if closed in (None, "false") and m["closed"]:
            continue  # the 2026-08 default: closed markets are invisible
        out.append(m)
    return out


def open_row(market_id, entry="0.7900", last="0.9995"):
    return {
        "platform": "poly", "market_id": market_id, "status": "open",
        "side": "yes", "entry_price": entry, "last_price": last,
        "resolved_ts": "", "result": "", "roi": "", "clv": "", "read": "",
    }


def test_grades_resolved_poly_market_hidden_by_default_filter(monkeypatch):
    monkeypatch.setattr(tipoff, "http_get_json", fake_gamma)
    row = open_row("0xresolved")

    graded = tipoff.resolve_open_positions([row], TS)

    assert graded == 1
    assert row["result"] == "yes"
    assert row["status"] == "won"


def test_open_poly_market_still_refreshes_last_price(monkeypatch):
    monkeypatch.setattr(tipoff, "http_get_json", fake_gamma)
    row = open_row("0xopen", last="")

    graded = tipoff.resolve_open_positions([row], TS)

    assert graded == 0
    assert row["status"] == "open"
    assert row["last_price"] == "0.4300"
