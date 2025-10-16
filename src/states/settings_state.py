"""
Estado de configuración del juego
"""

import pygame
from src.core.state import State
from src.ui.button import Button
from src.utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    WHITE, BLACK, RED, GREEN, GRAY, YELLOW
)


class SettingsState(State):
    """Estado para configurar opciones del juego"""

    def __init__(self, game):
        super().__init__(game)
        self.font_title = pygame.font.Font(None, 72)
        self.font_normal = pygame.font.Font(None, 48)
        self.font_description = pygame.font.Font(None, 32)

        # Dificultades disponibles
        self.dificultades = [
            {
                'id': 'facil',
                'nombre': 'FÁCIL',
                'descripcion': 'IA Defensiva - Cautelosa',
                'color': GREEN
            },
            {
                'id': 'normal',
                'nombre': 'NORMAL',
                'descripcion': 'IA Agresiva - Sin piedad',
                'color': YELLOW
            },
            {
                'id': 'dificil',
                'nombre': 'DIFÍCIL',
                'descripcion': 'IA Táctica - Estrategia avanzada',
                'color': RED
            }
        ]

        # Dificultad seleccionada (por defecto normal)
        self.dificultad_actual = getattr(game, 'dificultad', 'normal')

        # Crear botones de dificultad
        self.botones_dificultad = []
        start_y = 240  # Empezar más arriba
        button_spacing = 110  # Menos espacio entre botones
        for i, dif in enumerate(self.dificultades):
            btn = Button(
                WINDOW_WIDTH // 2 - 200,
                start_y + i * button_spacing,
                400,
                60,  # Botones más pequeños
                dif['nombre'],
                self._crear_callback_dificultad(dif['id'])
            )
            # Color del botón según dificultad
            btn.normal_color = dif['color']
            btn.hover_color = tuple(min(255, c + 30) for c in dif['color'])
            btn.pressed_color = tuple(max(0, c - 30) for c in dif['color'])
            self.botones_dificultad.append(btn)

        # Botón de volver - más abajo para evitar solapamiento
        self.btn_volver = Button(
            WINDOW_WIDTH // 2 - 100,
            WINDOW_HEIGHT - 80,  # Más cerca del borde inferior
            200,
            50,  # Botón más pequeño
            "VOLVER",
            self.volver_al_menu
        )
        self.btn_volver.normal_color = GRAY
        self.btn_volver.hover_color = (150, 150, 150)

    def _crear_callback_dificultad(self, dificultad_id):
        """Crea un callback para cambiar la dificultad"""
        def callback():
            self.dificultad_actual = dificultad_id
            # Guardar en el game para que persista
            self.game.dificultad = dificultad_id
            print(f"Dificultad cambiada a: {dificultad_id}")
        return callback

    def volver_al_menu(self):
        """Vuelve al menú principal"""
        from src.states.menu_state import MenuState
        self.game.change_state(MenuState(self.game))

    def handle_event(self, event):
        """Maneja eventos"""
        # Manejar botones de dificultad
        for btn in self.botones_dificultad:
            btn.handle_event(event)

        # Manejar botón de volver
        self.btn_volver.handle_event(event)

        # ESC para volver
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.volver_al_menu()

    def update(self, dt):
        """Actualiza el estado"""
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.botones_dificultad:
            btn.update(mouse_pos)
        self.btn_volver.update(mouse_pos)

    def render(self, screen):
        """Renderiza la pantalla de configuración"""
        # Fondo degradado romano
        for i in range(WINDOW_HEIGHT):
            color_value = 20 + i * 0.02
            color = (min(60, color_value), min(30, color_value/2), min(20, color_value/3))
            pygame.draw.line(screen, color, (0, i), (WINDOW_WIDTH, i))

        # Título
        title_text = self.font_title.render("CONFIGURACIÓN", True, (255, 215, 0))
        title_rect = title_text.get_rect(centerx=WINDOW_WIDTH // 2, y=50)
        screen.blit(title_text, title_rect)

        # Subtítulo de dificultad
        subtitle_text = self.font_normal.render("Selecciona Dificultad", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(centerx=WINDOW_WIDTH // 2, y=150)
        screen.blit(subtitle_text, subtitle_rect)

        # Renderizar botones y descripciones
        for i, (btn, dif) in enumerate(zip(self.botones_dificultad, self.dificultades)):
            # Resaltar si está seleccionado
            if dif['id'] == self.dificultad_actual:
                # Dibujar marco dorado alrededor del botón seleccionado
                pygame.draw.rect(
                    screen,
                    (255, 215, 0),  # Dorado
                    (btn.rect.x - 5, btn.rect.y - 5, btn.rect.width + 10, btn.rect.height + 10),
                    3
                )

                # Indicador de selección
                check_text = self.font_normal.render("✓", True, (255, 215, 0))
                check_rect = check_text.get_rect(
                    centery=btn.rect.y + btn.rect.height // 2,
                    x=btn.rect.x - 50
                )
                screen.blit(check_text, check_rect)

            # Renderizar botón
            btn.render(screen)

            # Renderizar descripción debajo del botón
            desc_text = self.font_description.render(
                dif['descripcion'],
                True,
                (200, 200, 200)
            )
            desc_rect = desc_text.get_rect(
                centerx=WINDOW_WIDTH // 2,
                y=btn.rect.y + btn.rect.height + 5  # Menos espacio después del botón
            )
            screen.blit(desc_text, desc_rect)

        # Renderizar botón de volver
        self.btn_volver.render(screen)

        # Decoración romana
        self._renderizar_decoracion_romana(screen)

    def _renderizar_decoracion_romana(self, screen):
        """Añade decoración temática romana"""
        # Columnas decorativas a los lados
        column_color = (139, 90, 43)
        column_width = 30

        # Columna izquierda
        pygame.draw.rect(screen, column_color, (20, 100, column_width, WINDOW_HEIGHT - 200))
        pygame.draw.rect(screen, (100, 60, 30), (20, 100, column_width // 3, WINDOW_HEIGHT - 200))

        # Columna derecha
        pygame.draw.rect(screen, column_color, (WINDOW_WIDTH - 50, 100, column_width, WINDOW_HEIGHT - 200))
        pygame.draw.rect(screen, (100, 60, 30), (WINDOW_WIDTH - 50, 100, column_width // 3, WINDOW_HEIGHT - 200))

        # SPQR en la parte inferior
        spqr_text = self.font_description.render("S.P.Q.R.", True, (139, 69, 19))
        spqr_rect = spqr_text.get_rect(centerx=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT - 40)
        screen.blit(spqr_text, spqr_rect)