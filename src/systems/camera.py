"""
Camera system for viewport management
"""

import pygame

class Camera:
    """Camera for managing the game viewport"""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.position = [0, 0]  # Top-left corner of camera in world coords
        self.zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 2.0

    def move(self, dx, dy):
        """Move the camera by a delta amount"""
        self.position[0] += dx / self.zoom
        self.position[1] += dy / self.zoom

    def set_position(self, x, y):
        """Set camera position directly"""
        self.position[0] = x
        self.position[1] = y

    def center_on(self, world_pos):
        """Center the camera on a world position"""
        self.position[0] = world_pos[0] - (self.screen_width / 2) / self.zoom
        self.position[1] = world_pos[1] - (self.screen_height / 2) / self.zoom

    def zoom_in(self):
        """Zoom in the camera"""
        self.set_zoom(self.zoom * 1.1)

    def zoom_out(self):
        """Zoom out the camera"""
        self.set_zoom(self.zoom * 0.9)

    def adjust_zoom(self, delta):
        """Adjust zoom by a delta amount"""
        new_zoom = self.zoom * (1 + delta)
        self.set_zoom(new_zoom)

    def set_zoom(self, zoom_level):
        """Set the zoom level"""
        # Store the center position before zooming
        center_x = self.position[0] + (self.screen_width / 2) / self.zoom
        center_y = self.position[1] + (self.screen_height / 2) / self.zoom

        # Apply zoom with limits
        self.zoom = max(self.min_zoom, min(self.max_zoom, zoom_level))

        # Restore center position after zooming
        self.position[0] = center_x - (self.screen_width / 2) / self.zoom
        self.position[1] = center_y - (self.screen_height / 2) / self.zoom

    def world_to_screen(self, world_pos):
        """Convert world coordinates to screen coordinates"""
        screen_x = (world_pos[0] - self.position[0]) * self.zoom
        screen_y = (world_pos[1] - self.position[1]) * self.zoom
        return (int(screen_x), int(screen_y))

    def screen_to_world(self, screen_pos):
        """Convert screen coordinates to world coordinates"""
        world_x = screen_pos[0] / self.zoom + self.position[0]
        world_y = screen_pos[1] / self.zoom + self.position[1]
        return (world_x, world_y)

    def get_visible_rect(self):
        """Get the visible rectangle in world coordinates"""
        return pygame.Rect(
            self.position[0],
            self.position[1],
            self.screen_width / self.zoom,
            self.screen_height / self.zoom
        )

    def is_visible(self, world_rect):
        """Check if a world rectangle is visible on screen"""
        visible_rect = self.get_visible_rect()
        return visible_rect.colliderect(world_rect)