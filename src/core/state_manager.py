"""
State manager for handling different game states
"""

class StateManager:
    """Manages game states using a stack-based approach"""

    def __init__(self):
        self.states = []
        self.current_state = None

    def push_state(self, state):
        """Push a new state onto the stack"""
        if self.current_state:
            self.current_state.on_pause()
        self.states.append(state)
        self.current_state = state
        self.current_state.on_enter()

    def pop_state(self):
        """Pop the current state from the stack"""
        if self.states:
            leaving_state = self.states.pop()
            leaving_state.on_exit()

            if self.states:
                self.current_state = self.states[-1]
                self.current_state.on_resume()
            else:
                self.current_state = None

    def change_state(self, new_state):
        """Replace the current state with a new one"""
        if self.states:
            self.states[-1].on_exit()
            self.states[-1] = new_state
            self.current_state = new_state
            new_state.on_enter()

    def update(self, dt):
        """Update the current state"""
        if self.current_state:
            self.current_state.update(dt)

    def render(self, screen):
        """Render the current state"""
        if self.current_state:
            self.current_state.render(screen)