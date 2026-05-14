# =========================================================
# INTERACTIVE CFO LEARNING PLATFORM
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Interactive CFO Learning Platform",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

defaults = {

    "round": 1,
    "cash": 250.0,
    "debt": 180.0,
    "equity": 420.0,
    "revenue": 700.0,
    "profit": 85.0,
    "stock_price": 120.0,
    "wacc": 0.10,
    "history": []
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# FUNCTIONS
# =========================================================

def calculate_npv(
    investment,
    cashflow,
    rate,
    years=5
):

    npv = -investment

    for t in range(1, years + 1):

        npv += (
            cashflow /
            ((1 + rate) ** t)
        )

    return round(npv, 2)


def calculate_wacc(
    debt,
    equity,
    interest_rate
):

    total = debt + equity

    rd = interest_rate / 100
    re = 0.14
    tax = 0.30

    wacc = (
        (equity / total) * re
        +
        (debt / total) * rd * (1 - tax)
    )

    return round(wacc, 4)


def generate_economic_environment():

    environments = [

        {
            "title": "Economic Expansion",
            "description":
            """
            Consumer demand is increasing rapidly.
            Investors remain optimistic regarding
            growth-oriented firms.
            """,
            "impact": 10
        },

        {
            "title": "Rising Interest Rates",
            "description":
            """
            Central banks increased interest rates
            due to inflationary pressure.
            Highly leveraged firms face increased risk.
            """,
            "impact": -8
        },

        {
            "title": "Technology Disruption",
            "description":
            """
            Competitors are investing aggressively
            in AI-enabled automation.
            Firms delaying investment risk losing market share.
            """,
            "impact": 12
        },

        {
            "title": "Economic Slowdown",
            "description":
            """
            Consumer spending weakened significantly.
            Liquidity preservation becomes critical.
            """,
            "impact": -10
        }
    ]

    return random.choice(environments)

# =========================================================
# TITLE
# =========================================================

st.title("Interactive CFO Learning Platform")

st.markdown("""
An experiential corporate finance learning environment
where students assume the role of Chief Financial Officer (CFO)
and make strategic financial decisions under uncertainty.
""")

# =========================================================
# COMPANY INTRODUCTION
# =========================================================

st.header("Your Role")

st.write("""
You are the CFO of a mid-sized manufacturing company
experiencing expansion opportunities, financing pressure,
and evolving investor expectations.

Your objective is to maximize:
- shareholder wealth,
- financial stability,
- operational sustainability,
- and long-term firm value.
""")

# =========================================================
# ECONOMIC ENVIRONMENT
# =========================================================

environment = generate_economic_environment()

st.header("Current Economic Environment")

st.subheader(environment["title"])

st.info(environment["description"])

# =========================================================
# COMPANY DASHBOARD
# =========================================================

st.header("Current Financial Position")

d1, d2, d3, d4 = st.columns(4)

d1.metric(
    "Cash",
    f"₹ {round(st.session_state.cash,2)} Cr"
)

d2.metric(
    "Debt",
    f"₹ {round(st.session_state.debt,2)} Cr"
)

d3.metric(
    "Profit",
    f"₹ {round(st.session_state.profit,2)} Cr"
)

d4.metric(
    "Stock Price",
    f"₹ {round(st.session_state.stock_price,2)}"
)

# =========================================================
# STRATEGIC CHALLENGE
# =========================================================

st.header("Strategic Challenge")

st.write("""
Management proposes a major investment in AI-enabled
manufacturing automation to improve long-term productivity
and competitiveness.
""")

st.warning("""
The project may increase profitability,
but financing decisions could significantly
affect leverage and financial risk.
""")

# =========================================================
# CAPITAL BUDGETING
# =========================================================

st.header("Capital Budgeting Decision")

with st.expander(
    "Learn About Capital Budgeting"
):

    st.latex(
        r'''NPV = \sum_{t=1}^{n}\frac{CF_t}{(1+r)^t} - C_0'''
    )

    st.write("""
    Net Present Value (NPV) measures
    shareholder value creation after considering
    the time value of money.
    """)

    st.write("""
    Positive NPV projects generally increase
    firm value.
    """)

investment_amount = st.slider(
    "Project Investment (₹ Cr)",
    20,
    300,
    80
)

expected_cashflow = st.slider(
    "Expected Annual Cash Flow (₹ Cr)",
    10,
    120,
    30
)

discount_rate = st.slider(
    "Discount Rate (%)",
    5,
    20,
    10
)

npv = calculate_npv(
    investment_amount,
    expected_cashflow,
    discount_rate / 100
)

st.metric(
    "Net Present Value",
    f"₹ {npv} Cr"
)

# =========================================================
# CAPITAL STRUCTURE
# =========================================================

st.header("Capital Structure Decision")

with st.expander(
    "Learn About Capital Structure"
):

    st.latex(
        r'''WACC = \frac{E}{V}R_e + \frac{D}{V}R_d(1-T)'''
    )

    st.latex(
        r'''V_L = V_U + Tax\ Shield'''
    )

    st.write("""
    Debt financing provides tax advantages,
    but excessive leverage increases
    financial distress risk.
    """)

debt_financing = st.slider(
    "Debt Financing (₹ Cr)",
    0,
    250,
    40
)

equity_financing = st.slider(
    "Equity Financing (₹ Cr)",
    0,
    250,
    20
)

projected_debt = (
    st.session_state.debt +
    debt_financing
)

projected_equity = (
    st.session_state.equity +
    equity_financing
)

projected_wacc = calculate_wacc(
    projected_debt,
    projected_equity,
    8
)

de_ratio = round(
    projected_debt /
    projected_equity,
    2
)

c1, c2 = st.columns(2)

c1.metric(
    "Projected WACC",
    f"{round(projected_wacc*100,2)}%"
)

c2.metric(
    "Debt-to-Equity Ratio",
    de_ratio
)

# =========================================================
# DIVIDEND POLICY
# =========================================================

st.header("Dividend Policy Decision")

with st.expander(
    "Learn About Dividend Policy"
):

    st.latex(
        r'''Dividend\ Payout\ Ratio = \frac{Dividends}{Net\ Income}'''
    )

    st.write("""
    Dividend policy influences:
    - investor expectations,
    - internal financing capacity,
    - and market signaling.
    """)

dividend_policy = st.selectbox(

    "Dividend Strategy",

    [
        "Stable Dividend",
        "High Dividend",
        "Residual Dividend",
        "No Dividend",
        "Share Buyback"
    ]
)

dividend_payout = st.slider(
    "Dividend Payout Ratio (%)",
    0,
    100,
    30
)

# =========================================================
# WORKING CAPITAL MANAGEMENT
# =========================================================

st.header("Working Capital Management")

with st.expander(
    "Learn About Working Capital"
):

    st.latex(
        r'''CCC = DIO + DSO - DPO'''
    )

    st.write("""
    Working capital management ensures
    operational liquidity and efficiency.
    """)

credit_policy = st.selectbox(
    "Customer Credit Policy",
    [
        "Strict",
        "Moderate",
        "Liberal"
    ]
)

inventory_policy = st.selectbox(
    "Inventory Policy",
    [
        "Low",
        "Medium",
        "High"
    ]
)

supplier_payment = st.selectbox(
    "Supplier Payment Policy",
    [
        "Early",
        "Standard",
        "Delayed"
    ]
)

# =========================================================
# RISK MANAGEMENT
# =========================================================

st.header("Risk Management")

with st.expander(
    "Learn About Risk Management"
):

    st.write("""
    Firms face:
    - interest rate risk,
    - liquidity risk,
    - foreign exchange risk,
    - and operational uncertainty.
    """)

hedging_strategy = st.selectbox(

    "Hedging Strategy",

    [
        "No Hedging",
        "Partial Hedging",
        "Full Hedging"
    ]
)

# =========================================================
# RUN DECISION ROUND
# =========================================================

st.header("Execute Strategic Decisions")

if st.button("Run CFO Decision Round"):

    # -----------------------------------------------------
    # REVENUE IMPACT
    # -----------------------------------------------------

    growth = np.random.uniform(
        0.03,
        0.15
    )

    updated_revenue = (
        st.session_state.revenue *
        (1 + growth)
    )

    # -----------------------------------------------------
    # PROFIT IMPACT
    # -----------------------------------------------------

    updated_profit = (
        updated_revenue * 0.12
    ) + environment["impact"]

    # -----------------------------------------------------
    # DIVIDEND IMPACT
    # -----------------------------------------------------

    dividend_amount = (
        updated_profit *
        (dividend_payout / 100)
    )

    # -----------------------------------------------------
    # CASH IMPACT
    # -----------------------------------------------------

    updated_cash = (

        st.session_state.cash
        +
        updated_profit
        -
        investment_amount
        +
        debt_financing
        +
        equity_financing
        -
        dividend_amount
    )

    # -----------------------------------------------------
    # STOCK PRICE
    # -----------------------------------------------------

    updated_stock_price = max(

        10,

        st.session_state.stock_price
        +
        (updated_profit / 12)
    )

    # -----------------------------------------------------
    # UPDATE SESSION
    # -----------------------------------------------------

    st.session_state.cash = updated_cash

    st.session_state.revenue = updated_revenue

    st.session_state.profit = updated_profit

    st.session_state.stock_price = (
        updated_stock_price
    )

    st.session_state.debt = projected_debt

    st.session_state.equity = projected_equity

    st.session_state.wacc = projected_wacc

    # -----------------------------------------------------
    # SAVE HISTORY
    # -----------------------------------------------------

    st.session_state.history.append({

        "Round": st.session_state.round,
        "Revenue": updated_revenue,
        "Profit": updated_profit,
        "Cash": updated_cash,
        "Stock Price": updated_stock_price
    })

    st.session_state.round += 1

    # =====================================================
    # EDUCATIONAL FEEDBACK
    # =====================================================

    st.header("Board and Market Reactions")

    if npv > 0:

        st.success("""
        Board members approved the investment strategy
        because the project is expected to create
        long-term shareholder value.
        """)

    else:

        st.error("""
        Investors expressed concern regarding
        the project's weak value creation potential.
        """)

    if de_ratio > 1.5:

        st.warning("""
        Credit analysts warned that excessive leverage
        may increase financial distress risk despite
        tax shield benefits.
        """)

    elif de_ratio < 0.5:

        st.info("""
        The firm maintains conservative leverage,
        but may be underutilizing debt tax advantages.
        """)

    if updated_cash < 40:

        st.error("""
        Liquidity stress is emerging.
        Management may need to reconsider
        dividend payouts or financing strategy.
        """)

    if hedging_strategy == "No Hedging":

        st.warning("""
        The company remains fully exposed
        to market volatility.
        """)

    # =====================================================
    # REFLECTION QUESTIONS
    # =====================================================

    st.header("Strategic Reflection")

    st.text_area(
        "Why did you choose your financing strategy?",
        height=120
    )

    st.text_area(
        "Did your investment decision maximize shareholder value?",
        height=120
    )

    st.text_area(
        "How would you modify your strategy under worsening economic conditions?",
        height=120
    )

# =========================================================
# FINANCIAL STATEMENTS
# =========================================================

st.header("Simplified Financial Statements")

income_statement = pd.DataFrame({

    "Item": [
        "Revenue",
        "Operating Profit",
        "Interest Expense",
        "Net Profit"
    ],

    "Amount": [

        round(st.session_state.revenue,2),

        round(st.session_state.profit,2),

        round(st.session_state.debt * 0.08,2),

        round(
            st.session_state.profit -
            (st.session_state.debt * 0.08),
            2
        )
    ]
})

balance_sheet = pd.DataFrame({

    "Item": [
        "Cash",
        "Debt",
        "Equity"
    ],

    "Amount": [

        round(st.session_state.cash,2),

        round(st.session_state.debt,2),

        round(st.session_state.equity,2)
    ]
})

f1, f2 = st.columns(2)

with f1:

    st.subheader("Income Statement")

    st.dataframe(
        income_statement,
        use_container_width=True
    )

with f2:

    st.subheader("Balance Sheet")

    st.dataframe(
        balance_sheet,
        use_container_width=True
    )

# =========================================================
# PERFORMANCE VISUALIZATION
# =========================================================

st.header("Firm Performance Dashboard")

if len(st.session_state.history) > 0:

    df = pd.DataFrame(
        st.session_state.history
    )

    fig1 = px.line(

        df,
        x="Round",
        y="Revenue",
        title="Revenue Trend"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2 = px.line(

        df,
        x="Round",
        y="Stock Price",
        title="Stock Price Trend"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

else:

    st.info(
        "No decision rounds completed yet."
    )

# =========================================================
# RESET BUTTON
# =========================================================

st.sidebar.header("Simulation Control")

if st.sidebar.button(
    "Reset Simulation"
):

    for key in list(
        st.session_state.keys()
    ):

        del st.session_state[key]

    st.rerun()
