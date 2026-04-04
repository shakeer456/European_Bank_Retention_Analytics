"""pages/engagement.py — Engagement vs Churn tab"""
from components.charts import (
    bar_churn_by_profile, stacked_active_by_geo,
    bar_churn_active_vs_inactive, funnel_engagement, bar_gender_churn,
)
import pandas as pd
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def render(df: pd.DataFrame):
    st.markdown("""
    <h2 style='margin:0 0 4px 0; color:#fff;'>⚡ Engagement vs Churn</h2>
    <p style='color:#888; margin:0 0 18px 0; font-size:0.9rem;'>
        How member activity, engagement profiles and demographics drive retention.
    </p>""", unsafe_allow_html=True)

    if df.empty:
        st.warning("⚠️ No customers match the current filters.")
        return

    # Insight banner
    active_churn = df[df['IsActiveMember'] == 1]['Exited'].mean() * 100
    inactive_churn = df[df['IsActiveMember'] == 0]['Exited'].mean() * 100
    gap = inactive_churn - active_churn

    # Engagement profile cards
    c1, c2, c3, c4 = st.columns(4)

    total = len(df)
    profiles = {
        'Active engaged':         {'icon': '🟢', 'color': '#2ECC71', 'border': 'rgba(46,204,113,0.5)',  'bg': 'rgba(46,204,113,0.12)'},
        'Inactive multi-product': {'icon': '🔴', 'color': '#E74C3C', 'border': 'rgba(231,76,60,0.5)',   'bg': 'rgba(231,76,60,0.12)'},
        'Active low-product':     {'icon': '🟡', 'color': '#FFB347', 'border': 'rgba(255,183,71,0.5)',  'bg': 'rgba(255,183,71,0.12)'},
        'Inactive disengaged':    {'icon': '🟣', 'color': '#9B59B6', 'border': 'rgba(155,89,182,0.5)',  'bg': 'rgba(155,89,182,0.12)'},
    }
    labels = {
        'Active engaged':         'Active + 2 or more products',
        'Inactive multi-product': 'Inactive high-balance customers',
        'Active low-product':     'Active but low-product customers',
        'Inactive disengaged':    'Inactive + 1 product only',
    }
    req_names = {
        'Active engaged':         'Active Engaged Customers',
        'Inactive multi-product': 'Inactive High-Balance Customers',
        'Active low-product':     'Active Low-Product Customers',
        'Inactive disengaged':    'Inactive Disengaged Customers',
    }

    for col, (profile, style) in zip([c1, c2, c3, c4], profiles.items()):
        sub = df[df['EngagementProfile'] == profile]
        count = len(sub)
        pct = count / total * 100 if total > 0 else 0
        churn = sub['Exited'].mean() * 100 if count > 0 else 0
        col.markdown(f"""
        <div style='background:{style["bg"]}; border:1px solid {style["border"]};
                    border-radius:12px; padding:16px; text-align:center;'>
            <div style='font-size:1.6rem;'>{style["icon"]}</div>
            <div style='font-size:0.72rem; color:#888; text-transform:uppercase;
                        letter-spacing:1px; margin:6px 0 4px;'>
                {req_names[profile]}
            </div>
            <div style='font-size:1.5rem; font-weight:800; color:{style["color"]};'>
                {count:,}
            </div>
            <div style='font-size:0.72rem; color:#888;'>{pct:.1f}% of total</div>
            <div style='font-size:0.75rem; color:{style["color"]}; margin-top:6px;'>
                Churn: <b>{churn:.1f}%</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(108,99,255,0.2),rgba(255,101,132,0.1));
                border:1px solid rgba(108,99,255,0.4); border-radius:12px;
                padding:14px 20px; margin-bottom:20px;'>
        🔎 <b style='color:#6C63FF;'>Engagement Retention Ratio insight:</b>
        <span style='color:#ccc;'>Inactive members churn at </span>
        <b style='color:#E74C3C;'>{inactive_churn:.1f}%</b>
        <span style='color:#ccc;'> vs </span>
        <b style='color:#2ECC71;'>{active_churn:.1f}%</b>
        <span style='color:#ccc;'> for active — a gap of </span>
        <b style='color:#FFB347;'>{gap:+.1f} pp</b>.
        <span style='color:#ccc;'>Re-engagement campaigns can close this gap.</span>
    </div>
    """, unsafe_allow_html=True)

    # Row 1
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(bar_churn_active_vs_inactive(df),
                        use_container_width=True)
    with c2:
        st.plotly_chart(bar_gender_churn(df), use_container_width=True)

    # Row 2
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(bar_churn_by_profile(df), use_container_width=True)
    with c4:
        st.plotly_chart(stacked_active_by_geo(df), use_container_width=True)

    # Funnel full width
    st.plotly_chart(funnel_engagement(df), use_container_width=True)

    # Breakdown table
    with st.expander("📋 Engagement profile breakdown"):
        tbl = (
            df.groupby('EngagementProfile')
            .agg(
                Customers=('CustomerId', 'count'),
                Churn_Rate=('Exited', 'mean'),
                Avg_Balance=('Balance', 'mean'),
                Avg_RSI=('RSI', 'mean'),
                Active_Pct=('IsActiveMember', 'mean'),
            ).reset_index()
        )
        tbl['Churn_Rate'] = (tbl['Churn_Rate'] * 100).round(1)
        tbl['Active_Pct'] = (tbl['Active_Pct'] * 100).round(1)
        tbl['Avg_Balance'] = tbl['Avg_Balance'].round(0)
        tbl['Avg_RSI'] = tbl['Avg_RSI'].round(1)
        tbl.columns = ['Profile', 'Customers', 'Churn Rate (%)',
                       'Avg Balance (€)', 'Avg RSI', 'Active (%)']
        st.dataframe(
            tbl.style.background_gradient(
                subset=['Churn Rate (%)'], cmap='RdYlGn_r'),
            use_container_width=True, hide_index=False,
        )
