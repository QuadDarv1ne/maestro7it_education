import frappe
from frappe.model.document import Document

class ProjectTimeline(Document):
	def validate(self):
		# Проверить что дата начала не после даты окончания
		if self.start_date and self.end_date:
			if self.start_date > self.end_date:
				frappe.throw("Start date cannot be after end date")
		
		# Проверить тип шкалы времени
		if self.timeline_type not in ["Milestone", "Phase", "Task", "Event"]:
			frappe.throw("Timeline type must be Milestone, Phase, Task, or Event")
		
		# Проверить связь проекта
		if self.project and self.task:
			task_project = frappe.db.get_value("Task", self.task, "project")
			if task_project != self.project:
				frappe.throw("Selected task does not belong to the selected project")
	
	def before_save(self):
		# Установить продолжительность если обе даты заданы
		if self.start_date and self.end_date:
			from datetime import datetime
			duration = (self.end_date - self.start_date).days + 1
			self.duration = duration