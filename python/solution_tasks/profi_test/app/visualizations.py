# -*- coding: utf-8 -*-
"""
Модуль визуализации данных для ПрофиТест
Предоставляет интерактивные диаграммы и визуализации для данных пользователей и аналитики
"""
import plotly.graph_objs as go
import plotly.offline as pyo
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from app import db
from app.models import User, TestResult, CareerGoal, LearningPath
import json
from collections import defaultdict


class DataVisualizer:
    """
    Визуализатор данных для системы ПрофиТест.
    Создает интерактивные диаграммы и визуализации для анализа данных пользователей.
    """
    def __init__(self):
        self.template = 'plotly_white'
    
    def create_user_progress_timeline(self, user_id):
        """
        Создает временную шкалу завершения тестов и достижения целей пользователя
        """
        try:
            # Get user's test results
            test_results = TestResult.query.filter_by(user_id=user_id).order_by(TestResult.created_at).all()
            
            if not test_results:
                return None
            
            dates = [result.created_at for result in test_results]
            methodologies = [result.methodology for result in test_results]
            
            fig = go.Figure()
            
            # Add test completions
            fig.add_trace(go.Scatter(
                x=dates,
                y=[1]*len(dates),
                mode='markers',
                marker=dict(size=15, color='blue', symbol='circle'),
                text=methodologies,
                hovertemplate='<b>Test Completed</b><br>Method: %{text}<br>Date: %{x}<extra></extra>',
                name='Tests'
            ))
            
            # Get user's career goals
            goals = CareerGoal.query.filter_by(user_id=user_id).all()
            if goals:
                goal_dates = []
                goal_titles = []
                
                for goal in goals:
                    if goal.created_at:
                        goal_dates.append(goal.created_at)
                        goal_titles.append(goal.title)
                
                if goal_dates:
                    fig.add_trace(go.Scatter(
                        x=goal_dates,
                        y=[2]*len(goal_dates),
                        mode='markers',
                        marker=dict(size=15, color='green', symbol='diamond'),
                        text=goal_titles,
                        hovertemplate='<b>Career Goal Set</b><br>Title: %{text}<br>Date: %{x}<extra></extra>',
                        name='Goals'
                    ))
            
            # Get user's learning paths
            paths = LearningPath.query.filter_by(user_id=user_id).all()
            if paths:
                path_dates = []
                path_titles = []
                
                for path in paths:
                    if path.created_at:
                        path_dates.append(path.created_at)
                        path_titles.append(path.title)
                
                if path_dates:
                    fig.add_trace(go.Scatter(
                        x=path_dates,
                        y=[3]*len(path_dates),
                        mode='markers',
                        marker=dict(size=15, color='orange', symbol='square'),
                        text=path_titles,
                        hovertemplate='<b>Learning Path Created</b><br>Title: %{text}<br>Date: %{x}<extra></extra>',
                        name='Learning Paths'
                    ))
            
            fig.update_layout(
                title='User Activity Timeline',
                xaxis_title='Date',
                yaxis_title='Activity Type',
                yaxis=dict(
                    tickmode='array',
                    tickvals=[1, 2, 3],
                    ticktext=['Tests', 'Goals', 'Learning Paths']
                ),
                template=self.template,
                height=500
            )
            
            return pyo.plot(fig, output_type='div', include_plotlyjs=False)
        except Exception as e:
            print(f"Error creating progress timeline: {str(e)}")
            return None
    
    def create_test_results_comparison(self, user_id):
        """
        Create a comparison chart of user's test results
        """
        try:
            test_results = TestResult.query.filter_by(user_id=user_id).all()
            
            if len(test_results) < 2:
                return None
            
            # Prepare data for comparison
            result_data = []
            for result in test_results:
                if result.results:
                    try:
                        data = json.loads(result.results)
                        if 'scores' in data:
                            result_data.append({
                                'date': result.created_at.strftime('%Y-%m-%d'),
                                'methodology': result.methodology,
                                'scores': data['scores'],
                                'id': result.id
                            })
                    except json.JSONDecodeError:
                        continue
            
            if not result_data:
                return None
            
            # Create grouped bar chart
            fig = go.Figure()
            
            # Get all categories from all tests
            all_categories = set()
            for data in result_data:
                all_categories.update(data['scores'].keys())
            
            all_categories = sorted(list(all_categories))
            
            for i, test_data in enumerate(result_data):
                scores = [test_data['scores'].get(cat, 0) for cat in all_categories]
                fig.add_trace(go.Bar(
                    name=f"{test_data['methodology']} ({test_data['date']})",
                    x=all_categories,
                    y=scores
                ))
            
            fig.update_layout(
                title='Comparison of Test Results Over Time',
                xaxis_title='Professional Categories',
                yaxis_title='Score',
                barmode='group',
                template=self.template,
                height=600
            )
            
            return pyo.plot(fig, output_type='div', include_plotlyjs=False)
        except Exception as e:
            print(f"Error creating test results comparison: {str(e)}")
            return None
    
    def create_user_engagement_heatmap(self):
        """
        Create a heatmap showing user engagement by day of week and hour
        """
        try:
            # Get all test results
            all_results = TestResult.query.all()
            
            if not all_results:
                return None
            
            # Create a matrix for day of week vs hour
            heatmap_data = np.zeros((24, 7))  # 24 hours x 7 days
            
            for result in all_results:
                hour = result.created_at.hour
                day_of_week = result.created_at.weekday()  # Monday is 0
                heatmap_data[hour][day_of_week] += 1
            
            # Create heatmap
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            hours = [f'{i}:00' for i in range(24)]
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data,
                x=days,
                y=hours,
                colorscale='Viridis',
                hoverongaps=False
            ))
            
            fig.update_layout(
                title='User Engagement Heatmap (Hour vs Day)',
                xaxis_title='Day of Week',
                yaxis_title='Hour of Day',
                template=self.template,
                height=700
            )
            
            return pyo.plot(fig, output_type='div', include_plotlyjs=False)
        except Exception as e:
            print(f"Error creating engagement heatmap: {str(e)}")
            return None
    
    def create_career_goals_progress(self, user_id):
        """
        Create a progress visualization for career goals
        """
        try:
            goals = CareerGoal.query.filter_by(user_id=user_id).all()
            
            if not goals:
                return None
            
            statuses = [goal.current_status for goal in goals]
            priorities = [goal.priority for goal in goals]
            titles = [goal.title[:20] + ('...' if len(goal.title) > 20 else '') for goal in goals]
            
            # Create horizontal bar chart
            fig = go.Figure()
            
            # Color code by status
            status_colors = {
                'planning': '#FFA500',  # Orange
                'in_progress': '#00CED1',  # Dark Turquoise
                'achieved': '#32CD32',  # Lime Green
                'paused': '#DCDCDC'  # Light Gray
            }
            
            colors = [status_colors.get(status, '#808080') for status in statuses]
            
            fig.add_trace(go.Bar(
                x=priorities,
                y=titles,
                orientation='h',
                marker_color=colors,
                text=statuses,
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>Status: %{text}<br>Priority: %{x}<extra></extra>'
            ))
            
            fig.update_layout(
                title='Career Goals Progress & Priority',
                xaxis_title='Priority Level (1-5)',
                yaxis_title='Goal Title',
                template=self.template,
                height=max(400, len(goals) * 50)  # Adjust height based on number of goals
            )
            
            return pyo.plot(fig, output_type='div', include_plotlyjs=False)
        except Exception as e:
            print(f"Error creating career goals progress: {str(e)}")
            return None
    
    def create_methodology_comparison(self):
        """
        Create a comparison of different test methodologies across all users
        """
        try:
            # Get all test results
            all_results = TestResult.query.all()
            
            if not all_results:
                return None
            
            # Group by methodology
            methodology_data = defaultdict(list)
            
            for result in all_results:
                if result.results:
                    try:
                        data = json.loads(result.results)
                        if 'scores' in data:
                            methodology_data[result.methodology].append(data['scores'])
                    except json.JSONDecodeError:
                        continue
            
            if not methodology_data:
                return None
            
            # Calculate average scores for each methodology
            avg_scores = {}
            for method, results in methodology_data.items():
                if results:
                    # Combine all scores for this methodology
                    all_scores = defaultdict(float)
                    counts = defaultdict(int)
                    
                    for result_scores in results:
                        for category, score in result_scores.items():
                            all_scores[category] += score
                            counts[category] += 1
                    
                    # Calculate averages
                    avg_scores[method] = {cat: all_scores[cat]/counts[cat] for cat in all_scores}
            
            if not avg_scores:
                return None
            
            # Create grouped bar chart
            fig = go.Figure()
            
            # Get all categories
            all_categories = set()
            for scores in avg_scores.values():
                all_categories.update(scores.keys())
            
            all_categories = sorted(list(all_categories))
            
            for method, scores in avg_scores.items():
                avg_values = [scores.get(cat, 0) for cat in all_categories]
                fig.add_trace(go.Bar(
                    name=method,
                    x=all_categories,
                    y=avg_values
                ))
            
            fig.update_layout(
                title='Average Scores by Methodology',
                xaxis_title='Professional Categories',
                yaxis_title='Average Score',
                barmode='group',
                template=self.template,
                height=600
            )
            
            return pyo.plot(fig, output_type='div', include_plotlyjs=False)
        except Exception as e:
            print(f"Error creating methodology comparison: {str(e)}")
            return None
    
    def create_learning_paths_progress(self, user_id):
        """
        Create a visualization of learning path progress
        """
        try:
            paths = LearningPath.query.filter_by(user_id=user_id).all()
            
            if not paths:
                return None
            
            statuses = [path.status for path in paths]
            difficulties = [path.difficulty_level for path in paths]
            titles = [path.title[:20] + ('...' if len(path.title) > 20 else '') for path in paths]
            durations = [path.duration_weeks or 0 for path in paths]
            
            # Create scatter plot
            difficulty_map = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
            difficulty_nums = [difficulty_map.get(diff, 1) for diff in difficulties]
            
            fig = go.Figure()
            
            # Color code by status
            status_colors = {
                'not_started': '#FF6B6B',  # Red
                'in_progress': '#4ECDC4',  # Teal
                'completed': '#45B7D1',   # Blue
                'archived': '#96CEB4'     # Green
            }
            
            colors = [status_colors.get(status, '#808080') for status in statuses]
            
            fig.add_trace(go.Scatter(
                x=durations,
                y=difficulty_nums,
                mode='markers',
                marker=dict(
                    size=15,
                    color=colors,
                    sizemode='diameter'
                ),
                text=titles,
                hovertemplate='<b>%{text}</b><br>Duration: %{x} weeks<br>Difficulty: %{y}<br>Status: ' + 
                             '<br>'.join(statuses) + '<extra></extra>',
                name='Learning Paths'
            ))
            
            fig.update_layout(
                title='Learning Paths Overview (Duration vs Difficulty)',
                xaxis_title='Duration (weeks)',
                yaxis_title='Difficulty Level',
                yaxis=dict(
                    tickmode='array',
                    tickvals=[1, 2, 3],
                    ticktext=['Beginner', 'Intermediate', 'Advanced']
                ),
                template=self.template,
                height=500
            )
            
            return pyo.plot(fig, output_type='div', include_plotlyjs=False)
        except Exception as e:
            print(f"Error creating learning paths progress: {str(e)}")
            return None
    
    def generate_user_dashboard_charts(self, user_id):
        """
        Generate all relevant charts for a user's dashboard
        """
        try:
            charts = {}
            
            # Individual user charts
            charts['progress_timeline'] = self.create_user_progress_timeline(user_id)
            charts['test_comparison'] = self.create_test_results_comparison(user_id)
            charts['goals_progress'] = self.create_career_goals_progress(user_id)
            charts['learning_paths'] = self.create_learning_paths_progress(user_id)
            
            # System-wide charts (only for admins or if specifically requested)
            # charts['engagement_heatmap'] = self.create_user_engagement_heatmap()
            # charts['methodology_comparison'] = self.create_methodology_comparison()
            
            return charts
        except Exception as e:
            print(f"Error generating user dashboard charts: {str(e)}")
            return {}


# Global instance
visualizer = DataVisualizer()