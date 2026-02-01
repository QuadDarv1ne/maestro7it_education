# Copyright (c) 2023, Your Name and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Resource(Document):
	def validate(self):
		# Validate resource type
		if self.resource_type not in ["Human", "Equipment", "Material"]:
			frappe.throw("Resource Type must be Human, Equipment, or Material")
		
		# Validate rate if provided
		if self.hourly_rate and self.hourly_rate < 0:
			frappe.throw("Hourly Rate cannot be negative")
	
	def before_save(self):
		# Set default resource code if not provided
		if not self.resource_code:
			self.resource_code = self.name