def main():
    running_total = 0        # 1. Initialize inventory to zero

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