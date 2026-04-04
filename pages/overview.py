"""pages/overview.py — Overview tab"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import pandas as pd
from components.kpi_cards import render_kpi_cards
from components.charts import (
    donut_churn, bar_churn_by_geo,
    bar_churn_by_age, bar_churn_by_credit,
)


def render(df: pd.DataFrame):
    st.markdown("""
    <h2 style='margin:0 0 4px 0; color:#fff;'>📊 Executive Overview</h2>
    <p style='color:#888; margin:0 0 18px 0; font-size:0.9rem;'>
        High-level churn snapshot across the filtered customer base.
    </p>""", unsafe_allow_html=True)

    if df.empty:
        st.warning("⚠️ No customers match the current filters.")
        return

    render_kpi_cards(df)
    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)

    # Row 1
    c1, c2 = st.columns([1, 1.7])
    with c1:
        st.plotly_chart(donut_churn(df), use_container_width=True)
    with c2:
        st.plotly_chart(bar_churn_by_geo(df), use_container_width=True)

    # Row 2
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(bar_churn_by_age(df), use_container_width=True)
    with c4:
        st.plotly_chart(bar_churn_by_credit(df), use_container_width=True)

    # Summary table
    with st.expander("📋 Summary statistics table"):
        num_cols = ['Age', 'CreditScore', 'Balance', 'Tenure',
                    'NumOfProducts', 'EstimatedSalary', 'RSI']
        st.dataframe(
            df[num_cols].describe().T.style.format("{:.2f}"),
            use_container_width=True,
            hide_index=False,
        )