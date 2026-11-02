import json
import os

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from subscription_product import SubscriptionProduct

FILENAME = "inventory.json"

# Maps the "type" identifier saved in JSON to the class that rebuilds it.
PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
    "subscription": SubscriptionProduct,
}


# ---------- File handling ----------
def load_inventory(inventory, filename=FILENAME):
    if not os.path.exists(filename):
        print("No saved inventory found. Starting empty.")
        return
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        loaded = 0
        for item in data:
            product_class = PRODUCT_TYPES.get(item.get("type"))
            if product_class is None:
                print(f"Skipping {item.get('product_id')}: "
                      f"unknown product type {item.get('type')!r}.")
                continue
            if inventory.add_product(product_class.from_dict(item)):
                loaded += 1
        print(f"Loaded {loaded} product(s) from {filename}.")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(f"Could not read {filename}: {e}")


def save_inventory(inventory, filename=FILENAME):
    data = [p.to_dict() for p in inventory.get_products()]
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {len(data)} product(s) to {filename}.")


# ---------- Menu / input ----------
def show_menu():
    print("\n=== Inventory Management System ===")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Exit")


def add_product_ui(inventory):
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

    try:
        if type_choice == "1":
            product = PhysicalProduct(product_id, name, price, stock, weight)
        elif type_choice == "2":
            product = DigitalProduct(product_id, name, price, stock,
                                     download_size)
        else:
            product = SubscriptionProduct(product_id, name, price, stock,
                                          billing_months)
    except ValueError as e:
        print(f"Invalid product details: {e}")
        return
    if inventory.add_product(product):
        print("Product added.")


def update_stock_ui(inventory):
    product = inventory.find_by_id(input("Product ID to update: ").strip())
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


def search_product_ui(inventory):
    results = inventory.search_product(input("Search (ID or name): ").strip())
    if not results:
        print("No matching products.")
    for product in results:
        product.display_information()


# ---------- Main program ----------
def main():
    inventory = Inventory()
    load_inventory(inventory)

    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_ui(inventory)
        elif choice == "3":
            update_stock_ui(inventory)
        elif choice == "4":
            search_product_ui(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()