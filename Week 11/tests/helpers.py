from __future__ import annotations

from supplier import Supplier
from product import Product
from product_factory import ProductFactory


def make_supplier() -> Supplier:
    return Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")


def make_product(price: float = 50.0, stock: int = 10,
                 product_id: str = "P001") -> Product:
    return ProductFactory.create("physical", product_id, "Test Item", price,
                                 stock, make_supplier(), weight=1.0)
