# European Bank — Customer Retention Analytics Dashboard

Interactive Streamlit + Plotly dashboard for customer engagement and churn analysis.

## Project structure

```
bank_dashboard/
├── app.py                        ← Entry point
├── config.py                     ← Constants & colour palette
├── utils.py                      ← Data loading & feature engineering
├── requirements.txt
├── data/
│   └── European_Bank.csv         ← Put your CSV here
├── components/
│   ├── sidebar.py                ← Sidebar filters
│   ├── kpi_cards.py              ← KPI metric cards
│   └── charts.py                 ← All Plotly chart functions
└── pages/
    ├── overview.py               ← Tab 1: Overview
    ├── engagement.py             ← Tab 2: Engagement vs Churn
    ├── products.py               ← Tab 3: Product Utilization
    ├── premium_risk.py           ← Tab 4: Premium Risk Detector
    └── retention_score.py        ← Tab 5: Retention Strength Scoring
```

## Setup & run

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place your CSV
#    Copy your dataset to:  data/European_Bank.csv
#    Column names expected:
#    CustomerId, Surname, CreditScore, Geography, Gender, Age, Tenure,
#    Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Exited

# 4. Run
streamlit run app.py
```

The dashboard opens at **http://localhost:8501**

## Features

| Tab | Key charts |
|-----|-----------|
| Overview | KPI cards, churn donut, churn by geography & age band |
| Engagement | Active vs inactive churn, engagement profiles, stacked geo chart |
| Products | Churn by product count, heatmap (products × activity), credit card stickiness |
| Premium Risk | Balance vs salary scatter, at-risk customer table, downloadable CSV |
| Retention Score | RSI gauge, RSI by profile, RSI histogram, scatter RSI vs age |

## Derived features

| Column | Description |
|--------|-------------|
| `EngagementProfile` | 4-class label combining activity + product count |
| `RSI` | Relationship Strength Index (0–100) |
| `PremiumAtRisk` | Flag: top-quartile balance + inactive |
| `BalanceSegment` | Binned balance buckets |
| `AgeBand` | Age decade bands |

## RSI formula

```
RSI = IsActiveMember × 30
    + NumOfProducts.clip(1,4) × 15
    + HasCrCard × 10
    + (Tenure / max_tenure) × 25
    + (Balance > 0) × 20
```
