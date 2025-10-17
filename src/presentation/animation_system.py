"""
Sistema de Animaciones Épico con Tweening y Efectos Cinematográficos
"""

import pygame
import math
from typing import Callable, Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class EaseType(Enum):
    """Tipos de interpolación para animaciones suaves"""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    BOUNCE = "bounce"
    ELASTIC = "elastic"
    BACK = "back"
    CUBIC = "cubic"
    SINE = "sine"
    EXPO = "expo"


class AnimationState(Enum):
    """Estados de una animación"""
    IDLE = "idle"
    MOVING = "moving"
    ATTACKING = "attacking"
    DEFENDING = "defending"
    DYING = "dying"
    CELEBRATING = "celebrating"
    PANICKING = "panicking"


@dataclass
class Tween:
    """Representa una interpolación entre dos valores"""
    start_value: float
    end_value: float
    duration: float
    elapsed: float = 0.0
    ease_type: EaseType = EaseType.EASE_IN_OUT
    on_complete: Optional[Callable] = None
    on_update: Optional[Callable[[float], None]] = None
    loop: bool = False
    yoyo: bool = False  # Ping-pong animation
    delay: float = 0.0
    _delay_elapsed: float = 0.0
    _direction: int = 1  # 1 for forward, -1 for backward (yoyo)

    @property
    def is_complete(self) -> bool:
        """Verifica si la animación completó"""
        if self.loop:
            return False
        return self.elapsed >= self.duration and self._delay_elapsed >= self.delay

    @property
    def progress(self) -> float:
        """Obtiene el progreso normalizado (0-1)"""
        if self._delay_elapsed < self.delay:
            return 0.0
        if self.duration <= 0:
            return 1.0
        return min(1.0, self.elapsed / self.duration)

    def get_value(self) -> float:
        """Obtiene el valor actual interpolado"""
        t = self.progress

        # Aplicar función de ease
        t = self._apply_ease(t)

        # Interpolar entre valores
        return self.start_value + (self.end_value - self.start_value) * t

    def update(self, delta_time: float) -> float:
        """Actualiza el tween y retorna el valor actual"""
        # Manejar delay
        if self._delay_elapsed < self.delay:
            self._delay_elapsed += delta_time
            return self.start_value

        # Actualizar tiempo transcurrido
        self.elapsed += delta_time * self._direction

        # Manejar yoyo
        if self.yoyo and (self.elapsed >= self.duration or self.elapsed <= 0):
            self._direction *= -1
            self.elapsed = max(0, min(self.duration, self.elapsed))

        # Manejar loop
        if self.loop and self.elapsed >= self.duration:
            self.elapsed = 0
            if not self.yoyo:
                self._delay_elapsed = 0  # Reset delay on loop

        value = self.get_value()

        # Callback de actualización
        if self.on_update:
            self.on_update(value)

        # Callback de completado
        if self.is_complete and self.on_complete:
            self.on_complete()
            self.on_complete = None  # Evitar llamadas múltiples

        return value

    def _apply_ease(self, t: float) -> float:
        """Aplica la función de easing al progreso"""
        if self.ease_type == EaseType.LINEAR:
            return t

        elif self.ease_type == EaseType.EASE_IN:
            return t * t

        elif self.ease_type == EaseType.EASE_OUT:
            return 1 - (1 - t) ** 2

        elif self.ease_type == EaseType.EASE_IN_OUT:
            if t < 0.5:
                return 2 * t * t
            else:
                return 1 - pow(-2 * t + 2, 2) / 2

        elif self.ease_type == EaseType.BOUNCE:
            if t < 0.363636:
                return 7.5625 * t * t
            elif t < 0.727272:
                t -= 0.545454
                return 7.5625 * t * t + 0.75
            elif t < 0.909090:
                t -= 0.818181
                return 7.5625 * t * t + 0.9375
            else:
                t -= 0.954545
                return 7.5625 * t * t + 0.984375

        elif self.ease_type == EaseType.ELASTIC:
            if t == 0 or t == 1:
                return t
            p = 0.3
            s = p / 4
            return pow(2, -10 * t) * math.sin((t - s) * (2 * math.pi) / p) + 1

        elif self.ease_type == EaseType.BACK:
            c1 = 1.70158
            c3 = c1 + 1
            if t < 0.5:
                return (pow(2 * t, 2) * ((c3 + 1) * 2 * t - c3)) / 2
            else:
                return (pow(2 * t - 2, 2) * ((c3 + 1) * (t * 2 - 2) + c3) + 2) / 2

        elif self.ease_type == EaseType.CUBIC:
            if t < 0.5:
                return 4 * t * t * t
            else:
                return 1 - pow(-2 * t + 2, 3) / 2

        elif self.ease_type == EaseType.SINE:
            return -(math.cos(math.pi * t) - 1) / 2

        elif self.ease_type == EaseType.EXPO:
            if t == 0:
                return 0
            elif t == 1:
                return 1
            elif t < 0.5:
                return pow(2, 20 * t - 10) / 2
            else:
                return (2 - pow(2, -20 * t + 10)) / 2

        return t


@dataclass
class AnimationSequence:
    """Secuencia de animaciones que se ejecutan una tras otra"""
    animations: List[Tween] = field(default_factory=list)
    current_index: int = 0
    on_complete: Optional[Callable] = None
    loop: bool = False

    @property
    def is_complete(self) -> bool:
        """Verifica si toda la secuencia completó"""
        if self.loop:
            return False
        return self.current_index >= len(self.animations)

    @property
    def current_animation(self) -> Optional[Tween]:
        """Obtiene la animación actual"""
        if self.current_index < len(self.animations):
            return self.animations[self.current_index]
        return None

    def add(self, tween: Tween) -> 'AnimationSequence':
        """Añade una animación a la secuencia"""
        self.animations.append(tween)
        return self

    def update(self, delta_time: float) -> Optional[float]:
        """Actualiza la secuencia"""
        if not self.current_animation:
            if self.loop and self.animations:
                self.current_index = 0
                # Reset todas las animaciones
                for anim in self.animations:
                    anim.elapsed = 0
                    anim._delay_elapsed = 0
            else:
                if self.on_complete and not self.is_complete:
                    self.on_complete()
                return None

        current = self.current_animation
        if current:
            value = current.update(delta_time)

            if current.is_complete:
                self.current_index += 1

            return value

        return None


class AnimationManager:
    """Gestor principal de animaciones del juego"""

    def __init__(self):
        self.tweens: Dict[str, Tween] = {}
        self.sequences: Dict[str, AnimationSequence] = {}
        self.sprite_animations: Dict[str, 'SpriteAnimation'] = {}
        self.particles_animations: List['ParticleAnimation'] = []

    def add_tween(self, name: str, tween: Tween) -> None:
        """Añade un tween al gestor"""
        self.tweens[name] = tween

    def create_tween(self, name: str, start: float, end: float, duration: float,
                     ease: EaseType = EaseType.EASE_IN_OUT,
                     on_complete: Optional[Callable] = None,
                     on_update: Optional[Callable[[float], None]] = None) -> Tween:
        """Crea y añade un tween"""
        tween = Tween(start, end, duration, ease_type=ease,
                     on_complete=on_complete, on_update=on_update)
        self.tweens[name] = tween
        return tween

    def add_sequence(self, name: str, sequence: AnimationSequence) -> None:
        """Añade una secuencia de animaciones"""
        self.sequences[name] = sequence

    def remove(self, name: str) -> None:
        """Elimina una animación por nombre"""
        self.tweens.pop(name, None)
        self.sequences.pop(name, None)
        self.sprite_animations.pop(name, None)

    def update(self, delta_time: float) -> None:
        """Actualiza todas las animaciones"""
        # Actualizar tweens
        completed_tweens = []
        for name, tween in self.tweens.items():
            tween.update(delta_time)
            if tween.is_complete and not tween.loop:
                completed_tweens.append(name)

        # Eliminar tweens completados
        for name in completed_tweens:
            self.tweens.pop(name)

        # Actualizar secuencias
        completed_sequences = []
        for name, sequence in self.sequences.items():
            sequence.update(delta_time)
            if sequence.is_complete and not sequence.loop:
                completed_sequences.append(name)

        # Eliminar secuencias completadas
        for name in completed_sequences:
            self.sequences.pop(name)

        # Actualizar animaciones de sprites
        completed_sprites = []
        for name, sprite_anim in self.sprite_animations.items():
            sprite_anim.update(delta_time)
            if sprite_anim.is_complete and not sprite_anim.loop:
                completed_sprites.append(name)

        for name in completed_sprites:
            self.sprite_animations.pop(name)

        # Actualizar animaciones de partículas
        self.particles_animations = [p for p in self.particles_animations
                                     if not p.update(delta_time)]

    # ========== ANIMACIONES PREDEFINIDAS ==========

    def create_move_animation(self, start_pos: Tuple[int, int],
                             end_pos: Tuple[int, int],
                             duration: float = 0.5,
                             on_complete: Optional[Callable] = None) -> Tuple[Tween, Tween]:
        """Crea animación de movimiento para una unidad"""
        x_tween = Tween(start_pos[0], end_pos[0], duration,
                       ease_type=EaseType.EASE_IN_OUT)
        y_tween = Tween(start_pos[1], end_pos[1], duration,
                       ease_type=EaseType.EASE_IN_OUT,
                       on_complete=on_complete)

        return x_tween, y_tween

    def create_shake_animation(self, intensity: float = 10,
                              duration: float = 0.3) -> Tween:
        """Crea animación de temblor"""
        return Tween(intensity, 0, duration, ease_type=EaseType.ELASTIC)

    def create_pulse_animation(self, scale_min: float = 0.9,
                              scale_max: float = 1.1,
                              duration: float = 0.5) -> Tween:
        """Crea animación de pulso/latido"""
        return Tween(scale_min, scale_max, duration,
                    ease_type=EaseType.SINE, loop=True, yoyo=True)

    def create_fade_animation(self, start_alpha: int = 255,
                             end_alpha: int = 0,
                             duration: float = 1.0) -> Tween:
        """Crea animación de desvanecimiento"""
        return Tween(start_alpha, end_alpha, duration,
                    ease_type=EaseType.EASE_OUT)

    def create_bounce_animation(self, height: float = 50,
                               duration: float = 0.5) -> Tween:
        """Crea animación de rebote"""
        return Tween(0, -height, duration,
                    ease_type=EaseType.BOUNCE, yoyo=True)

    def create_damage_number_animation(self, x: int, y: int,
                                      damage: int, color: Tuple[int, int, int],
                                      font: pygame.font.Font) -> 'FloatingText':
        """Crea número de daño flotante"""
        return FloatingText(x, y, str(damage), color, font,
                          rise_speed=50, duration=1.5,
                          fade_start=0.5)

    def create_screen_flash(self, color: Tuple[int, int, int, int] = (255, 255, 255, 128),
                           duration: float = 0.1) -> 'ScreenFlash':
        """Crea flash de pantalla"""
        return ScreenFlash(color, duration)


@dataclass
class SpriteAnimation:
    """Animación de sprites frame por frame"""
    frames: List[pygame.Surface]
    frame_duration: float  # Duración de cada frame
    current_frame: int = 0
    elapsed: float = 0.0
    loop: bool = False
    on_complete: Optional[Callable] = None

    @property
    def is_complete(self) -> bool:
        """Verifica si la animación completó"""
        if self.loop:
            return False
        return self.current_frame >= len(self.frames) - 1

    def get_current_frame(self) -> pygame.Surface:
        """Obtiene el frame actual"""
        if self.frames:
            return self.frames[min(self.current_frame, len(self.frames) - 1)]
        return None

    def update(self, delta_time: float) -> None:
        """Actualiza la animación"""
        self.elapsed += delta_time

        if self.elapsed >= self.frame_duration:
            self.elapsed = 0
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    if self.on_complete:
                        self.on_complete()
                        self.on_complete = None


@dataclass
class FloatingText:
    """Texto flotante animado (para daño, mensajes, etc)"""
    x: float
    y: float
    text: str
    color: Tuple[int, int, int]
    font: pygame.font.Font
    rise_speed: float = 30  # Píxeles por segundo
    duration: float = 2.0
    fade_start: float = 1.0  # Cuándo empieza a desvanecer
    elapsed: float = 0.0
    scale: float = 1.0
    rotation: float = 0.0

    @property
    def is_complete(self) -> bool:
        return self.elapsed >= self.duration

    @property
    def alpha(self) -> int:
        """Calcula el alpha actual"""
        if self.elapsed < self.fade_start:
            return 255
        else:
            fade_progress = (self.elapsed - self.fade_start) / (self.duration - self.fade_start)
            return int(255 * (1 - fade_progress))

    def update(self, delta_time: float) -> None:
        """Actualiza la posición y estado"""
        self.elapsed += delta_time
        self.y -= self.rise_speed * delta_time

        # Opcional: añadir ligero movimiento horizontal
        self.x += math.sin(self.elapsed * 5) * 0.5

    def render(self, screen: pygame.Surface) -> None:
        """Renderiza el texto"""
        if self.is_complete:
            return

        # Renderizar texto
        text_surface = self.font.render(self.text, True, self.color)

        # Aplicar alpha
        alpha = self.alpha
        if alpha < 255:
            text_surface.set_alpha(alpha)

        # Aplicar escala si es diferente de 1
        if self.scale != 1.0:
            width = int(text_surface.get_width() * self.scale)
            height = int(text_surface.get_height() * self.scale)
            text_surface = pygame.transform.scale(text_surface, (width, height))

        # Aplicar rotación si hay
        if self.rotation != 0:
            text_surface = pygame.transform.rotate(text_surface, self.rotation)

        # Dibujar centrado en la posición
        rect = text_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text_surface, rect)


@dataclass
class ParticleAnimation:
    """Animación de partícula individual"""
    x: float
    y: float
    vx: float  # Velocidad X
    vy: float  # Velocidad Y
    size: float
    color: Tuple[int, int, int, int]
    lifetime: float
    elapsed: float = 0.0
    gravity: float = 0.0
    fade: bool = True
    shrink: bool = False

    @property
    def is_complete(self) -> bool:
        return self.elapsed >= self.lifetime

    @property
    def alpha(self) -> int:
        """Calcula el alpha actual"""
        if not self.fade:
            return self.color[3] if len(self.color) > 3 else 255

        progress = self.elapsed / self.lifetime
        base_alpha = self.color[3] if len(self.color) > 3 else 255
        return int(base_alpha * (1 - progress))

    @property
    def current_size(self) -> float:
        """Calcula el tamaño actual"""
        if not self.shrink:
            return self.size

        progress = self.elapsed / self.lifetime
        return self.size * (1 - progress * 0.8)  # Reduce hasta 20% del tamaño original

    def update(self, delta_time: float) -> bool:
        """Actualiza la partícula. Retorna True si debe eliminarse"""
        self.elapsed += delta_time

        if self.is_complete:
            return True

        # Aplicar física
        self.vy += self.gravity * delta_time
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time

        return False

    def render(self, screen: pygame.Surface) -> None:
        """Renderiza la partícula"""
        if self.is_complete:
            return

        alpha = self.alpha
        size = self.current_size

        if alpha > 0 and size > 0:
            # Crear superficie para la partícula
            particle_surface = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
            color = (*self.color[:3], alpha)
            pygame.draw.circle(particle_surface, color,
                             (int(size), int(size)), int(size))

            # Dibujar en pantalla
            screen.blit(particle_surface, (int(self.x - size), int(self.y - size)))


@dataclass
class ScreenFlash:
    """Efecto de flash de pantalla"""
    color: Tuple[int, int, int, int]
    duration: float
    elapsed: float = 0.0

    @property
    def is_complete(self) -> bool:
        return self.elapsed >= self.duration

    @property
    def alpha(self) -> int:
        """Calcula el alpha actual (fade out)"""
        progress = self.elapsed / self.duration
        base_alpha = self.color[3] if len(self.color) > 3 else 128
        return int(base_alpha * (1 - progress))

    def update(self, delta_time: float) -> None:
        """Actualiza el flash"""
        self.elapsed += delta_time

    def render(self, screen: pygame.Surface) -> None:
        """Renderiza el flash"""
        if self.is_complete:
            return

        flash_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        color = (*self.color[:3], self.alpha)
        flash_surface.fill(color)
        screen.blit(flash_surface, (0, 0))


class CameraController:
    """Controlador de cámara con efectos cinematográficos"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.rotation = 0.0
        self.shake_x = 0
        self.shake_y = 0

        # Tweens para movimientos suaves
        self.position_tween: Optional[Tuple[Tween, Tween]] = None
        self.zoom_tween: Optional[Tween] = None
        self.shake_tween: Optional[Tween] = None

    def pan_to(self, x: float, y: float, duration: float = 1.0,
               ease: EaseType = EaseType.EASE_IN_OUT) -> None:
        """Mueve la cámara suavemente a una posición"""
        self.position_tween = (
            Tween(self.x, x, duration, ease_type=ease),
            Tween(self.y, y, duration, ease_type=ease)
        )

    def zoom_to(self, zoom: float, duration: float = 0.5,
                ease: EaseType = EaseType.EASE_IN_OUT) -> None:
        """Hace zoom suavemente"""
        self.zoom_tween = Tween(self.zoom, zoom, duration, ease_type=ease)

    def shake(self, intensity: float = 10, duration: float = 0.3) -> None:
        """Sacude la cámara"""
        self.shake_tween = Tween(intensity, 0, duration, ease_type=EaseType.ELASTIC)

    def focus_on_action(self, x: float, y: float, zoom: float = 1.2,
                       duration: float = 0.3) -> None:
        """Enfoca en una acción con zoom"""
        self.pan_to(x - self.screen_width // 2, y - self.screen_height // 2, duration)
        self.zoom_to(zoom, duration)

    def update(self, delta_time: float) -> None:
        """Actualiza la cámara"""
        # Actualizar posición
        if self.position_tween:
            x_tween, y_tween = self.position_tween
            self.x = x_tween.update(delta_time)
            self.y = y_tween.update(delta_time)

            if x_tween.is_complete and y_tween.is_complete:
                self.position_tween = None

        # Actualizar zoom
        if self.zoom_tween:
            self.zoom = self.zoom_tween.update(delta_time)
            if self.zoom_tween.is_complete:
                self.zoom_tween = None

        # Actualizar shake
        if self.shake_tween:
            intensity = self.shake_tween.update(delta_time)
            if intensity > 0:
                import random
                self.shake_x = random.uniform(-intensity, intensity)
                self.shake_y = random.uniform(-intensity, intensity)
            else:
                self.shake_x = 0
                self.shake_y = 0

            if self.shake_tween.is_complete:
                self.shake_tween = None

    def apply_transform(self, surface: pygame.Surface) -> pygame.Surface:
        """Aplica las transformaciones de cámara a una superficie"""
        # Aplicar zoom
        if self.zoom != 1.0:
            width = int(surface.get_width() * self.zoom)
            height = int(surface.get_height() * self.zoom)
            surface = pygame.transform.scale(surface, (width, height))

        # Aplicar rotación
        if self.rotation != 0:
            surface = pygame.transform.rotate(surface, self.rotation)

        return surface

    def get_offset(self) -> Tuple[float, float]:
        """Obtiene el offset total de la cámara"""
        return (self.x + self.shake_x, self.y + self.shake_y)


# Singleton global para fácil acceso
animation_manager = AnimationManager()