from flask import Blueprint, render_template, jsonify
from app.models.tournament import Tournament

api_docs_bp = Blueprint('api_docs', __name__, url_prefix='/api/docs')

@api_docs_bp.route('/')
def swagger_ui():
    """Страница документации API (Swagger UI)"""
    return render_template('api_docs/swagger.html')

@api_docs_bp.route('/spec')
def swagger_spec():
    """Спецификация OpenAPI 3.0"""
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "ChessCalendar-RU API",
            "description": "API для получения информации о шахматных турнирах в России",
            "version": "1.0.0",
            "contact": {
                "name": "Дуплей Максим Игоревич",
                "email": "quadd4rv1n7@gmail.com"
            }
        },
        "servers": [
            {
                "url": "http://127.0.0.1:5000",
                "description": "Локальный сервер разработки"
            }
        ],
        "paths": {
            "/api/tournaments": {
                "get": {
                    "summary": "Получить все турниры",
                    "description": "Возвращает список всех шахматных турниров в России",
                    "responses": {
                        "200": {
                            "description": "Успешный ответ",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Tournament"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/tournaments/{id}": {
                "get": {
                    "summary": "Получить турнир по ID",
                    "description": "Возвращает информацию о конкретном турнире",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "integer"
                            },
                            "description": "ID турнира"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Успешный ответ",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Tournament"
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Турнир не найден"
                        }
                    }
                }
            },
            "/api/tournaments/filter": {
                "get": {
                    "summary": "Получить отфильтрованные турниры",
                    "description": "Возвращает турниры с применением фильтров",
                    "parameters": [
                        {
                            "name": "category",
                            "in": "query",
                            "required": False,
                            "schema": {
                                "type": "string",
                                "enum": ["FIDE", "National", "Youth", "Seniors"]
                            },
                            "description": "Категория турнира"
                        },
                        {
                            "name": "status",
                            "in": "query",
                            "required": False,
                            "schema": {
                                "type": "string",
                                "enum": ["Scheduled", "Ongoing", "Completed"]
                            },
                            "description": "Статус турнира"
                        },
                        {
                            "name": "location",
                            "in": "query",
                            "required": False,
                            "schema": {
                                "type": "string"
                            },
                            "description": "Место проведения (частичное совпадение)"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Успешный ответ",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Tournament"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/recommendations/user/{user_id}": {
                "get": {
                    "summary": "Получить рекомендации для пользователя",
                    "description": "Возвращает персонализированные рекомендации турниров для конкретного пользователя",
                    "parameters": [
                        {
                            "name": "user_id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "integer"
                            },
                            "description": "ID пользователя"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Успешный ответ",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Tournament"
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Пользователь не найден"
                        }
                    }
                }
            },
            "/api/analytics/report": {
                "get": {
                    "summary": "Получить полный отчет аналитики",
                    "description": "Возвращает комплексный отчет по аналитике приложения",
                    "responses": {
                        "200": {
                            "description": "Успешный ответ",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/AnalyticsReport"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/analytics/tournament/{tournament_id}": {
                "get": {
                    "summary": "Получить аналитику по турниру",
                    "description": "Возвращает детальную аналитику для конкретного турнира",
                    "parameters": [
                        {
                            "name": "tournament_id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "integer"
                            },
                            "description": "ID турнира"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Успешный ответ",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TournamentAnalytics"
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Турнир не найден"
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "Tournament": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "description": "Уникальный идентификатор турнира"
                        },
                        "name": {
                            "type": "string",
                            "description": "Название турнира"
                        },
                        "start_date": {
                            "type": "string",
                            "format": "date",
                            "description": "Дата начала турнира"
                        },
                        "end_date": {
                            "type": "string",
                            "format": "date",
                            "description": "Дата окончания турнира"
                        },
                        "location": {
                            "type": "string",
                            "description": "Место проведения"
                        },
                        "category": {
                            "type": "string",
                            "enum": ["FIDE", "National", "Youth", "Seniors"],
                            "description": "Категория турнира"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["Scheduled", "Ongoing", "Completed"],
                            "description": "Статус турнира"
                        },
                        "fide_id": {
                            "type": "string",
                            "nullable": True,
                            "description": "FIDE ID турнира"
                        },
                        "source_url": {
                            "type": "string",
                            "nullable": True,
                            "description": "URL источника информации"
                        }
                    },
                    "required": ["id", "name", "start_date", "end_date", "location", "category", "status"]
                },
                "AnalyticsReport": {
                    "type": "object",
                    "properties": {
                        "generated_at": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Время генерации отчета"
                        },
                        "tournament_analytics": {
                            "type": "object",
                            "description": "Аналитика турниров"
                        },
                        "user_analytics": {
                            "type": "object",
                            "description": "Аналитика пользователей"
                        },
                        "interaction_analytics": {
                            "type": "object",
                            "description": "Аналитика взаимодействий"
                        }
                    }
                },
                "TournamentAnalytics": {
                    "type": "object",
                    "properties": {
                        "tournament": {
                            "$ref": "#/components/schemas/Tournament"
                        },
                        "total_interactions": {
                            "type": "integer",
                            "description": "Общее количество взаимодействий"
                        },
                        "total_ratings": {
                            "type": "integer",
                            "description": "Общее количество рейтингов"
                        },
                        "average_rating": {
                            "type": "number",
                            "format": "float",
                            "description": "Средний рейтинг"
                        },
                        "engagement_score": {
                            "type": "integer",
                            "description": "Оценка вовлеченности"
                        }
                    }
                }
            }
        }
    }
    
    return jsonify(spec)


@api_docs_bp.route('/health')
def health_check():
    """Проверка состояния системы"""
    from app.utils.monitoring import health_checker
    return jsonify(health_checker.run_health_checks())


@api_docs_bp.route('/metrics')
def metrics():
    """Получить метрики производительности"""
    from app.utils.monitoring import performance_monitor
    return jsonify(performance_monitor.get_metrics_summary())


@api_docs_bp.route('/system-info')
def system_info():
    """Получить информацию о системе"""
    import platform
    import psutil
    import os
    from datetime import datetime
    
    system_data = {
        "server": {
            "name": platform.node(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "architecture": platform.architecture()[0],
        },
        "runtime": {
            "python_version": platform.python_version(),
            "python_compiler": platform.python_compiler(),
        },
        "process": {
            "pid": os.getpid(),
            "cwd": os.getcwd(),
            "memory_percent": psutil.Process().memory_percent(),
        },
        "system": {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent if hasattr(os, 'statvfs') else 'N/A',
        },
        "timestamp": datetime.now().isoformat(),
        "status": "running"
    }
    return jsonify(system_data)