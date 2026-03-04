from modules.utils import load_data, save_data

MEAL_FILE = "data/meals.json"

def plan_meal():
    print("\n--- Meal Planner ---")
    meals = load_data(MEAL_FILE, [])
    food_name = input("Enter food item: ")
    quantity = input("Enter quantity: ")
    meals.append({"food": food_name, "quantity": quantity})
    save_data(MEAL_FILE, meals)
    print("✅ Meal planned successfully!")
