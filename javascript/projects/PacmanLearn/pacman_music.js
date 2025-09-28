// Pacman Music Generator
// This file generates the classic Pacman theme using Web Audio API

class PacmanMusic {
    constructor() {
        this.audioContext = null;
        this.isPlaying = false;
        this.volume = 0.3;
    }
    
    init() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            return true;
        } catch (e) {
            console.warn('Web Audio API is not supported in this browser');
            return false;
        }
    }
    
    // Classic Pacman theme notes
    getThemeNotes() {
        return [
            // First phrase
            { frequency: 261.63, duration: 0.2 }, // C4
            { frequency: 329.63, duration: 0.2 }, // E4
            { frequency: 392.00, duration: 0.2 }, // G4
            { frequency: 523.25, duration: 0.4 }, // C5
            { frequency: 392.00, duration: 0.2 }, // G4
            { frequency: 523.25, duration: 0.4 }, // C5
            
            // Second phrase
            { frequency: 261.63, duration: 0.2 }, // C4
            { frequency: 329.63, duration: 0.2 }, // E4
            { frequency: 392.00, duration: 0.2 }, // G4
            { frequency: 523.25, duration: 0.4 }, // C5
            { frequency: 392.00, duration: 0.2 }, // G4
            { frequency: 523.25, duration: 0.4 }, // C5
            
            // Third phrase
            { frequency: 659.25, duration: 0.2 }, // E5
            { frequency: 587.33, duration: 0.2 }, // D5
            { frequency: 523.25, duration: 0.2 }, // C5
            { frequency: 392.00, duration: 0.4 }, // G4
            { frequency: 440.00, duration: 0.2 }, // A4
            { frequency: 392.00, duration: 0.4 }, // G4
        ];
    }
    
    playNote(frequency, duration, startTime) {
        if (!this.audioContext) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.type = 'square';
        oscillator.frequency.value = frequency;
        
        // Set volume envelope
        gainNode.gain.setValueAtTime(0, startTime);
        gainNode.gain.setValueAtTime(this.volume, startTime + 0.01);
        gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + duration);
        
        oscillator.start(startTime);
        oscillator.stop(startTime + duration);
        
        return startTime + duration;
    }
    
    playTheme() {
        if (!this.audioContext || this.isPlaying) return;
        
        this.isPlaying = true;
        const notes = this.getThemeNotes();
        let startTime = this.audioContext.currentTime;
        
        // Play each note in sequence
        notes.forEach((note, index) => {
            startTime = this.playNote(note.frequency, note.duration, startTime + (index * 0.01));
        });
        
        // Schedule loop
        setTimeout(() => {
            if (this.isPlaying) {
                this.playTheme();
            }
        }, notes.length * 200);
    }
    
    stop() {
        this.isPlaying = false;
    }
}

// Export for use in the game
window.PacmanMusic = PacmanMusic;