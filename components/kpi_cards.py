"""components/kpi_cards.py — Beautiful KPI metric cards"""
import pandas as pd
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def compute_kpis(df: pd.DataFrame) -> dict:
    total = len(df)
    if total == 0:
        return {k: 0 for k in ["churn_rate", "engagement_gap",
                               "product_depth", "premium_risk_pct", "avg_rsi", "crcard_stickiness"]}

    churn_rate = df['Exited'].mean() * 100
    active = df[df['IsActiveMember'] == 1]
    inactive = df[df['IsActiveMember'] == 0]
    act_churn = active['Exited'].mean() * 100 if len(active) > 0 else 0
    inact_churn = inactive['Exited'].mean() * 100 if len(inactive) > 0 else 0
    engagement_gap = inact_churn - act_churn
    product_depth = df['NumOfProducts'].mean()
    premium = df[df['Balance'] >= df['Balance'].quantile(0.75)]
    premium_risk = (premium['IsActiveMember'] ==
                    0).mean() * 100 if len(premium) > 0 else 0
    avg_rsi = df['RSI'].mean()
    crcard = df[df['HasCrCard'] == 1]
    no_crcard = df[df['HasCrCard'] == 0]
    crcard_churn = crcard['Exited'].mean() * 100 if len(crcard) > 0 else 0
    nocard_churn = no_crcard['Exited'].mean(
    ) * 100 if len(no_crcard) > 0 else 0
    crcard_sticky = nocard_churn - crcard_churn

    return {
        "churn_rate":       churn_rate,
        "engagement_gap":   engagement_gap,
        "product_depth":    product_depth,
        "premium_risk_pct": premium_risk,
        "avg_rsi":          avg_rsi,
        "crcard_stickiness": crcard_sticky,
    }


def _card(col, icon, title, value, subtitle, bg_gradient, border_color):
    col.markdown(f"""
    <div style="
        background: {bg_gradient};
        border: 1px solid {border_color};
        border-radius: 14px;
        padding: 18px 20px 14px 20px;
        min-height: 110px;
        position: relative;
        overflow: hidden;
    ">
        <div style="font-size:1.7rem; margin-bottom:4px;">{icon}</div>
        <div style="font-size:0.72rem; color:rgba(255,255,255,0.6);
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">
            {title}
        </div>
        <div style="font-size:1.65rem; font-weight:800; color:#fff;
                    line-height:1.1; margin-bottom:4px;">
            {value}
        </div>
        <div style="font-size:0.72rem; color:rgba(255,255,255,0.5);">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_cards(df: pd.DataFrame):
    kpis = compute_kpis(df)
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    _card(c1, "📉", "Customer Turnover Churn Rate",
          f"{kpis['churn_rate']:.1f}%",
          "customers who exited",
          "linear-gradient(135deg,rgba(231,76,60,0.35),rgba(231,76,60,0.1))",
          "rgba(231,76,60,0.5)")

    gap = kpis['engagement_gap']
    _card(c2, "⚡", "Engagement Retention Ratio Gap",
          f"{gap:+.1f} pp",
          "inactive vs active churn",
          "linear-gradient(135deg,rgba(255,183,71,0.35),rgba(255,183,71,0.1))",
          "rgba(255,183,71,0.5)")

    _card(c3, "📦", "Product Depth Index  Avg Products",
          f"{kpis['product_depth']:.2f}",
          "products per customer",
          "linear-gradient(135deg,rgba(67,232,216,0.35),rgba(67,232,216,0.1))",
          "rgba(67,232,216,0.5)")

    _card(c4, "⚠️", "High-Balance Disengagement Rate",
          f"{kpis['premium_risk_pct']:.1f}%",
          "high-balance + inactive",
          "linear-gradient(135deg,rgba(255,101,132,0.35),rgba(255,101,132,0.1))",
          "rgba(255,101,132,0.5)")

    _card(c5, "💪", "Relationship Strength Index",
          f"{kpis['avg_rsi']:.1f}",
          "relationship strength /100",
          "linear-gradient(135deg,rgba(108,99,255,0.35),rgba(108,99,255,0.1))",
          "rgba(108,99,255,0.5)")

    _card(c6, "💳", "Credit Card Stickiness Score",
          f"{kpis['crcard_stickiness']:+.1f} pp",
          "card holders churn less by",
          "linear-gradient(135deg,rgba(67,232,216,0.35),rgba(67,232,216,0.1))",
          "rgba(67,232,216,0.5)")
