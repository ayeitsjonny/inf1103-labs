from __future__ import annotations

from product import Product
from discount import DiscountStrategy, NoDiscount


class OrderLine:
    """One product and the quantity of it requested in an order.

    Composition: an OrderLine is a PART of exactly one Order. It is only
    ever created by Order.add_order_line() (it lives in this module next
    to Order for that reason) and is never moved to another Order.

    Association: the OrderLine refers to a Product but does NOT own it.
    The Product exists independently and may also sit in an Inventory."""

    def __init__(self, product: Product, quantity: int):
        # OrderLine protects its own quantity, so no caller has to.
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("Quantity must be a whole number.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"  {self.__product.get_product_id():<6} "
              f"{self.__product.get_name():<15} "
              f"x{self.__quantity:<3} @ ${self.__product.get_price():>8.2f}"
              f" = ${self.calculate_subtotal():>9.2f}")


class Order:
    """Composition: an Order creates and manages its own OrderLine objects.
    Outside code passes in a Product and a quantity - never a ready-made
    OrderLine - so every line is born inside, and belongs to, this Order.
    When the Order goes away, its lines go with it.

    Strategy pattern (Lab 9): the Order is GIVEN a DiscountStrategy and just
    calls its apply() method. It contains no if/elif about discount types,
    so new discounts never require changes here.
    Association (not composition): the strategy is something the order
    uses, not a part of it. It is created outside, can be swapped with
    set_discount(), and one strategy object can be shared by many orders.
    Multiplicity: Order * ---> 1 DiscountStrategy."""

    def __init__(self, order_id: str,
                 discount: DiscountStrategy | None = None):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = NoDiscount()
        if discount is not None:
            self.set_discount(discount)

    def get_order_id(self) -> str:
        return self.__order_id

    def get_discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Swap the discount strategy at any time."""
        if not isinstance(discount, DiscountStrategy):
            raise TypeError("discount must be a DiscountStrategy.")
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)   # created HERE
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove (and discard) the line for this product. The Product
        itself is unaffected - only the line is deleted."""
        for line in self.__order_lines:
            if line.get_product().get_product_id().lower() == product_id.lower():
                self.__order_lines.remove(line)
                return True
        return False

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        """Read-only view: a tuple, so callers can't add/remove lines
        or slip a line into this Order from outside."""
        return tuple(self.__order_lines)

    def calculate_subtotal(self) -> float:
        """Total BEFORE any discount."""
        # Ask each part for its subtotal rather than doing the maths here.
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def calculate_total(self) -> float:
        """Total AFTER the discount: delegate to the strategy."""
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        return self.__discount.apply(total)

    def display_information(self) -> None:
        print(f"Order {self.__order_id}")
        if not self.__order_lines:
            print("  (no order lines)")
        for line in self.__order_lines:
            line.display_information()
        print(f"  Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"  Discount: {self.__discount}")
        print(f"  Total:    ${self.calculate_total():.2f}")

    def __len__(self) -> int:
        return len(self.__order_lines)
