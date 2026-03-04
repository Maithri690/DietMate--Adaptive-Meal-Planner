from modules.utils import load_data

def generate_report():
    profile = load_data("data/profile.json")
    foods = load_data("data/food_db.json")
    meals = load_data("data/meals.json")
    shop = load_data("data/shopping_list.json")

    print("\n--- DietMate Summary Report ---")
    print(f"👤 Profile: {profile.get('name', 'N/A')} | Goal: {profile.get('goal', 'N/A')}")
    print(f"🍽 Foods in Database: {len(foods)}")
    print(f"🧠 Planned Meals: {len(meals)}")
    print(f"🛒 Shopping Items: {len(shop)}")
    print("✅ Data stored persistently in JSON files.")
