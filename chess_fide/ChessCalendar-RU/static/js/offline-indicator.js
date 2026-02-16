// Offline Indicator - индикатор работы офлайн

class OfflineIndicator {
    constructor() {
        this.isOnline = navigator.onLine;
        this.init();
    }

    init() {
        this.createIndicator();
        this.attachEventListeners();
        this.checkConnection();
    }

    createIndicator() {
        // Проверяем, не создан ли уже индикатор
        if (document.getElementById('offlineIndicator')) return;

        const indicator = document.createElement('div');
        indicator.id = 'offlineIndicator';
        indicator.innerHTML = `
            <style>
                #offlineIndicator {
                    position: fixed;
                    top: 70px;
                    left: 50%;
                    transform: translateX(-50%) translateY(-100px);
                    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                    color: white;
                    padding: 1rem 2rem;
                    border-radius: 12px;
                    box-shadow: 0 8px 24px rgba(239, 68, 68, 0.4);
                    z-index: 9999;
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                    font-weight: 600;
                    transition: transform 0.3s ease;
                    pointer-events: none;
                }
                
                #offlineIndicator.show {
                    transform: translateX(-50%) translateY(0);
                    pointer-events: all;
                }
                
                #offlineIndicator.online {
                    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                    box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
                }
                
                .offline-icon {
                    font-size: 1.5rem;
                    animation: pulse 2s ease-in-out infinite;
                }
                
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }
                
                .offline-message {
                    display: flex;
                    flex-direction: column;
                    gap: 0.25rem;
                }
                
                .offline-title {
                    font-size: 1rem;
                    font-weight: 700;
                }
                
                .offline-subtitle {
                    font-size: 0.875rem;
                    opacity: 0.9;
                }
                
                .offline-close {
                    background: rgba(255, 255, 255, 0.2);
                    border: none;
                    color: white;
                    width: 28px;
                    height: 28px;
                    border-radius: 50%;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 0.2s ease;
                    margin-left: 1rem;
                }
                
                .offline-close:hover {
                    background: rgba(255, 255, 255, 0.3);
                }
                
                @media (max-width: 768px) {
                    #offlineIndicator {
                        top: 60px;
                        left: 1rem;
                        right: 1rem;
                        transform: translateY(-100px);
                        padding: 0.875rem 1.25rem;
                    }
                    
                    #offlineIndicator.show {
                        transform: translateY(0);
                    }
                    
                    .offline-title {
                        font-size: 0.9rem;
                    }
                    
                    .offline-subtitle {
                        font-size: 0.8rem;
                    }
                }
            </style>
            
            <div class="offline-icon">
                <i class="bi bi-wifi-off"></i>
            </div>
            <div class="offline-message">
                <div class="offline-title">Нет подключения к интернету</div>
                <div class="offline-subtitle">Некоторые функции могут быть недоступны</div>
            </div>
            <button class="offline-close" onclick="offlineIndicator.hide()">
                <i class="bi bi-x"></i>
            </button>
        `;

        document.body.appendChild(indicator);
    }

    attachEventListeners() {
        window.addEventListener('online', () => this.handleOnline());
        window.addEventListener('offline', () => this.handleOffline());
        
        // Периодическая проверка соединения
        setInterval(() => this.checkConnection(), 30000); // Каждые 30 секунд
    }

    handleOnline() {
        this.isOnline = true;
        this.showOnlineMessage();
        
        // Обновляем кэш
        if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
            navigator.serviceWorker.controller.postMessage({
                type: 'SYNC_CACHE'
            });
        }
    }

    handleOffline() {
        this.isOnline = false;
        this.showOfflineMessage();
    }

    showOfflineMessage() {
        const indicator = document.getElementById('offlineIndicator');
        if (!indicator) return;

        indicator.classList.remove('online');
        indicator.querySelector('.offline-icon i').className = 'bi bi-wifi-off';
        indicator.querySelector('.offline-title').textContent = 'Нет подключения к интернету';
        indicator.querySelector('.offline-subtitle').textContent = 'Некоторые функции могут быть недоступны';
        
        indicator.classList.add('show');
        
        if (window.toast) {
            window.toast.warning('Потеряно подключение к интернету');
        }
    }

    showOnlineMessage() {
        const indicator = document.getElementById('offlineIndicator');
        if (!indicator) return;

        indicator.classList.add('online');
        indicator.querySelector('.offline-icon i').className = 'bi bi-wifi';
        indicator.querySelector('.offline-title').textContent = 'Подключение восстановлено';
        indicator.querySelector('.offline-subtitle').textContent = 'Все функции доступны';
        
        indicator.classList.add('show');
        
        if (window.toast) {
            window.toast.success('Подключение к интернету восстановлено');
        }
        
        // Автоматически скрываем через 3 секунды
        setTimeout(() => this.hide(), 3000);
    }

    hide() {
        const indicator = document.getElementById('offlineIndicator');
        if (indicator) {
            indicator.classList.remove('show');
        }
    }

    async checkConnection() {
        try {
            const response = await fetch('/health', {
                method: 'HEAD',
                cache: 'no-cache'
            });
            
            if (response.ok && !this.isOnline) {
                this.handleOnline();
            }
        } catch (error) {
            if (this.isOnline) {
                this.handleOffline();
            }
        }
    }

    getStatus() {
        return {
            online: this.isOnline,
            effectiveType: navigator.connection?.effectiveType || 'unknown',
            downlink: navigator.connection?.downlink || 0,
            rtt: navigator.connection?.rtt || 0
        };
    }
}

// Инициализация
const offlineIndicator = new OfflineIndicator();
window.offlineIndicator = offlineIndicator;

// Показываем индикатор если офлайн при загрузке
if (!navigator.onLine) {
    setTimeout(() => offlineIndicator.showOfflineMessage(), 1000);
}
