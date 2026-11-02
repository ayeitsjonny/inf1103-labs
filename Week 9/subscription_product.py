from product import Product


class SubscriptionProduct(Product):
    """A product billed repeatedly (e.g. a software subscription)."""

    def __init__(self, product_id, name, price, stock, billing_months):
        super().__init__(product_id, name, price, stock)
        if not isinstance(billing_months, int) or billing_months < 1:
            raise ValueError("Billing period must be a whole number of months >= 1.")
        self.__billing_months = billing_months

    def get_billing_months(self):
        return self.__billing_months

    def display_information(self):
        super().display_information()
        print(f"    Billed every {self.__billing_months} month(s)")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "subscription"
        data["billing_months"] = self.__billing_months
        return data

    def get_fulfilment_info(self):
        return "Subscription product: activated online and billed on a recurring cycle."

    @classmethod
    def from_dict(cls, data):
        return cls(data["product_id"], data["name"], data["price"],
                   data["stock"], data["billing_months"])