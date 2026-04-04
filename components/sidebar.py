"""components/sidebar.py — Sidebar filters with styled UI"""
import base64
import pandas as pd
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_logo():
    try:
        path = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "static", "ECB_2.jpg")
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""


def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    logo = get_logo()
    img_tag = f"<img src='data:image/png;base64,{logo}' style='width:206px;height:206px;object-fit:contain;'>" if logo else "<span style='font-size:2.2rem;'>🏦</span>"
    st.sidebar.markdown(f"""
    <div style='text-align:center; padding: 10px 0 18px 0;'>
        {img_tag}<br>
       
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### 🔎 Filters")

    # Geography
    all_geo = sorted(df['Geography'].unique())
    geo = st.sidebar.multiselect("🌍 Geography", all_geo, default=all_geo)

    # Gender
    all_gender = sorted(df['Gender'].unique())
    gender = st.sidebar.multiselect("👤 Gender", all_gender, default=all_gender)

    # Age
    age_min, age_max = int(df['Age'].min()), int(df['Age'].max())
    age_range = st.sidebar.slider(
        "🎂 Age range", age_min, age_max, (age_min, age_max))

    # Products
    prod_min = int(df['NumOfProducts'].min())
    prod_max = int(df['NumOfProducts'].max())
    products = st.sidebar.slider(
        "📦 # of products", prod_min, prod_max, (prod_min, prod_max))

    # Balance
    bal_max = int(df['Balance'].max())
    bal_range = st.sidebar.slider(
        "💰 Balance range (€)", 0, bal_max, (0, bal_max), step=5_000)

    # Tenure
    ten_min, ten_max = int(df['Tenure'].min()), int(df['Tenure'].max())
    tenure = st.sidebar.slider(
        "📅 Tenure (years)", ten_min, ten_max, (ten_min, ten_max))

    st.sidebar.markdown("### ⚙️ Member flags")
    active_only = st.sidebar.checkbox("Active members only", value=False)
    crcard_only = st.sidebar.checkbox("Credit card holders only", value=False)
    churned_only = st.sidebar.checkbox("Churned customers only", value=False)

    # ── Apply filters ─────────────────────────────────────────────────────
    mask = (
        df['Geography'].isin(geo)
        & df['Gender'].isin(gender)
        & df['Age'].between(*age_range)
        & df['NumOfProducts'].between(*products)
        & df['Balance'].between(*bal_range)
        & df['Tenure'].between(*tenure)
    )
    if active_only:
        mask &= df['IsActiveMember'] == 1
    if crcard_only:
        mask &= df['HasCrCard'] == 1
    if churned_only:
        mask &= df['Exited'] == 1

    filtered = df[mask]

    st.sidebar.markdown("---")
    total = len(df)
    shown = len(filtered)
    pct = shown / total * 100 if total > 0 else 0
    churn_r = filtered['Exited'].mean() * 100 if shown > 0 else 0

    st.sidebar.markdown(f"""
    <div style='background:rgba(108,99,255,0.12); border:1px solid rgba(108,99,255,0.3);
                border-radius:10px; padding:12px 14px; font-size:0.82rem;'>
        <b style='color:#6C63FF;'>📊 Dataset snapshot</b><br><br>
        <span style='color:#ccc;'>Showing:</span>
        <b style='color:#fff;'>{shown:,}</b>
        <span style='color:#888;'> / {total:,} ({pct:.1f}%)</span><br>
        <span style='color:#ccc;'>Churn rate:</span>
        <b style='color:#FF6584;'>{churn_r:.1f}%</b>
    </div>
    """, unsafe_allow_html=True)

    return filtered
