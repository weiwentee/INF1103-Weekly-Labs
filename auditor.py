def main():
    total_inventory = 0
    failed_entries = 0

    while True:
        entry = input("Enter stock quantity (or 'quit' to finish): ").strip()

        if entry.lower() == "quit":
            break

        # Reject non-numeric input (isdigit() only works on non-negative integers,
        # which is fine here since we reject negatives separately anyway)
        if not entry.isdigit():
            print(f"Error: '{entry}' is not a valid number. Entry rejected.")
            failed_entries += 1
            continue

        quantity = int(entry)

        if quantity < 0:
            print(f"Error: {quantity} is negative. Entry rejected.")
            failed_entries += 1
            continue

        total_inventory += quantity

        if total_inventory > 500:
            print(f"OVERSTOCK ALERT! Total inventory ({total_inventory}) exceeds 500 units. Halting entry.")
            break
        elif total_inventory == 500:
            print("Inventory exactly at capacity (500 units).")
        else:
            print(f"Accepted. Current total inventory: {total_inventory}")

    print("\n--- Audit Report ---")
    print(f"Total Units Processed: {total_inventory}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")


if __name__ == "__main__":
    main()