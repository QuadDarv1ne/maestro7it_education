import base64
from io import BytesIO
from datetime import datetime, date
from app.models import Employee, Department, Position, Vacation
from functools import lru_cache
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Try to import optional packages
try:
    import matplotlib
    matplotlib.use('Agg')  # Установка backend для работы в многопоточной среде
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Настройка стиля для matplotlib
# (Настройки стиля отключены из-за проблем с импортом)

@lru_cache(maxsize=32)
def create_employee_distribution_chart(department_stats):
    """Создание графика распределения сотрудников по подразделениям"""
    if not MATPLOTLIB_AVAILABLE:
        return None
    
    try:
        # Создаем график matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        
        departments = [stat['name'] for stat in department_stats]
        counts = [stat['count'] for stat in department_stats]
        
        bars = ax.bar(departments, counts, color='skyblue')
        ax.set_xlabel('Подразделения')
        ax.set_ylabel('Количество сотрудников')
        ax.set_title('Распределение сотрудников по подразделениям')
        ax.tick_params(axis='x', rotation=45)
        
        # Добавляем значения на столбцы
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Конвертируем в base64 для отображения в HTML
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        plt.close(fig)
        
        return graphic
    except Exception as e:
        logger.error(f"Error creating employee distribution chart: {str(e)}")
        return None

@lru_cache(maxsize=32)
def create_employee_status_chart(active_count, dismissed_count):
    """Создание круговой диаграммы статусов сотрудников"""
    if not MATPLOTLIB_AVAILABLE:
        return None
    
    try:
        fig, ax = plt.subplots(figsize=(8, 8))
        
        labels = ['Активные', 'Уволенные']
        sizes = [active_count, dismissed_count]
        colors = ['lightgreen', 'lightcoral']
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title('Распределение сотрудников по статусам')
        
        plt.tight_layout()
        
        # Конвертируем в base64 для отображения в HTML
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        plt.close(fig)
        
        return graphic
    except Exception as e:
        logger.error(f"Error creating employee status chart: {str(e)}")
        return None

@lru_cache(maxsize=32)
def create_hiring_trend_chart(employees):
    """Создание графика тенденций найма по месяцам"""
    if not MATPLOTLIB_AVAILABLE or not PANDAS_AVAILABLE:
        return None
    
    try:
        # Создаем DataFrame с датами приема на работу
        hire_dates = [emp.hire_date for emp in employees]
        df = pd.DataFrame({'hire_date': hire_dates})
        df['month_year'] = df['hire_date'].apply(lambda x: x.strftime('%Y-%m'))
        
        # Группируем по месяцам
        monthly_hires = df.groupby('month_year').size().reset_index(name='count')
        
        # Создаем график
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(monthly_hires['month_year'], monthly_hires['count'], marker='o', linewidth=2, markersize=6, color='#1f77b4')
        ax.set_xlabel('Месяц')
        ax.set_ylabel('Количество нанятых сотрудников')
        ax.set_title('Динамика найма сотрудников по месяцам')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Конвертируем в base64 для отображения в HTML
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        plt.close(fig)
        
        return graphic
    except Exception as e:
        logger.error(f"Error creating hiring trend chart: {str(e)}")
        return None

@lru_cache(maxsize=32)
def create_vacation_analysis_chart(vacations):
    """Создание анализа отпусков по типам"""
    if not MATPLOTLIB_AVAILABLE:
        return None
    
    try:
        # Подсчитываем количество отпусков по типам
        vacation_types = {}
        for vacation in vacations:
            v_type = vacation.type
            vacation_type_names = {
                'paid': 'Оплачиваемый',
                'unpaid': 'Неоплачиваемый',
                'sick': 'Больничный'
            }
            type_name = vacation_type_names.get(v_type, 'Другое')
                
            if type_name in vacation_types:
                vacation_types[type_name] += 1
            else:
                vacation_types[type_name] = 1
        
        # Создаем круговую диаграмму
        fig, ax = plt.subplots(figsize=(8, 8))
        
        labels = list(vacation_types.keys())
        sizes = list(vacation_types.values())
        colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen']
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title('Распределение отпусков по типам')
        
        plt.tight_layout()
        
        # Конвертируем в base64 для отображения в HTML
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        plt.close(fig)
        
        return graphic
    except Exception as e:
        logger.error(f"Error creating vacation analysis chart: {str(e)}")
        return None

@lru_cache(maxsize=32)
def create_department_comparison_chart(departments, employees):
    """Создание сравнения подразделений по численности"""
    if not MATPLOTLIB_AVAILABLE:
        return None
    
    try:
        # Подсчитываем количество сотрудников в каждом подразделении
        dept_counts = {}
        for dept in departments:
            dept_counts[dept.name] = len([e for e in employees if e.department_id == dept.id])
        
        # Создаем график
        fig, ax = plt.subplots(figsize=(10, 6))
        
        dept_names = list(dept_counts.keys())
        counts = list(dept_counts.values())
        
        bars = ax.bar(dept_names, counts, color='lightseagreen')
        ax.set_xlabel('Подразделения')
        ax.set_ylabel('Количество сотрудников')
        ax.set_title('Сравнение численности подразделений')
        ax.tick_params(axis='x', rotation=45)
        
        # Добавляем значения на столбцы
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Конвертируем в base64 для отображения в HTML
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        plt.close(fig)
        
        return graphic
    except Exception as e:
        logger.error(f"Error creating department comparison chart: {str(e)}")
        return None

@lru_cache(maxsize=32)
def create_turnover_chart(employees):
    """Создание графика текучести кадров"""
    if not MATPLOTLIB_AVAILABLE or not PANDAS_AVAILABLE:
        return None
    
    try:
        # Фильтруем уволенных сотрудников
        dismissed_employees = [emp for emp in employees if emp.status == 'dismissed']
        if not dismissed_employees:
            return None
            
        # Создаем DataFrame с датами увольнения
        dismissal_dates = [emp.hire_date for emp in dismissed_employees]
        df = pd.DataFrame({'dismissal_date': dismissal_dates})
        df['month_year'] = df['dismissal_date'].apply(lambda x: x.strftime('%Y-%m'))
        
        # Группируем по месяцам
        monthly_dismissals = df.groupby('month_year').size().reset_index(name='count')
        
        # Создаем график
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(monthly_dismissals['month_year'], monthly_dismissals['count'], color='indianred')
        ax.set_xlabel('Месяц')
        ax.set_ylabel('Количество уволенных сотрудников')
        ax.set_title('Текучесть кадров по месяцам')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Конвертируем в base64 для отображения в HTML
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        plt.close(fig)
        
        return graphic
    except Exception as e:
        logger.error(f"Error creating turnover chart: {str(e)}")
        return None

@lru_cache(maxsize=32)
def create_vacation_duration_chart(vacations):
    """Создание гистограммы длительности отпусков"""
    if not MATPLOTLIB_AVAILABLE:
        return None
    
    try:
        # Вычисляем длительность отпусков
        durations = [(v.end_date - v.start_date).days + 1 for v in vacations]
        
        if not durations:
            return None
            
        # Создаем гистограмму
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(durations, bins=20, color='mediumpurple', alpha=0.7, edgecolor='black')
        ax.set_xlabel('Длительность (дни)')
        ax.set_ylabel('Количество отпусков')
        ax.set_title('Распределение отпусков по длительности')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Конвертируем в base64 для отображения в HTML
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        plt.close(fig)
        
        return graphic
    except Exception as e:
        logger.error(f"Error creating vacation duration chart: {str(e)}")
        return None

@lru_cache(maxsize=32)
def create_employee_performance_chart(employees, vacations):
    """Создание графика производительности сотрудников по отпускам"""
    if not MATPLOTLIB_AVAILABLE:
        return None
    
    try:
        # Вычисляем количество отпусков на сотрудника
        employee_vacation_counts = {}
        for vacation in vacations:
            emp_id = vacation.employee_id
            if emp_id in employee_vacation_counts:
                employee_vacation_counts[emp_id] += 1
            else:
                employee_vacation_counts[emp_id] = 1
        
        # Создаем график
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Получаем имена сотрудников и количество отпусков
        employee_names = []
        vacation_counts = []
        
        # Берем только первые 20 сотрудников для читаемости графика
        sorted_employees = sorted(employee_vacation_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        
        for emp_id, count in sorted_employees:
            # Находим сотрудника по ID
            employee = next((e for e in employees if e.id == emp_id), None)
            if employee:
                employee_names.append(employee.full_name)
                vacation_counts.append(count)
        
        if not employee_names:
            return None
        
        bars = ax.bar(range(len(employee_names)), vacation_counts, color='cornflowerblue')
        ax.set_xlabel('Сотрудники')
        ax.set_ylabel('Количество отпусков')
        ax.set_title('Топ-20 сотрудников по количеству отпусков')
        ax.set_xticks(range(len(employee_names)))
        ax.set_xticklabels(employee_names, rotation=45, ha='right')
        
        # Добавляем значения на столбцы
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Конвертируем в base64 для отображения в HTML
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        plt.close(fig)
        
        return graphic
    except Exception as e:
        logger.error(f"Error creating employee performance chart: {str(e)}")
        return None

def create_interactive_dashboard_data(employees, departments, positions, vacations):
    """Создание данных для интерактивной панели мониторинга"""
    try:
        # Статистика по сотрудникам
        total_employees = len(employees)
        active_employees = len([e for e in employees if e.status == 'active'])
        dismissed_employees = len([e for e in employees if e.status == 'dismissed'])
        
        # Статистика по подразделениям
        dept_data = []
        for dept in departments:
            dept_count = len([e for e in employees if e.department_id == dept.id])
            dept_data.append({
                'name': dept.name,
                'employee_count': dept_count
            })
        
        # Статистика по должностям
        position_data = []
        for pos in positions:
            pos_count = len([e for e in employees if e.position_id == pos.id])
            position_data.append({
                'title': pos.title,
                'employee_count': pos_count
            })
        
        # Статистика по отпускам
        vacation_stats = {
            'paid': len([v for v in vacations if v.type == 'paid']),
            'unpaid': len([v for v in vacations if v.type == 'unpaid']),
            'sick': len([v for v in vacations if v.type == 'sick'])
        }
        
        # Тренды найма
        monthly_hires = []
        if PANDAS_AVAILABLE:
            try:
                hire_dates = [emp.hire_date for emp in employees]
                df = pd.DataFrame({'hire_date': hire_dates})
                df['month_year'] = df['hire_date'].apply(lambda x: x.strftime('%Y-%m'))
                monthly_hires_df = df.groupby('month_year').size().reset_index(name='count')
                monthly_hires = monthly_hires_df.to_dict('records')
            except Exception as e:
                logger.error(f"Error processing hiring trends: {str(e)}")
                monthly_hires = []
        
        # Средняя продолжительность отпусков
        if vacations:
            total_vacation_days = sum([(v.end_date - v.start_date).days + 1 for v in vacations])
            avg_vacation_duration = total_vacation_days / len(vacations)
        else:
            avg_vacation_duration = 0
        
        return {
            'total_employees': total_employees,
            'active_employees': active_employees,
            'dismissed_employees': dismissed_employees,
            'department_stats': dept_data,
            'position_stats': position_data,
            'vacation_stats': vacation_stats,
            'monthly_hires': monthly_hires,
            'avg_vacation_duration': round(avg_vacation_duration, 2)
        }
    except Exception as e:
        logger.error(f"Error creating interactive dashboard data: {str(e)}")
        return {
            'total_employees': 0,
            'active_employees': 0,
            'dismissed_employees': 0,
            'department_stats': [],
            'position_stats': [],
            'vacation_stats': {},
            'monthly_hires': [],
            'avg_vacation_duration': 0
        }

def create_interactive_charts(interactive_data, departments=None, employees=None, vacations=None):
    """Создание интерактивных графиков с помощью Plotly"""
    charts = {}
    
    if not PLOTLY_AVAILABLE:
        return charts
    
    try:
        # Круговая диаграмма статусов сотрудников
        fig1 = go.Figure(data=[go.Pie(labels=['Активные', 'Уволенные'], 
                                     values=[interactive_data['active_employees'], 
                                            interactive_data['dismissed_employees']],
                                     marker_colors=['lightgreen', 'lightcoral'])])
        fig1.update_layout(title='Распределение сотрудников по статусам')
        charts['status_chart'] = fig1.to_html(include_plotlyjs=False, div_id='status_chart')
        
        # Гистограмма по подразделениям
        dept_names = [d['name'] for d in interactive_data['department_stats']]
        dept_counts = [d['employee_count'] for d in interactive_data['department_stats']]
        
        fig2 = go.Figure(data=[go.Bar(x=dept_names, y=dept_counts, marker_color='skyblue')])
        fig2.update_layout(title='Распределение сотрудников по подразделениям',
                          xaxis_title='Подразделения',
                          yaxis_title='Количество сотрудников')
        charts['department_chart'] = fig2.to_html(include_plotlyjs=False, div_id='department_chart')
        
        # Круговая диаграмма типов отпусков
        vacation_labels = list(interactive_data['vacation_stats'].keys())
        vacation_values = list(interactive_data['vacation_stats'].values())
        vacation_names = ['Оплачиваемый', 'Неоплачиваемый', 'Больничный']
        
        fig3 = go.Figure(data=[go.Pie(labels=vacation_names, values=vacation_values,
                                     marker_colors=['gold', 'lightcoral', 'lightskyblue'])])
        fig3.update_layout(title='Распределение отпусков по типам')
        charts['vacation_chart'] = fig3.to_html(include_plotlyjs=False, div_id='vacation_chart')
        
        # Линейный график тенденций найма
        months = [h['month_year'] for h in interactive_data['monthly_hires']]
        hire_counts = [h['count'] for h in interactive_data['monthly_hires']]
        
        fig4 = go.Figure(data=go.Scatter(x=months, y=hire_counts, mode='lines+markers',
                                        line=dict(color='blue', width=2),
                                        marker=dict(size=6)))
        fig4.update_layout(title='Динамика найма сотрудников по месяцам',
                          xaxis_title='Месяц',
                          yaxis_title='Количество нанятых сотрудников')
        charts['hiring_trend_chart'] = fig4.to_html(include_plotlyjs=False, div_id='hiring_trend_chart')
        
        # Add new charts if additional data is provided
        if departments and employees:
            # Department comparison chart
            dept_names = [dept.name for dept in departments]
            employee_counts = [len([e for e in employees if e.department_id == dept.id]) for dept in departments]
            
            fig5 = go.Figure(data=go.Bar(x=dept_names, y=employee_counts, marker_color='lightseagreen'))
            fig5.update_layout(title='Сравнение численности подразделений',
                              xaxis_title='Подразделения',
                              yaxis_title='Количество сотрудников')
            charts['department_comparison_chart'] = fig5.to_html(include_plotlyjs=False, div_id='department_comparison_chart')
        
        if employees:
            # Filter dismissed employees
            dismissed_employees = [emp for emp in employees if emp.status == 'dismissed']
            if dismissed_employees:
                # Create DataFrame with dismissal dates
                dismissal_dates = [emp.hire_date for emp in dismissed_employees]
                df = pd.DataFrame({'dismissal_date': dismissal_dates})
                df['month_year'] = df['dismissal_date'].apply(lambda x: x.strftime('%Y-%m'))
                
                # Group by month
                monthly_dismissals = df.groupby('month_year').size().reset_index(name='count')
                
                # Create chart
                fig6 = go.Figure(data=go.Bar(x=monthly_dismissals['month_year'], 
                                           y=monthly_dismissals['count'],
                                           marker_color='indianred'))
                fig6.update_layout(title='Текучесть кадров по месяцам',
                                 xaxis_title='Месяц',
                                 yaxis_title='Количество уволенных сотрудников')
                charts['turnover_chart'] = fig6.to_html(include_plotlyjs=False, div_id='turnover_chart')
        
        if vacations:
            # Calculate vacation durations
            durations = [(v.end_date - v.start_date).days + 1 for v in vacations]
            
            if durations:
                # Create histogram
                fig7 = go.Figure(data=go.Histogram(x=durations, 
                                                 marker_color='mediumpurple',
                                                 xbins=dict(size=1)))
                fig7.update_layout(title='Распределение отпусков по длительности',
                                 xaxis_title='Длительность (дни)',
                                 yaxis_title='Количество отпусков')
                charts['vacation_duration_chart'] = fig7.to_html(include_plotlyjs=False, div_id='vacation_duration_chart')
        
        # Average vacation duration indicator
        fig8 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=interactive_data.get('avg_vacation_duration', 0),
            title={'text': "Средняя длительность отпуска (дни)"},
            gauge={'axis': {'range': [None, 30]},
                   'bar': {'color': "lightseagreen"},
                   'steps': [{'range': [0, 10], 'color': "lightcyan"},
                            {'range': [10, 20], 'color': "cyan"},
                            {'range': [20, 30], 'color': "royalblue"}],
                   'threshold': {'line': {'color': "red", 'width': 4},
                               'thickness': 0.75,
                               'value': 14}}))
        charts['avg_vacation_duration_chart'] = fig8.to_html(include_plotlyjs=False, div_id='avg_vacation_duration_chart')
        
        return charts
    except Exception as e:
        logger.error(f"Error creating interactive charts: {str(e)}")
        return charts

# New functions for additional analytics

@lru_cache(maxsize=32)
def create_department_vacation_analysis(departments, employees, vacations):
    """Создание анализа отпусков по подразделениям"""
    if not PLOTLY_AVAILABLE:
        return None
    
    try:
        # Подсчитываем количество отпусков по подразделениям
        dept_vacation_data = {}
        for vacation in vacations:
            employee = next((e for e in employees if e.id == vacation.employee_id), None)
            if employee:
                dept_name = employee.department.name
                if dept_name in dept_vacation_data:
                    dept_vacation_data[dept_name] += 1
                else:
                    dept_vacation_data[dept_name] = 1
        
        # Создаем график
        dept_names = list(dept_vacation_data.keys())
        vacation_counts = list(dept_vacation_data.values())
        
        fig = go.Figure(data=go.Bar(x=dept_names, y=vacation_counts, marker_color='orange'))
        fig.update_layout(title='Анализ отпусков по подразделениям',
                         xaxis_title='Подразделения',
                         yaxis_title='Количество отпусков')
        
        return fig.to_html(include_plotlyjs=False, div_id='dept_vacation_chart')
    except Exception as e:
        logger.error(f"Error creating department vacation analysis: {str(e)}")
        return None

@lru_cache(maxsize=32)
def create_employee_tenure_analysis(employees):
    """Создание анализа стажа сотрудников"""
    if not MATPLOTLIB_AVAILABLE or not PANDAS_AVAILABLE:
        return None
    
    try:
        # Вычисляем стаж сотрудников в годах
        today = date.today()
        tenures = []
        for emp in employees:
            if emp.hire_date:
                tenure_days = (today - emp.hire_date).days
                tenure_years = tenure_days / 365.25  # Учитываем високосные года
                tenures.append(tenure_years)
        
        if not tenures:
            return None
            
        # Создаем гистограмму
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(tenures, bins=20, color='lightblue', alpha=0.7, edgecolor='black')
        ax.set_xlabel('Стаж (годы)')
        ax.set_ylabel('Количество сотрудников')
        ax.set_title('Распределение сотрудников по стажу')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Конвертируем в base64 для отображения в HTML
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        plt.close(fig)
        
        return graphic
    except Exception as e:
        logger.error(f"Error creating employee tenure analysis: {str(e)}")
        return None

@lru_cache(maxsize=32)
def create_monthly_vacation_trend(vacations):
    """Создание графика тенденций отпусков по месяцам"""
    if not PLOTLY_AVAILABLE or not PANDAS_AVAILABLE:
        return None
    
    try:
        # Создаем DataFrame с датами отпусков
        start_dates = [vacation.start_date for vacation in vacations]
        df = pd.DataFrame({'start_date': start_dates})
        df['month_year'] = df['start_date'].apply(lambda x: x.strftime('%Y-%m'))
        
        # Группируем по месяцам
        monthly_vacations = df.groupby('month_year').size().reset_index(name='count')
        
        # Создаем график
        fig = go.Figure(data=go.Scatter(x=monthly_vacations['month_year'], 
                                       y=monthly_vacations['count'], 
                                       mode='lines+markers',
                                       line=dict(color='green', width=2),
                                       marker=dict(size=6)))
        fig.update_layout(title='Динамика отпусков по месяцам',
                         xaxis_title='Месяц',
                         yaxis_title='Количество отпусков')
        
        return fig.to_html(include_plotlyjs=False, div_id='monthly_vacation_trend')
    except Exception as e:
        logger.error(f"Error creating monthly vacation trend: {str(e)}")
        return None

# Additional new analytics functions

@lru_cache(maxsize=32)
def create_employee_performance_dashboard(employees, vacations):
    """Создание панели производительности сотрудников"""
    if not PLOTLY_AVAILABLE:
        return None
    
    try:
        # Вычисляем количество отпусков на сотрудника
        employee_vacation_counts = {}
        for vacation in vacations:
            emp_id = vacation.employee_id
            if emp_id in employee_vacation_counts:
                employee_vacation_counts[emp_id] += 1
            else:
                employee_vacation_counts[emp_id] = 1
        
        # Получаем имена сотрудников и количество отпусков
        employee_names = []
        vacation_counts = []
        
        # Берем только первые 15 сотрудников для читаемости графика
        sorted_employees = sorted(employee_vacation_counts.items(), key=lambda x: x[1], reverse=True)[:15]
        
        for emp_id, count in sorted_employees:
            # Находим сотрудника по ID
            employee = next((e for e in employees if e.id == emp_id), None)
            if employee:
                employee_names.append(employee.full_name)
                vacation_counts.append(count)
        
        if not employee_names:
            return None
        
        # Создаем горизонтальную гистограмму
        fig = go.Figure(data=go.Bar(
            x=vacation_counts,
            y=employee_names,
            orientation='h',
            marker_color='lightcoral'
        ))
        
        fig.update_layout(
            title='Топ-15 сотрудников по количеству отпусков',
            xaxis_title='Количество отпусков',
            yaxis_title='Сотрудники',
            height=600
        )
        
        return fig.to_html(include_plotlyjs=False, div_id='employee_performance_chart')
    except Exception as e:
        logger.error(f"Error creating employee performance dashboard: {str(e)}")
        return None

@lru_cache(maxsize=32)
def create_vacation_type_analysis(vacations):
    """Создание анализа типов отпусков"""
    if not PLOTLY_AVAILABLE:
        return None
    
    try:
        # Подсчитываем количество отпусков по типам
        vacation_types = {
            'paid': 0,
            'unpaid': 0,
            'sick': 0
        }
        
        for vacation in vacations:
            if vacation.type in vacation_types:
                vacation_types[vacation.type] += 1
        
        # Создаем круговую диаграмму
        labels = ['Оплачиваемый', 'Неоплачиваемый', 'Больничный']
        values = [vacation_types['paid'], vacation_types['unpaid'], vacation_types['sick']]
        colors = ['gold', 'lightcoral', 'lightskyblue']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker_colors=colors,
            hole=0.3  # Создаем кольцевую диаграмму
        )])
        
        fig.update_layout(
            title='Анализ типов отпусков',
            annotations=[dict(
                text='Типы отпусков',
                x=0.5,
                y=0.5,
                font_size=16,
                showarrow=False
            )]
        )
        
        return fig.to_html(include_plotlyjs=False, div_id='vacation_type_analysis')
    except Exception as e:
        logger.error(f"Error creating vacation type analysis: {str(e)}")
        return None

@lru_cache(maxsize=32)
def create_department_efficiency_analysis(departments, employees, vacations):
    """Создание анализа эффективности подразделений"""
    if not PLOTLY_AVAILABLE:
        return None
    
    try:
        # Подсчитываем метрики для каждого подразделения
        dept_metrics = {}
        for dept in departments:
            # Количество сотрудников
            dept_employees = [e for e in employees if e.department_id == dept.id]
            employee_count = len(dept_employees)
            
            # Количество отпусков
            dept_vacations = 0
            for emp in dept_employees:
                emp_vacations = [v for v in vacations if v.employee_id == emp.id]
                dept_vacations += len(emp_vacations)
            
            # Среднее количество отпусков на сотрудника
            avg_vacations_per_employee = dept_vacations / employee_count if employee_count > 0 else 0
            
            dept_metrics[dept.name] = {
                'employee_count': employee_count,
                'vacation_count': dept_vacations,
                'avg_vacations_per_employee': round(avg_vacations_per_employee, 2)
            }
        
        # Создаем составной график
        dept_names = list(dept_metrics.keys())
        employee_counts = [dept_metrics[name]['employee_count'] for name in dept_names]
        avg_vacations = [dept_metrics[name]['avg_vacations_per_employee'] for name in dept_names]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Гистограмма количества сотрудников
        fig.add_trace(
            go.Bar(x=dept_names, y=employee_counts, name='Количество сотрудников', marker_color='lightblue'),
            secondary_y=False,
        )
        
        # Линия среднего количества отпусков
        fig.add_trace(
            go.Scatter(x=dept_names, y=avg_vacations, mode='lines+markers', name='Средние отпуска/сотрудник', line=dict(color='red')),
            secondary_y=True,
        )
        
        fig.update_layout(
            title='Анализ эффективности подразделений',
            xaxis_title='Подразделения'
        )
        
        fig.update_yaxes(title_text="Количество сотрудников", secondary_y=False)
        fig.update_yaxes(title_text="Средние отпуска на сотрудника", secondary_y=True)
        
        return fig.to_html(include_plotlyjs=False, div_id='department_efficiency_chart')
    except Exception as e:
        logger.error(f"Error creating department efficiency analysis: {str(e)}")
        return None

@lru_cache(maxsize=32)
def create_time_series_analysis(employees, vacations):
    """Создание временного анализа найма и отпусков"""
    if not PLOTLY_AVAILABLE or not PANDAS_AVAILABLE:
        return None
    
    try:
        # Создаем DataFrame для найма
        hire_dates = [emp.hire_date for emp in employees]
        hire_df = pd.DataFrame({'date': hire_dates, 'type': 'hire'})
        
        # Создаем DataFrame для отпусков
        vacation_dates = [vac.start_date for vac in vacations]
        vacation_df = pd.DataFrame({'date': vacation_dates, 'type': 'vacation'})
        
        # Объединяем данные
        df = pd.concat([hire_df, vacation_df])
        df['month_year'] = df['date'].apply(lambda x: x.strftime('%Y-%m'))
        
        # Группируем по месяцам и типу
        monthly_data = df.groupby(['month_year', 'type']).size().reset_index(name='count')
        
        # Разделяем данные
        hire_data = monthly_data[monthly_data['type'] == 'hire']
        vacation_data = monthly_data[monthly_data['type'] == 'vacation']
        
        # Создаем график
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=hire_data['month_year'],
            y=hire_data['count'],
            mode='lines+markers',
            name='Найм сотрудников',
            line=dict(color='green', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=vacation_data['month_year'],
            y=vacation_data['count'],
            mode='lines+markers',
            name='Начало отпусков',
            line=dict(color='blue', width=2)
        ))
        
        fig.update_layout(
            title='Временной анализ найма и отпусков',
            xaxis_title='Месяц',
            yaxis_title='Количество событий'
        )
        
        return fig.to_html(include_plotlyjs=False, div_id='time_series_chart')
    except Exception as e:
        logger.error(f"Error creating time series analysis: {str(e)}")
        return None

def generate_comprehensive_analytics_report(employees, departments, positions, vacations):
    """Генерация комплексного аналитического отчета"""
    try:
        # Статистика по сотрудникам
        total_employees = len(employees)
        active_employees = len([e for e in employees if e.status == 'active'])
        dismissed_employees = len([e for e in employees if e.status == 'dismissed'])
        
        # Статистика по подразделениям
        dept_stats = []
        for dept in departments:
            dept_employees = [e for e in employees if e.department_id == dept.id]
            dept_active = len([e for e in dept_employees if e.status == 'active'])
            dept_stats.append({
                'name': dept.name,
                'total': len(dept_employees),
                'active': dept_active
            })
        
        # Статистика по отпускам
        total_vacations = len(vacations)
        paid_vacations = len([v for v in vacations if v.type == 'paid'])
        unpaid_vacations = len([v for v in vacations if v.type == 'unpaid'])
        sick_vacations = len([v for v in vacations if v.type == 'sick'])
        
        # Средняя продолжительность отпуска
        if vacations:
            total_days = sum([(v.end_date - v.start_date).days + 1 for v in vacations])
            avg_duration = total_days / len(vacations)
        else:
            avg_duration = 0
        
        # Анализ стажа
        today = date.today()
        avg_tenure = 0
        if employees:
            total_tenure = sum([(today - emp.hire_date).days for emp in employees if emp.hire_date])
            avg_tenure = total_tenure / len(employees) / 365.25  # В годах
        
        return {
            'employee_stats': {
                'total': total_employees,
                'active': active_employees,
                'dismissed': dismissed_employees,
                'avg_tenure_years': round(avg_tenure, 2)
            },
            'department_stats': dept_stats,
            'vacation_stats': {
                'total': total_vacations,
                'paid': paid_vacations,
                'unpaid': unpaid_vacations,
                'sick': sick_vacations,
                'avg_duration_days': round(avg_duration, 2)
            }
        }
    except Exception as e:
        logger.error(f"Error generating comprehensive analytics report: {str(e)}")
        return {
            'employee_stats': {},
            'department_stats': [],
            'vacation_stats': {}
        }
