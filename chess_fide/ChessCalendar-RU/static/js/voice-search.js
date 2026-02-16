/**
 * Voice Search Module
 * Голосовой поиск турниров
 */

class VoiceSearch {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.init();
    }

    init() {
        console.log('[VoiceSearch] Инициализация голосового поиска');
        
        // Проверяем поддержку Web Speech API
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('[VoiceSearch] Web Speech API не поддерживается');
            return;
        }

        this.setupRecognition();
        this.createVoiceButton();
    }

    setupRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        this.recognition.lang = 'ru-RU';
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.maxAlternatives = 1;

        this.recognition.onstart = () => {
            console.log('[VoiceSearch] Начало распознавания');
            this.isListening = true;
            this.updateButtonState();
            this.showListeningIndicator();
        };

        this.recognition.onresult = (event) => {
            const result = event.results[event.results.length - 1];
            const transcript = result[0].transcript;
            
            console.log('[VoiceSearch] Распознано:', transcript);
            
            if (result.isFinal) {
                this.processVoiceCommand(transcript);
            } else {
                this.updateListeningIndicator(transcript);
            }
        };

        this.recognition.onerror = (event) => {
            console.error('[VoiceSearch] Ошибка:', event.error);
            this.isListening = false;
            this.updateButtonState();
            this.hideListeningIndicator();
            
            let errorMessage = 'Ошибка распознавания речи';
            switch (event.error) {
                case 'no-speech':
                    errorMessage = 'Речь не обнаружена';
                    break;
                case 'audio-capture':
                    errorMessage = 'Микрофон недоступен';
                    break;
                case 'not-allowed':
                    errorMessage = 'Доступ к микрофону запрещён';
                    break;
            }
            
            this.showToast(errorMessage, 'error');
        };

        this.recognition.onend = () => {
            console.log('[VoiceSearch] Конец распознавания');
            this.isListening = false;
            this.updateButtonState();
            this.hideListeningIndicator();
        };
    }

    createVoiceButton() {
        const searchContainer = document.querySelector('.search-container');
        if (!searchContainer) return;

        const voiceBtn = document.createElement('button');
        voiceBtn.type = 'button';
        voiceBtn.className = 'btn btn-outline-light voice-search-btn';
        voiceBtn.id = 'voiceSearchBtn';
        voiceBtn.innerHTML = '<i class="bi bi-mic"></i>';
        voiceBtn.title = 'Голосовой поиск';
        
        voiceBtn.addEventListener('click', () => {
            this.toggleVoiceSearch();
        });

        // Вставляем кнопку рядом с поиском
        const searchBtn = searchContainer.querySelector('.btn');
        searchBtn.parentNode.insertBefore(voiceBtn, searchBtn);
    }

    toggleVoiceSearch() {
        if (this.isListening) {
            this.stopListening();
        } else {
            this.startListening();
        }
    }

    startListening() {
        if (!this.recognition) {
            this.showToast('Голосовой поиск не поддерживается', 'warning');
            return;
        }

        try {
            this.recognition.start();
        } catch (error) {
            console.error('[VoiceSearch] Ошибка запуска:', error);
            this.showToast('Не удалось запустить голосовой поиск', 'error');
        }
    }

    stopListening() {
        if (this.recognition) {
            this.recognition.stop();
        }
    }

    processVoiceCommand(transcript) {
        const command = transcript.toLowerCase().trim();
        
        console.log('[VoiceSearch] Обработка команды:', command);

        // Команды навигации
        if (command.includes('главная') || command.includes('домой')) {
            window.location.href = '/';
            return;
        }
        
        if (command.includes('календарь')) {
            window.location.href = '/calendar';
            return;
        }
        
        if (command.includes('карта')) {
            window.location.href = '/map';
            return;
        }
        
        if (command.includes('статистика')) {
            window.location.href = '/statistics';
            return;
        }

        if (command.includes('избранное')) {
            window.location.href = '/favorites';
            return;
        }

        // Команды темы
        if (command.includes('тёмная тема') || command.includes('темная тема')) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            this.showToast('Тёмная тема включена', 'success');
            return;
        }

        if (command.includes('светлая тема')) {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
            this.showToast('Светлая тема включена', 'success');
            return;
        }

        // Поиск турниров
        this.searchTournaments(command);
    }

    searchTournaments(query) {
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.value = query;
            
            // Триггерим поиск
            const event = new Event('input', { bubbles: true });
            searchInput.dispatchEvent(event);
            
            this.showToast(`Поиск: "${query}"`, 'info');
        }
    }

    updateButtonState() {
        const btn = document.getElementById('voiceSearchBtn');
        if (!btn) return;

        if (this.isListening) {
            btn.classList.add('listening');
            btn.innerHTML = '<i class="bi bi-mic-fill"></i>';
        } else {
            btn.classList.remove('listening');
            btn.innerHTML = '<i class="bi bi-mic"></i>';
        }
    }

    showListeningIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'voiceListeningIndicator';
        indicator.className = 'voice-listening-indicator';
        indicator.innerHTML = `
            <div class="voice-indicator-content">
                <div class="voice-wave">
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                <div class="voice-text">Слушаю...</div>
                <div class="voice-transcript"></div>
                <button class="btn btn-sm btn-danger mt-2" onclick="window.ChessCalendar.voiceSearch.stopListening()">
                    <i class="bi bi-stop-circle"></i> Остановить
                </button>
            </div>
        `;

        document.body.appendChild(indicator);
        
        // Анимация появления
        setTimeout(() => {
            indicator.classList.add('show');
        }, 10);
    }

    updateListeningIndicator(text) {
        const transcript = document.querySelector('.voice-transcript');
        if (transcript) {
            transcript.textContent = text;
        }
    }

    hideListeningIndicator() {
        const indicator = document.getElementById('voiceListeningIndicator');
        if (indicator) {
            indicator.classList.remove('show');
            setTimeout(() => {
                indicator.remove();
            }, 300);
        }
    }

    showToast(message, type = 'info') {
        if (window.ChessCalendar && window.ChessCalendar.showToast) {
            window.ChessCalendar.showToast(message, type);
        }
    }
}

// Стили
const style = document.createElement('style');
style.textContent = `
    .voice-search-btn {
        border-radius: 20px;
        margin-left: 0.5rem;
        padding: 0.4rem 0.8rem;
        transition: all 0.3s ease;
    }

    .voice-search-btn.listening {
        background: #ef4444;
        border-color: #ef4444;
        color: white;
        animation: pulse-red 1.5s infinite;
    }

    @keyframes pulse-red {
        0%, 100% {
            box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
        }
        50% {
            box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
        }
    }

    .voice-listening-indicator {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: var(--bg-primary);
        border: 2px solid var(--primary-color);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--box-shadow-lg);
        z-index: 10000;
        min-width: 300px;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .voice-listening-indicator.show {
        opacity: 1;
    }

    .voice-indicator-content {
        text-align: center;
    }

    .voice-wave {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.25rem;
        height: 50px;
        margin-bottom: 1rem;
    }

    .voice-wave span {
        display: inline-block;
        width: 4px;
        height: 20px;
        background: var(--primary-color);
        border-radius: 2px;
        animation: wave 1.2s ease-in-out infinite;
    }

    .voice-wave span:nth-child(1) { animation-delay: 0s; }
    .voice-wave span:nth-child(2) { animation-delay: 0.1s; }
    .voice-wave span:nth-child(3) { animation-delay: 0.2s; }
    .voice-wave span:nth-child(4) { animation-delay: 0.3s; }
    .voice-wave span:nth-child(5) { animation-delay: 0.4s; }

    @keyframes wave {
        0%, 100% {
            height: 20px;
        }
        50% {
            height: 50px;
        }
    }

    .voice-text {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }

    .voice-transcript {
        min-height: 30px;
        color: var(--text-secondary);
        font-style: italic;
        margin-bottom: 1rem;
    }

    @media (max-width: 576px) {
        .voice-listening-indicator {
            min-width: 250px;
            padding: 1.5rem;
        }
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.ChessCalendar = window.ChessCalendar || {};
    window.ChessCalendar.voiceSearch = new VoiceSearch();
});
