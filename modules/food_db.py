from modules.utils import load_data, save_data

FOOD_FILE = "data/food_db.json"

def manage_food_db():
    # CLI menu kept for backward compatibility; storage is JSON file
    while True:
        print("\n--- Food Database ---")
        print("1. Add Food Item")
        print("2. View Food Items")
        print("3. Back")
        ch = input("Enter choice: ")

        if ch == '1':
            add_food()
        elif ch == '2':
            view_foods()
        elif ch == '3':
            break
        else:
            print("Invalid choice!")

def add_food():
    name = input("Food name: ")
    calories = input("Calories: ")
    food_list = load_data(FOOD_FILE, [])
    food_list.append({"name": name, "calories": calories})
    save_data(FOOD_FILE, food_list)
    print(f"✅ {name} added successfully!")

def view_foods():
    food_list = load_data(FOOD_FILE, [])
    if not food_list:
        print("No food items found.")
        return
    print("\nAvailable Foods:")
    for f in food_list:
        print(f"- {f['name']} ({f['calories']} kcal)")
