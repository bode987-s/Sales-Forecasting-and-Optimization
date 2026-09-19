
# 📊 IBM Data Science Project: Sales Forecasting and Optimization

## 🧭 Project Overview
This project aims to predict future sales for a retail business using historical sales data. The process includes:
📥 Data collection → 🧹 Cleaning → 🔍 Exploration → 🤖 Model development → 🛠️ Optimization → 🚀 Deployment.

🎯 **Goal:** Create an accurate prediction model to help businesses optimize inventory, marketing, and sales strategies.

---

## 👥 Contributors
- 👑 **Abdallah Adel Abdallah**
- **Abdelrahman Adel Abdelkader**
- **Abdelrahman Badawy Ali**
- **Asmaa Muhammad Abdelhamid**
- **Maryam Taha Abdelaty**
- **Muhammed Ahmed Abdelmegeed**

📌 **Supervised by:** Eng. Islam Adel

---

## 🧩 Table of Contents
1. [Project Overview](#project-overview)
2. [Contributors](#contributors)
3. [Project Milestones](#project-milestones)
4. [Business Impact](#business-impact)
5. [Limitations & Future Work](#limitations--future-work)
6. [Technologies Used](#technologies-used)
7. [Conclusion](#conclusion)

---

## 🛠️ Project Milestones

### 🥇 First Milestone: Data Collection and Exploration
- 📁 Dataset: Kaggle (`retail_store_inventory.csv`)
- 📊 Size: 73,100 rows × 15 columns
- 🔑 Key Features:
  - 🗓️ Date (Jan 2022)
  - 🏬 Store IDs (`S001`–`S005`), Product IDs (`P0001`–`P0020`)
  - 📦 Categories: Electronics, Clothing, Groceries, Toys, Furniture
  - 🌍 Region: North, South, East, West
  - 📈 Metrics: Inventory Level, Units Sold, Demand Forecast
  - 🌦️ External: Weather, Holidays/Promotions
- ✔️ Data Quality: No missing values or duplicates
- 💡 Insights:
  - Electronics had highest demand
  - East region led in sales
  - Discounts, price strongly correlated with sales

### 📉 Second Milestone: Data Analysis and Visualization
- 📐 Stats:
  - Correlation: Units Sold vs Discounts & Promotions
  - Hypothesis test: Holiday effect
  - ANOVA: Weather impact
- 📊 Visuals:
  - Monthly sales trends (2022–2023)
  - Sales vs Weather (low influence)
  - Promotions impact by category

### 🤖 Third Milestone: Forecasting Model Development
| Model               | 🏋️ Train R² | 🧪 Test R² | 📉 MAE  | 📉 RMSE |
|---------------------|------------|-----------|--------|--------|
| Linear Regression   | 0.9937     | 0.9937    | 7.47   | 8.65   |
| Decision Tree       | 1.0000     | 0.9871    | 10.12  | 12.39  |
| K-Nearest Neighbors | 0.9608     | 0.9430    | 21.00  | 26.06  |

✅ **Chosen Model:** Linear Regression
- Balanced metrics
- No overfitting
- High interpretability

### 🧱 Fourth Milestone: MLOps, Deployment, and Monitoring
- ⚙️ **MLOps:** MLflow for tracking + central server
- 🌐 **Deployment:** Streamlit app (real-time & batch)
- 📡 **Monitoring:**
  - Live performance tracking
  - Drift alerts
  - Dashboards for stakeholders

---

## 💼 Business Impact
- 📦 **Inventory Optimization:** Less stockouts/overstocking
- 💰 **Cost Efficiency:** 10% discount ≈ 15-unit sales boost
- 📊 **Decision-Making:** 99.37% forecast accuracy

---

## 🧪 Limitations & Future Work
- ⏳ **Limited Data:** Only 11 days (limits seasonal analysis)
- 🚀 **Model Upgrades:** Try Prophet, XGBoost
- 🔁 **Operational:** Add A/B testing + feedback loops

---

## 🧰 Technologies Used
- 🐍 Python
- 📈 pandas, scikit-learn
- 📊 MLflow
- 🌐 Streamlit

---

## 🏁 Conclusion
We successfully built a robust sales forecasting framework, achieving **99.37% accuracy** with low error (RMSE = 8.65).  
With an MLOps pipeline and a deployable app, the solution empowers businesses to make confident, data-driven inventory and marketing decisions.

--- 
