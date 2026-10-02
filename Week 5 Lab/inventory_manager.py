import json


def add_product():
    """
    Add New Product
    """
    print("Add New Product")
    product_id = input("Product ID: ")
    product_name = input("Product Name: ")
    product_price = float(input("Price: "))
    product_quantity = int(input("Stock Quantity: "))

    # Create a new product dictionary
    new_product = {
        "id": product_id,
        "name": product_name,
        "quantity": product_quantity,
        "price": product_price
    }

    # Append the new product to the inventory list
    inventory.append(new_product)
    print(f"Product '{product_name}' added successfully!")


def update_stock():
    """
    Update the stock quantity of an existing product.
    """
    print("Update Stock")
    product_id = input("Product ID: ")

    for product in inventory:
        if product["id"] == product_id:
            print("Product found:")
            print(f"Name: {product['name']}")
            print(f"Current Stock: {product['quantity']}")
            new_quantity = int(input(f"New Stock Quantity for '{product['name']}': "))
            product["quantity"] = new_quantity
            print(f"Stock for '{product['name']}' updated successfully!")
            return
    print(f"Product with ID '{product_id}' not found in inventory.")


def search_product():
    """
    Search for a product in the inventory by ID.
    """
    print("Search Product")
    product_id = input("Enter Product ID: ")
    for product in inventory:
        if product["id"] == product_id:
            print("Product found")
            print("-------------------")
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['quantity']}")
            print("-------------------")
            return
    print(f"Product with ID '{product_id}' not found in inventory.")


def display_all():
    """
    Display all products in the inventory.
    """
    if not inventory:
        print("Inventory is empty.")
        return

    print("Current Inventory:")
    print("-------------------")
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f} | Stock: {product['quantity']}")
    print("-------------------")

def load_inventory():
    """
    Load inventory from a JSON file.
    """
    try:
        with open("inventory.json", "r") as file:
            inventory.extend(json.load(file))
        print("\ninventory.json found.")
        print("Inventory loaded successfully.")
    except FileNotFoundError:
        print("inventory.json not found. Starting with an empty inventory.")

if __name__ == "__main__":
    inventory = []
    print("\n================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("================================")
    load_inventory()
    
    print("\n----------MENU----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Exit")
    print("------------------------")

    while True:
        choice = input("\nEnter your option (1-6): ")
        print()

        if choice == "1":
            display_all()
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_stock()
        elif choice == "4":
            search_product()
        elif choice == "5":
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")