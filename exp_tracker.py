import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

# ===== File Setup =====
file_name = "expenses.json"
if not os.path.exists(file_name):
    with open(file_name, "w") as f:
        json.dump([], f)

# ===== Functions =====
def load_expenses():
    with open(file_name, "r") as f:
        return json.load(f)

def save_expenses(expenses):
    with open(file_name, "w") as f:
        json.dump(expenses, f, indent=4)

def add_expense():
    category = category_var.get()
    amount = amount_var.get()
    note = note_var.get()
    try:
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Invalid amount")
        return
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    expenses = load_expenses()
    expenses.append({"category": category, "amount": amount, "note": note, "date": date})
    save_expenses(expenses)
    refresh_tree()
    amount_var.set("")
    note_var.set("")

def delete_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Select an expense to delete")
        return
    expenses = load_expenses()
    for sel in selected:
        idx = int(tree.item(sel)["text"]) - 1
        expenses.pop(idx)
    save_expenses(expenses)
    refresh_tree()

def refresh_tree():
    for i in tree.get_children():
        tree.delete(i)
    expenses = load_expenses()
    for idx, e in enumerate(expenses, 1):
        tree.insert("", "end", text=str(idx),
                    values=(e['date'], e['category'], e['amount'], e['note']))
    update_total()

def update_total():
    expenses = load_expenses()
    total = sum(e['amount'] for e in expenses)
    total_label.config(text=f"Total Expenses: ${total:.2f}")

# ===== GUI =====
root = tk.Tk()
root.title("Expense Tracker Pro")
root.geometry("800x500")

# --- Input Frame ---
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Category").grid(row=0, column=0, padx=5)
category_var = tk.StringVar()
ttk.Combobox(frame, textvariable=category_var,
             values=["Food", "Transport", "Bills", "Shopping", "Other"]).grid(row=0, column=1, padx=5)
category_var.set("Food")

tk.Label(frame, text="Amount").grid(row=0, column=2, padx=5)
amount_var = tk.StringVar()
tk.Entry(frame, textvariable=amount_var).grid(row=0, column=3, padx=5)

tk.Label(frame, text="Note").grid(row=0, column=4, padx=5)
note_var = tk.StringVar()
tk.Entry(frame, textvariable=note_var).grid(row=0, column=5, padx=5)

tk.Button(frame, text="Add Expense", bg="#4CAF50", fg="white", command=add_expense).grid(row=0, column=6, padx=5)
tk.Button(frame, text="Delete Selected", bg="#f44336", fg="white", command=delete_expense).grid(row=1, column=6, pady=5)

# --- Treeview ---
cols = ("Date", "Category", "Amount", "Note")
tree = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True, pady=10)
refresh_tree()

# --- Total Display ---
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=5)
total_label = tk.Label(bottom_frame, text="Total Expenses: $0.00", font=("Arial", 14))
total_label.pack(side="left", padx=10)

root.mainloop()
