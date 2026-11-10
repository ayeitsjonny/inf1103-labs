from __future__ import annotations

import json
import os

from inventory import Inventory
from order import Order
from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from subscription_product import SubscriptionProduct

FILENAME = "inventory.json"

# Maps the "type" identifier saved in JSON to the class that rebuilds it.
PRODUCT_TYPES: dict[str, type[Product]] = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
    "subscription": SubscriptionProduct,
}


# ---------- File handling ----------
def load_data(inventory: Inventory, suppliers: dict[str, Supplier],
              filename: str = FILENAME) -> None:
    """Suppliers are loaded first (they exist independently), then each
    Product is rebuilt and linked to its Supplier by supplier_id."""
    if not os.path.exists(filename):
        print("No saved inventory found. Starting empty.")
        return
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        for item in data.get("suppliers", []):
            supplier = Supplier.from_dict(item)
            suppliers[supplier.get_supplier_id()] = supplier

        loaded = 0
        for item in data.get("products", []):
            product_class = PRODUCT_TYPES.get(item.get("type"))
            supplier = suppliers.get(item.get("supplier_id"))
            if product_class is None or supplier is None:
                print(f"Skipping {item.get('product_id')}: unknown type "
                      f"or supplier.")
                continue
            if inventory.add_product(product_class.from_dict(item, supplier)):
                loaded += 1
        print(f"Loaded {len(suppliers)} supplier(s) and {loaded} "
              f"product(s) from {filename}.")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError,
            AttributeError) as e:
        print(f"Could not read {filename}: {e}")


def save_data(inventory: Inventory, suppliers: dict[str, Supplier],
              filename: str = FILENAME) -> None:
    data = {
        "suppliers": [s.to_dict() for s in suppliers.values()],
        "products": [p.to_dict() for p in inventory.get_products()],
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {len(data['suppliers'])} supplier(s) and "
          f"{len(data['products'])} product(s) to {filename}.")


# ---------- Menu / input ----------
def show_menu() -> None:
    print("\n=== Inventory Management System ===")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Remove a product")
    print("4. Update stock")
    print("5. Search for a product")
    print("6. Suppliers (view / add)")
    print("7. Create an order")
    print("8. Save inventory")
    print("9. Exit")


def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    if not suppliers:
        print("No suppliers yet. Add one first (option 6).")
        return None
    for supplier in suppliers.values():
        supplier.display_information()
    supplier = suppliers.get(input("Supplier ID: ").strip().upper())
    if supplier is None:
        print("Supplier not found.")
    return supplier


def add_product_ui(inventory: Inventory,
                   suppliers: dict[str, Supplier]) -> None:
    print("Product type: 1. Physical  2. Digital  3. Subscription")
    type_choice = input("Choose type (1-3): ").strip()
    if type_choice not in ("1", "2", "3"):
        print("Invalid product type.")
        return

    product_id = input("Product ID: ").strip()
    name = input("Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock: "))
        if type_choice == "1":
            weight = float(input("Weight (kg): "))
        elif type_choice == "2":
            download_size = float(input("Download size (MB): "))
        else:
            billing_months = int(input("Billing period (months): "))
    except ValueError:
        print("Invalid number entered.")
        return
    if price < 0 or not product_id or not name:
        print("Invalid product details.")
        return

    # The Supplier already exists; we pass the object, not just its ID.
    supplier = choose_supplier(suppliers)
    if supplier is None:
        return

    try:
        if type_choice == "1":
            product: Product = PhysicalProduct(product_id, name, price, stock,
                                               supplier, weight)
        elif type_choice == "2":
            product = DigitalProduct(product_id, name, price, stock,
                                     supplier, download_size)
        else:
            product = SubscriptionProduct(product_id, name, price, stock,
                                          supplier, billing_months)
    except ValueError as e:
        print(f"Invalid product details: {e}")
        return
    if inventory.add_product(product):
        print("Product added.")


def remove_product_ui(inventory: Inventory) -> None:
    removed = inventory.remove_product(input("Product ID to remove: ").strip())
    if removed is None:
        print("Product not found.")
    else:
        print(f"Removed {removed.get_name()} from the inventory.")


def update_stock_ui(inventory: Inventory) -> None:
    product = inventory.find_product(input("Product ID to update: ").strip())
    if product is None:
        print("Product not found.")
        return
    try:
        quantity = int(input("New stock quantity: "))
    except ValueError:
        print("Invalid number entered.")
        return
    if product.update_stock(quantity):
        print("Stock updated.")


def search_product_ui(inventory: Inventory) -> None:
    results = inventory.search_product(input("Search (ID or name): ").strip())
    if not results:
        print("No matching products.")
    for product in results:
        product.display_information()


def suppliers_ui(suppliers: dict[str, Supplier]) -> None:
    if suppliers:
        for supplier in suppliers.values():
            supplier.display_information()
    else:
        print("No suppliers yet.")
    if input("Add a new supplier? (y/n): ").strip().lower() != "y":
        return
    supplier_id = input("Supplier ID: ").strip().upper()
    if supplier_id in suppliers:
        print("Supplier ID already exists.")
        return
    try:
        supplier = Supplier(supplier_id, input("Name: ").strip(),
                            input("Contact email: ").strip())
    except ValueError as e:
        print(f"Invalid supplier details: {e}")
        return
    suppliers[supplier_id] = supplier
    print("Supplier added.")


def create_order_ui(inventory: Inventory, next_number: int) -> None:
    order = Order(f"O{next_number:03d}")
    print(f"Creating order {order.get_order_id()} "
          f"(blank product ID to finish).")
    while True:
        product_id = input("Product ID: ").strip()
        if not product_id:
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        try:
            order.add_order_line(product, int(input("Quantity: ")))
        except ValueError as e:
            print(f"Invalid quantity: {e}")
    order.display_information()


# ---------- Main program ----------
def main() -> None:
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}
    load_data(inventory, suppliers)
    orders_created = 0

    while True:
        show_menu()
        choice = input("Choose an option (1-9): ").strip()
        if choice == "1":
            inventory.display_all_products()
        elif choice == "2":
            add_product_ui(inventory, suppliers)
        elif choice == "3":
            remove_product_ui(inventory)
        elif choice == "4":
            update_stock_ui(inventory)
        elif choice == "5":
            search_product_ui(inventory)
        elif choice == "6":
            suppliers_ui(suppliers)
        elif choice == "7":
            orders_created += 1
            create_order_ui(inventory, orders_created)
        elif choice == "8":
            save_data(inventory, suppliers)
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-9.")


if __name__ == "__main__":
    main()
