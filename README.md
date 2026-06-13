# 📊 Global Supply Chain & Market Intelligence Audit
**Case Study:** Maritime Logistics & Commodity Trading Analysis (Northwind Database Pipeline)

---

## 📌 Executive Summary
This project simulates the role of a Quantitative Data Analyst in a commodity intelligence firm. Utilizing global transaction logs, I built SQL pipelines to audit maritime shipping efficiencies, isolate logistical cost anomalies, and map commodity sector dominance across international markets.

---

## 🛠️ Technical Implementation & SQL Scripts

The core structural queries are implemented directly within this repository. Below are the key highlights of the analytical execution:

### 🔵 Phase 1: Vessel Shipping Efficiency Audit (Medium Level)
Tracks the exact transit duration (arrival vs. departure dates) and average freight costs across different vessel couriers to optimize European trade routes.
* **Key Skills:** `INNER JOIN`, `JULIANDAY` date arithmetic, `GROUP BY`, `Aggregate Functions`.
* **Script:** [1_shipping_efficiency_audit.sql](1_shipping_efficiency_audit.sql)

### 🟢 Phase 2: Logistical Cost Anomaly Detection (Semi-Advanced Level)
Employs correlated subqueries to automatically flag shipments where the actual freight cost spikes over 250% above the historical country destination baseline.
* **Key Skills:** `Correlated Subqueries`, `Conditional Logic (CASE WHEN)`.
* **Script:** [2_freight_anomaly_detection.sql](2_freight_anomaly_detection.sql)

### 🔴 Phase 3: Market Share & Commodity Dominance (Advanced Level)
Computes the exact revenue generation per product category per country, utilizing window functions to evaluate the percentage market share contribution of each commodity sector.
* **Key Skills:** `Common Table Expressions (CTEs)`, `Window Functions (SUM OVER PARTITION)`.
* **Script:** [3_market_share_intelligence.sql](3_market_share_intelligence.sql)

---
## ⚙️ Automated ETL Pipeline & Data Quality Engineering (Python)

To mature the analytical models from ad-hoc SQL queries into a scalable asset, I developed a production-ready Python ETL pipeline utilizing **Pandas** and **SQLAlchemy**.

* **Robust Anomaly Mitigation:** Instead of a fragile historical mean, the Python pipeline implements a dynamic **Median-based Outlier Threshold ($2.5 \times \text{Median}$)** grouped by country. This guarantees long-term adaptability against global freight price drift or market inflation.
* **Database Persistence & Restructuring:** The pipeline automates data extraction, transformation, and load (`.to_sql`) routines back into the database, instantly creating a clean, analytics-ready layer (`fact_bunker_clean`) for downstream BI dashboarding.
* **Automated Scripts:**
  * `pipeline.py`: Code containing the full maritime core logic from database connection to outlier handling.
  * `check_database.py`: A dedicated verification script ensuring zero data leakage and strict database structural constraints before runtime.
---

## 📈 Strategic Business Insights
* **High-Priority Trade Corridor:** The *Beverages* sector heavily dominates the German market, contributing over 35-40% of the calculated regional import value. Supply chain stability to major German ports must be heavily prioritized.
* **Financial Risk Mitigation:** Automated flags successfully isolated severe freight cost deviations in multiple US and Austrian trade lines, indicating potential localized supply disruptions or vendor overcharging.
