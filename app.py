import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# App Config
# -----------------------------
st.set_page_config(
    page_title="Financial Freedom Simulator",
    layout="wide"
)

st.title("📈 Financial Freedom Simulator")
st.write(
    "Estimate when you reach financial independence while accounting for "
    "inflation and expense growth."
)

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("Your Financial Inputs")

current_net_worth = st.sidebar.number_input(
    "Current Net Worth ($)",
    min_value=0,
    value=100_000,
    step=10_000
)

annual_income = st.sidebar.number_input(
    "Annual Income ($)",
    min_value=0,
    value=120_000,
    step=5_000
)

savings_rate = st.sidebar.slider(
    "Savings Rate (%)",
    min_value=0.0,
    max_value=0.9,
    value=0.25
)

annual_expenses = st.sidebar.number_input(
    "Current Annual Expenses ($)",
    min_value=0,
    value=60_000,
    step=5_000
)

investment_return = st.sidebar.slider(
    "Expected Annual Investment Return (%)",
    min_value=0.0,
    max_value=0.15,
    value=0.07
)

inflation_rate = st.sidebar.slider(
    "Annual Inflation Rate (%)",
    min_value=0.0,
    max_value=0.08,
    value=0.025
)

expense_growth = st.sidebar.slider(
    "Lifestyle / Expense Growth (%)",
    min_value=0.0,
    max_value=0.10,
    value=0.01
)

years = st.sidebar.slider(
    "Years to Simulate",
    min_value=10,
    max_value=60,
    value=30
)

# -----------------------------
# Core Calculations
# -----------------------------
annual_savings = annual_income * savings_rate

net_worth = current_net_worth
expenses = annual_expenses

net_worth_projection = []
expense_projection = []
fi_target_projection = []

for year in range(1, years + 1):
    # Grow investments
    net_worth = net_worth * (1 + investment_return) + annual_savings

    # Grow expenses (inflation + lifestyle creep)
    expenses = expenses * (1 + inflation_rate + expense_growth)

    # Financial Independence target moves over time
    fi_target = expenses * 25

    net_worth_projection.append(net_worth)
    expense_projection.append(expenses)
    fi_target_projection.append(fi_target)

df = pd.DataFrame({
    "Year": np.arange(1, years + 1),
    "Net Worth": net_worth_projection,
    "Annual Expenses": expense_projection,
    "FI Target": fi_target_projection
})

# -----------------------------
# Visualization
# -----------------------------
st.subheader("📊 Net Worth vs Financial Independence Target")

fig, ax = plt.subplots()
ax.plot(df["Year"], df["Net Worth"], label="Net Worth")
ax.plot(df["Year"], df["FI Target"], linestyle="--", label="FI Target")

ax.set_xlabel("Year")
ax.set_ylabel("Dollars ($)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# -----------------------------
# Financial Freedom Result
# -----------------------------
st.subheader("🎯 Financial Independence Outcome")

fi_rows = df[df["Net Worth"] >= df["FI Target"]]

if not fi_rows.empty:
    fi_year = int(fi_rows["Year"].iloc[0])
    st.success(f"🎉 You reach financial freedom in **Year {fi_year}**")
else:
    st.warning("⚠️ Financial freedom not reached within the simulated timeframe.")

# -----------------------------
# Optional Data Table
# -----------------------------
with st.expander("🔍 View Year-by-Year Data"):
    st.dataframe(df.style.format({
        "Net Worth": "${:,.0f}",
        "Annual Expenses": "${:,.0f}",
        "FI Target": "${:,.0f}"
    }))
