from __future__ import annotations

import inspect
import unittest

import order as order_module
from discount import (DiscountStrategy, NoDiscount, PercentageDiscount,
                      BulkDiscount, StudentDiscount)
from order import Order
from tests.helpers import make_product


def order_totalling_250(discount: DiscountStrategy | None = None) -> Order:
    """Lines: 2 x $100 + 1 x $50 = $250."""
    order = Order("O001", discount)
    order.add_order_line(make_product(100.0, product_id="P001"), 2)
    order.add_order_line(make_product(50.0, product_id="P002"), 1)
    return order


class TestStrategies(unittest.TestCase):
    def test_no_discount_returns_total_unchanged(self):
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225)

    def test_bulk_discount_at_and_above_threshold(self):
        bulk = BulkDiscount(200, 20)
        self.assertEqual(bulk.apply(200), 180)     # exactly on threshold
        self.assertEqual(bulk.apply(250), 230)

    def test_bulk_discount_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(199.99), 199.99)

    def test_bulk_discount_never_negative(self):
        self.assertEqual(BulkDiscount(0, 50).apply(30), 0)

    def test_student_discount(self):
        self.assertAlmostEqual(StudentDiscount().apply(100), 95)

    def test_invalid_strategy_arguments_rejected(self):
        for bad in (0, -5, 101, "10", True):
            with self.assertRaises(ValueError):
                PercentageDiscount(bad)
        with self.assertRaises(ValueError):
            BulkDiscount(200, 0)
        with self.assertRaises(ValueError):
            BulkDiscount(-1, 20)

    def test_base_class_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()


class TestOrderUsesStrategy(unittest.TestCase):
    def test_default_is_no_discount(self):
        order = order_totalling_250()
        self.assertIsInstance(order.get_discount(), NoDiscount)
        self.assertEqual(order.calculate_total(), 250)

    def test_predict_first_bulk_then_percentage(self):
        order = order_totalling_250(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)
        self.assertEqual(order.calculate_subtotal(), 250)  # lines untouched

    def test_new_strategy_needs_no_change_to_order(self):
        # A brand-new strategy defined only inside this test.
        class HalfPrice(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total / 2

        self.assertEqual(order_totalling_250(HalfPrice()).calculate_total(),
                         125)

    def test_strategy_can_be_shared_by_two_orders(self):
        shared = PercentageDiscount(10)
        order_a, order_b = order_totalling_250(shared), order_totalling_250(shared)
        self.assertIs(order_a.get_discount(), order_b.get_discount())

    def test_set_discount_rejects_non_strategy(self):
        with self.assertRaises(TypeError):
            order_totalling_250().set_discount("bulk")

    def test_order_has_no_discount_if_elif_logic(self):
        source = inspect.getsource(order_module.Order)
        for word in ("percentage", "bulk", "student", "discount_type"):
            self.assertNotIn(f'"{word}"', source.lower())
        self.assertNotIn("isinstance(self.__discount", source)


if __name__ == "__main__":
    unittest.main()
