class SoundManager {
    constructor() {
        this.audioContext = null;
        this.sounds = {};
        this.musicPlayer = null;
        this.initAudio();
    }

    initAudio() {
        try {
            // Создать аудио контекст
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.warn('Web Audio API не поддерживается в этом браузере');
        }
    }

    playSound(type) {
        // Получаем настройки из localStorage или используем значения по умолчанию
        let settings = { soundEnabled: true };
        try {
            const savedSettings = localStorage.getItem('pacmanSettings');
            if (savedSettings) {
                settings = JSON.parse(savedSettings);
            }
        } catch (e) {
            console.warn('Ошибка загрузки настроек звука:', e);
        }

        if (!settings.soundEnabled || !this.audioContext) return;

        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);

            gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);

            switch(type) {
                case 'start':
                    oscillator.frequency.setValueAtTime(523.25, this.audioContext.currentTime); // До 5 октавы
                    oscillator.type = 'square';
                    break;
                case 'eat':
                    oscillator.frequency.setValueAtTime(783.99, this.audioContext.currentTime); // Соль 5 октавы
                    oscillator.type = 'triangle';
                    break;
                case 'power':
                    oscillator.frequency.setValueAtTime(1046.50, this.audioContext.currentTime); // До 6 октавы
                    oscillator.type = 'sawtooth';
                    break;
                case 'ghost':
                    oscillator.frequency.setValueAtTime(1567.98, this.audioContext.currentTime); // Соль 6 октавы
                    oscillator.type = 'square';
                    break;
                case 'death':
                    oscillator.frequency.setValueAtTime(220, this.audioContext.currentTime); // Ля 3 октавы
                    oscillator.type = 'sawtooth';
                    break;
                case 'level':
                    oscillator.frequency.setValueAtTime(1318.51, this.audioContext.currentTime); // Ми 6 октавы
                    oscillator.type = 'triangle';
                    break;
                case 'combo':
                    oscillator.frequency.setValueAtTime(1567.98, this.audioContext.currentTime); // Соль 6 октавы
                    oscillator.type = 'sine';
                    // Воспроизвести последовательность нот
                    gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.1);
                    oscillator.frequency.setValueAtTime(1567.98, this.audioContext.currentTime);
                    oscillator.frequency.setValueAtTime(1760, this.audioContext.currentTime + 0.1);
                    oscillator.frequency.setValueAtTime(1975.53, this.audioContext.currentTime + 0.2);
                    break;
                case 'gameover':
                    oscillator.frequency.setValueAtTime(130.81, this.audioContext.currentTime); // До 3 октавы
                    oscillator.type = 'sawtooth';
                    break;
                case 'fruit':
                    oscillator.frequency.setValueAtTime(1760, this.audioContext.currentTime); // Ля 6 октавы
                    oscillator.type = 'sine';
                    break;
                case 'achievement':
                    // Play a celebratory sound
                    oscillator.frequency.setValueAtTime(1046.50, this.audioContext.currentTime); // До 6 октавы
                    oscillator.frequency.setValueAtTime(1318.51, this.audioContext.currentTime + 0.1); // Ми 6 октавы
                    oscillator.frequency.setValueAtTime(1567.98, this.audioContext.currentTime + 0.2); // Соль 6 октавы
                    oscillator.type = 'sine';
                    break;
            }

            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.3);
        } catch (e) {
            console.warn('Ошибка воспроизведения звука:', e);
        }
    }

    playBackgroundMusic() {
        // Имитация воспроизведения фоновой музыки
        console.log('Воспроизведение фоновой музыки');
    }

    pauseBackgroundMusic() {
        // Имитация паузы фоновой музыки
        console.log('Пауза фоновой музыки');
    }
}

// Экспортируем класс для использования в других файлах
// В браузерной среде добавляем в глобальную область видимости
if (typeof window !== 'undefined') {
    window.SoundManager = SoundManager;
}

// Для Node.js или модульных систем
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SoundManager;
}