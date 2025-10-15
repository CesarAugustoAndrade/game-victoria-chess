"""
Map system for tile-based game world
"""

import pygame
import random
from enum import Enum

class TileType(Enum):
    """Enumeration of tile types"""
    GRASS = 0
    FOREST = 1
    WATER = 2
    MOUNTAIN = 3
    SAND = 4

class Tile:
    """Individual map tile"""

    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.walkable = tile_type not in [TileType.WATER, TileType.MOUNTAIN]
        self.building = None
        self.resource = None

    def get_color(self):
        """Get the display color for this tile"""
        colors = {
            TileType.GRASS: (34, 139, 34),
            TileType.FOREST: (0, 100, 0),
            TileType.WATER: (64, 164, 223),
            TileType.MOUNTAIN: (139, 137, 137),
            TileType.SAND: (238, 203, 173)
        }
        return colors.get(self.tile_type, (100, 100, 100))

class MapSystem:
    """Manages the game map and tiles"""

    def __init__(self, width, height, tile_size=32):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tiles = []

        # Initialize empty map
        self.clear_map()

    def clear_map(self):
        """Clear the map and create empty tiles"""
        self.tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Tile(x, y, TileType.GRASS))
            self.tiles.append(row)

    def generate_map(self):
        """Generate a random map with various terrain types"""
        # Start with grass base
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x] = Tile(x, y, TileType.GRASS)

        # Add forests
        self.generate_patches(TileType.FOREST, 8, 3, 7)

        # Add water bodies
        self.generate_patches(TileType.WATER, 3, 4, 8)

        # Add mountains
        self.generate_patches(TileType.MOUNTAIN, 4, 2, 5)

        # Add sand near water
        self.generate_sand_beaches()

    def generate_patches(self, tile_type, num_patches, min_size, max_size):
        """Generate patches of a specific tile type"""
        for _ in range(num_patches):
            # Random starting position
            start_x = random.randint(0, self.width - 1)
            start_y = random.randint(0, self.height - 1)

            # Patch size
            size = random.randint(min_size, max_size)

            # Grow patch from starting position
            to_process = [(start_x, start_y)]
            processed = set()

            while to_process and len(processed) < size * size:
                x, y = to_process.pop(0)

                if (x, y) in processed:
                    continue

                if 0 <= x < self.width and 0 <= y < self.height:
                    self.tiles[y][x].tile_type = tile_type
                    self.tiles[y][x].walkable = tile_type not in [TileType.WATER, TileType.MOUNTAIN]
                    processed.add((x, y))

                    # Add neighbors with some randomness
                    if random.random() > 0.3:
                        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                            new_x, new_y = x + dx, y + dy
                            if (new_x, new_y) not in processed:
                                to_process.append((new_x, new_y))

    def generate_sand_beaches(self):
        """Generate sand tiles near water"""
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[y][x].tile_type == TileType.GRASS:
                    # Check if adjacent to water
                    if self.is_adjacent_to_type(x, y, TileType.WATER):
                        if random.random() > 0.5:
                            self.tiles[y][x].tile_type = TileType.SAND

    def is_adjacent_to_type(self, x, y, tile_type):
        """Check if a tile is adjacent to a specific type"""
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.tiles[ny][nx].tile_type == tile_type:
                    return True
        return False

    def get_tile(self, x, y):
        """Get tile at specific coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    def world_to_tile(self, world_pos):
        """Convert world coordinates to tile coordinates"""
        tile_x = int(world_pos[0] // self.tile_size)
        tile_y = int(world_pos[1] // self.tile_size)
        return (tile_x, tile_y)

    def tile_to_world(self, tile_pos):
        """Convert tile coordinates to world coordinates"""
        world_x = tile_pos[0] * self.tile_size + self.tile_size // 2
        world_y = tile_pos[1] * self.tile_size + self.tile_size // 2
        return (world_x, world_y)

    def is_walkable(self, x, y):
        """Check if a tile is walkable"""
        tile = self.get_tile(x, y)
        return tile is not None and tile.walkable

    def render(self, screen, camera):
        """Render the visible portion of the map"""
        # Calculate visible tile range
        screen_width, screen_height = screen.get_size()

        # Get camera bounds in world coordinates
        cam_left, cam_top = camera.position
        cam_right = cam_left + screen_width / camera.zoom
        cam_bottom = cam_top + screen_height / camera.zoom

        # Convert to tile coordinates
        start_x = max(0, int(cam_left // self.tile_size))
        start_y = max(0, int(cam_top // self.tile_size))
        end_x = min(self.width, int(cam_right // self.tile_size) + 2)
        end_y = min(self.height, int(cam_bottom // self.tile_size) + 2)

        # Render visible tiles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.tiles[y][x]

                # Calculate screen position
                world_x = x * self.tile_size
                world_y = y * self.tile_size
                screen_pos = camera.world_to_screen((world_x, world_y))

                # Calculate tile size on screen
                tile_screen_size = int(self.tile_size * camera.zoom)

                # Draw tile
                tile_rect = pygame.Rect(
                    screen_pos[0],
                    screen_pos[1],
                    tile_screen_size + 1,  # +1 to avoid gaps
                    tile_screen_size + 1
                )

                pygame.draw.rect(screen, tile.get_color(), tile_rect)

                # Optional: Draw grid lines for debugging
                if camera.zoom > 0.5:  # Only show grid when zoomed in
                    pygame.draw.rect(screen, (50, 50, 50), tile_rect, 1)