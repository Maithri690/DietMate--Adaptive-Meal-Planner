from modules import profile, food_db, meal_planner, shopping_list, reports

def show_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Profile Setup")
        print("2. Food Database")
        print("3. Meal Planner")
        print("4. Shopping List")
        print("5. Reports")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            profile.manage_profile()
        elif choice == '2':
            food_db.manage_food_db()
        elif choice == '3':
            meal_planner.plan_meal()
        elif choice == '4':
            shopping_list.manage_list()
        elif choice == '5':
            reports.generate_report()
        elif choice == '6':
            print("Thank you for using DietMate! Stay healthy 🥗")
            break
        else:
            print("Invalid choice! Try again.")
