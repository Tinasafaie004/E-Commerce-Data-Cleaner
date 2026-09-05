# E-Commerce Data Cleaner

E-Commerce Data Cleaner is a data cleaning and analysis project that transforms a messy e-commerce order dataset into a clean, analysis-ready format. The program identifies data quality issues, applies standardization rules, removes duplicates, and generates business-focused insights for inventory management and order fulfillment.

## Skills Practiced

- Data inspection and quality assessment
- Text standardization (whitespace, capitalization)
- Data type conversion and error handling
- Handling missing values strategically
- Duplicate detection and removal
- Filtering with multiple boolean conditions
- Creating derived columns (inventory_value)
- Sorting and ranking data
- CSV export with proper formatting
- Translating business requirements into data queries

## Requirements

- Python 3.8 or later
- pandas

Install the dependency with:

```bash
pip install pandas
```

## Run the project

Open a terminal in this directory and run:

```bash
python order_cleaner.py
```

The script expects `messy_orders.csv` to be in the same directory. It will:

1. Inspect and report on data quality issues
2. Clean and standardize all columns
3. Validate the cleaning process
4. Generate five business-focused datasets
5. Export the cleaned data to `clean_orders.csv`

## Output Sections

### Part 1: Data Inspection
Displays:
- First 5 rows of raw data
- Dataset dimensions and column types
- Count of missing values (before cleaning)
- Count of duplicate rows (before cleaning)

### Part 2: Data Cleaning
Applies standardization:
- **Product**: Remove whitespace, apply title case
- **Category**: Standardize to recognized values (Electronics, Stationery, Office)
- **City**: Apply title case, replace missing with "Unknown"
- **Status**: Standardize to recognized values (Completed, Pending, Cancelled)
- **Price**: Convert to numeric, invalid values become NaN
- **Stock**: Convert to numeric, invalid values become NaN
- Remove completely duplicate rows

### Part 3: Validation
Displays:
- Missing values before vs. after cleaning
- Duplicate rows before vs. after cleaning
- Data types of all columns
- Unique values in categorical columns (category, city, status)

### Part 4: Analysis-Ready Dataset
Creates `usable_orders`:
- Contains only records with both price and stock values
- Includes new `inventory_value` column (price × stock)

### Part 5: Business Requests
Generates five filtered datasets:

- **High-Value Inventory**: Products with inventory_value ≥ $1,000, sorted highest to lowest
- **Affordable Electronics**: Electronics under $60 with 20+ units in stock, sorted by price
- **Toronto Fulfillment**: Completed orders from Toronto, sorted by order_id
- **Attention Queue**: Items with stock < 20 OR pending status, sorted by stock level
- **Top Products**: The 5 products with highest inventory value

### Part 6: Export
Saves cleaned data to `clean_orders.csv` (without row indices)

## Dataset Columns

| Column | Description |
| --- | --- |
| `order_id` | Unique order identifier |
| `product` | Product name |
| `category` | Product category |
| `price` | Unit price (numeric) |
| `stock` | Quantity in stock (numeric) |
| `city` | Delivery city |
| `status` | Order status |
| `inventory_value` | Derived: price × stock |

## Data Quality Handling

### Missing Values
- City: Replaced with "Unknown" (useful for analysis)
- Price/Stock: Converted to NaN for invalid entries (excluded from analysis)

### Text Standardization
- Whitespace trimmed from all text columns
- Proper title case applied
- Consistent category/status values enforced

### Duplicates
- Complete row duplicates removed
- Clean dataset indexed and exported without row numbers

## Project Files

```text
E-Commerce_Data_Cleaner/
├── order_cleaner.py
├── messy_orders.csv
├── clean_orders.csv
└── README.md
```

## Example Usage

Run the script to see console output showing:
- Data quality metrics before and after cleaning
- Verification that standardization worked (unique values per column)
- Business analysis results (high-value items, affordable products, etc.)
