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
			"label": _("Check Name"),
			"fieldname": "check_name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Check Type"),
			"fieldname": "check_type",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Priority"),
			"fieldname": "priority",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Compliance %"),
			"fieldname": "compliance_percentage",
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"label": _("Quality Rating"),
			"fieldname": "quality_rating",
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
			"label": _("Scheduled Date"),
			"fieldname": "scheduled_date",
			"fieldtype": "Date",
			"width": 100
		}
	]

def get_data(filters):
	conditions = []
	
	if filters:
		if filters.get("project"):
			conditions.append(f"project = '{filters.get('project')}'")
		if filters.get("check_type"):
			conditions.append(f"check_type = '{filters.get('check_type')}'")
		if filters.get("status"):
			conditions.append(f"status = '{filters.get('status')}'")
		if filters.get("priority"):
			conditions.append(f"priority = '{filters.get('priority')}'")
		if filters.get("quality_rating"):
			conditions.append(f"quality_rating = '{filters.get('quality_rating')}'")
	
	where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
	
	data = frappe.db.sql("""
		SELECT 
			project,
			check_name,
			check_type,
			status,
			priority,
			compliance_percentage,
			quality_rating,
			assigned_to,
			scheduled_date
		FROM `tabProject Quality Check`
		{where_clause}
		ORDER BY compliance_percentage ASC, creation DESC
	""".format(where_clause=where_clause), as_dict=1)
	
	return data