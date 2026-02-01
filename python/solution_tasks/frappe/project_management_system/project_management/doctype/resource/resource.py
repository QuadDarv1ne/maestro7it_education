import frappe
from frappe.model.document import Document

class Resource(Document):
	def validate(self):
		# Проверить тип ресурса
		if self.resource_type not in ["Human", "Equipment", "Material"]:
			frappe.throw("Resource Type must be Human, Equipment, or Material")
		
		# Проверить ставку если указана
		if self.hourly_rate and self.hourly_rate < 0:
			frappe.throw("Hourly Rate cannot be negative")
	
	def before_save(self):
		# Установить код ресурса по умолчанию если не указан
		if not self.resource_code:
			self.resource_code = self.name