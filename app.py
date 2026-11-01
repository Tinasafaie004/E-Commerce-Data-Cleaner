"""The web page for the data cleaner. Run it with: streamlit run app.py"""

from pathlib import Path

import pandas as pd
import streamlit as st

from order_cleaner import (
    REQUIRED_COLUMNS,
    answer_business_requests,
    clean_data,
    create_usable_orders,
    find_missing_columns,
    summarize_cleaning,
)

SAMPLE_FILE = Path(__file__).parent / "messy_orders.csv"


def load_orders(uploaded_file):
    """Read the uploaded CSV, or the sample data if nothing was uploaded."""
    # dtype=str keeps the raw values exactly as written, so the "before" table shows the mess.
    return pd.read_csv(uploaded_file or SAMPLE_FILE, dtype=str)


st.set_page_config(page_title="E-Commerce Data Cleaner", page_icon="🧹", layout="wide")

st.title("E-Commerce Data Cleaner")
st.write(
    "Messy order data breaks reports. This tool standardizes the text, flags invalid numbers, "
    "removes duplicates, and answers a few inventory questions. Try it with the sample data "
    "or upload your own CSV."
)

uploaded_file = st.file_uploader("Upload an orders CSV (optional)", type="csv")
st.caption(f"Your file needs these columns: {', '.join(REQUIRED_COLUMNS)}. Files are not saved.")

try:
    orders = load_orders(uploaded_file)
except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError):
    st.error("That file couldn't be read as a CSV. Please check the file and try again.")
    st.stop()

missing_columns = find_missing_columns(orders)
if missing_columns:
    st.error(f"That file is missing these columns: {', '.join(missing_columns)}.")
    st.stop()

if uploaded_file is None:
    st.info("Showing the sample data.")

clean_orders = clean_data(orders)
summary = summarize_cleaning(orders, clean_orders)

st.header("What the cleaning found")
rows, duplicates, cities, prices, stock = st.columns(5)
rows.metric("Rows kept", f"{summary['rows_after']} of {summary['rows_before']}")
duplicates.metric("Duplicates removed", summary["duplicates_removed"])
cities.metric("Missing cities", summary["cities_filled"])
prices.metric("Invalid prices", summary["invalid_prices"])
stock.metric("Invalid stock", summary["invalid_stock"])

st.header("Before and after")
before_column, after_column = st.columns(2)
with before_column:
    st.subheader("Before")
    st.dataframe(orders, hide_index=True)
with after_column:
    st.subheader("After")
    st.dataframe(clean_orders, hide_index=True)

st.download_button(
    "Download the clean CSV",
    clean_orders.to_csv(index=False),
    file_name="clean_orders.csv",
    mime="text/csv",
)

st.header("Inventory questions")
st.caption("Rows with an invalid price or stock value are left out of these answers.")
business_requests = answer_business_requests(create_usable_orders(clean_orders))
for tab, (title, result) in zip(st.tabs(list(business_requests)), business_requests.items()):
    with tab:
        if result.empty:
            st.write("No rows match this question.")
        else:
            st.dataframe(result, hide_index=True)
