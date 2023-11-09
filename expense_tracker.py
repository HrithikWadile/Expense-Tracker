import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)
        
        # Color scheme
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2563eb"
        self.secondary_color = "#10b981"
        self.danger_color = "#ef4444"
        
        self.root.configure(bg=self.bg_color)
        
        # Data storage
        self.expenses = []
        self.categories = ["Food", "Transportation", "Entertainment", "Shopping", "Bills", "Health", "Other"]
        self.data_file = "expenses.json"
        
        # Load existing data
        self.load_data()
        
        # Create UI
        self.create_ui()
        
        # Bind resize event
        self.root.bind('<Configure>', self.on_resize)
        
    def create_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="💰 Expense Tracker", 
                              font=("Arial", 24, "bold"), 
                              bg=self.bg_color, fg=self.primary_color)
        title_label.pack(pady=(0, 10))
        
        # Summary Frame
        self.create_summary_frame(main_frame)
        
        # Input Frame
        self.create_input_frame(main_frame)
        
        # Expense List Frame
        self.create_list_frame(main_frame)
        
        # Update summary
        self.update_summary()
        
    def create_summary_frame(self, parent):
        summary_frame = tk.Frame(parent, bg=self.bg_color)
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Total Expenses Card
        total_card = tk.Frame(summary_frame, bg="white", relief=tk.RAISED, borderwidth=2)
        total_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(total_card, text="Total Expenses", font=("Arial", 12), 
                bg="white", fg="#666").pack(pady=(10, 0))
        self.total_label = tk.Label(total_card, text="₹0.00", 
                                    font=("Arial", 20, "bold"), 
                                    bg="white", fg=self.danger_color)
        self.total_label.pack(pady=(0, 10))
        
        # Count Card
        count_card = tk.Frame(summary_frame, bg="white", relief=tk.RAISED, borderwidth=2)
        count_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(count_card, text="Total Transactions", font=("Arial", 12), 
                bg="white", fg="#666").pack(pady=(10, 0))
        self.count_label = tk.Label(count_card, text="0", 
                                    font=("Arial", 20, "bold"), 
                                    bg="white", fg=self.primary_color)
        self.count_label.pack(pady=(0, 10))
        
    def create_input_frame(self, parent):
        input_frame = tk.LabelFrame(parent, text="Add New Expense", 
                                    font=("Arial", 12, "bold"),
                                    bg="white", fg=self.primary_color,
                                    relief=tk.RAISED, borderwidth=2)
        input_frame.pack(fill=tk.X, pady=(0, 10), padx=5, ipady=10)
        
        # Grid layout for inputs
        form_frame = tk.Frame(input_frame, bg="white")
        form_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Description
        tk.Label(form_frame, text="Description:", font=("Arial", 10), 
                bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.desc_entry = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.desc_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # Amount
        tk.Label(form_frame, text="Amount (₹):", font=("Arial", 10), 
                bg="white").grid(row=0, column=2, sticky="w", pady=5)
        self.amount_entry = tk.Entry(form_frame, font=("Arial", 10), width=15)
        self.amount_entry.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        
        # Category
        tk.Label(form_frame, text="Category:", font=("Arial", 10), 
                bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.category_var = tk.StringVar(value=self.categories[0])
        category_menu = ttk.Combobox(form_frame, textvariable=self.category_var, 
                                     values=self.categories, state="readonly", 
                                     font=("Arial", 10), width=28)
        category_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="e")
        
        add_btn = tk.Button(button_frame, text="Add Expense", 
                           command=self.add_expense,
                           bg=self.secondary_color, fg="white",
                           font=("Arial", 10, "bold"),
                           relief=tk.FLAT, cursor="hand2",
                           padx=15, pady=5)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="Clear All", 
                             command=self.clear_all,
                             bg=self.danger_color, fg="white",
                             font=("Arial", 10, "bold"),
                             relief=tk.FLAT, cursor="hand2",
                             padx=15, pady=5)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        form_frame.columnconfigure(1, weight=2)
        form_frame.columnconfigure(3, weight=1)
        
    def create_list_frame(self, parent):
        list_frame = tk.LabelFrame(parent, text="Expense History", 
                                   font=("Arial", 12, "bold"),
                                   bg="white", fg=self.primary_color,
                                   relief=tk.RAISED, borderwidth=2)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # Treeview with scrollbar
        tree_frame = tk.Frame(list_frame, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        columns = ("Date", "Description", "Category", "Amount")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Column headings
        self.tree.heading("Date", text="Date & Time")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        
        # Column widths
        self.tree.column("Date", width=150, minwidth=120)
        self.tree.column("Description", width=250, minwidth=150)
        self.tree.column("Category", width=120, minwidth=100)
        self.tree.column("Amount", width=100, minwidth=80)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Style for alternating row colors
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        
        # Delete button
        delete_btn = tk.Button(list_frame, text="Delete Selected", 
                              command=self.delete_expense,
                              bg=self.danger_color, fg="white",
                              font=("Arial", 10, "bold"),
                              relief=tk.FLAT, cursor="hand2",
                              padx=15, pady=5)
        delete_btn.pack(pady=(0, 10))
        
        # Load expenses into tree
        self.refresh_tree()
        
    def add_expense(self):
        desc = self.desc_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_var.get()
        
        if not desc:
            messagebox.showwarning("Warning", "Please enter a description!")
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid positive amount!")
            return
        
        expense = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": desc,
            "category": category,
            "amount": amount
        }
        
        self.expenses.append(expense)
        self.save_data()
        self.refresh_tree()
        self.update_summary()
        
        # Clear inputs
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", "Expense added successfully!")
        
    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?"):
            for item in selected:
                index = self.tree.index(item)
                del self.expenses[index]
            
            self.save_data()
            self.refresh_tree()
            self.update_summary()
            messagebox.showinfo("Success", "Expense deleted successfully!")
    
    def clear_all(self):
        if not self.expenses:
            messagebox.showinfo("Info", "No expenses to clear!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete ALL expenses?"):
            self.expenses = []
            self.save_data()
            self.refresh_tree()
            self.update_summary()
            messagebox.showinfo("Success", "All expenses cleared!")
    
    def refresh_tree(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add expenses
        for expense in reversed(self.expenses):
            self.tree.insert("", 0, values=(
                expense["date"],
                expense["description"],
                expense["category"],
                f"₹{expense['amount']:.2f}"
            ))
    
    def update_summary(self):
        total = sum(e["amount"] for e in self.expenses)
        count = len(self.expenses)
        
        self.total_label.config(text=f"₹{total:.2f}")
        self.count_label.config(text=str(count))
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.expenses, f, indent=2)
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.expenses = json.load(f)
            except:
                self.expenses = []
    
    def on_resize(self, event):
        # Handle responsive behavior if needed
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()