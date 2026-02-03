"""
Enhanced Machine Learning Recommender System for Profi Test
This module implements advanced ML algorithms for personalized career recommendations
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import json
import pickle
from datetime import datetime
from app import db
from app.models import User, TestResult, CareerGoal, LearningPath
import logging


class EnhancedMLRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.scaler = StandardScaler()
        self.model_trained = False
        self.logger = logging.getLogger(__name__)
        
    def prepare_user_data(self):
        """
        Prepare user data for ML analysis
        """
        try:
            # Get all users with their test results
            users_data = []
            for user in User.query.all():
                user_features = {
                    'user_id': user.id,
                    'is_admin': user.is_admin,
                    'created_at_days': (datetime.utcnow() - user.created_at).days if user.created_at else 0
                }
                
                # Get user's test results
                test_results = TestResult.query.filter_by(user_id=user.id).all()
                if test_results:
                    latest_result = test_results[-1]  # Most recent result
                    try:
                        results_dict = json.loads(latest_result.results) if latest_result.results else {}
                        user_features.update({
                            'methodology': latest_result.methodology,
                            'recommendation': latest_result.recommendation or '',
                            'results_json': latest_result.results or '{}'
                        })
                        
                        # Add scores if available
                        if 'scores' in results_dict:
                            for category, score in results_dict['scores'].items():
                                clean_category = category.replace('-', '_').replace(' ', '_').lower()
                                user_features[f'score_{clean_category}'] = score
                                
                        # Add dominant category if available
                        if 'dominant_category' in results_dict:
                            user_features['dominant_category'] = results_dict['dominant_category']
                            
                    except json.JSONDecodeError:
                        self.logger.warning(f"Could not parse results for user {user.id}")
                
                # Get user's career goals
                career_goals = CareerGoal.query.filter_by(user_id=user.id).all()
                user_features['career_goals_count'] = len(career_goals)
                user_features['career_goals_priority_avg'] = np.mean([g.priority for g in career_goals]) if career_goals else 0
                
                # Get user's learning paths
                learning_paths = LearningPath.query.filter_by(user_id=user.id).all()
                user_features['learning_paths_count'] = len(learning_paths)
                user_features['completed_learning_paths'] = len([lp for lp in learning_paths if lp.status == 'completed'])
                
                users_data.append(user_features)
            
            return users_data
        except Exception as e:
            self.logger.error(f"Error preparing user data: {str(e)}")
            return []

    def train_model(self):
        """
        Train the ML model with user data
        """
        try:
            users_data = self.prepare_user_data()
            if not users_data:
                self.logger.warning("No user data available for training")
                return False
            
            df = pd.DataFrame(users_data)
            
            # Handle categorical features
            categorical_columns = ['methodology', 'dominant_category']
            for col in categorical_columns:
                if col in df.columns:
                    # One-hot encode categorical columns
                    dummies = pd.get_dummies(df[col], prefix=col)
                    df = pd.concat([df, dummies], axis=1)
                    df.drop(col, axis=1, inplace=True)
            
            # Select numeric features for clustering
            numeric_columns = [col for col in df.columns if col != 'user_id' and col != 'recommendation' and col != 'results_json']
            if not numeric_columns:
                self.logger.warning("No numeric columns available for clustering")
                return False
                
            X = df[numeric_columns].fillna(0)
            
            # Scale the features
            X_scaled = self.scaler.fit_transform(X)
            
            # Perform clustering to find similar users
            n_clusters = min(10, len(df), max(2, len(df) // 5))
            self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = self.kmeans.fit_predict(X_scaled)
            
            # Store clusters for each user
            self.user_clusters = {}
            for idx, user_id in enumerate(df['user_id']):
                self.user_clusters[user_id] = int(cluster_labels[idx])
            
            # Create recommendation matrix based on similarities
            similarity_matrix = cosine_similarity(X_scaled)
            self.similarity_matrix = similarity_matrix
            
            self.model_trained = True
            self.logger.info(f"ML model trained successfully with {len(df)} users and {n_clusters} clusters")
            return True
            
        except Exception as e:
            self.logger.error(f"Error training ML model: {str(e)}")
            return False

    def get_similar_users(self, user_id, n_similar=5):
        """
        Get users similar to the given user
        """
        if not self.model_trained:
            self.logger.warning("Model not trained yet")
            return []
        
        try:
            # Find the index of the given user
            users_data = self.prepare_user_data()
            df = pd.DataFrame(users_data)
            
            if user_id not in df['user_id'].values:
                return []
            
            user_idx = df[df['user_id'] == user_id].index[0]
            
            # Get similarity scores for this user
            similarity_scores = self.similarity_matrix[user_idx]
            
            # Get indices of most similar users (excluding the user themselves)
            similar_indices = np.argsort(similarity_scores)[::-1][1:n_similar+1]
            
            similar_users = []
            for idx in similar_indices:
                similar_user_id = int(df.iloc[idx]['user_id'])
                similarity_score = float(similarity_scores[idx])
                similar_users.append({
                    'user_id': similar_user_id,
                    'similarity_score': similarity_score
                })
            
            return similar_users
            
        except Exception as e:
            self.logger.error(f"Error getting similar users: {str(e)}")
            return []

    def generate_personalized_recommendations(self, user_id):
        """
        Generate personalized recommendations based on similar users
        """
        if not self.model_trained:
            self.logger.warning("Model not trained yet")
            return []
        
        try:
            # Get similar users
            similar_users = self.get_similar_users(user_id, n_similar=10)
            
            recommendations = []
            
            # Get the current user's test results
            user_test_results = TestResult.query.filter_by(user_id=user_id).all()
            if not user_test_results:
                return []
            
            current_user_results = user_test_results[-1]  # Latest result
            
            # If we have similar users, get their recommendations
            for similar_user in similar_users:
                similar_user_id = similar_user['user_id']
                similarity_score = similar_user['similarity_score']
                
                # Get similar user's test results
                similar_user_results = TestResult.query.filter_by(user_id=similar_user_id).all()
                if similar_user_results:
                    latest_similar_result = similar_user_results[-1]
                    
                    if (latest_similar_result.methodology == current_user_results.methodology and 
                        latest_similar_result.recommendation and 
                        latest_similar_result.recommendation != current_user_results.recommendation):
                        
                        recommendations.append({
                            'type': 'similar_user_recommendation',
                            'content': latest_similar_result.recommendation,
                            'confidence': similarity_score,
                            'source_user_id': similar_user_id,
                            'methodology': latest_similar_result.methodology
                        })
            
            # Also generate recommendations based on user's own data
            if current_user_results.results:
                try:
                    results_dict = json.loads(current_user_results.results)
                    
                    # Generate career path suggestions based on results
                    if 'scores' in results_dict:
                        top_categories = sorted(results_dict['scores'].items(), key=lambda x: x[1], reverse=True)[:3]
                        
                        for category, score in top_categories:
                            if score > 0:  # Only suggest categories with positive scores
                                recommendations.append({
                                    'type': 'category_based_suggestion',
                                    'content': f"Рассмотрите профессии в сфере '{category}' - ваш уровень интереса: {score}/10",
                                    'confidence': score / 10.0,
                                    'category': category,
                                    'score': score
                                })
                                
                    # Generate learning path suggestions
                    if 'dominant_category' in results_dict:
                        dominant_cat = results_dict['dominant_category']
                        recommendations.append({
                            'type': 'learning_path_suggestion',
                            'content': f"Рекомендуем начать с изучения профессий в сфере '{dominant_cat}'. Создайте соответствующую карьерную цель!",
                            'confidence': 0.8,
                            'category': dominant_cat
                        })
                        
                except json.JSONDecodeError:
                    self.logger.warning(f"Could not parse results for user {user_id}")
            
            # Sort recommendations by confidence
            recommendations.sort(key=lambda x: x.get('confidence', 0), reverse=True)
            
            return recommendations[:10]  # Return top 10 recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
            return []

    def get_cluster_insights(self):
        """
        Get insights about user clusters
        """
        if not self.model_trained:
            self.logger.warning("Model not trained yet")
            return {}
        
        try:
            cluster_analysis = {}
            
            # Analyze each cluster
            for cluster_id in set(self.user_clusters.values()):
                cluster_users = [user_id for user_id, cluster in self.user_clusters.items() if cluster == cluster_id]
                
                # Get test results for users in this cluster
                cluster_test_results = []
                for user_id in cluster_users:
                    user_results = TestResult.query.filter_by(user_id=user_id).all()
                    cluster_test_results.extend(user_results)
                
                # Analyze common characteristics
                methodology_counts = {}
                dominant_categories = {}
                
                for result in cluster_test_results:
                    # Count methodologies
                    method = result.methodology
                    methodology_counts[method] = methodology_counts.get(method, 0) + 1
                    
                    # Analyze dominant categories
                    if result.results:
                        try:
                            results_dict = json.loads(result.results)
                            if 'dominant_category' in results_dict:
                                cat = results_dict['dominant_category']
                                dominant_categories[cat] = dominant_categories.get(cat, 0) + 1
                        except json.JSONDecodeError:
                            continue
                
                cluster_analysis[cluster_id] = {
                    'user_count': len(cluster_users),
                    'methodology_distribution': methodology_counts,
                    'dominant_categories': dict(sorted(dominant_categories.items(), key=lambda x: x[1], reverse=True)[:5]),
                    'average_recommendations': len(cluster_test_results)
                }
            
            return cluster_analysis
            
        except Exception as e:
            self.logger.error(f"Error getting cluster insights: {str(e)}")
            return {}

    def save_model(self, filepath):
        """
        Save the trained model to disk
        """
        if not self.model_trained:
            self.logger.warning("Model not trained yet, nothing to save")
            return False
        
        try:
            model_data = {
                'vectorizer': self.vectorizer,
                'scaler': self.scaler,
                'kmeans': self.kmeans,
                'similarity_matrix': self.similarity_matrix,
                'user_clusters': self.user_clusters,
                'model_trained': self.model_trained
            }
            
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
            
            self.logger.info(f"Model saved to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving model: {str(e)}")
            return False

    def load_model(self, filepath):
        """
        Load a pre-trained model from disk
        """
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.scaler = model_data['scaler']
            self.kmeans = model_data['kmeans']
            self.similarity_matrix = model_data['similarity_matrix']
            self.user_clusters = model_data['user_clusters']
            self.model_trained = model_data['model_trained']
            
            self.logger.info(f"Model loaded from {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            return False


# Global instance
enhanced_ml_recommender_instance = EnhancedMLRecommender()