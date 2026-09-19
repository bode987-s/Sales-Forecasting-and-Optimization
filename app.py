import streamlit as st
import joblib
import pandas as pd
import numpy as np
import altair as alt
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent

# ------------------------------------------------------------------
# Design tokens — "Retail Intelligence Terminal" theme
# Deep navy background + gold/amber accent (retail & pricing),
# teal for positive signals, rose for negative/alert signals.
# ------------------------------------------------------------------
COLORS = {
    "bg": "#0B1220",
    "panel": "#131B2E",
    "panel_alt": "#1B2540",
    "border": "#263252",
    "text": "#EDF1F9",
    "muted": "#8B96AD",
    "gold": "#E8A33D",
    "teal": "#2DD4BF",
    "rose": "#F0665F",
}


def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap');

        html, body, [class*="css"], .stMarkdown, .stText, p, label, span {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background:
                radial-gradient(circle at 12% -10%, #142038 0%, {COLORS['bg']} 42%),
                {COLORS['bg']};
            color: {COLORS['text']};
        }}

        section[data-testid="stSidebar"] {{
            background: {COLORS['panel']};
            border-right: 1px solid {COLORS['border']};
        }}
        section[data-testid="stSidebar"] * {{
            color: {COLORS['text']} !important;
        }}
        section[data-testid="stSidebar"] .eyebrow {{
            margin-top: 4px;
        }}

        h1, h2, h3, h4 {{
            font-family: 'Space Grotesk', sans-serif !important;
            letter-spacing: -0.01em;
            color: {COLORS['text']};
        }}

        /* ---- header ---- */
        .app-header {{
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 4px;
        }}
        .app-header .badge {{
            font-size: 30px;
            width: 52px; height: 52px;
            display: flex; align-items: center; justify-content: center;
            background: linear-gradient(135deg, {COLORS['gold']}, #C97F1F);
            border-radius: 12px;
        }}
        .app-title {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 28px; font-weight: 700; margin: 0;
            color: {COLORS['text']};
        }}
        .app-subtitle {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px; letter-spacing: .12em; text-transform: uppercase;
            color: {COLORS['muted']}; margin-top: 2px;
        }}

        /* ---- ticker band ---- */
        .ticker-band {{
            display: flex; gap: 28px; flex-wrap: wrap;
            background: linear-gradient(135deg, {COLORS['panel']} 0%, {COLORS['panel_alt']} 100%);
            border: 1px solid {COLORS['border']};
            border-radius: 14px;
            padding: 18px 24px;
            margin: 18px 0 24px 0;
        }}
        .ticker-item {{ display: flex; flex-direction: column; min-width: 130px; }}
        .ticker-label {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px; text-transform: uppercase; letter-spacing: .08em;
            color: {COLORS['muted']}; margin-bottom: 5px;
        }}
        .ticker-value {{
            font-family: 'JetBrains Mono', monospace; font-size: 21px; font-weight: 600;
            color: {COLORS['text']};
        }}
        .ticker-value.gold {{ color: {COLORS['gold']}; }}
        .ticker-value.teal {{ color: {COLORS['teal']}; }}

        /* ---- eyebrow labels above sections ---- */
        .eyebrow {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 11.5px; letter-spacing: .14em; text-transform: uppercase;
            color: {COLORS['gold']}; margin-bottom: 2px;
        }}

        /* ---- cards ---- */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: {COLORS['panel']};
            border: 1px solid {COLORS['border']} !important;
            border-radius: 14px !important;
        }}

        /* ---- inputs ---- */
        .stSlider, .stSelectbox, .stNumberInput, .stRadio {{
            padding-bottom: 4px;
        }}
        div[data-baseweb="select"] > div {{
            background-color: {COLORS['panel_alt']} !important;
            border-color: {COLORS['border']} !important;
            color: {COLORS['text']} !important;
        }}
        input {{
            background-color: {COLORS['panel_alt']} !important;
            color: {COLORS['text']} !important;
        }}

        /* ---- buttons ---- */
        .stButton > button {{
            background: linear-gradient(135deg, {COLORS['gold']}, #C97F1F);
            color: #16110A; font-weight: 600; border: none; border-radius: 10px;
            padding: 0.6rem 1.5rem; font-family: 'Space Grotesk', sans-serif;
            transition: transform .15s ease, box-shadow .15s ease;
        }}
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(232,163,61,.30);
            color: #16110A;
        }}

        /* ---- prediction result ---- */
        .prediction-card {{
            background: linear-gradient(135deg, {COLORS['panel_alt']}, {COLORS['panel']});
            border: 1px solid {COLORS['gold']}66;
            border-radius: 16px;
            padding: 24px 28px;
            margin-top: 18px;
        }}
        .prediction-label {{
            font-family: 'JetBrains Mono', monospace; font-size: 12px;
            letter-spacing: .1em; text-transform: uppercase; color: {COLORS['muted']};
        }}
        .prediction-number {{
            font-family: 'JetBrains Mono', monospace; font-size: 44px; font-weight: 600;
            color: {COLORS['gold']}; line-height: 1.2; margin: 4px 0;
        }}
        .prediction-delta-up {{ color: {COLORS['teal']}; font-family: 'JetBrains Mono', monospace; font-size: 14px; }}
        .prediction-delta-down {{ color: {COLORS['rose']}; font-family: 'JetBrains Mono', monospace; font-size: 14px; }}

        [data-testid="stMetricValue"] {{ font-family: 'JetBrains Mono', monospace; color: {COLORS['text']}; }}
        [data-testid="stMetricLabel"] {{ color: {COLORS['muted']}; }}

        hr {{ border-color: {COLORS['border']}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def register_altair_theme():
    def retail_dark():
        return {
            "config": {
                "background": "transparent",
                "view": {"stroke": "transparent"},
                "axis": {
                    "labelColor": COLORS["muted"],
                    "titleColor": COLORS["text"],
                    "gridColor": COLORS["border"],
                    "domainColor": COLORS["border"],
                    "labelFont": "Inter",
                    "titleFont": "Space Grotesk",
                    "labelFontSize": 11,
                },
                "legend": {
                    "labelColor": COLORS["text"],
                    "titleColor": COLORS["muted"],
                    "labelFont": "Inter",
                },
                "title": {"color": COLORS["text"], "font": "Space Grotesk", "fontSize": 14},
                "range": {
                    "category": [COLORS["gold"], COLORS["teal"], COLORS["rose"],
                                 "#7C9CF0", "#C99BF0", "#5AD1A6", "#F0B15F"],
                    "heatmap": "goldgreen",
                    "ramp": "goldgreen",
                },
                "mark": {"color": COLORS["gold"]},
                "line": {"color": COLORS["gold"], "strokeWidth": 2.5},
                "bar": {"color": COLORS["gold"]},
                "point": {"color": COLORS["teal"]},
                "rect": {"color": COLORS["gold"]},
            }
        }

    alt.themes.register("retail_dark", retail_dark)
    alt.themes.enable("retail_dark")


def eyebrow_header(label, title):
    st.markdown(f'<div class="eyebrow">{label}</div>', unsafe_allow_html=True)
    st.subheader(title)


def ticker_band(items):
    """items: list of (label, value, style_class) where style_class in {'', 'gold', 'teal'}"""
    html = '<div class="ticker-band">'
    for label, value, style in items:
        html += (
            '<div class="ticker-item">'
            f'<div class="ticker-label">{label}</div>'
            f'<div class="ticker-value {style}">{value}</div>'
            '</div>'
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load the model trained with the project's pinned scikit-learn version."""
    try:
        return joblib.load(PROJECT_DIR / "sales_forecast_model.pkl")
    except AttributeError as exc:
        if "_RemainderColsList" in str(exc):
            raise RuntimeError(
                "This model was saved with scikit-learn 1.6.1 but the active "
                "environment uses an incompatible version. Install the project "
                "dependencies with `python -m pip install -r requirements.txt`, "
                "then restart Streamlit."
            ) from exc
        raise


@st.cache_data(ttl="1h")
def load_data():
    df = pd.read_csv(PROJECT_DIR / 'retail_store_inventory.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['Price Diff'] = df['Price'] - df['Competitor Pricing']

    def get_season(m):
        if m in [3, 4, 5]:
            return 'Spring'
        if m in [6, 7, 8]:
            return 'Summer'
        if m in [9, 10, 11]:
            return 'Autumn'
        return 'Winter'

    df['Season'] = df['Date'].dt.month.map(get_season)
    df['YearMonth'] = df['Date'].dt.to_period('M').dt.to_timestamp()
    return df


st.set_page_config(page_title="Retail Sales Terminal", layout="wide", page_icon="📈")
inject_css()
register_altair_theme()

st.markdown(
    """
    <div class="app-header">
        <div class="badge">📈</div>
        <div>
            <p class="app-title">Retail Sales Intelligence Terminal</p>
            <p class="app-subtitle">Forecasting Engine · Inventory Analytics</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown('<div class="eyebrow">Console</div>', unsafe_allow_html=True)
type_choice = st.sidebar.selectbox(
    "Select Mode:",
    ["Prediction", "Visualization"]
)

if type_choice == "Prediction":
    ticker_band([
        ("MODE", "PREDICTION", "gold"),
        ("ENGINE", "Regression Model", ""),
        ("STATUS", "Ready", "teal"),
    ])

    eyebrow_header("Forecasting Engine", "Sales Prediction")
    st.caption("Enter booking conditions below to estimate units sold.")

    try:
        model = load_model()
    except (FileNotFoundError, RuntimeError) as exc:
        st.error(str(exc))
        st.stop()

    with st.container(border=True):
        st.markdown('<div class="eyebrow">Timing</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            month = st.slider("Month", 1, 12, 1)
        with c2:
            day_of_week = st.selectbox(
                "Day of the Week",
                options=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'),
                         (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')],
                format_func=lambda x: x[1]
            )[0]
        with c3:
            season = st.selectbox("Season", ['Spring', 'Summer', 'Autumn', 'Winter'])

        st.markdown('<div class="eyebrow" style="margin-top:14px;">Conditions</div>', unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)
        with c4:
            weather = st.selectbox("Weather State", ['Sunny', 'Cloudy', 'Rainy', 'Snowy'])
        with c5:
            discount = st.slider("Discount %", 0, 50, 5)
        with c6:
            holiday = st.radio(
                "Promotion / Holiday?",
                [1, 0], format_func=lambda x: "Yes" if x == 1 else "No", horizontal=True
            )

        st.markdown('<div class="eyebrow" style="margin-top:14px;">Pricing & Demand</div>', unsafe_allow_html=True)
        c7, c8, c9 = st.columns(3)
        with c7:
            demand_forecast = st.number_input("Order forecast (system)", min_value=0, value=300)
        with c8:
            competitor_price = st.number_input("Competitor's price", min_value=0, value=100)
        with c9:
            price = st.number_input("Actual price", min_value=0, value=100)

        predict_clicked = st.button("Calculate Prediction")

    if predict_clicked:
        input_data = pd.DataFrame([{
            'Month': month,
            'DayOfWeek': day_of_week,
            'Discount': discount,
            'Holiday/Promotion': holiday,
            'Weather Condition': weather,
            'Seasonality': season,
            'Demand Forecast': demand_forecast,
            'Competitor Pricing': competitor_price,
            'Price': price
        }])
        prediction = int(model.predict(input_data)[0])
        delta = prediction - demand_forecast
        delta_class = "prediction-delta-up" if delta >= 0 else "prediction-delta-down"
        delta_sign = "▲" if delta >= 0 else "▼"
        st.markdown(
            f"""
            <div class="prediction-card">
                <div class="prediction-label">Predicted Units Sold</div>
                <div class="prediction-number">{prediction:,}</div>
                <div class="{delta_class}">{delta_sign} {abs(delta):,} vs. system order forecast ({demand_forecast:,})</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

else:
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("Data file 'retail_store_inventory.csv' not found. Please place it in the app directory.")
        st.stop()

    st.sidebar.markdown('<div class="eyebrow" style="margin-top:18px;">Filters</div>', unsafe_allow_html=True)
    min_date, max_date = st.sidebar.date_input(
        "Select Date Range", [df['Date'].min(), df['Date'].max()]
    )
    categories = st.sidebar.multiselect("Category", options=df['Category'].unique(), default=df['Category'].unique())
    regions = st.sidebar.multiselect("Region", options=df['Region'].unique(), default=df['Region'].unique())
    weathers = st.sidebar.multiselect("Weather Condition", options=df['Weather Condition'].unique(), default=df['Weather Condition'].unique())
    disc_range = st.sidebar.slider("Discount Range (%)", 0, 90, (0, 90))
    price_range = st.sidebar.slider("Price Range", 0, 100, (0, 100))

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

    total_units = int(filtered['Units Sold'].sum())
    avg_discount = filtered['Discount'].mean() if len(filtered) else 0
    n_records = len(filtered)
    promo_share = (filtered['Holiday/Promotion'].mean() * 100) if len(filtered) else 0

    ticker_band([
        ("RECORDS", f"{n_records:,}", ""),
        ("TOTAL UNITS SOLD", f"{total_units:,}", "gold"),
        ("AVG DISCOUNT", f"{avg_discount:.1f}%", ""),
        ("PROMO SHARE", f"{promo_share:.1f}%", "teal"),
    ])

    eyebrow_header("Analytics", "Interactive Retail Store Inventory Dashboard")

    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    with st.container(border=True):
        eyebrow_header("Weekly Pattern", "Units Sold by Day of the Week")
        data_day = (filtered.groupby('DayOfWeek')['Units Sold'].sum().reindex(order).reset_index())
        chart_day = alt.Chart(data_day).mark_bar().encode(
            x=alt.X('DayOfWeek:O', sort=order), y='Units Sold:Q', tooltip=['DayOfWeek', 'Units Sold']
        ) + alt.Chart(data_day).mark_line(point=True, color=COLORS["teal"]).encode(
            x=alt.X('DayOfWeek:O', sort=order), y='Units Sold:Q'
        )
        st.altair_chart(chart_day, use_container_width=True)

    with st.container(border=True):
        eyebrow_header("Pricing Strategy", "Total Units Sold by Discount Level")
        data_disc = filtered.groupby('Discount')['Units Sold'].sum().reset_index()
        chart_disc = alt.Chart(data_disc).mark_bar().encode(
            x='Discount:O', y='Units Sold:Q', tooltip=['Discount', 'Units Sold']
        ) + alt.Chart(data_disc).mark_line(point=True, color=COLORS["teal"]).encode(
            x='Discount:O', y='Units Sold:Q'
        )
        st.altair_chart(chart_disc, use_container_width=True)

    with st.container(border=True):
        eyebrow_header("Environmental Impact", "Heat Map: Avg Units Sold by Weather & Day")
        pivot = filtered.pivot_table(index='Weather Condition', columns='DayOfWeek', values='Units Sold', aggfunc='mean').reindex(columns=order)
        heat_data = pivot.reset_index().melt(id_vars=['Weather Condition'], var_name='Day', value_name='AvgUnits')
        chart_heat = alt.Chart(heat_data).mark_rect().encode(
            x=alt.X('Day:O', sort=order), y='Weather Condition:O', color=alt.Color('AvgUnits:Q', scale=alt.Scale(scheme='goldgreen')),
            tooltip=['Weather Condition', 'Day', 'AvgUnits']
        )
        st.altair_chart(chart_heat, use_container_width=True)

    with st.container(border=True):
        eyebrow_header("Campaign Effect", "Promotion & Holiday Effects")
        non = filtered[filtered['Holiday/Promotion'] == 0]['Units Sold'].sum()
        promo = filtered[filtered['Holiday/Promotion'] == 1]['Units Sold'].sum()
        df_w = pd.DataFrame({
            'Stage': ['Non-Promo', 'Promo', 'Total'],
            'Units Sold': [non, promo, non + promo]
        })
        chart_w = alt.Chart(df_w).mark_bar().encode(x='Stage:O', y='Units Sold:Q', tooltip=['Stage', 'Units Sold'])
        st.altair_chart(chart_w, use_container_width=True)

    def plot_scatter(x_col, y_col, title, eyebrow):
        with st.container(border=True):
            eyebrow_header(eyebrow, title)
            chart = alt.Chart(filtered).mark_circle(size=60, opacity=0.35, color=COLORS["teal"]).encode(
                x=f'{x_col}:Q', y=f'{y_col}:Q', tooltip=[x_col, y_col]
            ).interactive()
            st.altair_chart(chart, use_container_width=True)

    plot_scatter('Price', 'Units Sold', 'Price vs Units Sold', 'Correlation')
    plot_scatter('Price Diff', 'Units Sold', 'Price Diff vs Units Sold', 'Correlation')
    plot_scatter('Inventory Level', 'Units Sold', 'Inventory Level vs Units Sold', 'Correlation')
    plot_scatter('Units Ordered', 'Units Sold', 'Units Ordered vs Units Sold', 'Correlation')

    with st.container(border=True):
        eyebrow_header("Time Series", "Forecast vs Actual over Time")
        agg_time = filtered.groupby('YearMonth').agg({'Units Sold': 'sum', 'Demand Forecast': 'sum'}).reset_index()
        folded = agg_time.melt(id_vars=['YearMonth'], value_vars=['Units Sold', 'Demand Forecast'], var_name='Variable', value_name='Value')
        chart_time = alt.Chart(folded).mark_line(point=True).encode(
            x='YearMonth:T', y='Value:Q', color='Variable:N', tooltip=['YearMonth', 'Variable', 'Value']
        ).interactive()
        st.altair_chart(chart_time, use_container_width=True)

    with st.container(border=True):
        eyebrow_header("Breakdown", "Units Sold by Category, Region, Season")
        agg_cat = filtered.groupby('Category')['Units Sold'].sum().reset_index()
        agg_reg = filtered.groupby('Region')['Units Sold'].sum().reset_index()
        agg_sea = filtered.groupby('Season')['Units Sold'].sum().reset_index()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.altair_chart(alt.Chart(agg_cat).mark_bar().encode(x='Category:O', y='Units Sold:Q', tooltip=['Category', 'Units Sold']), use_container_width=True)
        with col2:
            st.altair_chart(alt.Chart(agg_reg).mark_bar().encode(x='Region:O', y='Units Sold:Q', tooltip=['Region', 'Units Sold']), use_container_width=True)
        with col3:
            st.altair_chart(alt.Chart(agg_sea).mark_bar().encode(x='Season:O', y='Units Sold:Q', tooltip=['Season', 'Units Sold']), use_container_width=True)

    with st.container(border=True):
        eyebrow_header("Statistics", "Correlation Matrix")
        corr = filtered[['Price', 'Discount', 'Units Sold', 'Units Ordered', 'Demand Forecast', 'Inventory Level', 'Competitor Pricing']].corr()
        corr_reset = corr.reset_index().melt(id_vars='index', var_name='Variable', value_name='Correlation')
        chart_corr = alt.Chart(corr_reset).mark_rect().encode(
            x=alt.X('Variable:O', sort=list(corr.columns)), y=alt.Y('index:O', sort=list(corr.index)),
            color=alt.Color('Correlation:Q', scale=alt.Scale(scheme='goldgreen')),
            tooltip=['index', 'Variable', 'Correlation']
        )
        st.altair_chart(chart_corr, use_container_width=True)

#    python -m streamlit run "e:\Sales_Forecasting_Project\apps\app.py"