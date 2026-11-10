from __future__ import annotations

from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped. Inherits from Product (is-a)
    and signs the CanBeShipped contract (must-be-able-to)."""

    BASE_SHIPPING: float = 5.00      # flat fee ($)
    RATE_PER_KG: float = 2.50        # $ per kilogram

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        if not isinstance(weight, (int, float)) or weight < 0:
            raise ValueError("Weight must be a number >= 0 (kg).")
        self.__weight: float = float(weight)

    def get_weight(self) -> float:
        return self.__weight

    # ---- overrides ----
    def display_information(self) -> None:
        super().display_information()
        print(f"    Weight: {self.__weight:.2f} kg | "
              f"Shipping: ${self.calculate_shipping_cost():.2f}")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    # ---- Product's abstract method ----
    def get_fulfilment_info(self) -> str:
        return "Physical product: requires storage and physical shipping."

    # ---- CanBeShipped's abstract method ----
    def calculate_shipping_cost(self) -> float:
        return self.BASE_SHIPPING + self.RATE_PER_KG * self.__weight

    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> PhysicalProduct:
        return cls(data["product_id"], data["name"], data["price"],
                   data["stock"], supplier, data["weight"])
