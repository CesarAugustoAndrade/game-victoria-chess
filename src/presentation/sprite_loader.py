"""
EPIC SPRITE LOADER SYSTEM - Load custom PNG sprites or generate them!
"""

import pygame
import os
import math
from pathlib import Path
from typing import Optional, Dict, Tuple
from src.domain.value_objects import TipoUnidad, Bando
from src.presentation.unit_sprites import UnitSpriteRenderer


class EpicSpriteLoader:
    """Ultimate sprite loading system with image support and fallback to programmatic sprites"""

    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent / "assets" / "sprites"
        self.sprite_cache: Dict[str, pygame.Surface] = {}
        self.programmatic_renderer = UnitSpriteRenderer()
        self.sprite_found_log = {}

        # Mapeo de nombres de archivo
        self.filename_map = {
            TipoUnidad.LEGIONARIO: "legionario",
            TipoUnidad.HASTATI: "hastati",
            TipoUnidad.TRIARII: "triarii",
            TipoUnidad.EQUITES: "equites",
            TipoUnidad.SAGITTARII: "sagittarii"
        }

        self.folder_map = {
            Bando.ROMA: "roman",
            Bando.BARBAROS: "barbarian"
        }

        # Inicializar sistema de sprites
        self._scan_available_sprites()

    def _scan_available_sprites(self):
        """Escanea qué sprites están disponibles como archivos"""
        try:
            print("[SPRITES] SCANNING FOR CUSTOM SPRITES...")
        except:
            pass  # Ignorar errores de encoding

        for bando, folder in self.folder_map.items():
            folder_path = self.base_path / folder
            if folder_path.exists():
                for tipo, filename in self.filename_map.items():
                    # Buscar PNG, JPG, o cualquier formato de imagen
                    for ext in ['.png', '.jpg', '.jpeg', '.gif']:
                        file_path = folder_path / f"{filename}{ext}"
                        if file_path.exists():
                            key = f"{bando.value}_{tipo.value}"
                            self.sprite_found_log[key] = str(file_path)
                            try:
                                print(f"  [OK] Found custom sprite: {file_path.name}")
                            except:
                                pass

        if not self.sprite_found_log:
            try:
                print("  [INFO] No custom sprites found - using awesome programmatic sprites!")
            except:
                pass
        else:
            try:
                print(f"  [SUCCESS] Loaded {len(self.sprite_found_log)} custom sprites!")
            except:
                pass

    def get_unit_sprite(self, tipo: TipoUnidad, bando: Bando, size: int = 60) -> pygame.Surface:
        """Get sprite from file or generate it programmatically"""
        cache_key = f"{bando.value}_{tipo.value}_{size}"

        # Check cache first
        if cache_key in self.sprite_cache:
            return self.sprite_cache[cache_key]

        # Try to load from file
        sprite_key = f"{bando.value}_{tipo.value}"
        if sprite_key in self.sprite_found_log:
            sprite = self._load_sprite_from_file(self.sprite_found_log[sprite_key], size)
            if sprite:
                self.sprite_cache[cache_key] = sprite
                return sprite

        # Fallback to programmatic sprite
        sprite = self.programmatic_renderer.get_unit_sprite(tipo, bando, size)
        self.sprite_cache[cache_key] = sprite
        return sprite

    def _load_sprite_from_file(self, file_path: str, size: int) -> Optional[pygame.Surface]:
        """Load and scale sprite from file"""
        try:
            # Load image
            original = pygame.image.load(file_path)

            # Convert with alpha channel for transparency
            original = original.convert_alpha()

            # Scale to desired size maintaining aspect ratio
            original_rect = original.get_rect()
            aspect = original_rect.width / original_rect.height

            if aspect > 1:  # Wider than tall
                new_width = size
                new_height = int(size / aspect)
            else:  # Taller than wide
                new_width = int(size * aspect)
                new_height = size

            # Scale the sprite
            scaled = pygame.transform.smoothscale(original, (new_width, new_height))

            # Create final surface with proper size and center the sprite
            final_surface = pygame.Surface((size, size), pygame.SRCALPHA)
            x = (size - new_width) // 2
            y = (size - new_height) // 2
            final_surface.blit(scaled, (x, y))

            return final_surface

        except Exception as e:
            try:
                print(f"[WARNING] Error loading sprite {file_path}: {e}")
            except:
                pass
            return None

    def reload_sprites(self):
        """Reload all sprites (useful for development)"""
        self.sprite_cache.clear()
        self.sprite_found_log.clear()
        self._scan_available_sprites()
        try:
            print("[INFO] Sprites reloaded!")
        except:
            pass


class AnimatedSprite:
    """Sprite animado para efectos especiales"""

    def __init__(self, frames: list[pygame.Surface], fps: int = 10):
        self.frames = frames
        self.fps = fps
        self.current_frame = 0
        self.time_accumulator = 0
        self.frame_duration = 1.0 / fps
        self.finished = False

    def update(self, dt: float):
        """Actualiza la animación"""
        if self.finished:
            return

        self.time_accumulator += dt

        while self.time_accumulator >= self.frame_duration:
            self.time_accumulator -= self.frame_duration
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                self.finished = True
                self.current_frame = len(self.frames) - 1

    def get_current_frame(self) -> pygame.Surface:
        """Obtiene el frame actual"""
        if self.frames:
            return self.frames[min(self.current_frame, len(self.frames) - 1)]
        return None

    def reset(self):
        """Reinicia la animación"""
        self.current_frame = 0
        self.time_accumulator = 0
        self.finished = False


class SpriteEffects:
    """Sistema de efectos visuales épicos"""

    @staticmethod
    def create_explosion(x: int, y: int, size: int = 60, color: Tuple[int, int, int] = (255, 100, 0)) -> AnimatedSprite:
        """Crea una explosión animada"""
        frames = []

        for i in range(8):
            frame = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)

            # Círculo expandiéndose
            radius = int(size * (i + 1) / 8)
            alpha = 255 - (i * 30)

            # Múltiples capas para efecto más dramático
            for layer in range(3):
                layer_radius = radius - layer * 5
                if layer_radius > 0:
                    layer_alpha = max(0, alpha - layer * 50)
                    layer_color = (*color, layer_alpha)
                    pygame.draw.circle(frame, layer_color, (size, size), layer_radius)

            # Partículas
            import random
            for _ in range(10):
                px = size + random.randint(-radius, radius)
                py = size + random.randint(-radius, radius)
                particle_size = random.randint(2, 6)
                particle_alpha = max(0, alpha - random.randint(0, 100))
                pygame.draw.circle(frame, (*color, particle_alpha), (px, py), particle_size)

            frames.append(frame)

        return AnimatedSprite(frames, fps=15)

    @staticmethod
    def create_blood_splatter(x: int, y: int, size: int = 40) -> AnimatedSprite:
        """Crea un efecto de salpicadura de sangre"""
        frames = []

        for i in range(6):
            frame = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)

            # Salpicaduras expandiéndose
            import random
            for _ in range(15):
                splat_x = size + random.randint(-size//2, size//2) * (i + 1) // 6
                splat_y = size + random.randint(-size//2, size//2) * (i + 1) // 6
                splat_size = random.randint(2, 8)
                alpha = 200 - i * 30
                color = (180 - i * 10, 0, 0, alpha)
                pygame.draw.circle(frame, color, (splat_x, splat_y), splat_size)

            frames.append(frame)

        return AnimatedSprite(frames, fps=12)

    @staticmethod
    def create_sword_slash(x: int, y: int, size: int = 80) -> AnimatedSprite:
        """Crea un efecto de corte de espada"""
        frames = []

        for i in range(5):
            frame = pygame.Surface((size, size), pygame.SRCALPHA)

            # Arco de corte
            start_angle = -0.5 + (i * 0.3)
            end_angle = start_angle + 1.5
            alpha = 255 - i * 40

            arc_rect = pygame.Rect(10, 10, size - 20, size - 20)

            # Efecto de estela
            for j in range(3):
                trail_alpha = max(0, alpha - j * 60)
                trail_color = (255, 255, 255, trail_alpha)
                trail_rect = arc_rect.inflate(-j * 5, -j * 5)
                if trail_rect.width > 0:
                    pygame.draw.arc(frame, trail_color, trail_rect, start_angle, end_angle, 3 - j)

            frames.append(frame)

        return AnimatedSprite(frames, fps=20)

    @staticmethod
    def create_shield_block(x: int, y: int, size: int = 60) -> AnimatedSprite:
        """Crea un efecto de bloqueo con escudo"""
        frames = []

        for i in range(6):
            frame = pygame.Surface((size, size), pygame.SRCALPHA)

            # Onda de impacto
            radius = 10 + i * 5
            alpha = 200 - i * 30
            color = (100, 150, 255, alpha)

            pygame.draw.circle(frame, color, (size//2, size//2), radius, 3)

            # Chispas
            import random
            for _ in range(5):
                spark_angle = random.uniform(0, 6.28)
                spark_dist = radius + random.randint(0, 10)
                spark_x = size//2 + int(spark_dist * math.cos(spark_angle))
                spark_y = size//2 + int(spark_dist * math.sin(spark_angle))
                pygame.draw.circle(frame, (255, 255, 200, alpha), (spark_x, spark_y), 2)

            frames.append(frame)

        return AnimatedSprite(frames, fps=15)


# Crear archivo de instrucciones para sprites personalizados
SPRITE_INSTRUCTIONS = """
# CÓMO AÑADIR TUS PROPIOS SPRITES

## Estructura de Carpetas:
```
assets/sprites/
├── roman/           # Sprites de unidades romanas
│   ├── legionario.png
│   ├── hastati.png
│   ├── triarii.png
│   ├── equites.png
│   └── sagittarii.png
└── barbarian/       # Sprites de unidades bárbaras
    ├── legionario.png  (guerrero)
    ├── hastati.png     (berserker)
    ├── triarii.png     (lancero)
    ├── equites.png     (jinete)
    └── sagittarii.png  (arquero)
```

## Requisitos de las Imágenes:
- **Formato**: PNG con transparencia (recomendado)
- **Tamaño**: 64x64, 128x128 o 256x256 píxeles
- **Fondo**: Transparente
- **Orientación**: Mirando hacia abajo o derecha

## Pasos para Añadir Sprites:
1. Coloca tu imagen PNG en la carpeta correcta
2. Usa el nombre de archivo exacto (ej: legionario.png)
3. El juego detectará y usará automáticamente tu sprite
4. Si no hay sprite, usará el sprite programático

## Dónde Conseguir Sprites:
- OpenGameArt.org
- Itch.io (assets gratuitos)
- Crear los tuyos con Aseprite o Piskel
- Generar con IA (DALL-E, Midjourney)

## Tips:
- Los sprites se escalan automáticamente
- Mantén proporciones cuadradas para mejor resultado
- Usa transparencia para mejor integración
"""