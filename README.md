# ⚽ Top 5 European Leagues Football (2025/2026)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg)
![Pandas](https://img.shields.io/badge/Data%20Analysis-Pandas-blue.svg)
![Plotly](https://img.shields.io/badge/Visualization-Plotly-red.svg)

---

An end-to-end data science and business intelligence pipeline designed to objectively evaluate team performance, tactical identity, and competitive equilibrium across Europe's Top 5 Leagues (Premier League, LaLiga, Ligue 1, Serie A, and Bundesliga).

By condensing 20+ match metrics into a two-axis, using Principal Component Analysis (PCA) matrix and applying K-Means clustering, this framework bridges the gap between raw Python execution and executive-level football operations.

---

## 📋 Table of Contents

1. [Business Objective & Strategic Utility](#-business-objective--strategic-utility)
2. [Data Pipeline & Normalization](#-data-pipeline--normalization)
3. [Machine Learning & Methodology](#-machine-learning--methodology)
   - [Sub-Domain PCA: The Tactical Matrix](#sub-domain-pca-the-tactical-matrix)
   - [K-Means Tactical Archetypes](#k-means-tactical-archetypes)
4. [Macro-Level League Insights](#-macro-level-league-insights)
5. [Interactive Dashboard Features](#-interactive-dashboard-features)
6. [Future Work](#-future-work)
7. [Technical Stack & Tools](#-technical-stack--tools)
8. [Repository Structure](#-repository-structure)
9. [Getting Started](#-getting-started)

---

## 🎯 Business Objective & Strategic Utility

Modern football scouting and executive decision-making often rely on fragmented surface-level metrics (e.g., raw goal totals or possession percentages) that are susceptible to tactical bias and league-quality inflation. This repository addresses those challenges by providing front offices with tools to:

* **Identify Tactical Archetypes:** Group 96 clubs across 5 leagues into playstyle-based clusters independent of domestic standings.
* **Evaluate Managerial Efficiency:** Diagnose systemic issues or Undervalued tactics 
* **Optimize Scouting & Resource Allocation:** Identify specific league characteristics allowing data-backed decision-making when recruiting players (top-heavy leagues, highly diverse tactical environments...)

---

## 🧹 Data Pipeline & Normalization

The underlying dataset covers 96 clubs across five top-flight domestic leagues:

* **Automated Data Extraction:** Web scraping pipeline built with `Selenium` and `BeautifulSoup` to ingest dynamic match stats and team performance logs.
* **Stats Normalization:** Accounted for match count discrepancies across leagues (34 matches in Bundesliga/Ligue 1 vs. 38 in EPL/LaLiga/Serie A) by programmatically normalizing all volume metrics:
  $$\text{Per-90 Metric} = \frac{\text{Season Total}}{\text{Total Games Played}} \times 90$$
* **Feature Engineering:** Calculated custom conversion rates (e.g., Big Chance Conversion %, Pass Success %) and derived metrics while removing redundant features.
* **Feature Scaling:** Standardized all sub-domain variables using `StandardScaler` ($\mu = 0, \sigma^2 = 1$) to prevent high-volume passing metrics from distorting low-volume defensive attributes.

---

## 🤖 Machine Learning & Methodology

### PCA: The Tactical Matrix

Rather than fitting a single global model, metrics were separated into two distinct tactical sub-domains to isolate **Performance** from **Game Control**:

1. **Performance Score (56.78% Variance Explained, Eigenvalue = 3.442):**
   * *Features:* Goals Scored/90, xG/90, Goals Conceded/90 (negative loading), xG Conceded/90 (negative loading), Shot Conversion %, Big Chance Conversion %.
   * *Strategic Meaning:* Quantifies overall clinical efficiency and defensive stability.

2. **Game Control Score (47.18% Variance Explained, Eigenvalue = 5.245):**
   * *Features:* Possession %, Passes/90, Touches in Opposition Box/90, Possession Won Attacking 3rd/90, Clearances/90 (negative loading), Long Balls/90 (negative loading).
   * *Strategic Meaning:* Measures game dominance and tactical identity (proactive, possession, reactive, direct...)

<img width="1321" height="461" alt="image" src="https://github.com/user-attachments/assets/25e18745-3014-47ee-9263-e1c62e704516" />

#### Quadrant Profiling Matrix:
* **Top-Right (High Control, High Performance):** The Proactive Elite (e.g., Real Madrid, PSG, Bayern Munich).
* **Bottom-Right (Low Control, High Performance):** Sustainable & Effective Counter-Attackers.
* **Top-Left (High Control, Low Performance):** Sterile Possessors (High ball dominance, severe lack of penetration).
* **Bottom-Left (Low Control, Low Performance):** Reactive/Pragmatic Survivors fighting relegation.

### K-Means Tactical Archetypes

Applied unsupervised K-Means clustering across Game Control metrics, using the **Elbow Method** (Sum of Squared Errors) to determine the optimal $K=4$ clusters:

* **Cluster 0 — Deep Block / Direct Teams (36 Teams):** Reactive, low-possession, heavy clearance reliance.
* **Cluster 1 — Elite Dominators (14 Teams):** Dominant possession, high pressing in attacking 3rd, high box touch volume.
* **Cluster 2 — Transition Specialists (19 Teams):** Balanced possession, vertical progression, strong mid-block structure.
* **Cluster 3 — High-Pressing Workhorses (27 Teams):** Intense pressing turnover rates with varied possession dominance.

---

## 📊 Macro-Level League Insights

Using **Median Absolute Deviation (MAD)** on PCA component axes, custom macro metrics were constructed to evaluate competitive structure across domestic leagues:

```text
League Strength/Level Gap Ranking (Performance Axis MAD):
1. Germany  (MAD: 1.284)  --> Highest internal inequality (Top-heavy power concentration)
2. Italy    (MAD: 1.259)
3. France   (MAD: 1.070)
4. Spain    (MAD: 0.682)
5. England  (MAD: 0.612)  --> Highest competitive parity bottom-to-top

League Tactical Diversity Ranking (Game Control Axis MAD):
1. France   (MAD: 1.898)  --> Most varied tactical spectrum (Elite testing ground for adaptability)
2. Italy    (MAD: 1.821)
3. Germany  (MAD: 1.492)
4. England  (MAD: 1.434)
5. Spain    (MAD: 0.644)  --> Most homogeneous playstyle distribution
