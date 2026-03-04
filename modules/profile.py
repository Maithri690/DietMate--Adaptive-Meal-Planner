from modules.utils import load_data, save_data

PROFILE_FILE = "data/profile.json"

def manage_profile():
    profile = load_data(PROFILE_FILE, {"name": "", "age": "", "height": "", "goal": ""})

    print("\n--- Profile Setup ---")
    name = input(f"Name [{profile['name']}]: ") or profile['name']
    age = input(f"Age [{profile['age']}]: ") or profile['age']
    height = input(f"Height (cm) [{profile['height']}]: ") or profile['height']
    goal = input(f"Goal (Weight Loss / Gain / Maintain) [{profile['goal']}]: ") or profile['goal']

    profile.update({"name": name, "age": age, "height": height, "goal": goal})
    save_data(PROFILE_FILE, profile)
    print("✅ Profile updated successfully!")

    print("\nCurrent Profile:")
    for key, value in profile.items():
        print(f"{key.capitalize()}: {value}")
