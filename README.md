# 🏦 European Bank — Customer Retention Analytics Dashboard

> **Interactive Streamlit + Plotly dashboard for customer engagement and churn analysis**
> Built with Python · Powered by behavioral analytics · Designed for retention strategy

---

## 🧠 The Story Behind This Project

While working on a real-world banking dataset containing customer demographics, financial behavior, and engagement signals, I asked myself a deeper question than just "who churned?"

**Why do bank customers leave — and can we predict it before they do?**

Traditional churn models focus on who a customer is — their age, salary, or credit score. But this project takes a different approach: it focuses on **how customers behave**. Are they actively using the bank? How many products do they hold? Is their balance sitting idle?

This project reframes customer retention from a **demographic lens** to a **behavioral and relationship-strength lens** — and builds an interactive dashboard to make those insights accessible to anyone in the organization, not just data scientists.

---

## 🔍 What This Dashboard Explores

The dashboard is built around five analytical pillars, each answering a real business question:

- How does **member activity status** affect the probability of churning?
- Does holding **more bank products** make a customer more loyal — or does it backfire?
- Are **high-balance customers** truly safe, or are some silently disengaging?
- Which customers can be classified as **sticky** (RSI ≥ 65) vs high flight risk (RSI < 40)?
- What is the **Relationship Strength Index** of each customer segment, and what does it mean for retention?

---

## 📈 Key Insights from the Data

After analyzing **10,000 European bank customers** across France, Germany, and Spain, several powerful patterns emerged:

- The overall churn rate is **20.4%** — meaning 1 in 5 customers has exited.
- **Inactive members churn at 26.9%** vs only **14.3%** for active members — a gap of +12.6 percentage points. Activity status is the single strongest predictor of retention.
- Customers with **2 products churn at just 7.6%**, but those with **3–4 products churn at 82–100%** — revealing a dangerous over-selling effect that most banks miss.
- **Germany has the highest churn rate at 32.4%**, nearly double France (16.2%) and Spain (16.7%).
- **1,129 PremiumAtRisk customers** — high balance but inactive — represent the bank's most dangerous silent churn segment.
- Customers aged **40–50** show the highest churn rates across all age bands.
- The **average RSI (Relationship Strength Index) is 70.2**, with 61.8% of customers classified as sticky (RSI ≥ 65).

---

## 🛠 Tools & Technologies Used

- **Python** — core language
- **Streamlit** — interactive web dashboard framework
- **Plotly** — rich, interactive chart library
- **Pandas & NumPy** — data manipulation and feature engineering
- **European Bank Dataset** — 10,000 customers, 14 variables

---

## 📊 Dashboard Preview

| Tab | Purpose | Key Charts |
|-----|---------|-----------|
| 📊 Overview | Executive churn snapshot | KPI cards, churn donut, geo bar, age band bar, credit score bar |
| ⚡ Engagement | Behavioral segmentation | 4 profile cards, active vs inactive bar, funnel, gender bar |
| 📦 Products | Product depth analysis | Churn by product count, heatmap, treemap, box plot |
| ⚠️ Premium Risk | Silent churn detection | Balance vs salary scatter, at-risk table, downloadable CSV |
| 💪 Retention Score | RSI scoring & sticky profiles | RSI gauge, radar chart, stability tiers, sticky customer summary |

---

## 🗂 Project Structure

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

---

## ⚙️ Setup & Run

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

---

## 🔢 Derived Features

| Column | Description |
|--------|-------------|
| `EngagementProfile` | 4-class label combining activity + product count |
| `RSI` | Relationship Strength Index (0–100) |
| `PremiumAtRisk` | Flag: top-quartile balance + inactive |
| `BalanceSegment` | Binned balance buckets (Zero / 1–50K / 50–100K / 100–150K / 150K+) |
| `AgeBand` | Age decade bands (<30 / 30–40 / 40–50 / 50–60 / 60+) |
| `CreditBand` | Credit score categories (Poor / Fair / Good / Excellent) |

---

## 📐 RSI Formula

The **Relationship Strength Index** is a composite 0–100 loyalty score built from five behavioral signals:

```
RSI = IsActiveMember      × 30   (activity — strongest signal)
    + NumOfProducts       × 15   (product depth, capped at 4)
    + HasCrCard           × 10   (credit card stickiness)
    + (Tenure / max)      × 25   (relationship length)
    + (Balance > 0)       × 20   (financial commitment)
```

| RSI Range | Customer Type | Action |
|-----------|--------------|--------|
| 0 – 40 | 🔴 High flight risk | Immediate retention intervention |
| 40 – 65 | 🟡 Needs nurturing | Targeted engagement campaigns |
| 65 – 100 | 🟢 Sticky / loyal | Cross-sell and upsell |

---

## 📚 What I Learned From This Project

This project taught me that data analytics is not just about building charts — it is about **answering business questions that drive real decisions**.

Through this project I learned:

- How to engineer behavioral features from raw transactional data
- How to design a multi-tab dashboard with real-time filtering
- How to translate data findings into actionable business recommendations
- How to build a composite scoring metric (RSI) that non-technical stakeholders can understand and act on
- That **what a customer does** matters far more than **who a customer is**

---

## 🚀 What's Next?

This is one milestone in a broader data analytics journey. Future directions include:

- Adding **machine learning churn prediction** (logistic regression, gradient boosting) for individual-level probability scoring
- Incorporating **transaction-level data** for richer behavioral signals
- Building a **longitudinal RSI tracker** to detect customers whose score is declining over time
- Deploying on **Streamlit Cloud** for stakeholder access without local setup

---

## 💬 Feedback

If you have suggestions on additional insights to explore, model improvements, or dashboard features, feedback is always welcome.

Constructive ideas help make the analysis sharper and more useful for real-world decision-making.

---

## 👨‍💻 Author

**Shakeer Shaik**
Data Science & Analytics · Streamlit · Plotly · Python
*Customer Engagement Analytics · Behavioral Segmentation · Retention Strategy*

---

## 🏛 Unified Mentor

**European Central Bank**
*This project was developed under the European Central Bank's Customer Engagement & Product Utilization Analytics for Retention Strategy program.*
