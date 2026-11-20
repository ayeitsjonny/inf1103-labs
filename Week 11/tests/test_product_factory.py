from __future__ import annotations

import ast
import pathlib
import unittest

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from subscription_product import SubscriptionProduct
from product_factory import ProductFactory
from tests.helpers import make_supplier

PROJECT = pathlib.Path(__file__).resolve().parent.parent


class TestProductFactory(unittest.TestCase):
    def setUp(self):
        self.supplier = make_supplier()

    def test_creates_each_type(self):
        cases = [("physical", PhysicalProduct), ("digital", DigitalProduct),
                 ("subscription", SubscriptionProduct)]
        for product_type, expected_class in cases:
            with self.subTest(product_type=product_type):
                product = ProductFactory.create(product_type, "X1", "Item",
                                                10.0, 5, self.supplier)
                self.assertIsInstance(product, expected_class)
                self.assertIsInstance(product, Product)

    def test_type_is_case_and_space_insensitive(self):
        product = ProductFactory.create("  Digital ", "D1", "App", 9.9, 1,
                                        self.supplier)
        self.assertIsInstance(product, DigitalProduct)

    def test_extra_details_are_passed_through(self):
        lamp = ProductFactory.create("physical", "P1", "Lamp", 25, 3,
                                     self.supplier, weight=2.0)
        self.assertEqual(lamp.get_weight(), 2.0)
        sub = ProductFactory.create("subscription", "S1", "Support", 99, 3,
                                    self.supplier, billing_months=12)
        self.assertEqual(sub.get_billing_months(), 12)

    def test_unknown_type_raises_clear_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "S001", "Installation", 30.0, 5,
                                  self.supplier)
        self.assertEqual(str(ctx.exception), "Unknown product type: service")

    def test_main_never_creates_products_directly(self):
        """Only product_factory.py may call the concrete constructors."""
        concrete = {"PhysicalProduct", "DigitalProduct", "SubscriptionProduct"}
        for path in PROJECT.glob("*.py"):
            if path.name == "product_factory.py":
                continue
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, concrete,
                                     f"{path.name} creates {node.func.id} directly")


if __name__ == "__main__":
    unittest.main()
