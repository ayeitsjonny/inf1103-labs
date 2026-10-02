# inventory_manager.py
# Inventory Management System

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