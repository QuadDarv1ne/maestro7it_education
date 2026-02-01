import frappe
from frappe.model.document import Document

class ProjectRisk(Document):
	def validate(self):
		# Проверить вероятность (должна быть от 0 до 100)
		if self.probability and (self.probability < 0 or self.probability > 100):
			frappe.throw("Вероятность должна быть от 0 до 100")
		
		# Проверить влияние (должно быть от 0 до 100)
		if self.impact and (self.impact < 0 or self.impact > 100):
			frappe.throw("Влияние должно быть от 0 до 100")
		
		# Рассчитать уровень риска
		self.calculate_risk_level()
		
		# Проверить связь проекта
		if self.project and self.task:
			task_project = frappe.db.get_value("Task", self.task, "project")
			if task_project != self.project:
				frappe.throw("Выбранная задача не принадлежит выбранному проекту")
	
	def calculate_risk_level(self):
		"""Рассчитать уровень риска на основе вероятности и влияния"""
		if self.probability and self.impact:
			risk_score = (self.probability * self.impact) / 100
			self.risk_score = risk_score
			
			# Определить уровень риска на основе оценки
			if risk_score >= 75:
				self.risk_level = "Критический"
			elif risk_score >= 50:
				self.risk_level = "Высокий"
			elif risk_score >= 25:
				self.risk_level = "Средний"
			else:
				self.risk_level = "Низкий"
	
	def before_save(self):
		# Рассчитать уровень риска перед сохранением
		self.calculate_risk_level()