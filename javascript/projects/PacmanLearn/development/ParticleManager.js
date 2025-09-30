import { PARTICLE_TYPES } from './Constants.js';

class ParticleManager {
    constructor() {
        this.particles = [];
        this.pool = [];
        this.maxParticles = 200;
        this.particleTypes = PARTICLE_TYPES;
        // Pre-allocate object pool for better performance
        this.initializePool();
    }

    // Initialize object pool with pre-allocated particles
    initializePool() {
        for (let i = 0; i < this.maxParticles; i++) {
            this.pool.push(this.createParticleObject());
        }
    }

    // Create a particle object with default values (reusable structure)
    createParticleObject() {
        return {
            x: 0,
            y: 0,
            vx: 0,
            vy: 0,
            color: '#FFFFFF',
            size: 1,
            life: 0,
            maxLife: 0,
            active: false,
            type: this.particleTypes.DEFAULT,
            decay: 0.05,
            glow: 0,
            gravity: 0,
            friction: 0.98
        };
    }

    // Get a particle from the pool or create a new one
    getParticle() {
        if (this.pool.length > 0) {
            return this.pool.pop();
        }
        // Only create new particle if absolutely necessary
        return this.createParticleObject();
    }

    // Return a particle to the pool
    releaseParticle(particle) {
        if (this.pool.length < this.maxParticles) {
            // Reset particle properties to default values
            particle.x = 0;
            particle.y = 0;
            particle.vx = 0;
            particle.vy = 0;
            particle.color = '#FFFFFF';
            particle.size = 1;
            particle.life = 0;
            particle.maxLife = 0;
            particle.active = false;
            particle.type = this.particleTypes.DEFAULT;
            particle.decay = 0.05;
            particle.glow = 0;
            particle.gravity = 0;
            particle.friction = 0.98;
            this.pool.push(particle);
        }
        // If pool is full, let the particle be garbage collected
    }

    // Create specialized particle effects
    createEffect(x, y, type, color, count = 10) {
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

        switch(type) {
            case this.particleTypes.EXPLOSION:
                this.createExplosion(x, y, color, count);
                break;
            case this.particleTypes.SPARKLE:
                this.createSparkle(x, y, color, count);
                break;
            case this.particleTypes.SMOKE:
                this.createSmoke(x, y, color, count);
                break;
            case this.particleTypes.GLOW:
                this.createGlow(x, y, color, count);
                break;
            default:
                this.createParticles(x, y, color, count);
        }
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
            particle.maxLife = 30;
            particle.active = true;
            particle.type = this.particleTypes.DEFAULT;
            particle.decay = 0.05;
            particle.glow = 0;
            particle.gravity = 0;
            particle.friction = 0.98;
            this.particles.push(particle);
        }
    }

    createExplosion(x, y, color, count = 20) {
        const particlesToAdd = Math.min(count, this.maxParticles - this.getActiveParticleCount());
        
        for (let i = 0; i < particlesToAdd; i++) {
            const particle = this.getParticle();
            const angle = Math.random() * Math.PI * 2;
            const speed = 1 + Math.random() * 5;
            
            particle.x = x;
            particle.y = y;
            particle.vx = Math.cos(angle) * speed;
            particle.vy = Math.sin(angle) * speed;
            particle.color = color;
            particle.size = 2 + Math.random() * 4;
            particle.life = 40 + Math.floor(Math.random() * 30);
            particle.maxLife = particle.life;
            particle.active = true;
            particle.type = this.particleTypes.EXPLOSION;
            particle.decay = 0.03 + Math.random() * 0.03;
            particle.glow = 0.7;
            particle.gravity = 0.1;
            particle.friction = 0.95;
            this.particles.push(particle);
        }
    }

    createSparkle(x, y, color, count = 15) {
        const particlesToAdd = Math.min(count, this.maxParticles - this.getActiveParticleCount());
        
        for (let i = 0; i < particlesToAdd; i++) {
            const particle = this.getParticle();
            const angle = Math.random() * Math.PI * 2;
            const speed = 0.5 + Math.random() * 2;
            
            particle.x = x;
            particle.y = y;
            particle.vx = Math.cos(angle) * speed;
            particle.vy = Math.sin(angle) * speed;
            particle.color = color;
            particle.size = 1 + Math.random() * 2;
            particle.life = 60 + Math.floor(Math.random() * 40);
            particle.maxLife = particle.life;
            particle.active = true;
            particle.type = this.particleTypes.SPARKLE;
            particle.decay = 0.02 + Math.random() * 0.02;
            particle.glow = 0.8;
            particle.gravity = -0.05;
            particle.friction = 0.99;
            this.particles.push(particle);
        }
    }

    createSmoke(x, y, color, count = 10) {
        const particlesToAdd = Math.min(count, this.maxParticles - this.getActiveParticleCount());
        
        for (let i = 0; i < particlesToAdd; i++) {
            const particle = this.getParticle();
            const angle = (Math.random() - 0.5) * Math.PI * 0.5;
            const speed = 0.2 + Math.random() * 1;
            
            particle.x = x + (Math.random() - 0.5) * 10;
            particle.y = y;
            particle.vx = Math.cos(angle) * speed;
            particle.vy = Math.sin(angle) * speed;
            particle.color = color;
            particle.size = 3 + Math.random() * 5;
            particle.life = 80 + Math.floor(Math.random() * 50);
            particle.maxLife = particle.life;
            particle.active = true;
            particle.type = this.particleTypes.SMOKE;
            particle.decay = 0.01 + Math.random() * 0.01;
            particle.glow = 0.3;
            particle.gravity = -0.02;
            particle.friction = 0.97;
            this.particles.push(particle);
        }
    }

    createGlow(x, y, color, count = 8) {
        const particlesToAdd = Math.min(count, this.maxParticles - this.getActiveParticleCount());
        
        for (let i = 0; i < particlesToAdd; i++) {
            const particle = this.getParticle();
            const angle = Math.random() * Math.PI * 2;
            const distance = 5 + Math.random() * 15;
            
            particle.x = x + Math.cos(angle) * distance;
            particle.y = y + Math.sin(angle) * distance;
            particle.vx = Math.cos(angle) * 0.5;
            particle.vy = Math.sin(angle) * 0.5;
            particle.color = color;
            particle.size = 2 + Math.random() * 3;
            particle.life = 50 + Math.floor(Math.random() * 30);
            particle.maxLife = particle.life;
            particle.active = true;
            particle.type = this.particleTypes.GLOW;
            particle.decay = 0.03 + Math.random() * 0.02;
            particle.glow = 1.0;
            particle.gravity = 0;
            particle.friction = 0.98;
            this.particles.push(particle);
        }
    }

    updateParticles() {
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            
            // Apply physics
            p.vy += p.gravity;
            p.vx *= p.friction;
            p.vy *= p.friction;
            
            p.x += p.vx;
            p.y += p.vy;
            p.life -= 1 + p.decay;

            if (p.life <= 0) {
                // Remove from active particles and return to pool
                this.particles.splice(i, 1);
                this.releaseParticle(p);
            }
        }
    }

    drawParticles(ctx) {
        // Use traditional for loop instead of forEach for better performance
        for (let i = 0; i < this.particles.length; i++) {
            const p = this.particles[i];
            
            // Save context
            ctx.save();
            
            // Set alpha based on remaining life
            const alpha = Math.min(1, p.life / p.maxLife);
            ctx.globalAlpha = alpha;
            
            // Add glow effect if applicable
            if (p.glow > 0) {
                ctx.shadowColor = p.color;
                ctx.shadowBlur = p.size * p.glow * 5;
            }
            
            // Draw based on particle type
            switch(p.type) {
                case this.particleTypes.SPARKLE:
                    // Sparkle particles twinkle
                    const twinkle = Math.abs(Math.sin(p.life * 0.2)) * 0.5 + 0.5;
                    ctx.globalAlpha = alpha * twinkle;
                    ctx.fillStyle = p.color;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                    ctx.fill();
                    break;
                    
                case this.particleTypes.SMOKE:
                    // Smoke particles expand as they rise
                    const scale = 1 + (1 - p.life / p.maxLife) * 2;
                    ctx.fillStyle = p.color;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.size * scale, 0, Math.PI * 2);
                    ctx.fill();
                    break;
                    
                case this.particleTypes.EXPLOSION:
                    // Explosion particles rotate
                    ctx.translate(p.x, p.y);
                    ctx.rotate(p.life * 0.1);
                    ctx.fillStyle = p.color;
                    ctx.fillRect(-p.size/2, -p.size/2, p.size, p.size);
                    break;
                    
                case this.particleTypes.GLOW:
                    // Glow particles pulse
                    const pulse = Math.sin(p.life * 0.3) * 0.3 + 0.7;
                    ctx.globalAlpha = alpha * pulse;
                    ctx.fillStyle = p.color;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                    ctx.fill();
                    break;
                    
                default:
                    // Default particles
                    ctx.fillStyle = p.color;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                    ctx.fill();
            }
            
            // Restore context
            ctx.restore();
        }
        ctx.globalAlpha = 1;
        ctx.shadowBlur = 0;
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