import sys
import importlib
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Interactive Retail Store Inventory Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv('retail_store_inventory.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['Price Diff'] = df['Price'] - df['Competitor Pricing']
    def get_season(m):
        if m in [3,4,5]: return 'Spring'
        if m in [6,7,8]: return 'Summer'
        if m in [9,10,11]: return 'Autumn'
        return 'Winter'
    df['Season'] = df['Date'].dt.month.map(get_season)
    df['YearMonth'] = df['Date'].dt.to_period('M').dt.to_timestamp()
    return df

# Load data
try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file 'retail_store_inventory.csv' not found.\nPlease place it in the same directory as this app.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filters")
min_date, max_date = st.sidebar.date_input(
    "Select Date Range", [df['Date'].min(), df['Date'].max()]
)
categories = st.sidebar.multiselect(
    "Category", options=df['Category'].unique(), default=list(df['Category'].unique())
)
regions = st.sidebar.multiselect(
    "Region", options=df['Region'].unique(), default=list(df['Region'].unique())
)
weathers = st.sidebar.multiselect(
    "Weather Condition", options=df['Weather Condition'].unique(), default=list(df['Weather Condition'].unique())
)
disc_range = st.sidebar.slider(
    "Discount Range (%)", float(df['Discount'].min()), float(df['Discount'].max()),
    (float(df['Discount'].min()), float(df['Discount'].max()))
)
price_range = st.sidebar.slider(
    "Price Range", float(df['Price'].min()), float(df['Price'].max()),
    (float(df['Price'].min()), float(df['Price'].max()))
)

# Apply Filters
mask = (
    (df['Date'] >= pd.to_datetime(min_date)) &
    (df['Date'] <= pd.to_datetime(max_date)) &
    df['Category'].isin(categories) &
    df['Region'].isin(regions) &
    df['Weather Condition'].isin(weathers) &
    df['Discount'].between(disc_range[0], disc_range[1]) &
    df['Price'].between(price_range[0], price_range[1])
)
filtered = df[mask]

# 1. Units Sold by Day of the Week
order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
data_day = (
    filtered.groupby('DayOfWeek')['Units Sold']
    .sum()
    .reindex(order)
    .reset_index()
)
chart_day = alt.Chart(data_day).mark_bar().encode(
    x=alt.X('DayOfWeek:O', sort=order),
    y='Units Sold:Q',
    tooltip=['DayOfWeek','Units Sold']
) + alt.Chart(data_day).mark_line(point=True).encode(
    x=alt.X('DayOfWeek:O', sort=order),
    y='Units Sold:Q'
)
st.subheader("Units Sold by Day of the Week")
st.altair_chart(chart_day, use_container_width=True)

# 2. Discount vs Units Sold

data_disc = filtered.groupby('Discount')['Units Sold'].sum().reset_index()
chart_disc = alt.Chart(data_disc).mark_bar().encode(
    x='Discount:O',
    y='Units Sold:Q',
    tooltip=['Discount','Units Sold']
) + alt.Chart(data_disc).mark_line(point=True).encode(
    x='Discount:O',
    y='Units Sold:Q'
)
st.subheader("Total Units Sold by Discount Level")
st.altair_chart(chart_disc, use_container_width=True)

# 3. Heat Map: Weather vs Day
pivot = (
    filtered.pivot_table(
        index='Weather Condition',
        columns='DayOfWeek',
        values='Units Sold',
        aggfunc='mean'
    )
    .reindex(columns=order)
)
heat_data = pivot.reset_index().melt(
    id_vars='Weather Condition',
    var_name='Day',
    value_name='Avg Units Sold'
)
chart_heat = alt.Chart(heat_data).mark_rect().encode(
    x=alt.X('Day:O', sort=order),
    y='Weather Condition:O',
    color='Avg Units Sold:Q',
    tooltip=['Weather Condition','Day','Avg Units Sold']
)
st.subheader("Heat Map: Avg Units Sold by Weather & Day")
st.altair_chart(chart_heat, use_container_width=True)

# 4. Promotions & Holiday Effects
non = filtered[filtered['Holiday/Promotion']==0]['Units Sold'].sum()
promo = filtered[filtered['Holiday/Promotion']==1]['Units Sold'].sum()
df_w = pd.DataFrame({
    'Stage': ['Non-Promo','Promo','Total'],
    'Units Sold': [non, promo, non+promo]
})
chart_w = alt.Chart(df_w).mark_bar().encode(
    x='Stage:O',
    y='Units Sold:Q',
    tooltip=['Stage','Units Sold']
)
st.subheader("Promotion & Holiday Effects")
st.altair_chart(chart_w, use_container_width=True)

# 5-8: Scatter plots
def plot_scatter(x_col, y_col, title):
    chart = alt.Chart(filtered).mark_circle(size=60, opacity=0.3).encode(
        x=f'{x_col}:Q',
        y=f'{y_col}:Q',
        tooltip=[x_col, y_col]
    ).interactive()
    st.subheader(title)
    st.altair_chart(chart, use_container_width=True)

plot_scatter('Price', 'Units Sold', 'Price vs Units Sold')
plot_scatter('Price Diff', 'Units Sold', 'Price Diff vs Units Sold')
plot_scatter('Inventory Level', 'Units Sold', 'Inventory Level vs Units Sold')
plot_scatter('Units Ordered', 'Units Sold', 'Units Ordered vs Units Sold')

# 9. Forecast vs Actual
agg_time = filtered.groupby('YearMonth').agg({
    'Units Sold':'sum',
    'Demand Forecast':'sum'
}).reset_index()
chart_time = alt.Chart(agg_time).transform_fold(
    ['Units Sold','Demand Forecast'],
    as_=['Type','Value']
).mark_line(point=True).encode(
    x='YearMonth:T',
    y='Value:Q',
    color='Type:N',
    tooltip=['YearMonth','Type','Value']
).interactive()
st.subheader("Forecast vs Actual over Time")
st.altair_chart(chart_time, use_container_width=True)

# 10-12: Bar charts
agg_cat = filtered.groupby('Category')['Units Sold'].sum().reset_index()
agg_reg = filtered.groupby('Region')['Units Sold'].sum().reset_index()
agg_sea = filtered.groupby('Season')['Units Sold'].sum().reset_index()

chart_cat = alt.Chart(agg_cat).mark_bar().encode(
    x='Category:O', y='Units Sold:Q', tooltip=['Category','Units Sold']
)
chart_reg = alt.Chart(agg_reg).mark_bar().encode(
    x='Region:O', y='Units Sold:Q', tooltip=['Region','Units Sold']
)
chart_sea = alt.Chart(agg_sea).mark_bar().encode(
    x='Season:O', y='Units Sold:Q', tooltip=['Season','Units Sold']
)
st.subheader("Units Sold by Category")
st.altair_chart(chart_cat, use_container_width=True)
st.subheader("Units Sold by Region")
st.altair_chart(chart_reg, use_container_width=True)
st.subheader("Units Sold by Season")
st.altair_chart(chart_sea, use_container_width=True)

# 13. Correlation Matrix
corr = filtered[['Price','Discount','Units Sold','Units Ordered','Demand Forecast','Inventory Level','Competitor Pricing']].corr()
corr_chart = alt.Chart(corr.reset_index().melt('index')).mark_rect().encode(
    x=alt.X('variable:O', sort=list(corr.columns)),
    y=alt.Y('index:O', sort=list(corr.index)),
    color='value:Q',
    tooltip=['index','variable','value']
)
st.subheader("Correlation Matrix")
st.altair_chart(corr_chart, use_container_width=True)
