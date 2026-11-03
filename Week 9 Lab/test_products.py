"""
Tests for Lab 7 (Section 7: Testing and review).
Run with: python test_products.py
"""
import json
import os
import tempfile

import inventory_manager
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory


def test_physical_product_stores_and_displays_weight():
    guitar = PhysicalProduct("P100", "Guitar", 350.0, 5, 3.5)
    assert guitar.get_weight() == 3.5
    guitar.display_information()


def test_digital_product_stores_and_displays_download_size():
    os_product = DigitalProduct("D100", "Operating System", 199.0, 100, 4500)
    assert os_product.get_download_size() == 4500
    os_product.display_information()


def test_both_subclasses_implement_fulfilment_info():
    guitar = PhysicalProduct("P100", "Guitar", 350.0, 5, 3.5)
    os_product = DigitalProduct("D100", "Operating System", 199.0, 100, 4500)
    print(guitar.get_fulfilment_info())
    print(os_product.get_fulfilment_info())
    assert "shipping" in guitar.get_fulfilment_info()
    assert "digitally" in os_product.get_fulfilment_info()


def test_product_cannot_be_instantiated():
    try:
        Product("X001", "Generic", 10.0, 1)
    except TypeError as error:
        print(f"TypeError raised as expected: {error}")
        return
    raise AssertionError("Product should not be instantiable.")


def test_physical_products_calculate_shipping_by_weight():
    for weight in (0.5, 2.0, 10.0):
        product = PhysicalProduct("P200", "Box", 20.0, 1, weight)
        print(f"{weight} kg -> ${product.calculate_shipping_cost():.2f}")
    assert PhysicalProduct("P201", "Light", 1.0, 1, 1.0).calculate_shipping_cost() == 7.0
    assert PhysicalProduct("P202", "Heavy", 1.0, 1, 10.0).calculate_shipping_cost() == 25.0


def test_digital_products_are_not_shippable():
    os_product = DigitalProduct("D100", "Operating System", 199.0, 100, 4500)
    assert isinstance(PhysicalProduct("P100", "Guitar", 350.0, 5, 3.5), CanBeShipped)
    assert not isinstance(os_product, CanBeShipped)
    assert not hasattr(os_product, "calculate_shipping_cost")


def test_inventory_operations_still_work():
    inventory = Inventory()
    assert inventory.add_product(PhysicalProduct("P100", "Guitar", 350.0, 5, 3.5))
    assert inventory.add_product(DigitalProduct("D100", "Operating System", 199.0, 100, 4500))
    assert not inventory.add_product(DigitalProduct("D100", "Duplicate", 1.0, 1, 1))
    inventory.search_product("P100").update_stock(8)
    assert inventory.search_product("P100").get_stock() == 8
    assert inventory.search_product("ZZZ") is None
    inventory.display_all()


def test_json_save_and_load_preserves_types():
    original_filename = inventory_manager.FILENAME
    with tempfile.TemporaryDirectory() as folder:
        inventory_manager.FILENAME = os.path.join(folder, "test_inventory.json")
        try:
            inventory = Inventory()
            inventory.add_product(PhysicalProduct("P100", "Guitar", 350.0, 5, 3.5))
            inventory.add_product(DigitalProduct("D100", "Operating System", 199.0, 100, 4500))
            inventory_manager.save_inventory(inventory)

            with open(inventory_manager.FILENAME) as file:
                saved = json.load(file)
            assert saved[0]["type"] == "physical"
            assert saved[1]["type"] == "digital"

            reloaded = Inventory()
            inventory_manager.load_inventory(reloaded)
        finally:
            inventory_manager.FILENAME = original_filename

    guitar = reloaded.search_product("P100")
    os_product = reloaded.search_product("D100")
    assert isinstance(guitar, PhysicalProduct) and guitar.get_weight() == 3.5
    assert isinstance(os_product, DigitalProduct) and os_product.get_download_size() == 4500


if __name__ == "__main__":
    tests = [value for name, value in list(globals().items()) if name.startswith("test_")]
    passed = 0
    for test in tests:
        print(f"\n=== {test.__name__} ===")
        try:
            test()
            print("PASS")
            passed += 1
        except AssertionError as error:
            print(f"FAIL: {error}")
    print(f"\n{passed}/{len(tests)} tests passed.")
