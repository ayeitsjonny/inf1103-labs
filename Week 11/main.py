from __future__ import annotations

import csv
import json

from inventory import Inventory
from order import Order
from product import Product
from product_factory import ProductFactory
from supplier import Supplier
from discount import (DiscountStrategy, NoDiscount, PercentageDiscount,
                      BulkDiscount, StudentDiscount)

FILENAME = "inventory.json"
PRODUCTS_CSV = "products.csv"

# main.py no longer imports PhysicalProduct / DigitalProduct /
# SubscriptionProduct: every product is created by ProductFactory.

# Menu choice -> (label, strategy). The strategy objects are created once
# and SHARED by every order that picks them (association, not composition).
DISCOUNT_OPTIONS: dict[str, tuple[str, DiscountStrategy]] = {
    "1": ("No discount", NoDiscount()),
    "2": ("10% off", PercentageDiscount(10)),
    "3": ("$20 off orders of $200 or more", BulkDiscount(200, 20)),
    "4": ("Student discount (5% off)", StudentDiscount()),
}


# ---------- Input helpers (exception handling: keep asking) ----------
def get_positive_float(prompt: str) -> float:
    """Ask until the user enters a number greater than zero."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:                      # validation
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:                      # float() failed
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_float(prompt: str) -> float:
    """Ask until the user enters a number >= 0 (e.g. a weight)."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a number that is 0 or more.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 1.5")


def get_whole_number(prompt: str, minimum: int = 0) -> int:
    """Ask until the user enters a whole number >= minimum."""
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print(f"Please enter a whole number of at least {minimum}.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 5")


def get_non_empty(prompt: str) -> str:
    """Ask until the user types something."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


# ---------- File handling ----------
def load_data(inventory: Inventory, suppliers: dict[str, Supplier],
              filename: str = FILENAME) -> None:
    """Suppliers are loaded first (they exist independently), then each
    Product is rebuilt and linked to its Supplier by supplier_id."""
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No saved inventory found. Starting empty.")
        return
    except json.JSONDecodeError as e:
        print(f"Could not read {filename}: {e}")
        return

    try:
        for item in data.get("suppliers", []):
            supplier = Supplier.from_dict(item)
            suppliers[supplier.get_supplier_id()] = supplier

        loaded = 0
        for item in data.get("products", []):
            supplier = suppliers.get(item.get("supplier_id"))
            if supplier is None:
                print(f"Skipping {item.get('product_id')}: unknown supplier.")
                continue
            try:
                product = ProductFactory.create(
                    item.get("type", ""), item["product_id"], item["name"],
                    item["price"], item["stock"], supplier,
                    weight=item.get("weight", 0.0),
                    download_size=item.get("download_size", 0.0),
                    billing_months=item.get("billing_months", 1))
            except ValueError as e:
                # One bad product is reported and skipped; the rest load.
                print(f"Skipping {item.get('product_id')}: {e}")
                continue
            if inventory.add_product(product):
                loaded += 1
        print(f"Loaded {len(suppliers)} supplier(s) and {loaded} "
              f"product(s) from {filename}.")
    except KeyError as e:
        print(f"Could not read {filename}: missing field {e}")
    except ValueError as e:
        print(f"Could not read {filename}: invalid supplier ({e})")


def load_products(path: str, inventory: Inventory,
                  supplier: Supplier) -> None:
    """Load products from a CSV file through ProductFactory.
    - missing file  -> FileNotFoundError is caught, nothing crashes
    - bad row       -> ValueError is caught for THAT row only; it is
                       reported and skipped, and loading carries on
    - finally       -> always runs, whatever happened above"""
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)                       # skip the header row
            for line_number, row in enumerate(reader, start=2):
                if not row:                          # ignore blank lines
                    continue
                try:
                    if len(row) != 5:
                        raise ValueError(
                            f"expected 5 columns, got {len(row)}")
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(
                        product_type, product_id.strip(), name.strip(),
                        float(price), int(stock), supplier)
                except ValueError as e:
                    print(f"Skipping row {line_number} ({','.join(row)}): {e}")
                    continue
                if inventory.add_product(product):
                    loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


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
    print("8. Load products from CSV")
    print("9. Save inventory")
    print("10. Exit")


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
    # Check for a supplier first, so the user doesn't type everything in
    # and then find out they can't finish.
    supplier = choose_supplier(suppliers)
    if supplier is None:
        return

    type_names = {"1": "physical", "2": "digital", "3": "subscription"}
    print("Product type: 1. Physical  2. Digital  3. Subscription")
    while True:
        type_choice = input("Choose type (1-3): ").strip()
        if type_choice in type_names:
            break
        print("Please choose 1, 2 or 3.")
    product_type = type_names[type_choice]

    product_id = get_non_empty("Product ID: ")
    if inventory.find_product(product_id) is not None:
        print(f"Product ID {product_id} already exists.")
        return
    name = get_non_empty("Name: ")
    price = get_positive_float("Price: ")
    stock = get_whole_number("Stock: ", minimum=0)

    # Each type needs one extra detail. This only decides which question
    # to ASK - building the object is still the factory's job.
    extra: dict[str, float | int] = {}
    if product_type == "physical":
        extra["weight"] = get_non_negative_float("Weight (kg): ")
    elif product_type == "digital":
        extra["download_size"] = get_non_negative_float("Download size (MB): ")
    else:
        extra["billing_months"] = get_whole_number("Billing period (months): ",
                                                   minimum=1)

    try:
        product = ProductFactory.create(product_type, product_id, name, price,
                                        stock, supplier, **extra)
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
    quantity = get_whole_number("New stock quantity: ", minimum=0)
    try:
        product.update_stock(quantity)
    except ValueError as e:
        print(f"Stock not updated: {e}")
        return
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
        quantity = get_whole_number("Quantity: ", minimum=1)
        try:
            order.add_order_line(product, quantity)
        except ValueError as e:
            print(f"Invalid quantity: {e}")
    order.set_discount(choose_discount())
    order.display_information()


def choose_discount() -> DiscountStrategy:
    print("Discounts:")
    for key, (label, _) in DISCOUNT_OPTIONS.items():
        print(f"  {key}. {label}")
    while True:
        choice = input(f"Choose a discount (1-{len(DISCOUNT_OPTIONS)}): ").strip()
        if choice in DISCOUNT_OPTIONS:
            return DISCOUNT_OPTIONS[choice][1]
        print("Please choose one of the listed options.")


# ---------- Main program ----------
def main() -> None:
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}
    load_data(inventory, suppliers)
    orders_created = 0

    while True:
        show_menu()
        choice = input("Choose an option (1-10): ").strip()
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
            supplier = choose_supplier(suppliers)
            if supplier is not None:
                path = input(f"CSV file [{PRODUCTS_CSV}]: ").strip()
                load_products(path or PRODUCTS_CSV, inventory, supplier)
        elif choice == "9":
            save_data(inventory, suppliers)
        elif choice == "10":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-10.")


if __name__ == "__main__":
    main()
