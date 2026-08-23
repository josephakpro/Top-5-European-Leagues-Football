# ⚽ Top 5 European Leagues Football Analysis & Dashboard

[![Live Dashboard](https://img.shields.io/badge/Render-Live%20Demo-brightgreen?logo=render)](https://top-5-european-leagues-football.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?logo=python)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg?logo=scikit-learn)](https://scikit-learn.org/)
[![Plotly Dash](https://img.shields.io/badge/Dashboard-Plotly%20Dash-red.svg?logo=plotly)](https://dash.plotly.com/)
[![Pandas](https://img.shields.io/badge/Data%20Analysis-Pandas-blue.svg?logo=pandas)](https://pandas.pydata.org/)

---

An end-to-end sports analytics and business intelligence project evaluating team performance, tactical profiles, and financial efficiency across Europe's top 5 domestic leagues (**Premier League (England), LaLiga (Spain), Ligue 1 (France), Serie A (Italy), and Bundesliga (Germany)**).

By condensing 20+ team-level stats and wage metrics through **Principal Component Analysis (PCA)** and **K-Means Clustering**, this project categorizes 96 clubs into distinct tactical archetypes and visualizes their performance in a deployed interactive web dashboard.

🔗 **Live Web Application:** [Top 5 European Leagues Football Dashboard](https://top-5-european-leagues-football.onrender.com/)

---

## 📋 Table of Contents

1. [Business Objective & Executive Utility](#-business-objective--executive-utility)
2. [Data Pipeline & Feature Engineering](#-data-pipeline--feature-engineering)
3. [Machine Learning & Methodology](#-machine-learning--methodology)
   - [PCA: Tactical Matrix](#sub-domain-pca-the-tactical-matrix)
   - [K-Means Tactical Archetypes](#k-means-tactical-archetypes)
4. [Macro-Level League & Financial Insights](#-macro-level-league--financial-insights)
5. [Interactive Dashboard Features](#-interactive-dashboard-features)
6. [Tech Stack](#-tech-stack)
7. [Repository Structure](#-repository-structure)
8. [Getting Started & Local Setup](#-getting-started--local-setup)

---

## 🎯 Business Objective & Executive Utility

Traditional scouting and front-office evaluations frequently rely on raw volume metrics (e.g., total goals, passes, or clean sheets) that are prone to tactical biases, match-count discrepancies, and league quality distortions. This project bridges raw statistical computing with strategic football operations to:

* **Categorize Tactical Archetypes:** Cluster 96 clubs across 5 leagues into playstyle profiles independent of domestic table standings.
* **Assess Tactical & Managerial Efficiency:** Diagnose systemic issues or undervalued tactics
* **Integrate Financial & Performance Context:** Contrast payroll distribution and estimated wages against on-pitch dominance to identify over- and under-performing squads.
---

## 🧹 Data Pipeline & Feature Engineering

The dataset consolidates match statistics and wage estimations across 96 clubs in the top 5 European leagues:

* **Automated Data Extraction:** Web scraping pipeline built with `Selenium` and `BeautifulSoup` to ingest dynamic match stats and team performance logs.
* **Season Length Normalization (Per-90 Metrics):** Handled domestic fixture discrepancies (34 matches in Bundesliga and Ligue 1 vs. 38 matches in Premier League, LaLiga, and Serie A) to standardize all volume metrics:
  $$\text{Metric / 90} = \frac{\text{Season Total}}{\text{Matches Played}} \times 90$$
* **Financial Data Integration:** Integrated club wage estimations (average salary in €M and total annual payroll in €M).  
  > *Note: Wage statistics are estimated club figures (sourced from FootyStats) for comparative performance context.*
* **Feature Engineering:** Calculated custom conversion rates (e.g., Big Chance Conversion %, Pass Success %) and derived metrics while removing redundant features.
* **Feature Scaling:** Applied `StandardScaler` to eliminate scale disparities between high and low volume metrics (Possession% or Goals per game)
* 
---

## 🤖 Machine Learning & Methodology

### PCA: The Tactical Matrix

To avoid conflating playstyle & dominance with efficiency (attacking and defending), the different metrics were decomposed into two distinct sub-domains:

1. **Performance Index:**
   * *Features:* Goals Scored/90, xG/90, Goals Conceded/90 (negative), xG Conceded/90 (negative), Shot Conversion %, Big Chance Conversion %.
   * *Strategic Focus:* Evaluates finishing clinicality, offensive threat, and defensive solidity.

2. **Game Control Index:**
   * *Features:* Possession %, Passes/90, Touches in Opposition Box/90, Possession Won in Attacking 3rd/90, Clearances/90 (negative), Long Balls/90 (negative).
   * *Strategic Focus:* Measures territorial dominance, build-up patience, and high-pressing intensity.

<img width="1321" height="461" alt="image" src="https://github.com/user-attachments/assets/25e18745-3014-47ee-9263-e1c62e704516" />

#### Tactical Quadrant Mapping
* **High Control & High Performance:** Proactive Elite (e.g., dominant title contenders maintaining both territory and clinical efficiency).
* **Low Control & High Performance:** Direct & Lethal Counter-Attackers (efficient transition units with low possession volume).
* **High Control & Low Performance:** Sterile Dominators (high possession and field tilt with inadequate box penetration or finishing).
* **Low Control & Low Performance:** Pragmatic & Reactive Survivors (deep-block structures battling relegation).

### K-Means Tactical Archetypes

Using the **Elbow Method** and **Silhouette Analysis** (combined with industry knowledge), $K=4$ was selected as the optimal cluster count to classify the different styles:

| Cluster | Archetype | Defining Characteristics |
| :--- | :--- | :--- |
| **Cluster 0** | **Deep Block / Direct Units** | Low possession, direct long-ball progression, high volume of clearances and defensive actions. |
| **Cluster 1** | **Elite Dominators** | High possession (>55%), high pressing in the final third, heavy penalty-box touch volume. |
| **Cluster 2** | **Transition Specialists** | Balanced possession, vertical transition play, resilient mid-block structure. |
| **Cluster 3** | **High-Pressing Workhorses** | Intensive defensive turnover generation, varied possession share, aggressive pressing actions. |

---

## 💻 Interactive Dashboard Features

The dashboard is deployed on Render and built with **Plotly Dash** to provide intuitive, multi-dimensional team evaluations:

* **Interactive Team Selector:** Filter clubs by domestic league to inspect individual tactical footprints.
* **Radar Chart:** Compare individual club metrics against both their tactical cluster average and the wider European top-5 average.
* **PCA Quadrant Scatter Plots:** Interactive scatter plots visualizing all 96 clubs across the Performance vs. Game Control axes with cluster coloring.
* **Financial vs. Performance Views:** Scatter visualizations mapping payroll allocations against tactical control and conversion rates.

---

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Data Processing & Analytics:** `pandas`, `numpy`
* **Machine Learning & Statistics:** `scikit-learn` (StandardScaler, PCA, KMeans)
* **Visualization & Web Application:** `plotly`, `plotly-express`, `dash`, `matplotlib`, `seaborn`
* **Deployment:** `Render` / `Gunicorn`

---

## 📁 Repository Structure

```text
├── .gitignore
├── Procfile                              # Render deployment command
├── requirements.txt                      # Project dependencies
├── app.py                                # Plotly Dash web dashboard application
├── Top_5_Soccer_Euro_Leagues.ipynb       # Core data cleaning, EDA, PCA & Clustering notebook
├── data/
│   ├── Raw_top5_euro_leagues_teams_stats/
│   │   ├── premierleague_team_stats.csv
│   │   ├── laliga_team_stats.csv
│   │   ├── bundesliga_team_stats.csv
│   │   ├── serieA_team_stats.csv
│   │   ├── ligue1_team_stats.csv
│   │   └── Salaries.csv
│   └── processed_top5_euro_leagues.csv
└── README.md
