"""
Resource manager for loading and caching game assets
"""

import pygame
import os
from pathlib import Path

class ResourceManager:
    """Manages loading and caching of game resources"""

    def __init__(self):
        self.sprites = {}
        self.sounds = {}
        self.fonts = {}
        self.base_path = Path(__file__).parent.parent.parent  # Project root

    def load_all(self):
        """Load all game resources"""
        self.load_sprites()
        self.load_sounds()
        self.load_fonts()

    def load_sprites(self):
        """Load sprite images"""
        sprite_path = self.base_path / "assets" / "sprites"

        # Create placeholder sprites if directory doesn't exist
        if not sprite_path.exists():
            print(f"Sprite directory not found: {sprite_path}")
            self.create_placeholder_sprites()
            return

        # Load all PNG files in sprites directory
        for file in sprite_path.glob("*.png"):
            try:
                sprite_name = file.stem
                self.sprites[sprite_name] = pygame.image.load(str(file))
                print(f"Loaded sprite: {sprite_name}")
            except pygame.error as e:
                print(f"Failed to load sprite {file}: {e}")

    def create_placeholder_sprites(self):
        """Create placeholder sprites for testing"""
        # Create colored surfaces as placeholders
        placeholder_sprites = {
            "worker": (32, 32, (100, 150, 255)),
            "soldier": (32, 32, (255, 100, 100)),
            "building": (64, 64, (150, 150, 150)),
            "tree": (32, 48, (34, 139, 34)),
            "rock": (24, 24, (128, 128, 128))
        }

        for name, (width, height, color) in placeholder_sprites.items():
            surface = pygame.Surface((width, height))
            surface.fill(color)
            self.sprites[name] = surface

    def load_sounds(self):
        """Load sound effects"""
        sound_path = self.base_path / "assets" / "sounds"

        if not sound_path.exists():
            print(f"Sound directory not found: {sound_path}")
            return

        # Load all WAV files in sounds directory
        for file in sound_path.glob("*.wav"):
            try:
                sound_name = file.stem
                self.sounds[sound_name] = pygame.mixer.Sound(str(file))
                print(f"Loaded sound: {sound_name}")
            except pygame.error as e:
                print(f"Failed to load sound {file}: {e}")

    def load_fonts(self):
        """Load custom fonts"""
        font_path = self.base_path / "assets" / "fonts"

        # Load default system fonts
        self.fonts["default"] = pygame.font.Font(None, 24)
        self.fonts["large"] = pygame.font.Font(None, 48)
        self.fonts["small"] = pygame.font.Font(None, 16)

        if not font_path.exists():
            print(f"Font directory not found: {font_path}")
            return

        # Load TTF files if they exist
        for file in font_path.glob("*.ttf"):
            try:
                font_name = file.stem
                # Load font in multiple sizes
                self.fonts[f"{font_name}_small"] = pygame.font.Font(str(file), 16)
                self.fonts[f"{font_name}_medium"] = pygame.font.Font(str(file), 24)
                self.fonts[f"{font_name}_large"] = pygame.font.Font(str(file), 48)
                print(f"Loaded font: {font_name}")
            except pygame.error as e:
                print(f"Failed to load font {file}: {e}")

    def get_sprite(self, name):
        """Get a sprite by name"""
        if name in self.sprites:
            return self.sprites[name]
        else:
            print(f"Sprite not found: {name}")
            # Return a placeholder surface
            placeholder = pygame.Surface((32, 32))
            placeholder.fill((255, 0, 255))  # Magenta for missing sprites
            return placeholder

    def get_sound(self, name):
        """Get a sound by name"""
        if name in self.sounds:
            return self.sounds[name]
        else:
            print(f"Sound not found: {name}")
            return None

    def get_font(self, name="default"):
        """Get a font by name"""
        if name in self.fonts:
            return self.fonts[name]
        else:
            print(f"Font not found: {name}, using default")
            return self.fonts.get("default", pygame.font.Font(None, 24))

    def play_sound(self, name, volume=0.5):
        """Play a sound effect"""
        sound = self.get_sound(name)
        if sound:
            sound.set_volume(volume)
            sound.play()

    def clear(self):
        """Clear all loaded resources"""
        self.sprites.clear()
        self.sounds.clear()
        self.fonts.clear()