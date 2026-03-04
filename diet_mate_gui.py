import tkinter as tk
from tkinter import messagebox
import json
import os

PROFILE_FILE = "data/profile.json"


# ---------- Utility functions ----------
def load_data(file_path, default_data):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    else:
        return default_data


def save_data(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


# ---------- GUI (exported) ----------
def create_profile_window(parent=None, on_save=None):
    """Create and return a profile window.

    If parent is None, this will create a standalone Tk root and call mainloop()
    before returning. If parent is provided, a Toplevel will be created and
    returned (no mainloop call).
    """

    def save_profile():
        profile = {
            "name": name_var.get(),
            "age": age_var.get(),
            "height": height_var.get(),
            "goal": goal_var.get()
        }
        save_data(PROFILE_FILE, profile)
        messagebox.showinfo("Success", "Profile saved successfully!")
        # call callback if provided (used to enable other UI features)
        if callable(on_save):
            try:
                on_save(profile)
            except Exception:
                pass
        # if this window was opened as a Toplevel (parent provided), close it after save
        try:
            if not is_standalone:
                win.destroy()
        except Exception:
            pass

    def load_profile():
        profile = load_data(PROFILE_FILE, {"name": "", "age": "", "height": "", "goal": ""})
        name_var.set(profile.get("name", ""))
        age_var.set(profile.get("age", ""))
        height_var.set(profile.get("height", ""))
        goal_var.set(profile.get("goal", ""))
        messagebox.showinfo("Loaded", "Profile loaded successfully!")

    # create either a new root or a Toplevel
    is_standalone = parent is None
    if is_standalone:
        win = tk.Tk()
    else:
        win = tk.Toplevel(parent)

    win.title("Diet Mate - Profile Setup")
    win.geometry("400x300")
    win.resizable(False, False)

    # Variables bound to this window
    name_var = tk.StringVar(win)
    age_var = tk.StringVar(win)
    height_var = tk.StringVar(win)
    goal_var = tk.StringVar(win)

    # Layout
    tk.Label(win, text="Name:").pack(pady=5)
    tk.Entry(win, textvariable=name_var).pack()

    tk.Label(win, text="Age:").pack(pady=5)
    tk.Entry(win, textvariable=age_var).pack()

    tk.Label(win, text="Height (cm):").pack(pady=5)
    tk.Entry(win, textvariable=height_var).pack()

    tk.Label(win, text="Goal:").pack(pady=5)
    tk.Entry(win, textvariable=goal_var).pack()

    # Buttons
    tk.Button(win, text="Save Profile", command=save_profile, bg="lightgreen").pack(pady=10)
    tk.Button(win, text="Load Profile", command=load_profile, bg="lightblue").pack()

    # If standalone, start the mainloop and block until closed
    if is_standalone:
        win.mainloop()

    return win


if __name__ == "__main__":
    # allow running this file directly for quick testing
    create_profile_window()
