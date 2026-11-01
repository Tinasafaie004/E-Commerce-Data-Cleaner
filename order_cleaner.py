"""
E-Commerce Data Cleaner
-----------------------

A Pandas-based data cleaning and analysis project that transforms messy
e-commerce order data into a clean, analysis-ready dataset.

The program inspects data quality issues, standardizes column values,
removes duplicates, creates business-ready datasets, and answers key
business questions about inventory value, product availability, and
order status across different cities.

The cleaning logic lives in functions so that both this script and the
web page (app.py) can use it.
"""


import pandas as pd


REQUIRED_COLUMNS = ["order_id", "product", "category", "price", "stock", "city", "status"]

# str.title() turns "USB Cable" into "Usb Cable", so these words are restored afterwards.
ACRONYMS = {r"\bUsb\b": "USB", r"\bHdmi\b": "HDMI", r"\bLed\b": "LED"}


def find_missing_columns(orders):
    """Return the required columns that are not in the DataFrame."""
    return [column for column in REQUIRED_COLUMNS if column not in orders.columns]


def standardize_text(column):
    """Remove surrounding whitespace, apply title capitalization, and treat blanks as missing."""
    cleaned = column.astype("string").str.strip().str.title()
    return cleaned.replace("", pd.NA)


def to_number(column):
    """Convert to numeric. Invalid entries (non-numeric strings) become missing."""
    numbers = pd.to_numeric(column, errors="coerce")

    # Pandas reads the text "inf" as infinity, which isn't a real price or stock level.
    numbers = numbers.replace([float("inf"), float("-inf")], float("nan"))

    # convert_dtypes keeps whole numbers as integers, so stock shows as 18 and not 18.0.
    return numbers.convert_dtypes()


def clean_data(orders):
    """Return a cleaned, standardized copy of the raw orders."""
    # Create an independent copy of the original data to preserve the raw dataset.
    clean_orders = orders.copy()

    # A. Product names: Remove whitespace, apply title capitalization, and restore acronyms.
    clean_orders["product"] = standardize_text(clean_orders["product"]).replace(ACRONYMS, regex=True)

    # B. Categories: Standardize to match recognized values (Electronics, Stationery, Office).
    clean_orders["category"] = standardize_text(clean_orders["category"])

    # C. Cities: Standardize the text. Replace missing values with "Unknown".
    clean_orders["city"] = standardize_text(clean_orders["city"]).fillna("Unknown")

    # D. Status: Standardize to recognized values (Completed, Pending, Cancelled).
    clean_orders["status"] = standardize_text(clean_orders["status"])

    # E. Price and stock: Convert to numeric.
    clean_orders["price"] = to_number(clean_orders["price"])
    clean_orders["stock"] = to_number(clean_orders["stock"])

    # F. Duplicates: Remove completely duplicated rows from the cleaned dataset.
    return clean_orders.drop_duplicates().reset_index(drop=True)


def summarize_cleaning(orders, clean_orders):
    """Count what the cleaning changed, for the validation report."""
    return {
        "rows_before": len(orders),
        "rows_after": len(clean_orders),
        "duplicates_removed": len(orders) - len(clean_orders),
        "cities_filled": int((clean_orders["city"] == "Unknown").sum()),
        "invalid_prices": int(clean_orders["price"].isna().sum()),
        "invalid_stock": int(clean_orders["stock"].isna().sum()),
    }


def create_usable_orders(clean_orders):
    """Keep records with both price and stock, and add inventory_value = price × stock."""
    usable_orders = clean_orders[
        (clean_orders["price"].notna()) &
        (clean_orders["stock"].notna())
    ].copy()
    usable_orders["inventory_value"] = usable_orders["price"] * usable_orders["stock"]
    return usable_orders


def answer_business_requests(usable_orders):
    """Return the five business requests as a dictionary of title -> DataFrame."""
    # Request 1: Find products with high inventory value (>= $1000).
    # Sort from highest to lowest inventory value for strategic planning.
    high_value_inventory = usable_orders[
        usable_orders["inventory_value"] >= 1000
    ].sort_values("inventory_value", ascending=False)

    # Request 2: Find affordable electronics under $60 with at least 20 units in stock.
    # Sort by price (lowest first) to highlight budget-friendly options.
    affordable_electronics = usable_orders[
        (usable_orders["category"] == "Electronics") &
        (usable_orders["price"] < 60) &
        (usable_orders["stock"] >= 20)
    ].sort_values("price")

    # Request 3: Find completed orders from Toronto.
    # Sort by order_id to track order sequence for fulfillment verification.
    toronto_orders = usable_orders[
        (usable_orders["city"] == "Toronto") &
        (usable_orders["status"] == "Completed")
    ].sort_values("order_id")

    # Request 4: Find items needing attention (low stock OR pending status).
    # Sort by stock level to prioritize items with critical inventory.
    # Note: Uses OR logic (|) not AND logic.
    attention_queue = usable_orders[
        (usable_orders["stock"] < 20) |
        (usable_orders["status"] == "Pending")
    ].sort_values("stock")

    # Request 5: Find the top 5 products by inventory value.
    # Reset index to create clean row numbering (0-4).
    top_products = usable_orders.sort_values(
        "inventory_value", ascending=False
    ).head(5).reset_index(drop=True)

    return {
        "High-value inventory": high_value_inventory,
        "Affordable electronics": affordable_electronics,
        "Toronto completed orders": toronto_orders,
        "Needs attention": attention_queue,
        "Top 5 products": top_products,
    }


def main():
    # Load the raw, messy order data into a DataFrame.
    orders = pd.read_csv("messy_orders.csv")

    # Display a preview of the data, plus column names, data types, and non-null counts.
    print(orders.head(5))
    orders.info()

    clean_orders = clean_data(orders)

    # Display comparison of missing values and duplicates before and after cleaning.
    print("\nMissing values BEFORE cleaning")
    print(orders.isna().sum())
    print("\nMissing values AFTER cleaning")
    print(clean_orders.isna().sum())
    print("\nDuplicates BEFORE cleaning")
    print(orders.duplicated().sum())
    print("\nDuplicates AFTER cleaning")
    print(clean_orders.duplicated().sum())

    # Display data types and unique values to verify the cleaning worked correctly.
    print("\nDATA TYPES AFTER CLEANING")
    print(clean_orders.dtypes)
    for column in ["category", "city", "status"]:
        print(f"\n{column} unique values:")
        print(clean_orders[column].value_counts())

    # Answer the business requests.
    for title, result in answer_business_requests(create_usable_orders(clean_orders)).items():
        print(f"\n{title}")
        print(result)

    # Export the cleaned dataset. index=False prevents writing row indices as an extra column.
    clean_orders.to_csv("clean_orders.csv", index=False)


if __name__ == "__main__":
    main()
