import frappe
from frappe.model.document import Document

class Budget(Document):
	def validate(self):
		# Проверить суммы
		if self.planned_amount and self.planned_amount < 0:
			frappe.throw("Planned Amount cannot be negative")
		
		if self.actual_amount and self.actual_amount < 0:
			frappe.throw("Actual Amount cannot be negative")
		
		# Проверить категорию бюджета
		if self.budget_category not in ["Labor", "Materials", "Equipment", "Overheads", "Other"]:
			frappe.throw("Budget Category must be Labor, Materials, Equipment, Overheads, or Other")
	
	def before_save(self):
		# Рассчитать отклонение
		if self.planned_amount and self.actual_amount:
			self.variance = self.actual_amount - self.planned_amount
			self.variance_percentage = (self.variance / self.planned_amount) * 100 if self.planned_amount != 0 else 0