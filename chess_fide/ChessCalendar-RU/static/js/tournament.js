// Tournament Detail Page Enhancements

class TournamentPage {
    constructor(tournamentId) {
        this.tournamentId = tournamentId;
        this.init();
    }
    
    init() {
        this.setupFavoriteButton();
        this.setupRatingSystem();
        this.setupShareButton();
        this.setupNotificationSubscription();
        this.trackView();
    }
    
    trackView() {
        if (window.ChessCalendarAnalytics) {
            const tournamentName = document.querySelector('h1')?.textContent || 'Unknown';
            window.ChessCalendarAnalytics.trackTournamentView(this.tournamentId, tournamentName);
        }
    }
    
    setupFavoriteButton() {
        const favoriteBtn = document.getElementById('favoriteBtn');
        if (!favoriteBtn) return;
        
        favoriteBtn.addEventListener('click', async () => {
            const isFavorite = favoriteBtn.classList.contains('active');
            
            try {
                const response = await fetch(`/api/favorites/${this.tournamentId}`, {
                    method: isFavorite ? 'DELETE' : 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    favoriteBtn.classList.toggle('active');
                    const icon = favoriteBtn.querySelector('i');
                    
                    if (isFavorite) {
                        icon.className = 'bi bi-heart';
                        favoriteBtn.innerHTML = '<i class="bi bi-heart"></i> В избранное';
                        window.ChessCalendar.showToast('Удалено из избранного', 'info');
                        
                        if (window.ChessCalendarAnalytics) {
                            window.ChessCalendarAnalytics.trackFavoriteRemove(this.tournamentId);
                        }
                    } else {
                        icon.className = 'bi bi-heart-fill';
                        favoriteBtn.innerHTML = '<i class="bi bi-heart-fill"></i> В избранном';
                        window.ChessCalendar.showToast('Добавлено в избранное', 'success');
                        
                        if (window.ChessCalendarAnalytics) {
                            window.ChessCalendarAnalytics.trackFavoriteAdd(this.tournamentId);
                        }
                    }
                } else {
                    window.ChessCalendar.showToast(data.error || 'Ошибка', 'danger');
                }
            } catch (error) {
                console.error('Favorite error:', error);
                window.ChessCalendar.showToast('Ошибка подключения', 'danger');
            }
        });
    }
    
    setupRatingSystem() {
        const stars = document.querySelectorAll('.rating-star');
        const ratingForm = document.getElementById('ratingForm');
        
        if (!stars.length || !ratingForm) return;
        
        let selectedRating = 0;
        
        // Hover effect
        stars.forEach((star, index) => {
            star.addEventListener('mouseenter', () => {
                this.highlightStars(stars, index + 1);
            });
            
            star.addEventListener('click', () => {
                selectedRating = index + 1;
                document.getElementById('ratingValue').value = selectedRating;
                this.highlightStars(stars, selectedRating, true);
            });
        });
        
        // Reset on mouse leave
        const ratingContainer = document.querySelector('.rating-stars');
        if (ratingContainer) {
            ratingContainer.addEventListener('mouseleave', () => {
                this.highlightStars(stars, selectedRating, true);
            });
        }
        
        // Form submission
        ratingForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (selectedRating === 0) {
                window.ChessCalendar.showToast('Выберите оценку', 'warning');
                return;
            }
            
            const comment = document.getElementById('ratingComment')?.value || '';
            
            try {
                const response = await fetch(`/api/tournaments/${this.tournamentId}/rate`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        rating: selectedRating,
                        comment: comment
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    window.ChessCalendar.showToast('Спасибо за оценку!', 'success');
                    setTimeout(() => location.reload(), 1500);
                } else {
                    window.ChessCalendar.showToast(data.error || 'Ошибка', 'danger');
                }
            } catch (error) {
                console.error('Rating error:', error);
                window.ChessCalendar.showToast('Ошибка подключения', 'danger');
            }
        });
    }
    
    highlightStars(stars, count, permanent = false) {
        stars.forEach((star, index) => {
            if (index < count) {
                star.classList.add('active');
                star.querySelector('i').className = 'bi bi-star-fill';
            } else {
                if (!permanent || index >= count) {
                    star.classList.remove('active');
                    star.querySelector('i').className = 'bi bi-star';
                }
            }
        });
    }
    
    setupShareButton() {
        const shareBtn = document.getElementById('shareBtn');
        if (!shareBtn) return;
        
        shareBtn.addEventListener('click', () => {
            const title = document.querySelector('h1')?.textContent || 'Турнир';
            const url = window.location.href;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    text: `Посмотрите этот турнир: ${title}`,
                    url: url
                }).then(() => {
                    window.ChessCalendar.showToast('Успешно поделились!', 'success');
                    
                    if (window.ChessCalendarAnalytics) {
                        window.ChessCalendarAnalytics.trackShare('native', url);
                    }
                }).catch(err => {
                    if (err.name !== 'AbortError') {
                        this.showShareModal(title, url);
                    }
                });
            } else {
                this.showShareModal(title, url);
            }
        });
    }
    
    showShareModal(title, url) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Поделиться турниром</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="d-grid gap-2">
                            <button class="btn btn-primary" onclick="window.open('https://vk.com/share.php?url=${encodeURIComponent(url)}', '_blank')">
                                <i class="bi bi-vk"></i> ВКонтакте
                            </button>
                            <button class="btn btn-info" onclick="window.open('https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}', '_blank')">
                                <i class="bi bi-telegram"></i> Telegram
                            </button>
                            <button class="btn btn-success" onclick="window.open('https://wa.me/?text=${encodeURIComponent(title + ' ' + url)}', '_blank')">
                                <i class="bi bi-whatsapp"></i> WhatsApp
                            </button>
                            <button class="btn btn-secondary" onclick="window.ChessCalendar.copyToClipboard('${url}', 'Ссылка скопирована!')">
                                <i class="bi bi-link-45deg"></i> Копировать ссылку
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
        
        if (window.ChessCalendarAnalytics) {
            window.ChessCalendarAnalytics.trackShare('modal', url);
        }
    }
    
    setupNotificationSubscription() {
        const subscribeBtn = document.getElementById('subscribeBtn');
        if (!subscribeBtn) return;
        
        subscribeBtn.addEventListener('click', async () => {
            const isSubscribed = subscribeBtn.classList.contains('active');
            
            if (isSubscribed) {
                // Unsubscribe
                if (confirm('Отписаться от уведомлений?')) {
                    // Implementation depends on your backend
                    window.ChessCalendar.showToast('Подписка отменена', 'info');
                    subscribeBtn.classList.remove('active');
                    subscribeBtn.innerHTML = '<i class="bi bi-bell"></i> Подписаться';
                }
            } else {
                // Subscribe
                try {
                    const response = await fetch(`/api/tournaments/${this.tournamentId}/subscribe`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            notify_before_start: true,
                            notify_on_update: true
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        window.ChessCalendar.showToast('Вы подписались на уведомления', 'success');
                        subscribeBtn.classList.add('active');
                        subscribeBtn.innerHTML = '<i class="bi bi-bell-fill"></i> Подписан';
                        
                        if (window.ChessCalendarAnalytics) {
                            window.ChessCalendarAnalytics.trackNotificationSubscribe(this.tournamentId);
                        }
                    } else {
                        window.ChessCalendar.showToast(data.error || 'Ошибка', 'danger');
                    }
                } catch (error) {
                    console.error('Subscribe error:', error);
                    window.ChessCalendar.showToast('Ошибка подключения', 'danger');
                }
            }
        });
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    const tournamentId = document.body.dataset.tournamentId;
    if (tournamentId) {
        new TournamentPage(tournamentId);
    }
});
