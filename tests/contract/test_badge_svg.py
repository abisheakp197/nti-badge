"""Contract tests for /api/badge SVG output."""
from api_handlers.badge import _badge_svg


def test_badge_svg_valid_xml():
    svg = _badge_svg("NTI-1", "not verified", "#555")
    assert svg.startswith("<svg")
    assert svg.endswith("</svg>")
    assert "NTI-1" in svg
    assert "not verified" in svg


def test_badge_svg_has_aria_label():
    svg = _badge_svg("NTI-1", "95/100", "#4ade80")
    assert "aria-label" in svg


def test_badge_svg_no_script_injection():
    svg = _badge_svg("NTI-1", "95/100", "#4ade80")
    assert "<script>" not in svg
