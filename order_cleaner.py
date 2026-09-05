"""
E-Commerce Data Cleaner
-----------------------

A Pandas-based data cleaning and analysis project that transforms messy 
e-commerce order data into a clean, analysis-ready dataset.

The program inspects data quality issues, standardizes column values,
removes duplicates, creates business-ready datasets, and answers key
business questions about inventory value, product availability, and
order status across different cities.
"""


import pandas as pd


# ============================================================
# PART 1 — INSPECT THE MESS
# ============================================================
# Load the raw, messy order data into a DataFrame.
orders = pd.read_csv("messy_orders.csv")

# Display the first five rows to preview the dataset structure and content.
first_five = orders.head(5)
print(first_five)

# Display dataset information including column names, data types, and non-null counts.
orders.info()

# Count missing values in each column before cleaning.
missing_before = orders.isna().sum()

# Count completely duplicated rows before cleaning.
duplicates_before = orders.duplicated().sum()



# ============================================================
# PART 2 — CLEAN THE DATASET
# ============================================================
# Create an independent copy of the original data to preserve the raw dataset.
clean_orders = orders.copy()

# A. Product names: Remove leading/trailing whitespace and apply title capitalization.
clean_orders["product"] = clean_orders["product"].str.strip().str.title()

# B. Categories: Standardize to match recognized values (Electronics, Stationery, Office).
clean_orders["category"] = clean_orders["category"].str.strip().str.title()

# C. Cities: Apply title capitalization and remove whitespace. Replace missing values with "Unknown".
clean_orders["city"] = clean_orders["city"].str.strip().str.title()
clean_orders["city"] = clean_orders["city"].fillna("Unknown")

# D. Status: Standardize to recognized values (Completed, Pending, Cancelled).
clean_orders["status"] = clean_orders["status"].str.strip().str.title()

# E. Price: Convert to numeric. Invalid entries (non-numeric strings) become NaN (missing).
clean_orders["price"] = pd.to_numeric(
    clean_orders["price"],
    errors="coerce"
)

# F. Stock: Convert to numeric. Invalid entries (non-numeric strings) become NaN (missing).
clean_orders["stock"] = pd.to_numeric(
    clean_orders["stock"],
    errors="coerce"
)

# G. Duplicates: Remove completely duplicated rows from the cleaned dataset.
clean_orders = clean_orders.drop_duplicates()



# ============================================================
# PART 3 — VALIDATE YOUR CLEANING
# ============================================================
# Count missing values in each column after cleaning.
missing_after = clean_orders.isna().sum()

# Count completely duplicated rows after cleaning.
duplicates_after = clean_orders.duplicated().sum()

# Display comparison of missing values before and after cleaning.
print("\nMissing values BEFORE cleaning")
print(missing_before)
print("\nMissing values AFTER cleaning")
print(missing_after)

# Display comparison of duplicates before and after cleaning.
print("\nDuplicates BEFORE cleaning")
print(duplicates_before)
print("\nDuplicates AFTER cleaning")
print(duplicates_after)

# Display data types of all columns to verify conversions (e.g., price and stock are numeric).
print("\n" + "="*50)
print("DATA TYPES AFTER CLEANING")
print("="*50)
print(clean_orders.dtypes)

# Inspect unique values in categorical columns to verify standardization worked correctly.
print("\n" + "="*50)
print("UNIQUE VALUES IN CATEGORICAL COLUMNS")
print("="*50)
print("\nCategory unique values:")
print(clean_orders["category"].value_counts())
print("\nCity unique values:")
print(clean_orders["city"].value_counts())
print("\nStatus unique values:")
print(clean_orders["status"].value_counts())



# ============================================================
# PART 4 — CREATE AN ANALYSIS-READY DATASET
# ============================================================
# Create a DataFrame containing only records with both price and stock values.
# These records are usable for financial and inventory analysis.
usable_orders = clean_orders[
    (clean_orders["price"].notna()) &
    (clean_orders["stock"].notna())
].copy()

# Add a new column: inventory_value = price × stock.
# This represents the total monetary value of inventory for each product.
usable_orders["inventory_value"] = usable_orders["price"] * usable_orders["stock"]



# ============================================================
# PART 5 — BUSINESS REQUESTS
# ============================================================
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
# These represent the most valuable inventory holdings.
# Reset index to create clean row numbering (0-4).
top_products = usable_orders.sort_values("inventory_value", ascending=False).head(5).reset_index(drop=True)



# ============================================================
# PART 6 — SAVE THE CLEAN DATA
# ============================================================
# Export the cleaned and standardized dataset to CSV.
# index=False prevents writing the DataFrame's row indices as an extra column.
clean_orders.to_csv('clean_orders.csv', index=False)
