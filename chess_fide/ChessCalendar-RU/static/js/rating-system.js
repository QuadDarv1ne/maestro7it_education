// Tournament Rating and Review System

class RatingSystem {
    constructor() {
        this.ratings = this.loadRatings();
        this.init();
    }

    init() {
        this.addRatingWidget();
    }

    loadRatings() {
        const saved = localStorage.getItem('tournamentRatings');
        return saved ? JSON.parse(saved) : {};
    }

    saveRatings() {
        localStorage.setItem('tournamentRatings', JSON.stringify(this.ratings));
    }

    addRatingWidget() {
        document.addEventListener('DOMContentLoaded', () => {
            const tournamentDetail = document.querySelector('.tournament-detail, .card-body');
            if (!tournamentDetail || document.getElementById('ratingWidget')) return;

            const tournamentId = this.extractTournamentId();
            if (!tournamentId) return;

            const widget = this.createRatingWidget(tournamentId);
            tournamentDetail.appendChild(widget);
        });
    }

    extractTournamentId() {
        const match = window.location.pathname.match(/\/tournament\/(\d+)/);
        return match ? parseInt(match[1]) : null;
    }

    createRatingWidget(tournamentId) {
        const container = document.createElement('div');
        container.id = 'ratingWidget';
        container.className = 'rating-widget mt-4';
        
        const rating = this.ratings[tournamentId] || { score: 0, count: 0, userRating: 0, reviews: [] };
        const avgRating = rating.count > 0 ? (rating.score / rating.count).toFixed(1) : 0;

        container.innerHTML = `
            <style>
                .rating-widget {
                    background: var(--bg-primary);
                    border-radius: var(--border-radius);
                    padding: 1.5rem;
                    box-shadow: var(--box-shadow);
                }
                
                .rating-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 1.5rem;
                }
                
                .rating-summary {
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                }
                
                .rating-score {
                    font-size: 3rem;
                    font-weight: 700;
                    color: var(--primary-color);
                }
                
                .rating-details {
                    display: flex;
                    flex-direction: column;
                }
                
                .rating-stars {
                    font-size: 1.5rem;
                    color: #fbbf24;
                }
                
                .rating-count {
                    color: var(--text-secondary);
                    font-size: 0.875rem;
                }
                
                .rating-input {
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                }
                
                .star-rating {
                    display: flex;
                    gap: 0.5rem;
                    font-size: 2rem;
                }
                
                .star {
                    cursor: pointer;
                    color: #d1d5db;
                    transition: all 0.2s;
                }
                
                .star:hover,
                .star.active {
                    color: #fbbf24;
                    transform: scale(1.2);
                }
                
                .review-input {
                    width: 100%;
                    min-height: 100px;
                    padding: 0.75rem;
                    border: 1px solid var(--border-color);
                    border-radius: 8px;
                    background: var(--bg-primary);
                    color: var(--text-primary);
                    resize: vertical;
                }
                
                .reviews-list {
                    margin-top: 2rem;
                }
                
                .review-item {
                    padding: 1rem;
                    border-bottom: 1px solid var(--border-color);
                }
                
                .review-item:last-child {
                    border-bottom: none;
                }
                
                .review-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 0.5rem;
                }
                
                .review-author {
                    font-weight: 600;
                    color: var(--text-primary);
                }
                
                .review-date {
                    font-size: 0.875rem;
                    color: var(--text-secondary);
                }
                
                .review-text {
                    color: var(--text-secondary);
                    line-height: 1.6;
                }
                
                .review-rating {
                    color: #fbbf24;
                    font-size: 0.875rem;
                }
            </style>
            
            <div class="rating-header">
                <h5><i class="bi bi-star-fill text-warning"></i> Рейтинг турнира</h5>
            </div>
            
            <div class="rating-summary">
                <div class="rating-score">${avgRating}</div>
                <div class="rating-details">
                    <div class="rating-stars">${this.renderStars(avgRating)}</div>
                    <div class="rating-count">${rating.count} оценок</div>
                </div>
            </div>
            
            <div class="rating-input mt-3">
                <div>
                    <strong>Ваша оценка:</strong>
                    <div class="star-rating" id="starRating">
                        ${[1, 2, 3, 4, 5].map(i => `
                            <span class="star ${i <= rating.userRating ? 'active' : ''}" 
                                  data-rating="${i}" 
                                  onclick="ratingSystem.setRating(${tournamentId}, ${i})">
                                ★
                            </span>
                        `).join('')}
                    </div>
                </div>
                
                <div>
                    <textarea class="review-input" 
                              id="reviewText" 
                              placeholder="Напишите отзыв о турнире..."></textarea>
                </div>
                
                <button class="btn btn-primary" onclick="ratingSystem.submitReview(${tournamentId})">
                    <i class="bi bi-send"></i> Отправить отзыв
                </button>
            </div>
            
            <div class="reviews-list" id="reviewsList">
                ${this.renderReviews(rating.reviews)}
            </div>
        `;

        return container;
    }

    renderStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

        let stars = '';
        for (let i = 0; i < fullStars; i++) stars += '★';
        if (hasHalfStar) stars += '⯨';
        for (let i = 0; i < emptyStars; i++) stars += '☆';

        return stars;
    }

    renderReviews(reviews) {
        if (!reviews || reviews.length === 0) {
            return '<p class="text-muted text-center">Пока нет отзывов</p>';
        }

        return reviews.map(review => `
            <div class="review-item">
                <div class="review-header">
                    <div>
                        <span class="review-author">${review.author}</span>
                        <div class="review-rating">${this.renderStars(review.rating)}</div>
                    </div>
                    <span class="review-date">${this.formatDate(review.date)}</span>
                </div>
                <div class="review-text">${this.escapeHtml(review.text)}</div>
            </div>
        `).join('');
    }

    setRating(tournamentId, rating) {
        if (!this.ratings[tournamentId]) {
            this.ratings[tournamentId] = { score: 0, count: 0, userRating: 0, reviews: [] };
        }

        // Update user rating
        const oldRating = this.ratings[tournamentId].userRating;
        this.ratings[tournamentId].userRating = rating;

        // Update total score
        if (oldRating > 0) {
            this.ratings[tournamentId].score = this.ratings[tournamentId].score - oldRating + rating;
        } else {
            this.ratings[tournamentId].score += rating;
            this.ratings[tournamentId].count++;
        }

        this.saveRatings();

        // Update UI
        document.querySelectorAll('.star').forEach((star, index) => {
            if (index < rating) {
                star.classList.add('active');
            } else {
                star.classList.remove('active');
            }
        });

        // Update summary
        const avgRating = (this.ratings[tournamentId].score / this.ratings[tournamentId].count).toFixed(1);
        document.querySelector('.rating-score').textContent = avgRating;
        document.querySelector('.rating-stars').innerHTML = this.renderStars(avgRating);
        document.querySelector('.rating-count').textContent = `${this.ratings[tournamentId].count} оценок`;

        if (window.toast) {
            window.toast.success(`Вы поставили ${rating} звезд`);
        }
    }

    submitReview(tournamentId) {
        const reviewText = document.getElementById('reviewText').value.trim();
        
        if (!reviewText) {
            if (window.toast) {
                window.toast.warning('Напишите текст отзыва');
            }
            return;
        }

        if (!this.ratings[tournamentId]) {
            this.ratings[tournamentId] = { score: 0, count: 0, userRating: 0, reviews: [] };
        }

        if (this.ratings[tournamentId].userRating === 0) {
            if (window.toast) {
                window.toast.warning('Сначала поставьте оценку');
            }
            return;
        }

        const review = {
            author: 'Пользователь',
            rating: this.ratings[tournamentId].userRating,
            text: reviewText,
            date: new Date().toISOString()
        };

        this.ratings[tournamentId].reviews.unshift(review);
        this.saveRatings();

        // Update UI
        document.getElementById('reviewsList').innerHTML = this.renderReviews(this.ratings[tournamentId].reviews);
        document.getElementById('reviewText').value = '';

        if (window.toast) {
            window.toast.success('Отзыв отправлен!');
        }
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: 'long',
            year: 'numeric'
        });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Get rating for a tournament
    getRating(tournamentId) {
        return this.ratings[tournamentId] || { score: 0, count: 0, userRating: 0, reviews: [] };
    }

    // Get average rating
    getAverageRating(tournamentId) {
        const rating = this.getRating(tournamentId);
        return rating.count > 0 ? (rating.score / rating.count).toFixed(1) : 0;
    }
}

// Initialize
const ratingSystem = new RatingSystem();

// Export for use in other scripts
window.ratingSystem = ratingSystem;
