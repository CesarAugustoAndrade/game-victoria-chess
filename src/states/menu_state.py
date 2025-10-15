"""
Main menu state
"""

import pygame
from src.core.state import State
from src.ui.button import Button
from src.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT

class MenuState(State):
    """Main menu state with buttons for game options"""

    def __init__(self, game):
        super().__init__(game)
        self.buttons = []
        self.title_font = pygame.font.Font(None, 72)
        self.setup_buttons()

    def setup_buttons(self):
        """Create menu buttons"""
        button_width = 200
        button_height = 50
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        start_y = WINDOW_HEIGHT // 2

        # New Game button
        self.buttons.append(
            Button(
                button_x, start_y,
                button_width, button_height,
                "New Game",
                self.start_game
            )
        )

        # Settings button
        self.buttons.append(
            Button(
                button_x, start_y + 70,
                button_width, button_height,
                "Settings",
                self.open_settings
            )
        )

        # Exit button
        self.buttons.append(
            Button(
                button_x, start_y + 140,
                button_width, button_height,
                "Exit",
                self.exit_game
            )
        )

    def start_game(self):
        """Start a new game"""
        from src.states.game_state import GameState
        self.game.change_state(GameState(self.game))

    def open_settings(self):
        """Open settings menu"""
        print("Settings not implemented yet")

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
        title_text = self.title_font.render("Strategy Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)

        # Draw buttons
        for button in self.buttons:
            button.render(screen)