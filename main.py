import tkinter as tk
from tkinter import messagebox
from diet_mate_gui import create_profile_window
from modules.utils import load_data, save_data
import os


def main():
    root = tk.Tk()
    root.title("DietMate Launcher")
    root.geometry("300x150")

    tk.Label(root, text="DietMate", font=(None, 16)).pack(pady=8)
    # Profile button (opens profile window and enables features via callback)
    def open_profile_with_callback():
        create_profile_window(root, on_save=enable_features)

    profile_btn = tk.Button(root, text="Profile Setup", width=20, command=open_profile_with_callback)
    profile_btn.pack(pady=5)
    # feature buttons (start disabled until profile exists)
    food_btn = tk.Button(root, text="Food Database", width=20, command=lambda: open_food_db_window(root))
    meal_btn = tk.Button(root, text="Meal Planner", width=20, command=lambda: open_meal_planner_window(root))
    shop_btn = tk.Button(root, text="Shopping List", width=20, command=lambda: open_shopping_list_window(root))
    report_btn = tk.Button(root, text="Reports", width=20, command=lambda: open_reports_window(root))

    for b in (food_btn, meal_btn, shop_btn, report_btn):
        b.pack(pady=3)

    def enable_features(_profile=None):
        # called after profile is saved; enable feature buttons
        food_btn.config(state=tk.NORMAL)
        meal_btn.config(state=tk.NORMAL)
        shop_btn.config(state=tk.NORMAL)
        report_btn.config(state=tk.NORMAL)
        # show confirmation
        messagebox.showinfo("Profile", "Profile saved — features enabled.")
    # initially disable
    for b in (food_btn, meal_btn, shop_btn, report_btn):
        b.config(state=tk.DISABLED)

    root.mainloop()


def open_food_db_window(parent):
    win = tk.Toplevel(parent)
    win.title("Food Database")
    win.geometry("400x350")

    listbox = tk.Listbox(win, width=50)
    listbox.pack(pady=6)

    def refresh():
        listbox.delete(0, tk.END)
        foods = load_data("data/food_db.json", [])
        for f in foods:
            listbox.insert(tk.END, f"{f.get('name','')} ({f.get('calories','')} kcal)")

    frame = tk.Frame(win)
    frame.pack(pady=4)
    tk.Label(frame, text="Name").grid(row=0, column=0)
    name_e = tk.Entry(frame)
    name_e.grid(row=0, column=1)
    tk.Label(frame, text="Calories").grid(row=1, column=0)
    cal_e = tk.Entry(frame)
    cal_e.grid(row=1, column=1)

    def add_food():
        name = name_e.get().strip()
        cal = cal_e.get().strip()
        if not name:
            messagebox.showwarning("Input needed", "Please enter a food name.")
            return
        foods = load_data("data/food_db.json", [])
        foods.append({"name": name, "calories": cal})
        save_data("data/food_db.json", foods)
        name_e.delete(0, tk.END)
        cal_e.delete(0, tk.END)
        refresh()
    # editing support
    editing_index = {'idx': -1}

    def on_select_food(event=None):
        sel = listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        foods = load_data("data/food_db.json", [])
        if idx < 0 or idx >= len(foods):
            return
        f = foods[idx]
        name_e.delete(0, tk.END)
        name_e.insert(0, f.get('name',''))
        cal_e.delete(0, tk.END)
        cal_e.insert(0, f.get('calories',''))
        editing_index['idx'] = idx

    def update_food():
        idx = editing_index.get('idx', -1)
        if idx == -1:
            messagebox.showinfo("Nothing to update", "No food is selected for update. Use Add to create a new item.")
            return
        name = name_e.get().strip()
        cal = cal_e.get().strip()
        if not name:
            messagebox.showwarning("Input needed", "Please enter a food name.")
            return
        foods = load_data("data/food_db.json", [])
        if idx < 0 or idx >= len(foods):
            messagebox.showerror("Index error", "Selected food no longer exists.")
            editing_index['idx'] = -1
            return
        foods[idx] = {"name": name, "calories": cal}
        save_data("data/food_db.json", foods)
        editing_index['idx'] = -1
        name_e.delete(0, tk.END)
        cal_e.delete(0, tk.END)
        refresh()

    def delete_food():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Select item", "Please select a food to delete.")
            return
        idx = sel[0]
        foods = load_data("data/food_db.json", [])
        if idx < 0 or idx >= len(foods):
            return
        confirm = messagebox.askyesno("Confirm delete", f"Delete '{foods[idx].get('name','')}'?")
        if not confirm:
            return
        foods.pop(idx)
        save_data("data/food_db.json", foods)
        editing_index['idx'] = -1
        name_e.delete(0, tk.END)
        cal_e.delete(0, tk.END)
        refresh()

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=4)
    tk.Button(btn_frame, text="Add Food", command=add_food, bg="lightgreen").grid(row=0, column=0, padx=4)
    tk.Button(btn_frame, text="Update", command=update_food).grid(row=0, column=1, padx=4)
    tk.Button(btn_frame, text="Delete", command=delete_food, bg="#ff9999").grid(row=0, column=2, padx=4)
    listbox.bind('<<ListboxSelect>>', on_select_food)
    refresh()


def open_meal_planner_window(parent):
    win = tk.Toplevel(parent)
    win.title("Meal Planner")
    win.geometry("380x300")

    tk.Label(win, text="Food Item").pack()
    food_e = tk.Entry(win, width=30)
    food_e.pack()
    tk.Label(win, text="Quantity").pack()
    qty_e = tk.Entry(win, width=30)
    qty_e.pack()

    listbox = tk.Listbox(win, width=50)
    listbox.pack(pady=6)

    def refresh():
        listbox.delete(0, tk.END)
        meals = load_data("data/meals.json", [])
        for m in meals:
            listbox.insert(tk.END, f"{m.get('food','')} x {m.get('quantity','')}")

    def add_meal():
        food = food_e.get().strip()
        qty = qty_e.get().strip()
        if not food:
            messagebox.showwarning("Input needed", "Please enter a food item.")
            return
        meals = load_data("data/meals.json", [])
        meals.append({"food": food, "quantity": qty})
        save_data("data/meals.json", meals)
        food_e.delete(0, tk.END)
        qty_e.delete(0, tk.END)
        refresh()

    # editing support for meals
    editing_index = {'idx': -1}

    def on_select_meal(event=None):
        sel = listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        meals = load_data("data/meals.json", [])
        if idx < 0 or idx >= len(meals):
            return
        m = meals[idx]
        food_e.delete(0, tk.END)
        food_e.insert(0, m.get('food',''))
        qty_e.delete(0, tk.END)
        qty_e.insert(0, m.get('quantity',''))
        editing_index['idx'] = idx

    def update_meal():
        idx = editing_index.get('idx', -1)
        if idx == -1:
            messagebox.showinfo("Nothing to update", "No meal is selected for update. Use Add to create a new meal.")
            return
        food = food_e.get().strip()
        qty = qty_e.get().strip()
        if not food:
            messagebox.showwarning("Input needed", "Please enter a food item.")
            return
        meals = load_data("data/meals.json", [])
        if idx < 0 or idx >= len(meals):
            messagebox.showerror("Index error", "Selected meal no longer exists.")
            editing_index['idx'] = -1
            return
        meals[idx] = {"food": food, "quantity": qty}
        save_data("data/meals.json", meals)
        editing_index['idx'] = -1
        food_e.delete(0, tk.END)
        qty_e.delete(0, tk.END)
        refresh()

    def delete_meal():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Select item", "Please select a meal to delete.")
            return
        idx = sel[0]
        meals = load_data("data/meals.json", [])
        if idx < 0 or idx >= len(meals):
            return
        confirm = messagebox.askyesno("Confirm delete", f"Delete meal '{meals[idx].get('food','')}'?")
        if not confirm:
            return
        meals.pop(idx)
        save_data("data/meals.json", meals)
        editing_index['idx'] = -1
        food_e.delete(0, tk.END)
        qty_e.delete(0, tk.END)
        refresh()

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=4)
    tk.Button(btn_frame, text="Add Meal", command=add_meal, bg="lightgreen").grid(row=0, column=0, padx=4)
    tk.Button(btn_frame, text="Update", command=update_meal).grid(row=0, column=1, padx=4)
    tk.Button(btn_frame, text="Delete", command=delete_meal, bg="#ff9999").grid(row=0, column=2, padx=4)
    tk.Button(win, text="Refresh", command=refresh).pack()
    listbox.bind('<<ListboxSelect>>', on_select_meal)
    refresh()


def open_shopping_list_window(parent):
    win = tk.Toplevel(parent)
    win.title("Shopping List")
    win.geometry("380x320")

    tk.Label(win, text="Item").pack()
    item_e = tk.Entry(win, width=30)
    item_e.pack()
    tk.Label(win, text="Quantity").pack()
    qty_e = tk.Entry(win, width=30)
    qty_e.pack()

    listbox = tk.Listbox(win, width=50)
    listbox.pack(pady=6)

    def refresh():
        listbox.delete(0, tk.END)
        lst = load_data("data/shopping_list.json", [])
        for i in lst:
            listbox.insert(tk.END, f"{i.get('item','')} ({i.get('quantity','')})")

    # track currently edited index (-1 means adding new)
    editing_index = {'idx': -1}

    def add_item():
        item = item_e.get().strip()
        qty = qty_e.get().strip()
        if not item:
            messagebox.showwarning("Input needed", "Please enter an item name.")
            return
        lst = load_data("data/shopping_list.json", [])
        lst.append({"item": item, "quantity": qty})
        save_data("data/shopping_list.json", lst)
        item_e.delete(0, tk.END)
        qty_e.delete(0, tk.END)
        refresh()

    def on_select_item(event=None):
        sel = listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        lst = load_data("data/shopping_list.json", [])
        if idx < 0 or idx >= len(lst):
            return
        item = lst[idx]
        item_e.delete(0, tk.END)
        item_e.insert(0, item.get('item',''))
        qty_e.delete(0, tk.END)
        qty_e.insert(0, item.get('quantity',''))
        editing_index['idx'] = idx
    def update_item():
        idx = editing_index.get('idx', -1)
        if idx == -1:
            messagebox.showinfo("Nothing to update", "No item is selected for update. Use Add to create a new item.")
            return
        item = item_e.get().strip()
        qty = qty_e.get().strip()
        if not item:
            messagebox.showwarning("Input needed", "Please enter an item name.")
            return
        lst = load_data("data/shopping_list.json", [])
        if idx < 0 or idx >= len(lst):
            messagebox.showerror("Index error", "Selected item no longer exists.")
            editing_index['idx'] = -1
            return
        lst[idx] = {"item": item, "quantity": qty}
        save_data("data/shopping_list.json", lst)
        editing_index['idx'] = -1
        item_e.delete(0, tk.END)
        qty_e.delete(0, tk.END)
        refresh()

    def delete_item():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Select item", "Please select an item to delete.")
            return
        idx = sel[0]
        lst = load_data("data/shopping_list.json", [])
        if idx < 0 or idx >= len(lst):
            return
        confirm = messagebox.askyesno("Confirm delete", f"Delete '{lst[idx].get('item','')}'?")
        if not confirm:
            return
        lst.pop(idx)
        save_data("data/shopping_list.json", lst)
        editing_index['idx'] = -1
        item_e.delete(0, tk.END)
        qty_e.delete(0, tk.END)
        refresh()

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=4)
    tk.Button(btn_frame, text="Add Item", command=add_item, bg="lightgreen").grid(row=0, column=0, padx=4)
    tk.Button(btn_frame, text="Update", command=update_item).grid(row=0, column=1, padx=4)
    tk.Button(btn_frame, text="Delete", command=delete_item, bg="#ff9999").grid(row=0, column=2, padx=4)
    listbox.bind('<<ListboxSelect>>', on_select_item)
    refresh()


def open_reports_window(parent):
    win = tk.Toplevel(parent)
    win.title("Reports")
    win.geometry("400x300")

    profile = load_data("data/profile.json", {})
    foods = load_data("data/food_db.json", [])
    meals = load_data("data/meals.json", [])
    shop = load_data("data/shopping_list.json", [])

    text = tk.Text(win, wrap=tk.WORD, width=48, height=12)
    text.pack(padx=6, pady=6)
    text.insert(tk.END, "--- DietMate Summary Report ---\n")
    text.insert(tk.END, f"Profile: {profile.get('name','N/A')} | Goal: {profile.get('goal','N/A')}\n")
    text.insert(tk.END, f"Foods in Database: {len(foods)}\n")
    text.insert(tk.END, f"Planned Meals: {len(meals)}\n")
    text.insert(tk.END, f"Shopping Items: {len(shop)}\n")
    text.configure(state=tk.DISABLED)


if __name__ == "__main__":
    main()

