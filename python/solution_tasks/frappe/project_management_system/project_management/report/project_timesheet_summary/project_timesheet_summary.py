import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"label": _("Project"),
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 150
		},
		{
			"label": _("Employee"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "User",
			"width": 150
		},
		{
			"label": _("Task"),
			"fieldname": "task",
			"fieldtype": "Link",
			"options": "Task",
			"width": 150
		},
		{
			"label": _("Work Date"),
			"fieldname": "work_date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("Hours Spent"),
			"fieldname": "hours_spent",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Hourly Rate"),
			"fieldname": "hourly_rate",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Total Amount"),
			"fieldname": "total_amount",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Description"),
			"fieldname": "description",
			"fieldtype": "Data",
			"width": 200
		}
	]

def get_data(filters):
	conditions = []
	
	if filters:
		if filters.get("project"):
			conditions.append(f"project = '{filters.get('project')}'")
		if filters.get("employee"):
			conditions.append(f"employee = '{filters.get('employee')}'")
		if filters.get("from_date"):
			conditions.append(f"work_date >= '{filters.get('from_date')}'")
		if filters.get("to_date"):
			conditions.append(f"work_date <= '{filters.get('to_date')}'")
	
	where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
	
	data = frappe.db.sql("""
		SELECT 
			project,
			employee,
			task,
			work_date,
			hours_spent,
			hourly_rate,
			total_amount,
			description
		FROM `tabProject Timesheet`
		{where_clause}
		ORDER BY work_date DESC, creation DESC
	""".format(where_clause=where_clause), as_dict=1)
	
	return data