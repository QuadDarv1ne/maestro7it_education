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
		# Вычислить метрики рисков
		self.calculate_risk_metrics()
		# Вычислить метрики качества
		self.calculate_quality_metrics()

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

	def calculate_risk_metrics(self):
		"""Вычисляет метрики рисков проекта"""
		if not self.name:
			return
		
		# Подсчитать общее количество рисков для проекта
		total_risks = frappe.db.count("Project Risk", {"project": self.name})
		
		if total_risks > 0:
			# Подсчитать критические и высокие риски
			high_risks = frappe.db.count("Project Risk", {
				"project": self.name,
				"risk_level": ["in", ["Критический", "Высокий"]]
			})
			
			# Вычислить процент высоких рисков
			self.high_risk_percentage = int((high_risks / total_risks) * 100)
		else:
			self.high_risk_percentage = 0

	def calculate_quality_metrics(self):
		"""Вычисляет метрики качества проекта"""
		if not self.name:
			return
		
		# Подсчитать общее количество проверок качества для проекта
		total_quality_checks = frappe.db.count("Project Quality Check", {"project": self.name})
		
		if total_quality_checks > 0:
			# Подсчитать успешные проверки качества
			passed_checks = frappe.db.count("Project Quality Check", {
				"project": self.name,
				"status": "Passed"
			})
			
			# Вычислить процент успешных проверок
			self.quality_pass_rate = int((passed_checks / total_quality_checks) * 100)
		else:
			self.quality_pass_rate = 0