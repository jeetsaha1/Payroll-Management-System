import json
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional

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

def validate_attendance_date(date_str: str, fmt: str = "%Y-%m-%d") -> bool:
    """Validate date string (default YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, fmt)
        return True
    except (ValueError, TypeError):
        return False

def add_attendance_record(attendance: Dict[str, Dict[str, bool]],
                          emp_id: str,
                          date_str: str,
                          present: bool = True) -> None:
    """
    Add/mark attendance for emp_id on date_str.
    attendance structure: { emp_id: { "2025-10-01": True, ... }, ... }
    """
    if not validate_employee_id(emp_id):
        raise ValueError("Invalid employee id")
    if not validate_attendance_date(date_str):
        raise ValueError("Invalid date format, expected YYYY-MM-DD")
    attendance.setdefault(emp_id, {})[date_str] = bool(present)

def get_attendance_for_employee(attendance: Dict[str, Dict[str, bool]], emp_id: str) -> Dict[str, bool]:
    """Return attendance dict for an employee (date -> present bool)."""
    return attendance.get(emp_id, {}).copy()

def attendance_percentage(attendance: Dict[str, Dict[str, bool]],
                          emp_id: str,
                          start_date: Optional[str] = None,
                          end_date: Optional[str] = None) -> float:
    """
    Compute attendance percentage for emp_id between optional start_date and end_date (inclusive).
    Dates must be YYYY-MM-DD. If no dates provided, compute over all recorded dates.
    Returns percentage 0.0 - 100.0
    """
    records = attendance.get(emp_id, {})
    if not records:
        return 0.0

    # filter by range if provided
    def to_dt(s): return datetime.strptime(s, "%Y-%m-%d")
    filtered = {}
    if start_date or end_date:
        if start_date and not validate_attendance_date(start_date):
            raise ValueError("Invalid start_date format")
        if end_date and not validate_attendance_date(end_date):
            raise ValueError("Invalid end_date format")
        s_dt = to_dt(start_date) if start_date else min(to_dt(d) for d in records)
        e_dt = to_dt(end_date) if end_date else max(to_dt(d) for d in records)
        current = s_dt
        while current <= e_dt:
            key = current.strftime("%Y-%m-%d")
            if key in records:
                filtered[key] = records[key]
            current += timedelta(days=1)
    else:
        filtered = records

    if not filtered:
        return 0.0

    present_count = sum(1 for v in filtered.values() if v)
    total = len(filtered)
    return (present_count / total) * 100.0

def serialize_employees(employees: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Convert employees mapping into JSON-serializable dict.
    Accepts Employee instances (has attributes) or already-serializable dicts.
    """
    out = {}
    for emp_id, emp in employees.items():
        if hasattr(emp, "__dict__"):
            # typical Employee instance
            data = {
                "emp_id": getattr(emp, "emp_id", emp_id),
                "name": getattr(emp, "name", ""),
                "basic": getattr(emp, "basic", 0.0),
                "hra": getattr(emp, "hra", 0.0),
                "allowance": getattr(emp, "allowance", 0.0),
                "pf": getattr(emp, "pf", 0.0),
                "tax": getattr(emp, "tax", 0.0)
            }
        elif isinstance(emp, dict):
            data = emp.copy()
            data.setdefault("emp_id", emp_id)
        else:
            # fallback to string
            data = {"emp_id": emp_id, "repr": str(emp)}
        out[emp_id] = data
    return out

def save_data(filepath: str,
              employees: Dict[str, Any],
              attendance: Dict[str, Dict[str, bool]]) -> None:
    """
    Save employees and attendance to JSON file.
    """
    payload = {
        "employees": serialize_employees(employees),
        "attendance": attendance
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

def load_data(filepath: str,
              create_employee_objects: bool = False):
    """
    Load employees and attendance from JSON file.
    If create_employee_objects True, will attempt to construct payroll.Employee objects
    (requires payroll module available). Otherwise returns raw dicts.
    Returns tuple: (employees_dict, attendance_dict)
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except FileNotFoundError:
        return {}, {}
    employees_raw = payload.get("employees", {})
    attendance = payload.get("attendance", {})

    if create_employee_objects:
        try:
            from payroll import Employee as _Emp
        except Exception:
            # cannot import, return raw
            return employees_raw, attendance
        employees_objs = {}
        for emp_id, data in employees_raw.items():
            try:
                emp = _Emp(
                    data.get("emp_id", emp_id),
                    data.get("name", ""),
                    float(data.get("basic", 0.0)),
                    float(data.get("hra", 0.0)),
                    float(data.get("allowance", 0.0)),
                    float(data.get("pf", 0.0)),
                    float(data.get("tax", 0.0))
                )
                employees_objs[emp_id] = emp
            except Exception:
                employees_objs[emp_id] = data  # fallback
        return employees_objs, attendance

    return employees_raw, attendance