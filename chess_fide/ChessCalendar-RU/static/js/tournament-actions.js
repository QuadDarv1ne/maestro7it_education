/**
 * Tournament Actions
 * Функциональность действий с турнирами
 */

(function() {
    'use strict';
    
    // ============================================
    // FAVORITES MANAGEMENT
    // ============================================
    class FavoritesManager {
        constructor() {
            this.favorites = this.loadFavorites();
        }
        
        loadFavorites() {
            const stored = localStorage.getItem('tournament_favorites');
            return stored ? JSON.parse(stored) : [];
        }
        
        saveFavorites() {
            localStorage.setItem('tournament_favorites', JSON.stringify(this.favorites));
        }
        
        add(tournamentId) {
            if (!this.favorites.includes(tournamentId)) {
                this.favorites.push(tournamentId);
                this.saveFavorites();
                this.syncWithServer(tournamentId, 'add');
                return true;
            }
            return false;
        }
        
        remove(tournamentId) {
            const index = this.favorites.indexOf(tournamentId);
            if (index > -1) {
                this.favorites.splice(index, 1);
                this.saveFavorites();
                this.syncWithServer(tournamentId, 'remove');
                return true;
            }
            return false;
        }
        
        has(tournamentId) {
            return this.favorites.includes(tournamentId);
        }
        
        toggle(tournamentId) {
            if (this.has(tournamentId)) {
                this.remove(tournamentId);
                return false;
            } else {
                this.add(tournamentId);
                return true;
            }
        }
        
        async syncWithServer(tournamentId, action) {
            try {
                const response = await fetch('/api/favorites', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        tournament_id: tournamentId,
                        action: action
                    })
                });
                
                if (!response.ok) {
                    console.warn('Failed to sync favorites with server');
                }
            } catch (error) {
                console.error('Error syncing favorites:', error);
            }
        }
        
        getAll() {
            return [...this.favorites];
        }
        
        count() {
            return this.favorites.length;
        }
    }
    
    // ============================================
    // CALENDAR EXPORT
    // ============================================
    class CalendarExporter {
        static exportToICS(tournament) {
            const event = {
                title: tournament.name,
                start: tournament.startDate,
                end: tournament.endDate,
                location: tournament.location,
                description: tournament.description || '',
                url: window.location.href
            };
            
            const icsContent = this.generateICS(event);
            this.downloadICS(icsContent, `${tournament.name}.ics`);
        }
        
        static generateICS(event) {
            const formatDate = (date) => {
                return date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
            };
            
            const startDate = new Date(event.start);
            const endDate = new Date(event.end);
            
            return [
                'BEGIN:VCALENDAR',
                'VERSION:2.0',
                'PRODID:-//ChessCalendar-RU//Tournament//EN',
                'CALSCALE:GREGORIAN',
                'METHOD:PUBLISH',
                'BEGIN:VEVENT',
                `DTSTART:${formatDate(startDate)}`,
                `DTEND:${formatDate(endDate)}`,
                `SUMMARY:${event.title}`,
                `DESCRIPTION:${event.description}`,
                `LOCATION:${event.location}`,
                `URL:${event.url}`,
                `UID:${Date.now()}@chesscalendar.ru`,
                'STATUS:CONFIRMED',
                'SEQUENCE:0',
                'END:VEVENT',
                'END:VCALENDAR'
            ].join('\r\n');
        }
        
        static downloadICS(content, filename) {
            const blob = new Blob([content], { type: 'text/calendar;charset=utf-8' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(link.href);
        }
        
        static async addToGoogleCalendar(tournament) {
            const baseUrl = 'https://calendar.google.com/calendar/render';
            const params = new URLSearchParams({
                action: 'TEMPLATE',
                text: tournament.name,
                dates: `${this.formatGoogleDate(tournament.startDate)}/${this.formatGoogleDate(tournament.endDate)}`,
                details: tournament.description || '',
                location: tournament.location,
                sf: 'true',
                output: 'xml'
            });
            
            window.open(`${baseUrl}?${params.toString()}`, '_blank');
        }
        
        static formatGoogleDate(dateString) {
            const date = new Date(dateString);
            return date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
        }
    }
    
    // ============================================
    // NOTIFICATIONS MANAGER
    // ============================================
    class NotificationsManager {
        constructor() {
            this.notifications = this.loadNotifications();
        }
        
        loadNotifications() {
            const stored = localStorage.getItem('tournament_notifications');
            return stored ? JSON.parse(stored) : [];
        }
        
        saveNotifications() {
            localStorage.setItem('tournament_notifications', JSON.stringify(this.notifications));
        }
        
        async enable(tournamentId, tournamentName, startDate) {
            if (this.isEnabled(tournamentId)) {
                return false;
            }
            
            // Request permission
            if ('Notification' in window) {
                let permission = Notification.permission;
                
                if (permission === 'default') {
                    permission = await Notification.requestPermission();
                }
                
                if (permission === 'granted') {
                    this.notifications.push({
                        id: tournamentId,
                        name: tournamentName,
                        startDate: startDate,
                        enabled: true,
                        createdAt: new Date().toISOString()
                    });
                    
                    this.saveNotifications();
                    this.scheduleNotification(tournamentId, tournamentName, startDate);
                    this.syncWithServer(tournamentId, 'enable');
                    
                    return true;
                }
            }
            
            return false;
        }
        
        disable(tournamentId) {
            const index = this.notifications.findIndex(n => n.id === tournamentId);
            if (index > -1) {
                this.notifications.splice(index, 1);
                this.saveNotifications();
                this.syncWithServer(tournamentId, 'disable');
                return true;
            }
            return false;
        }
        
        isEnabled(tournamentId) {
            return this.notifications.some(n => n.id === tournamentId);
        }
        
        scheduleNotification(tournamentId, tournamentName, startDate) {
            const start = new Date(startDate);
            const now = new Date();
            const dayBefore = new Date(start.getTime() - 24 * 60 * 60 * 1000);
            
            if (dayBefore > now) {
                const timeout = dayBefore.getTime() - now.getTime();
                setTimeout(() => {
                    this.showNotification(tournamentName, 'Турнир начнется завтра!');
                }, timeout);
            }
        }
        
        showNotification(title, body) {
            if ('Notification' in window && Notification.permission === 'granted') {
                new Notification(title, {
                    body: body,
                    icon: '/static/images/logo.png',
                    badge: '/static/images/badge.png',
                    tag: 'tournament-reminder',
                    requireInteraction: false
                });
            }
        }
        
        async syncWithServer(tournamentId, action) {
            try {
                await fetch('/api/notifications', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        tournament_id: tournamentId,
                        action: action
                    })
                });
            } catch (error) {
                console.error('Error syncing notifications:', error);
            }
        }
    }
    
    // ============================================
    // SHARE MANAGER
    // ============================================
    class ShareManager {
        static async share(tournament) {
            const shareData = {
                title: tournament.name,
                text: `${tournament.name} - ${tournament.location}`,
                url: window.location.href
            };
            
            if (navigator.share) {
                try {
                    await navigator.share(shareData);
                    return { success: true, method: 'native' };
                } catch (err) {
                    if (err.name === 'AbortError') {
                        return { success: false, method: 'cancelled' };
                    }
                    return this.fallbackShare(shareData);
                }
            } else {
                return this.fallbackShare(shareData);
            }
        }
        
        static fallbackShare(shareData) {
            // Show share modal with options
            this.showShareModal(shareData);
            return { success: true, method: 'modal' };
        }
        
        static showShareModal(shareData) {
            const modal = document.createElement('div');
            modal.className = 'share-modal-overlay';
            modal.innerHTML = `
                <div class="share-modal">
                    <div class="share-modal-header">
                        <h3>Поделиться турниром</h3>
                        <button class="share-modal-close">&times;</button>
                    </div>
                    <div class="share-modal-body">
                        <div class="share-options">
                            <button class="share-option" data-method="copy">
                                <i class="bi bi-link-45deg"></i>
                                <span>Копировать ссылку</span>
                            </button>
                            <button class="share-option" data-method="telegram">
                                <i class="bi bi-telegram"></i>
                                <span>Telegram</span>
                            </button>
                            <button class="share-option" data-method="whatsapp">
                                <i class="bi bi-whatsapp"></i>
                                <span>WhatsApp</span>
                            </button>
                            <button class="share-option" data-method="vk">
                                <i class="bi bi-vk"></i>
                                <span>VK</span>
                            </button>
                            <button class="share-option" data-method="email">
                                <i class="bi bi-envelope"></i>
                                <span>Email</span>
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            // Close button
            modal.querySelector('.share-modal-close').addEventListener('click', () => {
                modal.remove();
            });
            
            // Click outside to close
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.remove();
                }
            });
            
            // Share options
            modal.querySelectorAll('.share-option').forEach(btn => {
                btn.addEventListener('click', () => {
                    const method = btn.getAttribute('data-method');
                    this.shareVia(method, shareData);
                    modal.remove();
                });
            });
        }
        
        static shareVia(method, data) {
            const url = encodeURIComponent(data.url);
            const text = encodeURIComponent(data.text);
            
            const urls = {
                telegram: `https://t.me/share/url?url=${url}&text=${text}`,
                whatsapp: `https://wa.me/?text=${text}%20${url}`,
                vk: `https://vk.com/share.php?url=${url}&title=${text}`,
                email: `mailto:?subject=${text}&body=${url}`
            };
            
            if (method === 'copy') {
                this.copyToClipboard(data.url);
            } else if (urls[method]) {
                window.open(urls[method], '_blank');
            }
        }
        
        static copyToClipboard(text) {
            if (navigator.clipboard) {
                navigator.clipboard.writeText(text).then(() => {
                    window.showToast('Ссылка скопирована', 'success', 2000);
                });
            } else {
                const textarea = document.createElement('textarea');
                textarea.value = text;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                window.showToast('Ссылка скопирована', 'success', 2000);
            }
        }
    }
    
    // ============================================
    // TOURNAMENT COMPARISON
    // ============================================
    class TournamentComparison {
        constructor() {
            this.selected = this.loadSelected();
        }
        
        loadSelected() {
            const stored = localStorage.getItem('tournament_comparison');
            return stored ? JSON.parse(stored) : [];
        }
        
        saveSelected() {
            localStorage.setItem('tournament_comparison', JSON.stringify(this.selected));
        }
        
        add(tournament) {
            if (this.selected.length >= 3) {
                window.showToast('Можно сравнить максимум 3 турнира', 'warning', 3000);
                return false;
            }
            
            if (!this.selected.find(t => t.id === tournament.id)) {
                this.selected.push(tournament);
                this.saveSelected();
                this.updateComparisonBar();
                return true;
            }
            return false;
        }
        
        remove(tournamentId) {
            this.selected = this.selected.filter(t => t.id !== tournamentId);
            this.saveSelected();
            this.updateComparisonBar();
        }
        
        clear() {
            this.selected = [];
            this.saveSelected();
            this.updateComparisonBar();
        }
        
        updateComparisonBar() {
            let bar = document.getElementById('comparison-bar');
            
            if (this.selected.length === 0) {
                if (bar) bar.remove();
                return;
            }
            
            if (!bar) {
                bar = document.createElement('div');
                bar.id = 'comparison-bar';
                bar.className = 'comparison-bar';
                document.body.appendChild(bar);
            }
            
            bar.innerHTML = `
                <div class="comparison-bar-content">
                    <div class="comparison-bar-title">
                        <i class="bi bi-bar-chart"></i>
                        Сравнение турниров (${this.selected.length}/3)
                    </div>
                    <div class="comparison-bar-items">
                        ${this.selected.map(t => `
                            <div class="comparison-bar-item">
                                <span>${t.name}</span>
                                <button class="comparison-bar-remove" data-id="${t.id}">
                                    <i class="bi bi-x"></i>
                                </button>
                            </div>
                        `).join('')}
                    </div>
                    <div class="comparison-bar-actions">
                        <button class="btn-enhanced btn-primary-enhanced btn-sm-enhanced" id="compare-btn">
                            <i class="bi bi-bar-chart"></i> Сравнить
                        </button>
                        <button class="btn-enhanced btn-secondary-enhanced btn-sm-enhanced" id="clear-comparison-btn">
                            <i class="bi bi-x-circle"></i> Очистить
                        </button>
                    </div>
                </div>
            `;
            
            // Event listeners
            bar.querySelectorAll('.comparison-bar-remove').forEach(btn => {
                btn.addEventListener('click', () => {
                    this.remove(btn.getAttribute('data-id'));
                });
            });
            
            bar.querySelector('#compare-btn').addEventListener('click', () => {
                this.showComparison();
            });
            
            bar.querySelector('#clear-comparison-btn').addEventListener('click', () => {
                this.clear();
            });
        }
        
        showComparison() {
            // Open comparison modal or page
            window.location.href = `/tournaments/compare?ids=${this.selected.map(t => t.id).join(',')}`;
        }
    }
    
    // ============================================
    // INITIALIZE
    // ============================================
    
    // Create global instances
    window.favoritesManager = new FavoritesManager();
    window.calendarExporter = CalendarExporter;
    window.notificationsManager = new NotificationsManager();
    window.shareManager = ShareManager;
    window.tournamentComparison = new TournamentComparison();
    
    // Initialize favorites on page load
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('.card-favorite-btn').forEach(btn => {
            const tournamentId = btn.getAttribute('data-tournament-id');
            if (window.favoritesManager.has(tournamentId)) {
                btn.classList.add('active');
                btn.querySelector('i').classList.remove('bi-heart');
                btn.querySelector('i').classList.add('bi-heart-fill');
            }
        });
        
        // Update favorites count in navbar
        updateFavoritesCount();
    });
    
    function updateFavoritesCount() {
        const count = window.favoritesManager.count();
        const badge = document.querySelector('.favorites-count-badge');
        if (badge) {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'inline-flex' : 'none';
        }
    }
    
    // Export for use in other scripts
    window.updateFavoritesCount = updateFavoritesCount;
    
})();
