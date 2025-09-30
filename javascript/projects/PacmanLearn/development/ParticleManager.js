class ParticleManager {
    constructor() {
        this.particles = [];
    }

    createParticles(x, y, color, count = 10) {
        // Получаем настройки из localStorage или используем значения по умолчанию
        let settings = { animationsEnabled: true };
        try {
            const savedSettings = localStorage.getItem('pacmanSettings');
            if (savedSettings) {
                settings = JSON.parse(savedSettings);
            }
        } catch (e) {
            console.warn('Ошибка загрузки настроек анимации:', e);
        }

        if (!settings.animationsEnabled) return;

        for (let i = 0; i < count; i++) {
            this.particles.push({
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 4,
                vy: (Math.random() - 0.5) * 4,
                color: color,
                size: Math.random() * 3 + 1,
                life: 30
            });
        }
    }

    updateParticles() {
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.life--;

            if (p.life <= 0) {
                this.particles.splice(i, 1);
            }
        }
    }

    drawParticles(ctx) {
        this.particles.forEach(p => {
            ctx.fillStyle = p.color;
            ctx.globalAlpha = p.life / 30;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.globalAlpha = 1;
    }

    clearParticles() {
        this.particles = [];
    }
}

// Экспортируем класс для использования в других файлах
// В браузерной среде добавляем в глобальную область видимости
if (typeof window !== 'undefined') {
    window.ParticleManager = ParticleManager;
}

// Для Node.js или модульных систем
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ParticleManager;
}