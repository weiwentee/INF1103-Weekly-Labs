"""
Tests for Lab 9: Strategy, Factory, validation and exception handling.
Run from the project folder with: python tests/test_lab9.py   (or: python -m pytest tests)
"""
import io
import os
import sys
import tempfile
from contextlib import redirect_stdout
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import inventory_manager
from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from order_line import OrderLine
from product_factory import ProductFactory
from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)

CSV_PATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "products.csv")


def make_supplier() -> Supplier:
    return Supplier("S001", "TechSupply Co", "sales@techsupply.com")


def make_order_of_250(discount: DiscountStrategy | None = None) -> Order:
    """
    Lines add up to 250: 2 x 100 + 1 x 50.
    """
    supplier = make_supplier()
    order = Order("O250", discount)
    order.add_order_line(ProductFactory.create("physical", "P100", "Chair", 100.0, 10, supplier, 5.0), 2)
    order.add_order_line(ProductFactory.create("digital", "D100", "E-book", 50.0, 10, supplier, 20.0), 1)
    return order


def expect_value_error(action, expected_text: str) -> None:
    try:
        action()
    except ValueError as error:
        print(f"ValueError raised as expected: {error}")
        assert expected_text in str(error), f"'{expected_text}' not in '{error}'"
        return
    raise AssertionError("Expected a ValueError.")


# ---------- Section 2: Strategy ----------

def test_strategies_apply_correct_discount() -> None:
    assert NoDiscount().apply(250) == 250
    assert PercentageDiscount(10).apply(250) == 225
    assert BulkDiscount(200, 20).apply(250) == 230
    assert BulkDiscount(200, 20).apply(199.99) == 199.99   # below threshold: unchanged
    assert BulkDiscount(200, 20).apply(200) == 180         # "200 or more"
    assert StudentDiscount().apply(100) == 95


def test_order_defaults_to_no_discount() -> None:
    order = make_order_of_250()
    assert isinstance(order.get_discount(), NoDiscount)
    assert order.calculate_total() == 250


def test_order_uses_strategy_and_set_discount() -> None:
    # Predict first: 250 with BulkDiscount(200, 20), then PercentageDiscount(10)
    order = make_order_of_250(BulkDiscount(200, 20))
    print(f"Bulk total: {order.calculate_total()}")
    assert order.calculate_total() == 230

    order.set_discount(PercentageDiscount(10))
    print(f"Percentage total: {order.calculate_total()}")
    assert order.calculate_total() == 225
    order.display_order()


def test_new_strategy_without_changing_order() -> None:
    class BlackFridayDiscount(DiscountStrategy):   # defined here, Order is untouched
        def apply(self, total: float) -> float:
            return total / 2

    order = make_order_of_250(BlackFridayDiscount())
    assert order.calculate_total() == 125
    order.set_discount(StudentDiscount())
    assert order.calculate_total() == 237.5


def test_order_has_no_discount_if_elif() -> None:
    import inspect
    source = inspect.getsource(Order)
    for word in ("percentage", "bulk", "student", "discount_type"):
        assert word not in source.lower(), f"Order mentions '{word}'"


def test_two_orders_can_share_one_strategy() -> None:
    shared = PercentageDiscount(10)
    order_1 = make_order_of_250(shared)
    order_2 = make_order_of_250(shared)
    assert order_1.get_discount() is order_2.get_discount()
    assert order_1.calculate_total() == order_2.calculate_total() == 225


def test_invalid_strategy_values_rejected() -> None:
    expect_value_error(lambda: PercentageDiscount(150), "between 0 and 100")
    expect_value_error(lambda: BulkDiscount(200, -5), "cannot be negative")


def test_discount_strategy_is_abstract() -> None:
    try:
        DiscountStrategy()
    except TypeError:
        return
    raise AssertionError("DiscountStrategy should not be instantiable.")


# ---------- Section 3: Factory ----------

def test_factory_creates_correct_subclass() -> None:
    supplier = make_supplier()
    physical = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, supplier, 1.5)
    digital = ProductFactory.create("digital", "D1", "Editor", 49.9, 100, supplier, 300)
    assert isinstance(physical, PhysicalProduct) and physical.get_weight() == 1.5
    assert isinstance(digital, DigitalProduct) and digital.get_download_size() == 300
    assert isinstance(physical, Product) and isinstance(digital, Product)


def test_factory_unknown_type_raises_value_error() -> None:
    expect_value_error(
        lambda: ProductFactory.create("service", "S1", "Installation", 30.0, 5, make_supplier()),
        "Unknown product type: service")


def test_manager_creates_products_through_factory() -> None:
    import inspect
    source = inspect.getsource(inventory_manager)
    assert "PhysicalProduct(" not in source and "DigitalProduct(" not in source
    assert "ProductFactory.create(" in source


# ---------- Section 4: Validation ----------

def test_invalid_price_rejected() -> None:
    supplier = make_supplier()
    expect_value_error(lambda: ProductFactory.create("physical", "P1", "Lamp", 0, 1, supplier), "Price")
    expect_value_error(lambda: ProductFactory.create("digital", "D1", "App", -5, 1, supplier), "Price")


def test_negative_stock_rejected_for_every_subclass() -> None:
    supplier = make_supplier()
    for product_type in ("physical", "digital"):   # LSP: same rule for both
        expect_value_error(lambda: ProductFactory.create(product_type, "X1", "Item", 10, -1, supplier),
                           "Stock quantity cannot be negative")
        product = ProductFactory.create(product_type, "X1", "Item", 10, 5, supplier)
        expect_value_error(lambda: product.update_stock(-3), "Stock quantity cannot be negative")
        assert product.get_stock() == 5   # unchanged after a rejected update


def test_invalid_order_quantity_rejected() -> None:
    product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, make_supplier())
    expect_value_error(lambda: OrderLine(product, 0), "greater than zero")
    order = Order("O1")
    expect_value_error(lambda: order.add_order_line(product, -2), "greater than zero")
    assert order.get_order_lines() == []


# ---------- Section 5: Exception handling ----------

def test_get_positive_float_retries_until_valid() -> None:
    # Predict first: abc, then -5, then 12.50
    output = io.StringIO()
    with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), redirect_stdout(output):
        value = inventory_manager.get_positive_float("Price: ")
    printed = output.getvalue().splitlines()
    print("\n".join(printed))
    assert printed == ["Please enter a valid number, e.g. 12.50",
                       "Please enter a number greater than zero."]
    assert value == 12.5


def test_load_products_skips_bad_rows() -> None:
    inventory = Inventory()
    output = io.StringIO()
    with redirect_stdout(output):
        inventory_manager.load_products(CSV_PATH, inventory, make_supplier())
    printed = output.getvalue().splitlines()
    print("\n".join(printed))

    ids = [product.get_product_id() for product in inventory.get_all_products()]
    assert ids == ["P001", "D001", "P003"]
    assert "Unknown product type: service" in printed[0]
    assert "could not convert string to float: 'abc'" in printed[1]
    assert printed[2] == "3 products loaded."
    assert printed[3] == "Load attempt finished."


def test_load_products_missing_file_does_not_crash() -> None:
    inventory = Inventory()
    with tempfile.TemporaryDirectory() as folder:
        missing = os.path.join(folder, "missing.csv")
        output = io.StringIO()
        with redirect_stdout(output):
            inventory_manager.load_products(missing, inventory, make_supplier())
    printed = output.getvalue().splitlines()
    print("\n".join(printed))
    assert printed == [f"Products file not found: {missing}", "Load attempt finished."]
    assert inventory.get_all_products() == []


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
    sys.exit(0 if passed == len(tests) else 1)
