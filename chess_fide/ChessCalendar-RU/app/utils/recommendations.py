from app import db
from app.models.user import User
from app.models.tournament import Tournament
from app.models.favorite import FavoriteTournament
from app.models.preference import UserInteraction
from datetime import datetime
from collections import defaultdict


class RecommendationEngine:
    """Engine for generating tournament recommendations based on user preferences and interactions"""
    
    @staticmethod
    def get_user_recommendations(user_id):
        """Get tournament recommendations for a user based on preferences and interactions"""
        # Get the user
        user = User.query.get(user_id)
        if not user:
            return []
        
        # Get all tournaments
        all_tournaments = Tournament.query.all()
        
        # Get user interactions
        interactions = UserInteraction.query.filter_by(user_id=user_id).all()
        
        # Get user's favorite tournaments
        favorites = FavoriteTournament.query.filter_by(user_id=user_id).all()
        favorite_tournament_ids = {fav.tournament_id for fav in favorites}
        
        # Calculate weights based on categories from interactions
        category_weights = defaultdict(float)
        location_weights = defaultdict(float)
        
        for interaction in interactions:
            tournament = interaction.tournament
            if tournament:
                # Increase category weight based on interaction type
                weight = interaction.interaction_value
                if interaction.interaction_type == 'favorite':
                    weight *= 3
                elif interaction.interaction_type == 'view':
                    weight *= 1
                
                category_weights[tournament.category] += weight
                location_weights[tournament.location] += weight
        
        # Sort weights
        sorted_categories = sorted(category_weights.items(), key=lambda x: x[1], reverse=True)
        sorted_locations = sorted(location_weights.items(), key=lambda x: x[1], reverse=True)
        
        # Calculate scores for each tournament
        tournament_scores = {}
        for tournament in all_tournaments:
            # Skip tournaments the user has already favorited
            if tournament.id in favorite_tournament_ids:
                continue
            
            # Skip completed tournaments
            if tournament.status == 'Completed':
                continue
            
            score = 0
            
            # Add score based on category
            if tournament.category in category_weights:
                score += category_weights[tournament.category] * 2  # Double category weight
            
            # Add score based on location
            if tournament.location in location_weights:
                score += location_weights[tournament.location]
            
            # Boost score for tournaments happening soon
            days_until_start = (tournament.start_date - datetime.today().date()).days
            if 0 <= days_until_start <= 30:  # Tournaments in the next month
                score += 5
            elif 31 <= days_until_start <= 60:  # Tournaments in the next 2 months
                score += 3
            
            tournament_scores[tournament.id] = score
        
        # Sort tournaments by score and return top 10
        sorted_tournaments = sorted(tournament_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return tournaments in score order
        recommended_tournaments = []
        for tid, score in sorted_tournaments[:10]:
            tournament = Tournament.query.get(tid)
            if tournament:
                recommended_tournaments.append(tournament)
        
        return recommended_tournaments
    
    @staticmethod
    def record_interaction(user_id, tournament_id, interaction_type, interaction_value=1):
        """Record a user interaction with a tournament"""
        interaction = UserInteraction(
            user_id=user_id,
            tournament_id=tournament_id,
            interaction_type=interaction_type,
            interaction_value=interaction_value
        )
        db.session.add(interaction)
        db.session.commit()
        return interaction