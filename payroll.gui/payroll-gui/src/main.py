from tkinter import Tk, StringVar, Label, Entry, Button, messagebox, Listbox, Scrollbar, END, Frame, Toplevel, LEFT, RIGHT, BOTH, Y, font

from payroll import PayrollSystem

class PayrollGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Payroll Accounting System")
        self.master.geometry("700x600")
        self.master.configure(bg="#f0f4f8")  # soft background
        self.payroll_system = PayrollSystem()

        # Fonts
        self.header_font = ("Segoe UI", 20, "bold")
        self.label_font = ("Segoe UI", 14)
        self.button_font = ("Segoe UI", 12, "bold")
        self.list_font = ("Segoe UI", 12)

        self.emp_id_var = StringVar()
        self.name_var = StringVar()
        self.basic_var = StringVar()
        self.hra_var = StringVar()
        self.allowance_var = StringVar()
        self.pf_var = StringVar()
        self.tax_var = StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Header
        Label(self.master, text="💼 Payroll Accounting System", font=self.header_font,
              bg="#4a90e2", fg="white", pady=10).pack(fill='x')

        # Left frame (inputs)
        input_frame = Frame(self.master, bg="white", bd=2, relief="ridge", padx=10, pady=10)
        input_frame.place(relx=0.02, rely=0.08, relwidth=0.45, relheight=0.85)

        fields = ["Employee ID", "Name", "Basic Salary", "HRA", "Allowance", "PF Deduction", "Tax Deduction"]
        self.entries = {}
        for i, field in enumerate(fields):
            Label(input_frame, text=field, font=self.label_font, bg="white").grid(row=i, column=0, sticky="w", pady=5)
            entry = Entry(input_frame, font=self.label_font, bd=2, relief="solid")
            entry.grid(row=i, column=1, pady=5)
            self.entries[field] = entry

        # Buttons
        Button(input_frame, text="Add Employee", bg="#4CAF50", fg="white", font=self.button_font,
               command=self.add_employee).grid(row=7, column=0, pady=10, padx=5)
        Button(input_frame, text="Show Payslip", bg="#2196F3", fg="white", font=self.button_font,
               command=self.show_payslip_popup).grid(row=7, column=1, pady=10, padx=5)
        Button(input_frame, text="Delete Employee", bg="#d9534f", fg="white", font=self.button_font,
               command=self.delete_employee).grid(row=7, column=2, pady=10, padx=5)
        Button(input_frame, text="Clear", bg="#f44336", fg="white", font=self.button_font,
               command=self.clear_entries).grid(row=8, column=0, columnspan=3, pady=5, sticky="we")

        # Right frame (employee list)
        list_frame = Frame(self.master, bg="white", bd=2, relief="ridge")
        list_frame.place(relx=0.50, rely=0.08, relwidth=0.48, relheight=0.85)

        Label(list_frame, text="Employees:", font=self.label_font, bg="white").pack(anchor="w", padx=5, pady=5)
        self.employee_listbox = Listbox(list_frame, font=self.list_font)
        self.employee_listbox.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        self.employee_listbox.bind('<<ListboxSelect>>', self.on_employee_select)

        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.employee_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.employee_listbox.yview)

        Button(self.master, text="Refresh List", bg="#FFC107", font=self.button_font,
               command=self.list_employees).place(relx=0.50, rely=0.95, relwidth=0.48)

    # Functions
    def add_employee(self):
        try:
            emp_id = self.entries["Employee ID"].get().strip()
            name = self.entries["Name"].get().strip()
            basic = float(self.entries["Basic Salary"].get())
            hra = float(self.entries["HRA"].get())
            allowance = float(self.entries["Allowance"].get())
            pf = float(self.entries["PF Deduction"].get())
            tax = float(self.entries["Tax Deduction"].get())
            if not emp_id or not name:
                messagebox.showerror("Error", "Employee ID and Name are required.")
                return
            if emp_id in self.payroll_system.employees:
                messagebox.showerror("Error", "Employee ID already exists.")
                return
            self.payroll_system.add_employee(emp_id, name, basic, hra, allowance, pf, tax)
            messagebox.showinfo("Success", f"Employee {name} added successfully!")
            self.clear_entries()
            self.list_employees()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values.")

    def show_payslip_popup(self):
        emp_id = self.entries["Employee ID"].get().strip()
        emp = self.payroll_system.employees.get(emp_id)
        if not emp:
            messagebox.showerror("Error", "Employee not found!")
            return
        gross, deductions, net = emp.calculate_salary()
        payslip = (
            f"----- PAYSLIP -----\n"
            f"Employee ID : {emp.emp_id}\n"
            f"Name        : {emp.name}\n"
            f"Basic       : {emp.basic}\n"
            f"HRA         : {emp.hra}\n"
            f"Allowance   : {emp.allowance}\n"
            f"Gross       : {gross}\n"
            f"PF Deduct   : {emp.pf}\n"
            f"Tax Deduct  : {emp.tax}\n"
            f"Net Salary  : {net}\n"
            f"-------------------"
        )
        self.show_popup("Payslip", payslip)

    def on_employee_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            emp_id = self.employee_listbox.get(index).split(" - ")[0]
            emp = self.payroll_system.employees.get(emp_id)
            if emp:
                self.entries["Employee ID"].delete(0, END)
                self.entries["Employee ID"].insert(0, emp.emp_id)
                self.entries["Name"].delete(0, END)
                self.entries["Name"].insert(0, emp.name)
                self.entries["Basic Salary"].delete(0, END)
                self.entries["Basic Salary"].insert(0, str(emp.basic))
                self.entries["HRA"].delete(0, END)
                self.entries["HRA"].insert(0, str(emp.hra))
                self.entries["Allowance"].delete(0, END)
                self.entries["Allowance"].insert(0, str(emp.allowance))
                self.entries["PF Deduction"].delete(0, END)
                self.entries["PF Deduction"].insert(0, str(emp.pf))
                self.entries["Tax Deduction"].delete(0, END)
                self.entries["Tax Deduction"].insert(0, str(emp.tax))

    def list_employees(self):
        self.employee_listbox.delete(0, END)
        for emp_id, emp in self.payroll_system.employees.items():
            self.employee_listbox.insert(END, f"{emp_id} - {emp.name}")

    def clear_entries(self):
        for field in self.entries.values():
            field.delete(0, END)

    def show_popup(self, title, message):
        popup = Toplevel(self.master)
        popup.title(title)
        Label(popup, text=message, justify="left", font=("Courier", 12), padx=10, pady=10).pack()
        Button(popup, text="Close", command=popup.destroy).pack(pady=5)

    def delete_employee(self):
        emp_id = self.entries["Employee ID"].get().strip()
        if not emp_id:
            messagebox.showerror("Error", "Enter/select Employee ID to delete.")
            return
        if emp_id not in self.payroll_system.employees:
            messagebox.showerror("Error", "Employee not found.")
            return
        confirm = messagebox.askyesno("Confirm Delete", f"Delete employee {emp_id}? This cannot be undone.")
        if not confirm:
            return
        deleted = self.payroll_system.delete_employee(emp_id)
        if deleted:
            messagebox.showinfo("Deleted", f"Employee {emp_id} deleted.")
            self.clear_entries()
            self.list_employees()
        else:
            messagebox.showerror("Error", "Failed to delete employee.")

if __name__ == "__main__":
    root = Tk()
    app = PayrollGUI(root)
    root.mainloop()
