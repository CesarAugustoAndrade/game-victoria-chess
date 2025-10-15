"""
Unit class for moveable game entities
"""

import pygame
import math
from src.entities.entity import Entity

class Unit(Entity):
    """Represents a controllable unit in the game"""

    def __init__(self, x, y, unit_type="worker"):
        super().__init__(x, y)
        self.unit_type = unit_type

        # Movement
        self.speed = 100  # pixels per second
        self.target_x = x
        self.target_y = y
        self.is_moving = False

        # Stats
        self.max_health = 100
        self.health = self.max_health
        self.attack_damage = 10
        self.attack_range = 50

        # Visual
        self.color = self.get_unit_color()
        self.radius = 15

    def get_unit_color(self):
        """Get color based on unit type"""
        colors = {
            "worker": (100, 150, 255),
            "soldier": (255, 100, 100),
            "scout": (100, 255, 100),
            "builder": (255, 200, 100)
        }
        return colors.get(self.unit_type, (200, 200, 200))

    def move_to(self, position):
        """Set a target position for the unit to move to"""
        self.target_x, self.target_y = position
        self.is_moving = True

    def stop(self):
        """Stop the unit's movement"""
        self.is_moving = False
        self.target_x = self.x
        self.target_y = self.y

    def update(self, dt):
        """Update unit state"""
        if not self.active:
            return

        # Handle movement
        if self.is_moving:
            # Calculate distance to target
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance > 5:  # Movement threshold
                # Normalize direction
                dx /= distance
                dy /= distance

                # Move towards target
                self.x += dx * self.speed * dt
                self.y += dy * self.speed * dt
            else:
                # Reached target
                self.x = self.target_x
                self.y = self.target_y
                self.is_moving = False

    def render(self, screen, camera):
        """Render the unit"""
        if not self.active:
            return

        # Convert world position to screen position
        screen_pos = camera.world_to_screen((self.x, self.y))

        # Draw unit circle
        pygame.draw.circle(
            screen,
            self.color,
            (int(screen_pos[0]), int(screen_pos[1])),
            self.radius
        )

        # Draw unit outline
        pygame.draw.circle(
            screen,
            (50, 50, 50),
            (int(screen_pos[0]), int(screen_pos[1])),
            self.radius,
            2
        )

        # Draw health bar
        if self.health < self.max_health:
            self.render_health_bar(screen, screen_pos)

    def render_health_bar(self, screen, screen_pos):
        """Render health bar above unit"""
        bar_width = 30
        bar_height = 4
        bar_x = screen_pos[0] - bar_width // 2
        bar_y = screen_pos[1] - self.radius - 10

        # Background
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (bar_x, bar_y, bar_width, bar_height)
        )

        # Health
        health_percentage = self.health / self.max_health
        health_width = int(bar_width * health_percentage)

        # Color based on health
        if health_percentage > 0.6:
            health_color = (0, 255, 0)
        elif health_percentage > 0.3:
            health_color = (255, 255, 0)
        else:
            health_color = (255, 0, 0)

        pygame.draw.rect(
            screen,
            health_color,
            (bar_x, bar_y, health_width, bar_height)
        )

    def take_damage(self, amount):
        """Apply damage to the unit"""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.active = False

    def heal(self, amount):
        """Heal the unit"""
        self.health = min(self.health + amount, self.max_health)