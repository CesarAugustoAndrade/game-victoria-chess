"""
Base state class for all game states
"""

class State:
    """Abstract base class for game states"""

    def __init__(self, game):
        self.game = game

    def on_enter(self):
        """Called when the state becomes active"""
        pass

    def on_exit(self):
        """Called when the state is being removed"""
        pass

    def on_pause(self):
        """Called when another state is pushed on top"""
        pass

    def on_resume(self):
        """Called when the state becomes active again after being paused"""
        pass

    def handle_event(self, event):
        """Handle pygame events"""
        pass

    def update(self, dt):
        """Update the state logic"""
        pass

    def render(self, screen):
        """Render the state"""
        pass