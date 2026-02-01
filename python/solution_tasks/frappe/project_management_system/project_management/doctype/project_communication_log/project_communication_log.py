import frappe
from frappe.model.document import Document

class ProjectCommunicationLog(Document):
	def validate(self):
		# Проверить тип коммуникации
		if self.communication_type not in ["Email", "Meeting", "Call", "Chat", "Document", "Report"]:
			frappe.throw("Тип коммуникации должен быть одним из: Email, Meeting, Call, Chat, Document, Report")
		
		# Проверить направление коммуникации
		if self.direction not in ["Incoming", "Outgoing"]:
			frappe.throw("Направление должно быть одним из: Incoming, Outgoing")
		
		# Проверить важность
		if self.importance not in ["Low", "Medium", "High", "Critical"]:
			frappe.throw("Важность должна быть одной из: Low, Medium, High, Critical")
		
		# Проверить статус
		if self.status not in ["Draft", "Sent", "Received", "Read", "Archived"]:
			frappe.throw("Статус должен быть одним из: Draft, Sent, Received, Read, Archived")
	
	def before_save(self):
		# Установить дату создания при первом сохранении
		if not self.creation_date:
			self.creation_date = frappe.utils.now_datetime()
		
		# Обновить дату последнего изменения
		self.last_modified = frappe.utils.now_datetime()
		
		# Установить дату отправки при изменении статуса
		if self.status == "Sent" and not self.sent_date:
			self.sent_date = frappe.utils.now_datetime()
		elif self.status == "Received" and not self.received_date:
			self.received_date = frappe.utils.now_datetime()
		elif self.status == "Read" and not self.read_date:
			self.read_date = frappe.utils.now_datetime()