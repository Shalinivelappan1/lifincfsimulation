import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.express as px
import random

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Corporate Finance Learning Lab",
    layout="wide"
)

# ==================================================
# SESSION STATE
# ==================================================

defaults = {
    "round": 1,
    "cash": 200.0,
    "debt": 150.0,
    "equity": 350.0,
    "revenue": 500.0,
    "profit": 60.0,
    "stock_price": 100.0,
    "wacc": 0.10,
    "history": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==================================================
# FUNCTIONS
# ==================================================

def generate_macro_conditions():

    return {
        "GDP Growth": random.choice([3, 4, 5, 6, 7]),
        "Inflation": random.choice([3, 4, 5, 6, 7, 8]),
        "Interest Rate": random.choice([5, 6, 7, 8, 9]),
        "Market Sentiment": random.choice(
            ["Bullish", "Neutral", "Bearish"]
        )
    }


def calculate_wacc(debt, equity, interest_rate):

    total = debt + equity

    if total == 0:
        return 0.10

    rd = interest_rate / 100
    re = 0.14
    tax = 0.30

    wacc = (
        (equity / total) * re
        + (debt / total) * rd * (1 - tax)
    )

    return round(wacc, 4)


def calculate_npv(
    initial_investment,
    annual_cashflow,
    discount_rate,
    years=5
):

    npv = -initial_investment

    for t in range(1, years + 1):

        npv += (
            annual_cashflow /
            ((1 + discount_rate) ** t)
        )

    return round(npv, 2)


def random_market_shock():

    events = [
        ("Interest Rate Hike", -5),
        ("Economic Boom", 10),
        ("Supply Chain Disruption", -8),
        ("Technology Breakthrough", 12),
        ("ESG Regulation", -3),
        ("Banking Liquidity Crisis", -10),
        ("Stable Economy", 2),
    ]

    return random.choice(events)


macro = generate_macro_conditions()

# ==================================================
# TITLE
# ==================================================

st.title("Corporate Finance Learning Lab")

st.markdown("""
An interactive MBA-level learning platform for:

- Capital Budgeting
- Capital Structure
- Dividend Policy
- Working Capital Management
- Risk Management
- Firm Valuation

Students can experiment with financial decisions
and observe their impact on firm value,
liquidity, leverage, and shareholder wealth.
""")

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("Simulation Status")

st.sidebar.metric(
    "Round",
    st.session_state.round
)

st.sidebar.header("Macroeconomic Conditions")

for key, value in macro.items():
    st.sidebar.write(f"**{key}:** {value}")

# ==================================================
# DASHBOARD
# ==================================================

st.header("Company Dashboard")

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

# ==================================================
# TABS
# ==================================================

(
    overview_tab,
    budgeting_tab,
    capital_structure_tab,
    dividend_tab,
    working_capital_tab,
    risk_tab,
    valuation_tab,
    results_tab
) = st.tabs([
    "Financial Health Overview",
    "Capital Budgeting",
    "Capital Structure",
    "Dividend Policy",
    "Working Capital",
    "Risk Management",
    "Firm Valuation",
    "Strategic Reflection"
])

# ==================================================
# OVERVIEW TAB
# ==================================================

with overview_tab:

    st.subheader("Financial Health Overview")

    debt_equity_ratio = (
        st.session_state.debt /
        st.session_state.equity
    )

    current_ratio = (
        (st.session_state.cash + 100) / 80
    )

    o1, o2, o3 = st.columns(3)

    o1.metric(
        "Debt-to-Equity Ratio",
        round(debt_equity_ratio, 2)
    )

    o2.metric(
        "Current Ratio",
        round(current_ratio, 2)
    )

    o3.metric(
        "WACC",
        f"{round(st.session_state.wacc*100,2)}%"
    )

    st.info("""
    This dashboard summarizes:
    - leverage,
    - liquidity,
    - financing cost,
    - and financial stability.
    """)

# ==================================================
# CAPITAL BUDGETING
# ==================================================

with budgeting_tab:

    st.subheader("Capital Budgeting")

    st.latex(
        r'''NPV = \sum_{t=1}^{n}\frac{CF_t}{(1+r)^t} - C_0'''
    )

    st.latex(
        r'''IRR : NPV = 0'''
    )

    st.latex(
        r'''PI = \frac{PV\ of\ Future\ Cash\ Flows}{Initial\ Investment}'''
    )

    with st.expander("Learn About Capital Budgeting"):
        st.write("""
        Capital budgeting evaluates long-term investments.
        Positive NPV projects create shareholder wealth.
        """)

    project = st.selectbox(
        "Select Project",
        [
            "Automation",
            "AI Expansion",
            "ESG Upgrade",
            "International Expansion"
        ]
    )

    scenario = st.selectbox(
        "Scenario Analysis",
        [
            "Best Case",
            "Base Case",
            "Worst Case"
        ]
    )

    investment_amount = st.slider(
        "Investment Amount (₹ Cr)",
        10,
        200,
        50
    )

    expected_cashflow = st.slider(
        "Expected Annual Cash Flow (₹ Cr)",
        5,
        100,
        20
    )

    discount_rate = st.slider(
        "Discount Rate (%)",
        5,
        20,
        10
    )

    if scenario == "Best Case":
        scenario_multiplier = 1.3

    elif scenario == "Worst Case":
        scenario_multiplier = 0.7

    else:
        scenario_multiplier = 1.0

    adjusted_cashflow = (
        expected_cashflow *
        scenario_multiplier
    )

    npv = calculate_npv(
        investment_amount,
        adjusted_cashflow,
        discount_rate / 100
    )

    cashflows = [-investment_amount]

    for i in range(5):
        cashflows.append(adjusted_cashflow)

    irr = round(
        npf.irr(cashflows) * 100,
        2
    )

    payback_period = round(
        investment_amount /
        adjusted_cashflow,
        2
    )

    profitability_index = round(
        (npv + investment_amount) /
        investment_amount,
        2
    )

    b1, b2, b3, b4 = st.columns(4)

    b1.metric("NPV", f"₹ {npv} Cr")
    b2.metric("IRR (%)", irr)
    b3.metric("Payback", payback_period)
    b4.metric("PI", profitability_index)

    if npv > 0:
        st.success(
            "The project is expected to create shareholder value."
        )

    else:
        st.error(
            "The project may destroy shareholder value."
        )

# ==================================================
# CAPITAL STRUCTURE
# ==================================================

with capital_structure_tab:

    st.subheader("Capital Structure")

    st.latex(
        r'''WACC = \frac{E}{V}R_e + \frac{D}{V}R_d(1-T)'''
    )

    st.latex(
        r'''R_e = R_f + \beta(R_m - R_f)'''
    )

    risk_free_rate = st.slider(
        "Risk-Free Rate (%)",
        2,
        10,
        5
    )

    beta = st.slider(
        "Beta",
        0.5,
        2.0,
        1.0
    )

    market_return = st.slider(
        "Expected Market Return (%)",
        6,
        18,
        12
    )

    cost_of_equity = round(
        risk_free_rate +
        beta * (
            market_return -
            risk_free_rate
        ),
        2
    )

    st.metric(
        "Cost of Equity (CAPM)",
        f"{cost_of_equity}%"
    )

    debt_financing = st.slider(
        "New Debt Raised (₹ Cr)",
        0,
        200,
        20
    )

    equity_financing = st.slider(
        "New Equity Raised (₹ Cr)",
        0,
        200,
        10
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
        macro["Interest Rate"]
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

    if de_ratio < 0.5:
        st.success(
            "The firm maintains conservative leverage."
        )

    elif de_ratio < 1.5:
        st.warning(
            "The firm uses moderate leverage."
        )

    else:
        st.error(
            "High leverage may increase bankruptcy risk."
        )

# ==================================================
# DIVIDEND POLICY
# ==================================================

with dividend_tab:

    st.subheader("Dividend Policy")

    st.latex(
        r'''Dividend\ Payout\ Ratio = \frac{Dividends}{Net\ Income}'''
    )

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

    if dividend_policy == "High Dividend":

        st.warning("""
        High dividends improve short-term
        investor satisfaction but reduce
        internal financing flexibility.
        """)

    elif dividend_policy == "No Dividend":

        st.info("""
        Retained earnings may support
        future investment opportunities.
        """)

    elif dividend_policy == "Share Buyback":

        st.success("""
        Buybacks may improve EPS
        and signal management confidence.
        """)

# ==================================================
# WORKING CAPITAL
# ==================================================

with working_capital_tab:

    st.subheader(
        "Working Capital Management"
    )

    st.latex(
        r'''CCC = DIO + DSO - DPO'''
    )

    credit_policy = st.selectbox(
        "Credit Policy",
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
        "Supplier Payment Strategy",
        [
            "Early",
            "Standard",
            "Delayed"
        ]
    )

    receivable_days = {
        "Strict": 30,
        "Moderate": 60,
        "Liberal": 90
    }[credit_policy]

    inventory_days = {
        "Low": 30,
        "Medium": 60,
        "High": 90
    }[inventory_policy]

    payable_days = {
        "Early": 20,
        "Standard": 45,
        "Delayed": 75
    }[supplier_payment]

    ccc = (
        inventory_days +
        receivable_days -
        payable_days
    )

    w1, w2 = st.columns(2)

    w1.metric(
        "Cash Conversion Cycle",
        f"{ccc} Days"
    )

    w2.metric(
        "Current Ratio",
        round(current_ratio, 2)
    )

    if ccc > 90:
        st.warning(
            "High CCC may create liquidity stress."
        )

# ==================================================
# RISK MANAGEMENT
# ==================================================

with risk_tab:

    st.subheader("Risk Management")

    hedge_policy = st.selectbox(
        "Hedging Strategy",
        [
            "No Hedging",
            "Partial Hedging",
            "Full Hedging"
        ]
    )

    current_risk = random.choice([
        "Interest Rate Risk",
        "FX Risk",
        "Commodity Risk",
        "Liquidity Risk"
    ])

    st.metric(
        "Current Major Risk",
        current_risk
    )

# ==================================================
# FIRM VALUATION
# ==================================================

with valuation_tab:

    st.subheader("Firm Valuation")

    st.latex(
        r'''Firm\ Value = \sum_{t=1}^{n}\frac{FCFF_t}{(1+WACC)^t}'''
    )

    estimated_value = round(
        st.session_state.profit /
        st.session_state.wacc,
        2
    )

    st.metric(
        "Estimated Firm Value",
        f"₹ {estimated_value} Cr"
    )

# ==================================================
# RUN SIMULATION
# ==================================================

st.header("Run Simulation")

if st.button("Run Simulation Round"):

    shock_name, shock_effect = (
        random_market_shock()
    )

    revenue_growth = np.random.uniform(
        0.02,
        0.15
    )

    if credit_policy == "Liberal":
        revenue_growth += 0.03

    updated_revenue = (
        st.session_state.revenue *
        (1 + revenue_growth)
    )

    updated_profit = (
        updated_revenue * 0.12
    ) + shock_effect

    dividend_amount = (
        updated_profit *
        (dividend_payout / 100)
    )

    updated_cash = (
        st.session_state.cash
        + updated_profit
        - investment_amount
        + debt_financing
        + equity_financing
        - dividend_amount
    )

    updated_stock_price = max(
        10,
        st.session_state.stock_price +
        (updated_profit / 10)
    )

    # UPDATE STATE

    st.session_state.revenue = updated_revenue
    st.session_state.profit = updated_profit
    st.session_state.cash = updated_cash
    st.session_state.stock_price = updated_stock_price
    st.session_state.debt = projected_debt
    st.session_state.equity = projected_equity
    st.session_state.wacc = projected_wacc

    # HISTORY

    st.session_state.history.append({
        "Round": st.session_state.round,
        "Revenue": updated_revenue,
        "Profit": updated_profit,
        "Cash": updated_cash,
        "Stock Price": updated_stock_price
    })

    st.session_state.round += 1

    st.success(
        f"Simulation Completed: {shock_name}"
    )

# ==================================================
# FINANCIAL STATEMENTS
# ==================================================

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
    st.dataframe(income_statement)

with f2:
    st.subheader("Balance Sheet")
    st.dataframe(balance_sheet)

# ==================================================
# REFLECTION QUESTIONS
# ==================================================

st.header("Strategic Reflection Questions")

st.text_area(
    "Explain how your investment decision impacts shareholder wealth.",
    height=120
)

st.text_area(
    "Discuss whether your financing strategy balances growth and financial risk effectively.",
    height=120
)

st.text_area(
    "How did working capital decisions affect liquidity and operational efficiency?",
    height=120
)

# ==================================================
# RESULTS
# ==================================================

with results_tab:

    st.subheader(
        "Strategic Reflection Dashboard"
    )

    if len(st.session_state.history) > 0:

        df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(df)

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
            "No simulation rounds completed yet."
        )

# ==================================================
# RESET BUTTON
# ==================================================

st.sidebar.header("Simulation Control")

if st.sidebar.button(
    "Reset Simulation"
):

    for key in list(
        st.session_state.keys()
    ):
        del st.session_state[key]

    st.rerun()
