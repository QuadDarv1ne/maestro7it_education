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
			"label": _("Issue Name"),
			"fieldname": "issue_name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Issue Type"),
			"fieldname": "issue_type",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Priority"),
			"fieldname": "priority",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Assigned To"),
			"fieldname": "assigned_to",
			"fieldtype": "Link",
			"options": "User",
			"width": 150
		},
		{
			"label": _("Raised By"),
			"fieldname": "raised_by",
			"fieldtype": "Link",
			"options": "User",
			"width": 150
		},
		{
			"label": _("Due Date"),
			"fieldname": "due_date",
			"fieldtype": "Date",
			"width": 100
		}
	]

def get_data(filters):
	conditions = []
	
	if filters:
		if filters.get("project"):
			conditions.append(f"project = '{filters.get('project')}'")
		if filters.get("priority"):
			conditions.append(f"priority = '{filters.get('priority')}'")
		if filters.get("status"):
			conditions.append(f"status = '{filters.get('status')}'")
		if filters.get("assigned_to"):
			conditions.append(f"assigned_to = '{filters.get('assigned_to')}'")
	
	where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
	
	data = frappe.db.sql("""
		SELECT 
			project,
			issue_name,
			issue_type,
			priority,
			status,
			assigned_to,
			raised_by,
			due_date
		FROM `tabProject Issue`
		{where_clause}
		ORDER BY creation DESC
	""".format(where_clause=where_clause), as_dict=1)
	
	return data