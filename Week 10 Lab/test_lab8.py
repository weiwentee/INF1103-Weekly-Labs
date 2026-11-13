"""
Tests for Lab 8: association, aggregation, composition, LSP and polymorphism.
Run with: python test_lab8.py
"""
from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


def make_supplier() -> Supplier:
    return Supplier("S001", "TechSupply Co", "sales@techsupply.com")


# ---------- Section 2: Association ----------

def test_association_supplier_and_product() -> None:
    supplier = make_supplier()
    guitar = PhysicalProduct("P100", "Guitar", 350.0, 5, supplier, 3.5)
    os_product = DigitalProduct("D100", "Operating System", 199.0, 100, supplier, 4500)

    guitar.get_supplier().display_information()
    os_product.get_supplier().display_information()

    assert guitar.get_supplier() is supplier
    assert os_product.get_supplier() is supplier
    assert guitar is not supplier

    del supplier  # Predict first: can the products still show their supplier?
    print("After del supplier:")
    guitar.get_supplier().display_information()
    os_product.get_supplier().display_information()
    assert guitar.get_supplier().get_name() == "TechSupply Co"


# ---------- Section 3: Aggregation ----------

def test_aggregation_inventory_and_product() -> None:
    product = PhysicalProduct("P200", "Keyboard", 80.0, 10, make_supplier(), 1.2)  # exists before any inventory
    inventory_a = Inventory("Inventory A")
    inventory_b = Inventory("Inventory B")

    assert inventory_a.add_product(product)
    inventory_a.display_all_products()

    removed = inventory_a.remove_product("P200")
    assert removed is product
    assert inventory_a.find_product("P200") is None

    # Predict first: does the product still work after removal?
    product.update_stock(15)
    product.display_information()
    assert product.get_stock() == 15

    assert inventory_b.add_product(product)
    assert inventory_b.find_product("P200") is product
    inventory_a.display_all_products()
    inventory_b.display_all_products()


# ---------- Section 4: Composition ----------

def test_composition_order_and_order_line() -> None:
    supplier = make_supplier()
    guitar = PhysicalProduct("P100", "Guitar", 350.0, 5, supplier, 3.5)
    os_product = DigitalProduct("D100", "Operating System", 199.0, 100, supplier, 4500)

    order_1 = Order("O001")
    order_1.add_order_line(guitar, 2)
    order_1.add_order_line(os_product, 1)
    order_1.display_order()
    assert order_1.calculate_total() == 899.0

    order_2 = Order("O002")
    order_2.add_order_line(guitar, 1)
    order_2.display_order()

    # Predict first: how many OrderLines and Products exist?
    line_1 = order_1.get_order_lines()[0]
    line_2 = order_2.get_order_lines()[0]
    print(f"OrderLine ids: {id(line_1)} vs {id(line_2)}")
    print(f"Product ids:   {id(line_1.get_product())} vs {id(line_2.get_product())}")
    assert line_1 is not line_2
    assert line_1.get_product() is line_2.get_product()

    assert order_1.remove_order_line("D100")
    order_1.display_order()
    assert order_1.calculate_total() == 700.0


# ---------- Section 6: LSP ----------

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def test_lsp_substitutability() -> None:
    supplier = make_supplier()
    products: list[Product] = [
        PhysicalProduct("P100", "Guitar", 350.0, 5, supplier, 3.5),
        DigitalProduct("D100", "Operating System", 199.0, 100, supplier, 4500),
    ]
    for product in products:
        show_product_details(product)
        product.update_stock(42)  # same expectation for both subclasses
        assert product.get_stock() == 42


# ---------- Section 7: Polymorphism ----------

def test_polymorphism_through_inventory() -> None:
    supplier = make_supplier()
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P100", "Guitar", 350.0, 5, supplier, 3.5))
    inventory.add_product(DigitalProduct("D100", "Operating System", 199.0, 100, supplier, 4500))

    # Predict first: what will each get_fulfilment_info() print?
    results: list[str] = []
    for product in inventory.get_all_products():  # one loop, no isinstance()
        product.display_information()
        info = product.get_fulfilment_info()
        print(info)
        results.append(info)

    assert "shipping" in results[0]
    assert "digitally" in results[1]


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
