from product import Product


class DigitalProduct(Product):
    """A product delivered by download. Not shippable, so it does NOT
    implement CanBeShipped."""

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        if not isinstance(download_size, (int, float)) or download_size < 0:
            raise ValueError("Download size must be a number >= 0 (MB).")
        self.__download_size = float(download_size)

    def get_download_size(self):
        return self.__download_size

    # ---- overrides ----
    def display_information(self):
        super().display_information()
        print(f"    Download size: {self.__download_size:.2f} MB")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    # ---- Product's abstract method ----
    def get_fulfilment_info(self):
        return "Digital product: delivered via download link, no shipping."

    @classmethod
    def from_dict(cls, data):
        return cls(data["product_id"], data["name"], data["price"],
                   data["stock"], data["download_size"])