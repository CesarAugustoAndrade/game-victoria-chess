"""
Strategy/Simulation Game
Main entry point for the game
"""

import pygame
import sys
from src.core.game import Game
from src.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE

def main():
    """Main entry point for the game"""
    pygame.init()
    pygame.display.set_caption(TITLE)

    # Create the game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Initialize the game
    game = Game(screen)

    # Game loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        # Update game state
        game.update(dt)

        # Render
        game.render()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()