"""
Game constants and configuration
"""

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
TITLE = "Strategy Simulation Game"

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Gameplay settings
DEFAULT_GAME_SPEED = 1.0
MAX_GAME_SPEED = 4.0
MIN_GAME_SPEED = 0.25

# Map settings
DEFAULT_MAP_WIDTH = 50
DEFAULT_MAP_HEIGHT = 50
TILE_SIZE = 32

# Camera settings
CAMERA_MOVE_SPEED = 500  # pixels per second
CAMERA_EDGE_SCROLL_ZONE = 50  # pixels from edge to trigger scrolling
CAMERA_MIN_ZOOM = 0.5
CAMERA_MAX_ZOOM = 2.0

# Unit settings
UNIT_MOVE_SPEED = 100  # pixels per second
UNIT_DEFAULT_HEALTH = 100
UNIT_DEFAULT_DAMAGE = 10
UNIT_SELECTION_RADIUS = 20

# Resource settings
STARTING_RESOURCES = {
    "gold": 1000,
    "food": 500,
    "wood": 500,
    "stone": 200
}

RESOURCE_GATHER_RATES = {
    "gold": 10,
    "food": 15,
    "wood": 20,
    "stone": 5
}

# Building costs
BUILDING_COSTS = {
    "house": {"wood": 50, "gold": 25},
    "barracks": {"wood": 100, "stone": 50, "gold": 150},
    "farm": {"wood": 30, "gold": 40},
    "mine": {"wood": 75, "stone": 25, "gold": 100},
    "sawmill": {"wood": 60, "stone": 20, "gold": 80}
}

# Building stats
BUILDING_HEALTH = {
    "house": 200,
    "barracks": 500,
    "farm": 150,
    "mine": 300,
    "sawmill": 250
}

# Unit costs
UNIT_COSTS = {
    "worker": {"food": 50, "gold": 30},
    "soldier": {"food": 80, "gold": 100},
    "scout": {"food": 40, "gold": 60},
    "archer": {"food": 60, "gold": 80, "wood": 30}
}

# Unit stats
UNIT_STATS = {
    "worker": {
        "health": 75,
        "speed": 80,
        "damage": 5,
        "gather_rate": 1.0
    },
    "soldier": {
        "health": 150,
        "speed": 100,
        "damage": 25,
        "armor": 5
    },
    "scout": {
        "health": 80,
        "speed": 150,
        "damage": 10,
        "sight_range": 200
    },
    "archer": {
        "health": 90,
        "speed": 90,
        "damage": 20,
        "range": 150
    }
}

# UI settings
UI_TOP_BAR_HEIGHT = 60
UI_BOTTOM_PANEL_HEIGHT = 150
UI_SIDE_PANEL_WIDTH = 200
UI_BUTTON_HEIGHT = 50
UI_MARGIN = 10

# Game states
GAME_STATE_MENU = "menu"
GAME_STATE_PLAYING = "playing"
GAME_STATE_PAUSED = "paused"
GAME_STATE_GAME_OVER = "game_over"

# Terrain types
TERRAIN_GRASS = 0
TERRAIN_FOREST = 1
TERRAIN_WATER = 2
TERRAIN_MOUNTAIN = 3
TERRAIN_SAND = 4

# Terrain movement costs (for pathfinding)
TERRAIN_MOVE_COSTS = {
    TERRAIN_GRASS: 1.0,
    TERRAIN_FOREST: 1.5,
    TERRAIN_WATER: float('inf'),  # Not walkable
    TERRAIN_MOUNTAIN: float('inf'),  # Not walkable
    TERRAIN_SAND: 1.2
}

# Debug settings
DEBUG_MODE = False
SHOW_FPS = True
SHOW_GRID = False
SHOW_PATHFINDING = False