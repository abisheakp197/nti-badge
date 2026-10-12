"""Badge SVG rendering logic."""


def render_badge_svg(label: str, value: str, color: str, tier_emoji: str = "") -> str:
    """Render a standalone SVG compliance badge."""
    label_w = 120
    value_w = 140
    total = label_w + value_w
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="22" role="img" aria-label="{label}: {value}">
  <title>{label}: {value}</title>
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r"><rect width="{total}" height="22" rx="4" fill="#fff"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="{label_w}" height="22" fill="#0a0a0a"/>
    <rect x="{label_w}" width="{value_w}" height="22" fill="{color}"/>
    <rect width="{total}" height="22" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,sans-serif" font-size="11">
    <text x="{label_w // 2}" y="15">NTI-1 {tier_emoji}</text>
    <text x="{label_w + value_w // 2}" y="15">{value}</text>
  </g>
</svg>'''
