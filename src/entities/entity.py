"""
Base entity class for all game objects
"""

import pygame

class Entity:
    """Base class for all game entities"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.active = True

    def update(self, dt):
        """Update entity logic"""
        pass

    def render(self, screen, camera):
        """Render the entity"""
        pass

    def get_rect(self):
        """Get the entity's bounding rectangle"""
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )

    def contains_point(self, point):
        """Check if a point is inside the entity"""
        rect = self.get_rect()
        return rect.collidepoint(point)