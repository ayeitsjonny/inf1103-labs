total_inventory = 0 #1. Initialize inventory to zero
failed_entries = 0
git 
while True: #2. Loop until user types "quit"
    user_input = input("Enter stock quantity (or 'quit' to finish): ")
    
    if user_input == "quit":
        break
