class SoundManager {
    constructor() {
        try {
            // Create audio context
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            
            // Initialize sound effects
            this.sounds = {};
            
            // Add background music support
            this.backgroundMusic = null;
            this.backgroundMusicGain = null;
            this.isMusicPlaying = false;
            
            // Add sound effect gain control
            this.masterGain = this.audioContext.createGain();
            this.masterGain.connect(this.audioContext.destination);
            
            // Add reverb effect for more immersive sound
            this.reverb = this.createReverb();
            
            console.log("SoundManager инициализирован");
        } catch (e) {
            console.warn('Web Audio API не поддерживается в этом браузере');
            this.audioContext = null;
        }
    }
    
    // Create a simple reverb effect
    createReverb() {
        if (!this.audioContext) return null;
        
        try {
            // Create convolution reverb
            const convolver = this.audioContext.createConvolver();
            const duration = 2;
            const sampleRate = this.audioContext.sampleRate;
            const length = duration * sampleRate;
            const impulse = this.audioContext.createBuffer(2, length, sampleRate);
            
            // Create impulse response
            for (let channel = 0; channel < 2; channel++) {
                const channelData = impulse.getChannelData(channel);
                for (let i = 0; i < length; i++) {
                    channelData[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / length, 2);
                }
            }
            
            convolver.buffer = impulse;
            return convolver;
        } catch (e) {
            console.warn('Не удалось создать реверберацию:', e);
            return null;
        }
    }
    
    // Метод для воспроизведения звукового эффекта
    playSound(type, volume = 1.0) {
        if (!this.audioContext) return;
        
        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            // Connect with reverb if available
            if (this.reverb) {
                const dryGain = this.audioContext.createGain();
                const wetGain = this.audioContext.createGain();
                
                oscillator.connect(dryGain);
                oscillator.connect(this.reverb);
                this.reverb.connect(wetGain);
                
                dryGain.connect(gainNode);
                wetGain.connect(gainNode);
                
                // Mix dry and wet signals
                dryGain.gain.setValueAtTime(0.7, this.audioContext.currentTime);
                wetGain.gain.setValueAtTime(0.3, this.audioContext.currentTime);
            } else {
                oscillator.connect(gainNode);
            }
            
            gainNode.connect(this.masterGain);
            
            // Apply volume
            gainNode.gain.setValueAtTime(0.1 * volume, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
            
            switch(type) {
                case SOUND_EFFECTS.EAT:
                    oscillator.frequency.setValueAtTime(783.99, this.audioContext.currentTime); // Соль 5 октавы
                    oscillator.type = 'triangle';
                    break;
                case SOUND_EFFECTS.POWER:
                    oscillator.frequency.setValueAtTime(1046.50, this.audioContext.currentTime); // До 6 октавы
                    oscillator.type = 'sawtooth';
                    break;
                case SOUND_EFFECTS.GHOST:
                    oscillator.frequency.setValueAtTime(1567.98, this.audioContext.currentTime); // Соль 6 октавы
                    oscillator.type = 'square';
                    break;
                case SOUND_EFFECTS.DEATH:
                    oscillator.frequency.setValueAtTime(220, this.audioContext.currentTime); // Ля 3 октавы
                    oscillator.type = 'sawtooth';
                    // Add descending tone effect
                    oscillator.frequency.exponentialRampToValueAtTime(110, this.audioContext.currentTime + 0.5);
                    break;
                case SOUND_EFFECTS.LEVEL_COMPLETE:
                    oscillator.frequency.setValueAtTime(1318.51, this.audioContext.currentTime); // Ми 6 октавы
                    oscillator.type = 'triangle';
                    // Play a short melody
                    oscillator.frequency.setValueAtTime(1318.51, this.audioContext.currentTime);
                    oscillator.frequency.setValueAtTime(1567.98, this.audioContext.currentTime + 0.1);
                    oscillator.frequency.setValueAtTime(1760, this.audioContext.currentTime + 0.2);
                    oscillator.frequency.setValueAtTime(2093, this.audioContext.currentTime + 0.3);
                    break;
                case SOUND_EFFECTS.GAME_OVER:
                    oscillator.frequency.setValueAtTime(130.81, this.audioContext.currentTime); // До 3 октавы
                    oscillator.type = 'sawtooth';
                    // Play a descending melody
                    oscillator.frequency.setValueAtTime(130.81, this.audioContext.currentTime);
                    oscillator.frequency.setValueAtTime(116.54, this.audioContext.currentTime + 0.2);
                    oscillator.frequency.setValueAtTime(103.83, this.audioContext.currentTime + 0.4);
                    oscillator.frequency.setValueAtTime(92.50, this.audioContext.currentTime + 0.6);
                    break;
                case SOUND_EFFECTS.FRUIT:
                    oscillator.frequency.setValueAtTime(1760, this.audioContext.currentTime); // Ля 6 октавы
                    oscillator.type = 'sine';
                    break;
                case SOUND_EFFECTS.COMBO:
                    oscillator.frequency.setValueAtTime(1567.98, this.audioContext.currentTime); // Соль 6 октавы
                    oscillator.type = 'sine';
                    // Воспроизвести последовательность нот
                    gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.1);
                    oscillator.frequency.setValueAtTime(1567.98, this.audioContext.currentTime);
                    oscillator.frequency.setValueAtTime(1760, this.audioContext.currentTime + 0.1);
                    oscillator.frequency.setValueAtTime(1975.53, this.audioContext.currentTime + 0.2);
                    break;
                case SOUND_EFFECTS.POWER_UP: // Новый звук для power-up'ов
                    // Создаем мелодию для power-up
                    oscillator.frequency.setValueAtTime(523.25, this.audioContext.currentTime); // До 5 октавы
                    oscillator.frequency.setValueAtTime(659.25, this.audioContext.currentTime + 0.05); // Ми 5 октавы
                    oscillator.frequency.setValueAtTime(783.99, this.audioContext.currentTime + 0.1); // Соль 5 октавы
                    oscillator.frequency.setValueAtTime(1046.50, this.audioContext.currentTime + 0.15); // До 6 октавы
                    oscillator.type = 'sine';
                    break;
                default:
                    // По умолчанию воспроизводим короткий звук
                    oscillator.frequency.setValueAtTime(440, this.audioContext.currentTime);
                    oscillator.type = 'sine';
            }
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.3);
        } catch (e) {
            console.warn('Ошибка воспроизведения звука:', e);
        }
    }
    
    // Метод для воспроизведения фоновой музыки
    playBackgroundMusic() {
        if (!this.audioContext || this.isMusicPlaying) return;
        
        try {
            // Create a simple background music pattern
            const oscillator1 = this.audioContext.createOscillator();
            const oscillator2 = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator1.type = 'sine';
            oscillator2.type = 'sine';
            
            // Connect oscillators to gain node
            oscillator1.connect(gainNode);
            oscillator2.connect(gainNode);
            gainNode.connect(this.masterGain);
            
            // Set volume
            gainNode.gain.setValueAtTime(0.05, this.audioContext.currentTime);
            
            // Create a simple melody pattern
            const baseFreq = 220; // Ля 3 октавы
            const notes = [0, 2, 4, 5, 7, 9, 11, 12]; // Major scale intervals
            
            // Schedule notes
            for (let i = 0; i < 16; i++) {
                const noteIndex = notes[i % notes.length];
                const freq = baseFreq * Math.pow(2, noteIndex / 12);
                
                oscillator1.frequency.setValueAtTime(freq, this.audioContext.currentTime + i * 0.5);
                oscillator2.frequency.setValueAtTime(freq * 1.5, this.audioContext.currentTime + i * 0.5);
            }
            
            // Start oscillators
            oscillator1.start(this.audioContext.currentTime);
            oscillator2.start(this.audioContext.currentTime);
            
            // Stop after 8 seconds (will loop in a real implementation)
            oscillator1.stop(this.audioContext.currentTime + 8);
            oscillator2.stop(this.audioContext.currentTime + 8);
            
            this.isMusicPlaying = true;
            
            // Reset flag when music ends
            setTimeout(() => {
                this.isMusicPlaying = false;
            }, 8000);
            
        } catch (e) {
            console.warn('Ошибка воспроизведения фоновой музыки:', e);
        }
    }
    
    // Метод для остановки всех звуков
    stopAllSounds() {
        if (this.audioContext) {
            this.audioContext.close();
        }
    }
    
    // Метод для установки громкости
    setVolume(volume) {
        if (this.masterGain) {
            this.masterGain.gain.setValueAtTime(volume, this.audioContext.currentTime);
        }
    }
    
    // Метод для включения/выключения звука
    toggleMute() {
        if (this.masterGain) {
            const currentGain = this.masterGain.gain.value;
            this.masterGain.gain.setValueAtTime(currentGain > 0 ? 0 : 1, this.audioContext.currentTime);
        }
    }
}

// Экспортируем класс для использования в других файлах
export { SoundManager };