import frappe
from frappe import _

def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	
	user = frappe.session.user
	context.projects = get_projects_for_user(user)
	context.tasks = get_tasks_for_user(user)
	context.stats = get_user_stats(user)

def get_projects_for_user(user):
	"""Получить проекты, назначенные или управляемые пользователем"""
	# Проекты, где пользователь является менеджером проекта
	managed_projects = frappe.get_all(
		"Project",
		filters={"project_manager": user},
		fields=["name", "title", "status", "progress", "expected_start_date", "expected_end_date"],
		order_by="creation desc"
	)
	
	# Проекты, где у пользователя есть назначенные задачи
	task_projects = frappe.db.sql("""
		SELECT DISTINCT p.name, p.title, p.status, p.progress, p.expected_start_date, p.expected_end_date
		FROM `tabProject` p
		JOIN `tabTask` t ON p.name = t.project
		WHERE t.assignee = %s
	""", user, as_dict=1)
	
	# Объединить и удалить дубликаты
	all_projects = managed_projects + [p for p in task_projects if p not in managed_projects]
	return all_projects

def get_tasks_for_user(user):
	"""Получить задачи, назначенные пользователю"""
	tasks = frappe.get_all(
		"Task",
		filters={"assignee": user},
		fields=["name", "title", "status", "priority", "project", "exp_start_date", "exp_end_date"],
		order_by="creation desc"
	)
	return tasks

def get_user_stats(user):
	"""Получить статистику пользователя"""
	stats = {}
	
	# Всего проектов под управлением
	stats['managed_projects'] = frappe.db.count("Project", {"project_manager": user})
	
	# Всего проектов, в которых участвует
	stats['involved_projects'] = len(get_projects_for_user(user))
	
	# Всего назначенных задач
	stats['assigned_tasks'] = frappe.db.count("Task", {"assignee": user})
	
	# Выполненные задачи
	stats['completed_tasks'] = frappe.db.count("Task", {"assignee": user, "status": "Completed"})
	
	# Незавершенные задачи
	stats['pending_tasks'] = stats['assigned_tasks'] - stats['completed_tasks']
	
	return stats