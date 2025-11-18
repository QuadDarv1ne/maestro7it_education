/**
 * Advanced Data Grid Component for Simple HR
 */
class DataGrid {
    constructor(container, options = {}) {
        this.container = typeof container === 'string' ? document.querySelector(container) : container;
        this.options = {
            data: [],
            columns: [],
            pageSize: 10,
            sortable: true,
            filterable: true,
            selectable: false,
            exportable: true,
            rowActions: [],
            bulkActions: [],
            height: 'auto',
            onRowClick: null,
            onSelectionChange: null,
            emptyMessage: 'Нет данных',
            loadingMessage: 'Загрузка...',
            ...options
        };
        
        this.state = {
            currentPage: 1,
            sortColumn: null,
            sortDirection: 'asc',
            filters: {},
            selectedRows: new Set(),
            data: [...this.options.data],
            filteredData: [...this.options.data]
        };
        
        this.init();
    }

    init() {
        this.render();
        this.attachEventListeners();
    }

    render() {
        this.container.innerHTML = '';
        this.container.className = 'data-grid-container';

        // Toolbar
        const toolbar = this.createToolbar();
        this.container.appendChild(toolbar);

        // Grid wrapper
        const gridWrapper = document.createElement('div');
        gridWrapper.className = 'data-grid-wrapper';
        if (this.options.height !== 'auto') {
            gridWrapper.style.height = this.options.height;
        }

        // Table
        const table = this.createTable();
        gridWrapper.appendChild(table);
        this.container.appendChild(gridWrapper);

        // Footer
        const footer = this.createFooter();
        this.container.appendChild(footer);
    }

    createToolbar() {
        const toolbar = document.createElement('div');
        toolbar.className = 'data-grid-toolbar';

        // Bulk actions
        if (this.options.bulkActions.length > 0 && this.options.selectable) {
            const bulkActionsDiv = document.createElement('div');
            bulkActionsDiv.className = 'data-grid-bulk-actions';
            bulkActionsDiv.innerHTML = `
                <span class="selected-count">Выбрано: <strong>0</strong></span>
                <div class="btn-group ms-2">
                    ${this.options.bulkActions.map(action => `
                        <button class="btn btn-sm btn-outline-primary bulk-action" data-action="${action.name}">
                            <i class="${action.icon}"></i> ${action.label}
                        </button>
                    `).join('')}
                </div>
            `;
            toolbar.appendChild(bulkActionsDiv);
        }

        // Search
        if (this.options.filterable) {
            const searchDiv = document.createElement('div');
            searchDiv.className = 'data-grid-search ms-auto';
            searchDiv.innerHTML = `
                <div class="input-group input-group-sm">
                    <span class="input-group-text">
                        <i class="fas fa-search"></i>
                    </span>
                    <input type="text" class="form-control global-search" placeholder="Поиск...">
                </div>
            `;
            toolbar.appendChild(searchDiv);
        }

        // Export buttons
        if (this.options.exportable) {
            const exportDiv = document.createElement('div');
            exportDiv.className = 'data-grid-export ms-2';
            exportDiv.innerHTML = `
                <div class="btn-group">
                    <button class="btn btn-sm btn-outline-secondary export-csv">
                        <i class="fas fa-file-csv"></i> CSV
                    </button>
                    <button class="btn btn-sm btn-outline-secondary export-excel">
                        <i class="fas fa-file-excel"></i> Excel
                    </button>
                    <button class="btn btn-sm btn-outline-secondary export-pdf">
                        <i class="fas fa-file-pdf"></i> PDF
                    </button>
                </div>
            `;
            toolbar.appendChild(exportDiv);
        }

        return toolbar;
    }

    createTable() {
        const table = document.createElement('table');
        table.className = 'table table-hover data-grid-table';

        // Header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');

        // Select all checkbox
        if (this.options.selectable) {
            const selectTh = document.createElement('th');
            selectTh.style.width = '40px';
            selectTh.innerHTML = `
                <input type="checkbox" class="form-check-input select-all">
            `;
            headerRow.appendChild(selectTh);
        }

        // Column headers
        this.options.columns.forEach(column => {
            const th = document.createElement('th');
            if (column.width) th.style.width = column.width;
            
            let content = column.label;
            
            if (this.options.sortable && column.sortable !== false) {
                th.className = 'sortable';
                th.dataset.field = column.field;
                content += ` <i class="fas fa-sort sort-icon"></i>`;
            }
            
            if (this.options.filterable && column.filterable !== false) {
                content += `
                    <div class="column-filter mt-1">
                        <input type="text" class="form-control form-control-sm" 
                               placeholder="Фильтр..." 
                               data-field="${column.field}">
                    </div>
                `;
            }
            
            th.innerHTML = content;
            headerRow.appendChild(th);
        });

        // Actions column
        if (this.options.rowActions.length > 0) {
            const actionsTh = document.createElement('th');
            actionsTh.textContent = 'Действия';
            actionsTh.style.width = '150px';
            headerRow.appendChild(actionsTh);
        }

        thead.appendChild(headerRow);
        table.appendChild(thead);

        // Body
        const tbody = this.createTableBody();
        table.appendChild(tbody);

        return table;
    }

    createTableBody() {
        const tbody = document.createElement('tbody');
        
        const startIndex = (this.state.currentPage - 1) * this.options.pageSize;
        const endIndex = startIndex + this.options.pageSize;
        const pageData = this.getFilteredAndSortedData().slice(startIndex, endIndex);

        if (pageData.length === 0) {
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            td.colSpan = this.options.columns.length + (this.options.selectable ? 1 : 0) + (this.options.rowActions.length > 0 ? 1 : 0);
            td.className = 'text-center text-muted py-4';
            td.innerHTML = `
                <i class="fas fa-inbox" style="font-size: 3rem;"></i>
                <div class="mt-2">${this.options.emptyMessage}</div>
            `;
            tr.appendChild(td);
            tbody.appendChild(tr);
            return tbody;
        }

        pageData.forEach((row, index) => {
            const tr = document.createElement('tr');
            tr.dataset.index = startIndex + index;

            // Select checkbox
            if (this.options.selectable) {
                const td = document.createElement('td');
                td.innerHTML = `
                    <input type="checkbox" class="form-check-input row-select" data-index="${startIndex + index}">
                `;
                tr.appendChild(td);
            }

            // Data columns
            this.options.columns.forEach(column => {
                const td = document.createElement('td');
                const value = this.getNestedValue(row, column.field);
                
                if (column.render) {
                    td.innerHTML = column.render(value, row);
                } else if (column.format) {
                    td.textContent = column.format(value);
                } else {
                    td.textContent = value || '';
                }
                
                tr.appendChild(td);
            });

            // Actions
            if (this.options.rowActions.length > 0) {
                const td = document.createElement('td');
                td.innerHTML = `
                    <div class="btn-group btn-group-sm">
                        ${this.options.rowActions.map(action => `
                            <button class="btn btn-outline-${action.variant || 'primary'} row-action" 
                                    data-action="${action.name}" 
                                    data-index="${startIndex + index}"
                                    title="${action.label}">
                                <i class="${action.icon}"></i>
                            </button>
                        `).join('')}
                    </div>
                `;
                tr.appendChild(td);
            }

            tbody.appendChild(tr);
        });

        return tbody;
    }

    createFooter() {
        const footer = document.createElement('div');
        footer.className = 'data-grid-footer';

        const totalRecords = this.getFilteredAndSortedData().length;
        const totalPages = Math.ceil(totalRecords / this.options.pageSize);

        footer.innerHTML = `
            <div class="data-grid-info">
                Показано ${Math.min((this.state.currentPage - 1) * this.options.pageSize + 1, totalRecords)}-${Math.min(this.state.currentPage * this.options.pageSize, totalRecords)} из ${totalRecords}
            </div>
            <nav aria-label="Навигация по страницам">
                <ul class="pagination pagination-sm mb-0">
                    ${this.createPaginationButtons(totalPages)}
                </ul>
            </nav>
        `;

        return footer;
    }

    createPaginationButtons(totalPages) {
        if (totalPages <= 1) return '';

        let buttons = '';

        // Previous
        buttons += `
            <li class="page-item ${this.state.currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link pagination-btn" href="#" data-page="${this.state.currentPage - 1}">
                    <i class="fas fa-chevron-left"></i>
                </a>
            </li>
        `;

        // Page numbers
        const maxButtons = 5;
        let startPage = Math.max(1, this.state.currentPage - Math.floor(maxButtons / 2));
        let endPage = Math.min(totalPages, startPage + maxButtons - 1);

        if (endPage - startPage < maxButtons - 1) {
            startPage = Math.max(1, endPage - maxButtons + 1);
        }

        if (startPage > 1) {
            buttons += `<li class="page-item"><a class="page-link pagination-btn" href="#" data-page="1">1</a></li>`;
            if (startPage > 2) {
                buttons += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
            }
        }

        for (let i = startPage; i <= endPage; i++) {
            buttons += `
                <li class="page-item ${i === this.state.currentPage ? 'active' : ''}">
                    <a class="page-link pagination-btn" href="#" data-page="${i}">${i}</a>
                </li>
            `;
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                buttons += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
            }
            buttons += `<li class="page-item"><a class="page-link pagination-btn" href="#" data-page="${totalPages}">${totalPages}</a></li>`;
        }

        // Next
        buttons += `
            <li class="page-item ${this.state.currentPage === totalPages ? 'disabled' : ''}">
                <a class="page-link pagination-btn" href="#" data-page="${this.state.currentPage + 1}">
                    <i class="fas fa-chevron-right"></i>
                </a>
            </li>
        `;

        return buttons;
    }

    attachEventListeners() {
        // Sorting
        this.container.addEventListener('click', (e) => {
            const sortable = e.target.closest('th.sortable');
            if (sortable) {
                const field = sortable.dataset.field;
                this.sort(field);
            }
        });

        // Filtering
        this.container.addEventListener('input', (e) => {
            if (e.target.classList.contains('column-filter')) {
                const field = e.target.dataset.field;
                this.filter(field, e.target.value);
            } else if (e.target.classList.contains('global-search')) {
                this.globalSearch(e.target.value);
            }
        });

        // Pagination
        this.container.addEventListener('click', (e) => {
            if (e.target.closest('.pagination-btn')) {
                e.preventDefault();
                const page = parseInt(e.target.closest('.pagination-btn').dataset.page);
                if (page > 0) this.goToPage(page);
            }
        });

        // Selection
        this.container.addEventListener('change', (e) => {
            if (e.target.classList.contains('select-all')) {
                this.selectAll(e.target.checked);
            } else if (e.target.classList.contains('row-select')) {
                this.toggleRowSelection(parseInt(e.target.dataset.index));
            }
        });

        // Row actions
        this.container.addEventListener('click', (e) => {
            const actionBtn = e.target.closest('.row-action');
            if (actionBtn) {
                const action = actionBtn.dataset.action;
                const index = parseInt(actionBtn.dataset.index);
                const row = this.state.filteredData[index];
                const actionConfig = this.options.rowActions.find(a => a.name === action);
                if (actionConfig && actionConfig.handler) {
                    actionConfig.handler(row, index);
                }
            }
        });

        // Bulk actions
        this.container.addEventListener('click', (e) => {
            const bulkBtn = e.target.closest('.bulk-action');
            if (bulkBtn) {
                const action = bulkBtn.dataset.action;
                const selectedRows = Array.from(this.state.selectedRows).map(i => this.state.filteredData[i]);
                const actionConfig = this.options.bulkActions.find(a => a.name === action);
                if (actionConfig && actionConfig.handler) {
                    actionConfig.handler(selectedRows);
                }
            }
        });

        // Export
        this.container.addEventListener('click', (e) => {
            if (e.target.closest('.export-csv')) {
                this.exportToCSV();
            } else if (e.target.closest('.export-excel')) {
                this.exportToExcel();
            } else if (e.target.closest('.export-pdf')) {
                this.exportToPDF();
            }
        });
    }

    sort(field) {
        if (this.state.sortColumn === field) {
            this.state.sortDirection = this.state.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            this.state.sortColumn = field;
            this.state.sortDirection = 'asc';
        }

        this.updateSortIcons();
        this.render();
    }

    updateSortIcons() {
        const headers = this.container.querySelectorAll('th.sortable');
        headers.forEach(th => {
            const icon = th.querySelector('.sort-icon');
            if (icon) {
                if (th.dataset.field === this.state.sortColumn) {
                    icon.className = `fas fa-sort-${this.state.sortDirection === 'asc' ? 'up' : 'down'} sort-icon`;
                } else {
                    icon.className = 'fas fa-sort sort-icon';
                }
            }
        });
    }

    filter(field, value) {
        if (value) {
            this.state.filters[field] = value.toLowerCase();
        } else {
            delete this.state.filters[field];
        }
        
        this.state.currentPage = 1;
        this.applyFilters();
        this.render();
    }

    globalSearch(query) {
        const lowerQuery = query.toLowerCase();
        
        if (!query) {
            this.state.filteredData = [...this.state.data];
        } else {
            this.state.filteredData = this.state.data.filter(row => {
                return this.options.columns.some(column => {
                    const value = this.getNestedValue(row, column.field);
                    return value && value.toString().toLowerCase().includes(lowerQuery);
                });
            });
        }
        
        this.state.currentPage = 1;
        this.render();
    }

    applyFilters() {
        this.state.filteredData = this.state.data.filter(row => {
            return Object.entries(this.state.filters).every(([field, value]) => {
                const cellValue = this.getNestedValue(row, field);
                return cellValue && cellValue.toString().toLowerCase().includes(value);
            });
        });
    }

    getFilteredAndSortedData() {
        let data = [...this.state.filteredData];

        if (this.state.sortColumn) {
            data.sort((a, b) => {
                const aVal = this.getNestedValue(a, this.state.sortColumn);
                const bVal = this.getNestedValue(b, this.state.sortColumn);

                let comparison = 0;
                if (aVal < bVal) comparison = -1;
                if (aVal > bVal) comparison = 1;

                return this.state.sortDirection === 'asc' ? comparison : -comparison;
            });
        }

        return data;
    }

    getNestedValue(obj, path) {
        return path.split('.').reduce((current, prop) => current?.[prop], obj);
    }

    goToPage(page) {
        this.state.currentPage = page;
        this.render();
    }

    selectAll(checked) {
        if (checked) {
            const startIndex = (this.state.currentPage - 1) * this.options.pageSize;
            const endIndex = startIndex + this.options.pageSize;
            for (let i = startIndex; i < Math.min(endIndex, this.state.filteredData.length); i++) {
                this.state.selectedRows.add(i);
            }
        } else {
            this.state.selectedRows.clear();
        }
        
        this.updateSelectionUI();
    }

    toggleRowSelection(index) {
        if (this.state.selectedRows.has(index)) {
            this.state.selectedRows.delete(index);
        } else {
            this.state.selectedRows.add(index);
        }
        
        this.updateSelectionUI();
    }

    updateSelectionUI() {
        const count = this.state.selectedRows.size;
        const countEl = this.container.querySelector('.selected-count strong');
        if (countEl) countEl.textContent = count;

        if (this.options.onSelectionChange) {
            const selectedData = Array.from(this.state.selectedRows).map(i => this.state.filteredData[i]);
            this.options.onSelectionChange(selectedData);
        }
    }

    exportToCSV() {
        const data = this.getFilteredAndSortedData();
        let csv = this.options.columns.map(col => col.label).join(',') + '\n';
        
        data.forEach(row => {
            csv += this.options.columns.map(col => {
                const value = this.getNestedValue(row, col.field);
                return `"${value || ''}"`;
            }).join(',') + '\n';
        });

        this.downloadFile(csv, 'data.csv', 'text/csv');
    }

    exportToExcel() {
        showInfo('Экспорт в Excel будет доступен в следующей версии');
    }

    exportToPDF() {
        showInfo('Экспорт в PDF будет доступен в следующей версии');
    }

    downloadFile(content, filename, type) {
        const blob = new Blob([content], { type });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.click();
        URL.revokeObjectURL(url);
    }

    setData(data) {
        this.state.data = data;
        this.state.filteredData = [...data];
        this.state.currentPage = 1;
        this.state.selectedRows.clear();
        this.render();
    }

    refresh() {
        this.render();
    }
}

// Export
window.DataGrid = DataGrid;
