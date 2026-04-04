"""pages/premium_risk.py — Premium Risk Detector tab"""
from components.charts import (
    scatter_balance_salary, bar_premium_vs_general,
    bar_balance_segment_churn, violin_balance_churn,
)
import pandas as pd
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def render(df: pd.DataFrame):
    st.markdown("""
    <h2 style='margin:0 0 4px 0; color:#fff;'>⚠️ Premium Risk Detector</h2>
    <p style='color:#888; margin:0 0 18px 0; font-size:0.9rem;'>
        Identifies high-balance disengaged customers — the silent churn threat.
    </p>""", unsafe_allow_html=True)

    if df.empty:
        st.warning("⚠️ No customers match the current filters.")
        return

    # Metric row
    bal_75 = df['Balance'].quantile(0.75)
    premium = df[df['Balance'] >= bal_75]
    at_risk = df[df['PremiumAtRisk'] == 1]
    at_risk_churn = at_risk['Exited'].mean() * 100 if len(at_risk) > 0 else 0
    gen_churn = df['Exited'].mean() * 100

    col1, col2, col3, col4 = st.columns(4)
    for col, icon, label, val, color in [
        (col1, "👑", "Premium customers",
         f"{len(premium):,}",       "#6C63FF"),
        (col2, "🚨", "Premium at-risk",
         f"{len(at_risk):,}",       "#FF6584"),
        (col3, "📉", "At-risk churn rate",
         f"{at_risk_churn:.1f}%",   "#E74C3C"),
        (col4, "📊", "Overall churn rate",
         f"{gen_churn:.1f}%",        "#FFB347"),
    ]:
        col.markdown(f"""
        <div style='background:rgba(255,255,255,0.04); border:1px solid {color}44;
                    border-radius:12px; padding:16px; text-align:center;'>
            <div style='font-size:1.6rem;'>{icon}</div>
            <div style='font-size:0.72rem; color:#888; text-transform:uppercase;
                        letter-spacing:1px; margin:6px 0 4px;'>{label}</div>
            <div style='font-size:1.5rem; font-weight:800; color:{color};'>{val}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

    # Charts row 1
    st.plotly_chart(scatter_balance_salary(df), use_container_width=True)

    # Charts row 2
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(bar_premium_vs_general(df), use_container_width=True)
    with c2:
        st.plotly_chart(bar_balance_segment_churn(df),
                        use_container_width=True)

    # Violin full width
    st.plotly_chart(violin_balance_churn(df), use_container_width=True)

    # At-risk customer table
    # st.markdown("### 🚨 Premium at-risk customer list")
    st.markdown(
        "### 🚨 High-Value Disengaged Customer Detector — Premium At-Risk List")
    risk_df = df[df['PremiumAtRisk'] == 1][[
        'CustomerId', 'Surname', 'Geography', 'Gender', 'Age',
        'Balance', 'NumOfProducts', 'Tenure', 'RSI', 'Exited',
    ]].sort_values('Balance', ascending=False).reset_index(drop=True)

    st.dataframe(
        risk_df.style.background_gradient(subset=['Balance'], cmap='YlOrRd')
                     .background_gradient(subset=['RSI'], cmap='RdYlGn'),
        use_container_width=True, hide_index=False,
    )

    csv = risk_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Download at-risk list as CSV",
        data=csv,
        file_name="premium_at_risk_customers.csv",
        mime="text/csv",
        type="primary",
    )
