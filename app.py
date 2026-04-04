"""
app.py — Main entry point
Run:  streamlit run app.py
"""
import base64
from config import APP_TITLE, APP_ICON, DATA_PATH
from components.sidebar import render_sidebar
from utils import load_and_engineer
import pandas as pd
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global dark theme CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Hide auto-generated page nav in sidebar ── */
[data-testid="stSidebarNav"] { display: none !important; }

# /* ── Kill the white top toolbar / header bar ── */
# [data-testid="stHeader"],
# header[data-testid="stHeader"],
# .stAppHeader,
# #stDecoration { 
#     background: #0D0D1A !important;
#     border-bottom: 1px solid rgba(108,99,255,0.15) !important;
# }
            
/* Completely remove header visual */
[data-testid="stHeader"] {
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
    position: relative !important;
}

/* Remove top decoration line */
#stDecoration {
    display: none !important;
}

/* ── Base dark background ── */
.stApp {
    background: linear-gradient(135deg, #0D0D1A 0%, #111128 50%, #0D0D1A 100%);
    background-attachment: fixed;
}

/* ── Block container — remove top gap left by hidden header ── */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 6rem !important;
    max-width: 100% !important;
}

/* ── Sidebar dark ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12122A 0%, #0D0D1A 100%) !important;
    border-right: 1px solid rgba(108,99,255,0.2);
}
[data-testid="stSidebar"] * { color: #D0D0D0 !important; }

/* ── Filter tag chips — #FF4B4B fill, white text ── */
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: #FF4B4B !important;
    border: none !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] span,
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] svg {
    color: #ffffff !important;
    fill: #ffffff !important;
}

/* ── Slider track & thumb — red to match tags ── */
[data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: #FF4B4B !important;
    border-color: #FF4B4B !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] div[data-testid="stSliderThumb"] {
    background: #FF4B4B !important;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: #888 !important;
    font-size: 14px;
    font-weight: 500;
    padding: 8px 18px;
    transition: all 0.2s;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6C63FF, #FF6584) !important;
    color: #fff !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="stMetricValue"] { color: #fff !important; font-size: 1.5rem !important; }
[data-testid="stMetricLabel"] { color: #888 !important; }

/* ── Expander ── */
# [data-testid="stExpander"] {
#     background: rgba(255,255,255,0.03) !important;
#     border: 1px solid rgba(255,255,255,0.08) !important;
#     border-radius: 10px !important;
# }


/* ── Dataframe ── */
# [data-testid="stDataFrame"] {
#     border-radius: 10px !important;
#     overflow: hidden;
# }
            


/* ── Expander ── */
[data-testid="stExpander"] {
    background: #12122A !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    background: #12122A !important;
    color: #ffffff !important;
}
[data-testid="stExpander"] summary:hover {
    background: #1E1E3A !important;
}
[data-testid="stExpanderDetails"] {
    background: #12122A !important;
}
details[data-testid="stExpander"] > div {
    background: #12122A !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden;
    background: #12122A !important;
}
[data-testid="stDataFrame"] > div {
    background: #12122A !important;
}


/* ── Buttons ── */
.stDownloadButton button, .stButton button {
    background: linear-gradient(135deg, #6C63FF33 0%, #FF658433 50%, #43E8D833 100%);
    border: none !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: opacity 0.2s !important;
}
.stDownloadButton button:hover, .stButton button:hover { opacity: 0.85 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
::-webkit-scrollbar-thumb { background: #FF4B4B99; border-radius: 3px; }

/* ── Text ── */
h1, h2, h3, h4 { color: #fff !important; }
p, span, label { color: #ccc; }

/* ── Warning / info boxes ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left-width: 4px !important;
}

/* ── Checkbox ── */
[data-testid="stCheckbox"] label { color: #ccc !important; }

/* ── Multiselect dropdown control ── */
[data-baseweb="select"] {
    background: rgba(255,255,255,0.05) !important;
    border-color: rgba(255,75,75,0.4) !important;
}
            

</style>
""", unsafe_allow_html=True)

# ── Header banner ─────────────────────────────────────────────────────────────


def get_svg(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""


_here = os.path.dirname(os.path.abspath(__file__))
svg_path = os.path.join(_here, "static", "ECB.png")
svg_b64 = get_svg(svg_path)
svg_img = f"<img src='data:image/png;base64,{svg_b64}' style='width:56px;height:56px;object-fit:contain;'>" if svg_b64 else "<span style='font-size:2.4rem;'>🏦</span>"

st.markdown(f"""
<div style='
    background: linear-gradient(135deg, rgba(108,99,255,0.25) 0%,
                rgba(255,101,132,0.15) 50%, rgba(67,232,216,0.1) 100%);
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 16px;
    padding: 22px 28px;
    margin-top: 38px;
    margin-bottom: 24px;
    width: 100%;
    box-sizing: border-box;
'>
    <div style='display:flex; align-items:center; gap:14px;'>
        {svg_img}
        <div>
            <div style='font-size:1.55rem; font-weight:800; color:#fff;
                        letter-spacing:0.3px; line-height:1.2;'>
                Customer Engagement & Product Utilization Analytics for Retention Strategy
            </div>
            <div style='font-size:0.82rem; color:#888; margin-top:4px;'>
                Customer Engagement &amp; Product Utilization Analytics ·
                <span style='color:#6C63FF;'>10,000 customers</span> ·
                European Central Bank Dataset
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────────────────────


@st.cache_data(show_spinner="⚙️ Loading and engineering features…")
def get_data(path: str) -> pd.DataFrame:
    return load_and_engineer(path)


_here = os.path.dirname(os.path.abspath(__file__))
_data_path = os.path.join(_here, DATA_PATH)

try:
    df_raw = get_data(_data_path)
except FileNotFoundError:
    st.error(
        f"Dataset not found at `{_data_path}`. Place your CSV at `data/European_Bank.csv`.")
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
df = render_sidebar(df_raw)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Overview",
    "⚡  Engagement",
    "📦  Products",
    "⚠️  Premium Risk",
    "💪  Retention Score",
])

with tab1:
    from pages.overview import render
    render(df)

with tab2:
    from pages.engagement import render as re
    re(df)

with tab3:
    from pages.products import render as rp
    rp(df)

with tab4:
    from pages.premium_risk import render as rr
    rr(df)

with tab5:
    from pages.retention_score import render as rs
    rs(df)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:20px 0 8px; color:#aaa; font-size:0.75rem;
            border-top:1px solid rgba(255,255,255,0.06); margin-top:32px;
            margin-bottom: 2rem;'>
    European Bank Retention Analytics · 2025 <br>
    Created by <span style='color:#6C63FF;'>Shakeer</span> 
    <span style='color:#FF6584;'>Shaik</span>
</div>
""", unsafe_allow_html=True)
