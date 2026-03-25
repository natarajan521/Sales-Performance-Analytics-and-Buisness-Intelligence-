# ============================================================
# Sales Performance Analytics and Business Insights
# Dataset: Sample - Superstore
# Tools: Python | Pandas | Matplotlib | Seaborn
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", palette="muted")

# ------------------------------------------------------------------
# SECTION 1: DATA LOADING & PREPROCESSING
# ------------------------------------------------------------------

# Locate the CSV (handles both 'Sample - Superstore.csv' and
# 'Sample - Superstore.csv.csv' filenames)
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # __file__ is not set when executing code inside some notebook cells
    BASE_DIR = os.getcwd()
possible_names = [
    "Sample - Superstore.csv.csv",
    "Sample - Superstore.csv",
]
csv_path = None
for name in possible_names:
    candidate = os.path.join(BASE_DIR, name)
    if os.path.exists(candidate):
        csv_path = candidate
        break

if csv_path is None:
    raise FileNotFoundError(
        "Superstore CSV not found. Place 'Sample - Superstore.csv' "
        f"in: {BASE_DIR}"
    )

print(f"[INFO] Loading dataset from: {csv_path}\n")
try:
    df = pd.read_csv(csv_path, encoding="latin-1")
except Exception as e:
    raise RuntimeError(f"Failed to read CSV file at {csv_path}: {e}") from e

# --- Basic info ---
print("=== Dataset Overview ===")
print(f"Shape          : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Missing values : {df.isnull().sum().sum()}")
print(f"Duplicate rows : {df.duplicated().sum()}\n")

# Remove missing values & duplicates
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# Convert Order Date to datetime
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=False)

# Extract Month and Year for time-based analysis
df["Year"]       = df["Order Date"].dt.year
df["Month"]      = df["Order Date"].dt.month
df["Month-Year"] = df["Order Date"].dt.to_period("M")

print(f"Records after cleaning: {df.shape[0]} rows\n")

# ------------------------------------------------------------------
# SECTION 2: EXPLORATORY DATA ANALYSIS (EDA)
# ------------------------------------------------------------------

print("=" * 50)
print("SECTION 2 — EXPLORATORY DATA ANALYSIS")
print("=" * 50)

# --- Key Metrics ---
total_sales   = df["Sales"].sum()
total_profit  = df["Profit"].sum()
avg_profit    = df["Profit"].mean()
profit_margin = (total_profit / total_sales) * 100

print(f"\n📦 Total Sales         : ${total_sales:,.2f}")
print(f"💰 Total Profit        : ${total_profit:,.2f}")
print(f"📊 Average Profit      : ${avg_profit:,.2f}")
print(f"📈 Overall Profit Margin: {profit_margin:.2f}%")

# --- Sales & Profit by Category ---
print("\n--- Sales & Profit by Category ---")
category_summary = (
    df.groupby("Category")[["Sales", "Profit"]]
    .sum()
    .sort_values("Sales", ascending=False)
)
print(category_summary.to_string())

# --- Sales & Profit by Region ---
print("\n--- Sales & Profit by Region ---")
region_summary = (
    df.groupby("Region")[["Sales", "Profit"]]
    .sum()
    .sort_values("Sales", ascending=False)
)
print(region_summary.to_string())

# --- Sales & Profit by Segment ---
print("\n--- Sales & Profit by Segment ---")
segment_summary = (
    df.groupby("Segment")[["Sales", "Profit"]]
    .sum()
    .sort_values("Sales", ascending=False)
)
print(segment_summary.to_string())

# --- Top 10 Products by Sales ---
print("\n--- Top 10 Products by Sales Revenue ---")
top10_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
print(top10_products.to_string(index=False))

# ------------------------------------------------------------------
# SECTION 3: DATA VISUALIZATION
# ------------------------------------------------------------------

print("\n\n" + "=" * 50)
print("SECTION 3 — GENERATING VISUALIZATIONS")
print("=" * 50)

CHART_DIR = BASE_DIR   # Save PNGs in the project root

# ── Chart 1: Monthly Sales Trend (Line Chart) ─────────────────────
monthly_sales = (
    df.groupby("Month-Year")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Month-Year")
)
monthly_sales["Month-Year-str"] = monthly_sales["Month-Year"].astype(str)

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(
    monthly_sales["Month-Year-str"],
    monthly_sales["Sales"],
    marker="o",
    linewidth=2,
    color="#2563EB",
    markerfacecolor="#EF4444",
    markersize=5,
)
ax.fill_between(
    monthly_sales["Month-Year-str"],
    monthly_sales["Sales"],
    alpha=0.12,
    color="#2563EB",
)
ax.set_title("Monthly Sales Trend", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Month-Year", fontsize=12)
ax.set_ylabel("Total Sales ($)", fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
step = max(1, len(monthly_sales) // 12)
tick_positions = list(range(0, len(monthly_sales), step))
ax.set_xticks(tick_positions)
ax.set_xticklabels(
    [monthly_sales["Month-Year-str"].iloc[i] for i in tick_positions],
    rotation=45, ha="right", fontsize=9,
)
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
out1 = os.path.join(CHART_DIR, "monthly_sales_trend.png")
plt.savefig(out1, dpi=150)
plt.close()
print(f"[SAVED] {out1}")

# ── Chart 2: Sales by Region (Bar Chart) ──────────────────────────
region_plot = region_summary.reset_index().sort_values("Sales", ascending=False)
colors_region = ["#2563EB", "#10B981", "#F59E0B", "#EF4444"]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(region_plot["Region"], region_plot["Sales"], color=colors_region, width=0.55, edgecolor="white")
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 8000,
        f"${bar.get_height():,.0f}",
        ha="center", va="bottom", fontsize=9, fontweight="bold",
    )
ax.set_title("Total Sales by Region", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Region", fontsize=12)
ax.set_ylabel("Total Sales ($)", fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.set_ylim(0, region_plot["Sales"].max() * 1.18)
plt.tight_layout()
out2 = os.path.join(CHART_DIR, "sales_by_region.png")
plt.savefig(out2, dpi=150)
plt.close()
print(f"[SAVED] {out2}")

# ── Chart 3: Sales & Profit by Category (Grouped Bar) ─────────────
cat_plot = category_summary.reset_index()
x        = range(len(cat_plot))
width    = 0.38

fig, ax = plt.subplots(figsize=(9, 5))
bars_s = ax.bar([i - width / 2 for i in x], cat_plot["Sales"],  width, label="Sales",  color="#2563EB", edgecolor="white")
bars_p = ax.bar([i + width / 2 for i in x], cat_plot["Profit"], width, label="Profit", color="#10B981", edgecolor="white")
for bar in bars_s:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 4000,
            f"${bar.get_height():,.0f}", ha="center", va="bottom", fontsize=8, color="#2563EB")
for bar in bars_p:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 4000,
            f"${bar.get_height():,.0f}", ha="center", va="bottom", fontsize=8, color="#10B981")
ax.set_title("Sales & Profit by Product Category", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Category", fontsize=12)
ax.set_ylabel("Amount ($)", fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.set_xticks(list(x))
ax.set_xticklabels(cat_plot["Category"], fontsize=11)
ax.legend(fontsize=11)
ax.set_ylim(0, cat_plot["Sales"].max() * 1.22)
plt.tight_layout()
out3 = os.path.join(CHART_DIR, "sales_profit_by_category.png")
plt.savefig(out3, dpi=150)
plt.close()
print(f"[SAVED] {out3}")

# ── Chart 4: Distribution of Profit (Histogram) ───────────────────
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(df["Profit"], bins=50, color="#6366F1", edgecolor="white", alpha=0.85)
ax.axvline(df["Profit"].mean(),   color="#EF4444", linestyle="--", linewidth=1.8, label=f"Mean  ${df['Profit'].mean():,.2f}")
ax.axvline(df["Profit"].median(), color="#F59E0B", linestyle="--", linewidth=1.8, label=f"Median ${df['Profit'].median():,.2f}")
ax.set_title("Distribution of Profit", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Profit ($)", fontsize=12)
ax.set_ylabel("Frequency", fontsize=12)
ax.legend(fontsize=11)
plt.tight_layout()
out4 = os.path.join(CHART_DIR, "profit_distribution.png")
plt.savefig(out4, dpi=150)
plt.close()
print(f"[SAVED] {out4}")

# ── Chart 5: Correlation Heatmap ──────────────────────────────────
corr_cols = ["Sales", "Profit", "Discount", "Quantity"]
corr_matrix = df[corr_cols].corr()

fig, ax = plt.subplots(figsize=(7, 5))
mask = None
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5,
    linecolor="white",
    annot_kws={"size": 12},
    ax=ax,
    vmin=-1, vmax=1,
    square=True,
)
ax.set_title("Correlation Heatmap\n(Sales, Profit, Discount, Quantity)", fontsize=14, fontweight="bold", pad=15)
plt.tight_layout()
out5 = os.path.join(CHART_DIR, "correlation_heatmap.png")
plt.savefig(out5, dpi=150)
plt.close()
print(f"[SAVED] {out5}")

# ------------------------------------------------------------------
# SECTION 4: BUSINESS INSIGHTS
# ------------------------------------------------------------------

print("\n\n" + "=" * 50)
print("SECTION 4 — BUSINESS INSIGHTS")
print("=" * 50)

# ── Prepare key data for insights ─────────────────────────────────
top_category      = category_summary["Sales"].idxmax()
low_profit_cat    = category_summary[category_summary["Profit"] < 0]
top_region        = region_summary["Sales"].idxmax()
low_region        = region_summary["Sales"].idxmin()
margin_by_cat     = (category_summary["Profit"] / category_summary["Sales"] * 100).round(2)

# INSIGHT 1: Technology leads all categories in revenue
print(f"\n💡 Insight 1 — Top Revenue Category:")
print(f"   '{top_category}' generates the highest sales revenue.")
print(f"   Profit margin breakdown by category:")
for cat, margin in margin_by_cat.items():
    print(f"     {cat:<20} : {margin:.2f}% margin")

# INSIGHT 2: West and East dominate regional sales; South lags behind
print(f"\n💡 Insight 2 — Regional Sales Performance:")
print(f"   Highest sales region : {top_region}  (${region_summary.loc[top_region]['Sales']:,.0f})")
print(f"   Lowest  sales region : {low_region}  (${region_summary.loc[low_region]['Sales']:,.0f})")
print(f"   → Invest more in the {low_region} region to unlock untapped potential.")

# INSIGHT 3: Furniture has high sales but significantly lower profit margins
# compared to Technology — heavy discounts or logistics costs erode margins.
furniture_margin = margin_by_cat.get("Furniture", 0)
tech_margin      = margin_by_cat.get("Technology", 0)
print(f"\n💡 Insight 3 — High Sales, Low Profit (Furniture vs Technology):")
print(f"   Furniture  profit margin: {furniture_margin:.2f}%")
print(f"   Technology profit margin: {tech_margin:.2f}%")
print(f"   → Furniture discounting strategy needs review to protect margins.")

# INSIGHT 4: Discount has a strong negative correlation with Profit.
# Reducing excessive discounts (especially in Furniture & Office Supplies)
# could significantly improve overall profitability.
discount_profit_corr = df[["Discount", "Profit"]].corr().iloc[0, 1]
print(f"\n💡 Insight 4 — Discount Impact on Profit:")
print(f"   Discount ↔ Profit correlation: {discount_profit_corr:.3f}")
print(f"   → Higher discounts strongly reduce profit. Cap discounts at 20%.")

# INSIGHT 5: Consumer segment accounts for the largest share of sales.
# Targeting Corporate and Home Office segments with tailored promotions
# could diversify revenue and reduce segment concentration risk.
seg_sales_share = (segment_summary["Sales"] / segment_summary["Sales"].sum() * 100).round(2)
top_segment     = seg_sales_share.idxmax()
print(f"\n💡 Insight 5 — Segment Revenue Concentration:")
for seg, share in seg_sales_share.items():
    print(f"   {seg:<15} : {share:.2f}% of total sales")
print(f"   → '{top_segment}' dominates. Grow Corporate/Home Office segments.")

print("\n✅ Analysis complete — all charts saved to project folder.\n")
