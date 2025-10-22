"""
Ability panel UI component for displaying and managing unit abilities
"""

import pygame
from typing import List, Optional
from src.domain.abilities import HabilidadActiva


class BotonHabilidad:
    """Button for a single ability"""

    def __init__(self, x: int, y: int, ancho: int, alto: int, habilidad: HabilidadActiva):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.habilidad = habilidad
        self.hover = False
        self.puede_usar = habilidad.puede_usar()

        # Colors
        self.color_normal = (60, 60, 80)
        self.color_hover = (80, 80, 100)
        self.color_deshabilitado = (40, 40, 40)
        self.color_borde = (100, 100, 120)
        self.color_texto = (255, 255, 255)
        self.color_cooldown = (200, 100, 100)

    def actualizar(self, mouse_pos):
        """Update hover state"""
        self.hover = self.rect.collidepoint(mouse_pos)
        self.puede_usar = self.habilidad.puede_usar()

    def dibujar(self, screen, font):
        """Draw the ability button"""
        # Background color
        if not self.puede_usar:
            color = self.color_deshabilitado
        elif self.hover:
            color = self.color_hover
        else:
            color = self.color_normal

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.color_borde, self.rect, 2)

        # Ability name
        texto_nombre = font.render(self.habilidad.nombre[:15], True, self.color_texto)
        nombre_rect = texto_nombre.get_rect(centerx=self.rect.centerx, y=self.rect.y + 5)
        screen.blit(texto_nombre, nombre_rect)

        # Cooldown or uses remaining
        if self.habilidad.cooldown_actual > 0:
            texto_cd = font.render(f"CD: {self.habilidad.cooldown_actual}", True, self.color_cooldown)
            cd_rect = texto_cd.get_rect(centerx=self.rect.centerx, y=self.rect.y + 25)
            screen.blit(texto_cd, cd_rect)
        elif self.habilidad.usos_restantes is not None:
            texto_usos = font.render(f"Usos: {self.habilidad.usos_restantes}", True, self.color_texto)
            usos_rect = texto_usos.get_rect(centerx=self.rect.centerx, y=self.rect.y + 25)
            screen.blit(texto_usos, usos_rect)

    def click(self):
        """Handle click on button"""
        if self.puede_usar:
            return self.habilidad.nombre
        return None


class PanelHabilidades:
    """Panel for displaying unit abilities"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.ancho = 200
        self.alto = 0  # Dynamic based on abilities
        self.botones: List[BotonHabilidad] = []
        self.unidad_actual = None

        # Visual settings
        self.color_fondo = (30, 30, 40, 200)  # Semi-transparent
        self.color_borde = (80, 80, 100)
        self.color_titulo = (200, 200, 220)
        self.margen = 10
        self.espaciado_botones = 5
        self.alto_boton = 45

    def actualizar(self, unidad, mouse_pos):
        """Update panel with unit's abilities"""
        if unidad == self.unidad_actual:
            # Just update hover states
            for boton in self.botones:
                boton.actualizar(mouse_pos)
            return

        self.unidad_actual = unidad
        self.botones.clear()

        if not unidad or not unidad.gestor_habilidades:
            self.alto = 0
            return

        # Create buttons for each active ability
        y_actual = self.y + 40  # Space for title
        for habilidad in unidad.gestor_habilidades.habilidades_activas:
            boton = BotonHabilidad(
                x=self.x + self.margen,
                y=y_actual,
                ancho=self.ancho - 2 * self.margen,
                alto=self.alto_boton,
                habilidad=habilidad
            )
            self.botones.append(boton)
            y_actual += self.alto_boton + self.espaciado_botones

        # Calculate total height
        self.alto = y_actual - self.y + self.margen

    def dibujar(self, screen, font):
        """Draw the ability panel"""
        if not self.botones:
            return

        # Create surface with alpha for transparency
        superficie = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        superficie.fill(self.color_fondo)

        # Draw border
        pygame.draw.rect(superficie, self.color_borde, (0, 0, self.ancho, self.alto), 2)

        # Draw title
        titulo = font.render("Habilidades", True, self.color_titulo)
        titulo_rect = titulo.get_rect(centerx=self.ancho // 2, y=10)
        superficie.blit(titulo, titulo_rect)

        # Blit to main screen
        screen.blit(superficie, (self.x, self.y))

        # Draw buttons (directly on screen, not on surface)
        for boton in self.botones:
            boton.dibujar(screen, font)

    def manejar_click(self, pos) -> Optional[str]:
        """Handle click on panel, return ability name if clicked"""
        for boton in self.botones:
            if boton.rect.collidepoint(pos):
                return boton.click()
        return None

    def obtener_tooltip(self, pos) -> Optional[str]:
        """Get tooltip for ability at position"""
        for boton in self.botones:
            if boton.rect.collidepoint(pos):
                return boton.habilidad.descripcion
        return None


class TooltipHabilidad:
    """Tooltip for showing ability descriptions"""

    def __init__(self):
        self.color_fondo = (20, 20, 30, 230)
        self.color_borde = (100, 100, 120)
        self.color_texto = (255, 255, 255)
        self.padding = 10
        self.ancho_max = 250

    def dibujar(self, screen, font, texto: str, pos):
        """Draw tooltip at position"""
        if not texto:
            return

        # Split text into lines
        palabras = texto.split()
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            test_linea = f"{linea_actual} {palabra}".strip()
            if font.size(test_linea)[0] <= self.ancho_max:
                linea_actual = test_linea
            else:
                if linea_actual:
                    lineas.append(linea_actual)
                linea_actual = palabra

        if linea_actual:
            lineas.append(linea_actual)

        # Calculate dimensions
        alto_linea = font.get_height()
        ancho = max(font.size(linea)[0] for linea in lineas) if lineas else 0
        alto = len(lineas) * alto_linea

        # Create surface
        superficie = pygame.Surface(
            (ancho + 2 * self.padding, alto + 2 * self.padding),
            pygame.SRCALPHA
        )
        superficie.fill(self.color_fondo)
        pygame.draw.rect(
            superficie,
            self.color_borde,
            (0, 0, ancho + 2 * self.padding, alto + 2 * self.padding),
            2
        )

        # Draw text
        y = self.padding
        for linea in lineas:
            texto_render = font.render(linea, True, self.color_texto)
            superficie.blit(texto_render, (self.padding, y))
            y += alto_linea

        # Position tooltip (avoid going off screen)
        x, y = pos
        x = min(x, screen.get_width() - superficie.get_width())
        y = min(y, screen.get_height() - superficie.get_height())

        screen.blit(superficie, (x, y))