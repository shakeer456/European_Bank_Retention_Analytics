"""
utils.py — Data loading and feature engineering
All derived columns are built once here; every page reuses them.
"""
import pandas as pd
import numpy as np


def load_and_engineer(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # ── Engagement Profile ────────────────────────────────────────────────
    conditions = [
        (df['IsActiveMember'] == 1) & (df['NumOfProducts'] >= 2),
        (df['IsActiveMember'] == 0) & (df['NumOfProducts'] >= 2),
        (df['IsActiveMember'] == 1) & (df['NumOfProducts'] == 1),
        (df['IsActiveMember'] == 0) & (df['NumOfProducts'] == 1),
    ]
    labels = [
        'Active engaged',
        'Inactive multi-product',
        'Active low-product',
        'Inactive disengaged',
    ]
    df['EngagementProfile'] = np.select(conditions, labels, default='Unknown')

    # ── Relationship Strength Index (RSI) 0–100 ───────────────────────────
    tenure_max = df['Tenure'].max()
    tenure_norm = df['Tenure'] / tenure_max if tenure_max > 0 else 0

    df['RSI'] = (
        df['IsActiveMember'] * 30
        + df['NumOfProducts'].clip(1, 4) * 15
        + df['HasCrCard'] * 10
        + tenure_norm * 25
        + (df['Balance'] > 0).astype(int) * 20
    ).clip(0, 100)

    # ── Premium at-risk flag ──────────────────────────────────────────────
    bal_75 = df['Balance'].quantile(0.75)
    df['PremiumAtRisk'] = (
        (df['Balance'] >= bal_75) & (df['IsActiveMember'] == 0)
    ).astype(int)

    # ── Balance segment ───────────────────────────────────────────────────
    df['BalanceSegment'] = pd.cut(
        df['Balance'],
        bins=[-1, 0, 50_000, 100_000, 150_000, 999_999],
        labels=['Zero', '1–50K', '50–100K', '100–150K', '150K+'],
    )

    # ── Age band ──────────────────────────────────────────────────────────
    df['AgeBand'] = pd.cut(
        df['Age'],
        bins=[0, 30, 40, 50, 60, 120],
        labels=['<30', '30–40', '40–50', '50–60', '60+'],
    )

    # ── Credit score band ─────────────────────────────────────────────────
    df['CreditBand'] = pd.cut(
        df['CreditScore'],
        bins=[0, 550, 650, 750, 850],
        labels=['Poor (<550)', 'Fair (550–650)',
                'Good (650–750)', 'Excellent (750+)'],
    )

    return df
