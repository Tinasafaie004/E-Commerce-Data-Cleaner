import unittest

import pandas as pd

from order_cleaner import clean_data, create_usable_orders, find_missing_columns


def make_orders(**overrides):
    row = {
        "order_id": "1",
        "product": "  desk lamp ",
        "category": " OFFICE",
        "price": "10.50",
        "stock": "4",
        "city": "toronto ",
        "status": "COMPLETED",
    }
    row.update(overrides)
    return pd.DataFrame([row])


class TestCleanData(unittest.TestCase):
    def test_standardizes_text(self):
        clean = clean_data(make_orders()).iloc[0]
        self.assertEqual(clean["product"], "Desk Lamp")
        self.assertEqual(clean["category"], "Office")
        self.assertEqual(clean["city"], "Toronto")
        self.assertEqual(clean["status"], "Completed")

    def test_keeps_acronyms_in_product_names(self):
        clean = clean_data(make_orders(product="USB-C Hub ")).iloc[0]
        self.assertEqual(clean["product"], "USB-C Hub")

    def test_invalid_numbers_become_missing(self):
        clean = clean_data(make_orders(price="inf", stock="none")).iloc[0]
        self.assertTrue(pd.isna(clean["price"]))
        self.assertTrue(pd.isna(clean["stock"]))

    def test_missing_and_blank_cities_become_unknown(self):
        for city in [None, "", "   "]:
            clean = clean_data(make_orders(city=city)).iloc[0]
            self.assertEqual(clean["city"], "Unknown")

    def test_removes_rows_that_only_match_after_cleaning(self):
        orders = pd.concat([make_orders(), make_orders(product="DESK LAMP")])
        self.assertEqual(len(clean_data(orders)), 1)

    def test_handles_a_completely_empty_city_column(self):
        orders = make_orders()
        orders["city"] = float("nan")
        self.assertEqual(clean_data(orders).iloc[0]["city"], "Unknown")


class TestUsableOrders(unittest.TestCase):
    def test_calculates_inventory_value(self):
        usable = create_usable_orders(clean_data(make_orders()))
        self.assertEqual(usable.iloc[0]["inventory_value"], 42)

    def test_leaves_out_rows_without_a_price(self):
        usable = create_usable_orders(clean_data(make_orders(price="unknown")))
        self.assertTrue(usable.empty)


class TestFindMissingColumns(unittest.TestCase):
    def test_names_the_missing_column(self):
        orders = make_orders().drop(columns=["price"])
        self.assertEqual(find_missing_columns(orders), ["price"])


if __name__ == "__main__":
    unittest.main()
