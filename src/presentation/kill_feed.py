"""
Sistema de Kill Feed - Notificaciones de eliminaciones en tiempo real
"""

import pygame
from dataclasses import dataclass
from typing import List
from src.domain.value_objects import Bando


@dataclass
class KillEntry:
    """Entrada en el kill feed"""
    asesino_nombre: str
    victima_nombre: str
    asesino_bando: Bando
    victima_bando: Bando
    fue_critico: bool
    tiempo_restante: int  # milisegundos antes de desaparecer
    alpha: int = 255  # Transparencia (255 = opaco, 0 = transparente)


class KillFeed:
    """
    Sistema de Kill Feed estilo juegos FPS modernos
    Muestra últimas eliminaciones en la esquina superior derecha
    """

    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Configuración
        self.max_entries = 5  # Máximo de kills visibles
        self.entry_duration = 5000  # 5 segundos antes de fade out
        self.fade_duration = 1000  # 1 segundo de fade out
        self.entry_height = 30  # Altura de cada entrada
        self.entry_width = 250  # Ancho de cada entrada
        self.padding = 10  # Espacio entre entradas

        # Posición (esquina superior derecha)
        self.x = screen_width - self.entry_width - 20
        self.y = 60  # Debajo de la barra de interfaz

        # Entradas activas
        self.entries: List[KillEntry] = []

        # Fuentes
        try:
            self.font_normal = pygame.font.Font(None, 20)
            self.font_critico = pygame.font.Font(None, 22)
            self.font_critico.set_bold(True)
        except:
            self.font_normal = pygame.font.SysFont("arial", 20)
            self.font_critico = pygame.font.SysFont("arial", 22, bold=True)

        # Colores
        self.color_roma = (180, 20, 20)  # Rojo romano
        self.color_barbaros = (50, 100, 50)  # Verde bárbaro
        self.color_critico = (255, 215, 0)  # Dorado para críticos
        self.color_fondo = (0, 0, 0, 200)  # Fondo semi-transparente
        self.color_texto = (255, 255, 255)  # Blanco

    def agregar_kill(
        self,
        asesino_nombre: str,
        victima_nombre: str,
        asesino_bando: Bando,
        victima_bando: Bando,
        fue_critico: bool = False
    ):
        """Agrega una nueva kill al feed"""
        entry = KillEntry(
            asesino_nombre=asesino_nombre,
            victima_nombre=victima_nombre,
            asesino_bando=asesino_bando,
            victima_bando=victima_bando,
            fue_critico=fue_critico,
            tiempo_restante=self.entry_duration + self.fade_duration,
            alpha=255
        )

        self.entries.insert(0, entry)  # Añadir al principio

        # Limitar número de entradas
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[:self.max_entries]

    def update(self, dt: int):
        """Actualiza el kill feed (llamar cada frame)"""
        # Actualizar tiempos y alphas
        entries_to_remove = []

        for entry in self.entries:
            entry.tiempo_restante -= dt

            # Calcular alpha (fade out gradual)
            if entry.tiempo_restante <= self.fade_duration:
                # Fade out
                entry.alpha = int(255 * (entry.tiempo_restante / self.fade_duration))
                entry.alpha = max(0, entry.alpha)

            # Marcar para remover si ya expiró
            if entry.tiempo_restante <= 0:
                entries_to_remove.append(entry)

        # Remover entradas expiradas
        for entry in entries_to_remove:
            self.entries.remove(entry)

    def render(self, screen: pygame.Surface):
        """Renderiza el kill feed"""
        if not self.entries:
            return

        # Renderizar cada entrada
        for i, entry in enumerate(self.entries):
            y_pos = self.y + (i * (self.entry_height + self.padding))

            # Crear superficie con transparencia
            entry_surface = pygame.Surface((self.entry_width, self.entry_height), pygame.SRCALPHA)

            # Fondo semi-transparente con alpha variable
            bg_alpha = int(self.color_fondo[3] * (entry.alpha / 255))
            bg_color = (*self.color_fondo[:3], bg_alpha)
            pygame.draw.rect(
                entry_surface,
                bg_color,
                (0, 0, self.entry_width, self.entry_height),
                border_radius=5
            )

            # Borde (dorado si fue crítico, normal si no)
            if entry.fue_critico:
                border_color = (*self.color_critico, entry.alpha)
                border_width = 2
            else:
                border_color = (100, 100, 100, entry.alpha)
                border_width = 1

            pygame.draw.rect(
                entry_surface,
                border_color,
                (0, 0, self.entry_width, self.entry_height),
                width=border_width,
                border_radius=5
            )

            # Renderizar texto: "Asesino [X] Víctima"
            font = self.font_critico if entry.fue_critico else self.font_normal

            # Nombre del asesino (color según bando)
            color_asesino = (
                self.color_roma if entry.asesino_bando == Bando.ROMA
                else self.color_barbaros
            )
            asesino_surface = font.render(entry.asesino_nombre, True, color_asesino)
            asesino_surface.set_alpha(entry.alpha)

            # Icono de kill
            if entry.fue_critico:
                kill_icon = "⚡"  # Rayo para críticos
                icon_color = self.color_critico
            else:
                kill_icon = "⚔"  # Espadas cruzadas
                icon_color = self.color_texto

            icon_surface = font.render(kill_icon, True, icon_color)
            icon_surface.set_alpha(entry.alpha)

            # Nombre de la víctima (color según bando)
            color_victima = (
                self.color_roma if entry.victima_bando == Bando.ROMA
                else self.color_barbaros
            )
            victima_surface = font.render(entry.victima_nombre, True, color_victima)
            victima_surface.set_alpha(entry.alpha)

            # Calcular posiciones para centrar el texto
            spacing = 5
            total_width = (
                asesino_surface.get_width() +
                icon_surface.get_width() +
                victima_surface.get_width() +
                spacing * 2
            )
            start_x = (self.entry_width - total_width) // 2
            text_y = (self.entry_height - asesino_surface.get_height()) // 2

            # Blit texto en la superficie de entrada
            current_x = start_x
            entry_surface.blit(asesino_surface, (current_x, text_y))
            current_x += asesino_surface.get_width() + spacing

            entry_surface.blit(icon_surface, (current_x, text_y - 2))  # -2 para centrar mejor
            current_x += icon_surface.get_width() + spacing

            entry_surface.blit(victima_surface, (current_x, text_y))

            # Blit entrada completa en pantalla
            screen.blit(entry_surface, (self.x, y_pos))

    def clear(self):
        """Limpia todas las entradas del feed"""
        self.entries.clear()

    def tiene_entradas(self) -> bool:
        """Verifica si hay entradas activas"""
        return len(self.entries) > 0

    def contar_kills_consecutivos(self, bando: Bando) -> int:
        """Cuenta kills consecutivos recientes de un bando"""
        count = 0
        for entry in self.entries:
            if entry.asesino_bando == bando:
                count += 1
            else:
                break  # Rompe la racha
        return count


class KillNotification:
    """
    Notificación grande temporal para kills épicos
    Aparece en el centro de la pantalla por unos segundos
    """

    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.active = False
        self.message = ""
        self.tiempo_restante = 0
        self.duracion_total = 2000  # 2 segundos
        self.es_critico_devastador = False

        # Fuentes
        try:
            self.font_titulo = pygame.font.Font(None, 60)
            self.font_titulo.set_bold(True)
            self.font_subtitulo = pygame.font.Font(None, 30)
        except:
            self.font_titulo = pygame.font.SysFont("arial", 60, bold=True)
            self.font_subtitulo = pygame.font.SysFont("arial", 30)

        # Colores
        self.color_critico = (255, 215, 0)  # Dorado
        self.color_devastador = (255, 50, 50)  # Rojo brillante
        self.color_sombra = (0, 0, 0)

    def mostrar(self, mensaje: str, es_devastador: bool = False):
        """Muestra una notificación épica"""
        self.active = True
        self.message = mensaje
        self.tiempo_restante = self.duracion_total
        self.es_critico_devastador = es_devastador

    def update(self, dt: int):
        """Actualiza la notificación"""
        if self.active:
            self.tiempo_restante -= dt
            if self.tiempo_restante <= 0:
                self.active = False

    def render(self, screen: pygame.Surface):
        """Renderiza la notificación"""
        if not self.active:
            return

        # Calcular alpha basado en tiempo restante
        if self.tiempo_restante < 500:  # Último medio segundo: fade out
            alpha = int(255 * (self.tiempo_restante / 500))
        else:
            alpha = 255

        # Calcular escala (animación de entrada)
        tiempo_transcurrido = self.duracion_total - self.tiempo_restante
        if tiempo_transcurrido < 300:  # Primeros 300ms: pop in
            scale = 0.5 + (tiempo_transcurrido / 300) * 0.5
        else:
            scale = 1.0

        # Color según tipo
        color = self.color_devastador if self.es_critico_devastador else self.color_critico

        # Renderizar texto con sombra
        font = self.font_titulo

        # Aplicar escala al font size (recrear font con nuevo tamaño)
        scaled_size = int(60 * scale)
        try:
            font_scaled = pygame.font.Font(None, scaled_size)
            font_scaled.set_bold(True)
        except:
            font_scaled = pygame.font.SysFont("arial", scaled_size, bold=True)

        # Renderizar sombra
        text_shadow = font_scaled.render(self.message, True, self.color_sombra)
        text_shadow.set_alpha(alpha)

        # Renderizar texto principal
        text_surface = font_scaled.render(self.message, True, color)
        text_surface.set_alpha(alpha)

        # Posición centrada
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4

        # Blit
        screen.blit(text_shadow, shadow_rect)
        screen.blit(text_surface, text_rect)

        # Si es devastador, agregar subtítulo
        if self.es_critico_devastador:
            subtitulo = "¡DEVASTADOR!"
            sub_surface = self.font_subtitulo.render(subtitulo, True, color)
            sub_surface.set_alpha(alpha)
            sub_rect = sub_surface.get_rect(
                center=(self.screen_width // 2, self.screen_height // 2 + 10)
            )
            screen.blit(sub_surface, sub_rect)
