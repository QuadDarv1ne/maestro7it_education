// ChessCalendar-RU Analytics Tracking

class Analytics {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.events = [];
        this.maxEvents = 100;
        this.flushInterval = 30000; // 30 seconds
        
        this.init();
    }
    
    init() {
        // Track page views
        this.trackPageView();
        
        // Track user interactions
        this.setupEventListeners();
        
        // Periodic flush
        setInterval(() => this.flush(), this.flushInterval);
        
        // Flush on page unload
        window.addEventListener('beforeunload', () => this.flush(true));
        
        // Track performance metrics
        this.trackPerformance();
    }
    
    generateSessionId() {
        return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }
    
    trackPageView() {
        this.track('page_view', {
            url: window.location.href,
            path: window.location.pathname,
            title: document.title,
            referrer: document.referrer,
            timestamp: new Date().toISOString()
        });
    }
    
    track(eventName, data = {}) {
        const event = {
            event: eventName,
            session_id: this.sessionId,
            timestamp: new Date().toISOString(),
            user_agent: navigator.userAgent,
            screen_resolution: `${window.screen.width}x${window.screen.height}`,
            viewport_size: `${window.innerWidth}x${window.innerHeight}`,
            ...data
        };
        
        this.events.push(event);
        
        // Auto flush if too many events
        if (this.events.length >= this.maxEvents) {
            this.flush();
        }
        
        console.log('[Analytics]', eventName, data);
    }
    
    setupEventListeners() {
        // Track clicks on important elements
        document.addEventListener('click', (e) => {
            const target = e.target.closest('a, button, .card, .tournament-card');
            if (target) {
                const eventData = {
                    element: target.tagName.toLowerCase(),
                    text: target.textContent.trim().substring(0, 50),
                    href: target.href || null,
                    classes: target.className
                };
                
                if (target.closest('.tournament-card')) {
                    this.track('tournament_click', eventData);
                } else if (target.tagName === 'A') {
                    this.track('link_click', eventData);
                } else if (target.tagName === 'BUTTON') {
                    this.track('button_click', eventData);
                }
            }
        });
        
        // Track search queries
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            let searchTimer;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimer);
                searchTimer = setTimeout(() => {
                    if (e.target.value.trim().length >= 2) {
                        this.track('search', {
                            query: e.target.value.trim(),
                            query_length: e.target.value.trim().length
                        });
                    }
                }, 1000);
            });
        }
        
        // Track form submissions
        document.addEventListener('submit', (e) => {
            const form = e.target;
            this.track('form_submit', {
                form_id: form.id || 'unknown',
                form_action: form.action,
                form_method: form.method
            });
        });
        
        // Track scroll depth
        let maxScroll = 0;
        let scrollTimer;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimer);
            scrollTimer = setTimeout(() => {
                const scrollPercent = Math.round(
                    (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100
                );
                
                if (scrollPercent > maxScroll) {
                    maxScroll = scrollPercent;
                    
                    // Track milestones
                    if ([25, 50, 75, 100].includes(scrollPercent)) {
                        this.track('scroll_depth', {
                            depth: scrollPercent,
                            page: window.location.pathname
                        });
                    }
                }
            }, 500);
        });
        
        // Track time on page
        let startTime = Date.now();
        window.addEventListener('beforeunload', () => {
            const timeOnPage = Math.round((Date.now() - startTime) / 1000);
            this.track('time_on_page', {
                duration_seconds: timeOnPage,
                page: window.location.pathname
            });
        });
        
        // Track errors
        window.addEventListener('error', (e) => {
            this.track('javascript_error', {
                message: e.message,
                filename: e.filename,
                line: e.lineno,
                column: e.colno,
                stack: e.error?.stack?.substring(0, 500)
            });
        });
        
        // Track unhandled promise rejections
        window.addEventListener('unhandledrejection', (e) => {
            this.track('promise_rejection', {
                reason: e.reason?.toString().substring(0, 500)
            });
        });
    }
    
    trackPerformance() {
        if ('performance' in window) {
            window.addEventListener('load', () => {
                setTimeout(() => {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    if (perfData) {
                        this.track('performance', {
                            dns_time: Math.round(perfData.domainLookupEnd - perfData.domainLookupStart),
                            tcp_time: Math.round(perfData.connectEnd - perfData.connectStart),
                            request_time: Math.round(perfData.responseStart - perfData.requestStart),
                            response_time: Math.round(perfData.responseEnd - perfData.responseStart),
                            dom_processing: Math.round(perfData.domComplete - perfData.domInteractive),
                            load_time: Math.round(perfData.loadEventEnd - perfData.loadEventStart),
                            total_time: Math.round(perfData.loadEventEnd - perfData.fetchStart)
                        });
                    }
                    
                    // Track resource timing
                    const resources = performance.getEntriesByType('resource');
                    const slowResources = resources
                        .filter(r => r.duration > 1000)
                        .map(r => ({
                            name: r.name,
                            duration: Math.round(r.duration),
                            size: r.transferSize
                        }));
                    
                    if (slowResources.length > 0) {
                        this.track('slow_resources', {
                            resources: slowResources.slice(0, 10)
                        });
                    }
                }, 0);
            });
        }
    }
    
    async flush(sync = false) {
        if (this.events.length === 0) return;
        
        const eventsToSend = [...this.events];
        this.events = [];
        
        const payload = {
            events: eventsToSend,
            session_id: this.sessionId
        };
        
        try {
            if (sync && navigator.sendBeacon) {
                // Use sendBeacon for synchronous sending on page unload
                const blob = new Blob([JSON.stringify(payload)], { type: 'application/json' });
                navigator.sendBeacon('/api/analytics', blob);
            } else {
                // Regular async request
                await fetch('/api/analytics', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });
            }
            
            console.log('[Analytics] Flushed', eventsToSend.length, 'events');
        } catch (error) {
            console.error('[Analytics] Flush failed:', error);
            // Re-add events if failed
            this.events = [...eventsToSend, ...this.events].slice(0, this.maxEvents);
        }
    }
    
    // Public API
    trackEvent(name, data) {
        this.track(name, data);
    }
    
    trackTournamentView(tournamentId, tournamentName) {
        this.track('tournament_view', {
            tournament_id: tournamentId,
            tournament_name: tournamentName
        });
    }
    
    trackFavoriteAdd(tournamentId) {
        this.track('favorite_add', {
            tournament_id: tournamentId
        });
    }
    
    trackFavoriteRemove(tournamentId) {
        this.track('favorite_remove', {
            tournament_id: tournamentId
        });
    }
    
    trackShare(method, url) {
        this.track('share', {
            method: method,
            url: url
        });
    }
    
    trackNotificationSubscribe(tournamentId) {
        this.track('notification_subscribe', {
            tournament_id: tournamentId
        });
    }
}

// Initialize analytics
const analytics = new Analytics();

// Export for global use
window.ChessCalendarAnalytics = analytics;

// Add convenience methods to ChessCalendar object
if (window.ChessCalendar) {
    window.ChessCalendar.analytics = analytics;
}

console.log('[Analytics] Initialized');
