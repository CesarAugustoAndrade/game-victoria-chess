"""
EPIC PARTICLE SYSTEM - Blood, Fire, and Glory!
"""

import pygame
import random
import math
from typing import List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class Particle:
    """Partícula individual"""
    x: float
    y: float
    vx: float  # Velocidad X
    vy: float  # Velocidad Y
    life: float  # Vida restante (0-1)
    max_life: float  # Vida máxima
    size: float
    color: Tuple[int, int, int, int]  # RGBA
    gravity: float = 0
    fade: bool = True
    shrink: bool = False
    glow: bool = False
    trail: bool = False
    trail_positions: List[Tuple[float, float]] = field(default_factory=list)

    def __post_init__(self):
        if self.trail and self.trail_positions is None:
            self.trail_positions = []


class ParticleSystem:
    """Sistema de partículas épico para efectos visuales"""

    def __init__(self, max_particles: int = 1000):
        self.particles: List[Particle] = []
        self.max_particles = max_particles
        self.emitters: List['ParticleEmitter'] = []

    def update(self, dt: float):
        """Actualiza todas las partículas"""
        # Actualizar emisores
        for emitter in self.emitters[:]:
            emitter.update(dt)
            if emitter.finished:
                self.emitters.remove(emitter)

        # Actualizar partículas
        for particle in self.particles[:]:
            # Aplicar física
            particle.vy += particle.gravity * dt
            particle.x += particle.vx * dt
            particle.y += particle.vy * dt

            # Actualizar vida
            particle.life -= dt / particle.max_life

            # Guardar trail si está activo
            if particle.trail and len(particle.trail_positions) < 10:
                particle.trail_positions.append((particle.x, particle.y))

            # Remover partículas muertas
            if particle.life <= 0:
                self.particles.remove(particle)

    def render(self, screen: pygame.Surface, camera_offset: Tuple[int, int] = (0, 0)):
        """Renderiza todas las partículas"""
        for particle in self.particles:
            x = int(particle.x - camera_offset[0])
            y = int(particle.y - camera_offset[1])

            # Calcular alpha basado en vida
            alpha = int(255 * particle.life) if particle.fade else 255

            # Calcular tamaño
            size = particle.size
            if particle.shrink:
                size = particle.size * particle.life

            # Renderizar trail si existe
            if particle.trail and particle.trail_positions:
                for i, (tx, ty) in enumerate(particle.trail_positions):
                    trail_alpha = int(alpha * (i / len(particle.trail_positions)))
                    trail_size = size * (i / len(particle.trail_positions))
                    if trail_alpha > 0 and trail_size > 0:
                        self._draw_particle(
                            screen,
                            int(tx - camera_offset[0]),
                            int(ty - camera_offset[1]),
                            trail_size,
                            (*particle.color[:3], trail_alpha),
                            particle.glow
                        )

            # Renderizar partícula principal
            if alpha > 0 and size > 0:
                self._draw_particle(screen, x, y, size, (*particle.color[:3], alpha), particle.glow)

    def _draw_particle(self, screen: pygame.Surface, x: int, y: int, size: float,
                      color: Tuple[int, int, int, int], glow: bool):
        """Dibuja una partícula individual"""
        if size < 1:
            return

        # Crear superficie con alpha
        particle_surf = pygame.Surface((int(size * 4), int(size * 4)), pygame.SRCALPHA)

        if glow:
            # Efecto de brillo con múltiples capas
            for i in range(3):
                glow_size = size * (3 - i)
                glow_alpha = color[3] // (i + 2)
                glow_color = (*color[:3], glow_alpha)
                pygame.draw.circle(particle_surf, glow_color,
                                 (int(size * 2), int(size * 2)), int(glow_size))

        # Partícula central
        pygame.draw.circle(particle_surf, color, (int(size * 2), int(size * 2)), int(size))

        # Blit a la pantalla
        screen.blit(particle_surf, (x - size * 2, y - size * 2))

    def add_particle(self, particle: Particle):
        """Añade una partícula al sistema"""
        if len(self.particles) < self.max_particles:
            self.particles.append(particle)

    def add_emitter(self, emitter: 'ParticleEmitter'):
        """Añade un emisor de partículas"""
        self.emitters.append(emitter)
        emitter.particle_system = self

    def clear(self):
        """Limpia todas las partículas"""
        self.particles.clear()
        self.emitters.clear()


class ParticleEmitter:
    """Emisor de partículas para efectos continuos o explosivos"""

    def __init__(self, x: float, y: float, emission_rate: float = 10,
                 lifetime: float = -1, burst: bool = False, burst_count: int = 20):
        self.x = x
        self.y = y
        self.emission_rate = emission_rate
        self.lifetime = lifetime
        self.burst = burst
        self.burst_count = burst_count
        self.time_alive = 0
        self.emission_accumulator = 0
        self.finished = False
        self.particle_system: Optional[ParticleSystem] = None

        # Configuración de partículas
        self.particle_config = {
            'min_speed': 50,
            'max_speed': 200,
            'min_life': 0.5,
            'max_life': 2.0,
            'min_size': 2,
            'max_size': 6,
            'color': (255, 100, 0, 255),
            'gravity': 100,
            'fade': True,
            'shrink': True,
            'glow': False,
            'trail': False,
            'spread': 360  # Grados de dispersión
        }

    def update(self, dt: float):
        """Actualiza el emisor"""
        if self.finished or not self.particle_system:
            return

        self.time_alive += dt

        # Verificar lifetime
        if self.lifetime > 0 and self.time_alive >= self.lifetime:
            self.finished = True
            return

        if self.burst and self.time_alive == dt:
            # Modo explosión - emitir todas las partículas de una vez
            for _ in range(self.burst_count):
                self.emit_particle()
            self.finished = True
        else:
            # Modo continuo
            self.emission_accumulator += dt
            particles_to_emit = int(self.emission_accumulator * self.emission_rate)
            self.emission_accumulator -= particles_to_emit / self.emission_rate

            for _ in range(particles_to_emit):
                self.emit_particle()

    def emit_particle(self):
        """Emite una partícula"""
        config = self.particle_config

        # Ángulo aleatorio
        angle = random.uniform(
            -config['spread'] / 2,
            config['spread'] / 2
        ) * math.pi / 180

        # Velocidad aleatoria
        speed = random.uniform(config['min_speed'], config['max_speed'])
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle) - 50  # Bias hacia arriba

        # Crear partícula
        particle = Particle(
            x=self.x + random.uniform(-5, 5),
            y=self.y + random.uniform(-5, 5),
            vx=vx,
            vy=vy,
            life=1.0,
            max_life=random.uniform(config['min_life'], config['max_life']),
            size=random.uniform(config['min_size'], config['max_size']),
            color=config['color'],
            gravity=config['gravity'],
            fade=config['fade'],
            shrink=config['shrink'],
            glow=config['glow'],
            trail=config['trail']
        )

        self.particle_system.add_particle(particle)


class ParticleEffects:
    """Efectos de partículas predefinidos épicos"""

    @staticmethod
    def create_blood_explosion(system: ParticleSystem, x: float, y: float):
        """Crea una explosión de sangre"""
        emitter = ParticleEmitter(x, y, burst=True, burst_count=30)
        emitter.particle_config.update({
            'min_speed': 100,
            'max_speed': 300,
            'color': (180, 0, 0, 255),
            'gravity': 400,
            'min_size': 1,
            'max_size': 4,
            'glow': False,
            'trail': True
        })
        system.add_emitter(emitter)

    @staticmethod
    def create_fire_effect(system: ParticleSystem, x: float, y: float, duration: float = 2.0):
        """Crea un efecto de fuego"""
        emitter = ParticleEmitter(x, y, emission_rate=50, lifetime=duration)
        emitter.particle_config.update({
            'min_speed': 30,
            'max_speed': 80,
            'color': (255, random.randint(100, 200), 0, 255),
            'gravity': -50,  # Fuego sube
            'min_size': 2,
            'max_size': 8,
            'glow': True,
            'spread': 45
        })
        system.add_emitter(emitter)

    @staticmethod
    def create_dust_cloud(system: ParticleSystem, x: float, y: float):
        """Crea una nube de polvo"""
        emitter = ParticleEmitter(x, y, burst=True, burst_count=20)
        emitter.particle_config.update({
            'min_speed': 20,
            'max_speed': 60,
            'color': (150, 120, 80, 200),
            'gravity': 0,
            'min_size': 8,
            'max_size': 15,
            'min_life': 1.0,
            'max_life': 2.0,
            'shrink': True,
            'spread': 360
        })
        system.add_emitter(emitter)

    @staticmethod
    def create_spark_burst(system: ParticleSystem, x: float, y: float):
        """Crea una explosión de chispas"""
        emitter = ParticleEmitter(x, y, burst=True, burst_count=15)
        emitter.particle_config.update({
            'min_speed': 200,
            'max_speed': 400,
            'color': (255, 255, 200, 255),
            'gravity': 300,
            'min_size': 1,
            'max_size': 3,
            'min_life': 0.3,
            'max_life': 0.8,
            'glow': True,
            'trail': True,
            'spread': 120
        })
        system.add_emitter(emitter)

    @staticmethod
    def create_magic_aura(system: ParticleSystem, x: float, y: float, color: Tuple[int, int, int] = (100, 100, 255)):
        """Crea un aura mágica"""
        emitter = ParticleEmitter(x, y, emission_rate=20, lifetime=1.0)
        emitter.particle_config.update({
            'min_speed': 10,
            'max_speed': 30,
            'color': (*color, 200),
            'gravity': -20,
            'min_size': 3,
            'max_size': 6,
            'min_life': 1.0,
            'max_life': 2.0,
            'glow': True,
            'spread': 360
        })
        system.add_emitter(emitter)

    @staticmethod
    def create_arrow_trail(system: ParticleSystem, x: float, y: float):
        """Crea un rastro de flecha"""
        emitter = ParticleEmitter(x, y, emission_rate=30, lifetime=0.5)
        emitter.particle_config.update({
            'min_speed': 5,
            'max_speed': 20,
            'color': (200, 200, 200, 150),
            'gravity': 0,
            'min_size': 1,
            'max_size': 2,
            'min_life': 0.3,
            'max_life': 0.5,
            'spread': 30
        })
        system.add_emitter(emitter)

    @staticmethod
    def create_victory_celebration(system: ParticleSystem, x: float, y: float):
        """Crea fuegos artificiales de victoria"""
        colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]

        for _ in range(5):
            emitter = ParticleEmitter(
                x + random.randint(-100, 100),
                y + random.randint(-50, 50),
                burst=True,
                burst_count=50
            )
            color = random.choice(colors)
            emitter.particle_config.update({
                'min_speed': 100,
                'max_speed': 300,
                'color': (*color, 255),
                'gravity': 200,
                'min_size': 2,
                'max_size': 5,
                'glow': True,
                'trail': True,
                'spread': 360
            })
            system.add_emitter(emitter)