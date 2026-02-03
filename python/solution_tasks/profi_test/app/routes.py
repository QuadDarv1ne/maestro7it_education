# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app.models import TestResult

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Маршрут главной страницы"""
    return render_template('index.html')

@main.route('/about')
def about():
    """Маршрут страницы о нас"""
    return render_template('about.html')

@main.route('/profile')
@login_required
def profile():
    """Маршрут профиля пользователя"""
    test_results = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.created_at.desc()).all()
    return render_template('profile.html', test_results=test_results)