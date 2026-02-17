#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Health Check endpoints
"""

from flask import Blueprint, jsonify, request
from app.utils.unified_monitoring import health_checker
import logging

logger = logging.getLogger('chess_calendar')

health_bp = Blueprint('health', __name__, url_prefix='/health')


@health_bp.route('/', methods=['GET'])
@health_bp.route('', methods=['GET'])
def health_check():
    """Простая проверка здоровья приложения"""
    try:
        result = health_checker.check_all()
        status_code = 200 if result['status'] == 'healthy' else 503
        return jsonify(result), status_code
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 503


@health_bp.route('/detailed', methods=['GET'])
def health_check_detailed():
    """Подробная проверка здоровья приложения"""
    try:
        result = health_checker.check_all()
        status_code = 200 if result['status'] in ['healthy', 'degraded'] else 503
        return jsonify(result), status_code
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 503


@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """Проверка готовности приложения (для Kubernetes)"""
    try:
        result = health_checker.check_database()
        if result['healthy']:
            return jsonify({'ready': True}), 200
        return jsonify({'ready': False, 'details': result}), 503
    except Exception as e:
        return jsonify({'ready': False, 'error': str(e)}), 503


@health_bp.route('/live', methods=['GET'])
def liveness_check():
    """Проверка живости приложения (для Kubernetes)"""
    return jsonify({'alive': True}), 200


@health_bp.route('/startup', methods=['GET'])
def startup_check():
    """Проверка запуска приложения (для Kubernetes)"""
    try:
        result = health_checker.check_all()
        if result['status'] in ['healthy', 'degraded']:
            return jsonify({'started': True}), 200
        return jsonify({'started': False, 'details': result}), 503
    except Exception as e:
        return jsonify({'started': False, 'error': str(e)}), 503
