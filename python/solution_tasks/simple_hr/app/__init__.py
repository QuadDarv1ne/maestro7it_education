    # Регистрация blueprint'ов
    try:
        from app.routes.auth import bp as auth_bp
        app.register_blueprint(auth_bp)
        
        from app.routes.main import bp as main_bp
        app.register_blueprint(main_bp)
        
        from app.routes.employees import bp as employees_bp
        app.register_blueprint(employees_bp, url_prefix='/employees')
        
        from app.routes.departments import bp as departments_bp
        app.register_blueprint(departments_bp, url_prefix='/departments')
        
        from app.routes.positions import bp as positions_bp
        app.register_blueprint(positions_bp, url_prefix='/positions')
        
        from app.routes.orders import bp as orders_bp
        app.register_blueprint(orders_bp, url_prefix='/orders')
        
        from app.routes.vacations import bp as vacations_bp
        app.register_blueprint(vacations_bp, url_prefix='/vacations')
        
        from app.routes.reports import bp as reports_bp
        app.register_blueprint(reports_bp, url_prefix='/reports')
        
        from app.routes.analytics import bp as analytics_bp
        app.register_blueprint(analytics_bp, url_prefix='/analytics')
        
        from app.routes.notifications import bp as notifications_bp
        app.register_blueprint(notifications_bp, url_prefix='/notifications')
        
        from app.routes.admin import bp as admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')
        
        from app.routes.audit import bp as audit_bp
        app.register_blueprint(audit_bp, url_prefix='/audit')
        
        # Two-Factor Authentication (temporarily disabled - missing qrcode module)
        # from app.routes.two_factor import bp as two_factor_bp
        # app.register_blueprint(two_factor_bp)
        
        # Advanced Search
        from app.routes.search import bp as search_bp
        app.register_blueprint(search_bp)
        
        # Dashboard with Charts
        from app.routes.dashboard import bp as dashboard_bp
        app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
        
        # REST API endpoints
        from app.routes.api import bp as api_bp
        app.register_blueprint(api_bp)
        
        # REST API v1 endpoints
        from app.routes.api_v1 import bp as api_v1_bp
        app.register_blueprint(api_v1_bp)
        
        # Health check endpoints
        from app.routes.health import health_bp
        app.register_blueprint(health_bp)