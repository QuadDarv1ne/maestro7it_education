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
			"label": _("Title"),
			"fieldname": "title",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Progress"),
			"fieldname": "progress",
			"fieldtype": "Percent",
			"width": 100
		},
		{
			"label": _("Start Date"),
			"fieldname": "start_date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("End Date"),
			"fieldname": "end_date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("Project Manager"),
			"fieldname": "project_manager",
			"fieldtype": "Link",
			"options": "User",
			"width": 150
		},
		{
			"label": _("Total Budget"),
			"fieldname": "total_budget",
			"fieldtype": "Currency",
			"width": 120
		}
	]

def get_data(filters):
	conditions = []
	
	if filters:
		if filters.get("project"):
			conditions.append(f"name = '{filters.get('project')}'")
		if filters.get("status"):
			conditions.append(f"status = '{filters.get('status')}'")
	
	where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
	
	data = frappe.db.sql("""
		SELECT 
			name as project,
			title,
			status,
			progress,
			expected_start_date as start_date,
			expected_end_date as end_date,
			project_manager,
			total_budget
		FROM `tabProject`
		{where_clause}
		ORDER BY creation DESC
	""".format(where_clause=where_clause), as_dict=1)
	
	return data