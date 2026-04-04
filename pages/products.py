"""pages/products.py — Product Utilization tab"""
from components.charts import (
    bar_churn_by_products, heatmap_products_activity,
    box_balance_by_products, bar_crcard_churn, treemap_product_geo, bar_single_vs_multi,
)
import pandas as pd
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def render(df: pd.DataFrame):
    st.markdown("""
    <h2 style='margin:0 0 4px 0; color:#fff;'>📦 Product Utilization Impact</h2>
    <p style='color:#888; margin:0 0 18px 0; font-size:0.9rem;'>
        How product depth and credit card ownership shape customer loyalty.
    </p>""", unsafe_allow_html=True)

    if df.empty:
        st.warning("⚠️ No customers match the current filters.")
        return

    # Insight banner
    single = df[df['NumOfProducts'] == 1]['Exited'].mean() * 100
    multi = df[df['NumOfProducts'] >= 2]['Exited'].mean() * 100
    three_plus = df[df['NumOfProducts'] >= 3]['Exited'].mean() * 100

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(67,232,216,0.15),rgba(255,183,71,0.1));
                border:1px solid rgba(67,232,216,0.35); border-radius:12px;
                padding:14px 20px; margin-bottom:20px;'>
        🔎 <b style='color:#43E8D8;'>Product Utilization Analysis insight:</b>
        <span style='color:#ccc;'> Single-product customers churn at </span>
        <b style='color:#E74C3C;'>{single:.1f}%</b>
        <span style='color:#ccc;'> vs </span>
        <b style='color:#2ECC71;'>{multi:.1f}%</b>
        <span style='color:#ccc;'> for multi-product holders. However, 3+ product customers show
        elevated churn at </span><b style='color:#FFB347;'>{three_plus:.1f}%</b>
        <span style='color:#ccc;'> — watch for over-sold segments.</span>
    </div>
    """, unsafe_allow_html=True)

    # Row 1
    # c1, c2 = st.columns(2)
    # with c1:
    #     st.plotly_chart(bar_churn_by_products(df), use_container_width=True)
    # with c2:
    #     st.plotly_chart(bar_crcard_churn(df), use_container_width=True)

    # Row 1
    c1, c2, c3 = st.columns(3)
    with c1:
        st.plotly_chart(bar_churn_by_products(df), use_container_width=True)
    with c2:
        st.plotly_chart(bar_single_vs_multi(df), use_container_width=True)
    with c3:
        st.plotly_chart(bar_crcard_churn(df), use_container_width=True)

    # Row 2
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(heatmap_products_activity(df),
                        use_container_width=True)
    with c4:
        st.plotly_chart(box_balance_by_products(df), use_container_width=True)

    # Treemap full width
    st.plotly_chart(treemap_product_geo(df), use_container_width=True)

    # Breakdown table
    with st.expander("📋 Product count breakdown"):
        tbl = (
            df.groupby('NumOfProducts')
            .agg(
                Customers=('CustomerId', 'count'),
                Churn_Rate=('Exited', 'mean'),
                Avg_Balance=('Balance', 'mean'),
                Active_Pct=('IsActiveMember', 'mean'),
                Avg_RSI=('RSI', 'mean'),
            ).reset_index()
        )
        tbl['Churn_Rate'] = (tbl['Churn_Rate'] * 100).round(1)
        tbl['Active_Pct'] = (tbl['Active_Pct'] * 100).round(1)
        tbl['Avg_Balance'] = tbl['Avg_Balance'].round(0)
        tbl['Avg_RSI'] = tbl['Avg_RSI'].round(1)
        tbl.columns = ['# Products', 'Customers', 'Churn Rate (%)',
                       'Avg Balance (€)', 'Active (%)', 'Avg RSI']
        st.dataframe(
            tbl.style.background_gradient(
                subset=['Churn Rate (%)'], cmap='RdYlGn_r'),
            use_container_width=True, hide_index=False,
        )
