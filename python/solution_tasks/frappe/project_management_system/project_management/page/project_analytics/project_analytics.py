import frappe
from frappe import _

def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	
	user = frappe.session.user
	context.project_stats = get_project_statistics()
	context.task_stats = get_task_statistics()
	context.resource_stats = get_resource_statistics()
	context.budget_stats = get_budget_statistics()

def get_project_statistics():
	"""Получить статистику по проектам"""
	stats = {}
	
	# Общее количество проектов
	stats['total_projects'] = frappe.db.count("Project")
	stats['active_projects'] = frappe.db.count("Project", {"status": ["in", ["Open", "Working"]]})
	stats['completed_projects'] = frappe.db.count("Project", {"status": "Completed"})
	stats['cancelled_projects'] = frappe.db.count("Project", {"status": "Cancelled"})
	
	# Средний прогресс проектов
	avg_progress = frappe.db.sql("""
		SELECT AVG(progress) FROM `tabProject` WHERE status IN ('Open', 'Working')
	""")[0][0] or 0
	stats['avg_project_progress'] = round(avg_progress, 2)
	
	# Проекты по приоритету
	stats['projects_by_priority'] = frappe.db.sql("""
		SELECT priority, COUNT(*) as count
		FROM `tabProject`
		GROUP BY priority
	""", as_dict=True)
	
	return stats

def get_task_statistics():
	"""Получить статистику по задачам"""
	stats = {}
	
	# Общее количество задач
	stats['total_tasks'] = frappe.db.count("Task")
	stats['completed_tasks'] = frappe.db.count("Task", {"status": "Completed"})
	stats['pending_tasks'] = frappe.db.count("Task", {"status": ["in", ["Open", "Working"]]})
	
	# Задачи по приоритету
	stats['tasks_by_priority'] = frappe.db.sql("""
		SELECT priority, COUNT(*) as count
		FROM `tabTask`
		GROUP BY priority
	""", as_dict=True)
	
	# Задачи по статусу
	stats['tasks_by_status'] = frappe.db.sql("""
		SELECT status, COUNT(*) as count
		FROM `tabTask`
		GROUP BY status
	""", as_dict=True)
	
	return stats

def get_resource_statistics():
	"""Получить статистику по ресурсам"""
	stats = {}
	
	# Общее количество ресурсов
	stats['total_resources'] = frappe.db.count("Resource")
	stats['human_resources'] = frappe.db.count("Resource", {"resource_type": "Human"})
	stats['equipment_resources'] = frappe.db.count("Resource", {"resource_type": "Equipment"})
	stats['material_resources'] = frappe.db.count("Resource", {"resource_type": "Material"})
	
	# Средняя почасовая ставка по типу
	stats['avg_hourly_rate_by_type'] = frappe.db.sql("""
		SELECT resource_type, AVG(hourly_rate) as avg_rate
		FROM `tabResource`
		GROUP BY resource_type
	""", as_dict=True)
	
	return stats

def get_budget_statistics():
	"""Получить статистику по бюджету"""
	stats = {}
	
	# Общая статистика бюджета
	total_budget = frappe.db.sql("""
		SELECT SUM(total_budget) FROM `tabProject` WHERE total_budget IS NOT NULL
	""")[0][0] or 0
	stats['total_budget_across_projects'] = total_budget
	
	# Статистика отклонений бюджета
	budget_variance = frappe.db.sql("""
		SELECT 
			COUNT(*) as total_budgets,
			SUM(CASE WHEN variance > 0 THEN 1 ELSE 0 END) as over_budget_count,
			SUM(CASE WHEN variance < 0 THEN 1 ELSE 0 END) as under_budget_count,
			AVG(variance) as avg_variance
		FROM `tabBudget`
		WHERE variance IS NOT NULL
	""")[0]
	
	stats['budget_variance_stats'] = {
		'total_budgets': budget_variance[0],
		'over_budget_count': budget_variance[1] or 0,
		'under_budget_count': budget_variance[2] or 0,
		'avg_variance': budget_variance[3] or 0
	}
	
	return stats