"""
Main gameplay state
"""

import pygame
from src.core.state import State
from src.systems.map_system import MapSystem
from src.systems.entity_manager import EntityManager
from src.systems.camera import Camera
from src.ui.hud import HUD
from src.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT

class GameState(State):
    """Main gameplay state where the strategy game takes place"""

    def __init__(self, game):
        super().__init__(game)

        # Initialize game systems
        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.map_system = MapSystem(50, 50)  # 50x50 tile map
        self.entity_manager = EntityManager()
        self.hud = HUD()

        # Game state variables
        self.selected_units = []
        self.resources = {
            "gold": 1000,
            "food": 500,
            "wood": 500,
            "stone": 200
        }

        # Camera controls
        self.camera_speed = 500  # pixels per second
        self.keys_pressed = set()

    def on_enter(self):
        """Initialize the game state"""
        # Generate initial map
        self.map_system.generate_map()

        # Create some initial units for testing
        from src.entities.unit import Unit
        for i in range(5):
            unit = Unit(100 + i * 50, 200, "worker")
            self.entity_manager.add_entity(unit)

    def handle_event(self, event):
        """Handle game events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Return to menu
                from src.states.menu_state import MenuState
                self.game.change_state(MenuState(self.game))
            else:
                self.keys_pressed.add(event.key)

        elif event.type == pygame.KEYUP:
            self.keys_pressed.discard(event.key)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.handle_left_click(event.pos)
            elif event.button == 3:  # Right click
                self.handle_right_click(event.pos)

        elif event.type == pygame.MOUSEWHEEL:
            # Zoom with mouse wheel
            self.camera.adjust_zoom(event.y * 0.1)

    def handle_left_click(self, pos):
        """Handle left mouse click for selection"""
        world_pos = self.camera.screen_to_world(pos)

        # Check if clicking on UI
        if self.hud.is_point_in_ui(pos):
            self.hud.handle_click(pos)
            return

        # Select units
        self.selected_units = self.entity_manager.get_units_at(world_pos)

    def handle_right_click(self, pos):
        """Handle right mouse click for commands"""
        if not self.selected_units:
            return

        world_pos = self.camera.screen_to_world(pos)

        # Move selected units
        for unit in self.selected_units:
            unit.move_to(world_pos)

    def update(self, dt):
        """Update game logic"""
        # Update camera based on keyboard input
        camera_dx = 0
        camera_dy = 0

        if pygame.K_LEFT in self.keys_pressed or pygame.K_a in self.keys_pressed:
            camera_dx = -self.camera_speed * dt
        if pygame.K_RIGHT in self.keys_pressed or pygame.K_d in self.keys_pressed:
            camera_dx = self.camera_speed * dt
        if pygame.K_UP in self.keys_pressed or pygame.K_w in self.keys_pressed:
            camera_dy = -self.camera_speed * dt
        if pygame.K_DOWN in self.keys_pressed or pygame.K_s in self.keys_pressed:
            camera_dy = self.camera_speed * dt

        self.camera.move(camera_dx, camera_dy)

        # Update entities
        self.entity_manager.update(dt)

        # Update HUD
        self.hud.update(self.resources, self.selected_units)

    def render(self, screen):
        """Render the game state"""
        # Create a surface for the game world
        world_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Render map
        self.map_system.render(world_surface, self.camera)

        # Render entities
        self.entity_manager.render(world_surface, self.camera)

        # Draw selection boxes
        for unit in self.selected_units:
            self.draw_selection_box(world_surface, unit)

        # Blit world to screen
        screen.blit(world_surface, (0, 0))

        # Render HUD on top
        self.hud.render(screen)

    def draw_selection_box(self, surface, unit):
        """Draw selection box around selected unit"""
        screen_pos = self.camera.world_to_screen((unit.x, unit.y))
        pygame.draw.rect(
            surface,
            (0, 255, 0),
            (screen_pos[0] - 20, screen_pos[1] - 20, 40, 40),
            2
        )