/**
 * ChessCalendar-RU Embeddable Widget
 * 
 * Usage:
 * <div id="chess-calendar-widget" 
 *      data-category="blitz" 
 *      data-limit="5"
 *      data-theme="light"></div>
 * <script src="https://chesscalendar.ru/static/js/widget.js"></script>
 */

(function() {
    'use strict';
    
    class ChessCalendarWidget {
        constructor(container) {
            this.container = container;
            this.config = {
                apiUrl: 'https://chesscalendar.ru/api',
                category: container.dataset.category || null,
                location: container.dataset.location || null,
                limit: parseInt(container.dataset.limit) || 5,
                theme: container.dataset.theme || 'light',
                showImages: container.dataset.showImages !== 'false',
                showRating: container.dataset.showRating !== 'false',
                compact: container.dataset.compact === 'true'
            };
            
            this.init();
        }
        
        async init() {
            this.injectStyles();
            await this.loadTournaments();
        }
        
        injectStyles() {
            const styles = `
                .ccw-widget {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    max-width: 100%;
                    background: ${this.config.theme === 'dark' ? '#1e293b' : '#ffffff'};
                    color: ${this.config.theme === 'dark' ? '#f8fafc' : '#1e293b'};
                    border-radius: 12px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    padding: 1.5rem;
                }
                
                .ccw-header {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    margin-bottom: 1rem;
                    padding-bottom: 1rem;
                    border-bottom: 2px solid ${this.config.theme === 'dark' ? '#334155' : '#e2e8f0'};
                }
                
                .ccw-logo {
                    font-size: 1.5rem;
                }
                
                .ccw-title {
                    font-size: 1.25rem;
                    font-weight: 700;
                    margin: 0;
                }
                
                .ccw-tournament {
                    padding: 1rem;
                    margin-bottom: 0.75rem;
                    background: ${this.config.theme === 'dark' ? '#334155' : '#f8fafc'};
                    border-radius: 8px;
                    transition: all 0.3s ease;
                    text-decoration: none;
                    display: block;
                    color: inherit;
                }
                
                .ccw-tournament:hover {
                    transform: translateX(5px);
                    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
                }
                
                .ccw-tournament-name {
                    font-weight: 600;
                    margin-bottom: 0.5rem;
                    color: ${this.config.theme === 'dark' ? '#f8fafc' : '#1e293b'};
                }
                
                .ccw-tournament-info {
                    font-size: 0.875rem;
                    color: ${this.config.theme === 'dark' ? '#cbd5e1' : '#64748b'};
                    display: flex;
                    flex-wrap: wrap;
                    gap: 1rem;
                }
                
                .ccw-info-item {
                    display: flex;
                    align-items: center;
                    gap: 0.25rem;
                }
                
                .ccw-badge {
                    display: inline-block;
                    padding: 0.25rem 0.75rem;
                    background: #2563eb;
                    color: white;
                    border-radius: 20px;
                    font-size: 0.75rem;
                    font-weight: 600;
                    margin-top: 0.5rem;
                }
                
                .ccw-rating {
                    color: #fbbf24;
                    margin-top: 0.5rem;
                }
                
                .ccw-footer {
                    margin-top: 1rem;
                    padding-top: 1rem;
                    border-top: 1px solid ${this.config.theme === 'dark' ? '#334155' : '#e2e8f0'};
                    text-align: center;
                }
                
                .ccw-link {
                    color: #2563eb;
