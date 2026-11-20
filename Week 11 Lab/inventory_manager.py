import csv
import json

from supplier import Supplier
from product import Product
from product_factory import ProductFactory
from inventory import Inventory

FILENAME: str = "inventory.json"
PRODUCTS_CSV: str = "products.csv"
DEFAULT_SUPPLIER: dict[str, str] = {"supplier_id": "S000", "name": "Unknown Supplier", "contact_email": "-"}


# ---------- Input helpers (exception handling) ----------

def get_positive_float(prompt: str) -> float:
    """
    Keep asking until the user enters a number greater than zero.
    float() raises ValueError for text; the if check is our own validation.
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_float(prompt: str) -> float:
    """
    Keep asking until the user enters a number that is zero or more (weight, download size).
    """
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a number that is zero or more.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 1.5")


def get_non_negative_int(prompt: str) -> int:
    """
    Keep asking until the user enters a whole number that is zero or more (stock).
    """
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number that is zero or more.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 10")


# ---------- File handling ----------

def create_product_from_dict(item: dict, suppliers: dict[str, Supplier]) -> Product:
    """
    Use the saved type identifier and the ProductFactory to create the correct Product.
    Products with the same supplier ID share one Supplier object (association).
    """
    supplier_data = item.get("supplier", DEFAULT_SUPPLIER)
    supplier_id = supplier_data["supplier_id"]
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, supplier_data["name"], supplier_data["contact_email"])
    supplier = suppliers[supplier_id]

    extra = item.get("weight", item.get("download_size", 0.0))
    return ProductFactory.create(item["type"], item["id"], item["name"], item["price"],
                                 item["quantity"], supplier, extra)


def load_inventory(inventory: Inventory) -> None:
    """
    Load products from a JSON file into the inventory.
    """
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"{FILENAME} not found. Starting with an empty inventory.")
        return
    except json.JSONDecodeError:
        print(f"{FILENAME} is not valid JSON. Starting with an empty inventory.")
        return

    suppliers: dict[str, Supplier] = {}
    for item in data:
        try:
            inventory.add_product(create_product_from_dict(item, suppliers))
        except (ValueError, KeyError) as error:
            print(f"Skipping saved product {item}: {error}")
    print(f"\n{FILENAME} found.")
    print("Inventory loaded successfully.")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """
    Load products from a CSV file through the ProductFactory.
    One bad row is reported and skipped; the rest still load.
    """
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for row_number, row in enumerate(reader, start=2):
                try:
                    product_type, product_id, name, price, stock_quantity = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock_quantity), supplier)
                except ValueError as error:
                    print(f"Skipping row {row_number} {row}: {error}")
                    continue
                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Skipping row {row_number}: product ID '{product_id}' already exists.")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def save_inventory(inventory: Inventory) -> None:
    """
    Save inventory data to a JSON file.
    """
    print("Saving inventory...")
    data: list[dict[str, object]] = []
    for product in inventory.get_all_products():
        data.append(product.to_dict())
    try:
        with open(FILENAME, "w") as file:
            json.dump(data, file, indent=4)
    except OSError as error:
        print(f"Could not save inventory: {error}")
        return
    print(f"Inventory saved successfully to {FILENAME}.")


# ---------- Menu actions ----------

def add_product(inventory: Inventory) -> None:
    """
    Ask the user for product details and add it to the inventory.
    Invalid numbers are re-asked instead of cancelling the whole action.
    """
    print("Add New Product")
    product_types = {"1": "physical", "2": "digital"}
    choice = input("Product Type (1 = Physical, 2 = Digital): ")
    while choice not in product_types:
        print("Please enter 1 or 2.")
        choice = input("Product Type (1 = Physical, 2 = Digital): ")
    product_type = product_types[choice]

    product_id = input("Product ID: ")
    product_name = input("Product Name: ")
    product_price = get_positive_float("Price: ")
    product_quantity = get_non_negative_int("Stock Quantity: ")
    supplier = Supplier(input("Supplier ID: "), input("Supplier Name: "), input("Supplier Email: "))
    if product_type == "physical":
        extra = get_non_negative_float("Weight (kg): ")
    else:
        extra = get_non_negative_float("Download Size (MB): ")

    product = ProductFactory.create(product_type, product_id, product_name,
                                    product_price, product_quantity, supplier, extra)

    if inventory.add_product(product):
        print(f"Product '{product_name}' added successfully!")
        print(product.get_fulfilment_info())
    else:
        print(f"Product with ID '{product_id}' already exists.")


def update_stock(inventory: Inventory) -> None:
    """
    Update the stock quantity of an existing product.
    """
    print("Update Stock")
    product_id = input("Product ID: ")
    product = inventory.find_product(product_id)

    if product is None:
        print(f"Product with ID '{product_id}' not found in inventory.")
        return

    print("Product found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    new_quantity = get_non_negative_int(f"New Stock Quantity for '{product.get_name()}': ")
    product.update_stock(new_quantity)
    print(f"Stock for '{product.get_name()}' updated successfully!")


def search_product(inventory: Inventory) -> None:
    """
    Search for a product in the inventory by ID.
    """
    print("Search Product")
    product_id = input("Enter Product ID: ")
    product = inventory.find_product(product_id)

    if product is None:
        print(f"Product with ID '{product_id}' not found in inventory.")
        return

    print("Product found")
    print("-------------------")
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")
    print("-------------------")


def import_products_csv(inventory: Inventory) -> None:
    """
    Import products from a CSV file. All imported products share one supplier.
    """
    print("Import Products from CSV")
    path = input(f"CSV file path (Enter for '{PRODUCTS_CSV}'): ").strip() or PRODUCTS_CSV
    supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")
    load_products(path, inventory, supplier)


if __name__ == "__main__":
    inventory = Inventory()
    print("\n================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("================================")
    load_inventory(inventory)

    print("\n----------MENU----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Import Products from CSV")
    print("6. Save Inventory")
    print("7. Exit")
    print("------------------------")

    while True:
        choice = input("\nEnter your option (1-7): ")
        print()

        if choice == "1":
            inventory.display_all_products()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            import_products_csv(inventory)
        elif choice == "6":
            save_inventory(inventory)
        elif choice == "7":
            save_inventory(inventory)
            print("\nThank you for using the Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")
