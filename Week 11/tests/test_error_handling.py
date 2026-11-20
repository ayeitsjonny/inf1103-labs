from __future__ import annotations

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from inventory import Inventory
from main import get_positive_float, load_products
from tests.helpers import make_supplier

LAB_CSV = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


class TestGetPositiveFloat(unittest.TestCase):
    def test_keeps_asking_until_valid(self):
        """Predict first 5.1: abc, then -5, then 12.50."""
        out = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), \
                redirect_stdout(out):
            value = get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(out.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_zero_is_rejected(self):
        with patch("builtins.input", side_effect=["0", "1"]), \
                redirect_stdout(io.StringIO()):
            self.assertEqual(get_positive_float("Price: "), 1.0)


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory("Test")
        self.supplier = make_supplier()
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def run_load(self, path: str) -> list[str]:
        out = io.StringIO()
        with redirect_stdout(out):
            load_products(path, self.inventory, self.supplier)
        return out.getvalue().splitlines()

    def test_lab_file_skips_bad_rows_and_loads_the_rest(self):
        path = os.path.join(self.tmp.name, "products.csv")
        with open(path, "w", newline="") as f:
            f.write(LAB_CSV)
        lines = self.run_load(path)

        self.assertEqual(len(self.inventory), 3)
        for product_id in ("P001", "D001", "P003"):
            self.assertIsNotNone(self.inventory.find_product(product_id))
        for product_id in ("S001", "P002"):
            self.assertIsNone(self.inventory.find_product(product_id))

        self.assertEqual(len(lines), 4)
        self.assertIn("Unknown product type: service", lines[0])
        self.assertIn("could not convert string to float: 'abc'", lines[1])
        self.assertEqual(lines[2], "3 products loaded.")
        self.assertEqual(lines[3], "Load attempt finished.")

    def test_missing_file_is_handled_gracefully(self):
        path = os.path.join(self.tmp.name, "nope.csv")
        lines = self.run_load(path)          # must not raise
        self.assertEqual(lines, [f"Products file not found: {path}",
                                 "Load attempt finished."])
        self.assertEqual(len(self.inventory), 0)

    def test_negative_stock_row_is_skipped(self):
        path = os.path.join(self.tmp.name, "neg.csv")
        with open(path, "w", newline="") as f:
            f.write("product_type,product_id,name,price,stock_quantity\n"
                    "physical,P009,Broken,10.00,-4\n"
                    "digital,D009,Fine,5.00,1\n")
        lines = self.run_load(path)
        self.assertEqual(len(self.inventory), 1)
        self.assertIn("cannot be negative", lines[0])


if __name__ == "__main__":
    unittest.main()
