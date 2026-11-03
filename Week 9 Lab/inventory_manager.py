import json

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

FILENAME = "inventory.json"


# ---------- File handling ----------

def create_product_from_dict(item):
    """
    Use the saved type identifier to create the correct Product subclass.
    """
    if item["type"] == "physical":
        return PhysicalProduct(item["id"], item["name"], item["price"], item["quantity"], item["weight"])
    elif item["type"] == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"], item["quantity"], item["download_size"])
    raise ValueError(f"Unknown product type '{item['type']}'.")


def load_inventory(inventory):
    """
    Load products from a JSON file into the inventory.
    """
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
        for item in data:
            inventory.add_product(create_product_from_dict(item))
        print(f"\n{FILENAME} found.")
        print("Inventory loaded successfully.")
    except FileNotFoundError:
        print(f"{FILENAME} not found. Starting with an empty inventory.")


def save_inventory(inventory):
    """
    Save inventory data to a JSON file.
    """
    print("Saving inventory...")
    data = []
    for product in inventory.get_all_products():
        data.append(product.to_dict())
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Inventory saved successfully to {FILENAME}.")


# ---------- Menu actions ----------

def add_product(inventory):
    """
    Ask the user for product details and add it to the inventory.
    """
    print("Add New Product")
    product_type = input("Product Type (1 = Physical, 2 = Digital): ")
    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Product ID: ")
    product_name = input("Product Name: ")
    try:
        product_price = float(input("Price: "))
        product_quantity = int(input("Stock Quantity: "))
        if product_type == "1":
            weight = float(input("Weight (kg): "))
            product = PhysicalProduct(product_id, product_name, product_price, product_quantity, weight)
        else:
            download_size = float(input("Download Size (MB): "))
            product = DigitalProduct(product_id, product_name, product_price, product_quantity, download_size)
    except ValueError as error:
        print(f"Invalid input: {error}")
        return

    if inventory.add_product(product):
        print(f"Product '{product_name}' added successfully!")
        print(product.get_fulfilment_info())
    else:
        print(f"Product with ID '{product_id}' already exists.")


def update_stock(inventory):
    """
    Update the stock quantity of an existing product.
    """
    print("Update Stock")
    product_id = input("Product ID: ")
    product = inventory.search_product(product_id)

    if product is None:
        print(f"Product with ID '{product_id}' not found in inventory.")
        return

    print("Product found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    try:
        new_quantity = int(input(f"New Stock Quantity for '{product.get_name()}': "))
        product.update_stock(new_quantity)
        print(f"Stock for '{product.get_name()}' updated successfully!")
    except ValueError as error:
        print(f"Invalid input: {error}")


def search_product(inventory):
    """
    Search for a product in the inventory by ID.
    """
    print("Search Product")
    product_id = input("Enter Product ID: ")
    product = inventory.search_product(product_id)

    if product is None:
        print(f"Product with ID '{product_id}' not found in inventory.")
        return

    print("Product found")
    print("-------------------")
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")
    print("-------------------")


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
    print("5. Save Inventory")
    print("6. Exit")
    print("------------------------")

    while True:
        choice = input("\nEnter your option (1-6): ")
        print()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            save_inventory(inventory)
            print("\nThank you for using the Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")
