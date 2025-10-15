"""
Heads-up display for game interface
"""

import pygame
from src.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT

class HUD:
    """HUD displaying game information and controls"""

    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 32)

        # UI areas
        self.top_bar_height = 60
        self.bottom_panel_height = 150

        # Colors
        self.bg_color = (40, 40, 50)
        self.border_color = (80, 80, 90)
        self.text_color = (255, 255, 255)
        self.resource_colors = {
            "gold": (255, 215, 0),
            "food": (139, 69, 19),
            "wood": (101, 67, 33),
            "stone": (128, 128, 128)
        }

        # Current data
        self.resources = {}
        self.selected_units = []

    def is_point_in_ui(self, pos):
        """Check if a point is within UI elements"""
        x, y = pos
        # Check top bar
        if y < self.top_bar_height:
            return True
        # Check bottom panel
        if y > WINDOW_HEIGHT - self.bottom_panel_height:
            return True
        return False

    def handle_click(self, pos):
        """Handle clicks on UI elements"""
        # Add button handling here as needed
        pass

    def update(self, resources, selected_units):
        """Update HUD data"""
        self.resources = resources
        self.selected_units = selected_units

    def render(self, screen):
        """Render the HUD"""
        self.render_top_bar(screen)
        self.render_bottom_panel(screen)

    def render_top_bar(self, screen):
        """Render top resource bar"""
        # Draw background
        top_rect = pygame.Rect(0, 0, WINDOW_WIDTH, self.top_bar_height)
        pygame.draw.rect(screen, self.bg_color, top_rect)
        pygame.draw.rect(screen, self.border_color, top_rect, 2)

        # Draw resources
        x_offset = 20
        for resource, amount in self.resources.items():
            # Resource name
            color = self.resource_colors.get(resource, self.text_color)
            text = self.font.render(f"{resource.capitalize()}:", True, color)
            screen.blit(text, (x_offset, 10))

            # Resource amount
            amount_text = self.font.render(str(amount), True, self.text_color)
            screen.blit(amount_text, (x_offset, 30))

            x_offset += 120

        # Draw game time or other info on the right
        time_text = self.font.render("Day 1", True, self.text_color)
        time_rect = time_text.get_rect(right=WINDOW_WIDTH - 20, centery=30)
        screen.blit(time_text, time_rect)

    def render_bottom_panel(self, screen):
        """Render bottom control panel"""
        # Draw background
        bottom_rect = pygame.Rect(
            0,
            WINDOW_HEIGHT - self.bottom_panel_height,
            WINDOW_WIDTH,
            self.bottom_panel_height
        )
        pygame.draw.rect(screen, self.bg_color, bottom_rect)
        pygame.draw.rect(screen, self.border_color, bottom_rect, 2)

        # Draw selected unit info
        if self.selected_units:
            y_offset = WINDOW_HEIGHT - self.bottom_panel_height + 10

            # Selection count
            count_text = self.large_font.render(
                f"Selected: {len(self.selected_units)} unit(s)",
                True,
                self.text_color
            )
            screen.blit(count_text, (20, y_offset))

            # Unit details
            if len(self.selected_units) == 1:
                unit = self.selected_units[0]
                y_offset += 40

                # Unit type
                type_text = self.font.render(
                    f"Type: {unit.unit_type}",
                    True,
                    self.text_color
                )
                screen.blit(type_text, (20, y_offset))

                # Unit health
                y_offset += 25
                health_text = self.font.render(
                    f"Health: {unit.health}/{unit.max_health}",
                    True,
                    self.text_color
                )
                screen.blit(health_text, (20, y_offset))

        else:
            # No selection message
            no_selection_text = self.font.render(
                "No units selected",
                True,
                (150, 150, 150)
            )
            screen.blit(
                no_selection_text,
                (20, WINDOW_HEIGHT - self.bottom_panel_height + 20)
            )

        # Draw action buttons (placeholder)
        self.render_action_buttons(screen)

    def render_action_buttons(self, screen):
        """Render action buttons in the bottom panel"""
        # This is where you'd add buttons for unit actions, building, etc.
        button_size = 50
        button_margin = 10
        start_x = WINDOW_WIDTH - (button_size + button_margin) * 4
        start_y = WINDOW_HEIGHT - self.bottom_panel_height + 20

        # Example action buttons (just visual for now)
        actions = ["Build", "Move", "Attack", "Stop"]
        for i, action in enumerate(actions):
            button_rect = pygame.Rect(
                start_x + i * (button_size + button_margin),
                start_y,
                button_size,
                button_size
            )
            pygame.draw.rect(screen, (60, 60, 70), button_rect)
            pygame.draw.rect(screen, self.border_color, button_rect, 2)

            # Draw action label
            action_text = self.font.render(action[0], True, self.text_color)
            text_rect = action_text.get_rect(center=button_rect.center)
            screen.blit(action_text, text_rect)