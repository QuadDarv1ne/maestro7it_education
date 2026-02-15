from app import db
from app.models.user import User
from app.models.tournament import Tournament
from app.models.favorite import FavoriteTournament
from app.models.preference import UserInteraction
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import math


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
                elif interaction.interaction_type == 'register':
                    weight *= 2
                elif interaction.interaction_type == 'attend':
                    weight *= 4
                
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
            elif days_until_start > 60:  # Future tournaments
                score += 1
            
            # Add collaborative filtering component
            similar_users_score = RecommendationEngine._collaborative_filtering_score(user_id, tournament.id)
            score += similar_users_score
            
            # Add popularity bonus
            popularity_bonus = RecommendationEngine._calculate_popularity_bonus(tournament.id)
            score += popularity_bonus
            
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

    @staticmethod
    def _collaborative_filtering_score(user_id, tournament_id):
        """Calculate collaborative filtering score based on similar users"""
        # Find users who interacted with the same tournaments
        user_interactions = UserInteraction.query.filter_by(user_id=user_id).all()
        user_tournament_ids = {ui.tournament_id for ui in user_interactions}

        # Find other users who interacted with similar tournaments
        similar_users = set()
        for tournament_id in user_tournament_ids:
            interactions = UserInteraction.query.filter_by(tournament_id=tournament_id).all()
            for interaction in interactions:
                if interaction.user_id != user_id:
                    similar_users.add(interaction.user_id)

        # Calculate score based on similar users' interactions with this tournament
        score = 0
        for similar_user_id in similar_users:
            interactions = UserInteraction.query.filter_by(
                user_id=similar_user_id,
                tournament_id=tournament_id
            ).all()
            for interaction in interactions:
                if interaction.interaction_type == 'favorite':
                    score += 2
                elif interaction.interaction_type == 'register':
                    score += 1.5
                elif interaction.interaction_type == 'attend':
                    score += 3
                elif interaction.interaction_type == 'view':
                    score += 0.5

        return score

    @staticmethod
    def _calculate_popularity_bonus(tournament_id):
        """Calculate popularity bonus based on number of interactions"""
        interactions = UserInteraction.query.filter_by(tournament_id=tournament_id).all()
        interaction_count = len(interactions)

        # Logarithmic scale to prevent overly popular items from dominating
        if interaction_count > 0:
            return math.log(interaction_count + 1)
        return 0

    @staticmethod
    def get_collaborative_recommendations(user_id, limit=10):
        """Get recommendations based on collaborative filtering"""
        # Find users with similar interests
        user_interactions = UserInteraction.query.filter_by(user_id=user_id).all()
        user_tournament_ids = {ui.tournament_id for ui in user_interactions}

        # Find other users who interacted with similar tournaments
        candidate_tournaments = defaultdict(int)
        for tournament_id in user_tournament_ids:
            interactions = UserInteraction.query.filter_by(tournament_id=tournament_id).all()
            for interaction in interactions:
                if interaction.user_id != user_id:
                    # Get other tournaments this similar user interacted with
                    other_interactions = UserInteraction.query.filter_by(user_id=interaction.user_id).all()
                    for other_interaction in other_interactions:
                        if other_interaction.tournament_id not in user_tournament_ids:
                            candidate_tournaments[other_interaction.tournament_id] += 1

        # Sort by score and return top candidates
        sorted_candidates = sorted(candidate_tournaments.items(), key=lambda x: x[1], reverse=True)
        recommended_tournaments = []
        for tournament_id, score in sorted_candidates[:limit]:
            tournament = Tournament.query.get(tournament_id)
            if tournament and tournament.status != 'Completed':
                recommended_tournaments.append(tournament)

        return recommended_tournaments