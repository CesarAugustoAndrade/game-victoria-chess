"""
Main menu state
"""

import pygame
from src.core.state import State
from src.ui.button import Button
from src.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from src.utils.save_manager import save_manager

class MenuState(State):
    """Main menu state with buttons for game options"""

    def __init__(self, game):
        super().__init__(game)
        self.buttons = []
        self.title_font = pygame.font.Font(None, 72)
        self.save_exists = save_manager.save_exists()
        self.setup_buttons()

    def setup_buttons(self):
        """Create menu buttons"""
        button_width = 220
        button_height = 50
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        start_y = WINDOW_HEIGHT // 2 - 80

        # Botón Continuar Campaña (solo si existe guardado)
        if self.save_exists:
            self.buttons.append(
                Button(
                    button_x, start_y,
                    button_width, button_height,
                    "Continuar Campaña",
                    self.continue_campaign
                )
            )
            start_y += 70

        # Nueva Campaña / Campaña (según si existe guardado)
        campaign_text = "Nueva Campaña" if self.save_exists else "Campaña"
        self.buttons.append(
            Button(
                button_x, start_y,
                button_width, button_height,
                campaign_text,
                self.new_campaign
            )
        )

        # Quick Battle button (batalla rápida con ejércitos completos)
        self.buttons.append(
            Button(
                button_x, start_y + 70,
                button_width, button_height,
                "Batalla Rápida",
                self.start_quick_battle
            )
        )

        # Settings button
        self.buttons.append(
            Button(
                button_x, start_y + 140,
                button_width, button_height,
                "Opciones",
                self.open_settings
            )
        )

        # Exit button
        self.buttons.append(
            Button(
                button_x, start_y + 210,
                button_width, button_height,
                "Salir",
                self.exit_game
            )
        )

    def continue_campaign(self):
        """Continúa la campaña cargando el progreso guardado"""
        from src.states.selector_campania_state import SelectorCampaniaState
        self.game.change_state(SelectorCampaniaState(self.game, es_continuar=True))

    def new_campaign(self):
        """Inicia una nueva campaña (permite elegir entre Tutorial o César)"""
        from src.states.selector_campania_state import SelectorCampaniaState
        # ARREGLO: NO borrar guardados - permitir múltiples campañas en paralelo
        # El usuario puede tener progreso en Tutorial Y en César simultáneamente
        self.game.change_state(SelectorCampaniaState(self.game, es_continuar=False))

    def start_quick_battle(self):
        """Inicia una batalla rápida con ejércitos completos"""
        from src.states.batalla_state import BatallaState
        self.game.change_state(BatallaState(self.game))

    def open_settings(self):
        """Open settings menu"""
        from src.states.settings_state import SettingsState
        self.game.change_state(SettingsState(self.game))

    def exit_game(self):
        """Exit the game"""
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def handle_event(self, event):
        """Handle menu events"""
        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt):
        """Update menu state"""
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)

    def render(self, screen):
        """Render the menu"""
        # Draw title
        title_text = self.title_font.render("LEGIO ROMANA", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)

        # Subtítulo
        subtitle_font = pygame.font.Font(None, 36)
        subtitle_text = subtitle_font.render("Batalla Táctica", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
        screen.blit(subtitle_text, subtitle_rect)

        # Draw buttons
        for button in self.buttons:
            button.render(screen)