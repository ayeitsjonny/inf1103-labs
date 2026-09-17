def main():
    running_total = 0        # 1. Initialize inventory to zero
    while True:
        value, status = get_valid_input()
        if status == "quit":
            break
        if status == "invalid":
            continue
        running_total = process_delivery(running_total, value)
        tax = calculate_tax(value)
        total_tax_collected += tax
        deliveries_processed += 1
    generate_report(deliveries_processed, failed_attempts)
    print(f"Total Units in Inventory: {running_total}")
    print(f"Total Tax Collected: {total_tax_collected:.2f}")

if __name__ == "__main__":
    main()

def get_valid_input():
    raw = input("Enter stock quantity (or 'quit' to finish): ").strip()

    if raw.lower() == "quit":
        return None, "quit"

    try:
        value = int(raw)
    except ValueError:
        print(f"  -> Invalid entry: '{raw}' is not a whole number. Try again.")
        return None, "invalid"

    if value < 0:
        print("  -> Invalid entry: quantity cannot be negative. Try again.")
        return None, "invalid"

    return value, "ok"  

    while True:  # 2. Continuous loop until 'quit'
        value, status = get_valid_input()

        if status == "quit":
            break

        if status == "invalid":
            failed_attempts += 1
            continue  

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

def generate_report(total_units, failed_attempts):
    print("\n----- FINAL REPORT -----")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print("-------------------------")