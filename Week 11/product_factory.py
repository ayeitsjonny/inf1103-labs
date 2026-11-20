from __future__ import annotations

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from subscription_product import SubscriptionProduct
from supplier import Supplier


class ProductFactory:
    """Factory pattern: the ONE place that decides which Product subclass
    to build. The rest of the program asks for a "physical" / "digital" /
    "subscription" product and gets back a Product - it never names a
    concrete class, so it stays decoupled from them.

    Trade-off: adding a new product type still means editing create()
    (so the factory itself is not closed for modification). That is
    accepted here: the change is in one place instead of scattered across
    main.py, and a registry/plugin design would be over-engineering for a
    system with three product types.

    Each subclass needs one extra value, so those are optional keyword
    arguments with defaults (a CSV row, for example, has no weight)."""

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, *,
               weight: float = 0.0, download_size: float = 0.0,
               billing_months: int = 1) -> Product:
        kind = str(product_type).strip().lower()
        if kind == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity,
                                   supplier, weight)
        elif kind == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity,
                                  supplier, download_size)
        elif kind == "subscription":
            return SubscriptionProduct(product_id, name, price,
                                       stock_quantity, supplier,
                                       billing_months)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
