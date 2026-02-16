// Admin Dashboard Enhancements

class AdminDashboard {
    constructor() {
        this.charts = {};
        this.refreshInterval = 60000; // 1 minute
        this.init();
    }
    
    init() {
        this.loadStatistics();
        this.setupAutoRefresh();
        this.setupEventListeners();
    }
    
    async loadStatistics() {
        try {
            const response = await fetch('/api/admin/statistics');
            const data = await response.json();
            
            this.updateStatCards(data);
            this.renderCharts(data);
        } catch (error) {
            console.error('Failed to load statistics:', error);
            window.ChessCalendar.showToast('Ошибка загрузки статистики', 'danger');
        }
    }
    
    updateStatCards(data) {
        // Update stat cards with animation
        this.animateValue('totalUsers', 0, data.total_users || 0, 1000);
        this.animateValue('totalTournaments', 0, data.total_tournaments || 0, 1000);
        this.animateValue('activeTournaments', 0, data.active_tournaments || 0, 1000);
        this.animateValue('totalViews', 0, data.total_views || 0, 1000);
    }
    
    animateValue(elementId, start, end, duration) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
                current = end;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current).toLocaleString('ru-RU');
        }, 16);
    }
    
    renderCharts(data) {
        // This is a placeholder - in production, use Chart.js or similar
        console.log('Chart data:', data);
        
        // Example: Render user growth chart
        if (data.user_growth) {
            this.renderUserGrowthChart(data.user_growth);
        }
        
        // Example: Render tournament distribution
        if (data.tournament_distribution) {
            this.renderTournamentDistribution(data.tournament_distribution);
        }
    }
    
    renderUserGrowthChart(data) {
        const canvas = document.getElementById('userGrowthChart');
        if (!canvas) return;
        
        // Placeholder for actual chart implementation
        console.log('User growth data:', data);
    }
    
    renderTournamentDistribution(data) {
        const canvas = document.getElementById('tournamentDistChart');
        if (!canvas) return;
        
        // Placeholder for actual chart implementation
        console.log('Tournament distribution:', data);
    }
    
    setupAutoRefresh() {
        setInterval(() => {
            this.loadStatistics();
        }, this.refreshInterval);
    }
    
    setupEventListeners() {
        // Refresh button
        const refreshBtn = document.getElementById('refreshStats');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                window.ChessCalendar.showLoader();
                this.loadStatistics().finally(() => {
                    window.ChessCalendar.hideLoader();
                    window.ChessCalendar.showToast('Статистика обновлена', 'success');
                });
            });
        }
        
        // Export buttons
        const exportCsvBtn = document.getElementById('exportCsv');
        if (exportCsvBtn) {
            exportCsvBtn.addEventListener('click', () => {
                window.location.href = '/api/admin/export/csv';
            });
        }
        
        const exportJsonBtn = document.getElementById('exportJson');
        if (exportJsonBtn) {
            exportJsonBtn.addEventListener('click', () => {
                window.location.href = '/api/admin/export/json';
            });
        }
        
        // Bulk actions
        const bulkActionBtn = document.getElementById('bulkAction');
        if (bulkActionBtn) {
            bulkActionBtn.addEventListener('click', () => {
                this.handleBulkAction();
            });
        }
    }
    
    handleBulkAction() {
        const action = document.getElementById('bulkActionSelect')?.value;
        const checkboxes = document.querySelectorAll('.tournament-checkbox:checked');
        
        if (!action || checkboxes.length === 0) {
            window.ChessCalendar.showToast('Выберите действие и турниры', 'warning');
            return;
        }
        
        const tournamentIds = Array.from(checkboxes).map(cb => cb.value);
        
        if (confirm(`Применить действие "${action}" к ${tournamentIds.length} турнирам?`)) {
            this.executeBulkAction(action, tournamentIds);
        }
    }
    
    async executeBulkAction(action, tournamentIds) {
        try {
            window.ChessCalendar.showLoader();
            
            const response = await fetch('/api/admin/bulk-action', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: action,
                    tournament_ids: tournamentIds
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                window.ChessCalendar.showToast(`Действие выполнено для ${data.affected} турниров`, 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                window.ChessCalendar.showToast(data.error || 'Ошибка', 'danger');
            }
        } catch (error) {
            console.error('Bulk action error:', error);
            window.ChessCalendar.showToast('Ошибка выполнения', 'danger');
        } finally {
            window.ChessCalendar.hideLoader();
        }
    }
}

// Real-time updates using Server-Sent Events (optional)
class RealtimeUpdates {
    constructor() {
        this.eventSource = null;
        this.init();
    }
    
    init() {
        if (!window.EventSource) {
            console.warn('SSE not supported');
            return;
        }
        
        this.connect();
    }
    
    connect() {
        this.eventSource = new EventSource('/api/admin/realtime');
        
        this.eventSource.addEventListener('update', (e) => {
            const data = JSON.parse(e.data);
            this.handleUpdate(data);
        });
        
        this.eventSource.addEventListener('error', (e) => {
            console.error('SSE error:', e);
            this.eventSource.close();
            
            // Reconnect after 5 seconds
            setTimeout(() => this.connect(), 5000);
        });
    }
    
    handleUpdate(data) {
        console.log('Realtime update:', data);
        
        // Update UI based on data type
        if (data.type === 'new_user') {
            this.showNotification('Новый пользователь зарегистрирован');
        } else if (data.type === 'new_tournament') {
            this.showNotification('Добавлен новый турнир');
        }
    }
    
    showNotification(message) {
        if (window.ChessCalendar) {
            window.ChessCalendar.showToast(message, 'info');
        }
    }
    
    disconnect() {
        if (this.eventSource) {
            this.eventSource.close();
        }
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.body.classList.contains('admin-page')) {
        const dashboard = new AdminDashboard();
        
        // Optional: Enable realtime updates
        // const realtime = new RealtimeUpdates();
    }
});

// Export for global use
window.AdminDashboard = AdminDashboard;
window.RealtimeUpdates = RealtimeUpdates;
