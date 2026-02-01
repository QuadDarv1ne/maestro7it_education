import frappe
from frappe.model.document import Document

class ProjectQualityCheck(Document):
	def validate(self):
		# Проверить статус качества
		if self.status not in ["Open", "In Progress", "Passed", "Failed", "Closed"]:
			frappe.throw("Статус должен быть одним из: Open, In Progress, Passed, Failed, Closed")
		
		# Проверить тип проверки
		if self.check_type not in ["Audit", "Inspection", "Review", "Testing", "Compliance"]:
			frappe.throw("Тип проверки должен быть одним из: Audit, Inspection, Review, Testing, Compliance")
		
		# Проверить приоритет
		if self.priority not in ["Low", "Medium", "High", "Critical"]:
			frappe.throw("Приоритет должен быть одним из: Low, Medium, High, Critical")
		
		# Проверить связь проекта
		if self.project and self.task:
			task_project = frappe.db.get_value("Task", self.task, "project")
			if task_project != self.project:
				frappe.throw("Выбранная задача не принадлежит выбранному проекту")
	
	def before_save(self):
		# Обновить дату последнего изменения
		self.last_updated = frappe.utils.now_datetime()
		
		# Установить дату завершения при определенных статусах
		if self.status in ["Passed", "Failed"] and not self.completed_date:
			self.completed_date = frappe.utils.now_datetime()
		
		# Рассчитать результат проверки качества
		self.calculate_quality_result()
	
	def calculate_quality_result(self):
		"""Рассчитать результат проверки качества на основе критериев"""
		if self.passed_criteria and self.total_criteria:
			self.compliance_percentage = (self.passed_criteria / self.total_criteria) * 100
			if self.compliance_percentage >= 90:
				self.quality_rating = "Отлично"
			elif self.compliance_percentage >= 75:
				self.quality_rating = "Хорошо"
			elif self.compliance_percentage >= 50:
				self.quality_rating = "Удовлетворительно"
			else:
				self.quality_rating = "Неудовлетворительно"