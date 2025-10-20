from tkinter import *
from tkinter import ttk, messagebox
from payroll import PayrollSystem

class PayrollGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Payroll Accounting System")
        self.master.geometry("900x650")
        self.master.configure(bg="#e0e5ec")  # soft background
        self.payroll_system = PayrollSystem()

        self.create_widgets()

    def create_widgets(self):
        # Header
        header = Label(self.master, text="💼 Payroll Accounting System", font=("Segoe UI", 26, "bold"),
                       bg="#4a90e2", fg="white", pady=20)
        header.pack(fill=X)

        # Main frame
        main_frame = Frame(self.master, bg="#e0e5ec")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Left frame for form
        form_frame = Frame(main_frame, bg="white", bd=0, relief=RIDGE)
        form_frame.place(relx=0, rely=0, relwidth=0.45, relheight=1)

        # Form Title
        Label(form_frame, text="Add / Update Employee", font=("Segoe UI", 18, "bold"),
              bg="white", fg="#4a90e2").pack(pady=15)

        # Input fields with labels
        fields = ["Employee ID", "Employee Name", "Basic Salary", "HRA", "Allowance", "PF Deduction", "Tax Deduction"]
        self.entries = {}

        for i, field in enumerate(fields):
            lbl = Label(form_frame, text=field + ":", font=("Segoe UI", 12), bg="white", anchor=W)
            lbl.pack(fill=X, padx=20, pady=(10 if i==0 else 5,0))
            entry = Entry(form_frame, font=("Segoe UI", 12), bd=2, relief=SOLID)
            entry.pack(fill=X, padx=20, pady=5)
            self.entries[field] = entry

        # Buttons
        button_frame = Frame(form_frame, bg="white")
        button_frame.pack(pady=20)

        btn_style = {"font": ("Segoe UI", 12, "bold"), "bd":0, "fg":"white", "width":15, "cursor":"hand2"}

        self.add_button = Button(button_frame, text="Add Employee", bg="#4CAF50", **btn_style,
                                 command=self.add_employee)
        self.add_button.grid(row=0, column=0, padx=5, pady=5)
        self.add_button.bind("<Enter>", lambda e: self.add_button.config(bg="#45a049"))
        self.add_button.bind("<Leave>", lambda e: self.add_button.config(bg="#4CAF50"))

        self.show_button = Button(button_frame, text="Show Payslip", bg="#2196F3", **btn_style,
                                  command=self.show_payslip)
        self.show_button.grid(row=0, column=1, padx=5, pady=5)
        self.show_button.bind("<Enter>", lambda e: self.show_button.config(bg="#1e88e5"))
        self.show_button.bind("<Leave>", lambda e: self.show_button.config(bg="#2196F3"))

        self.clear_button = Button(button_frame, text="Clear Form", bg="#FF5722", **btn_style,
                                   command=self.clear_entries)
        self.clear_button.grid(row=1, column=0, padx=5, pady=5)
        self.clear_button.bind("<Enter>", lambda e: self.clear_button.config(bg="#e64a19"))
        self.clear_button.bind("<Leave>", lambda e: self.clear_button.config(bg="#FF5722"))

        self.list_button = Button(button_frame, text="Refresh List", bg="#FF9800", **btn_style,
                                  command=self.update_employee_list)
        self.list_button.grid(row=1, column=1, padx=5, pady=5)
        self.list_button.bind("<Enter>", lambda e: self.list_button.config(bg="#fb8c00"))
        self.list_button.bind("<Leave>", lambda e: self.list_button.config(bg="#FF9800"))

        # Right frame for employee list & payslip
        right_frame = Frame(main_frame, bg="white", bd=0, relief=RIDGE)
        right_frame.place(relx=0.46, rely=0, relwidth=0.54, relheight=1)

        # Search
        search_frame = Frame(right_frame, bg="white")
        search_frame.pack(fill=X, pady=10, padx=10)

        Label(search_frame, text="Search Employee:", bg="white", font=("Segoe UI",12)).pack(side=LEFT, padx=5)
        self.search_entry = Entry(search_frame, font=("Segoe UI",12))
        self.search_entry.pack(side=LEFT, fill=X, expand=True, padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_employee())

        # Employee List
        self.employee_listbox = Listbox(right_frame, font=("Segoe UI", 12))
        self.employee_listbox.pack(fill=BOTH, expand=True, padx=10, pady=10, side=LEFT)
        self.employee_listbox.bind("<<ListboxSelect>>", self.display_payslip)

        scrollbar = Scrollbar(right_frame, orient=VERTICAL)
        scrollbar.config(command=self.employee_listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.employee_listbox.config(yscrollcommand=scrollbar.set)

        # Payslip display
        self.payslip_text = Text(right_frame, height=10, font=("Courier", 11), bg="#f0f4f8")
        self.payslip_text.pack(fill=X, padx=10, pady=(0,10))

    # Employee functions
    def add_employee(self):
        try:
            emp_id = self.entries["Employee ID"].get()
            name = self.entries["Employee Name"].get()
            basic = float(self.entries["Basic Salary"].get())
            hra = float(self.entries["HRA"].get())
            allowance = float(self.entries["Allowance"].get())
            pf = float(self.entries["PF Deduction"].get())
            tax = float(self.entries["Tax Deduction"].get())
            self.payroll_system.add_employee(emp_id, name, basic, hra, allowance, pf, tax)
            messagebox.showinfo("Success", f"Employee {name} added successfully!")
            self.clear_entries()
            self.update_employee_list()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")

    def show_payslip(self):
        selected = self.employee_listbox.curselection()
        if selected:
            emp_id = self.employee_listbox.get(selected[0]).split(" - ")[0]
            payslip = self.payroll_system.employees[emp_id].generate_payslip()
            self.payslip_text.delete(1.0, END)
            self.payslip_text.insert(END, payslip)
        else:
            messagebox.showerror("Error", "Select an employee from the list!")

    def update_employee_list(self):
        self.employee_listbox.delete(0, END)
        for emp_id, emp in self.payroll_system.employees.items():
            self.employee_listbox.insert(END, f"{emp_id} - {emp.name}")

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, END)

    def search_employee(self):
        query = self.search_entry.get().lower()
        self.employee_listbox.delete(0, END)
        for emp_id, emp in self.payroll_system.employees.items():
            if query in emp_id.lower() or query in emp.name.lower():
                self.employee_listbox.insert(END, f"{emp_id} - {emp.name}")

    def display_payslip(self, event):
        self.show_payslip()


if __name__ == "__main__":
    root = Tk()
    app = PayrollGUI(root)
    root.mainloop()
