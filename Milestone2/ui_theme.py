"""
Shared ui_theme.py for FreightQuote AI & FranchiseOps AI
Milestone 2 — refreshed "Maritime Modern" palette: clean, attractive, simple.
Deep navy + teal accent + warm coral highlight, soft shadows (not neo-brutalist).
"""
import streamlit as st

COLORS = {
    "bg_main":       "#f7f9fc",
    "bg_card":       "#ffffff",
    "bg_alt":        "#eef2f9",
    "text_heading":  "#0b2545",
    "text_body":     "#33415c",
    "text_main":     "#33415c",
    "text_muted":    "#6b7789",
    "border":        "#dde3ee",
    "accent":        "#0f6e6e",
    "accent_subtle": "#e5f4f2",
    "accent_text":   "#ffffff",
    "cyan":          "#e6f6f8",
    "pink":          "#fff0ee",
    "coral":         "#ff6b5b",
    "green":         "#20b487",
    "yellow":        "#f5a623",
    "red":           "#e8543f",
}

NEO_BRUTALIST_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: {COLORS["text_body"]};
    background-color: {COLORS["bg_main"]};
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: 'Space Grotesk', sans-serif;
    color: {COLORS["text_heading"]};
    font-weight: 700;
}}

.pn-card {{
    background: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 14px rgba(11, 37, 69, 0.06);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}}
.pn-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(11, 37, 69, 0.10);
}}
.pn-card-alt {{
    background: {COLORS["accent_subtle"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 14px rgba(11, 37, 69, 0.06);
}}

.pn-badge {{
    display: inline-block;
    padding: 4px 12px;
    border: 1.5px solid {COLORS["border"]};
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.02em;
}}
.agent-badge {{
    display: inline-block;
    padding: 5px 14px;
    background: {COLORS["accent"]};
    color: #ffffff;
    border: none;
    border-radius: 20px;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 13px;
    box-shadow: 0 3px 8px rgba(15, 110, 110, 0.35);
}}

/* Streamlit Buttons */
div.stButton > button {{
    background: {COLORS["accent"]} !important;
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    box-shadow: 0 4px 12px rgba(15, 110, 110, 0.28) !important;
    transition: all 0.15s ease !important;
}}
div.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 18px rgba(15, 110, 110, 0.36) !important;
    background: #0c5a5a !important;
}}

/* Streamlit Inputs & Selectboxes */
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {{
    background: #ffffff !important;
    border: 1.5px solid {COLORS["border"]} !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}}

/* Streamlit Tabs */
button[data-baseweb="tab"] {{
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    color: {COLORS["text_muted"]} !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: {COLORS["accent"]} !important;
    border-bottom: 3px solid {COLORS["accent"]} !important;
}}

/* Password strength badges */
.pw-weak {{ color: {COLORS["red"]}; font-weight: 700; }}
.pw-avg  {{ color: {COLORS["yellow"]}; font-weight: 700; }}
.pw-good {{ color: {COLORS["green"]}; font-weight: 700; }}
</style>
"""

def inject_css():
    st.markdown(NEO_BRUTALIST_CSS, unsafe_allow_html=True)

def apply_theme():
    inject_css()

def render_header(title, subtitle="", icon="⚡"):
    inject_css()
    st.markdown(f"""
    <div style="background:{COLORS['bg_card']};border:1px solid {COLORS['border']};border-radius:18px;padding:22px 28px;margin-bottom:24px;box-shadow:0 4px 14px rgba(11,37,69,0.06);">
        <div style="display:flex;align-items:center;gap:16px;">
            <div style="font-size:42px;line-height:1;">{icon}</div>
            <div>
                <h1 style="margin:0;font-size:26px;letter-spacing:-0.5px;">{title}</h1>
                <p style="margin:4px 0 0;color:{COLORS['text_muted']};font-size:14px;">{subtitle}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_card(content, alt=False):
    c_class = "pn-card-alt" if alt else "pn-card"
    st.markdown(f'<div class="{c_class}">{content}</div>', unsafe_allow_html=True)

def risk_badge(text, level="Low"):
    color_map = {"Low": COLORS["green"], "Medium": COLORS["yellow"], "High": COLORS["red"], "Critical": COLORS["red"]}
    c = color_map.get(level, COLORS["cyan"])
    return f'<span class="pn-badge" style="background:{c};color:#ffffff;border-color:{c};">{text}</span>'

def password_strength(pw: str):
    """Returns (label, css_class, blocked: bool) per Milestone 2 Section 6 policy."""
    if not pw or len(pw) < 5:
        return "🔴 Weak", "pw-weak", True
    if len(pw) < 10:
        return "🟡 Average", "pw-avg", False
    return "🟢 Good", "pw-good", False
