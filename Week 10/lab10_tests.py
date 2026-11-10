"""Lab 8 (Week 10) tests: association, aggregation, composition, LSP and
polymorphism. Run with:  python lab10_tests.py
Each check uses assert, so the script stops loudly if a relationship breaks.
"""
from __future__ import annotations

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from subscription_product import SubscriptionProduct
from inventory import Inventory
from order import Order


def heading(title: str) -> None:
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")


# ---------------------------------------------------------------
def test_association() -> None:
    heading("2. ASSOCIATION: Supplier --- Product  [Predict first #1]")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    laptop = PhysicalProduct("P001", "Laptop", 1200.0, 15, supplier, 2.2)
    antivirus = DigitalProduct("P005", "Antivirus", 49.9, 100, supplier, 350)

    print("Supplier info read THROUGH each product:")
    laptop.get_supplier().display_information()
    antivirus.get_supplier().display_information()

    # Separate objects: a product is not a supplier, and both products
    # point at the SAME supplier object (one supplier, many products).
    assert laptop is not supplier and antivirus is not supplier
    assert laptop.get_supplier() is antivirus.get_supplier() is supplier
    print(f"id(supplier)                 = {id(supplier)}")
    print(f"id(laptop.get_supplier())    = {id(laptop.get_supplier())}")
    print(f"id(antivirus.get_supplier()) = {id(antivirus.get_supplier())}")

    print("\nRunning: del supplier")
    del supplier
    print("Products after deleting the 'supplier' variable:")
    laptop.display_information()
    antivirus.display_information()
    assert laptop.get_supplier().get_name() == "TechSource Pte Ltd"
    print("PASS: products still reach their supplier - 'del' only removed "
          "one name, not the object.")


# ---------------------------------------------------------------
def test_aggregation() -> None:
    heading("3. AGGREGATION: Inventory o-- Product  [Predict first #2]")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")

    # 1. Product exists BEFORE any inventory.
    mouse = PhysicalProduct("P002", "Mouse", 25.5, 40, supplier, 0.1)
    inventory_a = Inventory("Inventory A")
    inventory_b = Inventory("Inventory B")

    # 2. Add to A.
    inventory_a.add_product(mouse)
    assert inventory_a.find_product("P002") is mouse
    print(f"Added Mouse to {inventory_a.get_name()} "
          f"({len(inventory_a)} product)")

    # 3. Remove from A - product still usable.
    removed = inventory_a.remove_product("P002")
    assert removed is mouse
    assert inventory_a.find_product("P002") is None
    print(f"Removed from {inventory_a.get_name()} "
          f"({len(inventory_a)} products). Product still works:")
    mouse.update_stock(35)
    mouse.display_information()
    assert mouse.get_stock() == 35

    # 4. Add the SAME object to B.
    inventory_b.add_product(mouse)
    assert inventory_b.find_product("P002") is mouse
    print(f"Same object now in {inventory_b.get_name()}: "
          f"{inventory_b.find_product('P002') is mouse}")

    # 5. Transfer back, then empty the inventory entirely.
    assert inventory_b.transfer_product("P002", inventory_a)
    print(f"Transferred back to {inventory_a.get_name()}")
    inventory_a.clear()
    print(f"{inventory_a.get_name()} cleared ({len(inventory_a)} products). "
          f"Product still exists:")
    mouse.display_information()
    print("PASS: removing/emptying only drops references; "
          "the Product is never destroyed.")


# ---------------------------------------------------------------
def test_composition() -> None:
    heading("4. COMPOSITION: Order *-- OrderLine  "
            "[Predict first #3]")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    laptop = PhysicalProduct("P001", "Laptop", 1200.0, 15, supplier, 2.2)
    cable = PhysicalProduct("P003", "Cable", 10.0, 7, supplier, 0.2)
    editor = DigitalProduct("P008", "Photo Editor", 59.0, 30, supplier, 800)

    order_1 = Order("O001")
    order_1.add_order_line(laptop, 1)   # Order creates the OrderLine
    order_1.add_order_line(cable, 3)
    order_1.add_order_line(editor, 2)
    order_1.display_information()
    assert order_1.calculate_total() == 1200.0 + 30.0 + 118.0

    order_2 = Order("O002")
    order_2.add_order_line(laptop, 2)   # same Product, different Order
    order_2.display_information()

    line_1 = order_1.get_order_lines()[0]
    line_2 = order_2.get_order_lines()[0]
    print("\nSame Product (Laptop) in two Orders:")
    print(f"  line in O001 is line in O002?              {line_1 is line_2}")
    print(f"  id(line in O001) = {id(line_1)}")
    print(f"  id(line in O002) = {id(line_2)}")
    print(f"  both lines point to the same Laptop object? "
          f"{line_1.get_product() is line_2.get_product() is laptop}")
    print(f"  id(laptop) = {id(laptop)}")
    assert line_1 is not line_2
    assert line_1.get_product() is line_2.get_product() is laptop

    print("\nRemoving the Cable line from O001 via Order.remove_order_line():")
    assert order_1.remove_order_line("P003")
    order_1.display_information()
    print("Cable product still exists (only the LINE was removed):")
    cable.display_information()

    print("\nCancelling order O002 (deleting the Order):")
    del order_2
    print("O002's OrderLine went with it; the Laptop product is untouched:")
    laptop.display_information()
    print("PASS: each Order creates and owns its own lines; "
          "Products are only referenced.")


# ---------------------------------------------------------------
def show_product_details(product: Product) -> None:
    """Accepts ANY Product. No isinstance(), no subclass knowledge."""
    product.display_information()
    print(f"    -> {product.get_fulfilment_info()}")


def test_lsp() -> None:
    heading("6. LISKOV SUBSTITUTION")
    supplier = Supplier("S002", "SoftWorks Asia", "orders@softworks.asia")
    products: list[Product] = [
        PhysicalProduct("P004", "Monitor", 299.99, 7, supplier, 4.5),
        DigitalProduct("P005", "Antivirus", 49.9, 100, supplier, 350),
        SubscriptionProduct("P006", "Premium Support", 99.99, 50, supplier, 12),
    ]

    print("show_product_details() with each subclass, unchanged function:")
    for product in products:
        show_product_details(product)

    print("\nContract check - update_stock() must behave the same for all:")
    for product in products:
        assert product.update_stock(20) is True and product.get_stock() == 20
        assert product.update_stock(-5) is False and product.get_stock() == 20
        assert product.update_stock(0) is True and product.get_stock() == 0
        print(f"  {type(product).__name__:<20} valid -> True, "
              f"invalid -> False, stock unchanged on reject: OK")

    inventory = Inventory("LSP test")
    for product in products:
        assert inventory.add_product(product)
    assert inventory.find_product("P005") is products[1]
    assert inventory.remove_product("P006") is products[2]
    print("Inventory add/find/remove work for every subclass: OK")
    print("PASS: every subclass can stand in for Product.")


# ---------------------------------------------------------------
def test_polymorphism() -> None:
    heading("7. POLYMORPHISM through list[Product]  [Predict first #4]")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    inventory = Inventory("Mixed")
    inventory.add_product(
        PhysicalProduct("P007", "Keyboard", 79.9, 25, supplier, 0.8))
    inventory.add_product(
        DigitalProduct("P008", "Photo Editor", 59.0, 30, supplier, 800))

    # ONE loop, no isinstance(): Python picks each object's own method.
    for product in inventory.get_products():
        product.display_information()
        print(f"    -> {product.get_fulfilment_info()}")
    print("PASS: one loop, correct specialised behaviour for each object.")


if __name__ == "__main__":
    test_association()
    test_aggregation()
    test_composition()
    test_lsp()
    test_polymorphism()
    print("\nAll Lab 8 tests passed.")
