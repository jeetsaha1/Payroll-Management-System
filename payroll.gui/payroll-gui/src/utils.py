def validate_employee_id(emp_id):
    return emp_id.isalnum() and len(emp_id) > 0

def validate_name(name):
    return len(name) > 0

def validate_salary(value):
    try:
        float_value = float(value)
        return float_value >= 0
    except ValueError:
        return False

def format_currency(value):
    return "${:,.2f}".format(value)