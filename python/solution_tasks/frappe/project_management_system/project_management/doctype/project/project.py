import frappe
from frappe.model.document import Document

class Project(Document):
	def validate(self):
		# Проверить даты проекта
		if self.expected_start_date and self.expected_end_date:
			if self.expected_start_date > self.expected_end_date:
				frappe.throw("Expected Start Date cannot be greater than Expected End Date")
		
		# Проверить бюджет
		if self.total_budget and self.total_budget < 0:
			frappe.throw("Total Budget cannot be negative")
	
	def before_save(self):
		# Вычислить прогресс проекта
		self.calculate_progress()
		# Вычислить завершение вех
		self.calculate_milestone_completion()
	
	def calculate_progress(self):
		"""Вычисляет прогресс проекта на основе задач"""
		if not self.name:
			return
		
		total_tasks = frappe.db.count("Task", {"project": self.name})
		if total_tasks == 0:
			self.progress = 0
			return
		
		completed_tasks = frappe.db.count("Task", {
			"project": self.name,
			"status": "Completed"
		})
		
		self.progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

	def calculate_milestone_completion(self):
		"""Вычисляет завершение вех проекта"""
		if not self.name:
			return
		
		total_milestones = frappe.db.count("Project Milestone", {"project": self.name})
		if total_milestones == 0:
			self.milestone_completion = 0
			return
		
		completed_milestones = frappe.db.count("Project Milestone", {
			"project": self.name,
			"status": "Completed"
		})
		
		self.milestone_completion = int((completed_milestones / total_milestones) * 100) if total_milestones > 0 else 0