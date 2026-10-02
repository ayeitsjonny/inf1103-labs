# inventory_manager.py
# Inventory Management System

from fileinput import filename
import json
import os

INVENTORY_FILE = "inventory.json"

DEFAULT_INVENTORY = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
]

if __name__ == "__main__":
    print(DEFAULT_INVENTORY)

def load_inventory(filename):
    """Loads inventory from a JSON file.
    If the file exists, loads and returns its contents.
    If it doesn't exist, starts with a default 3-product inventory
    and does not raise an error.
    """
    if os.path.exists(filename):
        print(f"{filename} found.")
        with open(filename, "r") as f:
            inventory = json.load(f)
        print("Inventory loaded successfully.")
        return inventory
    else:
        print(f"{filename} not found. Starting with a default inventory.")
        return [item.copy() for item in DEFAULT_INVENTORY]


if __name__ == "__main__":
    inventory = load_inventory(INVENTORY_FILE)
    print(inventory)