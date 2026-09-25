def load_inventory(filename):
    """Reads previously saved inventory state.
    Returns (total, history) as (int, list).
    If the file doesn't exist, starts empty instead of crashing.
    """
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return 0, []
 
    total = 0
    history = []
 
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("TOTAL,"):
            total = int(line.split(",", 1)[1])
        else:
            history.append(int(line))
 
    return total, history

def save_inventory(filename, total, history):
    """Writes the final total and full transaction history to file."""
    with open(filename, "w") as f:
        f.write(f"TOTAL,{total}\n")
        for amount in history:
            f.write(f"{amount}\n")
 
 
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
 
 
def process_delivery(current_total, new_value):
    return current_total + new_value
 
 
def calculate_tax(amount):
    return amount * 0.10
 
 
def generate_report(total_units, failed_attempts):
    print("\n----- FINAL REPORT -----")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print("-------------------------")
 
 
def main():
    INVENTORY_FILE = "inventory.txt"
 
    # 1. Persistence: load whatever was saved last time (or start empty)
    running_total, history = load_inventory(INVENTORY_FILE)
 
    if history:
        print(f"Loaded existing inventory. Current total: {running_total}, "
              f"past transactions: {len(history)}")
    else:
        print("No existing inventory found. Starting fresh.")
 
    deliveries_processed = 0
    failed_attempts = 0
    total_tax_collected = 0.0
 
    while True:
        value, status = get_valid_input()
 
        if status == "quit":
            break
 
        if status == "invalid":
            failed_attempts += 1
            continue
 
        running_total = process_delivery(running_total, value)
        tax = calculate_tax(value)
        total_tax_collected += tax
        deliveries_processed += 1
 
        # 2. History Tracking: record every valid transaction amount
        history.append(value)
 
        print(f"  -> Delivery accepted: {value} units | Tax: {tax:.2f} | "
              f"Running Total: {running_total}")


    save_inventory(INVENTORY_FILE, running_total, history)
    print(f"\nInventory saved to {INVENTORY_FILE}")
 
    generate_report(deliveries_processed, failed_attempts)
    print(f"Total Units in Inventory: {running_total}")
    print(f"Total Tax Collected This Session: {total_tax_collected:.2f}")
 
 
if __name__ == "__main__":
    main()