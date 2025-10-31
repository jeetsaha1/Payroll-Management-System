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
        # store attendance here so utils.save_data/load_data can persist it
        self.attendance = {}

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

    def delete_employee(self, emp_id) -> bool:
        """
        Delete an employee by emp_id.
        Returns True if deleted, False if not found.
        """
        if emp_id in self.employees:
            del self.employees[emp_id]
            # optionally remove attendance too
            self.attendance.pop(emp_id, None)
            return True
        return False

    def add_attendance(self, emp_id: str, date_str: str, present: bool = True) -> None:
        """Add or update attendance for an employee (wrapper over utils)."""
        from utils import add_attendance_record
        add_attendance_record(self.attendance, emp_id, date_str, present)

    def get_attendance(self, emp_id: str):
        """Return attendance dict for emp_id."""
        return self.attendance.get(emp_id, {}).copy()

    def attendance_percentage(self, emp_id: str, start_date: str = None, end_date: str = None) -> float:
        """Compute attendance percentage for an employee (wrapper over utils)."""
        from utils import attendance_percentage
        return attendance_percentage(self.attendance, emp_id, start_date, end_date)

    def get_employee(self, emp_id: str):
        """Return Employee object or None."""
        return self.employees.get(emp_id)

    def update_employee(self, emp_id: str, name: str = None,
                        basic: float = None, hra: float = None,
                        allowance: float = None, pf: float = None,
                        tax: float = None) -> bool:
        """
        Update fields for an existing employee.
        Pass only the fields you want to update.
        Returns True if updated, False if employee not found or invalid data.
        """
        emp = self.employees.get(emp_id)
        if not emp:
            return False
        try:
            if name is not None:
                emp.name = name
            if basic is not None:
                emp.basic = float(basic)
            if hra is not None:
                emp.hra = float(hra)
            if allowance is not None:
                emp.allowance = float(allowance)
            if pf is not None:
                emp.pf = float(pf)
            if tax is not None:
                emp.tax = float(tax)
        except (ValueError, TypeError):
            return False
        return True

    def search_employees(self, query: str):
        """
        Search employees by emp_id or name (case-insensitive, partial match).
        Returns list of tuples (emp_id, name).
        """
        q = (query or "").strip().lower()
        if not q:
            return []
        results = []
        for emp_id, emp in self.employees.items():
            if q in emp_id.lower() or q in emp.name.lower():
                results.append((emp_id, emp.name))
        return results