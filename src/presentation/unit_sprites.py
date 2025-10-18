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
            elif bando == Bando.GALIA:
                self._draw_gallic_unit(surface, tipo, size)
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

        elif tipo == TipoUnidad.VELITES:
            self._draw_velites(surface, center, size, is_roman=True)

        elif tipo == TipoUnidad.PRINCEPS:
            self._draw_princeps(surface, center, size, is_roman=True)

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

        elif tipo == TipoUnidad.VELITES:
            self._draw_velites(surface, center, size, is_roman=False)

        elif tipo == TipoUnidad.PRINCEPS:
            self._draw_princeps(surface, center, size, is_roman=False)

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

    def _draw_velites(self, surface: pygame.Surface, center: int, size: int, is_roman: bool):
        """Dibuja un Veles - infantería ligera con jabalinas"""
        # Colores
        primary = (170, 40, 40) if is_roman else (70, 90, 60)
        secondary = (210, 180, 140) if is_roman else (160, 140, 100)  # Cuero
        javelin_color = (101, 67, 33)

        # Cuerpo ligero (sin armadura pesada)
        body_rect = pygame.Rect(center - 10, center - 6, 20, 16)
        pygame.draw.rect(surface, primary, body_rect)
        pygame.draw.rect(surface, secondary, body_rect, 1)

        # Escudo pequeño de cuero (parma)
        pygame.draw.circle(surface, secondary, (center - 14, center), 8)
        pygame.draw.circle(surface, primary, (center - 14, center), 8, 2)
        # Diseño en el escudo
        pygame.draw.circle(surface, primary, (center - 14, center), 3)

        # Jabalina principal en la mano
        javelin_start = (center + 6, center + 8)
        javelin_end = (center + 16, center - 20)
        pygame.draw.line(surface, javelin_color, javelin_start, javelin_end, 2)
        # Punta de jabalina metálica
        javelin_tip = [
            (center + 16, center - 22),
            (center + 14, center - 20),
            (center + 18, center - 20)
        ]
        pygame.draw.polygon(surface, (150, 150, 150), javelin_tip)

        # Jabalina extra en la espalda
        pygame.draw.line(surface, javelin_color,
                        (center + 8, center - 8),
                        (center + 12, center - 16), 2)

        # Espada corta (gladius) en el cinturón
        sword_rect = pygame.Rect(center - 4, center + 4, 2, 8)
        pygame.draw.rect(surface, (150, 150, 150), sword_rect)

        # Casco ligero o gorro de cuero
        if is_roman:
            helmet_rect = pygame.Rect(center - 6, center - 13, 12, 7)
            pygame.draw.ellipse(surface, (120, 100, 80), helmet_rect)
        else:
            # Gorro de cuero para bárbaros
            hood_points = [
                (center - 6, center - 10),
                (center, center - 13),
                (center + 6, center - 10)
            ]
            pygame.draw.polygon(surface, secondary, hood_points)

        # Piernas (ligeras, rápidas)
        pygame.draw.line(surface, primary, (center - 4, center + 8), (center - 4, center + 18), 3)
        pygame.draw.line(surface, primary, (center + 4, center + 8), (center + 4, center + 18), 3)

        # Sandalias
        pygame.draw.circle(surface, secondary, (center - 4, center + 18), 2)
        pygame.draw.circle(surface, secondary, (center + 4, center + 18), 2)

    def _draw_princeps(self, surface: pygame.Surface, center: int, size: int, is_roman: bool):
        """Dibuja un Princeps - infantería veterana"""
        # Colores
        primary = (160, 20, 20) if is_roman else (90, 70, 50)
        secondary = (218, 165, 32) if is_roman else (200, 180, 150)  # Dorado oscuro
        armor_color = (130, 130, 130)

        # Cuerpo con lorica segmentata (armadura de placas)
        body_rect = pygame.Rect(center - 13, center - 9, 26, 22)
        pygame.draw.rect(surface, armor_color, body_rect)
        pygame.draw.rect(surface, primary, body_rect, 3)

        # Placas de armadura (detalles horizontales)
        for i in range(4):
            y = center - 7 + i * 5
            pygame.draw.line(surface, secondary, (center - 11, y), (center + 11, y), 1)

        # Escudo grande rectangular (scutum)
        shield_rect = pygame.Rect(center - 19, center - 11, 11, 24)
        pygame.draw.rect(surface, primary, shield_rect)
        pygame.draw.rect(surface, secondary, shield_rect, 2)

        # Águila o decoración en el escudo (solo romanos)
        if is_roman:
            # Águila estilizada
            pygame.draw.circle(surface, secondary, (center - 13, center - 2), 2)
            pygame.draw.line(surface, secondary,
                           (center - 13, center),
                           (center - 13, center + 6), 2)
            # Alas
            pygame.draw.line(surface, secondary,
                           (center - 13, center + 2),
                           (center - 16, center + 4), 1)
            pygame.draw.line(surface, secondary,
                           (center - 13, center + 2),
                           (center - 10, center + 4), 1)

        # Gladius (espada) desenvainada
        sword_start = (center + 9, center)
        sword_end = (center + 16, center - 12)
        pygame.draw.line(surface, (150, 150, 150), sword_start, sword_end, 3)
        # Empuñadura dorada
        pygame.draw.circle(surface, secondary, (center + 10, center + 2), 3)
        # Pomo
        pygame.draw.circle(surface, secondary, sword_end, 2)

        # Casco imperial con cresta transversal
        helmet_rect = pygame.Rect(center - 9, center - 17, 18, 10)
        pygame.draw.ellipse(surface, armor_color, helmet_rect)
        pygame.draw.ellipse(surface, secondary, helmet_rect, 2)

        # Cresta transversal (crista transversa) - distintivo de los Principes
        if is_roman:
            crest_color = (200, 0, 0)  # Rojo intenso
            for i in range(7):
                x = center - 6 + i * 2
                y_base = center - 19
                y_top = y_base - 4 - abs(3 - i)  # Forma arqueada
                pygame.draw.line(surface, crest_color, (x, y_base), (x, y_top), 2)
        else:
            # Cuernos o decoración bárbara
            pygame.draw.arc(surface, secondary,
                          pygame.Rect(center - 10, center - 22, 6, 6),
                          0, math.pi, 2)
            pygame.draw.arc(surface, secondary,
                          pygame.Rect(center + 4, center - 22, 6, 6),
                          0, math.pi, 2)

        # Protección de piernas (grebas)
        greave_color = armor_color if is_roman else primary
        pygame.draw.rect(surface, greave_color, (center - 6, center + 11, 4, 11))
        pygame.draw.rect(surface, greave_color, (center + 2, center + 11, 4, 11))
        pygame.draw.rect(surface, secondary, (center - 6, center + 11, 4, 11), 1)
        pygame.draw.rect(surface, secondary, (center + 2, center + 11, 4, 11), 1)

        # Capa roja (distintivo de veteranos)
        if is_roman:
            cape_points = [
                (center - 10, center - 5),
                (center - 12, center + 8),
                (center - 8, center + 10),
                (center - 6, center)
            ]
            pygame.draw.polygon(surface, (180, 0, 0), cape_points)
            pygame.draw.polygon(surface, secondary, cape_points, 1)

    def _draw_gallic_unit(self, surface: pygame.Surface, tipo: TipoUnidad, size: int):
        """Dibuja unidades galas con estilo celta distintivo"""
        center = size // 2

        if tipo == TipoUnidad.GUERRERO_TRIBAL:
            self._draw_guerrero_tribal(surface, center, size)
        elif tipo == TipoUnidad.ESPADAS_ELEGIDAS:
            self._draw_espadas_elegidas(surface, center, size)
        elif tipo == TipoUnidad.FANATICOS_DESNUDOS:
            self._draw_fanaticos_desnudos(surface, center, size)
        elif tipo == TipoUnidad.ESCARAMUZADORES:
            self._draw_escaramuzadores(surface, center, size)
        elif tipo == TipoUnidad.CABALLERIA_BARBARA:
            self._draw_caballeria_barbara(surface, center, size)
        elif tipo == TipoUnidad.CABALLERIA_NOBLE:
            self._draw_caballeria_noble(surface, center, size)
        elif tipo == TipoUnidad.CARROS_GUERRA:
            self._draw_carros_guerra(surface, center, size)

    def _draw_guerrero_tribal(self, surface: pygame.Surface, center: int, size: int):
        """Dibuja Guerrero Tribal galo"""
        verde_bosque = (70, 120, 70)
        marron_cuero = (139, 90, 43)
        piel = (200, 150, 100)
        metal = (150, 150, 150)
        oro = (218, 165, 32)

        # Cuerpo - Túnica con patrón tribal
        body_rect = pygame.Rect(center - 11, center - 7, 22, 18)
        pygame.draw.rect(surface, verde_bosque, body_rect)
        pygame.draw.rect(surface, marron_cuero, body_rect, 2)

        # Patrón tribal (líneas diagonales)
        for i in range(3):
            pygame.draw.line(surface, (50, 90, 50),
                           (center - 8 + i*5, center - 5),
                           (center - 5 + i*5, center + 5), 2)

        # Escudo ovalado característico galo
        shield_points = [
            (center - 16, center - 2),
            (center - 18, center + 5),
            (center - 12, center + 8),
            (center - 10, center + 1)
        ]
        pygame.draw.polygon(surface, marron_cuero, shield_points)
        pygame.draw.polygon(surface, verde_bosque, shield_points, 2)
        pygame.draw.circle(surface, metal, (center - 14, center + 3), 3)

        # Espada larga gala (Spatha)
        pygame.draw.line(surface, metal,
                        (center + 8, center + 8),
                        (center + 17, center - 15), 3)
        pygame.draw.circle(surface, oro, (center + 17, center - 15), 2)

        # Cabeza
        pygame.draw.circle(surface, piel, (center, center - 13), 7)

        # Cabello largo (trenzas galas)
        for offset in [-6, 6]:
            pygame.draw.line(surface, (120, 80, 40),
                           (center + offset, center - 13),
                           (center + offset, center - 5), 3)

        # Bigote galo prominente
        bigote_rect = pygame.Rect(center - 5, center - 13, 10, 6)
        pygame.draw.arc(surface, (120, 80, 40), bigote_rect, math.pi, 2*math.pi, 2)

        # Torques (collar de oro - símbolo galo)
        torques_rect = pygame.Rect(center - 6, center - 8, 12, 8)
        pygame.draw.arc(surface, oro, torques_rect, 0, math.pi, 3)

        # Pantalones (braies - característico galo)
        pygame.draw.line(surface, verde_bosque,
                        (center - 5, center + 10),
                        (center - 5, center + 20), 4)
        pygame.draw.line(surface, verde_bosque,
                        (center + 5, center + 10),
                        (center + 5, center + 20), 4)

    def _draw_espadas_elegidas(self, surface: pygame.Surface, center: int, size: int):
        """Dibuja Espadas Elegidas (Soldurii) - élite gala"""
        azul_oscuro = (40, 80, 120)
        plata = (192, 192, 192)
        oro = (218, 165, 32)

        # Cota de malla
        body_rect = pygame.Rect(center - 13, center - 9, 26, 22)
        pygame.draw.rect(surface, plata, body_rect)

        # Patrón de malla
        for i in range(3):
            for j in range(4):
                pygame.draw.circle(surface, (150, 150, 150),
                                 (center - 10 + j*6, center - 7 + i*6), 1)

        # Sobreveste con decoración
        vest_rect = pygame.Rect(center - 11, center - 8, 22, 18)
        pygame.draw.rect(surface, azul_oscuro, vest_rect)
        pygame.draw.rect(surface, oro, vest_rect, 2)

        # Escudo hexagonal grande
        shield_points = [
            (center - 20, center - 4),
            (center - 18, center - 10),
            (center - 9, center - 10),
            (center - 7, center - 4),
            (center - 9, center + 14),
            (center - 18, center + 14)
        ]
        pygame.draw.polygon(surface, azul_oscuro, shield_points)
        pygame.draw.polygon(surface, oro, shield_points, 3)
        pygame.draw.circle(surface, plata, (center - 14, center + 2), 4)
        pygame.draw.circle(surface, oro, (center - 14, center + 2), 4, 2)

        # Espada larga de élite
        pygame.draw.line(surface, plata,
                        (center + 10, center + 5),
                        (center + 18, center - 14), 4)
        pygame.draw.rect(surface, oro, (center + 13, center - 6, 3, 8))
        pygame.draw.circle(surface, oro, (center + 18, center - 14), 3)

        # Casco celta con adornos
        helmet_rect = pygame.Rect(center - 9, center - 18, 18, 11)
        pygame.draw.ellipse(surface, plata, helmet_rect)
        pygame.draw.ellipse(surface, oro, helmet_rect, 2)

        # Cresta/penacho
        for i in range(4):
            pygame.draw.line(surface, (150, 50, 50),
                           (center - 4 + i*2, center - 19),
                           (center - 4 + i*2, center - 24), 2)

        # Piernas con grebas
        pygame.draw.rect(surface, plata, (center - 6, center + 11, 4, 11))
        pygame.draw.rect(surface, plata, (center + 2, center + 11, 4, 11))
        pygame.draw.rect(surface, oro, (center - 6, center + 11, 4, 11), 1)
        pygame.draw.rect(surface, oro, (center + 2, center + 11, 4, 11), 1)

    def _draw_fanaticos_desnudos(self, surface: pygame.Surface, center: int, size: int):
        """Dibuja Fanáticos Desnudos (Gaesatae) - berserkers"""
        piel = (180, 140, 100)
        pintura_guerra = (150, 40, 40)
        metal = (150, 150, 150)

        # Cuerpo desnudo musculoso
        torso_points = [
            (center - 10, center - 8),
            (center + 10, center - 8),
            (center + 12, center + 6),
            (center - 12, center + 6)
        ]
        pygame.draw.polygon(surface, piel, torso_points)

        # Pintura de guerra (espirales celtas)
        for radio in [3, 5, 7]:
            pygame.draw.circle(surface, pintura_guerra,
                             (center - 4, center - 2), radio, 1)

        # Líneas tribales
        pygame.draw.line(surface, pintura_guerra,
                        (center - 8, center - 5),
                        (center + 8, center - 5), 2)
        pygame.draw.line(surface, pintura_guerra,
                        (center - 6, center),
                        (center + 6, center), 2)

        # Gran espada de dos manos
        pygame.draw.line(surface, metal,
                        (center + 15, center + 10),
                        (center + 22, center - 20), 5)
        pygame.draw.rect(surface, (101, 67, 33), (center + 17, center - 8, 3, 12))
        pygame.draw.circle(surface, (100, 80, 20), (center + 22, center - 20), 3)

        # Segunda arma (dual wield)
        pygame.draw.line(surface, metal,
                        (center - 12, center + 8),
                        (center - 18, center - 15), 3)

        # Cabeza con cabello erizado (cal)
        pygame.draw.circle(surface, piel, (center, center - 14), 7)

        # Cabello salvaje con cal (blanco)
        for i in range(7):
            angulo = (i - 3) * 0.4
            x = center + int(6 * math.sin(angulo))
            y = center - 14 + int(-6 * math.cos(angulo))
            pygame.draw.line(surface, (220, 220, 180),
                           (center, center - 14), (x, y), 2)

        # Ojos furiosos
        pygame.draw.circle(surface, pintura_guerra, (center - 2, center - 14), 2)
        pygame.draw.circle(surface, pintura_guerra, (center + 2, center - 14), 2)

        # Piernas desnudas
        pygame.draw.line(surface, piel,
                        (center - 5, center + 6),
                        (center - 5, center + 20), 5)
        pygame.draw.line(surface, piel,
                        (center + 5, center + 6),
                        (center + 5, center + 20), 5)

    def _draw_escaramuzadores(self, surface: pygame.Surface, center: int, size: int):
        """Dibuja Escaramuzadores (Funditores) - infantería ligera"""
        verde_oliva = (90, 100, 70)
        cuero_claro = (160, 140, 100)
        piel = (180, 140, 100)

        # Cuerpo ligero
        body_rect = pygame.Rect(center - 9, center - 6, 18, 15)
        pygame.draw.rect(surface, verde_oliva, body_rect)
        pygame.draw.rect(surface, cuero_claro, body_rect, 1)

        # Mochila con proyectiles
        mochila_points = [
            (center + 8, center - 4),
            (center + 12, center - 6),
            (center + 12, center + 2),
            (center + 8, center + 4)
        ]
        pygame.draw.polygon(surface, cuero_claro, mochila_points)

        # Honda en la mano
        honda_rect = pygame.Rect(center - 20, center - 10, 15, 20)
        pygame.draw.arc(surface, (139, 90, 43), honda_rect, -math.pi/3, math.pi/3, 2)
        pygame.draw.circle(surface, (100, 100, 100), (center - 15, center), 3)

        # Jabalinas en la espalda
        for i in range(3):
            x_offset = i * 2
            pygame.draw.line(surface, (101, 67, 33),
                           (center + 6 + x_offset, center - 5),
                           (center + 8 + x_offset, center - 16), 2)
            pygame.draw.circle(surface, (120, 120, 120),
                             (center + 8 + x_offset, center - 16), 2)

        # Escudo pequeño de mimbre
        pygame.draw.circle(surface, (139, 90, 43), (center + 10, center + 2), 5)
        pygame.draw.circle(surface, cuero_claro, (center + 10, center + 2), 5, 1)

        # Cabeza con gorro
        pygame.draw.circle(surface, piel, (center, center - 12), 6)
        gorro_points = [
            (center - 6, center - 11),
            (center, center - 15),
            (center + 6, center - 11)
        ]
        pygame.draw.polygon(surface, cuero_claro, gorro_points)

        # Piernas ligeras
        pygame.draw.line(surface, verde_oliva,
                        (center - 4, center + 8),
                        (center - 4, center + 18), 3)
        pygame.draw.line(surface, verde_oliva,
                        (center + 4, center + 8),
                        (center + 4, center + 18), 3)

    def _draw_caballeria_barbara(self, surface: pygame.Surface, center: int, size: int):
        """Dibuja Caballería Bárbara - caballería ligera gala"""
        marron = (100, 70, 40)
        cuero = (160, 130, 90)
        caballo_oscuro = (80, 50, 30)
        metal = (150, 150, 150)

        # Caballo - cuerpo
        horse_body = pygame.Rect(center - 16, center + 2, 32, 14)
        pygame.draw.ellipse(surface, caballo_oscuro, horse_body)

        # Cabeza del caballo
        head_points = [
            (center - 18, center + 4),
            (center - 24, center - 2),
            (center - 23, center - 6),
            (center - 17, center - 3)
        ]
        pygame.draw.polygon(surface, caballo_oscuro, head_points)
        pygame.draw.circle(surface, (255, 255, 255), (center - 20, center - 2), 2)
        pygame.draw.circle(surface, (0, 0, 0), (center - 20, center - 2), 1)

        # Crin
        for i in range(5):
            pygame.draw.line(surface, (60, 40, 20),
                           (center - 18 + i*3, center - 3),
                           (center - 18 + i*3, center - 8), 2)

        # Patas
        patas = [
            (center - 12, center + 14, center - 12, center + 22),
            (center - 6, center + 14, center - 7, center + 20),
            (center + 6, center + 14, center + 5, center + 21),
            (center + 12, center + 14, center + 12, center + 22)
        ]
        for x1, y1, x2, y2 in patas:
            pygame.draw.line(surface, caballo_oscuro, (x1, y1), (x2, y2), 3)

        # Jinete
        rider_rect = pygame.Rect(center - 9, center - 10, 18, 16)
        pygame.draw.rect(surface, marron, rider_rect)
        pygame.draw.rect(surface, cuero, rider_rect, 2)

        # Lanza
        pygame.draw.line(surface, (101, 67, 33),
                        (center + 8, center - 6),
                        (center + 22, center - 22), 3)
        punta = [
            (center + 22, center - 24),
            (center + 20, center - 22),
            (center + 24, center - 22)
        ]
        pygame.draw.polygon(surface, metal, punta)

        # Escudo
        shield_rect = pygame.Rect(center - 16, center - 6, 8, 14)
        pygame.draw.ellipse(surface, cuero, shield_rect)
        pygame.draw.ellipse(surface, marron, shield_rect, 2)

        # Casco simple
        helmet_rect = pygame.Rect(center - 7, center - 17, 14, 9)
        pygame.draw.ellipse(surface, (120, 100, 80), helmet_rect)

        # Cola
        cola_points = [
            (center + 16, center + 6),
            (center + 24, center + 10),
            (center + 22, center + 14)
        ]
        pygame.draw.lines(surface, (60, 40, 20), False, cola_points, 3)

    def _draw_caballeria_noble(self, surface: pygame.Surface, center: int, size: int):
        """Dibuja Caballería Noble - élite montada gala"""
        purpura = (80, 40, 100)
        oro = (218, 165, 32)
        caballo_noble = (60, 60, 80)
        plata = (192, 192, 192)

        # Caballo de guerra con armadura
        horse_body = pygame.Rect(center - 17, center + 1, 34, 16)
        pygame.draw.ellipse(surface, caballo_noble, horse_body)
        pygame.draw.ellipse(surface, plata, horse_body, 2)

        # Cabeza con armadura
        head_points = [
            (center - 19, center + 3),
            (center - 26, center - 4),
            (center - 24, center - 8),
            (center - 17, center - 4)
        ]
        pygame.draw.polygon(surface, caballo_noble, head_points)
        pygame.draw.polygon(surface, plata, head_points, 2)
        pygame.draw.circle(surface, oro, (center - 22, center - 4), 3)

        # Crin trenzada
        for i in range(4):
            x = center - 19 + i*3
            pygame.draw.line(surface, (40, 40, 60),
                           (x, center - 4), (x, center - 10), 3)
            pygame.draw.circle(surface, oro, (x, center - 10), 1)

        # Patas con protección
        for x_offset in [-13, -7, 7, 13]:
            x = center + x_offset
            pygame.draw.line(surface, caballo_noble, (x, center + 15), (x, center + 23), 4)
            pygame.draw.line(surface, plata, (x, center + 15), (x, center + 19), 2)

        # Jinete aristocrático
        rider_rect = pygame.Rect(center - 10, center - 12, 20, 18)
        pygame.draw.rect(surface, plata, rider_rect)
        vest_rect = pygame.Rect(center - 8, center - 11, 16, 16)
        pygame.draw.rect(surface, purpura, vest_rect)
        pygame.draw.rect(surface, oro, vest_rect, 2)

        # Espada noble
        pygame.draw.line(surface, plata,
                        (center + 9, center - 2),
                        (center + 19, center - 16), 4)
        pygame.draw.rect(surface, oro, (center + 13, center - 10, 3, 8))
        pygame.draw.circle(surface, oro, (center + 19, center - 16), 3)
        pygame.draw.circle(surface, (200, 50, 50), (center + 19, center - 16), 1)

        # Escudo noble con heráldica
        shield_rect = pygame.Rect(center - 18, center - 8, 10, 18)
        pygame.draw.ellipse(surface, purpura, shield_rect)
        pygame.draw.ellipse(surface, oro, shield_rect, 3)
        pygame.draw.ellipse(surface, oro, (center - 15, center - 2, 4, 6))

        # Casco noble con cresta
        helmet_rect = pygame.Rect(center - 8, center - 20, 16, 10)
        pygame.draw.ellipse(surface, plata, helmet_rect)
        pygame.draw.ellipse(surface, oro, helmet_rect, 2)

        # Plumas nobles
        for i in range(5):
            pygame.draw.line(surface, (150, 50, 50),
                           (center - 6 + i*3, center - 21),
                           (center - 6 + i*3, center - 26), 2)

        # Cola decorada
        cola_points = [
            (center + 17, center + 7),
            (center + 25, center + 11),
            (center + 23, center + 16)
        ]
        pygame.draw.lines(surface, (40, 40, 60), False, cola_points, 4)

    def _draw_carros_guerra(self, surface: pygame.Surface, center: int, size: int):
        """Dibuja Carros de Guerra (Esseda) - unidad especial britana"""
        azul_acero = (60, 90, 120)
        madera = (101, 67, 33)
        metal = (150, 150, 150)
        caballo = (80, 60, 40)

        # Ruedas
        for x_offset in [-10, 10]:
            wheel_center = (center + x_offset, center + 12)
            pygame.draw.circle(surface, madera, wheel_center, 8)
            pygame.draw.circle(surface, metal, wheel_center, 8, 2)
            # Radios
            for angulo in [0, math.pi/3, 2*math.pi/3, math.pi, 4*math.pi/3, 5*math.pi/3]:
                x_fin = wheel_center[0] + int(7 * math.cos(angulo))
                y_fin = wheel_center[1] + int(7 * math.sin(angulo))
                pygame.draw.line(surface, madera, wheel_center, (x_fin, y_fin), 1)

        # Plataforma
        platform_rect = pygame.Rect(center - 14, center - 2, 28, 12)
        pygame.draw.rect(surface, madera, platform_rect)
        pygame.draw.rect(surface, metal, platform_rect, 2)

        # Barandilla frontal
        rail_rect = pygame.Rect(center - 14, center - 8, 28, 10)
        pygame.draw.arc(surface, metal, rail_rect, 0, math.pi, 3)

        # Eje
        pygame.draw.line(surface, metal,
                        (center - 12, center + 12),
                        (center + 12, center + 12), 4)

        # Caballos (dos)
        # Caballo izquierdo
        horse_body_l = pygame.Rect(center - 22, center - 6, 14, 8)
        pygame.draw.ellipse(surface, caballo, horse_body_l)
        pygame.draw.circle(surface, caballo, (center - 26, center - 8), 4)
        pygame.draw.line(surface, caballo, (center - 20, center + 2), (center - 20, center + 10), 2)
        pygame.draw.line(surface, caballo, (center - 24, center + 2), (center - 24, center + 10), 2)

        # Caballo derecho
        horse_body_r = pygame.Rect(center + 8, center - 6, 14, 8)
        pygame.draw.ellipse(surface, caballo, horse_body_r)
        pygame.draw.circle(surface, caballo, (center + 26, center - 8), 4)
        pygame.draw.line(surface, caballo, (center + 20, center + 2), (center + 20, center + 10), 2)
        pygame.draw.line(surface, caballo, (center + 24, center + 2), (center + 24, center + 10), 2)

        # Riendas
        pygame.draw.line(surface, (139, 90, 43), (center - 26, center - 8), (center - 5, center - 4), 1)
        pygame.draw.line(surface, (139, 90, 43), (center + 26, center - 8), (center + 5, center - 4), 1)

        # Guerrero en el carro
        warrior_rect = pygame.Rect(center - 6, center - 12, 12, 14)
        pygame.draw.rect(surface, azul_acero, warrior_rect)
        pygame.draw.rect(surface, metal, warrior_rect, 1)

        # Casco
        helmet_rect = pygame.Rect(center - 5, center - 18, 10, 8)
        pygame.draw.ellipse(surface, metal, helmet_rect)

        # Lanza
        pygame.draw.line(surface, madera,
                        (center + 6, center - 8),
                        (center + 18, center - 22), 2)
        punta = [
            (center + 18, center - 24),
            (center + 16, center - 22),
            (center + 20, center - 22)
        ]
        pygame.draw.polygon(surface, metal, punta)

        # Escudo en el carro
        pygame.draw.circle(surface, azul_acero, (center - 10, center - 6), 5)
        pygame.draw.circle(surface, metal, (center - 10, center - 6), 5, 1)