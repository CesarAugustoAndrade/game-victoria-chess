"""
Sistema de Efectos de Cámara Cinematográficos
"""

import pygame
import math
import random
from typing import Optional, Tuple, List
from dataclasses import dataclass
from enum import Enum


class ZoomMode(Enum):
    """Modos de zoom de la cámara"""
    NORMAL = 1.0
    COMBAT_FOCUS = 1.3
    OVERVIEW = 0.8
    DRAMATIC = 1.5
    CINEMATIC = 2.0


class ScreenEffect(Enum):
    """Efectos de post-procesamiento"""
    NONE = "none"
    VIGNETTE = "vignette"
    BLOOD_OVERLAY = "blood_overlay"
    VICTORY_GLOW = "victory_glow"
    DEFEAT_DARKNESS = "defeat_darkness"
    SLOW_MOTION = "slow_motion"
    SPEED_LINES = "speed_lines"


@dataclass
class CameraShake:
    """Configuración de temblor de cámara"""
    intensity: float = 0.0
    duration: float = 0.0
    frequency: float = 30.0  # Vibraciones por segundo
    decay: float = 0.95  # Qué tan rápido decae
    elapsed: float = 0.0
    offset_x: float = 0.0
    offset_y: float = 0.0


class CinematicCamera:
    """Cámara cinematográfica con efectos épicos"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Posición y zoom
        self.x = 0.0
        self.y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0
        self.zoom = 1.0
        self.target_zoom = 1.0
        self.rotation = 0.0
        self.target_rotation = 0.0

        # Velocidades de interpolación
        self.pan_speed = 5.0
        self.zoom_speed = 3.0
        self.rotation_speed = 2.0

        # FLAGS para desactivar animaciones
        self.enable_pan_animation = False  # DESACTIVADO - movimiento instantáneo
        self.enable_zoom_animation = False  # DESACTIVADO - zoom instantáneo
        self.enable_rotation_animation = False  # DESACTIVADO - rotación instantánea

        # Shake
        self.shake = CameraShake()

        # Efectos activos
        self.active_effects: List[ScreenEffect] = []
        self.effect_intensities = {}

        # Slow motion
        self.time_scale = 1.0
        self.target_time_scale = 1.0

        # Viñeta
        self.vignette_intensity = 0.3
        self.vignette_surface = None
        self._create_vignette()

        # Flash de pantalla
        self.flash_color = (255, 255, 255)
        self.flash_alpha = 0
        self.flash_decay = 10.0

        # Speed lines para movimiento rápido
        self.speed_lines = []
        self.speed_line_alpha = 0

        # Letterbox para modo cinemático
        self.letterbox_height = 0
        self.target_letterbox = 0

        # Modo de enfoque
        self.focus_point: Optional[Tuple[float, float]] = None
        self.focus_strength = 0.0

    def _create_vignette(self):
        """Crea el efecto de viñeta"""
        size = max(self.screen_width, self.screen_height)
        self.vignette_surface = pygame.Surface((size, size), pygame.SRCALPHA)

        center = size // 2
        max_radius = size // 2

        for radius in range(max_radius, 0, -5):
            alpha = int(255 * (1 - radius / max_radius) * self.vignette_intensity)
            color = (0, 0, 0, alpha)
            pygame.draw.circle(self.vignette_surface, color, (center, center), radius)

    def set_position(self, x: float, y: float, instant: bool = False):
        """Establece la posición de la cámara"""
        self.target_x = x
        self.target_y = y
        if instant:
            self.x = x
            self.y = y

    def set_zoom(self, zoom: float, instant: bool = False):
        """Establece el nivel de zoom - DESACTIVADO"""
        # Mantener zoom en 1.0 siempre (sin zoom)
        self.zoom = 1.0
        self.target_zoom = 1.0

    def shake_camera(self, intensity: float, duration: float = 0.5,
                     frequency: float = 30.0):
        """Inicia temblor de cámara - DESACTIVADO"""
        # No hacer nada - shake desactivado
        pass

    def add_trauma(self, trauma: float):
        """Añade trauma a la cámara (para shake acumulativo) - DESACTIVADO"""
        # No hacer nada - shake desactivado
        pass

    def screen_flash(self, color: Tuple[int, int, int] = (255, 255, 255),
                    alpha: int = 200):
        """Crea un flash de pantalla"""
        self.flash_color = color
        self.flash_alpha = min(255, alpha)

    def set_slow_motion(self, time_scale: float, duration: float = 1.0):
        """Activa cámara lenta"""
        self.target_time_scale = max(0.1, min(1.0, time_scale))
        # Auto-reset después de la duración
        pygame.time.set_timer(pygame.USEREVENT + 1, int(duration * 1000))

    def focus_on_point(self, x: float, y: float, zoom: float = 1.3,
                      duration: float = 0.5):
        """Enfoca en un punto con zoom dramático - DESACTIVADO"""
        # No hacer nada - zoom desactivado
        pass

    def enter_cinematic_mode(self):
        """Entra en modo cinemático con letterbox"""
        self.target_letterbox = 80
        self.add_effect(ScreenEffect.VIGNETTE)

    def exit_cinematic_mode(self):
        """Sale del modo cinemático"""
        self.target_letterbox = 0
        self.remove_effect(ScreenEffect.VIGNETTE)

    def add_effect(self, effect: ScreenEffect, intensity: float = 1.0):
        """Añade un efecto de pantalla"""
        if effect not in self.active_effects:
            self.active_effects.append(effect)
        self.effect_intensities[effect] = intensity

    def remove_effect(self, effect: ScreenEffect):
        """Elimina un efecto de pantalla"""
        if effect in self.active_effects:
            self.active_effects.remove(effect)
            self.effect_intensities.pop(effect, None)

    def create_speed_lines(self, direction: float, intensity: float = 1.0):
        """Crea líneas de velocidad para movimiento rápido"""
        self.speed_lines.clear()
        num_lines = int(20 * intensity)

        for _ in range(num_lines):
            # Punto de origen aleatorio en los bordes
            if random.random() < 0.5:
                # Bordes horizontales
                x = random.randint(0, self.screen_width)
                y = 0 if random.random() < 0.5 else self.screen_height
            else:
                # Bordes verticales
                x = 0 if random.random() < 0.5 else self.screen_width
                y = random.randint(0, self.screen_height)

            # Calcular punto final basado en dirección
            length = random.randint(100, 300)
            end_x = x + math.cos(direction) * length
            end_y = y + math.sin(direction) * length

            self.speed_lines.append({
                'start': (x, y),
                'end': (end_x, end_y),
                'alpha': random.randint(50, 150)
            })

        self.speed_line_alpha = 255

    def update(self, delta_time: float):
        """Actualiza la cámara"""
        # Interpolar posición (o movimiento instantáneo)
        if self.enable_pan_animation:
            if abs(self.x - self.target_x) > 0.1:
                self.x += (self.target_x - self.x) * self.pan_speed * delta_time
            else:
                self.x = self.target_x

            if abs(self.y - self.target_y) > 0.1:
                self.y += (self.target_y - self.y) * self.pan_speed * delta_time
            else:
                self.y = self.target_y
        else:
            # Movimiento instantáneo
            self.x = self.target_x
            self.y = self.target_y

        # Interpolar zoom (o zoom instantáneo)
        if self.enable_zoom_animation:
            if abs(self.zoom - self.target_zoom) > 0.01:
                self.zoom += (self.target_zoom - self.zoom) * self.zoom_speed * delta_time
            else:
                self.zoom = self.target_zoom
        else:
            # Zoom instantáneo
            self.zoom = self.target_zoom

        # Interpolar rotación (o rotación instantánea)
        if self.enable_rotation_animation:
            if abs(self.rotation - self.target_rotation) > 0.01:
                self.rotation += (self.target_rotation - self.rotation) * self.rotation_speed * delta_time
            else:
                self.rotation = self.target_rotation
        else:
            # Rotación instantánea
            self.rotation = self.target_rotation

        # Shake desactivado - mantener offsets en 0
        self.shake.intensity = 0
        self.shake.offset_x = 0
        self.shake.offset_y = 0

        # Actualizar flash
        if self.flash_alpha > 0:
            self.flash_alpha = max(0, self.flash_alpha - self.flash_decay)

        # Actualizar time scale
        if abs(self.time_scale - self.target_time_scale) > 0.01:
            self.time_scale += (self.target_time_scale - self.time_scale) * 5 * delta_time

        # Actualizar letterbox
        if abs(self.letterbox_height - self.target_letterbox) > 1:
            self.letterbox_height += (self.target_letterbox - self.letterbox_height) * 5 * delta_time
        else:
            self.letterbox_height = self.target_letterbox

        # Actualizar speed lines
        if self.speed_line_alpha > 0:
            self.speed_line_alpha = max(0, self.speed_line_alpha - 500 * delta_time)

        # Actualizar focus
        if self.focus_strength > 0:
            self.focus_strength = max(0, self.focus_strength - delta_time)

    def apply_transform(self, screen: pygame.Surface) -> pygame.Surface:
        """Aplica transformaciones de cámara a la pantalla"""
        # Crear superficie temporal si hay transformaciones
        if self.zoom != 1.0 or self.rotation != 0 or self.shake.intensity > 0:
            # Calcular nuevo tamaño con zoom
            new_width = max(1, min(10000, int(self.screen_width * self.zoom)))
            new_height = max(1, min(10000, int(self.screen_height * self.zoom)))

            # Validar dimensiones
            if new_width <= 0 or new_height <= 0:
                return screen

            # Crear superficie escalada
            scaled_surface = pygame.Surface((new_width, new_height))
            pygame.transform.scale(screen, (new_width, new_height), scaled_surface)

            # Aplicar rotación si hay
            if self.rotation != 0:
                scaled_surface = pygame.transform.rotate(scaled_surface, self.rotation)

            # Calcular posición con shake
            pos_x = (self.screen_width - new_width) // 2 + self.shake.offset_x
            pos_y = (self.screen_height - new_height) // 2 + self.shake.offset_y

            # Clear y blit
            final_surface = pygame.Surface((self.screen_width, self.screen_height))
            final_surface.fill((0, 0, 0))
            final_surface.blit(scaled_surface, (pos_x, pos_y))

            return final_surface

        return screen

    def render_effects(self, screen: pygame.Surface):
        """Renderiza efectos de post-procesamiento"""
        # Viñeta
        if ScreenEffect.VIGNETTE in self.active_effects:
            intensity = self.effect_intensities.get(ScreenEffect.VIGNETTE, 1.0)
            vignette = self.vignette_surface.copy()
            vignette.set_alpha(int(255 * intensity * 0.5))
            screen.blit(vignette, (0, 0))

        # Speed lines
        if self.speed_line_alpha > 0:
            for line in self.speed_lines:
                alpha = int((line['alpha'] / 255.0) * self.speed_line_alpha)
                # Crear superficie para la línea con alpha
                line_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                pygame.draw.line(line_surface,
                               (255, 255, 255, alpha),
                               line['start'], line['end'], 3)
                screen.blit(line_surface, (0, 0))

        # Flash de pantalla
        if self.flash_alpha > 0:
            flash_surface = pygame.Surface((self.screen_width, self.screen_height))
            flash_surface.fill(self.flash_color)
            flash_surface.set_alpha(self.flash_alpha)
            screen.blit(flash_surface, (0, 0))

        # Letterbox para modo cinemático
        if self.letterbox_height > 0:
            height = int(self.letterbox_height)
            # Barra superior
            pygame.draw.rect(screen, (0, 0, 0),
                           (0, 0, self.screen_width, height))
            # Barra inferior
            pygame.draw.rect(screen, (0, 0, 0),
                           (0, self.screen_height - height, self.screen_width, height))

        # Overlay de victoria
        if ScreenEffect.VICTORY_GLOW in self.active_effects:
            glow_surface = pygame.Surface((self.screen_width, self.screen_height))
            glow_surface.fill((255, 215, 0))  # Dorado
            glow_surface.set_alpha(30)
            screen.blit(glow_surface, (0, 0))

        # Overlay de derrota
        if ScreenEffect.DEFEAT_DARKNESS in self.active_effects:
            dark_surface = pygame.Surface((self.screen_width, self.screen_height))
            dark_surface.fill((20, 0, 0))  # Rojo oscuro
            dark_surface.set_alpha(100)
            screen.blit(dark_surface, (0, 0))

        # Efecto de sangre
        if ScreenEffect.BLOOD_OVERLAY in self.active_effects:
            self._render_blood_overlay(screen)

    def _render_blood_overlay(self, screen: pygame.Surface):
        """Renderiza overlay de sangre en los bordes"""
        blood_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)

        # Crear salpicaduras de sangre en los bordes
        num_splatters = 15
        for _ in range(num_splatters):
            # Posición aleatoria en los bordes
            if random.random() < 0.5:
                x = random.randint(0, 100) if random.random() < 0.5 else random.randint(self.screen_width - 100, self.screen_width)
                y = random.randint(0, self.screen_height)
            else:
                x = random.randint(0, self.screen_width)
                y = random.randint(0, 100) if random.random() < 0.5 else random.randint(self.screen_height - 100, self.screen_height)

            # Dibujar salpicadura
            radius = random.randint(20, 60)
            alpha = random.randint(50, 150)
            pygame.draw.circle(blood_surface, (139, 0, 0, alpha), (x, y), radius)

        screen.blit(blood_surface, (0, 0))

    def get_offset(self) -> Tuple[float, float]:
        """Obtiene el offset total de la cámara"""
        return (self.x + self.shake.offset_x, self.y + self.shake.offset_y)

    def world_to_screen(self, world_x: float, world_y: float) -> Tuple[float, float]:
        """Convierte coordenadas del mundo a pantalla"""
        screen_x = (world_x - self.x) * self.zoom + self.shake.offset_x
        screen_y = (world_y - self.y) * self.zoom + self.shake.offset_y
        return (screen_x, screen_y)

    def screen_to_world(self, screen_x: float, screen_y: float) -> Tuple[float, float]:
        """Convierte coordenadas de pantalla a mundo"""
        world_x = (screen_x - self.shake.offset_x) / self.zoom + self.x
        world_y = (screen_y - self.shake.offset_y) / self.zoom + self.y
        return (world_x, world_y)

    def is_on_screen(self, x: float, y: float, margin: float = 50) -> bool:
        """Verifica si un punto está en pantalla"""
        screen_x, screen_y = self.world_to_screen(x, y)
        return (-margin <= screen_x <= self.screen_width + margin and
                -margin <= screen_y <= self.screen_height + margin)


class CombatZoomController:
    """Controlador automático de zoom para combates"""

    def __init__(self, camera: CinematicCamera):
        self.camera = camera
        self.combat_active = False
        self.zoom_level = ZoomMode.NORMAL
        self.auto_zoom_enabled = False  # DESACTIVADO - No zoom automático en combate
        self.combat_timer = 0.0
        self.combat_duration = 1.0  # Segundos antes de retornar a normal

    def update(self, delta_time: float):
        """Actualiza el controlador de zoom de combate"""
        if self.combat_active:
            self.combat_timer += delta_time

            # Retornar a zoom normal después de la duración
            if self.combat_timer >= self.combat_duration:
                self.end_combat()

    def start_combat(self, attacker_pos: Tuple[float, float],
                    defender_pos: Tuple[float, float]):
        """Inicia zoom de combate - DESACTIVADO"""
        # No hacer nada - zoom y efectos de cámara desactivados
        pass

    def end_combat(self):
        """Termina el zoom de combate - DESACTIVADO"""
        # No hacer nada - zoom desactivado
        pass

    def critical_hit(self):
        """Efecto para golpe crítico - DESACTIVADO"""
        # No hacer nada - efectos de cámara desactivados
        pass

    def unit_death(self, position: Tuple[float, float]):
        """Efecto cuando muere una unidad - DESACTIVADO"""
        # No hacer nada - efectos de cámara desactivados
        pass