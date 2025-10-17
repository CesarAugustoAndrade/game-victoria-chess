"""
EPIC SOUND SYSTEM - Roman Battle Sounds & Music!
"""

import pygame
import random
from pathlib import Path
from typing import Optional, Dict
from src.domain.value_objects import TipoUnidad


class EpicSoundSystem:
    """Sistema de sonido épico para batallas romanas"""

    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_tracks: Dict[str, str] = {}
        self.base_path = Path(__file__).parent.parent.parent / "assets" / "sounds"

        # Volúmenes
        self.sfx_volume = 0.7
        self.music_volume = 0.5
        self.voice_volume = 0.8

        # Estado
        self.music_playing = False
        self.current_music = None

        # Cargar sonidos si existen
        self._load_sounds()

        # Si no hay archivos, crear sonidos sintéticos
        if not self.sounds:
            self._create_synthetic_sounds()

    def _load_sounds(self):
        """Carga archivos de sonido si existen"""
        effects_path = self.base_path / "effects"

        if effects_path.exists():
            # Sonidos de combate
            sound_files = {
                "sword_hit": ["sword_hit.wav", "sword_hit.ogg", "hit.wav"],
                "arrow_shot": ["arrow.wav", "bow.wav", "arrow_shot.wav"],
                "horse_gallop": ["horse.wav", "gallop.wav"],
                "shield_block": ["shield.wav", "block.wav"],
                "death_scream": ["death.wav", "scream.wav"],
                "march": ["march.wav", "footsteps.wav"],
                "horn": ["horn.wav", "warhorn.wav"],
                "battle_cry": ["warcry.wav", "shout.wav"]
            }

            for sound_name, possible_files in sound_files.items():
                for filename in possible_files:
                    file_path = effects_path / filename
                    if file_path.exists():
                        try:
                            self.sounds[sound_name] = pygame.mixer.Sound(str(file_path))
                            self.sounds[sound_name].set_volume(self.sfx_volume)
                            pass  # Silenciosamente cargado
                            break
                        except:
                            pass

        # Música
        music_path = self.base_path / "music"
        if music_path.exists():
            music_files = {
                "menu": "menu_theme",
                "battle": "battle_theme",
                "victory": "victory_theme",
                "defeat": "defeat_theme"
            }

            for music_name, base_name in music_files.items():
                for ext in [".mp3", ".ogg", ".wav"]:
                    file_path = music_path / f"{base_name}{ext}"
                    if file_path.exists():
                        self.music_tracks[music_name] = str(file_path)
                        pass  # Música cargada
                        break

    def _create_synthetic_sounds(self):
        """Crea sonidos sintéticos si no hay archivos"""
        print("[SOUND] Creating synthetic battle sounds...")

        # Generar tonos sintéticos para efectos
        sample_rate = 22050
        duration = 0.2
        num_samples = int(sample_rate * duration)

        # Sonido de espada (ruido blanco + tono bajo) - Crear en estéreo
        sword_samples = []
        for i in range(num_samples):
            t = i / sample_rate
            # Tono bajo decayendo
            tone = int(1000 * pygame.math.Vector2(1, 0).rotate(440 * t * 360).x * (1 - t/duration))
            # Añadir ruido
            noise = random.randint(-500, 500)
            value = max(-32768, min(32767, tone + noise))
            # Añadir canal izquierdo y derecho (estéreo)
            sword_samples.append([value, value])

        import numpy as np
        sword_array = np.array(sword_samples, dtype=np.int16)
        self.sounds["sword_hit"] = pygame.sndarray.make_sound(sword_array)

    def play_battle_sound(self, sound_type: str, position: Optional[tuple] = None):
        """Reproduce un sonido de batalla"""
        if sound_type in self.sounds:
            sound = self.sounds[sound_type]

            # Ajustar volumen basado en posición (si se proporciona)
            if position:
                # Calcular distancia del centro
                center_x, center_y = 640, 360
                dist_x = abs(position[0] - center_x) / 640
                dist_y = abs(position[1] - center_y) / 360
                distance_factor = max(0.3, 1 - (dist_x + dist_y) / 2)

                # Ajustar panorama (estéreo)
                pan = (position[0] - center_x) / 640

                channel = sound.play()
                if channel:
                    channel.set_volume(
                        self.sfx_volume * distance_factor * (1 - pan * 0.5),  # Left
                        self.sfx_volume * distance_factor * (1 + pan * 0.5)   # Right
                    )
            else:
                sound.play()

    def play_unit_sound(self, unit_type: TipoUnidad, action: str):
        """Reproduce sonido específico de unidad"""
        sound_map = {
            TipoUnidad.LEGIONARIO: {
                "attack": "sword_hit",
                "move": "march",
                "death": "death_scream"
            },
            TipoUnidad.HASTATI: {
                "attack": "sword_hit",
                "move": "march",
                "death": "death_scream"
            },
            TipoUnidad.TRIARII: {
                "attack": "spear_thrust",
                "move": "march",
                "death": "death_scream"
            },
            TipoUnidad.EQUITES: {
                "attack": "sword_hit",
                "move": "horse_gallop",
                "death": "horse_neigh"
            },
            TipoUnidad.SAGITTARII: {
                "attack": "arrow_shot",
                "move": "march",
                "death": "death_scream"
            }
        }

        if unit_type in sound_map and action in sound_map[unit_type]:
            self.play_battle_sound(sound_map[unit_type][action])

    def play_war_cry(self, is_roman: bool = True):
        """Reproduce grito de guerra"""
        if is_roman:
            # Gritos romanos en orden de preferencia
            cries = ["roma_invicta", "battle_cry", "horn"]
        else:
            # Gritos bárbaros
            cries = ["barbarian_cry", "battle_cry"]

        for cry in cries:
            if cry in self.sounds:
                self.sounds[cry].play()
                break

    def play_music(self, track_name: str, loops: int = -1):
        """Reproduce música de fondo"""
        if track_name in self.music_tracks:
            try:
                pygame.mixer.music.load(self.music_tracks[track_name])
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loops)
                self.music_playing = True
                self.current_music = track_name
                print(f"[MUSIC] Playing music: {track_name}")
            except:
                print(f"[WARNING] Could not play music: {track_name}")

    def stop_music(self, fade_out_ms: int = 1000):
        """Detiene la música"""
        if self.music_playing:
            pygame.mixer.music.fadeout(fade_out_ms)
            self.music_playing = False
            self.current_music = None

    def play_ambient_battle(self):
        """Reproduce ambiente de batalla"""
        # Sonidos ambientales aleatorios
        ambient_sounds = ["distant_battle", "wind", "horn", "march"]

        if random.random() < 0.02:  # 2% chance cada frame
            sound = random.choice(ambient_sounds)
            if sound in self.sounds:
                channel = self.sounds[sound].play()
                if channel:
                    channel.set_volume(self.sfx_volume * 0.3)  # Volumen bajo para ambiente

    def play_formation_sound(self, formation: str):
        """Reproduce sonido de cambio de formación"""
        formation_sounds = {
            "testudo": "shields_up",
            "cuneus": "charge",
            "orbis": "defensive",
            "linea": "horn"
        }

        sound = formation_sounds.get(formation, "horn")
        if sound in self.sounds:
            self.sounds[sound].play()
        else:
            # Sonido genérico de cuerno
            self.play_battle_sound("horn")

    def set_sfx_volume(self, volume: float):
        """Ajusta volumen de efectos"""
        self.sfx_volume = max(0, min(1, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

    def set_music_volume(self, volume: float):
        """Ajusta volumen de música"""
        self.music_volume = max(0, min(1, volume))
        pygame.mixer.music.set_volume(self.music_volume)


# Generador de gritos de guerra latinos
class WarCryGenerator:
    """Generador de gritos de guerra latinos épicos"""

    ROMAN_CRIES = [
        "ROMA INVICTA!",
        "SENATUS POPULUSQUE ROMANUS!",
        "VICTORIA AUT MORS!",
        "PRO GLORIA ROMAE!",
        "MARS NOBISCUM!",
        "LEGIO AETERNA!",
        "AD VICTORIAM!",
        "GLADIUS ET SCUTUM!",
        "FORTUNA AUDACES IUVAT!",
        "DULCE ET DECORUM EST!"
    ]

    BARBARIAN_CRIES = [
        "AAAAARGH!",
        "SANGRE Y MUERTE!",
        "POR LA HORDA!",
        "DESTRUCCIÓN!",
        "SIN PIEDAD!",
        "MUERTE A ROMA!",
        "LIBERTAD O MUERTE!",
        "FUEGO Y ACERO!",
        "TORMENTA DE GUERRA!",
        "FURIA SALVAJE!"
    ]

    @staticmethod
    def get_random_cry(is_roman: bool = True) -> str:
        """Obtiene un grito de guerra aleatorio"""
        if is_roman:
            return random.choice(WarCryGenerator.ROMAN_CRIES)
        else:
            return random.choice(WarCryGenerator.BARBARIAN_CRIES)

    @staticmethod
    def get_victory_message(is_roman: bool = True) -> str:
        """Obtiene mensaje de victoria"""
        if is_roman:
            return random.choice([
                "¡VICTORIA! ¡Roma es eterna!",
                "¡Los dioses sonríen a Roma!",
                "¡Gloria al Imperio!",
                "¡Otro triunfo para las águilas romanas!",
                "¡César estaría orgulloso!"
            ])
        else:
            return random.choice([
                "¡Las legiones han caído!",
                "¡Roma tiembla ante nosotros!",
                "¡Libertad para nuestro pueblo!",
                "¡El imperio sangra!",
                "¡Victoria salvaje!"
            ])

    @staticmethod
    def get_defeat_message(is_roman: bool = True) -> str:
        """Obtiene mensaje de derrota"""
        if is_roman:
            return random.choice([
                "Las águilas han caído...",
                "Roma llora a sus hijos...",
                "Una batalla perdida, no la guerra...",
                "Volveremos más fuertes...",
                "El honor permanece..."
            ])
        else:
            return random.choice([
                "La horda se dispersa...",
                "Roma prevalece hoy...",
                "Nuestra furia no fue suficiente...",
                "Los dioses nos abandonaron...",
                "Otro día lucharemos..."
            ])