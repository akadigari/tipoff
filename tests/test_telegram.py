"""Telegram formatter: exact header, one fact per line, phone-skimmable."""

from tipoff import ALERT_HEADER, format_alert


def alert(**overrides):
    base = {
        "title": "Will the Fed cut rates in September?",
        "platform": "kalshi",
        "market_id": "KXFED-25SEP-C",
        "signals": ["volume spike (12x baseline, z=4.1)",
                    "price jump +9c in 1.0h"],
        "side": "yes",
        "entry_price": 0.62,
        "category": "politics",
        "stake_usd": 50.0,
        "hours_to_close": 30.0,
        "score": 72,
        "url": "",
    }
    base.update(overrides)
    return base


def test_header_is_exact_and_leads():
    msg = format_alert(alert())
    assert msg.splitlines()[0] == "🚨🚨 ALERT!!! INSIDER TRADING SCOOP 🚨🚨"
    assert msg.splitlines()[0] == ALERT_HEADER


def test_required_facts_each_on_own_line():
    lines = format_alert(alert()).splitlines()
    assert any("Will the Fed cut rates" in ln for ln in lines)
    assert any(ln.startswith("🔔 Signal:") and "volume spike" in ln
               and "price jump" in ln for ln in lines)
    assert any(ln.startswith("💵 Price: 62c") for ln in lines)
    assert any(ln.startswith("🏷 Category: politics") for ln in lines)
    assert any(ln.startswith("📐 Suggested size: $50") for ln in lines)
    assert any("Window open — verify + move." in ln for ln in lines)


def test_side_is_explicit():
    assert "buy YES" in format_alert(alert(side="yes"))
    assert "buy NO" in format_alert(alert(side="no"))


def test_resolve_window_formats_hours_and_days():
    assert "resolves in 30h" in format_alert(alert(hours_to_close=30.0))
    assert "resolves in 5d" in format_alert(alert(hours_to_close=120.0))


def test_url_included_only_when_present():
    assert "🔗" not in format_alert(alert(url=""))
    msg = format_alert(alert(url="https://polymarket.com/event/foo"))
    assert msg.splitlines()[-1] == "🔗 https://polymarket.com/event/foo"


def test_fits_single_telegram_message():
    long_title = "W" * 300
    msg = format_alert(alert(title=long_title,
                             signals=["volume spike (99x baseline, z=8.0)"] * 4))
    assert len(msg) < 4096  # Telegram sendMessage hard limit
