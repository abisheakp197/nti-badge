"""Category 6 API Mismatch Tests: Test README Python API usage examples verbatim."""

from typing import Any

import nti_badge


def test_readme_code_example_verbatim(sample_certificate: dict[str, Any]) -> None:
    # 1. Render an SVG badge
    svg_content = nti_badge.render_badge_svg(
        label="NTI-1",
        value="95/100 Platinum",
        color="#e5e4e2",
        tier_emoji="🏆",
    )
    assert isinstance(svg_content, str)
    assert "<svg" in svg_content

    # Prepare sample cert with valid signature & hash
    signed_cert = nti_badge.sign_badge(dict(sample_certificate))

    # 2. Parse and validate an NTI-Cert/1 certificate
    cert = nti_badge.parse_certificate(signed_cert)
    assert cert["repo"] == "test/repo"

    # 3. Verify signature and cryptographic hash integrity offline
    is_valid_sig = nti_badge.is_valid_signature(cert)
    is_valid_hash = nti_badge.verify_cert_integrity(cert)

    assert is_valid_sig is True
    assert is_valid_hash is True
