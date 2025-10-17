"""
Sistema de Clima y Ambiente Épico
"""

import pygame
import random
import math
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class WeatherType(Enum):
    """Tipos de clima disponibles"""
    CLEAR = "clear"
    RAIN = "rain"
    STORM = "storm"
    SNOW = "snow"
    FOG = "fog"
    SANDSTORM = "sandstorm"
    ASH_FALL = "ash_fall"  # Para batallas épicas


class TimeOfDay(Enum):
    """Momentos del día"""
    DAWN = "dawn"
    MORNING = "morning"
    NOON = "noon"
    AFTERNOON = "afternoon"
    DUSK = "dusk"
    NIGHT = "night"


@dataclass
class Particle:
    """Partícula de clima"""
    x: float
    y: float
    vx: float
    vy: float
    size: float
    alpha: int = 255
    life: float = 1.0
    color: Tuple[int, int, int] = (255, 255, 255)
    type: str = "generic"


class WeatherSystem:
    """Sistema de clima dinámico para ambientación épica"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Estado actual
        self.weather_type = WeatherType.CLEAR
        self.time_of_day = TimeOfDay.NOON
        self.intensity = 0.5  # 0.0 a 1.0

        # Partículas
        self.particles: List[Particle] = []
        self.max_particles = 500

        # Viento
        self.wind_strength = 0.0
        self.wind_direction = 0.0  # En radianes
        self.wind_variation = 0.0

        # Efectos visuales
        self.fog_surface = None
        self.lighting_surface = None
        self.lightning_flash = 0
        self.thunder_delay = 0

        # Configuración por tipo de clima
        self.weather_configs = {
            WeatherType.CLEAR: {
                'particles': 0,
                'wind': 0.1,
                'fog_alpha': 0,
                'ambient_color': (255, 255, 255)
            },
            WeatherType.RAIN: {
                'particles': 200,
                'wind': 0.3,
                'fog_alpha': 30,
                'ambient_color': (180, 190, 200)
            },
            WeatherType.STORM: {
                'particles': 300,
                'wind': 0.7,
                'fog_alpha': 50,
                'ambient_color': (120, 130, 140)
            },
            WeatherType.SNOW: {
                'particles': 150,
                'wind': 0.2,
                'fog_alpha': 40,
                'ambient_color': (230, 240, 255)
            },
            WeatherType.FOG: {
                'particles': 0,
                'wind': 0.05,
                'fog_alpha': 120,
                'ambient_color': (200, 200, 210)
            },
            WeatherType.SANDSTORM: {
                'particles': 250,
                'wind': 0.8,
                'fog_alpha': 80,
                'ambient_color': (210, 180, 140)
            },
            WeatherType.ASH_FALL: {
                'particles': 100,
                'wind': 0.15,
                'fog_alpha': 60,
                'ambient_color': (150, 140, 140)
            }
        }

        # Inicializar superficies
        self._create_fog_surface()
        self._create_lighting_surface()

        # Sonidos ambientales
        self.ambient_sounds = {
            WeatherType.RAIN: "rain_loop",
            WeatherType.STORM: "storm_loop",
            WeatherType.SNOW: "wind_howl",
            WeatherType.SANDSTORM: "sandstorm_loop"
        }

    def _create_fog_surface(self):
        """Crea la superficie de niebla"""
        self.fog_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)

        # Crear patrón de niebla con gradiente y ruido
        for y in range(0, self.screen_height, 20):
            for x in range(0, self.screen_width, 20):
                # Ruido perlin simulado
                noise = math.sin(x * 0.01) * math.cos(y * 0.01)
                alpha = int(50 + noise * 30)
                alpha = max(0, min(255, alpha))

                # Dibujar círculos suaves para la niebla
                size = random.randint(40, 80)
                pygame.draw.circle(self.fog_surface, (200, 200, 200, alpha),
                                 (x + random.randint(-10, 10), y + random.randint(-10, 10)),
                                 size)

    def _create_lighting_surface(self):
        """Crea la superficie de iluminación"""
        self.lighting_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)

    def set_weather(self, weather_type: WeatherType, intensity: float = 0.5,
                    transition_time: float = 2.0):
        """Cambia el clima con transición suave"""
        self.weather_type = weather_type
        self.intensity = max(0.0, min(1.0, intensity))

        # Ajustar viento según el clima
        config = self.weather_configs[weather_type]
        self.wind_strength = config['wind'] * intensity

        # Limpiar partículas existentes si cambia drásticamente
        if weather_type == WeatherType.CLEAR or weather_type == WeatherType.FOG:
            self.particles.clear()

    def set_time_of_day(self, time: TimeOfDay):
        """Establece la hora del día"""
        self.time_of_day = time

    def update(self, delta_time: float):
        """Actualiza el sistema de clima"""
        # Actualizar viento
        self._update_wind(delta_time)

        # Generar nuevas partículas según el clima
        self._generate_particles()

        # Actualizar partículas existentes
        self._update_particles(delta_time)

        # Efectos especiales por clima
        if self.weather_type == WeatherType.STORM:
            self._update_storm_effects(delta_time)

        # Actualizar iluminación según hora del día
        self._update_lighting()

    def _update_wind(self, delta_time: float):
        """Actualiza el viento con variación natural"""
        # Variación sinusoidal del viento
        self.wind_variation += delta_time
        variation = math.sin(self.wind_variation * 0.5) * 0.3

        # Cambios aleatorios ocasionales en dirección
        if random.random() < 0.01:
            self.wind_direction += random.uniform(-0.5, 0.5)

        # Aplicar límites
        self.wind_direction = self.wind_direction % (2 * math.pi)

    def _generate_particles(self):
        """Genera partículas según el tipo de clima"""
        config = self.weather_configs[self.weather_type]
        target_particles = int(config['particles'] * self.intensity)

        if len(self.particles) < target_particles:
            particles_to_add = min(5, target_particles - len(self.particles))

            for _ in range(particles_to_add):
                if self.weather_type == WeatherType.RAIN:
                    self._create_rain_particle()
                elif self.weather_type == WeatherType.STORM:
                    self._create_storm_particle()
                elif self.weather_type == WeatherType.SNOW:
                    self._create_snow_particle()
                elif self.weather_type == WeatherType.SANDSTORM:
                    self._create_sand_particle()
                elif self.weather_type == WeatherType.ASH_FALL:
                    self._create_ash_particle()

    def _create_rain_particle(self):
        """Crea una partícula de lluvia"""
        particle = Particle(
            x=random.randint(-50, self.screen_width + 50),
            y=random.randint(-100, -10),
            vx=self.wind_strength * 100 * math.cos(self.wind_direction),
            vy=random.randint(400, 600),
            size=random.uniform(1, 3),
            alpha=random.randint(100, 200),
            color=(150, 180, 220),
            type="rain"
        )
        self.particles.append(particle)

    def _create_storm_particle(self):
        """Crea una partícula de tormenta (lluvia intensa)"""
        particle = Particle(
            x=random.randint(-100, self.screen_width + 100),
            y=random.randint(-100, -10),
            vx=self.wind_strength * 200 * math.cos(self.wind_direction),
            vy=random.randint(600, 800),
            size=random.uniform(2, 4),
            alpha=random.randint(150, 255),
            color=(100, 130, 180),
            type="storm_rain"
        )
        self.particles.append(particle)

    def _create_snow_particle(self):
        """Crea una partícula de nieve"""
        particle = Particle(
            x=random.randint(-50, self.screen_width + 50),
            y=random.randint(-50, -10),
            vx=self.wind_strength * 50 * math.cos(self.wind_direction) + random.uniform(-20, 20),
            vy=random.randint(30, 80),
            size=random.uniform(2, 6),
            alpha=random.randint(150, 255),
            color=(255, 255, 255),
            type="snow"
        )
        self.particles.append(particle)

    def _create_sand_particle(self):
        """Crea una partícula de arena"""
        particle = Particle(
            x=random.randint(-100, -10) if self.wind_direction < math.pi else random.randint(self.screen_width + 10, self.screen_width + 100),
            y=random.randint(0, self.screen_height),
            vx=self.wind_strength * 300 * math.cos(self.wind_direction),
            vy=random.uniform(-50, 50),
            size=random.uniform(1, 4),
            alpha=random.randint(50, 150),
            color=(210, 180, 140),
            type="sand"
        )
        self.particles.append(particle)

    def _create_ash_particle(self):
        """Crea una partícula de ceniza"""
        particle = Particle(
            x=random.randint(0, self.screen_width),
            y=random.randint(-50, -10),
            vx=self.wind_strength * 30 * math.cos(self.wind_direction) + random.uniform(-10, 10),
            vy=random.randint(20, 50),
            size=random.uniform(3, 8),
            alpha=random.randint(80, 180),
            color=(80, 80, 80),
            type="ash"
        )
        self.particles.append(particle)

    def _update_particles(self, delta_time: float):
        """Actualiza todas las partículas"""
        for particle in self.particles[:]:
            # Física básica
            particle.x += particle.vx * delta_time
            particle.y += particle.vy * delta_time

            # Efectos específicos por tipo
            if particle.type == "snow":
                # Movimiento ondulante de la nieve
                particle.x += math.sin(particle.y * 0.01) * 30 * delta_time

            elif particle.type == "ash":
                # Ceniza flotante
                particle.vy += random.uniform(-10, 10)
                particle.vx += random.uniform(-5, 5)

            # Reducir vida
            particle.life -= delta_time * 0.2

            # Eliminar partículas fuera de pantalla o muertas
            if (particle.y > self.screen_height + 100 or
                particle.x < -200 or particle.x > self.screen_width + 200 or
                particle.life <= 0):
                self.particles.remove(particle)

    def _update_storm_effects(self, delta_time: float):
        """Actualiza efectos especiales de tormenta"""
        # Relámpagos aleatorios
        if random.random() < 0.002 * self.intensity:  # Probabilidad baja
            self.lightning_flash = 255
            self.thunder_delay = random.uniform(0.5, 2.0)  # Delay para el trueno

        # Decay del flash
        if self.lightning_flash > 0:
            self.lightning_flash = max(0, self.lightning_flash - 1000 * delta_time)

        # Trueno después del relámpago
        if self.thunder_delay > 0:
            self.thunder_delay -= delta_time
            if self.thunder_delay <= 0:
                # Aquí se reproduciría el sonido del trueno
                pass

    def _update_lighting(self):
        """Actualiza la iluminación según la hora del día"""
        # Colores de iluminación por hora
        lighting_colors = {
            TimeOfDay.DAWN: (255, 200, 150, 50),      # Naranja suave
            TimeOfDay.MORNING: (255, 240, 200, 30),   # Amarillo claro
            TimeOfDay.NOON: (255, 255, 255, 0),       # Sin tinte
            TimeOfDay.AFTERNOON: (255, 230, 180, 20), # Amarillo cálido
            TimeOfDay.DUSK: (255, 150, 100, 80),      # Naranja intenso
            TimeOfDay.NIGHT: (100, 100, 150, 120)     # Azul oscuro
        }

        color = lighting_colors.get(self.time_of_day, (255, 255, 255, 0))
        self.lighting_surface.fill(color)

    def render(self, screen: pygame.Surface):
        """Renderiza los efectos de clima"""
        # Renderizar partículas
        self._render_particles(screen)

        # Renderizar niebla si aplica
        if self.weather_type in [WeatherType.FOG, WeatherType.RAIN, WeatherType.STORM,
                                 WeatherType.SANDSTORM, WeatherType.ASH_FALL]:
            self._render_fog(screen)

        # Renderizar iluminación
        self._render_lighting(screen)

        # Flash de relámpago
        if self.lightning_flash > 0:
            flash_surface = pygame.Surface((self.screen_width, self.screen_height))
            flash_surface.fill((255, 255, 255))
            flash_surface.set_alpha(int(self.lightning_flash))
            screen.blit(flash_surface, (0, 0))

    def _render_particles(self, screen: pygame.Surface):
        """Renderiza las partículas del clima"""
        for particle in self.particles:
            if particle.alpha <= 0:
                continue

            # Ajustar alpha según la vida
            alpha = int(particle.alpha * particle.life)

            if particle.type in ["rain", "storm_rain"]:
                # Lluvia como líneas
                end_x = particle.x + particle.vx * 0.1
                end_y = particle.y + particle.vy * 0.1

                # Crear superficie para la línea con alpha
                line_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                pygame.draw.line(line_surface, (*particle.color, alpha),
                               (particle.x, particle.y), (end_x, end_y),
                               int(particle.size))
                screen.blit(line_surface, (0, 0))

            else:
                # Otros tipos como círculos
                particle_surface = pygame.Surface((int(particle.size * 2), int(particle.size * 2)), pygame.SRCALPHA)

                if particle.type == "snow":
                    # Copos de nieve con forma de estrella
                    center = int(particle.size)
                    # Cruz principal
                    pygame.draw.line(particle_surface, (*particle.color, alpha),
                                   (center - particle.size, center),
                                   (center + particle.size, center), 2)
                    pygame.draw.line(particle_surface, (*particle.color, alpha),
                                   (center, center - particle.size),
                                   (center, center + particle.size), 2)
                    # Cruz diagonal
                    s = int(particle.size * 0.7)
                    pygame.draw.line(particle_surface, (*particle.color, alpha),
                                   (center - s, center - s),
                                   (center + s, center + s), 1)
                    pygame.draw.line(particle_surface, (*particle.color, alpha),
                                   (center - s, center + s),
                                   (center + s, center - s), 1)
                else:
                    # Círculo simple para arena, ceniza, etc.
                    pygame.draw.circle(particle_surface, (*particle.color, alpha),
                                     (int(particle.size), int(particle.size)),
                                     int(particle.size))

                screen.blit(particle_surface, (particle.x - particle.size, particle.y - particle.size))

    def _render_fog(self, screen: pygame.Surface):
        """Renderiza el efecto de niebla"""
        config = self.weather_configs[self.weather_type]
        alpha = int(config['fog_alpha'] * self.intensity)

        if alpha > 0:
            # Animar la niebla con movimiento lento
            offset_x = int(math.sin(pygame.time.get_ticks() * 0.0001) * 20)
            offset_y = int(math.cos(pygame.time.get_ticks() * 0.0001) * 10)

            fog_copy = self.fog_surface.copy()
            fog_copy.set_alpha(alpha)
            screen.blit(fog_copy, (offset_x, offset_y))

    def _render_lighting(self, screen: pygame.Surface):
        """Renderiza los efectos de iluminación"""
        if self.time_of_day != TimeOfDay.NOON:
            screen.blit(self.lighting_surface, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

    def get_ambient_color(self) -> Tuple[int, int, int]:
        """Obtiene el color ambiente actual"""
        config = self.weather_configs[self.weather_type]
        base_color = config['ambient_color']

        # Modificar por hora del día
        time_modifiers = {
            TimeOfDay.DAWN: (1.2, 0.9, 0.8),
            TimeOfDay.MORNING: (1.1, 1.0, 0.9),
            TimeOfDay.NOON: (1.0, 1.0, 1.0),
            TimeOfDay.AFTERNOON: (1.1, 1.0, 0.9),
            TimeOfDay.DUSK: (1.2, 0.8, 0.6),
            TimeOfDay.NIGHT: (0.5, 0.5, 0.7)
        }

        modifier = time_modifiers.get(self.time_of_day, (1.0, 1.0, 1.0))

        return tuple(int(min(255, c * m)) for c, m in zip(base_color, modifier))

    def create_battle_atmosphere(self):
        """Crea atmósfera épica de batalla"""
        # Ceniza cayendo y niebla de guerra
        self.set_weather(WeatherType.ASH_FALL, 0.7)

        # Añadir partículas de fuego/chispas ocasionales
        for _ in range(10):
            spark = Particle(
                x=random.randint(0, self.screen_width),
                y=random.randint(0, self.screen_height // 2),
                vx=random.uniform(-50, 50),
                vy=random.uniform(-100, -50),
                size=2,
                alpha=255,
                color=(255, random.randint(100, 200), 0),
                type="spark"
            )
            self.particles.append(spark)