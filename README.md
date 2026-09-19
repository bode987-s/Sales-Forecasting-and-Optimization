# Sales Forecasting & Optimization

## Overview

This project explores how historical retail data can be used to
forecast sales and support better inventory and business decisions.

The workflow covers the complete process, from preparing the dataset
and identifying useful patterns to training a forecasting model and
deploying it through an application.

## Project Objectives

- Analyze historical retail sales data
- Identify factors associated with changes in demand
- Build and compare multiple machine-learning models
- Evaluate model performance using standard regression metrics
- Develop a workflow for tracking and monitoring the model
- Provide a deployable interface for making predictions

## Dataset

The project uses the `retail_store_inventory.csv` dataset obtained
from Kaggle.

The dataset contains 73,100 records and 15 variables, including:

- Date
- Store and product identifiers
- Product category
- Region
- Inventory level
- Units sold
- Demand forecast
- Weather conditions
- Holidays and promotions

## Analysis

The exploratory analysis focused on sales patterns and the relationship
between sales and factors such as discounts, promotions, holidays,
and weather.

Statistical analysis included correlation analysis, a hypothesis test
for holiday effects, and ANOVA to investigate weather-related effects.

## Forecasting Models

Several regression approaches were evaluated:

| Model | Train R² | Test R² | MAE | RMSE |
|---|---:|---:|---:|---:|
| Linear Regression | 0.9937 | 0.9937 | 7.47 | 8.65 |
| Decision Tree | 1.0000 | 0.9871 | 10.12 | 12.39 |
| KNN | 0.9608 | 0.9430 | 21.00 | 26.06 |

Based on the reported evaluation results, Linear Regression was used
as the main forecasting model because it provided strong test
performance while remaining easy to interpret.

## MLOps & Deployment

The project also includes components for taking the model beyond
experimentation:

- MLflow for experiment/model tracking
- Streamlit for the prediction interface
- Performance monitoring
- Data/model drift alerts
- Stakeholder-facing dashboards

## Business Applications

The forecasting results can support decisions related to:

- Inventory planning
- Avoiding excessive stock
- Reducing stockout risk
- Promotion and pricing decisions
- Sales planning

## Future Improvements

Possible extensions include:

- Testing XGBoost and Prophet
- Adding more historical data for stronger seasonal analysis
- Introducing A/B testing
- Incorporating feedback from actual operational usage

## Tech Stack

- Python
- pandas
- scikit-learn
- MLflow
- Streamlit
