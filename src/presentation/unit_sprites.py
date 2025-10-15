"""
Sistema de sprites/iconos para las unidades de Legio Romana
"""

import pygame
import math
from typing import Tuple
from src.domain.value_objects import TipoUnidad, Bando


class UnitSpriteRenderer:
    """Renderiza sprites personalizados para cada tipo de unidad"""

    def __init__(self):
        self.cache = {}  # Cache de superficies pre-renderizadas

    def get_unit_sprite(self, tipo: TipoUnidad, bando: Bando, size: int = 60) -> pygame.Surface:
        """Obtiene o crea el sprite de una unidad"""
        cache_key = (tipo, bando, size)

        if cache_key not in self.cache:
            surface = pygame.Surface((size, size), pygame.SRCALPHA)

            if bando == Bando.ROMA:
                self._draw_roman_unit(surface, tipo, size)
            else:
                self._draw_barbarian_unit(surface, tipo, size)

            self.cache[cache_key] = surface

        return self.cache[cache_key]

    def _draw_roman_unit(self, surface: pygame.Surface, tipo: TipoUnidad, size: int):
        """Dibuja unidades romanas con estilo distintivo"""
        center = size // 2

        if tipo == TipoUnidad.LEGIONARIO:
            self._draw_legionary(surface, center, size, is_roman=True)

        elif tipo == TipoUnidad.HASTATI:
            self._draw_heavy_infantry(surface, center, size, is_roman=True)

        elif tipo == TipoUnidad.TRIARII:
            self._draw_spearman(surface, center, size, is_roman=True)

        elif tipo == TipoUnidad.EQUITES:
            self._draw_cavalry(surface, center, size, is_roman=True)

        elif tipo == TipoUnidad.SAGITTARII:
            self._draw_archer(surface, center, size, is_roman=True)

    def _draw_barbarian_unit(self, surface: pygame.Surface, tipo: TipoUnidad, size: int):
        """Dibuja unidades bárbaras con estilo distintivo"""
        center = size // 2

        if tipo == TipoUnidad.LEGIONARIO:
            self._draw_warrior(surface, center, size)

        elif tipo == TipoUnidad.HASTATI:
            self._draw_berserker(surface, center, size)

        elif tipo == TipoUnidad.TRIARII:
            self._draw_spearman(surface, center, size, is_roman=False)

        elif tipo == TipoUnidad.EQUITES:
            self._draw_cavalry(surface, center, size, is_roman=False)

        elif tipo == TipoUnidad.SAGITTARII:
            self._draw_archer(surface, center, size, is_roman=False)

    def _draw_legionary(self, surface: pygame.Surface, center: int, size: int, is_roman: bool):
        """Dibuja un legionario romano"""
        # Colores
        primary = (180, 20, 20) if is_roman else (50, 100, 50)
        secondary = (255, 215, 0) if is_roman else (139, 69, 19)
        shield_color = (200, 50, 50) if is_roman else (100, 100, 100)

        # Cuerpo (torso)
        body_rect = pygame.Rect(center - 12, center - 8, 24, 20)
        pygame.draw.rect(surface, primary, body_rect)
        pygame.draw.rect(surface, secondary, body_rect, 2)

        # Escudo rectangular (scutum romano)
        shield_rect = pygame.Rect(center - 18, center - 10, 12, 22)
        pygame.draw.rect(surface, shield_color, shield_rect)
        pygame.draw.rect(surface, secondary, shield_rect, 2)

        # Águila romana en el escudo (solo para romanos)
        if is_roman:
            pygame.draw.circle(surface, secondary, (center - 12, center), 3)

        # Espada (gladius)
        sword_start = (center + 8, center - 5)
        sword_end = (center + 14, center - 15)
        pygame.draw.line(surface, (150, 150, 150), sword_start, sword_end, 3)
        pygame.draw.circle(surface, secondary, sword_end, 2)  # Pomo

        # Casco
        helmet_rect = pygame.Rect(center - 8, center - 15, 16, 8)
        pygame.draw.ellipse(surface, (100, 100, 100), helmet_rect)
        pygame.draw.arc(surface, secondary, helmet_rect, 0, math.pi, 2)

        # Piernas
        pygame.draw.line(surface, primary, (center - 5, center + 10), (center - 5, center + 20), 3)
        pygame.draw.line(surface, primary, (center + 5, center + 10), (center + 5, center + 20), 3)

    def _draw_heavy_infantry(self, surface: pygame.Surface, center: int, size: int, is_roman: bool):
        """Dibuja infantería pesada (Hastati/Berserker)"""
        # Colores
        primary = (150, 20, 20) if is_roman else (80, 80, 80)
        secondary = (192, 192, 192) if is_roman else (200, 200, 200)
        armor_color = (120, 120, 120)

        # Cuerpo con armadura pesada
        body_rect = pygame.Rect(center - 14, center - 10, 28, 24)
        pygame.draw.rect(surface, armor_color, body_rect)
        pygame.draw.rect(surface, primary, body_rect, 3)

        # Detalles de armadura (placas)
        for i in range(3):
            y = center - 8 + i * 6
            pygame.draw.line(surface, secondary, (center - 12, y), (center + 12, y), 1)

        # Escudo grande
        shield_points = [
            (center - 20, center - 12),
            (center - 8, center - 14),
            (center - 8, center + 14),
            (center - 20, center + 12)
        ]
        pygame.draw.polygon(surface, primary, shield_points)
        pygame.draw.polygon(surface, secondary, shield_points, 2)

        # Espada ancha
        sword_rect = pygame.Rect(center + 10, center - 18, 4, 20)
        pygame.draw.rect(surface, (150, 150, 150), sword_rect)
        pygame.draw.circle(surface, secondary, (center + 12, center - 20), 3)

        # Casco con pluma
        helmet_rect = pygame.Rect(center - 10, center - 18, 20, 10)
        pygame.draw.ellipse(surface, armor_color, helmet_rect)
        # Pluma
        if is_roman:
            for i in range(3):
                x = center + i * 2 - 2
                y = center - 22 - i
                pygame.draw.line(surface, (255, 0, 0), (x, y), (x, y - 5), 2)

        # Piernas con grebas (protección)
        leg_color = armor_color if is_roman else primary
        pygame.draw.rect(surface, leg_color, (center - 7, center + 12, 5, 10))
        pygame.draw.rect(surface, leg_color, (center + 2, center + 12, 5, 10))

    def _draw_spearman(self, surface: pygame.Surface, center: int, size: int, is_roman: bool):
        """Dibuja lancero (Triarii/Piquero)"""
        # Colores
        primary = (120, 20, 20) if is_roman else (60, 60, 120)
        secondary = (205, 127, 50) if is_roman else (180, 180, 180)

        # Cuerpo
        body_rect = pygame.Rect(center - 10, center - 8, 20, 18)
        pygame.draw.rect(surface, primary, body_rect)
        pygame.draw.rect(surface, secondary, body_rect, 2)

        # Lanza larga (hasta)
        spear_start = (center + 5, center + 15)
        spear_end = (center + 18, center - 25)
        pygame.draw.line(surface, (101, 67, 33), spear_start, spear_end, 3)

        # Punta de lanza
        spear_tip = [
            (center + 18, center - 28),
            (center + 15, center - 25),
            (center + 21, center - 25)
        ]
        pygame.draw.polygon(surface, (150, 150, 150), spear_tip)

        # Escudo pequeño redondo
        pygame.draw.circle(surface, primary, (center - 12, center), 10)
        pygame.draw.circle(surface, secondary, (center - 12, center), 10, 2)
        # Centro del escudo
        pygame.draw.circle(surface, secondary, (center - 12, center), 3)

        # Casco
        helmet_rect = pygame.Rect(center - 7, center - 14, 14, 8)
        pygame.draw.ellipse(surface, (100, 100, 100), helmet_rect)

        # Piernas
        pygame.draw.line(surface, primary, (center - 4, center + 8), (center - 4, center + 18), 3)
        pygame.draw.line(surface, primary, (center + 4, center + 8), (center + 4, center + 18), 3)

    def _draw_cavalry(self, surface: pygame.Surface, center: int, size: int, is_roman: bool):
        """Dibuja caballería (Equites/Jinete)"""
        # Colores
        primary = (160, 30, 30) if is_roman else (100, 50, 0)
        secondary = (255, 255, 255) if is_roman else (200, 150, 100)
        horse_color = (101, 67, 33) if is_roman else (60, 40, 20)

        # Caballo - cuerpo
        horse_body = pygame.Rect(center - 15, center, 30, 15)
        pygame.draw.ellipse(surface, horse_color, horse_body)

        # Caballo - cabeza
        horse_head = [
            (center - 18, center + 2),
            (center - 25, center - 5),
            (center - 22, center - 8),
            (center - 15, center - 5)
        ]
        pygame.draw.polygon(surface, horse_color, horse_head)

        # Caballo - patas (4 patas)
        for x in [center - 10, center - 5, center + 5, center + 10]:
            pygame.draw.line(surface, horse_color, (x, center + 12), (x, center + 22), 3)

        # Jinete - cuerpo
        rider_rect = pygame.Rect(center - 8, center - 10, 16, 15)
        pygame.draw.rect(surface, primary, rider_rect)
        pygame.draw.rect(surface, secondary, rider_rect, 1)

        # Jinete - casco con cresta
        helmet_rect = pygame.Rect(center - 6, center - 16, 12, 8)
        pygame.draw.ellipse(surface, (100, 100, 100), helmet_rect)
        if is_roman:
            # Cresta romana
            for i in range(5):
                y = center - 18 - i
                pygame.draw.line(surface, (255, 0, 0), (center - 3 + i, y), (center - 3 + i, y - 3), 1)

        # Lanza de caballería
        lance_start = (center + 8, center - 8)
        lance_end = (center + 20, center - 20)
        pygame.draw.line(surface, (101, 67, 33), lance_start, lance_end, 2)
        pygame.draw.circle(surface, (150, 150, 150), lance_end, 3)

        # Cola del caballo
        tail_points = [
            (center + 15, center + 5),
            (center + 22, center + 8),
            (center + 20, center + 12),
            (center + 15, center + 10)
        ]
        pygame.draw.lines(surface, horse_color, False, tail_points, 2)

    def _draw_archer(self, surface: pygame.Surface, center: int, size: int, is_roman: bool):
        """Dibuja arquero (Sagittarii)"""
        # Colores
        primary = (140, 25, 25) if is_roman else (50, 80, 50)
        secondary = (139, 69, 19) if is_roman else (150, 150, 150)
        bow_color = (101, 67, 33)

        # Cuerpo (más ligero, sin armadura pesada)
        body_rect = pygame.Rect(center - 8, center - 6, 16, 16)
        pygame.draw.rect(surface, primary, body_rect)
        pygame.draw.rect(surface, secondary, body_rect, 1)

        # Arco
        bow_rect = pygame.Rect(center - 20, center - 15, 15, 30)
        pygame.draw.arc(surface, bow_color, bow_rect, -math.pi/2, math.pi/2, 3)

        # Cuerda del arco
        pygame.draw.line(surface, (200, 200, 200),
                        (center - 20, center - 15),
                        (center - 20, center + 15), 1)

        # Flecha preparada
        arrow_start = (center - 18, center)
        arrow_end = (center - 5, center)
        pygame.draw.line(surface, (101, 67, 33), arrow_start, arrow_end, 2)
        # Punta de flecha
        arrow_tip = [
            (center - 5, center),
            (center - 8, center - 2),
            (center - 8, center + 2)
        ]
        pygame.draw.polygon(surface, (150, 150, 150), arrow_tip)

        # Carcaj con flechas
        quiver_rect = pygame.Rect(center + 8, center - 5, 6, 15)
        pygame.draw.rect(surface, secondary, quiver_rect)
        # Flechas en el carcaj
        for i in range(3):
            x = center + 10 + i * 2
            pygame.draw.line(surface, (101, 67, 33), (x, center - 5), (x, center - 10), 1)

        # Capucha o casco ligero
        hood_points = [
            (center - 6, center - 12),
            (center, center - 15),
            (center + 6, center - 12),
            (center + 4, center - 8),
            (center - 4, center - 8)
        ]
        pygame.draw.polygon(surface, primary, hood_points)

        # Piernas
        pygame.draw.line(surface, primary, (center - 3, center + 8), (center - 3, center + 18), 3)
        pygame.draw.line(surface, primary, (center + 3, center + 8), (center + 3, center + 18), 3)

    def _draw_warrior(self, surface: pygame.Surface, center: int, size: int):
        """Dibuja guerrero bárbaro básico"""
        # Colores bárbaros
        primary = (50, 100, 50)
        secondary = (139, 69, 19)

        # Cuerpo con pieles
        body_points = [
            (center - 12, center - 8),
            (center + 12, center - 8),
            (center + 10, center + 10),
            (center - 10, center + 10)
        ]
        pygame.draw.polygon(surface, primary, body_points)
        pygame.draw.polygon(surface, secondary, body_points, 2)

        # Hacha bárbara
        axe_handle_start = (center + 10, center + 5)
        axe_handle_end = (center + 18, center - 12)
        pygame.draw.line(surface, (101, 67, 33), axe_handle_start, axe_handle_end, 3)

        # Cabeza del hacha
        axe_head = [
            (center + 15, center - 14),
            (center + 22, center - 12),
            (center + 20, center - 8),
            (center + 16, center - 10)
        ]
        pygame.draw.polygon(surface, (150, 150, 150), axe_head)

        # Escudo redondo pequeño
        pygame.draw.circle(surface, (100, 100, 100), (center - 10, center), 8)
        pygame.draw.circle(surface, secondary, (center - 10, center), 8, 2)

        # Cabeza con barba
        pygame.draw.circle(surface, (200, 150, 100), (center, center - 12), 6)
        # Barba
        beard_points = [
            (center - 4, center - 10),
            (center - 2, center - 6),
            (center + 2, center - 6),
            (center + 4, center - 10)
        ]
        pygame.draw.polygon(surface, (100, 50, 0), beard_points)

        # Piernas
        pygame.draw.line(surface, primary, (center - 5, center + 8), (center - 5, center + 20), 4)
        pygame.draw.line(surface, primary, (center + 5, center + 8), (center + 5, center + 20), 4)

    def _draw_berserker(self, surface: pygame.Surface, center: int, size: int):
        """Dibuja berserker bárbaro"""
        # Colores salvajes
        primary = (80, 80, 80)
        secondary = (200, 200, 200)
        rage_color = (150, 0, 0)

        # Cuerpo musculoso
        body_rect = pygame.Rect(center - 14, center - 10, 28, 24)
        pygame.draw.rect(surface, primary, body_rect)

        # Marcas de guerra
        for i in range(3):
            y = center - 5 + i * 5
            pygame.draw.line(surface, rage_color, (center - 10, y), (center + 10, y), 2)

        # Dos hachas (dual wield)
        # Hacha izquierda
        pygame.draw.line(surface, (101, 67, 33), (center - 15, center), (center - 20, center - 10), 2)
        pygame.draw.polygon(surface, (150, 150, 150), [
            (center - 22, center - 10),
            (center - 18, center - 12),
            (center - 18, center - 8)
        ])

        # Hacha derecha
        pygame.draw.line(surface, (101, 67, 33), (center + 15, center), (center + 20, center - 10), 2)
        pygame.draw.polygon(surface, (150, 150, 150), [
            (center + 22, center - 10),
            (center + 18, center - 12),
            (center + 18, center - 8)
        ])

        # Cabeza con cuernos en el casco
        pygame.draw.circle(surface, (200, 150, 100), (center, center - 14), 7)
        # Cuernos
        pygame.draw.arc(surface, secondary,
                       pygame.Rect(center - 12, center - 20, 8, 8),
                       0, math.pi, 2)
        pygame.draw.arc(surface, secondary,
                       pygame.Rect(center + 4, center - 20, 8, 8),
                       0, math.pi, 2)

        # Ojos furiosos
        pygame.draw.circle(surface, rage_color, (center - 2, center - 14), 1)
        pygame.draw.circle(surface, rage_color, (center + 2, center - 14), 1)

        # Piernas
        pygame.draw.line(surface, primary, (center - 6, center + 12), (center - 6, center + 22), 5)
        pygame.draw.line(surface, primary, (center + 6, center + 12), (center + 6, center + 22), 5)