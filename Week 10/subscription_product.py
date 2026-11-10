from __future__ import annotations

from product import Product
from supplier import Supplier


class SubscriptionProduct(Product):
    """A product billed repeatedly (e.g. a software subscription).
    "stock" here means subscription seats available."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, billing_months: int):
        super().__init__(product_id, name, price, stock, supplier)
        if not isinstance(billing_months, int) or billing_months < 1:
            raise ValueError(
                "Billing period must be a whole number of months >= 1.")
        self.__billing_months: int = billing_months

    def get_billing_months(self) -> int:
        return self.__billing_months

    def display_information(self) -> None:
        super().display_information()
        print(f"    Billed every {self.__billing_months} month(s)")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "subscription"
        data["billing_months"] = self.__billing_months
        return data

    def get_fulfilment_info(self) -> str:
        return ("Subscription product: activated online and billed on a "
                "recurring cycle.")

    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> SubscriptionProduct:
        return cls(data["product_id"], data["name"], data["price"],
                   data["stock"], supplier, data["billing_months"])
