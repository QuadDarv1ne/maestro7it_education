/**
 * Print Helper Module
 * Помощник для печати турниров
 */

class PrintHelper {
    constructor() {
        this.init();
    }

    init() {
        console.log('[PrintHelper] Инициализация помощника печати');
        this.createPrintButton();
        this.setupPrintHandlers();
    }

    createPrintButton() {
        // Создаём плавающую кнопку печати
        const printBtn = document.createElement('button');
        printBtn.className = 'btn btn-primary print-button';
        printBtn.innerHTML = '<i class="bi bi-printer"></i>';
        printBtn.title = 'Печать';
        printBtn.onclick = () => this.showPrintOptions();
        
        document.body.appendChild(printBtn);
    }

    showPrintOptions() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'printOptionsModal';
        modal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-printer"></i> Параметры печати
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Что печатать:</label>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="printContent" 
                                    id="printCurrent" value="current" checked>
                                <label class="form-check-label" for="printCurrent">
                                    Текущую страницу
                                </label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="printContent" 
                                    id="printSelected" value="selected">
                                <label class="form-check-label" for="printSelected">
                                    Выбранные турниры
                                </label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="printContent" 
                                    id="printAll" value="all">
                                <label class="form-check-label" for="printAll">
                                    Все турниры на странице
                                </label>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Ориентация:</label>
                            <div class="btn-group w-100" role="group">
                                <input type="radio" class="btn-check" name="orientation" 
                                    id="portrait" value="portrait" checked>
                                <label class="btn btn-outline-primary" for="portrait">
                                    <i class="bi bi-file-earmark-text"></i> Книжная
                                </label>
                                
                                <input type="radio" class="btn-check" name="orientation" 
                                    id="landscape" value="landscape">
                                <label class="btn btn-outline-primary" for="landscape">
                                    <i class="bi bi-file-earmark-text-fill"></i> Альбомная
                                </label>
                            </div>
                        </div>

                        <div class="mb-3">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="includeHeader" checked>
                                <label class="form-check-label" for="includeHeader">
                                    Включить заголовок
                                </label>
                            </div>
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="includeDate" checked>
                                <label class="form-check-label" for="includeDate">
                                    Включить дату печати
                                </label>
                            </div>
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="includeQR">
                                <label class="form-check-label" for="includeQR">
                                    Включить QR-код
                                </label>
                            </div>
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="colorPrint" checked>
                                <label class="form-check-label" for="colorPrint">
                                    Цветная печать
                                </label>
                            </div>
                        </div>

                        <div class="alert alert-info">
                            <i class="bi bi-info-circle"></i>
                            <small>
                                Для лучшего результата используйте функцию "Печать" в браузере 
                                и выберите "Сохранить как PDF" для предварительного просмотра.
                            </small>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Отмена
                        </button>
                        <button type="button" class="btn btn-outline-primary" id="previewPrint">
                            <i class="bi bi-eye"></i> Предпросмотр
                        </button>
                        <button type="button" class="btn btn-primary" id="startPrint">
                            <i class="bi bi-printer"></i> Печать
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();

        // Обработчики
        modal.querySelector('#previewPrint').addEventListener('click', () => {
            this.preparePrint(modal, true);
            bsModal.hide();
        });

        modal.querySelector('#startPrint').addEventListener('click', () => {
            this.preparePrint(modal, false);
            bsModal.hide();
        });

        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }

    preparePrint(modal, preview = false) {
        const options = {
            content: modal.querySelector('input[name="printContent"]:checked').value,
            orientation: modal.querySelector('input[name="orientation"]:checked').value,
            includeHeader: modal.querySelector('#includeHeader').checked,
            includeDate: modal.querySelector('#includeDate').checked,
            includeQR: modal.querySelector('#includeQR').checked,
            colorPrint: modal.querySelector('#colorPrint').checked
        };

        // Добавляем заголовок для печати
        if (options.includeHeader) {
            this.addPrintHeader();
        }

        // Добавляем дату
        if (options.includeDate) {
            this.addPrintDate();
        }

        // Добавляем QR-код
        if (options.includeQR) {
            this.addPrintQR();
        }

        // Устанавливаем ориентацию
        if (options.orientation === 'landscape') {
            document.body.classList.add('landscape-print');
        }

        // Режим ч/б печати
        if (!options.colorPrint) {
            document.body.classList.add('monochrome-print');
        }

        if (preview) {
            this.showPrintPreview();
        } else {
            // Небольшая задержка для применения стилей
            setTimeout(() => {
                window.print();
                this.cleanupPrint();
            }, 100);
        }
    }

    addPrintHeader() {
        if (document.querySelector('.print-header')) return;

        const header = document.createElement('div');
        header.className = 'print-header';
        header.innerHTML = `
            <h1>ChessCalendar-RU</h1>
            <p>Календарь шахматных турниров</p>
        `;

        const main = document.querySelector('main');
        if (main) {
            main.insertBefore(header, main.firstChild);
        }
    }

    addPrintDate() {
        if (document.querySelector('.print-date')) return;

        const dateEl = document.createElement('div');
        dateEl.className = 'print-date';
        dateEl.textContent = `Дата печати: ${new Date().toLocaleDateString('ru-RU', {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        })}`;

        const main = document.querySelector('main');
        if (main) {
            const header = main.querySelector('.print-header');
            if (header) {
                header.after(dateEl);
            } else {
                main.insertBefore(dateEl, main.firstChild);
            }
        }
    }

    addPrintQR() {
        if (document.querySelector('.print-qr')) return;

        const qr = document.createElement('div');
        qr.className = 'print-qr';
        qr.innerHTML = `
            <p>Сканируйте QR-код для просмотра онлайн:</p>
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(window.location.href)}" 
                 alt="QR Code">
            <p><small>${window.location.href}</small></p>
        `;

        const main = document.querySelector('main');
        if (main) {
            main.appendChild(qr);
        }
    }

    showPrintPreview() {
        document.body.classList.add('print-preview-mode');
        
        const overlay = document.createElement('div');
        overlay.className = 'print-preview-overlay';
        overlay.innerHTML = `
            <div class="print-preview-controls">
                <button class="btn btn-primary" onclick="window.print()">
                    <i class="bi bi-printer"></i> Печать
                </button>
                <button class="btn btn-secondary" onclick="window.ChessCalendar.printHelper.closePrintPreview()">
                    <i class="bi bi-x-lg"></i> Закрыть
                </button>
            </div>
        `;
        
        document.body.appendChild(overlay);
    }

    closePrintPreview() {
        document.body.classList.remove('print-preview-mode');
        const overlay = document.querySelector('.print-preview-overlay');
        if (overlay) {
            overlay.remove();
        }
        this.cleanupPrint();
    }

    cleanupPrint() {
        // Удаляем временные элементы
        const printHeader = document.querySelector('.print-header');
        const printDate = document.querySelector('.print-date');
        const printQR = document.querySelector('.print-qr');
        
        if (printHeader) printHeader.remove();
        if (printDate) printDate.remove();
        if (printQR) printQR.remove();

        // Удаляем классы
        document.body.classList.remove('landscape-print', 'monochrome-print');
    }

    setupPrintHandlers() {
        // Обработчик Ctrl+P
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
                e.preventDefault();
                this.showPrintOptions();
            }
        });

        // Обработчик после печати
        window.addEventListener('afterprint', () => {
            this.cleanupPrint();
        });
    }

    // Экспорт в PDF (требует библиотеку)
    async exportToPDF() {
        this.showToast('Функция экспорта в PDF в разработке', 'info');
    }

    showToast(message, type = 'info') {
        if (window.ChessCalendar && window.ChessCalendar.showToast) {
            window.ChessCalendar.showToast(message, type);
        }
    }
}

// Дополнительные стили
const style = document.createElement('style');
style.textContent = `
    .print-preview-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: rgba(0, 0, 0, 0.9);
        z-index: 9999;
        padding: 1rem;
    }

    .print-preview-controls {
        display: flex;
        justify-content: center;
        gap: 1rem;
    }

    @media print {
        .print-preview-overlay {
            display: none !important;
        }
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.ChessCalendar = window.ChessCalendar || {};
    window.ChessCalendar.printHelper = new PrintHelper();
});
