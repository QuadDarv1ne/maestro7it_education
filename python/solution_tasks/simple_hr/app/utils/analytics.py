import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Установка backend для работы в многопоточной среде
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime, date
from app.models import Employee, Department, Position, Vacation
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Настройка стиля для matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_employee_distribution_chart(department_stats):
    """Создание графика распределения сотрудников по подразделениям"""
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
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close(fig)
    
    return graphic

def create_employee_status_chart(active_count, dismissed_count):
    """Создание круговой диаграммы статусов сотрудников"""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    labels = ['Активные', 'Уволенные']
    sizes = [active_count, dismissed_count]
    colors = ['lightgreen', 'lightcoral']
    
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.set_title('Распределение сотрудников по статусам')
    
    plt.tight_layout()
    
    # Конвертируем в base64 для отображения в HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close(fig)
    
    return graphic

def create_hiring_trend_chart(employees):
    """Создание графика тенденций найма по месяцам"""
    # Создаем DataFrame с датами приема на работу
    hire_dates = [emp.hire_date for emp in employees]
    df = pd.DataFrame({'hire_date': hire_dates})
    df['month_year'] = df['hire_date'].apply(lambda x: x.strftime('%Y-%m'))
    
    # Группируем по месяцам
    monthly_hires = df.groupby('month_year').size().reset_index(name='count')
    
    # Создаем график
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_hires['month_year'], monthly_hires['count'], marker='o', linewidth=2, markersize=6)
    ax.set_xlabel('Месяц')
    ax.set_ylabel('Количество нанятых сотрудников')
    ax.set_title('Динамика найма сотрудников по месяцам')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Конвертируем в base64 для отображения в HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close(fig)
    
    return graphic

def create_vacation_analysis_chart(vacations):
    """Создание анализа отпусков по типам"""
    # Подсчитываем количество отпусков по типам
    vacation_types = {}
    for vacation in vacations:
        v_type = vacation.type
        if v_type == 'paid':
            type_name = 'Оплачиваемый'
        elif v_type == 'unpaid':
            type_name = 'Неоплачиваемый'
        elif v_type == 'sick':
            type_name = 'Больничный'
        else:
            type_name = 'Другое'
            
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
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close(fig)
    
    return graphic

def create_interactive_dashboard_data(employees, departments, positions, vacations):
    """Создание данных для интерактивной панели мониторинга"""
    # Статистика по сотрудникам
    total_employees = len(employees)
    active_employees = len([e for e in employees if e.status == 'active'])
    dismissed_employees = len([e for e in employees if e.status == 'dismissed'])
    
    # Статистика по подразделениям
    dept_data = []
    for dept in departments:
        dept_data.append({
            'name': dept.name,
            'employee_count': len(dept.employees)
        })
    
    # Статистика по должностям
    position_data = []
    for pos in positions:
        position_data.append({
            'title': pos.title,
            'employee_count': len(pos.employees)
        })
    
    # Статистика по отпускам
    vacation_stats = {
        'paid': len([v for v in vacations if v.type == 'paid']),
        'unpaid': len([v for v in vacations if v.type == 'unpaid']),
        'sick': len([v for v in vacations if v.type == 'sick'])
    }
    
    # Тренды найма
    hire_dates = [emp.hire_date for emp in employees]
    df = pd.DataFrame({'hire_date': hire_dates})
    df['month_year'] = df['hire_date'].apply(lambda x: x.strftime('%Y-%m'))
    monthly_hires = df.groupby('month_year').size().reset_index(name='count')
    
    return {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'dismissed_employees': dismissed_employees,
        'department_stats': dept_data,
        'position_stats': position_data,
        'vacation_stats': vacation_stats,
        'monthly_hires': monthly_hires.to_dict('records')
    }

def create_interactive_charts(interactive_data):
    """Создание интерактивных графиков с помощью Plotly"""
    charts = {}
    
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
    
    return charts