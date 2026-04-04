"""
check_files.py
Run this from your project root:  python check_files.py
It will tell you exactly which files are old and need replacing.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

checks = {
    "config.py": "COLOR_RETAINED",
    "utils.py": "CreditBand",
    "components/charts.py": "import sys, os",
    "components/kpi_cards.py": "import sys, os",
    "components/sidebar.py": "import sys, os",
    "pages/overview.py": "import sys, os",
    "pages/engagement.py": "bar_churn_by_profile, stacked_active_by_geo",
    "pages/products.py": "import sys, os",
    "pages/premium_risk.py": "import sys, os",
    "pages/retention_score.py": "import sys, os",
}

print("\n🔍 Checking file versions...\n")
all_ok = True
for filepath, expected_text in checks.items():
    full_path = os.path.join(ROOT, filepath)
    if not os.path.exists(full_path):
        print(f"  ❌ MISSING  — {filepath}")
        all_ok = False
        continue
    content = open(full_path, encoding="utf-8").read()
    if expected_text in content:
        print(f"  ✅ OK       — {filepath}")
    else:
        print(f"  ❌ OLD FILE — {filepath}  (missing: '{expected_text}')")
        all_ok = False

print()
if all_ok:
    print("✅ All files are up to date. Run:  streamlit run app.py")
else:
    print("❌ Replace the files marked OLD FILE above with the new downloaded versions.")
print()
