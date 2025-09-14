class Employee:
    def __init__(self, emp_id, name, basic, hra, allowance, pf, tax):
        self.emp_id = emp_id
        self.name = name
        self.basic = basic
        self.hra = hra
        self.allowance = allowance
        self.pf = pf
        self.tax = tax

    def calculate_salary(self):
        gross = self.basic + self.hra + self.allowance
        deductions = self.pf + self.tax
        net = gross - deductions
        return gross, deductions, net

    def generate_payslip(self):
        gross, deductions, net = self.calculate_salary()
        payslip = {
            "Employee ID": self.emp_id,
            "Name": self.name,
            "Basic Salary": self.basic,
            "HRA": self.hra,
            "Allowance": self.allowance,
            "Gross Salary": gross,
            "PF Deduction": self.pf,
            "TAX Deduction": self.tax,
            "Total Deductions": deductions,
            "Net Salary": net
        }
        return payslip


class PayrollSystem:
    def __init__(self):
        self.employees = {}

    def add_employee(self, emp_id, name, basic, hra, allowance, pf, tax):
        emp = Employee(emp_id, name, basic, hra, allowance, pf, tax)
        self.employees[emp_id] = emp

    def show_payslip(self, emp_id):
        if emp_id in self.employees:
            return self.employees[emp_id].generate_payslip()
        else:
            return None

    def list_employees(self):
        return [(emp_id, emp.name) for emp_id, emp in self.employees.items()]