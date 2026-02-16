// Lazy Loader Module for ChessCalendar-RU
// Implements component-based lazy loading for improved performance

class LazyLoader {
    constructor() {
        this.loadedModules = new Set();
        this.loadingPromises = new Map();
        this.moduleRegistry = new Map();
        this.observer = null;
        this.init();
    }

    init() {
        // Initialize intersection observer for component lazy loading
        if ('IntersectionObserver' in window) {
            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const component = entry.target;
                        this.loadComponent(component);
                        this.observer.unobserve(component);
                    }
                });
            }, {
                rootMargin: '50px' // Load 50px before entering viewport
            });
        }
        
        // Initialize dynamic imports for route-based modules
        this.setupRouteBasedLoading();
        
        // Initialize component detection
        this.observeComponents();
    }

    // Register a module for lazy loading
    registerModule(name, importFunction) {
        this.moduleRegistry.set(name, importFunction);
    }

    // Load a module by name
    async loadModule(name) {
        if (this.loadedModules.has(name)) {
            return Promise.resolve();
        }

        if (this.loadingPromises.has(name)) {
            return this.loadingPromises.get(name);
        }

        const importFunction = this.moduleRegistry.get(name);
        if (!importFunction) {
            console.warn(`Module ${name} not registered`);
            return Promise.resolve();
        }

        const promise = importFunction()
            .then(() => {
                this.loadedModules.add(name);
                this.loadingPromises.delete(name);
            })
            .catch(error => {
                console.error(`Failed to load module ${name}:`, error);
                this.loadingPromises.delete(name);
            });

        this.loadingPromises.set(name, promise);
        return promise;
    }

    // Observe components that should be lazily loaded
    observeComponents() {
        const lazyComponents = document.querySelectorAll('[data-lazy-component]');
        lazyComponents.forEach(component => {
            if (this.observer) {
                this.observer.observe(component);
            } else {
                // Fallback: load immediately if IntersectionObserver is not supported
                this.loadComponent(component);
            }
        });
    }

    // Load a specific component
    async loadComponent(element) {
        const componentName = element.dataset.lazyComponent;
        if (!componentName) return;

        // Add loading class
        element.classList.add('loading');
        
        try {
            await this.loadModule(componentName);
            
            // Dispatch custom event when component is loaded
            element.dispatchEvent(new CustomEvent('componentLoaded', {
                detail: { componentName }
            }));
            
            element.classList.remove('loading');
            element.classList.add('loaded');
        } catch (error) {
            console.error(`Failed to load component ${componentName}:`, error);
            element.classList.remove('loading');
            element.classList.add('load-error');
        }
    }

    // Setup route-based module loading
    setupRouteBasedLoading() {
        const currentPath = window.location.pathname;
        
        // Define route-to-module mappings
        const routeModules = this.getRouteModules(currentPath);
        
        // Preload critical modules for current route
        routeModules.critical.forEach(module => {
            this.loadModule(module).catch(console.error);
        });

        // Schedule non-critical modules for later loading
        setTimeout(() => {
            routeModules.nonCritical.forEach(module => {
                this.loadModule(module).catch(console.error);
            });
        }, 1000);
    }

    // Get modules for a specific route
    getRouteModules(path) {
        const modules = {
            critical: [],
            nonCritical: []
        };

        if (path === '/' || path.includes('/tournaments')) {
            modules.critical = ['search', 'filters'];
            modules.nonCritical = ['favorites', 'ratings', 'comparison'];
        } else if (path.includes('/calendar')) {
            modules.critical = ['calendar'];
            modules.nonCritical = ['export', 'print'];
        } else if (path.includes('/profile')) {
            modules.critical = ['user-profile'];
            modules.nonCritical = ['achievements', 'history'];
        } else if (path.includes('/admin')) {
            modules.critical = ['admin-dashboard'];
            modules.nonCritical = ['analytics', 'reports'];
        } else if (path.includes('/notifications')) {
            modules.critical = ['notifications'];
            modules.nonCritical = ['reminders'];
        } else if (path.includes('/recommendations')) {
            modules.critical = ['recommendations'];
            modules.nonCritical = ['ai-engine'];
        }

        return modules;
    }

    // Preload modules that might be needed soon
    preloadModules(moduleNames) {
        setTimeout(() => {
            moduleNames.forEach(moduleName => {
                if (!this.loadedModules.has(moduleName)) {
                    // Don't await, just trigger loading in background
                    this.loadModule(moduleName).catch(console.error);
                }
            });
        }, 2000); // Delay preload slightly to avoid impacting initial render
    }

    // Check if a module is loaded
    isModuleLoaded(name) {
        return this.loadedModules.has(name);
    }

    // Get loading status
    getLoadStatus() {
        return {
            loaded: Array.from(this.loadedModules),
            loading: Array.from(this.loadingPromises.keys()),
            totalRegistered: this.moduleRegistry.size
        };
    }
}

// Create global instance
const lazyLoader = new LazyLoader();

// Register all available modules
lazyLoader.registerModule('search', () => import('./search.js'));
lazyLoader.registerModule('filters', () => import('./filters.js'));
lazyLoader.registerModule('advanced-search', () => import('./advanced-search.js'));
lazyLoader.registerModule('quick-filters', () => import('./quick-filters.js'));
lazyLoader.registerModule('calendar', () => import('./calendar.js'));
lazyLoader.registerModule('enhanced-calendar', () => import('./enhanced-calendar.js'));
lazyLoader.registerModule('calendar-export', () => import('./calendar-export.js'));
lazyLoader.registerModule('print', () => import('./print-helper.js'));
lazyLoader.registerModule('favorites', () => import('./favorites.js'));
lazyLoader.registerModule('favorites-manager', () => import('./favorites-manager.js'));
lazyLoader.registerModule('ratings', () => import('./rating-system.js'));
lazyLoader.registerModule('comparison', () => import('./tournament-comparison.js'));
lazyLoader.registerModule('tournament-compare', () => import('./tournament-compare.js'));
lazyLoader.registerModule('user-profile', () => import('./profile.js')); // Assuming this exists or create new
lazyLoader.registerModule('achievements', () => import('./achievements-system.js'));
lazyLoader.registerModule('history', () => import('./tournament-history.js'));
lazyLoader.registerModule('admin-dashboard', () => import('./admin-dashboard.js'));
lazyLoader.registerModule('analytics', () => import('./analytics.js'));
lazyLoader.registerModule('reports', () => import('./reports.js')); // Assuming this exists or create new
lazyLoader.registerModule('notifications', () => import('./smart-notifications.js'));
lazyLoader.registerModule('reminders', () => import('./advanced-reminders.js'));
lazyLoader.registerModule('recommendations', () => import('./recommendations.js'));
lazyLoader.registerModule('ai-engine', () => import('./ai-recommendations.js')); // Assuming this exists or create new

// Export for global use
window.LazyLoader = lazyLoader;

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Preload modules that are likely to be needed based on user behavior
    const likelyModules = [];
    
    // If user is logged in, preload user-related modules
    if (document.body.classList.contains('user-logged-in') || document.querySelector('.user-menu')) {
        likelyModules.push('favorites', 'achievements', 'user-profile');
    }
    
    // Preload modules based on page type
    if (document.querySelector('.tournament-list') || document.querySelector('#tournamentGrid')) {
        likelyModules.push('comparison', 'filters');
    }
    
    if (document.querySelector('.calendar-container')) {
        likelyModules.push('calendar', 'calendar-export');
    }
    
    if (likelyModules.length > 0) {
        lazyLoader.preloadModules(likelyModules);
    }
});

// Add CSS for loading states
const style = document.createElement('style');
style.textContent = `
    [data-lazy-component] {
        opacity: 1;
        transition: opacity 0.3s ease;
    }
    
    [data-lazy-component].loading {
        opacity: 0.7;
        pointer-events: none;
    }
    
    [data-lazy-component].loaded {
        opacity: 1;
        pointer-events: auto;
    }
    
    [data-lazy-component].load-error {
        opacity: 1;
        border-left: 4px solid #dc3545;
    }
`;
document.head.appendChild(style);

// Export the lazy loader for external use
export default lazyLoader;