import frappe
from frappe.model.document import Document

class ProjectChangeRequest(Document):
	def validate(self):
		# Проверить статус запроса
		if self.status not in ["Draft", "Submitted", "Review", "Approved", "Rejected", "Implemented"]:
			frappe.throw("Статус должен быть одним из: Draft, Submitted, Review, Approved, Rejected, Implemented")
		
		# Проверить тип изменений
		if self.change_type not in ["Scope", "Schedule", "Budget", "Resource", "Quality", "Risk"]:
			frappe.throw("Тип изменений должен быть одним из: Scope, Schedule, Budget, Resource, Quality, Risk")
		
		# Проверить приоритет
		if self.priority not in ["Low", "Medium", "High", "Critical"]:
			frappe.throw("Приоритет должен быть одним из: Low, Medium, High, Critical")
		
		# Проверить влияние
		if self.impact not in ["Low", "Medium", "High", "Critical"]:
			frappe.throw("Влияние должно быть одним из: Low, Medium, High, Critical")
	
	def before_save(self):
		# Установить дату создания при первом сохранении
		if not self.creation_date:
			self.creation_date = frappe.utils.now_datetime()
		
		# Обновить дату последнего изменения
		self.last_modified = frappe.utils.now_datetime()
		
		# Установить даты статусов при изменении
		if self.status == "Submitted" and not self.submitted_date:
			self.submitted_date = frappe.utils.now_datetime()
		elif self.status == "Approved" and not self.approved_date:
			self.approved_date = frappe.utils.now_datetime()
		elif self.status == "Rejected" and not self.rejected_date:
			self.rejected_date = frappe.utils.now_datetime()
		elif self.status == "Implemented" and not self.implemented_date:
			self.implemented_date = frappe.utils.now_datetime()