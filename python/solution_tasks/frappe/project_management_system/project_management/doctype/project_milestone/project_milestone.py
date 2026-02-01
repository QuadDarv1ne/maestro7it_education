import frappe
from frappe.model.document import Document

class ProjectMilestone(Document):
	def validate(self):
		# Проверить даты вехи
		if self.target_date and self.actual_date:
			if self.actual_date and self.actual_date > self.target_date:
				frappe.throw("Actual completion date cannot be after target date")
		
		# Проверить переходы статусов
		if self.status == "Completed" and not self.actual_date:
			frappe.throw("Actual completion date is required when status is Completed")
		
		# Проверить связь проекта
		if self.project and self.task:
			task_project = frappe.db.get_value("Task", self.task, "project")
			if task_project != self.project:
				frappe.throw("Selected task does not belong to the selected project")
	
	def before_save(self):
		# Обновить проект если веха завершена
		if self.status == "Completed" and self.docstatus == 1:
			self.update_project_completion()
	
	def update_project_completion(self):
		"""Обновить статус завершения вехи проекта"""
		if self.project:
			# Подсчитать общее количество вех для этого проекта
			total_milestones = frappe.db.count("Project Milestone", {"project": self.project})
			
			# Подсчитать завершенные вехи
			completed_milestones = frappe.db.count("Project Milestone", {
				"project": self.project,
				"status": "Completed"
			})
			
			# Обновить процент завершения вех проекта
			if total_milestones > 0:
				milestone_completion = (completed_milestones / total_milestones) * 100
				
				# Обновить документ проекта
				project_doc = frappe.get_doc("Project", self.project)
				project_doc.milestone_completion = milestone_completion
				project_doc.save()