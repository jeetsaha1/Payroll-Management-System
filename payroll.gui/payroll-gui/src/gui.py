from tkinter import *
from tkinter import messagebox
from payroll import PayrollSystem

class PayrollGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Payroll Accounting System")
        self.payroll_system = PayrollSystem()

        self.create_widgets()

    def create_widgets(self):
        self.emp_id_label = Label(self.master, text="Employee ID:")
        self.emp_id_label.grid(row=0, column=0)
        self.emp_id_entry = Entry(self.master)
        self.emp_id_entry.grid(row=0, column=1)

        self.name_label = Label(self.master, text="Employee Name:")
        self.name_label.grid(row=1, column=0)
        self.name_entry = Entry(self.master)
        self.name_entry.grid(row=1, column=1)

        self.basic_label = Label(self.master, text="Basic Salary:")
        self.basic_label.grid(row=2, column=0)
        self.basic_entry = Entry(self.master)
        self.basic_entry.grid(row=2, column=1)

        self.hra_label = Label(self.master, text="HRA:")
        self.hra_label.grid(row=3, column=0)
        self.hra_entry = Entry(self.master)
        self.hra_entry.grid(row=3, column=1)

        self.allowance_label = Label(self.master, text="Allowance:")
        self.allowance_label.grid(row=4, column=0)
        self.allowance_entry = Entry(self.master)
        self.allowance_entry.grid(row=4, column=1)

        self.pf_label = Label(self.master, text="PF Deduction:")
        self.pf_label.grid(row=5, column=0)
        self.pf_entry = Entry(self.master)
        self.pf_entry.grid(row=5, column=1)

        self.tax_label = Label(self.master, text="Tax Deduction:")
        self.tax_label.grid(row=6, column=0)
        self.tax_entry = Entry(self.master)
        self.tax_entry.grid(row=6, column=1)

        self.add_button = Button(self.master, text="Add Employee", command=self.add_employee)
        self.add_button.grid(row=7, column=0, columnspan=2)

        self.show_button = Button(self.master, text="Show Payslip", command=self.show_payslip)
        self.show_button.grid(row=8, column=0, columnspan=2)

        self.list_button = Button(self.master, text="List Employees", command=self.list_employees)
        self.list_button.grid(row=9, column=0, columnspan=2)

    def add_employee(self):
        try:
            emp_id = self.emp_id_entry.get()
            name = self.name_entry.get()
            basic = float(self.basic_entry.get())
            hra = float(self.hra_entry.get())
            allowance = float(self.allowance_entry.get())
            pf = float(self.pf_entry.get())
            tax = float(self.tax_entry.get())
            self.payroll_system.add_employee(emp_id, name, basic, hra, allowance, pf, tax)
            messagebox.showinfo("Success", f"Employee {name} added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for salary and deductions.")

    def show_payslip(self):
        emp_id = self.emp_id_entry.get()
        if emp_id in self.payroll_system.employees:
            payslip = self.payroll_system.employees[emp_id].generate_payslip()
            messagebox.showinfo("Payslip", payslip)
        else:
            messagebox.showerror("Error", "Employee not found!")

    def list_employees(self):
        employee_list = "\n".join([f"{emp_id} - {emp.name}" for emp_id, emp in self.payroll_system.employees.items()])
        messagebox.showinfo("Employee List", employee_list if employee_list else "No employees found.")

if __name__ == "__main__":
    root = Tk()
    app = PayrollGUI(root)
    root.mainloop()