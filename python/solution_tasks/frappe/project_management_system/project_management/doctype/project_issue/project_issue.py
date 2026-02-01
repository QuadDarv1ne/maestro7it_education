import frappe
from frappe.model.document import Document

class ProjectIssue(Document):
	def validate(self):
		# Проверить приоритет
		if self.priority not in ["Low", "Medium", "High", "Critical"]:
			frappe.throw("Приоритет должен быть одним из: Low, Medium, High, Critical")
		
		# Проверить статус
		if self.status not in ["Open", "In Progress", "Resolved", "Closed", "Cancelled"]:
			frappe.throw("Статус должен быть одним из: Open, In Progress, Resolved, Closed, Cancelled")
		
		# Проверить тип проблемы
		if self.issue_type not in ["Bug", "Feature Request", "Improvement", "Task", "Epic"]:
			frappe.throw("Тип проблемы должен быть одним из: Bug, Feature Request, Improvement, Task, Epic")
		
		# Проверить связь проекта
		if self.project and self.task:
			task_project = frappe.db.get_value("Task", self.task, "project")
			if task_project != self.project:
				frappe.throw("Выбранная задача не принадлежит выбранному проекту")
	
	def before_save(self):
		# Обновить дату последнего изменения
		self.modified_date = frappe.utils.now_datetime()
		
		# Если проблема решена, установить дату решения
		if self.status == "Resolved" and not self.resolved_date:
			self.resolved_date = frappe.utils.now_datetime()
		
		# Если проблема закрыта, установить дату закрытия
		if self.status == "Closed" and not self.closed_date:
			self.closed_date = frappe.utils.now_datetime()