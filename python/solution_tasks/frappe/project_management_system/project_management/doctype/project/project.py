# Copyright (c) 2023, Your Name and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Project(Document):
	def validate(self):
		# Validate project dates
		if self.expected_start_date and self.expected_end_date:
			if self.expected_start_date > self.expected_end_date:
				frappe.throw("Expected Start Date cannot be greater than Expected End Date")
		
		# Validate budget
		if self.total_budget and self.total_budget < 0:
			frappe.throw("Total Budget cannot be negative")
	
	def before_save(self):
		# Calculate project progress
		self.calculate_progress()
	
	def calculate_progress(self):
		"""Calculate project progress based on tasks"""
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