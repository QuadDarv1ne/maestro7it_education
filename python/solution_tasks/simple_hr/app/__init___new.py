"""
Flask application factory and initialization module.

This module contains the Flask app factory and initialization of all extensions,
blueprints registration, and middleware setup.
"""

from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Any, Optional

from flask import Flask, Response
from flask_caching import Cache
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.pool import Pool

from instance.config import Config

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Flask extensions
db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()
login_manager: LoginManager = LoginManager()
limiter: Limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)
cache: Cache = Cache()

# SocketIO will be initialized later in create_app
socketio: Optional[Any] = None


def create_app(config_class: type = Config) -> Flask:
    """
    Create and configure the Flask application.

    This factory function creates a Flask application instance, configures
    all extensions, registers blueprints, and sets up middleware.

    Args:
        config_class: Configuration class for the application (default: Config).

    Returns:
        Configured Flask application instance.

    Raises:
        Exception: If there are errors during initialization (caught and logged).
    """
    global socketio
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Setup logging configuration
    _setup_logging(app)
    logger.info("Starting application initialization")

    # Configure database connection pooling for better performance
    _setup_database_pragmas()

    # Initialize Flask extensions
    _initialize_extensions(app)
    logger.info("Extensions initialized")

    # Setup CORS configuration
    _setup_cors(app)

    # Setup security headers
    _setup_security_headers(app)

    # Setup user loader for Flask-Login
    _setup_user_loader()

    # Register all application blueprints
    _register_blueprints(app)
    logger.info("Blueprints registered")

    # Setup application middleware
    _setup_middleware(app)

    # Initialize monitoring and optimization systems
    _initialize_monitoring(app)

    # Register CLI commands
    _register_cli_commands(app)

    logger.info("Application initialization completed successfully")
    return app


def _setup_logging(app: Flask) -> None:
    """
    Setup application logging configuration.

    Creates logs directory and configures rotating file handler for production.

    Args:
        app: Flask application instance.
    """
    if not app.debug and not app.testing:
        logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir, exist_ok=True)

        log_file = os.path.join(logs_dir, 'simple_hr.log')
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10240, backupCount=10
        )
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Simple HR startup')


def _setup_database_pragmas() -> None:
    """
    Configure database connection pooling for better performance.

    Sets SQLite pragma for foreign key support when using SQLite.
    """
    @event.listens_for(Pool, "connect")
    def set_sqlite_pragma(
        dbapi_connection: Any, connection_record: Any
    ) -> None:
        """Enable SQLite foreign key support."""
        try:
            if 'sqlite' in str(type(dbapi_connection)).lower():
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
        except Exception as e:
            logger.error(f"Error setting SQLite pragma: {str(e)}")


def _initialize_extensions(app: Flask) -> None:
    """
    Initialize Flask extensions with application context.

    Args:
        app: Flask application instance.
    """
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    limiter.init_app(app)
    cache.init_app(
        app,
        config={
            'CACHE_TYPE': 'SimpleCache',
            'CACHE_DEFAULT_TIMEOUT': 300,
        },
    )


def _setup_cors(app: Flask) -> None:
    """
    Setup CORS with secure parameters.

    Args:
        app: Flask application instance.
    """
    cors_origins = app.config.get('CORS_ORIGINS', ['http://localhost:5000'])
    CORS(
        app,
        resources={
            r"/*": {
                "origins": cors_origins,
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
            }
        },
    )


def _setup_security_headers(app: Flask) -> None:
    """
    Setup security headers for all responses.

    Args:
        app: Flask application instance.
    """
    @app.after_request
    def set_security_headers(response: Response) -> Response:
        """Add security headers to response."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = (
            'max-age=31536000; includeSubDomains'
        )
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; script-src 'self' 'unsafe-inline' "
            "https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' "
            "https://cdn.jsdelivr.net; img-src 'self' data: https:;"
        )
        return response


def _setup_user_loader() -> None:
    """Setup user loader for Flask-Login."""
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[UserMixin]:
        """
        Load user from database by ID.

        Args:
            user_id: User ID as string.

        Returns:
            User object or None if not found.
        """
        try:
            return User.query.get(int(user_id))
        except (ValueError, TypeError) as e:
            logger.debug(f"Invalid user ID format: {user_id}")
            return None
        except Exception as e:
            logger.error(f"Error loading user {user_id}: {str(e)}")
            return None


def _register_blueprints(app: Flask) -> None:
    """
    Register all application blueprints.

    Args:
        app: Flask application instance.
    """
    blueprints_config = [
        ('app.routes.auth', 'bp', None),
        ('app.routes.main', 'bp', None),
        ('app.routes.employees', 'bp', '/employees'),
        ('app.routes.departments', 'bp', '/departments'),
        ('app.routes.positions', 'bp', '/positions'),
        ('app.routes.orders', 'bp', '/orders'),
        ('app.routes.vacations', 'bp', '/vacations'),
        ('app.routes.reports', 'bp', '/reports'),
        ('app.routes.analytics', 'bp', '/analytics'),
        ('app.routes.notifications', 'bp', '/notifications'),
        ('app.routes.admin', 'bp', '/admin'),
        ('app.routes.audit', 'bp', '/audit'),
        ('app.routes.search', 'bp', None),
        ('app.routes.dashboard', 'bp', '/dashboard'),
        ('app.routes.profile', 'bp', '/profile'),
        ('app.routes.api', 'bp', None),
        ('app.routes.health', 'health_bp', None),
    ]

    for module_name, bp_name, url_prefix in blueprints_config:
        try:
            module = __import__(module_name, fromlist=[bp_name])
            bp = getattr(module, bp_name)
            if url_prefix:
                app.register_blueprint(bp, url_prefix=url_prefix)
            else:
                app.register_blueprint(bp)
            logger.debug(f"Registered blueprint: {module_name}.{bp_name}")
        except ImportError as e:
            logger.warning(f"Could not import blueprint {module_name}: {str(e)}")
        except AttributeError as e:
            logger.warning(
                f"Blueprint '{bp_name}' not found in {module_name}: {str(e)}"
            )
        except Exception as e:
            logger.error(
                f"Error registering blueprint {module_name}.{bp_name}: {str(e)}"
            )


def _setup_middleware(app: Flask) -> None:
    """
    Setup application middleware.

    Args:
        app: Flask application instance.
    """
    try:
        from app.middleware import setup_middleware

        setup_middleware(app)
        logger.info("Middleware setup completed")
    except ImportError:
        logger.debug("Middleware module not found")
    except Exception as e:
        logger.error(f"Error setting up middleware: {str(e)}")


def _initialize_monitoring(app: Flask) -> None:
    """
    Initialize monitoring and optimization systems.

    Args:
        app: Flask application instance.
    """
    # Initialize Redis cache
    try:
        from app.utils.redis_cache import cache as redis_cache

        redis_cache.init_app(app)
        logger.info("Redis cache initialized")
    except ImportError:
        logger.debug("Redis cache module not available")
    except Exception as e:
        logger.warning(f"Redis cache initialization: {str(e)}")

    # Initialize performance monitoring
    try:
        from app.utils.performance_monitoring import performance_monitor

        performance_monitor.init_app(app)
        logger.info("Performance monitoring initialized")
    except ImportError:
        logger.debug("Performance monitoring module not available")
    except Exception as e:
        logger.warning(f"Performance monitoring initialization: {str(e)}")

    # Initialize error handlers
    try:
        from app.utils.error_handlers import (
            init_error_handlers,
            register_api_error_handlers,
        )

        init_error_handlers(app)
        register_api_error_handlers(app)
        logger.info("Error handlers initialized")
    except ImportError:
        logger.debug("Error handlers module not available")
    except Exception as e:
        logger.warning(f"Error handlers initialization: {str(e)}")

    # Initialize scheduler (only for production)
    if not app.debug and not app.testing:
        try:
            from app.utils.scheduler import init_scheduler

            init_scheduler(app)
            logger.info("Task scheduler initialized")
        except ImportError:
            logger.debug("Scheduler module not available")
        except Exception as e:
            logger.warning(f"Task scheduler initialization: {str(e)}")


def _register_cli_commands(app: Flask) -> None:
    """
    Register CLI commands.

    Args:
        app: Flask application instance.
    """
    try:
        from app.cli import register_commands

        register_commands(app)
        logger.info("CLI commands registered")
    except ImportError:
        logger.debug("CLI module not available")
    except Exception as e:
        logger.debug(f"CLI commands registration: {str(e)}")
