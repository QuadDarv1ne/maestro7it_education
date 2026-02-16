// Embeddable Widget for External Websites
// Usage: <script src="https://chesscalendar-ru.ru/static/js/embed-widget.js" data-widget="upcoming" data-limit="5"></script>

(function() {
    'use strict';

    class ChessCalendarWidget {
        constructor(config) {
            this.config = {
                type: config.type || 'upcoming', // upcoming, popular, category
                limit: config.limit || 5,
                category: config.category || '',
                theme: config.theme || 'light', // light, dark
                showImages: config.showImages !== 'false',
                showDates: config.showDates !== 'false',
                showLocation: config.showLocation !== 'false',
                apiUrl: config.apiUrl || 'http://127.0.0.1:5000',
                ...config
            };

            this.container = null;
            this.data = [];
            this.init();
        }

        async init() {
            this.createContainer();
            await this.fetchData();
            this.render();
        }

        createContainer() {
            const scripts = document.getElementsByTagName('script');
            const currentScript = scripts[scripts.length - 1];
            
            this.container = document.createElement('div');
            this.container.className = 'chess-calendar-widget';
            this.container.id = `chess-widget-${Date.now()}`;
            
            currentScript.parentNode.insertBefore(this.container, currentScript);
        }

        async fetchData() {
            try {
                let url = `${this.config.apiUrl}/api/tournaments`;
                
                if (this.config.type === 'upcoming') {
                    url += `?status=upcoming&limit=${this.config.limit}`;
                } else if (this.config.category) {
                    url += `?category=${encodeURIComponent(this.config.category)}&limit=${this.config.limit}`;
                }

                const response = await fetch(url);
                const result = await response.json();
                this.data = result.tournaments || result;
            } catch (error) {
                console.error('Chess Calendar Widget: Failed to fetch data', error);
                this.data = [];
            }
        }

        render() {
            const styles = this.getStyles();
            const html = this.getHTML();

            this.container.innerHTML = `
                <style>${styles}</style>
                ${html}
            `;
        }

        getStyles() {
            const isDark = this.config.theme === 'dark';
            
            return `
                .chess-calendar-widget {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: ${isDark ? '#1e293b' : '#ffffff'};
                    border-radius: 12px;
                    padding: 1.5rem;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    color: ${isDark ? '#f8fafc' : '#1e293b'};
                }

                .chess-widget-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 1rem;
                    padding-bottom: 1rem;
                    border-bottom: 2px solid ${isDark ? '#334155' : '#e2e8f0'};
                }

                .chess-widget-title {
                    font-size: 1.25rem;
                    font-weight: 700;
                    margin: 0;
                    color: ${isDark ? '#f8fafc' : '#1e293b'};
                }

                .chess-widget-logo {
                    font-size: 1.5rem;
                }

                .chess-widget-list {
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }

                .chess-widget-item {
                    padding: 1rem;
                    margin-bottom: 0.75rem;
                    background: ${isDark ? '#334155' : '#f8fafc'};
                    border-radius: 8px;
                    transition: all 0.3s ease;
                    cursor: pointer;
                }

                .chess-widget-item:hover {
                    transform: translateX(5px);
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
                }

                .chess-widget-item:last-child {
                    margin-bottom: 0;
                }

                .chess-widget-item-title {
                    font-weight: 600;
                    font-size: 1rem;
                    margin-bottom: 0.5rem;
                    color: ${isDark ? '#f8fafc' : '#1e293b'};
                }

                .chess-widget-item-meta {
                    display: flex;
                    gap: 1rem;
                    font-size: 0.875rem;
                    color: ${isDark ? '#cbd5e1' : '#64748b'};
                }

                .chess-widget-item-meta span {
                    display: flex;
                    align-items: center;
                    gap: 0.25rem;
                }

                .chess-widget-footer {
                    margin-top: 1rem;
                    padding-top: 1rem;
                    border-top: 1px solid ${isDark ? '#334155' : '#e2e8f0'};
                    text-align: center;
                }

                .chess-widget-link {
                    color: #2563eb;
                    text-decoration: none;
                    font-weight: 600;
                    font-size: 0.875rem;
                }

                .chess-widget-link:hover {
                    text-decoration: underline;
                }

                .chess-widget-empty {
                    text-align: center;
                    padding: 2rem;
                    color: ${isDark ? '#94a3b8' : '#64748b'};
                }
            `;
        }

        getHTML() {
            if (this.data.length === 0) {
                return `
                    <div class="chess-widget-header">
                        <h3 class="chess-widget-title">
                            <span class="chess-widget-logo">♟️</span> Шахматные турниры
                        </h3>
                    </div>
                    <div class="chess-widget-empty">
                        Нет доступных турниров
                    </div>
                `;
            }

            const title = this.getWidgetTitle();
            const items = this.data.slice(0, this.config.limit).map(tournament => 
                this.renderTournamentItem(tournament)
            ).join('');

            return `
                <div class="chess-widget-header">
                    <h3 class="chess-widget-title">
                        <span class="chess-widget-logo">♟️</span> ${title}
                    </h3>
                </div>
                <ul class="chess-widget-list">
                    ${items}
                </ul>
                <div class="chess-widget-footer">
                    <a href="${this.config.apiUrl}" class="chess-widget-link" target="_blank">
                        Все турниры на ChessCalendar-RU →
                    </a>
                </div>
            `;
        }

        getWidgetTitle() {
            if (this.config.type === 'upcoming') {
                return 'Предстоящие турниры';
            } else if (this.config.category) {
                return `Турниры: ${this.config.category}`;
            }
            return 'Шахматные турниры';
        }

        renderTournamentItem(tournament) {
            const url = `${this.config.apiUrl}/tournament/${tournament.id}`;
            
            return `
                <li class="chess-widget-item" onclick="window.open('${url}', '_blank')">
                    <div class="chess-widget-item-title">${this.escapeHtml(tournament.name)}</div>
                    <div class="chess-widget-item-meta">
                        ${this.config.showDates ? `
                            <span>
                                📅 ${this.formatDate(tournament.start_date)}
                            </span>
                        ` : ''}
                        ${this.config.showLocation ? `
                            <span>
                                📍 ${this.escapeHtml(tournament.location)}
                            </span>
                        ` : ''}
                    </div>
                </li>
            `;
        }

        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('ru-RU', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            });
        }

        escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    }

    // Auto-initialize from script tag attributes
    function autoInit() {
        const scripts = document.getElementsByTagName('script');
        const currentScript = scripts[scripts.length - 1];
        
        if (currentScript && currentScript.src.includes('embed-widget.js')) {
            const config = {
                type: currentScript.getAttribute('data-widget') || 'upcoming',
                limit: parseInt(currentScript.getAttribute('data-limit')) || 5,
                category: currentScript.getAttribute('data-category') || '',
                theme: currentScript.getAttribute('data-theme') || 'light',
                showImages: currentScript.getAttribute('data-show-images'),
                showDates: currentScript.getAttribute('data-show-dates'),
                showLocation: currentScript.getAttribute('data-show-location'),
                apiUrl: currentScript.getAttribute('data-api-url') || 'http://127.0.0.1:5000'
            };

            new ChessCalendarWidget(config);
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', autoInit);
    } else {
        autoInit();
    }

    // Export for manual initialization
    window.ChessCalendarWidget = ChessCalendarWidget;
})();
