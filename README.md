#  Sales Performance Analytics and Business Insights

A complete Python-based data analysis project built on the **Superstore Sales Dataset**, covering data cleaning, exploratory data analysis, visualizations, and actionable business insights.

---

##  Project Structure

```
Sales-Performance-Analytics-and-Buisness-Intelligence-/
│
├── Sample - Superstore.csv.csv   ← Dataset (latin-1 encoded)
├── sales_analysis.py             ← Main Python script (run in terminal / VS Code)
├── sales_analysis.ipynb          ← Jupyter Notebook (VS Code / Google Colab)
├── requirements.txt              ← Python dependencies
│
└── Generated Chart PNGs:
    ├── monthly_sales_trend.png
    ├── sales_by_region.png
    ├── sales_profit_by_category.png
    ├── profit_distribution.png
    └── correlation_heatmap.png
```

---

##  Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Python Script (VS Code / Terminal)
```bash
python sales_analysis.py
```

### 3. Run the Jupyter Notebook (VS Code)
Open `sales_analysis.ipynb` → **Run All Cells**

### 4. Run in Google Colab
1. Upload `sales_analysis.ipynb` and `Sample - Superstore.csv.csv` to Colab.
2. Run all cells.

---

##  Dataset

The CSV used is `Sample - Superstore.csv.csv` (original Superstore dataset). The file contains these columns:

- `Row ID`: Unique row identifier
- `Order ID`: Unique order identifier
- `Order Date`: Date order was placed
- `Ship Date`: Date order shipped
- `Ship Mode`: Shipping service used
- `Customer ID`: Unique customer identifier
- `Customer Name`: Customer name
- `Segment`: Customer segment (Consumer | Corporate | Home Office)
- `Country`: Country (all entries are United States)
- `City`, `State`, `Postal Code`: Location details
- `Region`: Region (West | East | Central | South)
- `Product ID`: Unique product identifier
- `Category`: Product category (Furniture | Office Supplies | Technology)
- `Sub-Category`: Detailed sub-category
- `Product Name`: Product description
- `Sales`: Sales revenue amount
- `Quantity`: Units sold
- `Discount`: Discount rate (0–1)
- `Profit`: Profit value (can be negative)

The script loads this dataset, applies cleaning, computes metrics, and builds visualizations.

---

##  Visualizations Generated

| # | Chart | File |
|---|---|---|
| 1 | Monthly Sales Trend (Line) | `monthly_sales_trend.png` |
| 2 | Sales by Region (Bar) | `sales_by_region.png` |
| 3 | Sales & Profit by Category (Grouped Bar) | `sales_profit_by_category.png` |
| 4 | Distribution of Profit (Histogram) | `profit_distribution.png` |
| 5 | Correlation Heatmap | `correlation_heatmap.png` |

---

##  Key Business Insights

1. **Technology** is the top-revenue category with the highest profit margins.
2. **West** region leads in sales; **South** lags and needs investment.
3. **Furniture** shows high sales volume but dangerously thin profit margins due to excessive discounting.
4. **Discount ↔ Profit** correlation is strongly negative — capping discounts at 20% is recommended.
5. **Consumer** segment dominates revenue; growing **Corporate** and **Home Office** segments will diversify risk.

---

##  Tech Stack

- **Python 3.x**
- **Pandas** — data loading, cleaning, and exploratory analysis
- **Matplotlib** — chart rendering, axis formatting, and PNG export
- **Seaborn** — better chart style and correlation heatmap

---

##  What's implemented (functions/workflow)

1. Data loading
   - Detect either `Sample - Superstore.csv.csv` or `Sample - Superstore.csv`
   - Read data with `pd.read_csv(..., encoding='latin-1')`
   - Fail fast with clear error message if the file is missing

2. Data preprocessing
   - Drop missing rows and duplicates: `df.dropna()` + `df.drop_duplicates()`
   - Parse `Order Date` to datetime (`pd.to_datetime`)
   - Create derived time columns: `Year`, `Month`, `Month-Year`

3. Descriptive metrics and grouping
   - Total sales, total profit, average profit, profit margin
   - Group by `Category`, `Region`, `Segment` and summarize `Sales`/`Profit`
   - Top 10 products by sales revenue

4. Visualization generation
   - Monthly sales trend line + shaded area
   - Sales by region bar chart with value labels
   - Sales/profit grouped bar chart for categories
   - Profit distribution histogram + mean/median lines
   - Correlation heatmap for `Sales`, `Profit`, `Discount`, `Quantity`

5. Insight reporting
   - Top and bottom performers by category, region, segment
   - Margin and discount-risk analysis
   - Print clear business recommendations

---

##  How to view output

- Script prints summary and insights to console
- Charts are saved to project root as PNG files (see file list above)
- Optional: run within notebook and display chart images inline by using `IPython.display.Image` if desired

