"""
Main game class that manages the game state and flow
"""

import pygame
from src.core.state_manager import StateManager
from src.states.menu_state import MenuState
from src.states.game_state import GameState
from src.systems.resource_manager import ResourceManager

class Game:
    """Main game class that coordinates all game systems"""

    def __init__(self, screen):
        self.screen = screen
        self.running = True

        # Initialize managers
        self.resource_manager = ResourceManager()
        self.state_manager = StateManager()

        # Load resources
        self.resource_manager.load_all()

        # Initialize with menu state
        self.state_manager.push_state(MenuState(self))

    def handle_event(self, event):
        """Pass events to the current state"""
        if self.state_manager.current_state:
            self.state_manager.current_state.handle_event(event)

    def update(self, dt):
        """Update the current state"""
        self.state_manager.update(dt)

    def render(self):
        """Render the current state"""
        self.screen.fill((20, 25, 40))  # Dark blue background
        self.state_manager.render(self.screen)

    def change_state(self, new_state):
        """Change the current game state"""
        self.state_manager.change_state(new_state)

    def push_state(self, state):
        """Push a new state onto the stack"""
        self.state_manager.push_state(state)

    def pop_state(self):
        """Pop the current state from the stack"""
        self.state_manager.pop_state()