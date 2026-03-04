import json
import os

# Load JSON data
def load_data(filepath, default_data=None):
    """
    Loads data from a JSON file.
    If the file does not exist, returns default_data (or empty dict if not provided).
    """
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return json.load(file)
    else:
        return default_data if default_data is not None else {}

# Save JSON data
def save_data(filepath, data):
    """
    Saves data to a JSON file.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)
