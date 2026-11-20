from __future__ import annotations

import unittest

from order import Order, OrderLine
from product_factory import ProductFactory
from tests.helpers import make_product, make_supplier


class TestProductValidation(unittest.TestCase):
    def test_price_must_be_greater_than_zero(self):
        for bad_price in (0, -1, -0.01):
            with self.subTest(price=bad_price):
                with self.assertRaises(ValueError) as ctx:
                    make_product(price=bad_price)
                self.assertIn("greater than zero", str(ctx.exception))

    def test_stock_cannot_be_negative_on_creation(self):
        with self.assertRaises(ValueError) as ctx:
            make_product(stock=-1)
        self.assertIn("cannot be negative", str(ctx.exception))

    def test_zero_stock_is_allowed(self):
        self.assertEqual(make_product(stock=0).get_stock(), 0)

    def test_update_stock_rejects_negative_and_keeps_old_value(self):
        product = make_product(stock=10)
        with self.assertRaises(ValueError):
            product.update_stock(-5)
        self.assertEqual(product.get_stock(), 10)

    def test_every_subclass_keeps_the_stock_rule(self):
        """LSP: no subclass may skip Product's validation."""
        for product_type in ("physical", "digital", "subscription"):
            with self.subTest(product_type=product_type):
                with self.assertRaises(ValueError):
                    ProductFactory.create(product_type, "X1", "Item", 10.0,
                                          -3, make_supplier())


class TestOrderLineValidation(unittest.TestCase):
    def test_quantity_must_be_greater_than_zero(self):
        for bad_quantity in (0, -2):
            with self.subTest(quantity=bad_quantity):
                with self.assertRaises(ValueError) as ctx:
                    OrderLine(make_product(), bad_quantity)
                self.assertEqual(str(ctx.exception),
                                 "Quantity must be greater than zero.")

    def test_order_rejects_bad_line_and_stays_unchanged(self):
        order = Order("O001")
        with self.assertRaises(ValueError):
            order.add_order_line(make_product(), 0)
        self.assertEqual(len(order), 0)


if __name__ == "__main__":
    unittest.main()
