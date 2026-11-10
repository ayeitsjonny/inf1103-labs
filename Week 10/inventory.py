from __future__ import annotations

from product import Product


class Inventory:
    """Aggregation: an Inventory groups Product objects, but it does not
    create them or own their lifecycle. Products exist before they are
    added, and removing one only drops the reference - the Product itself
    carries on and can be added to another Inventory.

    The collection is typed as list[Product] (the base class), so it can
    hold any current or future Product subclass without changes here."""

    def __init__(self, name: str = "Main"):
        self.__name: str = name
        self.__products: list[Product] = []

    def get_name(self) -> str:
        return self.__name

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            print(f"Product ID {product.get_product_id()} already exists "
                  f"in {self.__name}.")
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Drop the reference from this inventory and hand the Product back
        to the caller (so it can be moved elsewhere). Returns None if not
        found. The Product object is NOT destroyed."""
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def transfer_product(self, product_id: str, target: Inventory) -> bool:
        """Move the same Product object from this inventory to target."""
        product = self.find_product(product_id)
        if product is None or not target.add_product(product):
            return False
        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        """Return the exact Product with this ID, or None."""
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product
        return None

    def search_product(self, keyword: str) -> list[Product]:
        """Return products whose ID or name contains keyword."""
        keyword = keyword.lower()
        return [p for p in self.__products
                if keyword in p.get_product_id().lower()
                or keyword in p.get_name().lower()]

    def clear(self) -> None:
        """Empty the inventory. Only the references go; the Product
        objects still exist wherever else they are referenced."""
        self.__products.clear()

    def display_all_products(self) -> None:
        if not self.__products:
            print(f"Inventory '{self.__name}' is empty.")
            return
        # Polymorphism: no isinstance() checks. Each object runs its own
        # display_information() implementation.
        for product in self.__products:
            product.display_information()

    def get_products(self) -> list[Product]:
        """Return a copy of the list so outside code can't alter ours."""
        return list(self.__products)

    def __len__(self) -> int:
        return len(self.__products)
