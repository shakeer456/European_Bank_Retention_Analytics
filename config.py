# config.py — Central configuration for all constants, colors, and layout

APP_TITLE = "European Bank — Retention Intelligence"
APP_ICON = "🏦"
DATA_PATH = "data/European_Bank.csv"

# ── Brand color palette ───────────────────────────────────────────────────────
PRIMARY = "#6C63FF"   # indigo-violet
SECONDARY = "#FF6584"   # coral-pink
ACCENT_TEAL = "#43E8D8"   # teal
ACCENT_AMBER = "#FFB347"   # amber
ACCENT_GREEN = "#2ECC71"   # emerald
ACCENT_RED = "#E74C3C"   # crimson
ACCENT_BLUE = "#3498DB"   # sky blue
ACCENT_PURPLE = "#9B59B6"   # purple
ACCENT_ORANGE = "#E67E22"   # orange

# Churn status colors
COLOR_RETAINED = "#2ECC71"
COLOR_CHURNED = "#E74C3C"

# Geography palette
COLOR_GEO = {
    "France":  "#6C63FF",
    "Germany": "#FF6584",
    "Spain":   "#FFB347",
}

# Engagement profile palette
COLOR_PROFILE = {
    "Active engaged":         "#2ECC71",
    "Inactive multi-product": "#E74C3C",
    "Active low-product":     "#FFB347",
    "Inactive disengaged":    "#9B59B6",
}

# Product count palette
COLOR_PRODUCTS = ["#6C63FF", "#43E8D8", "#FFB347", "#E74C3C"]

# Sequential scales
SEQ_RED_GREEN = "RdYlGn_r"
SEQ_PURPLE = "Purples"
SEQ_TEAL = "Teal"
SEQ_VIRIDIS = "Viridis"

# ── Plotly layout defaults ────────────────────────────────────────────────────
PLOT_BG = "rgba(0,0,0,0)"
PAPER_BG = "rgba(0,0,0,0)"
FONT_FAM = "Inter, 'Segoe UI', sans-serif"

LAYOUT_DEFAULTS = dict(
    plot_bgcolor=PLOT_BG,
    paper_bgcolor=PAPER_BG,
    font=dict(family=FONT_FAM, size=13, color="#E0E0E0"),
    margin=dict(t=55, b=45, l=45, r=25),
    legend=dict(
        bgcolor="rgba(13,13,26,0.8)",
        bordercolor="rgba(255,255,255,0.15)",
        borderwidth=1,
        font=dict(size=12, color="#FFFFFF"),
    ),
    title=dict(font=dict(size=16, color="#FFFFFF"), x=0.01),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.07)",
        linecolor="rgba(255,255,255,0.15)",
        tickcolor="rgba(255,255,255,0.3)",
        tickfont=dict(color="#B0B0B0"),
        title_font=dict(color="#D0D0D0"),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.07)",
        linecolor="rgba(255,255,255,0.15)",
        tickcolor="rgba(255,255,255,0.3)",
        tickfont=dict(color="#B0B0B0"),
        title_font=dict(color="#D0D0D0"),
    ),
    hoverlabel=dict(
        bgcolor="#1E1E2E",
        bordercolor="#6C63FF",
        font=dict(family=FONT_FAM, size=13, color="#FFFFFF"),
    ),
)
