import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

st.set_page_config(page_title="Corporate Finance Simulation", layout="wide")

# --------------------------------------------------
# INITIAL SESSION STATE
# --------------------------------------------------

if "round" not in st.session_state:
    st.session_state.round = 1

if "cash" not in st.session_state:
    st.session_state.cash = 200.0

if "debt" not in st.session_state:
    st.session_state.debt = 150.0

if "equity" not in st.session_state:
    st.session_state.equity = 350.0

if "revenue" not in st.session_state:
    st.session_state.revenue = 500.0

if "profit" not in st.session_state:
    st.session_state.profit = 60.0

if "stock_price" not in st.session_state:
    st.session_state.stock_price = 100.0

if "wacc" not in st.session_state:
    st.session_state.wacc = 0.10

if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def generate_macro_conditions():
    return {
        "GDP Growth": random.choice([3, 4, 5, 6, 7]),
        "Inflation": random.choice([3, 4, 5, 6, 7, 8]),
        "Interest Rate": random.choice([5, 6, 7, 8, 9]),
        "Market Sentiment": random.choice(["Bullish", "Neutral", "Bearish"]),
    }


macro = generate_macro_conditions()


def calculate_wacc(debt, equity, interest_rate):
    total = debt + equity

    if total == 0:
        return 0.10

    rd = interest_rate / 100
    re = 0.14
    tax = 0.30

    wacc = ((equity / total) * re) + ((debt / total) * rd * (1 - tax))

    return round(wacc, 4)



def calculate_npv(initial_investment, annual_cashflow, discount_rate, years=5):
    cashflows = [annual_cashflow] * years

    npv = -initial_investment

    for t, cf in enumerate(cashflows, start=1):
        npv += cf / ((1 + discount_rate) ** t)

    return round(npv, 2)



def random_market_shock():
    events = [
        ("Interest Rate Hike", -5),
        ("Economic Boom", 10),
        ("Supply Chain Disruption", -8),
        ("ESG Regulation", -3),
        ("Technology Breakthrough", 12),
        ("Banking Liquidity Crisis", -10),
        ("Stable Economy", 2),
    ]

    return random.choice(events)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("Corporate Finance Simulation")

st.markdown("""
This simulation allows students to manage a company through multiple rounds of:
- Capital budgeting
- Financing decisions
- Working capital management
- Dividend policy
- Risk management
""")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Current Round")
st.sidebar.metric("Round", st.session_state.round)

st.sidebar.header("Macroeconomic Conditions")

for key, value in macro.items():
    st.sidebar.write(f"**{key}:** {value}")

# --------------------------------------------------
# COMPANY DASHBOARD
# --------------------------------------------------

st.header("Company Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Cash", f"₹ {round(st.session_state.cash,2)} Cr")
col2.metric("Debt", f"₹ {round(st.session_state.debt,2)} Cr")
col3.metric("Revenue", f"₹ {round(st.session_state.revenue,2)} Cr")
col4.metric("Stock Price", f"₹ {round(st.session_state.stock_price,2)}")

col5, col6, col7 = st.columns(3)

col5.metric("Profit", f"₹ {round(st.session_state.profit,2)} Cr")
col6.metric("Equity", f"₹ {round(st.session_state.equity,2)} Cr")
col7.metric("WACC", f"{round(st.session_state.wacc*100,2)}%")

# --------------------------------------------------
# TABS
# --------------------------------------------------

investment_tab, financing_tab, working_capital_tab, results_tab = st.tabs(
    [
        "Capital Budgeting",
        "Financing",
        "Working Capital",
        "Results",
    ]
)

# --------------------------------------------------
# CAPITAL BUDGETING TAB
# --------------------------------------------------

with investment_tab:

    st.subheader("Investment Decisions")

    project = st.selectbox(
        "Select Project",
        [
            "Automation",
            "AI Expansion",
            "ESG Upgrade",
            "International Expansion",
        ],
    )

    investment_amount = st.slider(
        "Investment Amount (₹ Cr)",
        10,
        200,
        50,
    )

    expected_cashflow = st.slider(
        "Expected Annual Cash Flow (₹ Cr)",
        5,
        100,
        20,
    )

    discount_rate = st.slider(
        "Discount Rate (%)",
        5,
        20,
        10,
    )

    npv = calculate_npv(
        investment_amount,
        expected_cashflow,
        discount_rate / 100,
    )

    st.metric("Calculated NPV", f"₹ {npv} Cr")

    if npv > 0:
        st.success("Positive NPV project")
    else:
        st.error("Negative NPV project")

# --------------------------------------------------
# FINANCING TAB
# --------------------------------------------------

with financing_tab:

    st.subheader("Financing Decisions")

    capital_structure_strategy = st.selectbox(
        "Capital Structure Strategy",
        ["Conservative", "Balanced", "Aggressive"]
    )

    debt_financing = st.slider(
        "New Debt Raised (₹ Cr)",
        0,
        200,
        20,
    )

    equity_financing = st.slider(
        "New Equity Issued (₹ Cr)",
        0,
        200,
        10,
    )

    dividend_payout = st.slider(
        "Dividend Payout Ratio (%)",
        0,
        100,
        30,
    )

    projected_debt = st.session_state.debt + debt_financing
    projected_equity = st.session_state.equity + equity_financing

    projected_wacc = calculate_wacc(
        projected_debt,
        projected_equity,
        macro["Interest Rate"],
    )

    # Capital Structure Metrics

    de_ratio = projected_debt / projected_equity

    if de_ratio < 0.5:
        credit_rating = "AAA"
        bankruptcy_risk = 5

    elif de_ratio < 1.0:
        credit_rating = "A"
        bankruptcy_risk = 15

    elif de_ratio < 1.5:
        credit_rating = "BBB"
        bankruptcy_risk = 35

    else:
        credit_rating = "Junk"
        bankruptcy_risk = 60

    financing_col1, financing_col2 = st.columns(2)

    financing_col1.metric(
        "Projected WACC",
        f"{round(projected_wacc*100,2)}%"
    )

    financing_col2.metric(
        "Debt-to-Equity Ratio",
        round(de_ratio,2)
    )

    st.metric("Credit Rating", credit_rating)

    st.metric(
        "Bankruptcy Risk",
        f"{bankruptcy_risk}%"
    )

    # Dividend Policy

    st.subheader("Dividend Policy")

    dividend_policy = st.selectbox(
        "Dividend Policy",
        [
            "Stable Dividend",
            "Residual Dividend",
            "High Dividend",
            "No Dividend",
            "Share Buyback"
        ]
    )

    investor_sentiment = 0

    if dividend_policy == "Stable Dividend":
        investor_sentiment += 5

    elif dividend_policy == "High Dividend":
        investor_sentiment += 8

    elif dividend_policy == "No Dividend":
        investor_sentiment -= 5

    elif dividend_policy == "Share Buyback":
        investor_sentiment += 10

    st.metric(
        "Investor Sentiment Score",
        investor_sentiment
    )

# --------------------------------------------------
# WORKING CAPITAL TAB
# --------------------------------------------------

with working_capital_tab:

    st.subheader("Working Capital Management")

    credit_policy = st.selectbox(
        "Credit Policy",
        ["Strict", "Moderate", "Liberal"],
    )

    inventory_policy = st.selectbox(
        "Inventory Policy",
        ["Low", "Medium", "High"],
    )

    supplier_payment = st.selectbox(
        "Supplier Payment Strategy",
        ["Early", "Standard", "Delayed"],
    )

    cash_reserve = st.slider(
        "Target Cash Reserve (₹ Cr)",
        10,
        150,
        50,
    )

    # Working Capital Logic

    receivables_days = {
        "Strict": 30,
        "Moderate": 60,
        "Liberal": 90,
    }[credit_policy]

    inventory_days = {
        "Low": 30,
        "Medium": 60,
        "High": 90,
    }[inventory_policy]

    payable_days = {
        "Early": 20,
        "Standard": 45,
        "Delayed": 75,
    }[supplier_payment]

    ccc = inventory_days + receivables_days - payable_days

    current_assets = st.session_state.cash + 100
    current_liabilities = 80 + debt_financing

    current_ratio = current_assets / current_liabilities

    quick_ratio = (current_assets - 40) / current_liabilities

    col_a, col_b, col_c = st.columns(3)

    col_a.metric("Current Ratio", round(current_ratio, 2))
    col_b.metric("Quick Ratio", round(quick_ratio, 2))
    col_c.metric("Cash Conversion Cycle", f"{ccc} Days")

    if ccc > 90:
        st.warning("High cash conversion cycle may create liquidity stress")

# --------------------------------------------------
# RUN SIMULATION
# --------------------------------------------------

st.header("Run Simulation")

if st.button("Run Round"):

    shock_name, shock_effect = random_market_shock()

    # Revenue impact
    revenue_growth = np.random.uniform(0.02, 0.15)

    if credit_policy == "Liberal":
        revenue_growth += 0.03

    if inventory_policy == "Low":
        revenue_growth -= 0.02

    updated_revenue = st.session_state.revenue * (1 + revenue_growth)

    # Profit calculation
    operating_margin = 0.12

    updated_profit = updated_revenue * operating_margin

    # Shock adjustment
    updated_profit += shock_effect

    # Dividend effect
    dividend_amount = updated_profit * (dividend_payout / 100)

    # Cash update
    updated_cash = (
        st.session_state.cash
        + updated_profit
        - investment_amount
        + debt_financing
        + equity_financing
        - dividend_amount
    )

    # Stock price update
    stock_change = (updated_profit / 10) + shock_effect

    updated_stock_price = max(
        10,
        st.session_state.stock_price + stock_change,
    )

    # Update WACC
    updated_wacc = calculate_wacc(
        projected_debt,
        projected_equity,
        macro["Interest Rate"],
    )

    # Save history
    st.session_state.history.append(
        {
            "Round": st.session_state.round,
            "Revenue": updated_revenue,
            "Profit": updated_profit,
            "Cash": updated_cash,
            "Stock Price": updated_stock_price,
        }
    )

    # Update state
    st.session_state.revenue = updated_revenue
    st.session_state.profit = updated_profit
    st.session_state.cash = updated_cash
    st.session_state.stock_price = updated_stock_price
    st.session_state.debt = projected_debt
    st.session_state.equity = projected_equity
    st.session_state.wacc = updated_wacc

    st.session_state.round += 1

    # RESULTS
    st.success(f"Simulation Round Completed: {shock_name}")

    st.subheader("Round Outcome")

    result1, result2, result3, result4 = st.columns(4)

    result1.metric("Updated Revenue", f"₹ {round(updated_revenue,2)} Cr")
    result2.metric("Updated Profit", f"₹ {round(updated_profit,2)} Cr")
    result3.metric("Updated Cash", f"₹ {round(updated_cash,2)} Cr")
    result4.metric("Updated Stock Price", f"₹ {round(updated_stock_price,2)}")

    if updated_cash < 20:
        st.error("Liquidity stress detected")

    if projected_debt / projected_equity > 1.5:
        st.warning("High leverage risk")

# --------------------------------------------------
# RESULTS TAB
# --------------------------------------------------

with results_tab:

    st.subheader("Historical Performance")

    if len(st.session_state.history) > 0:

        df = pd.DataFrame(st.session_state.history)

        st.dataframe(df)

        fig1 = px.line(
            df,
            x="Round",
            y="Revenue",
            title="Revenue Trend",
        )

        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.line(
            df,
            x="Round",
            y="Stock Price",
            title="Stock Price Trend",
        )

        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("No rounds completed yet")

# --------------------------------------------------
# RESET BUTTON
# --------------------------------------------------

st.sidebar.header("Simulation Control")

if st.sidebar.button("Reset Simulation"):

    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.rerun()
