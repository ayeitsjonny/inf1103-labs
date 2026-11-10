from __future__ import annotations

from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Abstract base class for every product in the system.

    Contract every subclass must keep (Liskov Substitution Principle):
      - update_stock(quantity) accepts any int >= 0, sets the stock to that
        value and returns True; anything else is rejected and returns False.
        It never raises for bad input.
      - get_fulfilment_info() returns a str describing fulfilment.
      - display_information() prints the product and returns None.
    """

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier):
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = 0
        self.update_stock(stock)  # reuse validation
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
    def update_stock(self, quantity: int) -> bool:
        """Set stock to quantity, rejecting invalid values."""
        if not isinstance(quantity, int) or quantity < 0:
            print("Invalid stock quantity. Must be a whole number >= 0.")
            return False
        self.__stock = quantity
        return True

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
