"""
Генератор автоматических отчетов
Создание ежедневных, еженедельных и месячных отчетов
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict
import json


class ReportGenerator:
    """Генератор отчетов для администраторов и пользователей"""
    
    def __init__(self):
        self.report_types = {
            'daily': self.generate_daily_report,
            'weekly': self.generate_weekly_report,
            'monthly': self.generate_monthly_report,
            'custom': self.generate_custom_report
        }
    
    def generate_daily_report(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Генерация ежедневного отчета
        
        Включает:
        - Статистику за день
        - Новые турниры
        - Активность пользователей
        - Производительность системы
        """
        from app.models.tournament import Tournament
        from app.models.user import User
        from app.utils.advanced_monitoring import performance_monitor
        
        if date is None:
            date = datetime.utcnow()
        
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        # Статистика турниров
        new_tournaments = Tournament.query.filter(
            Tournament.created_at >= start_of_day,
            Tournament.created_at < end_of_day
        ).count()
        
        upcoming_tournaments = Tournament.query.filter(
            Tournament.start_date >= date.date(),
            Tournament.start_date < (date + timedelta(days=7)).date()
        ).count()
        
        # Статистика пользователей
        new_users = User.query.filter(
            User.created_at >= start_of_day,
            User.created_at < end_of_day
        ).count()
        
        active_users = User.query.filter(
            User.last_login >= start_of_day,
            User.last_login < end_of_day
        ).count()
        
        # Производительность
        perf_summary = performance_monitor.get_summary()
        
        report = {
            'type': 'daily',
            'date': date.date().isoformat(),
            'generated_at': datetime.utcnow().isoformat(),
            'tournaments': {
                'new': new_tournaments,
                'upcoming_week': upcoming_tournaments
            },
            'users': {
                'new': new_users,
                'active': active_users
            },
            'performance': {
                'total_requests': perf_summary.get('total_requests', 0),
                'avg_response_time': perf_summary.get('avg_response_time', 0),
                'error_rate': perf_summary.get('error_rate', 0),
                'slow_requests': perf_summary.get('slow_requests', 0)
            }
        }
        
        return report
    
    def generate_weekly_report(self, start_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Генерация еженедельного отчета
        
        Включает:
        - Статистику за неделю
        - Топ турниров
        - Рост пользователей
        - Тренды производительности
        """
        from app.models.tournament import Tournament
        from app.models.user import User
        from app.models.favorite import FavoriteTournament
        from app.models.rating import TournamentRating
        from sqlalchemy import func
        
        if start_date is None:
            start_date = datetime.utcnow() - timedelta(days=7)
        
        end_date = start_date + timedelta(days=7)
        
        # Статистика турниров
        new_tournaments = Tournament.query.filter(
            Tournament.created_at >= start_date,
            Tournament.created_at < end_date
        ).count()
        
        # Топ турниров по избранному
        top_tournaments = db.session.query(
            Tournament.name,
            func.count(FavoriteTournament.id).label('favorites')
        ).join(
            FavoriteTournament,
            Tournament.id == FavoriteTournament.tournament_id
        ).filter(
            FavoriteTournament.created_at >= start_date,
            FavoriteTournament.created_at < end_date
        ).group_by(Tournament.id).order_by(
            func.count(FavoriteTournament.id).desc()
        ).limit(10).all()
        
        # Статистика пользователей
        new_users = User.query.filter(
            User.created_at >= start_date,
            User.created_at < end_date
        ).count()
        
        total_users = User.query.count()
        
        # Активность по дням
        daily_activity = []
        for i in range(7):
            day_start = start_date + timedelta(days=i)
            day_end = day_start + timedelta(days=1)
            
            active = User.query.filter(
                User.last_login >= day_start,
                User.last_login < day_end
            ).count()
            
            daily_activity.append({
                'date': day_start.date().isoformat(),
                'active_users': active
            })
        
        report = {
            'type': 'weekly',
            'period': {
                'start': start_date.date().isoformat(),
                'end': end_date.date().isoformat()
            },
            'generated_at': datetime.utcnow().isoformat(),
            'tournaments': {
                'new': new_tournaments,
                'top': [
                    {'name': name, 'favorites': favorites}
                    for name, favorites in top_tournaments
                ]
            },
            'users': {
                'new': new_users,
                'total': total_users,
                'growth_rate': round((new_users / total_users * 100), 2) if total_users > 0 else 0,
                'daily_activity': daily_activity
            }
        }
        
        return report
    
    def generate_monthly_report(self, month: Optional[int] = None, year: Optional[int] = None) -> Dict[str, Any]:
        """
        Генерация месячного отчета
        
        Включает:
        - Полная статистика за месяц
        - Тренды и аналитика
        - Сравнение с предыдущим месяцем
        - Рекомендации
        """
        from app.models.tournament import Tournament
        from app.models.user import User
        from sqlalchemy import func
        
        now = datetime.utcnow()
        if month is None:
            month = now.month
        if year is None:
            year = now.year
        
        # Период текущего месяца
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        # Период предыдущего месяца
        if month == 1:
            prev_start = datetime(year - 1, 12, 1)
            prev_end = datetime(year, 1, 1)
        else:
            prev_start = datetime(year, month - 1, 1)
            prev_end = start_date
        
        # Статистика турниров
        current_tournaments = Tournament.query.filter(
            Tournament.created_at >= start_date,
            Tournament.created_at < end_date
        ).count()
        
        prev_tournaments = Tournament.query.filter(
            Tournament.created_at >= prev_start,
            Tournament.created_at < prev_end
        ).count()
        
        # Статистика пользователей
        current_users = User.query.filter(
            User.created_at >= start_date,
            User.created_at < end_date
        ).count()
        
        prev_users = User.query.filter(
            User.created_at >= prev_start,
            User.created_at < prev_end
        ).count()
        
        # Расчет изменений
        tournament_change = ((current_tournaments - prev_tournaments) / prev_tournaments * 100) if prev_tournaments > 0 else 0
        user_change = ((current_users - prev_users) / prev_users * 100) if prev_users > 0 else 0
        
        # Распределение по категориям
        category_distribution = db.session.query(
            Tournament.category,
            func.count(Tournament.id)
        ).filter(
            Tournament.created_at >= start_date,
            Tournament.created_at < end_date
        ).group_by(Tournament.category).all()
        
        report = {
            'type': 'monthly',
            'period': {
                'month': month,
                'year': year,
                'start': start_date.date().isoformat(),
                'end': end_date.date().isoformat()
            },
            'generated_at': datetime.utcnow().isoformat(),
            'tournaments': {
                'current': current_tournaments,
                'previous': prev_tournaments,
                'change_percent': round(tournament_change, 2),
                'by_category': dict(category_distribution)
            },
            'users': {
                'current': current_users,
                'previous': prev_users,
                'change_percent': round(user_change, 2)
            },
            'insights': self._generate_insights(
                current_tournaments, prev_tournaments,
                current_users, prev_users
            )
        }
        
        return report
    
    def generate_custom_report(
        self,
        start_date: datetime,
        end_date: datetime,
        metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Генерация кастомного отчета за произвольный период
        
        Args:
            start_date: Начало периода
            end_date: Конец периода
            metrics: Список метрик для включения
        """
        from app.models.tournament import Tournament
        from app.models.user import User
        
        if metrics is None:
            metrics = ['tournaments', 'users', 'activity']
        
        report = {
            'type': 'custom',
            'period': {
                'start': start_date.date().isoformat(),
                'end': end_date.date().isoformat(),
                'days': (end_date - start_date).days
            },
            'generated_at': datetime.utcnow().isoformat(),
            'data': {}
        }
        
        if 'tournaments' in metrics:
            tournaments = Tournament.query.filter(
                Tournament.created_at >= start_date,
                Tournament.created_at < end_date
            ).count()
            report['data']['tournaments'] = tournaments
        
        if 'users' in metrics:
            users = User.query.filter(
                User.created_at >= start_date,
                User.created_at < end_date
            ).count()
            report['data']['users'] = users
        
        if 'activity' in metrics:
            active_users = User.query.filter(
                User.last_login >= start_date,
                User.last_login < end_date
            ).count()
            report['data']['active_users'] = active_users
        
        return report
    
    def _generate_insights(
        self,
        current_tournaments: int,
        prev_tournaments: int,
        current_users: int,
        prev_users: int
    ) -> List[str]:
        """Генерация инсайтов на основе данных"""
        insights = []
        
        # Анализ турниров
        if current_tournaments > prev_tournaments * 1.2:
            insights.append("Значительный рост количества турниров (+20%)")
        elif current_tournaments < prev_tournaments * 0.8:
            insights.append("Снижение количества турниров (-20%)")
        
        # Анализ пользователей
        if current_users > prev_users * 1.5:
            insights.append("Взрывной рост новых пользователей (+50%)")
        elif current_users > prev_users * 1.2:
            insights.append("Хороший рост новых пользователей (+20%)")
        elif current_users < prev_users * 0.8:
            insights.append("Снижение регистраций новых пользователей")
        
        # Общие рекомендации
        if current_tournaments > 50 and current_users < 100:
            insights.append("Рекомендация: Увеличить маркетинговые усилия для привлечения пользователей")
        
        if current_users > 100 and current_tournaments < 20:
            insights.append("Рекомендация: Добавить больше турниров для удержания пользователей")
        
        return insights
    
    def export_report(self, report: Dict[str, Any], format: str = 'json') -> str:
        """
        Экспорт отчета в различные форматы
        
        Args:
            report: Данные отчета
            format: Формат экспорта (json, html, pdf)
        """
        if format == 'json':
            return json.dumps(report, indent=2, ensure_ascii=False)
        
        elif format == 'html':
            return self._export_to_html(report)
        
        elif format == 'markdown':
            return self._export_to_markdown(report)
        
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _export_to_html(self, report: Dict[str, Any]) -> str:
        """Экспорт отчета в HTML"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Отчет {report['type']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2563eb; }}
                .metric {{ background: #f3f4f6; padding: 15px; margin: 10px 0; border-radius: 8px; }}
                .positive {{ color: #10b981; }}
                .negative {{ color: #ef4444; }}
            </style>
        </head>
        <body>
            <h1>Отчет: {report['type'].upper()}</h1>
            <p>Сгенерирован: {report['generated_at']}</p>
            <pre>{json.dumps(report, indent=2, ensure_ascii=False)}</pre>
        </body>
        </html>
        """
        return html
    
    def _export_to_markdown(self, report: Dict[str, Any]) -> str:
        """Экспорт отчета в Markdown"""
        md = f"# Отчет: {report['type'].upper()}\n\n"
        md += f"**Сгенерирован**: {report['generated_at']}\n\n"
        md += "## Данные\n\n"
        md += f"```json\n{json.dumps(report, indent=2, ensure_ascii=False)}\n```\n"
        return md


# Глобальный экземпляр
report_generator = ReportGenerator()


# Импорт db для использования в запросах
from app import db
