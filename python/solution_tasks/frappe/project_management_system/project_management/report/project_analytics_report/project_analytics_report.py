import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"label": _("Metric"),
			"fieldname": "metric",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Value"),
			"fieldname": "value",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Description"),
			"fieldname": "description",
			"fieldtype": "Data",
			"width": 300
		}
	]

def get_data(filters):
	data = []
	
	# Статистика проектов
	data.append({"metric": "Total Projects", "value": str(frappe.db.count("Project")), "description": "Overall number of projects in the system"})
	
	active_projects = frappe.db.count("Project", {"status": ["in", ["Open", "Working"]]})
	data.append({"metric": "Active Projects", "value": str(active_projects), "description": "Projects that are currently open or in progress"})
	
	completed_projects = frappe.db.count("Project", {"status": "Completed"})
	data.append({"metric": "Completed Projects", "value": str(completed_projects), "description": "Projects that have been completed"})
	
	# Средний прогресс проектов
	avg_progress = frappe.db.sql("""
		SELECT AVG(progress) FROM `tabProject` WHERE status IN ('Open', 'Working')
	""")[0][0] or 0
	data.append({"metric": "Average Project Progress", "value": f"{round(avg_progress, 2)}%", "description": "Average progress percentage of active projects"})
	
	# Статистика задач
	data.append({"metric": "Total Tasks", "value": str(frappe.db.count("Task")), "description": "Overall number of tasks in the system"})
	
	completed_tasks = frappe.db.count("Task", {"status": "Completed"})
	data.append({"metric": "Completed Tasks", "value": str(completed_tasks), "description": "Number of tasks that have been completed"})
	
	# Статистика ресурсов
	data.append({"metric": "Total Resources", "value": str(frappe.db.count("Resource")), "description": "Overall number of resources registered"})
	
	human_resources = frappe.db.count("Resource", {"resource_type": "Human"})
	data.append({"metric": "Human Resources", "value": str(human_resources), "description": "Number of human resources"})
	
	# Статистика бюджета
	total_budget = frappe.db.sql("""
		SELECT SUM(total_budget) FROM `tabProject` WHERE total_budget IS NOT NULL
	""")[0][0] or 0
	data.append({"metric": "Total Budget", "value": f"${total_budget:,.2f}", "description": "Sum of all project budgets"})
	
	return data