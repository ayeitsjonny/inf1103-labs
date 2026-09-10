total_inventory = 0 #1. Initialize inventory to zero
failed_entries = 0
git 
while True: #2. Loop until user types "quit"
    user_input = input("Enter stock quantity (or 'quit' to finish): ")
    
    if user_input == "quit":
        break

    if not user_input.isdigit(): #3 & 4. Accept integers, reject invalid strings
        print("Error: please enter a valid number.")
        failed_entries += 1
        continue

    quantity = int(user_input) #5. Reject negative numbers
    
    if quantity < 0:
        print("Error: negative values not allowed.")
        failed_entries += 1
        continue

    total_inventory += quantity #6. Keep a running total

    if total_inventory > 500: #7. Overstock alert
        print("ALERT: Overstock! Inventory exceeds 500 units.")
        break



