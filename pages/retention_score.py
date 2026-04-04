"""pages/retention_score.py — Retention Strength Scoring tab"""
from components.charts import (
    gauge_rsi, scatter_rsi_age,
    bar_rsi_by_profile, histogram_rsi, radar_profile, sticky_customer_summary, bar_churn_stability_tiers,
)
import pandas as pd
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def render(df: pd.DataFrame):
    st.markdown("""
    <h2 style='margin:0 0 4px 0; color:#fff;'>💪 Retention Strength Scoring</h2>
    <p style='color:#888; margin:0 0 18px 0; font-size:0.9rem;'>
        RSI — a composite 0–100 score combining activity, products, tenure, card &amp; balance.
    </p>""", unsafe_allow_html=True)

    # RSI legend
    st.markdown("### 🎯 Engagement Thresholds Linked to Retention")
    st.markdown("""
    <div style='display:flex; gap:12px; margin-bottom:20px; flex-wrap:wrap;'>
        <div style='background:rgba(231,76,60,0.15); border:1px solid rgba(231,76,60,0.4);
                    border-radius:8px; padding:8px 16px; font-size:0.82rem; color:#ffffff;'>
            🔴 <b style='color:#E74C3C;'>0–40</b> &nbsp;High flight risk
        </div>
        <div style='background:rgba(255,183,71,0.15); border:1px solid rgba(255,183,71,0.4);
                    border-radius:8px; padding:8px 16px; font-size:0.82rem; color:#ffffff;'>
            🟡 <b style='color:#FFB347;'>40–65</b> &nbsp;Needs nurturing
        </div>
        <div style='background:rgba(46,204,113,0.15); border:1px solid rgba(46,204,113,0.4);
                    border-radius:8px; padding:8px 16px; font-size:0.82rem; color:#ffffff;'>
            🟢 <b style='color:#2ECC71;'>65–100</b> &nbsp;Loyal — retain &amp; upsell
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.warning("⚠️ No customers match the current filters.")
        return

    avg_rsi = df['RSI'].mean()

    # Gauge (full width)
    st.plotly_chart(gauge_rsi(avg_rsi), use_container_width=True)

    # Row 1
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(bar_rsi_by_profile(df), use_container_width=True)
    with c2:
        st.plotly_chart(histogram_rsi(df), use_container_width=True)

    # Scatter full width
    st.plotly_chart(scatter_rsi_age(df), use_container_width=True)

    # Radar full width
    st.plotly_chart(radar_profile(df), use_container_width=True)

   # RSI tier breakdown
    st.markdown("### 📊 Churn Stability Across Engagement Tiers")
    st.plotly_chart(bar_churn_stability_tiers(df), use_container_width=True)
    with st.expander("📋 RSI tier breakdown — click to expand"):
        df2 = df.copy()
        df2['RSI Tier'] = pd.cut(
            df2['RSI'],
            bins=[-1, 40, 65, 101],
            labels=['🔴 High risk (0–40)', '🟡 Moderate (40–65)',
                    '🟢 Loyal (65–100)'],
        )
        tbl = (
            df2.groupby('RSI Tier', observed=True)
            .agg(
                Customers=('CustomerId', 'count'),
                Churn_Rate=('Exited', 'mean'),
                Avg_Balance=('Balance', 'mean'),
                Avg_Products=('NumOfProducts', 'mean'),
            ).reset_index()
        )
        tbl['Churn_Rate'] = (tbl['Churn_Rate'] * 100).round(1)
        tbl['Avg_Balance'] = tbl['Avg_Balance'].round(0)
        tbl['Avg_Products'] = tbl['Avg_Products'].round(2)
        tbl.columns = ['RSI Tier', 'Customers', 'Churn Rate (%)',
                       'Avg Balance (€)', 'Avg Products']
        st.dataframe(
            tbl.style.background_gradient(
                subset=['Churn Rate (%)'], cmap='RdYlGn_r'),
            use_container_width=True, hide_index=False,
        )

    # Sticky customer callout
    sticky = df[df['RSI'] >= 65]
    st.markdown("### 👑 Sticky Customer Profiles (RSI ≥ 65)")
    st.plotly_chart(sticky_customer_summary(df), use_container_width=True)
    if len(sticky) > 0:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,rgba(46,204,113,0.2),rgba(67,232,216,0.1));
                    border:1px solid rgba(46,204,113,0.4); border-radius:12px;
                    padding:14px 20px; margin-top:16px;'>
            ✅ <b style='color:#2ECC71;'>{len(sticky):,} sticky customers defined as RSI ≥ 65</b>
            <span style='color:#ccc;'> (RSI ≥ 65) — churn rate:
            <b style='color:#E74C3C;'>{sticky['Exited'].mean()*100:.1f}%</b> |
            avg balance: <b style='color:#43E8D8;'>€{sticky['Balance'].mean():,.0f}</b> |
            avg products: <b style='color:#FFB347;'>{sticky['NumOfProducts'].mean():.1f}</b>
            </span>
        </div>
        """, unsafe_allow_html=True)
