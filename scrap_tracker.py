import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Scrap Business Tracker", layout="centered")

st.title("🪨 Scrap Business Tracker")
st.write("Track your scrap material purchases, sales, and profits.")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = []

# Form to input new entry
with st.form("scrap_form"):
    st.subheader("Add New Entry")
    entry_date = st.date_input("Date", date.today())
    material = st.text_input("Material (e.g., Iron, Copper)")
    weight = st.number_input("Weight (kg)", min_value=0.0, step=1.0)
    buy_rate = st.number_input("Buy Rate (₹/kg)", min_value=0.0, step=1.0)
    sell_rate = st.number_input("Sell Rate (₹/kg)", min_value=0.0, step=1.0)
    expenses = st.number_input("Expenses (₹)", min_value=0.0, step=1.0)
    submit = st.form_submit_button("Add Entry")

    if submit:
        buy_total = weight * buy_rate
        sell_total = weight * sell_rate
        profit = sell_total - buy_total - expenses

        st.session_state.data.append({
            "Date": entry_date,
            "Material": material,
            "Weight (kg)": weight,
            "Buy Rate (₹)": buy_rate,
            "Buy Total (₹)": buy_total,
            "Sell Rate (₹)": sell_rate,
            "Sell Total (₹)": sell_total,
            "Expenses (₹)": expenses,
            "Profit (₹)": profit
        })
        st.success("Entry added successfully!")

# Display data table
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.subheader("📊 Business Summary")
    st.dataframe(df, use_container_width=True)

    total_weight = df["Weight (kg)"].sum()
    total_buy = df["Buy Total (₹)"].sum()
    total_sell = df["Sell Total (₹)"].sum()
    total_expenses = df["Expenses (₹)"].sum()
    total_profit = df["Profit (₹)"].sum()

    st.write("---")
    st.metric("Total Weight (kg)", f"{total_weight:.2f}")
    st.metric("Total Buy ₹", f"₹{total_buy:,.2f}")
    st.metric("Total Sell ₹", f"₹{total_sell:,.2f}")
    st.metric("Total Expenses ₹", f"₹{total_expenses:,.2f}")
    st.metric("Net Profit ₹", f"₹{total_profit:,.2f}")

    # Download option
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name="scrap_business_data.csv", mime="text/csv")

