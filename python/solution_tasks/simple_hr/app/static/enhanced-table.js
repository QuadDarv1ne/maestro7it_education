/**
 * Enhanced Table Component for Simple HR
 */
class EnhancedTable {
    constructor(tableElement, options = {}) {
        this.table = tableElement;
        this.options = {
            sortable: true,
            filterable: true,
            pagination: true,
            itemsPerPage: 10,
            searchPlaceholder: 'Поиск...',
            noDataText: 'Нет данных для отображения',
            showEntriesText: 'Показано {start} - {end} из {total}',
            ...options
        };
        
        this.data = [];
        this.filteredData = [];
        this.currentPage = 1;
        this.sortColumn = null;
        this.sortDirection = 'asc';
        this.searchQuery = '';
        
        this.init();
    }

    init() {
        this.extractData();
        this.createControls();
        this.setupEventListeners();
        this.render();
    }

    extractData() {
        const rows = this.table.querySelectorAll('tbody tr');
        this.data = Array.from(rows).map((row, index) => {
            const cells = row.querySelectorAll('td');
            return {
                index,
                element: row,
                data: Array.from(cells).map(cell => cell.textContent.trim()),
                rawData: Array.from(cells).map(cell => cell.innerHTML)
            };
        });
        this.filteredData = [...this.data];
    }

    createControls() {
        // Create wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'enhanced-table-wrapper';
        this.table.parentNode.insertBefore(wrapper, this.table);
        wrapper.appendChild(this.table);

        // Create header with search and entries selector
        if (this.options.filterable || this.options.pagination) {
            const header = document.createElement('div');
            header.className = 'enhanced-table-header d-flex justify-content-between align-items-center mb-3';
            
            if (this.options.pagination) {
                const entriesSelector = document.createElement('div');
                entriesSelector.className = 'enhanced-table-entries';
                entriesSelector.innerHTML = `
                    <label class="d-flex align-items-center gap-2">
                        <span>Показать</span>
                        <select class="form-select form-select-sm" style="width: auto;">
                            <option value="10" ${this.options.itemsPerPage === 10 ? 'selected' : ''}>10</option>
                            <option value="25" ${this.options.itemsPerPage === 25 ? 'selected' : ''}>25</option>
                            <option value="50" ${this.options.itemsPerPage === 50 ? 'selected' : ''}>50</option>
                            <option value="100" ${this.options.itemsPerPage === 100 ? 'selected' : ''}>100</option>
                        </select>
                        <span>записей</span>
                    </label>
                `;
                header.appendChild(entriesSelector);
                
                this.entriesSelect = entriesSelector.querySelector('select');
            }

            if (this.options.filterable) {
                const searchBox = document.createElement('div');
                searchBox.className = 'enhanced-table-search';
                searchBox.innerHTML = `
                    <div class="input-group" style="width: 300px;">
                        <span class="input-group-text">
                            <i class="bi bi-search"></i>
                        </span>
                        <input type="text" class="form-control" placeholder="${this.options.searchPlaceholder}">
                    </div>
                `;
                header.appendChild(searchBox);
                
                this.searchInput = searchBox.querySelector('input');
            }

            wrapper.insertBefore(header, this.table);
        }

        // Create footer with pagination and info
        if (this.options.pagination) {
            const footer = document.createElement('div');
            footer.className = 'enhanced-table-footer d-flex justify-content-between align-items-center mt-3';
            
            footer.innerHTML = `
                <div class="enhanced-table-info"></div>
                <nav aria-label="Навигация по страницам">
                    <ul class="pagination mb-0"></ul>
                </nav>
            `;
            
            wrapper.appendChild(footer);
            
            this.infoElement = footer.querySelector('.enhanced-table-info');
            this.paginationElement = footer.querySelector('.pagination');
        }

        // Add sortable headers
        if (this.options.sortable) {
            const headers = this.table.querySelectorAll('thead th');
            headers.forEach((header, index) => {
                if (!header.classList.contains('no-sort')) {
                    header.classList.add('sortable');
                    header.innerHTML += ' <i class="bi bi-arrow-down-up sort-icon"></i>';
                    header.dataset.column = index;
                }
            });
        }
    }

    setupEventListeners() {
        // Search input
        if (this.searchInput) {
            this.searchInput.addEventListener('input', (e) => {
                this.searchQuery = e.target.value.toLowerCase();
                this.filterData();
                this.currentPage = 1;
                this.render();
            });
        }

        // Entries selector
        if (this.entriesSelect) {
            this.entriesSelect.addEventListener('change', (e) => {
                this.options.itemsPerPage = parseInt(e.target.value);
                this.currentPage = 1;
                this.render();
            });
        }

        // Sortable headers
        if (this.options.sortable) {
            const headers = this.table.querySelectorAll('thead th.sortable');
            headers.forEach(header => {
                header.addEventListener('click', () => {
                    const column = parseInt(header.dataset.column);
                    this.sortBy(column);
                });
            });
        }
    }

    filterData() {
        if (!this.searchQuery) {
            this.filteredData = [...this.data];
            return;
        }

        this.filteredData = this.data.filter(row => {
            return row.data.some(cell => 
                cell.toLowerCase().includes(this.searchQuery)
            );
        });
    }

    sortBy(column) {
        if (this.sortColumn === column) {
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            this.sortColumn = column;
            this.sortDirection = 'asc';
        }

        this.filteredData.sort((a, b) => {
            const aVal = a.data[column];
            const bVal = b.data[column];

            // Try to parse as numbers
            const aNum = parseFloat(aVal);
            const bNum = parseFloat(bVal);

            let comparison = 0;
            if (!isNaN(aNum) && !isNaN(bNum)) {
                comparison = aNum - bNum;
            } else {
                comparison = aVal.localeCompare(bVal, 'ru');
            }

            return this.sortDirection === 'asc' ? comparison : -comparison;
        });

        this.updateSortIcons();
        this.render();
    }

    updateSortIcons() {
        const headers = this.table.querySelectorAll('thead th.sortable');
        headers.forEach((header, index) => {
            const icon = header.querySelector('.sort-icon');
            if (parseInt(header.dataset.column) === this.sortColumn) {
                icon.className = this.sortDirection === 'asc' 
                    ? 'bi bi-arrow-up sort-icon active' 
                    : 'bi bi-arrow-down sort-icon active';
            } else {
                icon.className = 'bi bi-arrow-down-up sort-icon';
            }
        });
    }

    render() {
        const start = (this.currentPage - 1) * this.options.itemsPerPage;
        const end = start + this.options.itemsPerPage;
        const pageData = this.filteredData.slice(start, end);

        // Clear tbody
        const tbody = this.table.querySelector('tbody');
        tbody.innerHTML = '';

        if (pageData.length === 0) {
            const noDataRow = document.createElement('tr');
            noDataRow.innerHTML = `
                <td colspan="100" class="text-center py-4 text-muted">
                    <i class="bi bi-inbox" style="font-size: 3rem;"></i>
                    <div class="mt-2">${this.options.noDataText}</div>
                </td>
            `;
            tbody.appendChild(noDataRow);
        } else {
            pageData.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = row.rawData.map(data => `<td>${data}</td>`).join('');
                tbody.appendChild(tr);
            });
        }

        this.renderPagination();
        this.renderInfo();
    }

    renderPagination() {
        if (!this.paginationElement) return;

        const totalPages = Math.ceil(this.filteredData.length / this.options.itemsPerPage);
        this.paginationElement.innerHTML = '';

        if (totalPages <= 1) return;

        // Previous button
        const prevLi = document.createElement('li');
        prevLi.className = `page-item ${this.currentPage === 1 ? 'disabled' : ''}`;
        prevLi.innerHTML = `
            <a class="page-link" href="#" aria-label="Предыдущая">
                <span aria-hidden="true">&laquo;</span>
            </a>
        `;
        if (this.currentPage > 1) {
            prevLi.querySelector('a').addEventListener('click', (e) => {
                e.preventDefault();
                this.currentPage--;
                this.render();
            });
        }
        this.paginationElement.appendChild(prevLi);

        // Page numbers
        const maxPages = 5;
        let startPage = Math.max(1, this.currentPage - Math.floor(maxPages / 2));
        let endPage = Math.min(totalPages, startPage + maxPages - 1);

        if (endPage - startPage < maxPages - 1) {
            startPage = Math.max(1, endPage - maxPages + 1);
        }

        if (startPage > 1) {
            const firstLi = this.createPageItem(1);
            this.paginationElement.appendChild(firstLi);
            
            if (startPage > 2) {
                const dotsLi = document.createElement('li');
                dotsLi.className = 'page-item disabled';
                dotsLi.innerHTML = '<span class="page-link">...</span>';
                this.paginationElement.appendChild(dotsLi);
            }
        }

        for (let i = startPage; i <= endPage; i++) {
            const pageLi = this.createPageItem(i);
            this.paginationElement.appendChild(pageLi);
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                const dotsLi = document.createElement('li');
                dotsLi.className = 'page-item disabled';
                dotsLi.innerHTML = '<span class="page-link">...</span>';
                this.paginationElement.appendChild(dotsLi);
            }
            
            const lastLi = this.createPageItem(totalPages);
            this.paginationElement.appendChild(lastLi);
        }

        // Next button
        const nextLi = document.createElement('li');
        nextLi.className = `page-item ${this.currentPage === totalPages ? 'disabled' : ''}`;
        nextLi.innerHTML = `
            <a class="page-link" href="#" aria-label="Следующая">
                <span aria-hidden="true">&raquo;</span>
            </a>
        `;
        if (this.currentPage < totalPages) {
            nextLi.querySelector('a').addEventListener('click', (e) => {
                e.preventDefault();
                this.currentPage++;
                this.render();
            });
        }
        this.paginationElement.appendChild(nextLi);
    }

    createPageItem(pageNum) {
        const li = document.createElement('li');
        li.className = `page-item ${this.currentPage === pageNum ? 'active' : ''}`;
        li.innerHTML = `<a class="page-link" href="#">${pageNum}</a>`;
        
        li.querySelector('a').addEventListener('click', (e) => {
            e.preventDefault();
            this.currentPage = pageNum;
            this.render();
        });
        
        return li;
    }

    renderInfo() {
        if (!this.infoElement) return;

        const start = Math.min((this.currentPage - 1) * this.options.itemsPerPage + 1, this.filteredData.length);
        const end = Math.min(this.currentPage * this.options.itemsPerPage, this.filteredData.length);
        const total = this.filteredData.length;

        const text = this.options.showEntriesText
            .replace('{start}', start)
            .replace('{end}', end)
            .replace('{total}', total);

        this.infoElement.textContent = text;
    }

    refresh() {
        this.extractData();
        this.filterData();
        this.render();
    }
}

// Auto-initialize tables with data-enhanced-table attribute
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('table[data-enhanced-table]').forEach(table => {
        new EnhancedTable(table);
    });
});

// Export for use in other scripts
window.EnhancedTable = EnhancedTable;
