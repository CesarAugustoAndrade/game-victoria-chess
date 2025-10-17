"""
Sistema de UI Moderno con Efectos y Tooltips
"""

import pygame
import math
import random
from typing import Optional, Tuple, List, Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum
from src.presentation.animation_system import Tween, EaseType


class TooltipPosition(Enum):
    """Posiciones posibles para tooltips"""
    AUTO = "auto"
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"


class ButtonState(Enum):
    """Estados de un botón"""
    NORMAL = "normal"
    HOVER = "hover"
    PRESSED = "pressed"
    DISABLED = "disabled"


@dataclass
class TooltipData:
    """Datos para un tooltip"""
    title: str
    description: str = ""
    stats: Dict[str, Any] = None
    icon: Optional[pygame.Surface] = None
    color_scheme: Tuple[int, int, int] = (50, 50, 50)
    position: TooltipPosition = TooltipPosition.AUTO


class ModernTooltip:
    """Sistema de tooltips flotantes con animaciones"""

    def __init__(self, font_title: pygame.font.Font = None,
                 font_text: pygame.font.Font = None):
        # Fonts
        if not font_title:
            font_title = pygame.font.Font(None, 20)
        if not font_text:
            font_text = pygame.font.Font(None, 16)

        self.font_title = font_title
        self.font_text = font_text

        # Estado
        self.visible = False
        self.data: Optional[TooltipData] = None
        self.position = (0, 0)
        self.target_position = (0, 0)

        # Animación
        self.alpha = 0
        self.scale = 0.8
        self.fade_tween = None

        # Cache de superficie renderizada
        self.surface: Optional[pygame.Surface] = None
        self.max_width = 300
        self.padding = 10
        self.line_spacing = 5

    def show(self, data: TooltipData, position: Tuple[int, int]):
        """Muestra el tooltip con animación"""
        self.data = data
        self.target_position = position
        self.visible = True

        # Crear superficie del tooltip
        self._create_surface()

        # Animación de entrada
        self.fade_tween = Tween(0, 255, 0.2, ease_type=EaseType.EASE_OUT)
        self.scale_tween = Tween(0.8, 1.0, 0.2, ease_type=EaseType.BACK)

    def hide(self):
        """Oculta el tooltip con animación"""
        if self.visible:
            self.fade_tween = Tween(self.alpha, 0, 0.15, ease_type=EaseType.EASE_IN,
                                   on_complete=self._on_hide_complete)

    def _on_hide_complete(self):
        """Callback cuando termina de ocultarse"""
        self.visible = False
        self.data = None
        self.surface = None

    def _create_surface(self):
        """Crea la superficie del tooltip"""
        if not self.data:
            return

        # Calcular dimensiones
        lines = []
        max_width = 0

        # Título
        title_surface = self.font_title.render(self.data.title, True, (255, 255, 255))
        lines.append(title_surface)
        max_width = max(max_width, title_surface.get_width())

        # Descripción
        if self.data.description:
            # Word wrap para descripción larga
            words = self.data.description.split(' ')
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                test_surface = self.font_text.render(test_line, True, (200, 200, 200))

                if test_surface.get_width() > self.max_width - 2 * self.padding:
                    if current_line:
                        line_surface = self.font_text.render(current_line, True, (200, 200, 200))
                        lines.append(line_surface)
                        max_width = max(max_width, line_surface.get_width())
                    current_line = word + " "
                else:
                    current_line = test_line

            if current_line:
                line_surface = self.font_text.render(current_line, True, (200, 200, 200))
                lines.append(line_surface)
                max_width = max(max_width, line_surface.get_width())

        # Stats
        if self.data.stats:
            lines.append(None)  # Separador
            for key, value in self.data.stats.items():
                stat_text = f"{key}: {value}"
                stat_surface = self.font_text.render(stat_text, True, (150, 200, 255))
                lines.append(stat_surface)
                max_width = max(max_width, stat_surface.get_width())

        # Calcular tamaño total
        height = sum(line.get_height() if line else self.line_spacing
                    for line in lines) + 2 * self.padding
        width = max_width + 2 * self.padding

        # Crear superficie con alpha
        self.surface = pygame.Surface((width + 10, height + 10), pygame.SRCALPHA)

        # Sombra
        shadow_rect = pygame.Rect(5, 5, width, height)
        pygame.draw.rect(self.surface, (0, 0, 0, 100), shadow_rect, border_radius=8)

        # Fondo principal con gradiente
        main_rect = pygame.Rect(0, 0, width, height)
        self._draw_gradient_rect(self.surface, main_rect, self.data.color_scheme)

        # Borde
        pygame.draw.rect(self.surface, (100, 100, 100), main_rect, 2, border_radius=8)

        # Dibujar contenido
        y_offset = self.padding
        for i, line in enumerate(lines):
            if line is None:
                y_offset += self.line_spacing
            else:
                x_offset = self.padding

                # Título centrado, resto alineado a la izquierda
                if i == 0:
                    x_offset = (width - line.get_width()) // 2

                self.surface.blit(line, (x_offset, y_offset))
                y_offset += line.get_height() + self.line_spacing

    def _draw_gradient_rect(self, surface: pygame.Surface, rect: pygame.Rect,
                           base_color: Tuple[int, int, int]):
        """Dibuja un rectángulo con gradiente"""
        # Color más claro arriba, más oscuro abajo
        for y in range(rect.height):
            progress = y / rect.height
            color = tuple(int(c * (1 + 0.3 * (1 - progress))) for c in base_color)
            color = tuple(min(255, c) for c in color)

            pygame.draw.line(surface, color + (200,),
                           (rect.x, rect.y + y),
                           (rect.x + rect.width, rect.y + y))

        # Aplicar border radius manualmente con máscara
        mask_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(mask_surface, (255, 255, 255, 255), (0, 0, rect.width, rect.height),
                        border_radius=8)
        surface.blit(mask_surface, (rect.x, rect.y), special_flags=pygame.BLEND_RGBA_MIN)

    def update(self, delta_time: float):
        """Actualiza las animaciones del tooltip"""
        if self.fade_tween:
            self.alpha = self.fade_tween.update(delta_time)
            if self.fade_tween.is_complete:
                self.fade_tween = None

        if hasattr(self, 'scale_tween') and self.scale_tween:
            self.scale = self.scale_tween.update(delta_time)
            if self.scale_tween.is_complete:
                self.scale_tween = None

        # Suavizar movimiento
        if self.position != self.target_position:
            self.position = (
                self.position[0] + (self.target_position[0] - self.position[0]) * 10 * delta_time,
                self.position[1] + (self.target_position[1] - self.position[1]) * 10 * delta_time
            )

    def render(self, screen: pygame.Surface):
        """Renderiza el tooltip"""
        if not self.visible or not self.surface or self.alpha <= 0:
            return

        # Aplicar escala si es diferente de 1
        if self.scale != 1.0:
            width = int(self.surface.get_width() * self.scale)
            height = int(self.surface.get_height() * self.scale)
            scaled_surface = pygame.transform.scale(self.surface, (width, height))
        else:
            scaled_surface = self.surface

        # Aplicar alpha
        scaled_surface.set_alpha(int(self.alpha))

        # Calcular posición (evitar que salga de pantalla)
        x, y = self.position
        screen_width, screen_height = screen.get_size()

        if x + scaled_surface.get_width() > screen_width:
            x = screen_width - scaled_surface.get_width() - 10
        if y + scaled_surface.get_height() > screen_height:
            y = screen_height - scaled_surface.get_height() - 10
        if x < 10:
            x = 10
        if y < 10:
            y = 10

        screen.blit(scaled_surface, (x, y))


class ModernButton:
    """Botón moderno con efectos y animaciones"""

    def __init__(self, x: int, y: int, width: int, height: int,
                 text: str = "", icon: Optional[pygame.Surface] = None,
                 callback: Optional[Callable] = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon = icon
        self.callback = callback

        # Estado
        self.state = ButtonState.NORMAL
        self.enabled = True

        # Colores
        self.colors = {
            ButtonState.NORMAL: (60, 60, 80),
            ButtonState.HOVER: (80, 80, 100),
            ButtonState.PRESSED: (40, 40, 60),
            ButtonState.DISABLED: (30, 30, 40)
        }

        self.text_colors = {
            ButtonState.NORMAL: (255, 255, 255),
            ButtonState.HOVER: (255, 255, 200),
            ButtonState.PRESSED: (200, 200, 200),
            ButtonState.DISABLED: (100, 100, 100)
        }

        # Animaciones
        self.scale = 1.0
        self.rotation = 0.0
        self.glow_alpha = 0
        self.ripple_effects = []

        # Font
        self.font = pygame.font.Font(None, 24)

        # Tooltip
        self.tooltip_data: Optional[TooltipData] = None

    def set_tooltip(self, tooltip: TooltipData):
        """Establece el tooltip del botón"""
        self.tooltip_data = tooltip

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Maneja eventos del botón"""
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                if self.state != ButtonState.PRESSED:
                    self.state = ButtonState.HOVER
                    self.on_hover()
                return True
            else:
                if self.state == ButtonState.HOVER:
                    self.state = ButtonState.NORMAL
                    self.on_leave()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.state = ButtonState.PRESSED
                self.on_press()
                return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.state == ButtonState.PRESSED:
                    self.state = ButtonState.HOVER
                    self.on_release()
                    if self.callback:
                        self.callback()
                    return True

        return False

    def on_hover(self):
        """Efecto al pasar el mouse"""
        # Animación de scale
        self.scale_tween = Tween(self.scale, 1.05, 0.2, ease_type=EaseType.EASE_OUT)
        self.glow_alpha = 100

    def on_leave(self):
        """Efecto al salir el mouse"""
        self.scale_tween = Tween(self.scale, 1.0, 0.2, ease_type=EaseType.EASE_OUT)
        self.glow_alpha = 0

    def on_press(self):
        """Efecto al presionar"""
        self.scale_tween = Tween(self.scale, 0.95, 0.1, ease_type=EaseType.EASE_IN)
        self.add_ripple_effect()

    def on_release(self):
        """Efecto al soltar"""
        self.scale_tween = Tween(self.scale, 1.05, 0.1, ease_type=EaseType.BOUNCE)

    def add_ripple_effect(self):
        """Añade efecto de ripple al hacer click"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        ripple = {
            'x': mouse_x - self.rect.x,
            'y': mouse_y - self.rect.y,
            'radius': 0,
            'max_radius': max(self.rect.width, self.rect.height),
            'alpha': 150,
            'color': (255, 255, 255)
        }
        self.ripple_effects.append(ripple)

    def update(self, delta_time: float):
        """Actualiza animaciones del botón"""
        # Actualizar scale
        if hasattr(self, 'scale_tween') and self.scale_tween:
            self.scale = self.scale_tween.update(delta_time)
            if self.scale_tween.is_complete:
                self.scale_tween = None

        # Actualizar ripples
        for ripple in self.ripple_effects[:]:
            ripple['radius'] += 200 * delta_time
            ripple['alpha'] = max(0, ripple['alpha'] - 300 * delta_time)

            if ripple['radius'] >= ripple['max_radius'] or ripple['alpha'] <= 0:
                self.ripple_effects.remove(ripple)

        # Pulso de glow en hover
        if self.state == ButtonState.HOVER:
            self.glow_alpha = 50 + 50 * abs(math.sin(pygame.time.get_ticks() * 0.003))

    def render(self, screen: pygame.Surface):
        """Renderiza el botón con efectos"""
        # Calcular rectángulo con escala
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        scaled_x = self.rect.x + (self.rect.width - scaled_width) // 2
        scaled_y = self.rect.y + (self.rect.height - scaled_height) // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)

        # Glow effect
        if self.glow_alpha > 0:
            glow_surface = pygame.Surface((scaled_width + 20, scaled_height + 20), pygame.SRCALPHA)
            glow_rect = pygame.Rect(10, 10, scaled_width, scaled_height)

            for i in range(10):
                alpha = int(self.glow_alpha * (1 - i / 10))
                expanded_rect = glow_rect.inflate(i * 2, i * 2)
                pygame.draw.rect(glow_surface, (*self.colors[self.state], alpha),
                               expanded_rect, border_radius=10)

            screen.blit(glow_surface, (scaled_x - 10, scaled_y - 10))

        # Sombra
        shadow_rect = scaled_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=8)

        # Fondo del botón con gradiente
        button_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)

        # Gradiente
        color = self.colors[self.state if self.enabled else ButtonState.DISABLED]
        for y in range(scaled_height):
            progress = y / scaled_height
            gradient_color = tuple(int(c * (1 + 0.3 * (1 - progress))) for c in color)
            gradient_color = tuple(min(255, c) for c in gradient_color) + (255,)
            pygame.draw.line(button_surface, gradient_color,
                           (0, y), (scaled_width, y))

        # Aplicar border radius
        mask_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        pygame.draw.rect(mask_surface, (255, 255, 255, 255),
                        (0, 0, scaled_width, scaled_height), border_radius=8)
        button_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        screen.blit(button_surface, scaled_rect)

        # Ripple effects
        for ripple in self.ripple_effects:
            if ripple['alpha'] > 0:
                ripple_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
                pygame.draw.circle(ripple_surface, (*ripple['color'], int(ripple['alpha'])),
                                 (ripple['x'], ripple['y']), int(ripple['radius']), 2)
                screen.blit(ripple_surface, scaled_rect)

        # Borde
        border_color = (150, 150, 150) if self.enabled else (50, 50, 50)
        pygame.draw.rect(screen, border_color, scaled_rect, 2, border_radius=8)

        # Icono y texto
        content_x = scaled_rect.centerx
        content_y = scaled_rect.centery

        if self.icon:
            icon_rect = self.icon.get_rect(center=(content_x, content_y - 10))
            screen.blit(self.icon, icon_rect)
            content_y += self.icon.get_height() // 2 + 5

        if self.text:
            text_color = self.text_colors[self.state if self.enabled else ButtonState.DISABLED]
            text_surface = self.font.render(self.text, True, text_color)
            text_rect = text_surface.get_rect(center=(content_x, content_y))
            screen.blit(text_surface, text_rect)


class NotificationSystem:
    """Sistema de notificaciones flotantes"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.notifications: List[Dict] = []
        self.font = pygame.font.Font(None, 20)
        self.max_notifications = 5

    def add_notification(self, text: str, color: Tuple[int, int, int] = (255, 255, 255),
                        duration: float = 3.0, icon: Optional[pygame.Surface] = None):
        """Añade una nueva notificación"""
        notification = {
            'text': text,
            'color': color,
            'icon': icon,
            'duration': duration,
            'elapsed': 0.0,
            'y': self.screen_height,  # Empieza fuera de pantalla
            'alpha': 0,
            'state': 'entering'  # entering, showing, exiting
        }

        self.notifications.append(notification)

        # Limitar número de notificaciones
        if len(self.notifications) > self.max_notifications:
            # Marcar la más antigua para salir
            self.notifications[0]['state'] = 'exiting'

    def update(self, delta_time: float):
        """Actualiza las notificaciones"""
        for i, notif in enumerate(self.notifications[:]):
            notif['elapsed'] += delta_time

            # Calcular posición objetivo
            target_y = 100 + i * 60

            # Estados de animación
            if notif['state'] == 'entering':
                notif['alpha'] = min(255, notif['alpha'] + 1000 * delta_time)
                notif['y'] += (target_y - notif['y']) * 10 * delta_time

                if notif['alpha'] >= 255:
                    notif['state'] = 'showing'

            elif notif['state'] == 'showing':
                notif['y'] += (target_y - notif['y']) * 10 * delta_time

                if notif['elapsed'] >= notif['duration']:
                    notif['state'] = 'exiting'

            elif notif['state'] == 'exiting':
                notif['alpha'] = max(0, notif['alpha'] - 500 * delta_time)
                notif['y'] -= 50 * delta_time

                if notif['alpha'] <= 0:
                    self.notifications.remove(notif)

    def render(self, screen: pygame.Surface):
        """Renderiza las notificaciones"""
        for notif in self.notifications:
            if notif['alpha'] <= 0:
                continue

            # Crear superficie de notificación
            text_surface = self.font.render(notif['text'], True, notif['color'])
            width = text_surface.get_width() + 40
            height = 40

            # Posición centrada horizontalmente
            x = (self.screen_width - width) // 2
            y = int(notif['y'])

            # Fondo con alpha
            notif_surface = pygame.Surface((width, height), pygame.SRCALPHA)

            # Fondo semi-transparente
            bg_alpha = int(notif['alpha'] * 0.8 / 255)
            pygame.draw.rect(notif_surface, (30, 30, 30, bg_alpha * 255),
                           (0, 0, width, height), border_radius=20)

            # Borde
            if notif['alpha'] > 100:
                pygame.draw.rect(notif_surface, (*notif['color'], int(notif['alpha'])),
                               (0, 0, width, height), 2, border_radius=20)

            # Texto
            text_surface.set_alpha(int(notif['alpha']))
            text_rect = text_surface.get_rect(center=(width // 2, height // 2))
            notif_surface.blit(text_surface, text_rect)

            screen.blit(notif_surface, (x, y))


class DamageNumberSystem:
    """Sistema de números de daño flotantes"""

    def __init__(self):
        self.numbers: List[Dict] = []
        self.font_small = pygame.font.Font(None, 24)
        self.font_normal = pygame.font.Font(None, 32)
        self.font_critical = pygame.font.Font(None, 48)

    def add_damage_number(self, x: int, y: int, damage: int, is_critical: bool = False,
                         is_heal: bool = False):
        """Añade un número de daño flotante"""
        if is_critical:
            font = self.font_critical
            color = (255, 50, 50)
            scale_max = 1.5
        elif is_heal:
            font = self.font_normal
            color = (50, 255, 50)
            scale_max = 1.2
        else:
            font = self.font_normal
            color = (255, 200, 50)
            scale_max = 1.0

        number = {
            'x': x + random.randint(-10, 10),
            'y': y,
            'damage': damage,
            'font': font,
            'color': color,
            'elapsed': 0.0,
            'duration': 1.5,
            'velocity_y': -100,
            'velocity_x': random.randint(-30, 30),
            'scale': 0.5,
            'scale_max': scale_max,
            'rotation': random.randint(-15, 15) if is_critical else 0
        }

        self.numbers.append(number)

    def update(self, delta_time: float):
        """Actualiza los números de daño"""
        for number in self.numbers[:]:
            number['elapsed'] += delta_time

            # Movimiento
            number['y'] += number['velocity_y'] * delta_time
            number['x'] += number['velocity_x'] * delta_time

            # Gravedad
            number['velocity_y'] += 200 * delta_time

            # Escala (bounce in)
            if number['elapsed'] < 0.2:
                progress = number['elapsed'] / 0.2
                number['scale'] = 0.5 + (number['scale_max'] - 0.5) * progress
            elif number['elapsed'] < 0.4:
                progress = (number['elapsed'] - 0.2) / 0.2
                number['scale'] = number['scale_max'] - (number['scale_max'] - 1.0) * progress

            # Fade out
            if number['elapsed'] > number['duration'] * 0.7:
                fade_progress = (number['elapsed'] - number['duration'] * 0.7) / (number['duration'] * 0.3)
                number['alpha'] = int(255 * (1 - fade_progress))
            else:
                number['alpha'] = 255

            # Eliminar si terminó
            if number['elapsed'] >= number['duration']:
                self.numbers.remove(number)

    def render(self, screen: pygame.Surface):
        """Renderiza los números de daño"""
        for number in self.numbers:
            if number['alpha'] <= 0:
                continue

            # Renderizar texto
            text = str(number['damage'])
            if number['damage'] > 0:
                text = f"-{text}"

            text_surface = number['font'].render(text, True, number['color'])

            # Aplicar escala
            if number['scale'] != 1.0:
                width = int(text_surface.get_width() * number['scale'])
                height = int(text_surface.get_height() * number['scale'])
                text_surface = pygame.transform.scale(text_surface, (width, height))

            # Aplicar rotación
            if number['rotation'] != 0:
                text_surface = pygame.transform.rotate(text_surface, number['rotation'])

            # Aplicar alpha
            text_surface.set_alpha(number['alpha'])

            # Borde negro para mejor visibilidad
            outline_surface = number['font'].render(text, True, (0, 0, 0))
            if number['scale'] != 1.0:
                width = int(outline_surface.get_width() * number['scale'])
                height = int(outline_surface.get_height() * number['scale'])
                outline_surface = pygame.transform.scale(outline_surface, (width, height))

            outline_surface.set_alpha(number['alpha'] // 2)

            # Dibujar
            rect = text_surface.get_rect(center=(int(number['x']), int(number['y'])))

            # Sombra/outline
            for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                screen.blit(outline_surface, (rect.x + dx, rect.y + dy))

            # Texto principal
            screen.blit(text_surface, rect)