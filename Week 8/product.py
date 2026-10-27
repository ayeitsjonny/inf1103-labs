class Product:
    """Represents and manages a single product."""

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = 0
        self.update_stock(stock)  # reuse validation

    # ---- read-only access ----
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    # ---- behaviour ----
    def update_stock(self, quantity):
        """Set stock to quantity, rejecting invalid values."""
        if not isinstance(quantity, int) or quantity < 0:
            print("Invalid stock quantity. Must be a whole number >= 0.")
            return False
        self.__stock = quantity
        return True

    def display_information(self):
        print(f"ID: {self.__product_id:<6} | Name: {self.__name:<15} | "
              f"Price: ${self.__price:>9.2f} | Stock: {self.__stock}")

    def to_dict(self):
        """Used by the file handling code to save this product."""
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }
