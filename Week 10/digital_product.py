from __future__ import annotations

from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A product delivered by download. Not shippable, so it does NOT
    implement CanBeShipped.

    LSP note: "stock" for a digital product means licence keys available
    to sell. update_stock() is inherited unchanged, so it accepts the same
    inputs and returns the same bool as Product promises."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        if not isinstance(download_size, (int, float)) or download_size < 0:
            raise ValueError("Download size must be a number >= 0 (MB).")
        self.__download_size: float = float(download_size)

    def get_download_size(self) -> float:
        return self.__download_size

    # ---- overrides ----
    def display_information(self) -> None:
        super().display_information()
        print(f"    Download size: {self.__download_size:.2f} MB")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    # ---- Product's abstract method ----
    def get_fulfilment_info(self) -> str:
        return "Digital product: delivered via download link, no shipping."

    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> DigitalProduct:
        return cls(data["product_id"], data["name"], data["price"],
                   data["stock"], supplier, data["download_size"])
