import frappe
from frappe.model.document import Document

class ProjectTimesheet(Document):
	def validate(self):
		# Проверить что часы положительны
		if self.hours_spent and self.hours_spent <= 0:
			frappe.throw("Hours spent must be greater than zero")
		
		# Проверить что дата не в будущем
		from datetime import date
		if self.work_date and self.work_date > date.today():
			frappe.throw("Work date cannot be in the future")
		
		# Проверить связь проекта и задачи
		if self.task and self.project:
			task_project = frappe.db.get_value("Task", self.task, "project")
			if task_project != self.project:
				frappe.throw("Selected task does not belong to the selected project")
	
	def before_save(self):
		# Рассчитать общую сумму если указана ставка
		if self.hourly_rate and self.hours_spent:
			self.total_amount = self.hourly_rate * self.hours_spent