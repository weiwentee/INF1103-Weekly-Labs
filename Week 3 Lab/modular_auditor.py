def calculate_tax(amount):
    return amount * 0.10

def get_valid_input():
    entry = input("Enter stock quantity (or 'quit' to finish): ").strip()

    if entry.lower() == "quit":
        return "quit"

    if not entry.isdigit():
        print(f"Error: '{entry}' is not a valid number. Entry rejected.")
        return None

    quantity = int(entry)

    if quantity < 0:
        print(f"Error: {quantity} is negative. Entry rejected.")
        return None
    
    return quantity

def generate_report(total_units, failed_attempts):
    print("\n--- Audit Report ---")
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

def process_delivery(current_total, new_value):
    return current_total + new_value

def main():
    total_inventory = 0
    failed_entries = 0

    while True:
        quantity = get_valid_input()

        if quantity is None:
            failed_entries += 1
            continue

        if quantity == "quit":
            break

        total_inventory += process_delivery(total_inventory, quantity)
        tax = calculate_tax(quantity)

        print(f"Accepted. Current total inventory: {total_inventory}.")
        print(f"Tax for this entry: {tax:.2f}")

    generate_report(total_inventory, failed_entries)

if __name__ == "__main__":
    main()