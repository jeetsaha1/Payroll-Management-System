from tkinter import Tk, StringVar, Label, Entry, Button, messagebox, Listbox, Scrollbar, END, Frame, Toplevel, LEFT, RIGHT, BOTH, Y, font
from payroll import PayrollSystem

class PayrollGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Payroll Accounting System")
        self.master.geometry("500x500")
        self.payroll_system = PayrollSystem()

        # Define a bigger font
        self.big_font = ("Arial", 14)
        self.list_font = ("Arial", 13)
        self.button_font = ("Arial", 13, "bold")

        self.emp_id_var = StringVar()
        self.name_var = StringVar()
        self.basic_var = StringVar()
        self.hra_var = StringVar()
        self.allowance_var = StringVar()
        self.pf_var = StringVar()
        self.tax_var = StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Input Frame
        input_frame = Frame(self.master, padx=10, pady=10)
        input_frame.pack(fill='x')

        Label(input_frame, text="Employee ID", font=self.big_font).grid(row=0, column=0, sticky='w')
        Entry(input_frame, textvariable=self.emp_id_var, font=self.big_font).grid(row=0, column=1)

        Label(input_frame, text="Name", font=self.big_font).grid(row=1, column=0, sticky='w')
        Entry(input_frame, textvariable=self.name_var, font=self.big_font).grid(row=1, column=1)

        Label(input_frame, text="Basic Salary", font=self.big_font).grid(row=2, column=0, sticky='w')
        Entry(input_frame, textvariable=self.basic_var, font=self.big_font).grid(row=2, column=1)

        Label(input_frame, text="HRA", font=self.big_font).grid(row=3, column=0, sticky='w')
        Entry(input_frame, textvariable=self.hra_var, font=self.big_font).grid(row=3, column=1)

        Label(input_frame, text="Allowance", font=self.big_font).grid(row=4, column=0, sticky='w')
        Entry(input_frame, textvariable=self.allowance_var, font=self.big_font).grid(row=4, column=1)

        Label(input_frame, text="PF Deduction", font=self.big_font).grid(row=5, column=0, sticky='w')
        Entry(input_frame, textvariable=self.pf_var, font=self.big_font).grid(row=5, column=1)

        Label(input_frame, text="Tax Deduction", font=self.big_font).grid(row=6, column=0, sticky='w')
        Entry(input_frame, textvariable=self.tax_var, font=self.big_font).grid(row=6, column=1)

        Button(input_frame, text="Add Employee", command=self.add_employee, bg="#4CAF50", fg="white", font=self.button_font).grid(row=7, column=0, pady=10)
        Button(input_frame, text="Show Payslip", command=self.show_payslip_popup, bg="#2196F3", fg="white", font=self.button_font).grid(row=7, column=1, pady=10)
        Button(input_frame, text="Clear", command=self.clear_entries, bg="#f44336", fg="white", font=self.button_font).grid(row=7, column=2, pady=10)

        # Employee List Frame
        list_frame = Frame(self.master, padx=10, pady=10)
        list_frame.pack(fill=BOTH, expand=True)

        Label(list_frame, text="Employees:", font=self.big_font).pack(anchor='w')
        self.employee_listbox = Listbox(list_frame, font=self.list_font)
        self.employee_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        self.employee_listbox.bind('<<ListboxSelect>>', self.on_employee_select)

        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.employee_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.employee_listbox.yview)

        Button(self.master, text="Refresh List", command=self.list_employees, bg="#FFC107", font=self.button_font).pack(pady=5)

    def add_employee(self):
        try:
            emp_id = self.emp_id_var.get().strip()
            name = self.name_var.get().strip()
            basic = float(self.basic_var.get())
            hra = float(self.hra_var.get())
            allowance = float(self.allowance_var.get())
            pf = float(self.pf_var.get())
            tax = float(self.tax_var.get())
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
            messagebox.showerror("Error", "Please enter valid numeric values for salary and deductions.")

    def show_payslip_popup(self):
        emp_id = self.emp_id_var.get().strip()
        if not emp_id:
            messagebox.showerror("Error", "Please enter an Employee ID.")
            return
        emp = self.payroll_system.employees.get(emp_id)
        if not emp:
            messagebox.showerror("Error", "Employee not found!")
            return
        gross, deductions, net = emp.calculate_salary()
        payslip = (
            f"------------------- PAYSLIP -------------------\n"
            f"Employee ID   : {emp.emp_id}\n"
            f"Name          : {emp.name}\n"
            f"Basic Salary  : {emp.basic}\n"
            f"HRA           : {emp.hra}\n"
            f"Allowance     : {emp.allowance}\n"
            f"Gross Salary  : {gross}\n"
            f"PF Deduction  : {emp.pf}\n"
            f"TAX Deduction : {emp.tax}\n"
            f"Total Deductions: {deductions}\n"
            f"Net Salary    : {net}\n"
            f"------------------------------------------------"
        )
        self.show_popup("Payslip", payslip)

    def on_employee_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            emp_id = self.employee_listbox.get(index).split(" - ")[0]
            emp = self.payroll_system.employees.get(emp_id)
            if emp:
                self.emp_id_var.set(emp.emp_id)
                self.name_var.set(emp.name)
                self.basic_var.set(str(emp.basic))
                self.hra_var.set(str(emp.hra))
                self.allowance_var.set(str(emp.allowance))
                self.pf_var.set(str(emp.pf))
                self.tax_var.set(str(emp.tax))

    def list_employees(self):
        self.employee_listbox.delete(0, END)
        for emp_id, emp in self.payroll_system.employees.items():
            self.employee_listbox.insert(END, f"{emp_id} - {emp.name}")

    def clear_entries(self):
        self.emp_id_var.set("")
        self.name_var.set("")
        self.basic_var.set("")
        self.hra_var.set("")
        self.allowance_var.set("")
        self.pf_var.set("")
        self.tax_var.set("")

    def show_popup(self, title, message):
        popup = Toplevel(self.master)
        popup.title(title)
        Label(popup, text=message, justify='left', padx=10, pady=10, font=("Courier", 14)).pack()
        Button(popup, text="Close", command=popup.destroy, font=self.button_font).pack(pady=5)

if __name__ == "__main__":
    root = Tk()
    app = PayrollGUI(root)
    root.mainloop()