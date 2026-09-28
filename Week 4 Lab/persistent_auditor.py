inventory_file = "inventory.txt"

def load_inventory():
    """Reads existing orders from file. Returns an empty list if file doesn't exist."""
    orders = []
    try:
        with open(inventory_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                order_id, name, qty = line.split(",")
                orders.append({
                    "id": int(order_id),
                    "name": name,
                    "qty": int(qty)
                })
    except FileNotFoundError:
        pass
    return orders

def save_inventory(orders):
    """Writes all orders to file, one per line."""
    with open(inventory_file, "w") as f:
        for order in orders:
            f.write(f"{order['id']}, {order['name']}, {order['qty']}\n")

def get_product_name():
    name = input("Enter Product Name (or 'quit' to finish): ").strip()

    if name.lower() == "quit":
        return "quit"

    if not name:
        print("Error: Product name cannot be empty. Entry rejected.")
        return None

    if "," in name:
        print("Error: Product name cannot contain commas. Entry rejected.")
        return None

    return name

def get_quantity():
    entry = input("Enter Quantity: ").strip()

    try:
        quantity = int(entry)
    except ValueError:
        print(f"Error: '{entry}' is not a valid number. Entry rejected.")
        return None

    if quantity < 0:
        print(f"Error: {quantity} is negative. Entry rejected.")
        return None

    return quantity

def get_next_id(orders):
    if not orders:
        return 1001
    return max(order["id"] for order in orders) + 1

def display_orders(orders):
    print("Current Orders:\n")
    for order in orders:
        print(f"{order['id']}, {order['name']}, {order['qty']}")

def main():
    orders = load_inventory()
    failed_entries = 0

    display_orders(orders)

    while True:
        print()
        name = get_product_name()

        if name == "quit":
            break

        if name is None:
            failed_entries += 1
            continue

        quantity = get_quantity()
        if quantity is None:
            failed_entries += 1
            continue

        new_id = get_next_id(orders)
        orders.append({"id": new_id, "name": name, "qty": quantity})

        print(f"\nNew Order Added:\n{new_id}, {name}, {quantity}")

        save_inventory(orders)
        print(f"\nOrder successfully saved to {inventory_file}")
        print(f"\nNumber of Failed/Rejected Entries: {failed_entries}")

if __name__ == "__main__":
    main()