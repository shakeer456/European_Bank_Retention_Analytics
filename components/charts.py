"""
components/charts.py
────────────────────
All reusable Plotly chart factory functions.
Dark-themed, colourful, production-grade.
"""
from config import (
    COLOR_RETAINED, COLOR_CHURNED,
    COLOR_GEO, COLOR_PROFILE, COLOR_PRODUCTS,
    SEQ_RED_GREEN, SEQ_VIRIDIS,
    LAYOUT_DEFAULTS,
    PRIMARY, SECONDARY, ACCENT_TEAL, ACCENT_AMBER,
    ACCENT_GREEN, ACCENT_BLUE, ACCENT_PURPLE, ACCENT_ORANGE,
)
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _apply(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(**LAYOUT_DEFAULTS)
    if title:
        fig.update_layout(title=dict(
            text=title, font=dict(size=15, color="#FFFFFF"), x=0.01))
    return fig


# ════════════════════════════════════════════════════════════════════════════
#  OVERVIEW
# ════════════════════════════════════════════════════════════════════════════

def donut_churn(df: pd.DataFrame) -> go.Figure:
    counts = df['Exited'].value_counts().reset_index()
    counts.columns = ['Exited', 'Count']
    counts['Status'] = counts['Exited'].map({0: 'Retained', 1: 'Churned'})
    fig = go.Figure(go.Pie(
        labels=counts['Status'],
        values=counts['Count'],
        hole=0.60,
        marker=dict(
            colors=[COLOR_RETAINED, COLOR_CHURNED],
            line=dict(color='rgba(0,0,0,0.4)', width=2),
        ),
        textfont=dict(size=13, color='white'),
        hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>',
    ))
    fig.add_annotation(
        text=f"<b>{df['Exited'].mean()*100:.1f}%</b><br><span style='font-size:11px'>Churn</span>",
        x=0.5, y=0.5, font=dict(size=18, color='white'),
        showarrow=False, align='center',
    )
    fig.update_traces(textposition='outside', textinfo='percent+label',
                      textfont=dict(color='#ffffff', size=13))
    fig = _apply(fig, "Overall churn split")
    fig.update_layout(legend=dict(
        font=dict(color='#ffffff', size=13),
        bgcolor='rgba(13,13,26,0.9)',
        bordercolor='rgba(255,255,255,0.2)',
        borderwidth=1,
    ))
    return fig


def bar_churn_by_geo(df: pd.DataFrame) -> go.Figure:
    grp = df.groupby('Geography')['Exited'].mean().reset_index()
    grp['Churn Rate'] = (grp['Exited'] * 100).round(1)
    colors = [COLOR_GEO.get(g, PRIMARY) for g in grp['Geography']]
    fig = go.Figure(go.Bar(
        x=grp['Geography'], y=grp['Churn Rate'],
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v:.1f}%" for v in grp['Churn Rate']],
        textposition='outside', textfont=dict(color='white', size=13),
        hovertemplate='<b>%{x}</b><br>Churn: %{y:.1f}%<extra></extra>',
    ))
    fig.update_yaxes(title='Churn rate (%)', range=[
                     0, grp['Churn Rate'].max() * 1.35])
    return _apply(fig, "Churn rate by geography")


def bar_churn_by_age(df: pd.DataFrame) -> go.Figure:
    grp = df.groupby('AgeBand', observed=True)['Exited'].mean().reset_index()
    grp['Churn Rate'] = (grp['Exited'] * 100).round(1)
    palette = [PRIMARY, ACCENT_TEAL, ACCENT_AMBER, SECONDARY, ACCENT_PURPLE]
    fig = go.Figure(go.Bar(
        x=grp['AgeBand'].astype(str), y=grp['Churn Rate'],
        marker=dict(
            color=grp['Churn Rate'],
            colorscale=[[0, '#2ECC71'], [0.5, '#FFB347'], [1, '#E74C3C']],
            showscale=True,
            colorbar=dict(title='Churn %', tickfont=dict(color='#ccc')),
            line=dict(width=0),
        ),
        text=[f"{v:.1f}%" for v in grp['Churn Rate']],
        textposition='outside', textfont=dict(color='white', size=12),
        hovertemplate='<b>Age %{x}</b><br>Churn: %{y:.1f}%<extra></extra>',
    ))
    fig.update_yaxes(title='Churn rate (%)')
    fig.update_xaxes(title='Age band')
    return _apply(fig, "Churn rate by age band")


def bar_churn_by_credit(df: pd.DataFrame) -> go.Figure:
    grp = df.groupby('CreditBand', observed=True)[
        'Exited'].mean().reset_index()
    grp['Churn Rate'] = (grp['Exited'] * 100).round(1)
    fig = go.Figure(go.Bar(
        x=grp['CreditBand'].astype(str), y=grp['Churn Rate'],
        marker=dict(color=[ACCENT_PURPLE, ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN],
                    line=dict(width=0)),
        text=[f"{v:.1f}%" for v in grp['Churn Rate']],
        textposition='outside', textfont=dict(color='white', size=12),
        hovertemplate='<b>%{x}</b><br>Churn: %{y:.1f}%<extra></extra>',
    ))
    fig.update_yaxes(title='Churn rate (%)')
    fig.update_xaxes(title='Credit score band')
    return _apply(fig, "Churn rate by credit score band")


# ════════════════════════════════════════════════════════════════════════════
#  ENGAGEMENT
# ════════════════════════════════════════════════════════════════════════════

def bar_churn_by_profile(df: pd.DataFrame) -> go.Figure:
    grp = (
        df.groupby('EngagementProfile')['Exited']
        .agg(['mean', 'count']).reset_index()
    )
    grp.columns = ['Profile', 'Churn Rate', 'Count']
    grp['Churn Rate'] = (grp['Churn Rate'] * 100).round(1)
    grp = grp.sort_values('Churn Rate', ascending=False)
    colors = [COLOR_PROFILE.get(p, PRIMARY) for p in grp['Profile']]
    fig = go.Figure(go.Bar(
        x=grp['Profile'], y=grp['Churn Rate'],
        marker=dict(color=colors, line=dict(width=0),
                    opacity=0.9),
        text=[f"{v:.1f}%" for v in grp['Churn Rate']],
        textposition='outside', textfont=dict(color='white', size=12),
        customdata=grp['Count'],
        hovertemplate='<b>%{x}</b><br>Churn: %{y:.1f}%<br>Customers: %{customdata:,}<extra></extra>',
    ))
    fig.update_yaxes(title='Churn rate (%)', range=[
                     0, grp['Churn Rate'].max() * 1.3])
    return _apply(fig, "Churn rate by engagement profile")


def stacked_active_by_geo(df: pd.DataFrame) -> go.Figure:
    grp = df.groupby(['Geography', 'IsActiveMember'])[
        'CustomerId'].count().reset_index()
    grp['Status'] = grp['IsActiveMember'].map({0: 'Inactive', 1: 'Active'})
    fig = px.bar(
        grp, x='Geography', y='CustomerId', color='Status',
        color_discrete_map={'Active': ACCENT_GREEN, 'Inactive': COLOR_CHURNED},
        barmode='stack',
        text_auto=True,
    )
    fig.update_yaxes(title='Customer count')
    fig.update_xaxes(title='')
    fig.update_traces(textfont_color='white')
    return _apply(fig, "Active vs inactive members by geography")


def bar_churn_active_vs_inactive(df: pd.DataFrame) -> go.Figure:
    grp = df.groupby('IsActiveMember')['Exited'].mean().reset_index()
    grp['Label'] = grp['IsActiveMember'].map({0: 'Inactive', 1: 'Active'})
    grp['Churn'] = (grp['Exited'] * 100).round(1)
    fig = go.Figure(go.Bar(
        x=grp['Label'], y=grp['Churn'],
        marker=dict(color=[COLOR_CHURNED, ACCENT_GREEN], line=dict(width=0)),
        text=[f"{v:.1f}%" for v in grp['Churn']],
        textposition='outside', textfont=dict(color='white', size=14),
        hovertemplate='<b>%{x}</b><br>Churn: %{y:.1f}%<extra></extra>',
    ))
    fig.update_yaxes(title='Churn rate (%)', range=[0, 100])
    return _apply(fig, "Engagement Retention Ratio — active vs inactive churn rates")
    # return _apply(fig, "Churn: active vs inactive members")


def funnel_engagement(df: pd.DataFrame) -> go.Figure:
    stages = []
    for profile in ['Active engaged', 'Active low-product',
                    'Inactive multi-product', 'Inactive disengaged']:
        sub = df[df['EngagementProfile'] == profile]
        stages.append({
            'Profile': profile,
            'Customers': len(sub),
            'Churned': sub['Exited'].sum(),
        })
    fdf = pd.DataFrame(stages)
    fig = go.Figure(go.Funnel(
        y=fdf['Profile'],
        x=fdf['Customers'],
        textinfo='value+percent initial',
        marker=dict(color=[ACCENT_GREEN, ACCENT_AMBER,
                    ACCENT_ORANGE, COLOR_CHURNED]),
        connector=dict(line=dict(color='rgba(255,255,255,0.1)', width=1)),
    ))
    return _apply(fig, "Customer funnel by engagement profile")


def bar_gender_churn(df: pd.DataFrame) -> go.Figure:
    grp = df.groupby(['Gender', 'Exited'])['CustomerId'].count().reset_index()
    grp['Status'] = grp['Exited'].map({0: 'Retained', 1: 'Churned'})
    fig = px.bar(
        grp, x='Gender', y='CustomerId', color='Status',
        color_discrete_map={'Retained': ACCENT_GREEN,
                            'Churned': COLOR_CHURNED},
        barmode='group', text_auto=True,
    )
    fig.update_yaxes(title='Customer count')
    fig.update_traces(textfont_color='white')
    return _apply(fig, "Churn by gender")


# ════════════════════════════════════════════════════════════════════════════
#  PRODUCTS
# ════════════════════════════════════════════════════════════════════════════

def bar_churn_by_products(df: pd.DataFrame) -> go.Figure:
    grp = df.groupby('NumOfProducts')['Exited'].mean().reset_index()
    grp['Churn Rate'] = (grp['Exited'] * 100).round(1)
    colors = [COLOR_PRODUCTS[min(i, len(COLOR_PRODUCTS)-1)]
              for i in range(len(grp))]
    fig = go.Figure(go.Bar(
        x=grp['NumOfProducts'].astype(str), y=grp['Churn Rate'],
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v:.1f}%" for v in grp['Churn Rate']],
        textposition='outside', textfont=dict(color='white', size=13),
        hovertemplate='<b>%{x} products</b><br>Churn: %{y:.1f}%<extra></extra>',
    ))
    fig.update_yaxes(title='Churn rate (%)', range=[
                     0, grp['Churn Rate'].max() * 1.35])
    fig.update_xaxes(title='Number of products held')
    return _apply(fig, "Churn rate by number of products")


def heatmap_products_activity(df: pd.DataFrame) -> go.Figure:
    pivot = (
        df.groupby(['NumOfProducts', 'IsActiveMember'])['Exited']
        .mean()
        .unstack(fill_value=0) * 100
    )
    # Ensure both columns exist
    for val in [0, 1]:
        if val not in pivot.columns:
            pivot[val] = 0.0
    pivot = pivot[[0, 1]]
    pivot.columns = ['Inactive', 'Active']

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=['Inactive', 'Active'],
        y=[str(i) for i in pivot.index],
        colorscale=[[0, '#2ECC71'], [0.4, '#FFB347'],
                    [0.7, '#E67E22'], [1, '#E74C3C']],
        text=[[f"{v:.1f}%" for v in row] for row in pivot.values],
        texttemplate='%{text}',
        textfont=dict(size=14, color='white'),
        showscale=True,
        colorbar=dict(title='Churn %', tickfont=dict(color='#ccc')),
        hovertemplate='Products: %{y}<br>Status: %{x}<br>Churn: %{z:.1f}%<extra></extra>',
    ))
    fig.update_xaxes(title='Member status')
    fig.update_yaxes(title='# of products')
    return _apply(fig, "Product Utilization Analysis — product depth vs churn relationship")
    # return _apply(fig, "Churn rate heatmap: products × activity")


def _hex_to_rgba(hex_color: str, alpha: float = 0.3) -> str:
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _hex_to_rgba(hex_color: str, alpha: float = 0.3) -> str:
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def box_balance_by_products(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for i, n in enumerate(sorted(df['NumOfProducts'].unique())):
        sub = df[df['NumOfProducts'] == n]['Balance']
        color = COLOR_PRODUCTS[min(i, len(COLOR_PRODUCTS)-1)]
        fig.add_trace(go.Box(
            y=sub,
            name=f"{n} product{'s' if n > 1 else ''}",
            marker_color=color,
            line_color=color,
            fillcolor=_hex_to_rgba(color, 0.3),
            boxmean='sd',
        ))
    fig.update_yaxes(title='Account balance (€)')
    fig.update_xaxes(title='')
    return _apply(fig, "Product Depth vs Churn — balance distribution by product count")
    # return _apply(fig, "Balance distribution by product count")


def bar_crcard_churn(df: pd.DataFrame) -> go.Figure:
    grp = df.groupby('HasCrCard')['Exited'].mean().reset_index()
    grp['Label'] = grp['HasCrCard'].map(
        {0: 'No credit card', 1: 'Has credit card'})
    grp['Churn'] = (grp['Exited'] * 100).round(1)
    fig = go.Figure(go.Bar(
        x=grp['Label'], y=grp['Churn'],
        marker=dict(color=[COLOR_CHURNED, ACCENT_BLUE], line=dict(width=0)),
        text=[f"{v:.1f}%" for v in grp['Churn']],
        textposition='outside', textfont=dict(color='white', size=13),
        hovertemplate='<b>%{x}</b><br>Churn: %{y:.1f}%<extra></extra>',
    ))
    fig.update_yaxes(title='Churn rate (%)', range=[0, 60])
    return _apply(fig, "Credit Card Stickiness Score — churn by card ownership")
    # return _apply(fig, "Credit card stickiness: churn by card ownership")


def treemap_product_geo(df: pd.DataFrame) -> go.Figure:
    grp = df.groupby(['Geography', 'NumOfProducts'])[
        'CustomerId'].count().reset_index()
    grp.columns = ['Geography', 'NumOfProducts', 'Customers']
    grp['Products'] = grp['NumOfProducts'].astype(str) + ' product(s)'
    fig = px.treemap(
        grp, path=['Geography', 'Products'], values='Customers',
        color='Customers',
        color_continuous_scale=['#6C63FF', '#43E8D8', '#FFB347'],
    )
    fig.update_traces(
        textfont=dict(size=13, color='white'),
        hovertemplate='<b>%{label}</b><br>Customers: %{value:,}<extra></extra>',
    )
    fig.update_coloraxes(showscale=False)
    return _apply(fig, "Product distribution by geography (treemap)")


# ════════════════════════════════════════════════════════════════════════════
#  PREMIUM RISK
# ════════════════════════════════════════════════════════════════════════════

def scatter_balance_salary(df: pd.DataFrame) -> go.Figure:
    plot_df = df.copy()
    plot_df['Status'] = plot_df['Exited'].map({0: 'Retained', 1: 'Churned'})
    fig = px.scatter(
        plot_df, x='EstimatedSalary', y='Balance',
        color='Status',
        color_discrete_map={'Retained': ACCENT_GREEN,
                            'Churned': COLOR_CHURNED},
        size='RSI', size_max=18,
        opacity=0.65,
        hover_data={
            'CustomerId': True, 'Geography': True,
            'Age': True, 'NumOfProducts': True, 'RSI': True,
            'EstimatedSalary': ':.0f', 'Balance': ':.0f',
        },
    )
    fig.update_xaxes(title='Estimated salary (€)')
    fig.update_yaxes(title='Account balance (€)')
    return _apply(fig, "Salary–Balance Mismatch Detection")
    # return _apply(fig, "Balance vs salary — bubble size = RSI score")


def bar_premium_vs_general(df: pd.DataFrame) -> go.Figure:
    bal_75 = df['Balance'].quantile(0.75)
    df2 = df.copy()
    df2['Segment'] = df2['Balance'].apply(
        lambda b: 'Premium (top 25%)' if b >= bal_75 else 'General'
    )
    grp = df2.groupby('Segment')['Exited'].mean().reset_index()
    grp['Churn'] = (grp['Exited'] * 100).round(1)
    fig = go.Figure(go.Bar(
        x=grp['Segment'], y=grp['Churn'],
        marker=dict(color=[ACCENT_ORANGE, ACCENT_BLUE], line=dict(width=0)),
        text=[f"{v:.1f}%" for v in grp['Churn']],
        textposition='outside', textfont=dict(color='white', size=13),
    ))
    fig.update_yaxes(title='Churn rate (%)', range=[
                     0, grp['Churn'].max() * 1.4])
    return _apply(fig, 'Identification of "At-Risk Premium Customers"')
    # return _apply(fig, "Premium segment vs general population churn")


def bar_balance_segment_churn(df: pd.DataFrame) -> go.Figure:
    grp = df.groupby('BalanceSegment', observed=True)[
        'Exited'].mean().reset_index()
    grp['Churn'] = (grp['Exited'] * 100).round(1)
    palette = [ACCENT_BLUE, ACCENT_TEAL,
               ACCENT_AMBER, ACCENT_ORANGE, COLOR_CHURNED]
    fig = go.Figure(go.Bar(
        x=grp['BalanceSegment'].astype(str), y=grp['Churn'],
        marker=dict(color=palette[:len(grp)], line=dict(width=0)),
        text=[f"{v:.1f}%" for v in grp['Churn']],
        textposition='outside', textfont=dict(color='white', size=12),
    ))
    fig.update_yaxes(title='Churn rate (%)')
    fig.update_xaxes(title='Balance segment')
    return _apply(fig, "Churn rate by balance segment")


def violin_balance_churn(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for status, color in [('Retained', ACCENT_GREEN), ('Churned', COLOR_CHURNED)]:
        sub = df[df['Exited'] == (0 if status == 'Retained' else 1)]['Balance']
        fig.add_trace(go.Violin(
            y=sub, name=status,
            box_visible=True, meanline_visible=True,
            fillcolor=_hex_to_rgba(color, 0.35),
            line_color=color,
        ))
    fig.update_yaxes(title='Account balance (€)')
    # return _apply(fig, "Financial Commitment vs Engagement — balance distribution by churn")
    return _apply(fig, "Balance vs activity cross-analysis(violin)")


# ════════════════════════════════════════════════════════════════════════════
#  RETENTION SCORING
# ════════════════════════════════════════════════════════════════════════════

# def gauge_rsi(avg_rsi: float) -> go.Figure:
#     if avg_rsi >= 65:
#         bar_color = ACCENT_GREEN
#     elif avg_rsi >= 40:
#         bar_color = ACCENT_AMBER
#     else:
#         bar_color = COLOR_CHURNED

#     fig = go.Figure(go.Indicator(
#         mode='gauge+number+delta',
#         value=avg_rsi,
#         delta={'reference': 50, 'valueformat': '.1f',
#                'increasing': {'color': ACCENT_GREEN},
#                'decreasing': {'color': COLOR_CHURNED}},
#         number={'suffix': ' / 100', 'font': {'size': 38, 'color': 'white'}},
#         gauge={
#             'axis': {'range': [0, 100], 'tickwidth': 1,
#                      'tickcolor': '#888', 'tickfont': {'color': '#ccc'}},
#             'bar':  {'color': bar_color, 'thickness': 0.25},
#             'bgcolor': 'rgba(0,0,0,0)',
#             'borderwidth': 0,
#             'steps': [
#                 {'range': [0,  40],  'color': 'rgba(231,76,60,0.2)'},
#                 {'range': [40, 65],  'color': 'rgba(255,183,71,0.2)'},
#                 {'range': [65, 100], 'color': 'rgba(46,204,113,0.2)'},
#             ],
#             'threshold': {
#                 'line':  {'color': 'white', 'width': 2},
#                 'thickness': 0.75,
#                 'value': 50,
#             },
#         },
#         title={'text': 'Avg Relationship Strength Index',
#                'font': {'size': 14, 'color': '#ccc'}},
#     ))
#     return _apply(fig)


def gauge_rsi(avg_rsi: float) -> go.Figure:
    if avg_rsi >= 65:
        bar_color = ACCENT_GREEN
    elif avg_rsi >= 40:
        bar_color = ACCENT_AMBER
    else:
        bar_color = COLOR_CHURNED

    fig = go.Figure(go.Indicator(
        mode='gauge+number',
        value=avg_rsi,
        number={'valueformat': '.1f', 'font': {'size': 38, 'color': 'white'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1,
                     'tickcolor': '#888', 'tickfont': {'color': '#ccc'}},
            'bar':  {'color': bar_color, 'thickness': 0.25},
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 0,
            'steps': [
                {'range': [0,  40],  'color': 'rgba(231,76,60,0.2)'},
                {'range': [40, 65],  'color': 'rgba(255,183,71,0.2)'},
                {'range': [65, 100], 'color': 'rgba(46,204,113,0.2)'},
            ],
            'threshold': {
                'line':  {'color': 'white', 'width': 2},
                'thickness': 0.75,
                'value': 50,
            },
        },
        title={'text': f'Avg Relationship Strength Index — {avg_rsi:.1f} / 100',
               'font': {'size': 14, 'color': '#ccc'}},
    ))
    fig.update_layout(**LAYOUT_DEFAULTS)
    fig.update_layout(title=dict(
        text='Relationship Strength Index (RSI)',
        font=dict(size=15, color='#FFFFFF'),
        x=0.01,
    ))
    return fig


def scatter_rsi_age(df: pd.DataFrame) -> go.Figure:
    plot_df = df.copy()
    plot_df['Status'] = plot_df['Exited'].map({0: 'Retained', 1: 'Churned'})

    fig = px.scatter(
        plot_df, x='Age', y='RSI',
        color='Status',
        color_discrete_map={'Retained': ACCENT_GREEN,
                            'Churned': COLOR_CHURNED},
        opacity=0.55,
        hover_data=['Geography', 'NumOfProducts', 'Balance'],
    )
    # Manual numpy trendline per group
    for label, color in [('Retained', ACCENT_GREEN), ('Churned', COLOR_CHURNED)]:
        sub = plot_df[plot_df['Status'] == label].dropna(subset=['Age', 'RSI'])
        if len(sub) < 2:
            continue
        x_v = sub['Age'].values
        y_v = sub['RSI'].values
        coeffs = np.polyfit(x_v, y_v, 1)
        x_line = np.linspace(x_v.min(), x_v.max(), 120)
        y_line = np.polyval(coeffs, x_line)
        fig.add_trace(go.Scatter(
            x=x_line, y=y_line, mode='lines',
            line=dict(color=color, width=2.5, dash='dot'),
            name=f'{label} trend', showlegend=False, hoverinfo='skip',
        ))

    fig.update_xaxes(title='Age')
    fig.update_yaxes(title='RSI score')
    return _apply(fig, "Retention Strength Assessment — RSI score vs age")
    # return _apply(fig, "RSI score vs age (with trendlines)")


def bar_rsi_by_profile(df: pd.DataFrame) -> go.Figure:
    grp = df.groupby('EngagementProfile')['RSI'].mean().reset_index()
    grp.columns = ['Profile', 'Avg RSI']
    grp = grp.sort_values('Avg RSI', ascending=True)
    colors = [COLOR_PROFILE.get(p, PRIMARY) for p in grp['Profile']]
    fig = go.Figure(go.Bar(
        x=grp['Avg RSI'], y=grp['Profile'],
        orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v:.1f}" for v in grp['Avg RSI']],
        textposition='outside', textfont=dict(color='white', size=12),
    ))
    fig.update_xaxes(title='Average RSI score', range=[0, 100])
    fig.update_yaxes(title='')
    return _apply(fig, "Avg RSI by engagement profile")
    # return _apply(fig, "Average RSI by engagement profile")


def histogram_rsi(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for status, color, name in [
        (0, ACCENT_GREEN, 'Retained'),
        (1, COLOR_CHURNED, 'Churned'),
    ]:
        sub = df[df['Exited'] == status]['RSI']
        fig.add_trace(go.Histogram(
            x=sub, name=name, nbinsx=20,
            marker_color=color,
            marker_line=dict(color=color, width=1),
            opacity=0.65,
        ))
    fig.update_layout(barmode='overlay')
    fig.update_xaxes(title='RSI score')
    fig.update_yaxes(title='Customer count')
    return _apply(fig, "Distribution: retained vs churned")
    # return _apply(fig, "RSI distribution: retained vs churned")


def radar_profile(df: pd.DataFrame) -> go.Figure:
    """Radar chart comparing engagement profile averages."""
    metrics = ['CreditScore', 'Age', 'Tenure',
               'Balance', 'EstimatedSalary', 'RSI']
    norm_df = df[metrics + ['EngagementProfile']].copy()
    for m in metrics:
        mn, mx = norm_df[m].min(), norm_df[m].max()
        norm_df[m] = (norm_df[m] - mn) / (mx - mn) * 100 if mx > mn else 50

    fig = go.Figure()
    for profile, color in COLOR_PROFILE.items():
        sub = norm_df[norm_df['EngagementProfile'] == profile]
        if len(sub) == 0:
            continue
        vals = [sub[m].mean() for m in metrics]
        vals += [vals[0]]
        cats = metrics + [metrics[0]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=cats, name=profile,
            line=dict(color=color, width=2),
            fill='toself',
            fillcolor=_hex_to_rgba(color, 0.13),
        ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0, 100],
                            gridcolor='rgba(255,255,255,0.1)',
                            tickfont=dict(color='#888')),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.1)',
                             tickfont=dict(color='#ccc')),
        ),
    )
    return _apply(fig, "Engagement profile radar (normalised metrics)")


def bar_single_vs_multi(df: pd.DataFrame) -> go.Figure:
    df2 = df.copy()
    df2['Product Type'] = df2['NumOfProducts'].apply(
        lambda x: 'Single-product' if x == 1 else 'Multi-product'
    )
    grp = df2.groupby('Product Type')['Exited'].mean().reset_index()
    grp['Churn Rate'] = (grp['Exited'] * 100).round(1)
    fig = go.Figure(go.Bar(
        x=grp['Product Type'], y=grp['Churn Rate'],
        marker=dict(color=[ACCENT_BLUE, ACCENT_GREEN], line=dict(width=0)),
        text=[f"{v:.1f}%" for v in grp['Churn Rate']],
        textposition='outside', textfont=dict(color='white', size=14),
        hovertemplate='<b>%{x}</b><br>Churn: %{y:.1f}%<extra></extra>',
    ))
    fig.update_yaxes(title='Churn rate (%)', range=[
                     0, grp['Churn Rate'].max() * 1.4])
    fig.update_xaxes(title='')
    return _apply(fig, "Single-product vs Multi-product Retention")


def sticky_customer_summary(df: pd.DataFrame) -> go.Figure:
    sticky = df[df['RSI'] >= 65]
    regular = df[df['RSI'] < 65]

    categories = ['Total Customers',
                  'Sticky Customers (RSI ≥ 65)', 'Regular Customers']
    values = [len(df), len(sticky), len(regular)]
    churn = [df['Exited'].mean()*100, sticky['Exited'].mean() *
             100, regular['Exited'].mean()*100]
    avg_bal = [df['Balance'].mean(), sticky['Balance'].mean(),
               regular['Balance'].mean()]
    avg_prod = [df['NumOfProducts'].mean(), sticky['NumOfProducts'].mean(),
                regular['NumOfProducts'].mean()]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Customer Count',
        x=categories,
        y=values,
        marker=dict(color=[ACCENT_BLUE, ACCENT_GREEN,
                    ACCENT_AMBER], line=dict(width=0)),
        text=[f"{v:,}" for v in values],
        textposition='outside',
        textfont=dict(color='white', size=13),
        yaxis='y',
        customdata=list(zip(churn, avg_bal, avg_prod)),
        hovertemplate=(
            '<b>%{x}</b><br>'
            'Customers: %{y:,}<br>'
            'Churn Rate: %{customdata[0]:.1f}%<br>'
            'Avg Balance: €%{customdata[1]:,.0f}<br>'
            'Avg Products: %{customdata[2]:.1f}<extra></extra>'
        ),
    ))
    fig.add_trace(go.Scatter(
        name='Churn Rate (%)',
        x=categories,
        y=churn,
        mode='lines+markers+text',
        line=dict(color=COLOR_CHURNED, width=2.5, dash='dot'),
        marker=dict(color=COLOR_CHURNED, size=10),
        text=[f"{v:.1f}%" for v in churn],
        textposition='top center',
        textfont=dict(color=COLOR_CHURNED, size=12),
        yaxis='y2',
    ))
    fig.update_layout(
        yaxis=dict(title='Customer count',  side='left',
                   gridcolor='rgba(255,255,255,0.07)', tickfont=dict(color='#B0B0B0')),
        yaxis2=dict(title='Churn rate (%)',  side='right', overlaying='y',
                    range=[0, max(churn)*1.5], gridcolor='rgba(255,255,255,0)',
                    tickfont=dict(color=COLOR_CHURNED)),
        legend=dict(
            font=dict(color='#ffffff'),
            x=1.08,
            y=1.0,
        ),
        barmode='group',
    )
    return _apply(fig, "👑 Sticky Customer Profiles — RSI ≥ 65 vs Regular Customers")


def bar_churn_stability_tiers(df: pd.DataFrame) -> go.Figure:
    df2 = df.copy()
    df2['RSI Tier'] = pd.cut(
        df2['RSI'],
        bins=[-1, 40, 65, 101],
        labels=['🔴 High risk (0–40)', '🟡 Moderate (40–65)',
                '🟢 Loyal (65–100)'],
    )
    grp = (
        df2.groupby('RSI Tier', observed=True)
        .agg(
            Customers=('CustomerId', 'count'),
            Churn_Rate=('Exited', 'mean'),
            Avg_RSI=('RSI', 'mean'),
            Avg_Balance=('Balance', 'mean'),
            Avg_Products=('NumOfProducts', 'mean'),
        ).reset_index()
    )
    grp['Churn_Rate'] = (grp['Churn_Rate'] * 100).round(1)

    colors = [COLOR_CHURNED, ACCENT_AMBER, ACCENT_GREEN]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grp['RSI Tier'].astype(str),
        y=grp['Churn_Rate'],
        name='Churn Rate (%)',
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v:.1f}%" for v in grp['Churn_Rate']],
        textposition='outside',
        textfont=dict(color='white', size=13),
        customdata=list(zip(
            grp['Customers'], grp['Avg_RSI'],
            grp['Avg_Balance'], grp['Avg_Products']
        )),
        hovertemplate=(
            '<b>%{x}</b><br>'
            'Churn Rate: %{y:.1f}%<br>'
            'Customers: %{customdata[0]:,}<br>'
            'Avg RSI: %{customdata[1]:.1f}<br>'
            'Avg Balance: €%{customdata[2]:,.0f}<br>'
            'Avg Products: %{customdata[3]:.1f}<extra></extra>'
        ),
    ))
    fig.add_trace(go.Scatter(
        x=grp['RSI Tier'].astype(str),
        y=grp['Customers'],
        name='Customer count',
        mode='lines+markers+text',
        line=dict(color=ACCENT_TEAL, width=2.5, dash='dot'),
        marker=dict(color=ACCENT_TEAL, size=10),
        text=[f"{v:,}" for v in grp['Customers']],
        textposition='top center',
        textfont=dict(color=ACCENT_TEAL, size=11),
        yaxis='y2',
    ))
    fig.update_layout(
        yaxis=dict(
            title='Churn rate (%)',
            gridcolor='rgba(255,255,255,0.07)',
            tickfont=dict(color='#B0B0B0'),
            range=[0, grp['Churn_Rate'].max() * 1.4],
        ),
        yaxis2=dict(
            title='Customer count',
            overlaying='y', side='right',
            gridcolor='rgba(255,255,255,0)',
            tickfont=dict(color=ACCENT_TEAL),
        ),
        legend=dict(
            font=dict(color='#ffffff'),
            x=1.08,
            y=1.0,
        ),
        barmode='group',
    )
    return _apply(fig, "Churn Stability Across Engagement Tiers — RSI tier vs churn rate")
