"""
Renderizador de batalla táctica para pygame
"""

import pygame
import math
from typing import Optional, List, Tuple
from src.domain.batalla import Batalla
from src.domain.value_objects import Posicion, Bando, TipoUnidad
from src.domain.entities import Unidad
from src.presentation.unit_sprites import UnitSpriteRenderer


class BattleRenderer:
    """Renderiza la batalla táctica en el tablero"""

    def __init__(self, screen_width: int = 1280, screen_height: int = 720):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Configuración del tablero
        self.board_width = 7
        self.board_height = 9
        self.tile_size = 70
        self.board_offset_x = (screen_width - (self.board_width * self.tile_size)) // 2
        self.board_offset_y = 100

        # Colores
        self.TILE_LIGHT = (240, 217, 181)
        self.TILE_DARK = (181, 136, 99)
        self.TILE_HIGHLIGHT = (255, 255, 150)
        self.TILE_VALID_MOVE = (150, 255, 150)
        self.TILE_ATTACKABLE = (255, 150, 150)
        self.BORDER_COLOR = (100, 60, 20)

        # Fuentes
        pygame.font.init()
        self.font_unit = pygame.font.Font(None, 36)
        self.font_stats = pygame.font.Font(None, 20)
        self.font_title = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 16)

        # Estado de renderizado
        self.selected_unit_id = None
        self.movimientos_validos = []
        self.objetivos_atacables = []
        self.animaciones = []

        # Sistema de sprites
        self.sprite_renderer = UnitSpriteRenderer()

    def render(self, screen: pygame.Surface, batalla: Optional[Batalla]):
        """Renderiza la batalla completa"""
        if not batalla:
            self._render_no_battle(screen)
            return

        # Fondo
        self._render_background(screen)

        # Tablero
        self._render_board(screen)

        # Casillas especiales (movimientos válidos, objetivos)
        self._render_special_tiles(screen, batalla)

        # Unidades
        self._render_units(screen, batalla)

        # UI
        self._render_ui(screen, batalla)

        # Animaciones
        self._render_animations(screen)

    def _render_background(self, screen: pygame.Surface):
        """Renderiza el fondo"""
        # Fondo tipo pergamino
        screen.fill((230, 210, 180))

        # Bordes decorativos
        pygame.draw.rect(screen, (150, 100, 50), (0, 0, self.screen_width, 50))
        pygame.draw.rect(screen, (150, 100, 50), (0, self.screen_height - 50, self.screen_width, 50))

    def _render_board(self, screen: pygame.Surface):
        """Renderiza el tablero de juego"""
        # Borde del tablero
        border_rect = pygame.Rect(
            self.board_offset_x - 5,
            self.board_offset_y - 5,
            self.board_width * self.tile_size + 10,
            self.board_height * self.tile_size + 10
        )
        pygame.draw.rect(screen, self.BORDER_COLOR, border_rect, 3)

        # Casillas del tablero
        for row in range(self.board_height):
            for col in range(self.board_width):
                x = self.board_offset_x + col * self.tile_size
                y = self.board_offset_y + row * self.tile_size

                # Color alternado
                color = self.TILE_LIGHT if (row + col) % 2 == 0 else self.TILE_DARK

                pygame.draw.rect(screen, color, (x, y, self.tile_size, self.tile_size))
                pygame.draw.rect(screen, self.BORDER_COLOR, (x, y, self.tile_size, self.tile_size), 1)

                # Coordenadas para debug
                if row == 0:
                    coord_text = self.font_stats.render(str(col), True, (80, 60, 40))
                    screen.blit(coord_text, (x + 5, y - 20))
                if col == 0:
                    coord_text = self.font_stats.render(str(row), True, (80, 60, 40))
                    screen.blit(coord_text, (x - 20, y + 5))

    def _render_special_tiles(self, screen: pygame.Surface, batalla: Batalla):
        """Renderiza casillas especiales (movimientos, ataques)"""
        # Movimientos válidos
        for posicion in self.movimientos_validos:
            self._render_tile_overlay(screen, posicion, self.TILE_VALID_MOVE, 100)

        # Objetivos atacables
        for unidad in self.objetivos_atacables:
            self._render_tile_overlay(screen, unidad.posicion, self.TILE_ATTACKABLE, 120)

        # Unidad seleccionada
        if batalla.unidad_seleccionada:
            self._render_tile_overlay(
                screen,
                batalla.unidad_seleccionada.posicion,
                self.TILE_HIGHLIGHT,
                150
            )

    def _render_tile_overlay(self, screen: pygame.Surface, posicion: Posicion, color: tuple, alpha: int):
        """Renderiza un overlay sobre una casilla"""
        x = self.board_offset_x + posicion.columna * self.tile_size
        y = self.board_offset_y + posicion.fila * self.tile_size

        overlay = pygame.Surface((self.tile_size, self.tile_size))
        overlay.set_alpha(alpha)
        overlay.fill(color)
        screen.blit(overlay, (x, y))

    def _render_units(self, screen: pygame.Surface, batalla: Batalla):
        """Renderiza todas las unidades"""
        # Renderizar primero las unidades enemigas
        for unidad in batalla.ejercito_enemigo.unidades_vivas:
            self._render_unit(screen, unidad)

        # Luego las unidades del jugador
        for unidad in batalla.ejercito_jugador.unidades_vivas:
            self._render_unit(screen, unidad)

    def _render_unit(self, screen: pygame.Surface, unidad: Unidad):
        """Renderiza una unidad individual con sprite personalizado"""
        x = self.board_offset_x + unidad.posicion.columna * self.tile_size
        y = self.board_offset_y + unidad.posicion.fila * self.tile_size

        # Obtener sprite de la unidad
        sprite = self.sprite_renderer.get_unit_sprite(
            unidad.tipo,
            unidad.bando,
            size=self.tile_size - 10  # Un poco más pequeño que la casilla
        )

        # Posicionar sprite centrado en la casilla
        sprite_x = x + (self.tile_size - sprite.get_width()) // 2
        sprite_y = y + (self.tile_size - sprite.get_height()) // 2
        screen.blit(sprite, (sprite_x, sprite_y))

        # Indicadores de estado
        self._render_unit_status_indicators(screen, unidad, x, y)

        # Barra de vida
        self._render_health_bar(screen, unidad, x, y)

        # Barra de moral (si está por debajo del 100%)
        if unidad.moral_actual < 100:
            self._render_morale_bar(screen, unidad, x, y)

    def _render_unit_status_indicators(self, screen: pygame.Surface, unidad: Unidad, x: int, y: int):
        """Renderiza indicadores de estado de la unidad"""
        # Indicador de acción disponible (solo para romanos)
        if unidad.bando == Bando.ROMA:
            indicator_x = x + 3
            indicator_y = y + 3

            if unidad.puede_actuar:
                # Punto verde - puede actuar completamente
                pygame.draw.circle(screen, (0, 255, 0), (indicator_x, indicator_y), 4)
                pygame.draw.circle(screen, (0, 150, 0), (indicator_x, indicator_y), 4, 1)
            elif unidad.puede_moverse:
                # Punto amarillo - solo puede moverse
                pygame.draw.circle(screen, (255, 255, 0), (indicator_x, indicator_y), 4)
                pygame.draw.circle(screen, (150, 150, 0), (indicator_x, indicator_y), 4, 1)
            else:
                # Punto gris - ya actuó
                pygame.draw.circle(screen, (100, 100, 100), (indicator_x, indicator_y), 3)

        # Indicador de pánico
        if unidad.esta_en_panico:
            panic_x = x + self.tile_size - 15
            panic_y = y + 5

            # Símbolo de pánico (!)
            panic_surface = self.font_stats.render("!", True, (255, 0, 0))
            screen.blit(panic_surface, (panic_x, panic_y))

            # Animación de temblor (efecto visual)
            import random
            if random.random() > 0.5:
                offset = random.randint(-1, 1)
                panic_surface = self.font_stats.render("!", True, (200, 0, 0))
                screen.blit(panic_surface, (panic_x + offset, panic_y))

    def _render_health_bar(self, screen: pygame.Surface, unidad: Unidad, x: int, y: int):
        """Renderiza la barra de vida de una unidad"""
        bar_width = self.tile_size - 14
        bar_height = 4
        bar_x = x + 7
        bar_y = y + self.tile_size - 12

        # Fondo de la barra
        pygame.draw.rect(screen, (40, 40, 40), (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2))
        pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))

        # Vida actual
        health_percentage = unidad.porcentaje_vida
        current_width = int(bar_width * health_percentage)

        # Color según vida
        if health_percentage > 0.6:
            health_color = (0, 200, 0)
        elif health_percentage > 0.3:
            health_color = (255, 200, 0)
        else:
            health_color = (255, 0, 0)

        if current_width > 0:
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, current_width, bar_height))

        # Texto de vida (opcional, para unidades seleccionadas)
        if unidad.bando == Bando.ROMA and health_percentage < 1.0:
            health_text = f"{unidad.vida_actual}/{unidad.estadisticas.vida_maxima}"
            text_surface = self.font_small.render(health_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(centerx=x + self.tile_size // 2, y=bar_y - 15)
            screen.blit(text_surface, text_rect)

    def _render_morale_bar(self, screen: pygame.Surface, unidad: Unidad, x: int, y: int):
        """Renderiza la barra de moral de una unidad"""
        bar_width = self.tile_size - 14
        bar_height = 3
        bar_x = x + 7
        bar_y = y + self.tile_size - 6

        # Solo mostrar si la moral no está al máximo
        morale_percentage = unidad.moral_actual / 100.0

        # Fondo de la barra
        pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height))

        # Moral actual
        current_width = int(bar_width * morale_percentage)

        # Color según moral
        if morale_percentage > 0.7:
            morale_color = (100, 100, 255)  # Azul - buena moral
        elif morale_percentage > 0.3:
            morale_color = (255, 255, 100)  # Amarillo - moral media
        else:
            morale_color = (200, 100, 100)  # Rojo oscuro - moral baja

        if current_width > 0:
            pygame.draw.rect(screen, morale_color, (bar_x, bar_y, current_width, bar_height))

    def _render_ui(self, screen: pygame.Surface, batalla: Batalla):
        """Renderiza la interfaz de usuario"""
        # Título
        title = "LEGIO ROMANA - BATALLA TÁCTICA"
        title_text = self.font_title.render(title, True, (139, 69, 19))
        title_rect = title_text.get_rect(centerx=self.screen_width // 2, y=20)
        screen.blit(title_text, title_rect)

        # Información de turno
        turno_text = f"Ronda {batalla.ronda_actual} - Turno: {'ROMA' if batalla.turno_actual.value == 'player' else 'BÁRBAROS'}"
        turno_surface = self.font_stats.render(turno_text, True, (80, 60, 40))
        screen.blit(turno_surface, (20, 70))

        # Estado del ejército
        self._render_army_status(screen, batalla)

        # Unidad seleccionada
        if batalla.unidad_seleccionada:
            self._render_unit_info(screen, batalla.unidad_seleccionada)

        # Controles
        self._render_controls(screen)

    def _render_army_status(self, screen: pygame.Surface, batalla: Batalla):
        """Renderiza el estado de los ejércitos"""
        # Ejército Romano
        roma_text = f"ROMA: {len(batalla.ejercito_jugador.unidades_vivas)} unidades | Moral: {batalla.ejercito_jugador.moral_promedio:.0f}%"
        roma_surface = self.font_stats.render(roma_text, True, (180, 20, 20))
        screen.blit(roma_surface, (20, 100))

        # Ejército Bárbaro
        barbaro_text = f"BÁRBAROS: {len(batalla.ejercito_enemigo.unidades_vivas)} unidades | Moral: {batalla.ejercito_enemigo.moral_promedio:.0f}%"
        barbaro_surface = self.font_stats.render(barbaro_text, True, (50, 100, 50))
        screen.blit(barbaro_surface, (20, 125))

    def _render_unit_info(self, screen: pygame.Surface, unidad: Unidad):
        """Renderiza información de la unidad seleccionada"""
        info_x = self.screen_width - 250
        info_y = 100

        # Fondo
        info_rect = pygame.Rect(info_x - 10, info_y - 10, 240, 200)
        pygame.draw.rect(screen, (200, 180, 150), info_rect)
        pygame.draw.rect(screen, self.BORDER_COLOR, info_rect, 2)

        # Nombre
        name_text = self.font_stats.render(unidad.visualizacion.nombre, True, (60, 40, 20))
        screen.blit(name_text, (info_x, info_y))

        # Nombre latino
        latin_text = self.font_stats.render(f"({unidad.visualizacion.nombre_latino})", True, (80, 60, 40))
        screen.blit(latin_text, (info_x, info_y + 25))

        # Estadísticas
        stats = [
            f"Vida: {unidad.vida_actual}/{unidad.estadisticas.vida_maxima}",
            f"Ataque: {unidad.estadisticas.ataque}",
            f"Defensa: {unidad.estadisticas.defensa}",
            f"Moral: {unidad.moral_actual}%",
            f"Movimiento: {unidad.estadisticas.rango_movimiento}",
            f"Alcance: {unidad.estadisticas.rango_ataque}"
        ]

        y_offset = 60
        for stat in stats:
            stat_text = self.font_stats.render(stat, True, (60, 40, 20))
            screen.blit(stat_text, (info_x, info_y + y_offset))
            y_offset += 20

    def _render_controls(self, screen: pygame.Surface):
        """Renderiza los controles del juego"""
        controls = [
            "Click izq: Seleccionar/Mover",
            "Click der: Atacar",
            "Espacio: Finalizar turno",
            "F: Cambiar formación",
            "ESC: Menú"
        ]

        y = self.screen_height - 150
        for control in controls:
            control_text = self.font_stats.render(control, True, (80, 60, 40))
            screen.blit(control_text, (20, y))
            y += 25

    def _render_no_battle(self, screen: pygame.Surface):
        """Renderiza cuando no hay batalla activa"""
        screen.fill((230, 210, 180))
        text = self.font_title.render("LEGIO ROMANA", True, (139, 69, 19))
        rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(text, rect)

    def _render_animations(self, screen: pygame.Surface):
        """Renderiza animaciones activas"""
        # Por ahora vacío, se implementarán las animaciones después
        pass

    def set_highlights(self, movimientos: List[Posicion], objetivos: List[Unidad]):
        """Establece las casillas resaltadas"""
        self.movimientos_validos = movimientos
        self.objetivos_atacables = objetivos

    def get_board_position(self, mouse_pos: tuple) -> Optional[Posicion]:
        """Convierte posición del mouse a coordenadas del tablero"""
        x, y = mouse_pos
        col = (x - self.board_offset_x) // self.tile_size
        row = (y - self.board_offset_y) // self.tile_size

        if 0 <= row < self.board_height and 0 <= col < self.board_width:
            return Posicion(row, col)
        return None