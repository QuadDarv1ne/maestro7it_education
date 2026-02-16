// Quick Filters - предустановленные фильтры для быстрого доступа

class QuickFilters {
    constructor() {
        this.filters = [
            {
                id: 'upcoming',
                name: 'Предстоящие',
                icon: 'bi-calendar-plus',
                color: '#2563eb',
                params: { status: 'Scheduled' }
            },
            {
                id: 'ongoing',
                name: 'Идут сейчас',
                icon: 'bi-play-circle',
                color: '#10b981',
                params: { status: 'Ongoing' }
            },
            {
                id: 'international',
                name: 'Международные',
                icon: 'bi-globe',
                color: '#06b6d4',
                params: { category: 'International' }
            },
            {
                id: 'this_month',
                name: 'В этом месяце',
                icon: 'bi-calendar-month',
                color: '#f59e0b',
                custom: true
            },
            {
                id: 'with_prize',
                name: 'С призовым фондом',
                icon: 'bi-cash-coin',
                color: '#10b981',
                custom: true
            },
            {
                id: 'moscow',
                name: 'Москва',
                icon: 'bi-geo-alt',
                color: '#ef4444',
                params: { location: 'Москва' }
            },
            {
                id: 'spb',
                name: 'Санкт-Петербург',
                icon: 'bi-geo-alt',
                color: '#8b5cf6',
                params: { location: 'Санкт-Петербург' }
            },
            {
                id: 'recent',
                name: 'Недавно добавленные',
                icon: 'bi-star',
                color: '#f59e0b',
                params: { sort_by: 'created_at' }
            }
        ];
        
        this.init();
    }

    init() {
        this.createQuickFiltersBar();
        this.attachEventListeners();
    }

    createQuickFiltersBar() {
        // Проверяем, находимся ли мы на главной странице
        if (window.location.pathname !== '/' && !window.location.pathname.includes('/tournaments')) {
            return;
        }

        // Проверяем, не создан ли уже виджет
        if (document.getElementById('quickFiltersBar')) return;

        const bar = document.createElement('div');
        bar.id = 'quickFiltersBar';
        bar.innerHTML = `
            <style>
                #quickFiltersBar {
                    background: var(--bg-primary);
                    padding: 1rem 0;
                    margin-bottom: 1.5rem;
                    border-radius: 12px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                }
                
                .quick-filters-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 0 1.25rem 0.75rem;
                    border-bottom: 2px solid var(--border-color);
                    margin-bottom: 1rem;
                }
                
                .quick-filters-header h6 {
                    margin: 0;
                    font-weight: 700;
                    color: var(--text-primary);
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                
                .quick-filters-container {
                    display: flex;
                    gap: 0.75rem;
                    padding: 0 1.25rem;
                    overflow-x: auto;
                    scrollbar-width: thin;
                    scrollbar-color: var(--primary-color) var(--bg-secondary);
                }
                
                .quick-filters-container::-webkit-scrollbar {
                    height: 6px;
                }
                
                .quick-filters-container::-webkit-scrollbar-track {
                    background: var(--bg-secondary);
                    border-radius: 3px;
                }
                
                .quick-filters-container::-webkit-scrollbar-thumb {
                    background: var(--primary-color);
                    border-radius: 3px;
                }
                
                .quick-filter-chip {
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                    padding: 0.6rem 1.25rem;
                    border-radius: 25px;
                    border: 2px solid var(--border-color);
                    background: var(--bg-primary);
                    color: var(--text-primary);
                    font-weight: 600;
                    font-size: 0.875rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    white-space: nowrap;
                    user-select: none;
                }
                
                .quick-filter-chip:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                }
                
                .quick-filter-chip.active {
                    border-color: var(--chip-color);
                    background: var(--chip-color);
                    color: white;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                }
                
                .quick-filter-chip i {
                    font-size: 1rem;
                }
                
                .filter-count {
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    min-width: 20px;
                    height: 20px;
                    padding: 0 0.4rem;
                    background: rgba(255, 255, 255, 0.3);
                    border-radius: 10px;
                    font-size: 0.75rem;
                    font-weight: 700;
                }
                
                .quick-filter-chip.active .filter-count {
                    background: rgba(255, 255, 255, 0.4);
                }
                
                .clear-filters-btn {
                    padding: 0.4rem 1rem;
                    background: var(--danger-color);
                    color: white;
                    border: none;
                    border-radius: 20px;
                    font-size: 0.875rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    display: none;
                }
                
                .clear-filters-btn.visible {
                    display: inline-block;
                }
                
                .clear-filters-btn:hover {
                    filter: brightness(1.1);
                }
                
                @media (max-width: 768px) {
                    #quickFiltersBar {
                        margin-bottom: 1rem;
                    }
                    
                    .quick-filters-header {
                        padding: 0 1rem 0.5rem;
                    }
                    
                    .quick-filters-container {
                        padding: 0 1rem;
                        gap: 0.5rem;
                    }
                    
                    .quick-filter-chip {
                        padding: 0.5rem 1rem;
                        font-size: 0.8rem;
                    }
                }
            </style>
            
            <div class="quick-filters-header">
                <h6><i class="bi bi-lightning-charge-fill"></i> Быстрые фильтры</h6>
                <button class="clear-filters-btn" id="clearQuickFilters">
                    <i class="bi bi-x-circle"></i> Сбросить
                </button>
            </div>
            
            <div class="quick-filters-container">
                ${this.renderFilters()}
            </div>
        `;

        // Вставляем перед списком турниров
        const container = document.querySelector('.container');
        const filterForm = document.querySelector('.filter-form');
        
        if (container && filterForm) {
            filterForm.parentNode.insertBefore(bar, filterForm.nextSibling);
        }
    }

    renderFilters() {
        return this.filters.map(filter => `
            <div class="quick-filter-chip" 
                 data-filter-id="${filter.id}"
                 style="--chip-color: ${filter.color}">
                <i class="${filter.icon}"></i>
                <span>${filter.name}</span>
            </div>
        `).join('');
    }

    attachEventListeners() {
        // Клик по фильтру
        document.addEventListener('click', (e) => {
            const chip = e.target.closest('.quick-filter-chip');
            if (chip) {
                const filterId = chip.dataset.filterId;
                this.applyFilter(filterId, chip);
            }
        });

        // Кнопка сброса
        const clearBtn = document.getElementById('clearQuickFilters');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearAllFilters());
        }

        // Проверяем активные фильтры при загрузке
        this.checkActiveFilters();
    }

    applyFilter(filterId, chipElement) {
        const filter = this.filters.find(f => f.id === filterId);
        if (!filter) return;

        // Убираем активность со всех чипов
        document.querySelectorAll('.quick-filter-chip').forEach(chip => {
            chip.classList.remove('active');
        });

        // Активируем текущий чип
        chipElement.classList.add('active');

        // Показываем кнопку сброса
        const clearBtn = document.getElementById('clearQuickFilters');
        if (clearBtn) {
            clearBtn.classList.add('visible');
        }

        // Применяем фильтр
        if (filter.custom) {
            this.applyCustomFilter(filterId);
        } else {
            this.applyStandardFilter(filter.params);
        }

        // Track achievement
        if (window.achievementsSystem) {
            window.achievementsSystem.trackAction('filter_used');
        }

        // Show toast
        if (window.toast) {
            window.toast.info(`Применён фильтр: ${filter.name}`);
        }
    }

    applyStandardFilter(params) {
        const url = new URL(window.location.href);
        
        // Очищаем старые параметры фильтрации
        url.searchParams.delete('category');
        url.searchParams.delete('status');
        url.searchParams.delete('location');
        url.searchParams.delete('sort_by');
        
        // Добавляем новые параметры
        Object.keys(params).forEach(key => {
            url.searchParams.set(key, params[key]);
        });
        
        // Перенаправляем
        window.location.href = url.toString();
    }

    applyCustomFilter(filterId) {
        const url = new URL(window.location.href);
        
        switch (filterId) {
            case 'this_month':
                // Фильтр по текущему месяцу
                const now = new Date();
                const year = now.getFullYear();
                const month = String(now.getMonth() + 1).padStart(2, '0');
                url.searchParams.set('date_from', `${year}-${month}-01`);
                url.searchParams.set('date_to', `${year}-${month}-31`);
                break;
                
            case 'with_prize':
                // Фильтр турниров с призовым фондом
                url.searchParams.set('has_prize', 'true');
                break;
        }
        
        window.location.href = url.toString();
    }

    clearAllFilters() {
        // Убираем все активные чипы
        document.querySelectorAll('.quick-filter-chip').forEach(chip => {
            chip.classList.remove('active');
        });

        // Скрываем кнопку сброса
        const clearBtn = document.getElementById('clearQuickFilters');
        if (clearBtn) {
            clearBtn.classList.remove('visible');
        }

        // Перенаправляем на главную без параметров
        window.location.href = window.location.pathname;
    }

    checkActiveFilters() {
        const url = new URL(window.location.href);
        
        // Проверяем каждый фильтр
        this.filters.forEach(filter => {
            if (filter.custom) return;
            
            let isActive = true;
            Object.keys(filter.params).forEach(key => {
                if (url.searchParams.get(key) !== filter.params[key]) {
                    isActive = false;
                }
            });
            
            if (isActive) {
                const chip = document.querySelector(`[data-filter-id="${filter.id}"]`);
                if (chip) {
                    chip.classList.add('active');
                    
                    // Показываем кнопку сброса
                    const clearBtn = document.getElementById('clearQuickFilters');
                    if (clearBtn) {
                        clearBtn.classList.add('visible');
                    }
                }
            }
        });
    }

    addCustomFilter(filter) {
        this.filters.push(filter);
        
        // Обновляем виджет
        const container = document.querySelector('.quick-filters-container');
        if (container) {
            container.innerHTML = this.renderFilters();
        }
    }
}

// Инициализация
if (window.location.pathname === '/' || window.location.pathname.includes('/tournaments')) {
    const quickFilters = new QuickFilters();
    window.quickFilters = quickFilters;
}
