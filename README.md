# OMO-and-Repo-Rate-analysis-
# Central Bank OMO & Repo Rate Policy Analysis

A Python-based data analysis pipeline for modeling, cleaning, and evaluating central bank monetary policy instruments—specifically Open Market Operations (OMO) and Repo/Reverse Repo rate adjustments—and analyzing their correlation with Consumer Price Index (CPI) inflation dynamics.

---

## Key Features

- **Unstructured Data Cleaning (Regex):** Parses raw text strings containing OMO transaction volumes and flags directionality (Liquidity Injection vs. Liquidity Absorption).
- **Feature Engineering:** Calculates the Policy Corridor Spread (`Repo Rate - Reverse Repo Rate`) and Month-over-Month (MoM) CPI Inflation percentage changes.
- **Z-Score Anomaly Detection:** Identifies statistical outliers in OMO liquidity operations using $Z$-score thresholds ($\vert{}Z\vert{} > 2.0$).
- **Correlation Analysis:** Evaluates policy effectiveness by computing Pearson correlation between Net OMO volume and CPI inflation rates.
- **Data Visualizations:**
  - **Policy Rate Trends:** Line charts comparing Repo Rate and Reverse Repo Rate trajectory over time.
  - **Policy Effectiveness Matrix:** Scatter plot mapping OMO liquidity volumes against CPI inflation with highlighted statistical anomalies.
- **Data Export:** Exports processed, feature-engineered datasets directly to `rbi-policy-data-analyzed.csv`.

---

## Tech Stack

- **Language:** Python 3.8+
- **Data Manipulation:** `pandas`, `numpy`
- **Pattern Matching:** `re` (Regular Expressions)
- **Data Visualization:** `matplotlib`

---

## Dataset Schema

The pipeline generates and transforms the following dataset attributes:

| Column | Type | Description |
| :--- | :--- | :--- |
| `Date` | `datetime` | Observation period (Monthly) |
| `RepoRate` | `float` | Central Bank Lending Rate (%) |
| `RevRepoRate` | `float` | Central Bank Borrowing Rate (%) |
| `CPIInfl` | `float` | Consumer Price Index Inflation Rate (%) |
| `OMONet` | `int` | Net OMO Volume (+ Injection / - Absorption in Crores) |
| `PolicySpread` | `float` | Interest rate corridor spread (`Repo - RevRepo`) |
| `MoMInflChg` | `float` | Percentage change in CPI Inflation |
| `OMOZ` | `float` | Standardized $Z$-score of OMO volumes |
| `Anomaly` | `string` | Outlier classification (`Normal` vs. `Anomaly`) |

---

## Quickstart & Execution

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/omo-repo-analysis.git](https://github.com/your-username/omo-repo-analysis.git)
   cd omo-repo-analysis
