class ParticleManager {
    constructor() {
        this.particles = [];
        this.pool = [];
        this.maxParticles = 100; // Limit maximum particles for performance
    }

    // Get a particle from the pool or create a new one
    getParticle() {
        if (this.pool.length > 0) {
            return this.pool.pop();
        }
        return {
            x: 0,
            y: 0,
            vx: 0,
            vy: 0,
            color: '#FFFFFF',
            size: 1,
            life: 30,
            active: false
        };
    }

    // Return a particle to the pool
    releaseParticle(particle) {
        particle.active = false;
        this.pool.push(particle);
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

        // Limit the number of particles to prevent performance issues
        const particlesToAdd = Math.min(count, this.maxParticles - this.getActiveParticleCount());
        
        for (let i = 0; i < particlesToAdd; i++) {
            const particle = this.getParticle();
            particle.x = x;
            particle.y = y;
            particle.vx = (Math.random() - 0.5) * 4;
            particle.vy = (Math.random() - 0.5) * 4;
            particle.color = color;
            particle.size = Math.random() * 3 + 1;
            particle.life = 30;
            particle.active = true;
            this.particles.push(particle);
        }
    }

    updateParticles() {
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.life--;

            if (p.life <= 0) {
                // Remove from active particles and return to pool
                this.particles.splice(i, 1);
                this.releaseParticle(p);
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
        // Return all particles to the pool
        while (this.particles.length > 0) {
            const particle = this.particles.pop();
            this.releaseParticle(particle);
        }
    }

    // Get count of active particles
    getActiveParticleCount() {
        return this.particles.length;
    }
}

// Экспортируем класс для использования в других файлах
export { ParticleManager };