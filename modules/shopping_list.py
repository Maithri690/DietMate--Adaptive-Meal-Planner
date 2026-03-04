from modules.utils import load_data, save_data

SHOPPING_FILE = "data/shopping_list.json"

def manage_list():
    while True:
        print("\n--- Shopping List ---")
        print("1. Add Item")
        print("2. View List")
        print("3. Back")
        ch = input("Enter choice: ")

        if ch == '1':
            add_item()
        elif ch == '2':
            view_list()
        elif ch == '3':
            break
        else:
            print("Invalid choice!")

def add_item():
    item = input("Enter grocery item: ")
    qty = input("Enter quantity: ")
    lst = load_data(SHOPPING_FILE, [])
    lst.append({"item": item, "quantity": qty})
    save_data(SHOPPING_FILE, lst)
    print("✅ Item added to shopping list!")

def view_list():
    lst = load_data(SHOPPING_FILE, [])
    if not lst:
        print("No items found.")
        return
    print("\nShopping List:")
    for i in lst:
        print(f"- {i['item']} ({i['quantity']})")
