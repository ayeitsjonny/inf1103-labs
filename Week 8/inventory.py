class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.find_by_id(product.get_product_id()) is not None:
            print(f"Product ID {product.get_product_id()} already exists.")
            return False
        self.__products.append(product)
        return True

    def find_by_id(self, product_id):
        """Return the exact Product with this ID, or None."""
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product
        return None

    def search_product(self, keyword):
        """Return a list of products whose ID or name contains keyword."""
        keyword = keyword.lower()
        return [p for p in self.__products
                if keyword in p.get_product_id().lower()
                or keyword in p.get_name().lower()]

    def display_all(self):
        if not self.__products:
            print("Inventory is empty.")
            return
        for product in self.__products:
            product.display_information()

    def get_products(self):
        """Return a copy of the list so outside code can't alter ours."""
        return list(self.__products)
