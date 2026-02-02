from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models import User, TestResult, CareerGoal, LearningPath, CalendarEvent, PortfolioProject
from datetime import datetime, timedelta
import json
import os

portfolio_bp = Blueprint('portfolio', __name__)

class PortfolioProject(db.Model):
    # Модель для проектов в портфолио пользователя
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    technologies = db.Column(db.Text)  # JSON string of technologies used
    github_url = db.Column(db.String(500))
    demo_url = db.Column(db.String(500))
    project_type = db.Column(db.String(50), default='personal')  # personal, freelance, work
    status = db.Column(db.String(20), default='in_progress')  # planning, in_progress, completed, archived
    start_date = db.Column(db.Date)
    completion_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='portfolio_projects')
    
    def __repr__(self):
        return f'<PortfolioProject {self.title} for User {self.user_id}>'


@portfolio_bp.route('/portfolio')
@login_required
def portfolio_page():
    # Страница портфолио пользователя
    return render_template('portfolio/index.html')


@portfolio_bp.route('/api/portfolio/projects')
@login_required
def get_portfolio_projects():
    # Получение проектов портфолио пользователя
    projects = PortfolioProject.query.filter_by(user_id=current_user.id).order_by(
        PortfolioProject.created_at.desc()
    ).all()
    
    projects_list = []
    for project in projects:
        try:
            technologies = json.loads(project.technologies) if project.technologies else []
        except:
            technologies = []
        
        projects_list.append({
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'technologies': technologies,
            'githubUrl': project.github_url,
            'demoUrl': project.demo_url,
            'projectType': project.project_type,
            'status': project.status,
            'startDate': project.start_date.isoformat() if project.start_date else None,
            'completionDate': project.completion_date.isoformat() if project.completion_date else None,
            'createdAt': project.created_at.isoformat()
        })
    
    return jsonify(projects_list)


@portfolio_bp.route('/api/portfolio/projects', methods=['POST'])
@login_required
def create_portfolio_project():
    # Создание нового проекта в портфолио
    data = request.get_json()
    
    title = data.get('title', '')
    description = data.get('description', '')
    technologies = data.get('technologies', [])
    github_url = data.get('githubUrl', '')
    demo_url = data.get('demoUrl', '')
    project_type = data.get('projectType', 'personal')
    status = data.get('status', 'planning')
    start_date_str = data.get('startDate')
    completion_date_str = data.get('completionDate')
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    # Validate project type
    valid_types = ['personal', 'freelance', 'work']
    if project_type not in valid_types:
        return jsonify({'error': f'Project type must be one of: {", ".join(valid_types)}'}), 400
    
    # Validate status
    valid_statuses = ['planning', 'in_progress', 'completed', 'archived']
    if status not in valid_statuses:
        return jsonify({'error': f'Status must be one of: {", ".join(valid_statuses)}'}), 400
    
    # Parse dates
    start_date = None
    completion_date = None
    if start_date_str:
        try:
            start_date = datetime.fromisoformat(start_date_str).date()
        except ValueError:
            return jsonify({'error': 'Invalid start date format'}), 400
    
    if completion_date_str:
        try:
            completion_date = datetime.fromisoformat(completion_date_str).date()
        except ValueError:
            return jsonify({'error': 'Invalid completion date format'}), 400
    
    project = PortfolioProject(
        user_id=current_user.id,
        title=title,
        description=description,
        technologies=json.dumps(technologies),
        github_url=github_url,
        demo_url=demo_url,
        project_type=project_type,
        status=status,
        start_date=start_date,
        completion_date=completion_date
    )
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Проект успешно добавлен в портфолио',
        'projectId': project.id
    })


@portfolio_bp.route('/api/portfolio/projects/<int:project_id>', methods=['PUT', 'DELETE'])
@login_required
def manage_portfolio_project(project_id):
    # Редактирование или удаление проекта из портфолио
    project = PortfolioProject.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'PUT':
        data = request.get_json()
        
        project.title = data.get('title', project.title)
        project.description = data.get('description', project.description)
        
        if 'technologies' in data:
            project.technologies = json.dumps(data['technologies'])
        
        project.github_url = data.get('githubUrl', project.github_url)
        project.demo_url = data.get('demoUrl', project.demo_url)
        project.project_type = data.get('projectType', project.project_type)
        project.status = data.get('status', project.status)
        
        if 'startDate' in data:
            if data['startDate']:
                try:
                    project.start_date = datetime.fromisoformat(data['startDate']).date()
                except ValueError:
                    return jsonify({'error': 'Invalid start date format'}), 400
            else:
                project.start_date = None
        
        if 'completionDate' in data:
            if data['completionDate']:
                try:
                    project.completion_date = datetime.fromisoformat(data['completionDate']).date()
                except ValueError:
                    return jsonify({'error': 'Invalid completion date format'}), 400
            else:
                project.completion_date = None
        
        project.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Проект успешно обновлен'
        })
    
    elif request.method == 'DELETE':
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Проект успешно удален из портфолио'
        })


@portfolio_bp.route('/api/portfolio/generate')
@login_required
def generate_portfolio():
    # Генерация автоматического портфолио на основе результатов тестов и достижений
    # Получаем результаты тестов пользователя
    test_results = TestResult.query.filter_by(user_id=current_user.id).order_by(
        TestResult.created_at.desc()
    ).limit(5).all()
    
    # Получаем карьерные цели
    career_goals = CareerGoal.query.filter_by(
        user_id=current_user.id,
        current_status='achieved'
    ).all()
    
    # Получаем завершенные проекты
    completed_projects = PortfolioProject.query.filter_by(
        user_id=current_user.id,
        status='completed'
    ).all()
    
    # Получаем завершенные образовательные траектории
    completed_paths = LearningPath.query.filter_by(
        user_id=current_user.id,
        status='completed'
    ).all()
    
    # Генерируем содержание портфолио
    portfolio_content = {
        'user_info': {
            'username': current_user.username,
            'email': current_user.email,
            'registration_date': current_user.created_at.isoformat()
        },
        'test_results_summary': [],
        'achieved_goals': [],
        'completed_projects': [],
        'completed_learning_paths': [],
        'skills_summary': {},
        'generated_at': datetime.utcnow().isoformat()
    }
    
    # Обрабатываем результаты тестов
    for result in test_results:
        try:
            results_dict = json.loads(result.results) if result.results else {}
            portfolio_content['test_results_summary'].append({
                'methodology': result.methodology,
                'dominant_category': results_dict.get('dominant_category', 'Не определено'),
                'date': result.created_at.isoformat(),
                'recommendation': result.recommendation[:200] + '...' if result.recommendation else ''
            })
        except:
            continue
    
    # Обрабатываем достигнутые цели
    for goal in career_goals:
        portfolio_content['achieved_goals'].append({
            'title': goal.title,
            'description': goal.description,
            'achievement_date': goal.updated_at.isoformat(),
            'priority': goal.priority
        })
    
    # Обрабатываем завершенные проекты
    for project in completed_projects:
        try:
            technologies = json.loads(project.technologies) if project.technologies else []
        except:
            technologies = []
        
        portfolio_content['completed_projects'].append({
            'title': project.title,
            'description': project.description,
            'technologies': technologies,
            'github_url': project.github_url,
            'demo_url': project.demo_url,
            'completion_date': project.completion_date.isoformat() if project.completion_date else project.updated_at.isoformat()
        })
    
    # Обрабатываем завершенные траектории обучения
    for path in completed_paths:
        portfolio_content['completed_learning_paths'].append({
            'title': path.title,
            'description': path.description,
            'duration_weeks': path.duration_weeks,
            'difficulty_level': path.difficulty_level,
            'completion_date': path.completed_at.isoformat() if path.completed_at else path.updated_at.isoformat()
        })
    
    # Генерируем сводку навыков на основе результатов тестов
    skills_summary = {}
    for result in test_results:
        try:
            results_dict = json.loads(result.results) if result.results else {}
            scores = results_dict.get('scores', {})
            for category, score in scores.items():
                if category not in skills_summary:
                    skills_summary[category] = {'total_score': 0, 'count': 0}
                skills_summary[category]['total_score'] += float(score)
                skills_summary[category]['count'] += 1
        except:
            continue
    
    # Вычисляем средние значения
    for category, data in skills_summary.items():
        if data['count'] > 0:
            portfolio_content['skills_summary'][category] = round(data['total_score'] / data['count'], 2)
    
    # Создаем HTML-файл портфолио
    html_content = generate_portfolio_html(portfolio_content)
    
    # Сохраняем файл
    portfolio_dir = os.path.join('app', 'static', 'portfolios')
    os.makedirs(portfolio_dir, exist_ok=True)
    
    filename = f"portfolio_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(portfolio_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Возвращаем ссылку на портфолио
    portfolio_url = f"/static/portfolios/{filename}"
    
    return jsonify({
        'success': True,
        'message': 'Портфолио успешно сгенерировано',
        'portfolio_url': portfolio_url,
        'portfolio_data': portfolio_content
    })


def generate_portfolio_html(portfolio_data):
    # Генерация HTML для портфолио
    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Портфолио {portfolio_data['user_info']['username']}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
            .header-section {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem 0; }}
            .section-title {{ border-bottom: 3px solid #667eea; padding-bottom: 10px; margin-bottom: 20px; }}
            .skill-badge {{ background: #667eea; color: white; padding: 5px 15px; border-radius: 20px; margin: 5px; display: inline-block; }}
            .project-card {{ transition: transform 0.3s; border: 1px solid #e0e0e0; }}
            .project-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
            .timeline-item {{ position: relative; padding-left: 30px; margin-bottom: 30px; }}
            .timeline-item:before {{ content: ''; position: absolute; left: 0; top: 5px; width: 12px; height: 12px; border-radius: 50%; background: #667eea; }}
            .timeline-item:after {{ content: ''; position: absolute; left: 5px; top: 17px; bottom: -20px; width: 2px; background: #e0e0e0; }}
            .timeline-item:last-child:after {{ display: none; }}
        </style>
    </head>
    <body>
        <!-- Header -->
        <div class="header-section text-center">
            <div class="container">
                <h1><i class="fas fa-user"></i> {portfolio_data['user_info']['username']}</h1>
                <p class="lead">Профессиональное портфолио</p>
                <p>Сгенерировано: {datetime.fromisoformat(portfolio_data['generated_at']).strftime('%d.%m.%Y %H:%M')}</p>
            </div>
        </div>
        
        <div class="container my-5">
            <!-- Skills Summary -->
            <section class="mb-5">
                <h2 class="section-title">Ключевые навыки</h2>
                <div class="row">
    """
    
    # Добавляем навыки
    for skill, score in portfolio_data['skills_summary'].items():
        html += f"""
                    <div class="col-md-3 mb-3">
                        <div class="skill-badge">
                            <i class="fas fa-star"></i> {skill}: {score}
                        </div>
                    </div>
        """
    
    html += """
                </div>
            </section>
            
            <!-- Test Results -->
            <section class="mb-5">
                <h2 class="section-title">Результаты профориентации</h2>
    """
    
    for result in portfolio_data['test_results_summary']:
        html += f"""
                <div class="card mb-3">
                    <div class="card-body">
                        <h5 class="card-title">{result['methodology'].title()} методика</h5>
                        <p class="card-text"><strong>Основная сфера:</strong> {result['dominant_category']}</p>
                        <p class="card-text"><strong>Рекомендация:</strong> {result['recommendation']}</p>
                        <small class="text-muted">Дата: {datetime.fromisoformat(result['date']).strftime('%d.%m.%Y')}</small>
                    </div>
                </div>
        """
    
    html += """
            </section>
            
            <!-- Achieved Goals -->
            <section class="mb-5">
                <h2 class="section-title">Достигнутые цели</h2>
                <div class="timeline">
    """
    
    for goal in portfolio_data['achieved_goals']:
        html += f"""
                    <div class="timeline-item">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">{goal['title']}</h5>
                                <p class="card-text">{goal['description']}</p>
                                <div class="d-flex justify-content-between">
                                    <span class="badge bg-success">Достигнуто</span>
                                    <small class="text-muted">Приоритет: {goal['priority']}</small>
                                </div>
                                <small class="text-muted">Дата достижения: {datetime.fromisoformat(goal['achievement_date']).strftime('%d.%m.%Y')}</small>
                            </div>
                        </div>
                    </div>
        """
    
    html += """
                </div>
            </section>
            
            <!-- Completed Projects -->
            <section class="mb-5">
                <h2 class="section-title">Завершенные проекты</h2>
                <div class="row">
    """
    
    for project in portfolio_data['completed_projects']:
        html += f"""
                    <div class="col-md-6 mb-4">
                        <div class="card project-card h-100">
                            <div class="card-body">
                                <h5 class="card-title">{project['title']}</h5>
                                <p class="card-text">{project['description']}</p>
    """
        
        if project['technologies']:
            html += '<p><strong>Технологии:</strong> '
            for tech in project['technologies'][:5]:  # Ограничиваем 5 технологиями
                html += f'<span class="badge bg-secondary me-1">{tech}</span>'
            html += '</p>'
        
        html += f"""
                                <div class="mt-3">
        """
        
        if project['github_url']:
            html += f'<a href="{project["github_url"]}" class="btn btn-outline-dark btn-sm me-2" target="_blank"><i class="fab fa-github"></i> GitHub</a>'
        
        if project['demo_url']:
            html += f'<a href="{project["demo_url"]}" class="btn btn-outline-primary btn-sm" target="_blank"><i class="fas fa-external-link-alt"></i> Демо</a>'
        
        html += f"""
                                </div>
                                <small class="text-muted">Завершен: {datetime.fromisoformat(project['completion_date']).strftime('%d.%m.%Y')}</small>
                            </div>
                        </div>
                    </div>
        """
    
    html += """
                </div>
            </section>
            
            <!-- Completed Learning Paths -->
            <section class="mb-5">
                <h2 class="section-title">Пройденные образовательные траектории</h2>
    """
    
    for path in portfolio_data['completed_learning_paths']:
        html += f"""
                <div class="card mb-3">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <h5 class="card-title">{path['title']}</h5>
                            <span class="badge bg-info">{path['difficulty_level'].title()}</span>
                        </div>
                        <p class="card-text">{path['description']}</p>
                        <div class="d-flex justify-content-between">
                            <small class="text-muted">Продолжительность: {path['duration_weeks']} недель</small>
                            <small class="text-muted">Завершено: {datetime.fromisoformat(path['completion_date']).strftime('%d.%m.%Y')}</small>
                        </div>
                    </div>
                </div>
        """
    
    html += """
            </section>
        </div>
        
        <footer class="bg-dark text-white text-center py-3">
            <div class="container">
                <p>Портфолио сгенерировано автоматически системой профориентации Maestro7IT</p>
                <p><small>© 2024 Maestro7IT - Dupley Maxim Igorevich</small></p>
            </div>
        </footer>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    
    return html