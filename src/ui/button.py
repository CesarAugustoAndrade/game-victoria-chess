"""
Button UI component
"""

import pygame

class Button:
    """Clickable button UI element"""

    def __init__(self, x, y, width, height, text, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

        # Colors
        self.normal_color = (70, 70, 70)
        self.hover_color = (100, 100, 100)
        self.pressed_color = (50, 50, 50)
        self.text_color = (255, 255, 255)

        # State
        self.is_hovered = False
        self.is_pressed = False

        # Font
        self.font = pygame.font.Font(None, 32)

    def handle_event(self, event):
        """Handle button events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:
                self.is_pressed = False
                if self.rect.collidepoint(event.pos) and self.callback:
                    self.callback()

    def update(self, mouse_pos):
        """Update button state"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if not pygame.mouse.get_pressed()[0]:
            self.is_pressed = False

    def render(self, screen):
        """Render the button"""
        # Determine color based on state
        if self.is_pressed:
            color = self.pressed_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.normal_color

        # Draw button background
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.text_color, self.rect, 2)

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)