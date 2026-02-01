# Copyright (c) 2023, Your Name and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Budget(Document):
	def validate(self):
		# Validate amounts
		if self.planned_amount and self.planned_amount < 0:
			frappe.throw("Planned Amount cannot be negative")
		
		if self.actual_amount and self.actual_amount < 0:
			frappe.throw("Actual Amount cannot be negative")
		
		# Validate budget category
		if self.budget_category not in ["Labor", "Materials", "Equipment", "Overheads", "Other"]:
			frappe.throw("Budget Category must be Labor, Materials, Equipment, Overheads, or Other")
	
	def before_save(self):
		# Calculate variance
		if self.planned_amount and self.actual_amount:
			self.variance = self.actual_amount - self.planned_amount
			self.variance_percentage = (self.variance / self.planned_amount) * 100 if self.planned_amount != 0 else 0