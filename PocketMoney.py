import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
from PIL import Image, ImageTk
from tkcalendar import Calendar

class PocketMoney:
    def _init_(self):
        self.budget = 0.0
        self.expenses = 0.0
        self.transactions = []

    def initialize(self, budget, month):
        self.budget = budget
        self.month = month
        self.load_transactions()  # Load previous transactions when initializing budget

    def spend(self, amount, description, date):
        if amount <= self.budget - self.expenses:
            self.expenses += amount
            self.transactions.append((date, description, amount))
            self.save_transactions()
            return True
        else:
            messagebox.showerror("Error", "Exceeds the budget! Cannot spend more.")
            return False

    def save_transactions(self):
        with open(f"{self.month}_transactions.txt", "w") as file:
            for transaction in self.transactions:
                file.write(",".join(map(str, transaction)) + "\n")

    def load_transactions(self):
        try:
            with open(f"{self.month}_transactions.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    self.transactions.append((parts[0], parts[1], float(parts[2])))
        except FileNotFoundError:
            pass

    def display_details(self):
        total_expenses = sum(transaction[2] for transaction in self.transactions)
        balance = self.budget - total_expenses
        message = f"Month: {self.month}\nBudget: {self.budget}\nExpenses: {total_expenses}\nBalance: {balance}"
        messagebox.showinfo("Pocket Manager Details", message)

    def show_transactions(self):
        message = f"Transactions History for {self.month}:\n"
        for transaction in self.transactions:
            date, description, amount = transaction
            message += f"Date: {date}, Description: {description}, Amount: {amount}\n"
        messagebox.showinfo("Transactions", message)

    def set_reminder(self):
        now = datetime.now()
        next_month = now.month + 1 if now.month < 12 else 1  # Increment month, reset to 1 in January
        next_year = now.year + 1 if now.month == 12 else now.year  # Increment year if December

        end_of_month = now.replace(day=1, month=next_month, year=next_year, hour=0, minute=0, second=0)
        reminder_message = f"Reminder: Reset the budget by the end of {self.month}!\n"
        reminder_message += f"The end of {self.month} is on: {end_of_month}"
        messagebox.showinfo("Reminder", reminder_message)

def initialize_budget():
    budget = float(budget_entry.get())
    month = month_var.get()
    pocket.initialize(budget, month)
    budget_entry.config(state=tk.DISABLED)
    month_menu.config(state=tk.DISABLED)
    initialize_button.config(state=tk.DISABLED)

def open_calendar():
    top = tk.Toplevel(root)
    cal = Calendar(top, selectmode="day", year=datetime.now().year, month=datetime.now().month)
    cal.pack()
    def select_date():
        spend_date_entry.delete(0, tk.END)
        spend_date_entry.insert(0, cal.get_date())
        top.destroy()
    select_button = tk.Button(top, text="Select Date", command=select_date, bg="grey", fg="white", font=("Helvetica", 12))  # Grey button color with white text
    select_button.pack()

def spend():
    amount = float(spend_amount_entry.get())
    desc = spend_description_entry.get()
    date = spend_date_entry.get()
    if pocket.spend(amount, desc, date):
        spend_amount_entry.delete(0, tk.END)
        spend_description_entry.delete(0, tk.END)
        spend_date_entry.delete(0, tk.END)

def display_details():
    pocket.display_details()

def show_transactions():
    pocket.show_transactions()

def set_reminder():
    pocket.set_reminder()

root = tk.Tk()
root.title("Pocket Money Manager")
root.configure(bg="#89C9B8")  # Set background color to a different shade of green

pocket = PocketMoney()

budget_label = tk.Label(root, text="ENTER BUDGET:", font=("Helvetica", 12,"bold","underline"), bg="#89C9B8")  # Changed font to Helvetica, set background color
budget_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # Adjusted padding and alignment

budget_entry = tk.Entry(root)
budget_entry.grid(row=0, column=1, padx=10, pady=10)  # Adjusted padding

month_label = tk.Label(root, text="SELECT MONTH:", font=("Helvetica", 12,"bold","underline"), bg="#89C9B8")  # Changed font to Helvetica, set background color
month_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")  # Adjusted padding and alignment

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
month_var = tk.StringVar(root)
month_var.set("January")  # Default to January
month_menu = tk.OptionMenu(root, month_var, *months)
month_menu.grid(row=1, column=1, padx=10, pady=10, sticky="ew")  # Adjusted padding and alignment

initialize_button = tk.Button(root, text="Initialize Budget", command=initialize_budget, bg="grey", fg="white", font=("Helvetica", 12,"bold"))  # Grey button color with white text
initialize_button.grid(row=2, column=0, columnspan=2, pady=10)  # Adjusted padding

spend_frame = tk.Frame(root, bg="#89C9B8")  # Set background color
spend_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)  # Adjusted padding

spend_label = tk.Label(spend_frame, text="MONEY SPENT", font=("Helvetica", 12,"bold","underline"), bg="#89C9B8")  # Changed font to Helvetica, set background color
spend_label.grid(row=0, column=0, pady=(10, 5), sticky="w")  # Increased padding and alignment

spend_amount_label = tk.Label(spend_frame, text="AMOUNT:", font=("Helvetica", 12,"bold"), bg="#89C9B8")  # Changed font to Helvetica, set background color
spend_amount_label.grid(row=1, column=0, sticky="w")

spend_amount_entry = tk.Entry(spend_frame)
spend_amount_entry.grid(row=1, column=1)

spend_description_label = tk.Label(spend_frame, text="DESCRIPTION:", font=("Helvetica", 12,"bold"), bg="#89C9B8")  # Changed font to Helvetica, set background color
spend_description_label.grid(row=2, column=0, sticky="w")

spend_description_entry = tk.Entry(spend_frame)
spend_description_entry.grid(row=2, column=1)

spend_date_label = tk.Label(spend_frame, text="DATE:", font=("Helvetica", 12,"bold"), bg="#89C9B8")  # Changed font to Helvetica, set background color
spend_date_label.grid(row=3, column=0, sticky="w")

spend_date_entry = tk.Entry(spend_frame)
spend_date_entry.grid(row=3, column=1)

calendar_button = tk.Button(spend_frame, text="Open Calendar", command=open_calendar, bg="grey", fg="white", font=("Helvetica", 12,"bold"))  # Grey button color with white text
calendar_button.grid(row=3, column=2, padx=5, sticky="ew")  # Placed beside date entry box

spend_button = tk.Button(spend_frame, text="Spend", command=spend, bg="grey", fg="white", font=("Helvetica", 12,"bold"))  # Grey button color with white text
spend_button.grid(row=4, column=0, columnspan=3, pady=(10, 5))  # Spanned multiple columns

display_button = tk.Button(root, text="Display Details", command=display_details, bg="grey", fg="white", font=("Helvetica", 12,"bold"))  # Grey button color with white text
display_button.grid(row=4, column=0, pady=(10, 5), sticky="ew")  # Adjusted padding and alignment

transactions_button = tk.Button(root, text="Show Transactions", command=show_transactions, bg="grey", fg="white", font=("Helvetica", 12,"bold"))  # Grey button color with white text
transactions_button.grid(row=4, column=1, pady=(10, 5), sticky="ew")  # Adjusted padding and alignment

reminder_button = tk.Button(root, text="Set Reminder", command=set_reminder, bg="grey", fg="white", font=("Helvetica", 12,"bold"))  # Grey button color with white text
reminder_button.grid(row=5, column=0, pady=10, sticky="ew")  # Adjusted padding and alignment

exit_button = tk.Button(root, text="Exit", command=root.quit, bg="grey", fg="white", font=("Helvetica", 12,"bold"))  # Grey button color with white text
exit_button.grid(row=5, column=1, pady=10, sticky="ew")  # Adjusted padding and alignment

# Load and display the image
image = Image.open("pocket_money_image.png")
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo, bg="#89C9B8")  # Set background color
image_label.grid(row=0, column=2, rowspan=7, padx=10, pady=10, sticky="nsew")  # Adjusted padding and alignment

root.mainloop()
