"""
Estado para seleccionar entre diferentes campañas
"""

import pygame
from src.core.state import State
from src.ui.button import Button
from src.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT

# Definir colores usados en este módulo
COLOR_NEGRO = (0, 0, 0)
COLOR_BLANCO = (255, 255, 255)
COLOR_ROJO_OSCURO = (180, 20, 20)
COLOR_DORADO = (255, 215, 0)
COLOR_GRIS_OSCURO = (64, 64, 64)


class SelectorCampaniaState(State):
    """
    Menú de selección de campaña

    Permite elegir entre:
    1. Campaña Tutorial (vs Bárbaros) - 9 niveles de entrenamiento
    2. César en la Galia (vs Galos) - 9 capítulos históricos
    """

    def __init__(self, game, es_continuar=False):
        """
        Inicializa el selector de campañas

        Args:
            game: Instancia del juego
            es_continuar: Si True, intenta cargar partidas guardadas
        """
        super().__init__(game)
        self.es_continuar = es_continuar

        # Configuración de campañas disponibles
        self.campanias = [
            {
                'id': 'tutorial',
                'nombre': 'CAMPAÑA TUTORIAL',
                'subtitulo': 'Legiones vs Bárbaros',
                'descripcion': [
                    'Aprende las mecánicas del juego',
                    '9 niveles progresivos',
                    'Desde básico hasta maestro táctico',
                    'Enemigos: Bárbaros del Norte'
                ],
                'color_principal': COLOR_ROJO_OSCURO,
                'color_secundario': COLOR_DORADO,
                'icono': '⚔',
                'dificultad': 'Progresiva',
                'niveles': 9
            },
            {
                'id': 'galia',
                'nombre': 'CÉSAR EN LA GALIA',
                'subtitulo': 'Guerras Gálicas 58-50 a.C.',
                'descripcion': [
                    'Campaña histórica de Julio César',
                    '9 capítulos épicos',
                    'De Bibracte a Alesia',
                    'Enemigos: Vercingétorix y las tribus galas'
                ],
                'color_principal': (70, 120, 70),  # Verde galo
                'color_secundario': (218, 165, 32),  # Oro
                'icono': '🛡',
                'dificultad': 'Histórica',
                'niveles': 9
            }
        ]

        self.campania_seleccionada = None
        self.hover_campania = None

        # Título del menú
        self.titulo = "SELECCIONA TU CAMPAÑA" if not es_continuar else "CONTINUAR CAMPAÑA"

        # Crear botones
        self.setup_buttons()

        # Fuentes
        self.titulo_font = pygame.font.Font(None, 64)
        self.nombre_font = pygame.font.Font(None, 48)
        self.subtitulo_font = pygame.font.Font(None, 32)
        self.desc_font = pygame.font.Font(None, 28)
        self.info_font = pygame.font.Font(None, 24)

    def setup_buttons(self):
        """Crea los botones de selección de campaña"""
        self.botones_campania = []
        self.boton_volver = None

        # Dimensiones de las tarjetas de campaña
        card_width = 450
        card_height = 400
        spacing = 80

        # Centrar horizontalmente
        total_width = len(self.campanias) * card_width + (len(self.campanias) - 1) * spacing
        start_x = (WINDOW_WIDTH - total_width) // 2
        card_y = 180

        # Crear botón para cada campaña
        for i, campania in enumerate(self.campanias):
            x = start_x + i * (card_width + spacing)

            boton = CampaniaCard(
                x=x,
                y=card_y,
                width=card_width,
                height=card_height,
                campania=campania,
                callback=lambda c=campania: self.seleccionar_campania(c)
            )
            self.botones_campania.append(boton)

        # Botón volver
        self.boton_volver = Button(
            x=WINDOW_WIDTH // 2 - 100,
            y=WINDOW_HEIGHT - 100,
            width=200,
            height=50,
            text="⬅ VOLVER",
            callback=self.volver_menu
        )

    def seleccionar_campania(self, campania):
        """
        Selecciona una campaña y va al selector de niveles

        Args:
            campania: Diccionario con información de la campaña
        """
        from src.states.nivel_selector_state import NivelSelectorState

        # Cambiar a selector de niveles con la campaña apropiada
        self.game.change_state(
            NivelSelectorState(
                self.game,
                tipo_campania=campania['id'],
                cargar_guardado=self.es_continuar
            )
        )

    def volver_menu(self):
        """Vuelve al menú principal"""
        from src.states.menu_state import MenuState
        self.game.change_state(MenuState(self.game))

    def handle_event(self, event):
        """Maneja eventos de input"""
        # Manejar botones de campaña
        for boton in self.botones_campania:
            boton.handle_event(event)

        # Manejar botón volver
        self.boton_volver.handle_event(event)

        # ESC para volver
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.volver_menu()

    def update(self, dt):
        """Actualiza el estado"""
        mouse_pos = pygame.mouse.get_pos()

        # Actualizar hover de campañas
        self.hover_campania = None
        for i, boton in enumerate(self.botones_campania):
            boton.update(mouse_pos)
            if boton.is_hovered:
                self.hover_campania = i

        # Actualizar botón volver
        self.boton_volver.update(mouse_pos)

    def render(self, screen):
        """Renderiza el menú de selección"""
        # Fondo
        screen.fill(COLOR_NEGRO)

        # Renderizar fondo decorativo
        self._render_background_decoration(screen)

        # Título
        titulo_surf = self.titulo_font.render(self.titulo, True, COLOR_DORADO)
        titulo_rect = titulo_surf.get_rect(centerx=WINDOW_WIDTH // 2, top=40)
        screen.blit(titulo_surf, titulo_rect)

        # Subtítulo
        if self.es_continuar:
            subtitulo = "Elige la campaña que deseas continuar"
        else:
            subtitulo = "¡Gloria eterna te espera, Comandante!"

        subtitulo_surf = self.subtitulo_font.render(subtitulo, True, COLOR_BLANCO)
        subtitulo_rect = subtitulo_surf.get_rect(centerx=WINDOW_WIDTH // 2, top=110)
        screen.blit(subtitulo_surf, subtitulo_rect)

        # Renderizar botones de campaña
        for boton in self.botones_campania:
            boton.render(screen)

        # Renderizar botón volver
        self.boton_volver.render(screen)

        # Instrucciones
        instrucciones = "Click en una campaña para comenzar | ESC para volver"
        instr_surf = self.info_font.render(instrucciones, True, COLOR_GRIS_OSCURO)
        instr_rect = instr_surf.get_rect(centerx=WINDOW_WIDTH // 2, bottom=WINDOW_HEIGHT - 20)
        screen.blit(instr_surf, instr_rect)

    def _render_background_decoration(self, screen):
        """Renderiza decoración de fondo temática romana"""
        # Líneas decorativas superior e inferior
        pygame.draw.line(screen, COLOR_DORADO, (100, 150), (WINDOW_WIDTH - 100, 150), 3)
        pygame.draw.line(screen, COLOR_DORADO, (100, WINDOW_HEIGHT - 130), (WINDOW_WIDTH - 100, WINDOW_HEIGHT - 130), 3)

        # Círculos decorativos en las esquinas
        for x, y in [(150, 150), (WINDOW_WIDTH - 150, 150)]:
            pygame.draw.circle(screen, COLOR_DORADO, (x, y), 8)
            pygame.draw.circle(screen, COLOR_ROJO_OSCURO, (x, y), 5)


class CampaniaCard(Button):
    """
    Tarjeta personalizada para mostrar información de campaña
    Hereda de Button para aprovechar lógica de interacción
    """

    def __init__(self, x, y, width, height, campania, callback=None):
        """
        Inicializa tarjeta de campaña

        Args:
            x, y: Posición
            width, height: Dimensiones
            campania: Diccionario con información de la campaña
            callback: Función a ejecutar al hacer click
        """
        super().__init__(x, y, width, height, "", callback)

        self.campania = campania

        # Colores personalizados por campaña
        self.normal_color = (40, 40, 40)
        self.hover_color = (60, 60, 60)
        self.pressed_color = (30, 30, 30)
        self.border_color = campania['color_principal']
        self.accent_color = campania['color_secundario']

        # Fuentes
        self.icono_font = pygame.font.Font(None, 120)
        self.nombre_font = pygame.font.Font(None, 42)
        self.subtitulo_font = pygame.font.Font(None, 28)
        self.desc_font = pygame.font.Font(None, 24)
        self.info_font = pygame.font.Font(None, 22)

    def render(self, screen):
        """Renderiza la tarjeta de campaña"""
        # Determinar color según estado
        if self.is_pressed:
            color = self.pressed_color
            border_width = 5
        elif self.is_hovered:
            color = self.hover_color
            border_width = 4
        else:
            color = self.normal_color
            border_width = 3

        # Fondo de la tarjeta
        pygame.draw.rect(screen, color, self.rect)

        # Borde con color de campaña
        pygame.draw.rect(screen, self.border_color, self.rect, border_width)

        # Borde interior decorativo
        inner_rect = self.rect.inflate(-10, -10)
        pygame.draw.rect(screen, self.accent_color, inner_rect, 1)

        # ICONO
        icono_surf = self.icono_font.render(self.campania['icono'], True, self.accent_color)
        icono_rect = icono_surf.get_rect(centerx=self.rect.centerx, top=self.rect.top + 30)
        screen.blit(icono_surf, icono_rect)

        # NOMBRE DE LA CAMPAÑA
        nombre_surf = self.nombre_font.render(self.campania['nombre'], True, self.accent_color)
        nombre_rect = nombre_surf.get_rect(centerx=self.rect.centerx, top=icono_rect.bottom + 20)
        screen.blit(nombre_surf, nombre_rect)

        # SUBTÍTULO
        subtitulo_surf = self.subtitulo_font.render(self.campania['subtitulo'], True, COLOR_BLANCO)
        subtitulo_rect = subtitulo_surf.get_rect(centerx=self.rect.centerx, top=nombre_rect.bottom + 10)
        screen.blit(subtitulo_surf, subtitulo_rect)

        # LÍNEA SEPARADORA
        line_y = subtitulo_rect.bottom + 15
        pygame.draw.line(
            screen,
            self.border_color,
            (self.rect.left + 40, line_y),
            (self.rect.right - 40, line_y),
            2
        )

        # DESCRIPCIÓN (4 líneas)
        current_y = line_y + 20
        for linea in self.campania['descripcion']:
            desc_surf = self.desc_font.render(linea, True, COLOR_BLANCO)
            desc_rect = desc_surf.get_rect(centerx=self.rect.centerx, top=current_y)
            screen.blit(desc_surf, desc_rect)
            current_y += 28

        # INFORMACIÓN ADICIONAL (en la parte inferior)
        current_y = self.rect.bottom - 60

        # Dificultad
        dif_text = f"Dificultad: {self.campania['dificultad']}"
        dif_surf = self.info_font.render(dif_text, True, self.accent_color)
        dif_rect = dif_surf.get_rect(centerx=self.rect.centerx, top=current_y)
        screen.blit(dif_surf, dif_rect)

        # Niveles
        niv_text = f"{self.campania['niveles']} Capítulos"
        niv_surf = self.info_font.render(niv_text, True, COLOR_BLANCO)
        niv_rect = niv_surf.get_rect(centerx=self.rect.centerx, top=current_y + 25)
        screen.blit(niv_surf, niv_rect)

        # Efecto de brillo en hover
        if self.is_hovered:
            # Overlay semi-transparente
            overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            overlay.fill((*self.accent_color, 20))  # Alpha = 20
            screen.blit(overlay, self.rect.topleft)
