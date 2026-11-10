from __future__ import annotations


class Supplier:
    """A company that supplies products.

    Association with Product: a Supplier is NOT part of a Product, and a
    Product is NOT part of a Supplier. Both are created independently and
    can exist on their own. Product holds a reference to its Supplier
    (navigable Product -> Supplier). Supplier deliberately does NOT keep a
    list of its products: nothing in the system needs that direction yet,
    so leaving it out keeps the two classes loosely coupled.
    """

    def __init__(self, supplier_id: str, name: str, contact_email: str):
        if not supplier_id or not name:
            raise ValueError("Supplier ID and name are required.")
        if "@" not in contact_email:
            raise ValueError("Contact email must contain '@'.")
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    # ---- read-only access ----
    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    # ---- behaviour ----
    def display_information(self) -> None:
        print(f"Supplier {self.__supplier_id}: {self.__name} "
              f"<{self.__contact_email}>")

    def to_dict(self) -> dict:
        return {
            "supplier_id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Supplier:
        return cls(data["supplier_id"], data["name"], data["contact_email"])
