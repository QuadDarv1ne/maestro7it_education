# Copyright (c) 2023, Your Name and contributors
# For license information, please see license.txt

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
	"""Get projects assigned to or managed by user"""
	# Projects where user is project manager
	managed_projects = frappe.get_all(
		"Project",
		filters={"project_manager": user},
		fields=["name", "title", "status", "progress", "expected_start_date", "expected_end_date"],
		order_by="creation desc"
	)
	
	# Projects where user has assigned tasks
	task_projects = frappe.db.sql("""
		SELECT DISTINCT p.name, p.title, p.status, p.progress, p.expected_start_date, p.expected_end_date
		FROM `tabProject` p
		JOIN `tabTask` t ON p.name = t.project
		WHERE t.assignee = %s
	""", user, as_dict=1)
	
	# Combine and deduplicate
	all_projects = managed_projects + [p for p in task_projects if p not in managed_projects]
	return all_projects

def get_tasks_for_user(user):
	"""Get tasks assigned to user"""
	tasks = frappe.get_all(
		"Task",
		filters={"assignee": user},
		fields=["name", "title", "status", "priority", "project", "exp_start_date", "exp_end_date"],
		order_by="creation desc"
	)
	return tasks

def get_user_stats(user):
	"""Get user statistics"""
	stats = {}
	
	# Total projects managed
	stats['managed_projects'] = frappe.db.count("Project", {"project_manager": user})
	
	# Total projects involved in
	stats['involved_projects'] = len(get_projects_for_user(user))
	
	# Total tasks assigned
	stats['assigned_tasks'] = frappe.db.count("Task", {"assignee": user})
	
	# Completed tasks
	stats['completed_tasks'] = frappe.db.count("Task", {"assignee": user, "status": "Completed"})
	
	# Pending tasks
	stats['pending_tasks'] = stats['assigned_tasks'] - stats['completed_tasks']
	
	return stats