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
			"label": _("Risk Name"),
			"fieldname": "risk_name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Risk Type"),
			"fieldname": "risk_type",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Probability (%)"),
			"fieldname": "probability",
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"label": _("Impact (%)"),
			"fieldname": "impact",
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"label": _("Risk Score"),
			"fieldname": "risk_score",
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"label": _("Risk Level"),
			"fieldname": "risk_level",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 120
		}
	]

def get_data(filters):
	conditions = []
	
	if filters:
		if filters.get("project"):
			conditions.append(f"project = '{filters.get('project')}'")
		if filters.get("risk_level"):
			conditions.append(f"risk_level = '{filters.get('risk_level')}'")
		if filters.get("status"):
			conditions.append(f"status = '{filters.get('status')}'")
	
	where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
	
	data = frappe.db.sql("""
		SELECT 
			project,
			risk_name,
			risk_type,
			probability,
			impact,
			risk_score,
			risk_level,
			status
		FROM `tabProject Risk`
		{where_clause}
		ORDER BY risk_score DESC, creation DESC
	""".format(where_clause=where_clause), as_dict=1)
	
	return data