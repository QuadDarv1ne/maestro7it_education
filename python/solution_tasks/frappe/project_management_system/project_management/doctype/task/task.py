# Copyright (c) 2023, Your Name and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Task(Document):
	def validate(self):
		# Validate task dates
		if self.exp_start_date and self.exp_end_date:
			if self.exp_start_date > self.exp_end_date:
				frappe.throw("Expected Start Date cannot be greater than Expected End Date")
		
		# Validate priority
		if self.priority not in ["Low", "Medium", "High"]:
			frappe.throw("Priority must be Low, Medium, or High")
		
		# Validate status
		if self.status not in ["Open", "Working", "Completed", "Cancelled"]:
			frappe.throw("Status must be one of: Open, Working, Completed, Cancelled")
	
	def on_update(self):
		# Update project progress when task is updated
		self.update_project_progress()
	
	def update_project_progress(self):
		"""Update project progress after task update"""
		if self.project:
			project_doc = frappe.get_doc("Project", self.project)
			project_doc.calculate_progress()
			project_doc.save()