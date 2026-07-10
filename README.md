# LaLiga-Teams-Analysis (2025/2026)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg)
![Pandas](https://img.shields.io/badge/Data%20Analysis-Pandas-blue.svg)

## Project Overview

This project applies machine learning and statistical analysis to 41 distinct team performance metrics from the La Liga 2025/2026 season. The goal is to move beyond basic descriptive statistics (like possession or goals scored) to mathematically quantify **Tactical Identity** and **Overall Performance**.

The repository culminates in a comprehensive Sub-Domain Principal Component Analysis (PCA) that objectively maps team philosophies and identifies structural anomalies within the league.

## Table of Contents

1. [Data Pipeline & Preprocessing](#data-pipeline--preprocessing)
2. [K-Means Clustering: Tactical Profiles](#k-means-clustering-tactical-profiles)
3. [Sub-Domain PCA: The Tactical Matrix](#sub-domain-pca-the-tactical-matrix)
4. [Future Work](#future-work)

## Data Pipeline & Preprocessing

The dataset consists of 41 variables covering attacking, defensive, buildup, and set-piece phases of play.

**Key Cleaning & Scaling Steps:**

* **Metric Standardization:** Prioritized `/90` and `(%)` metrics over raw totals to eliminate possession bias
* **Feature Scaling:** Applied `StandardScaler` (Mean = 0, Variance = 1) prior to any distance-based algorithms (K-Means, PCA) to ensure percentage metrics and volume metrics were weighted equally.
* **Dimensionality Reduction & Multicollinearity:** Addressed highly correlated variables (e.g., `Goals_scored` and `xG`) through feature grouping and PCA.

## K-Means Clustering: Tactical Profiles

Instead of analyzing all 41 variables simultaneously, the features were grouped into four distinct tactical domains. K-Means clustering was applied to each domain to categorize La Liga teams into discrete tactical buckets.

* **Attacking Threat (Optimal K=2):** Separated the elite goal-scoring outliers (e.g., Real Madrid, Barcelona) from the rest of the league.
* **Defensive Solidity (Optimal K=2):** Differentiated high-pressing teams (`Possession_won_attacking_3rd/90`) from deep, low-block defensive teams (`Clearances/90`).
* **Buildup Play (Optimal K=2):** Successfully isolated pure possession-based teams from direct, transition-heavy teams based on passing accuracy, cross volume...
* **Set Pieces (Optimal K=3):** Identified Set-Piece Dominators, Defensively Vulnerable teams, and middle-of-the-pack performers.

*Visualized via Normalized Parallel Coordinate Plots (see `/notebooks`).*

## Principal Component Analysis: The Tactical Matrix

1. **X-Axis (Performance):** A PCA model trained *only* on Attacking/Defensive output metrics (xG, Goal Difference, Shots on Target, etc.). Extracts PC1 as a measure of overall quality.
2. **Y-Axis (Identity):** A second PCA model trained *only* on Buildup metrics (Possession, Clearances, Long Balls). Extracts PC1 as a measure of Proactive vs. Reactive ball management.

**The Result:** A clean, 4-quadrant tactical matrix separating the league into:

* **Top-Right:** The Proactive Elite (High Quality, High Possession)
* **Bottom-Right:** The Effective Pragmatists (High Quality, Direct/Reactive)
* **Top-Left:** The Aspirational Possessors (Low Quality, High Possession)
* **Bottom-Left:** The Pragmatic Survivors (Low Quality, Direct/Reactive)

## Future Work
Transition the static end-of-season PCA models into a chronological rolling-window pipeline (e.g., 5-match rolling average). This will allow for the tracking of a team's tactical evolution over the season to quantify the impact of real-world events:

* **Managerial Changes:** Mathematically capture whether a new coach implements a different tactical system and evaluate its immediate success.

* **Injury Crises:** Measure how the loss of key personnel forces structural changes to a team's build-up or defensive solidity.

* **Transfer Window Impact:** Analyze how mid-season signings or departures alter a team's identity and overall performance trajectory.

* **European Top 5 Leagues Expansion:** Scale the pipeline across Europe's Top 5 leagues simultaneously, fitting a single global PCA model to place all 90+ clubs and apply league-based hue mapping to evaluate whether modern football has completely homogenized playstyles or if distinct domestic cultural identities still dominate.
