from __future__ import annotations

from product import Product


class OrderLine:
    """One product and the quantity of it requested in an order.

    Composition: an OrderLine is a PART of exactly one Order. It is only
    ever created by Order.add_order_line() (it lives in this module next
    to Order for that reason) and is never moved to another Order.

    Association: the OrderLine refers to a Product but does NOT own it.
    The Product exists independently and may also sit in an Inventory."""

    def __init__(self, product: Product, quantity: int):
        if not isinstance(quantity, int) or quantity < 1:
            raise ValueError("Quantity must be a whole number >= 1.")
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
    When the Order goes away, its lines go with it."""

    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

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

    def calculate_total(self) -> float:
        # Ask each part for its subtotal rather than doing the maths here.
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_information(self) -> None:
        print(f"Order {self.__order_id}")
        if not self.__order_lines:
            print("  (no order lines)")
        for line in self.__order_lines:
            line.display_information()
        print(f"  Total: ${self.calculate_total():.2f}")

    def __len__(self) -> int:
        return len(self.__order_lines)
