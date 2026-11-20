from __future__ import annotations

from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Abstract base class for every product in the system.

    Validation (Lab 9): Product owns its own rules, so every subclass
    gets them for free and no caller has to remember to check:
      - price must be a number greater than zero
      - stock must be a whole number >= 0
    A broken rule raises ValueError with a clear message.

    Contract every subclass must keep (Liskov Substitution Principle):
      - update_stock(quantity) accepts any int >= 0 and sets the stock;
        anything else raises ValueError and leaves the stock unchanged.
        A subclass must not skip or weaken this rule.
      - get_fulfilment_info() returns a str describing fulfilment.
      - display_information() prints the product and returns None.
    """

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier):
        if not product_id or not name:
            raise ValueError("Product ID and name are required.")
        if (isinstance(price, bool) or not isinstance(price, (int, float))
                or price <= 0):
            raise ValueError("Price must be greater than zero.")
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = float(price)
        self.__stock: int = 0
        self.update_stock(stock)  # reuse validation (raises if invalid)
        # Association: we keep a reference to a Supplier that was created
        # elsewhere. We don't create it and we don't own its lifecycle.
        self.__supplier: Supplier = supplier

    # ---- read-only access ----
    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    # ---- behaviour ----
    def update_stock(self, quantity: int) -> None:
        """Set stock to quantity. Raises ValueError if it is negative or
        not a whole number (the stock is left unchanged)."""
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("Stock quantity must be a whole number.")
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock = quantity

    def display_information(self) -> None:
        print(f"ID: {self.__product_id:<6} | Name: {self.__name:<15} | "
              f"Price: ${self.__price:>9.2f} | Stock: {self.__stock}")
        print(f"    Supplier: {self.__supplier.get_name()} "
              f"({self.__supplier.get_contact_email()})")

    def to_dict(self) -> dict:
        """Common fields only. Subclasses extend this with their own.
        Only the supplier's ID is saved: the Supplier is its own record."""
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.get_supplier_id(),
        }

    # ---- must be provided by every subclass ----
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return a message describing how this product is fulfilled."""
        pass
