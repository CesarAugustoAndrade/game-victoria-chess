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
        """Crea sonidos sintéticos épicos si no hay archivos"""
        print("[SOUND] Creating EPIC synthetic battle sounds...")

        try:
            import numpy as np
        except ImportError:
            print("[WARNING] NumPy not installed, sounds will be limited")
            return

        sample_rate = 44100  # Mayor calidad

        # ========== SONIDO DE ESPADA ÉPICO ==========
        duration = 0.3
        num_samples = int(sample_rate * duration)
        sword_samples = np.zeros((num_samples, 2), dtype=np.int16)

        for i in range(num_samples):
            t = i / sample_rate

            # Múltiples componentes de frecuencia para sonido metálico
            freq1 = 800 * (1 - t * 2)  # Frecuencia principal decayendo
            freq2 = 1200 * (1 - t * 1.5)  # Armónico alto
            freq3 = 400 * (1 - t)  # Bajo

            # Generar tonos
            tone1 = np.sin(2 * np.pi * freq1 * t) * 8000 * np.exp(-t * 10)
            tone2 = np.sin(2 * np.pi * freq2 * t) * 4000 * np.exp(-t * 15)
            tone3 = np.sin(2 * np.pi * freq3 * t) * 6000 * np.exp(-t * 5)

            # Ruido metálico
            metallic_noise = np.random.randint(-2000, 2000) * np.exp(-t * 8)

            # Combinar
            value = tone1 + tone2 + tone3 + metallic_noise
            value = int(np.clip(value, -32768, 32767))

            # Estéreo con ligera diferencia
            sword_samples[i] = [value, int(value * 0.95)]

        self.sounds["sword_hit"] = pygame.sndarray.make_sound(sword_samples)

        # ========== FLECHA VOLANDO ==========
        duration = 0.5
        num_samples = int(sample_rate * duration)
        arrow_samples = np.zeros((num_samples, 2), dtype=np.int16)

        for i in range(num_samples):
            t = i / sample_rate

            # Whoosh ascendente
            freq = 200 + t * 800  # Frecuencia aumentando
            volume = 5000 * np.sin(np.pi * t / duration)  # Envolvente

            # Tono principal
            tone = np.sin(2 * np.pi * freq * t) * volume

            # Añadir algo de viento/silbido
            wind = np.random.randn() * 1000 * volume / 5000

            value = int(np.clip(tone + wind, -32768, 32767))
            arrow_samples[i] = [value, value]

        self.sounds["arrow_shot"] = pygame.sndarray.make_sound(arrow_samples)

        # ========== GALOPE DE CABALLO ==========
        duration = 1.0
        num_samples = int(sample_rate * duration)
        horse_samples = np.zeros((num_samples, 2), dtype=np.int16)

        # Patrón de galope (4 golpes)
        hoof_times = [0.0, 0.15, 0.35, 0.5, 0.65, 0.8]

        for hoof_time in hoof_times:
            hoof_start = int(hoof_time * sample_rate)
            hoof_duration = int(0.05 * sample_rate)

            for i in range(hoof_duration):
                if hoof_start + i < num_samples:
                    t = i / sample_rate

                    # Impacto bajo
                    impact = np.sin(2 * np.pi * 60 * t) * 15000 * np.exp(-t * 50)
                    # Ruido de tierra
                    dirt = np.random.randint(-3000, 3000) * np.exp(-t * 30)

                    value = int(np.clip(impact + dirt, -32768, 32767))
                    horse_samples[hoof_start + i] += np.array([value, int(value * 0.9)], dtype=np.int16)

        self.sounds["horse_gallop"] = pygame.sndarray.make_sound(horse_samples)

        # ========== ESCUDO BLOQUEANDO ==========
        duration = 0.2
        num_samples = int(sample_rate * duration)
        shield_samples = np.zeros((num_samples, 2), dtype=np.int16)

        for i in range(num_samples):
            t = i / sample_rate

            # Impacto sordo
            freq = 150 * (1 - t * 2)
            tone = np.sin(2 * np.pi * freq * t) * 10000 * np.exp(-t * 20)

            # Resonancia de madera
            wood_freq = 300 * (1 - t)
            wood = np.sin(2 * np.pi * wood_freq * t) * 5000 * np.exp(-t * 15)

            # Ruido de impacto
            impact_noise = np.random.randint(-4000, 4000) * np.exp(-t * 25)

            value = int(np.clip(tone + wood + impact_noise, -32768, 32767))
            shield_samples[i] = [value, value]

        self.sounds["shield_block"] = pygame.sndarray.make_sound(shield_samples)

        # ========== GRITO DE MUERTE ==========
        duration = 1.2
        num_samples = int(sample_rate * duration)
        death_samples = np.zeros((num_samples, 2), dtype=np.int16)

        for i in range(num_samples):
            t = i / sample_rate

            # Grito descendente
            freq = 800 * (1 - t * 0.5)  # Frecuencia bajando
            volume = 8000 * np.exp(-t * 0.8)  # Decayendo

            # Voz con vibrato
            vibrato = np.sin(2 * np.pi * 5 * t) * 50
            voice = np.sin(2 * np.pi * (freq + vibrato) * t) * volume

            # Añadir armónicos para voz más realista
            harmonic2 = np.sin(2 * np.pi * (freq * 2) * t) * volume * 0.3
            harmonic3 = np.sin(2 * np.pi * (freq * 3) * t) * volume * 0.1

            value = int(np.clip(voice + harmonic2 + harmonic3, -32768, 32767))
            death_samples[i] = [value, value]

        self.sounds["death_scream"] = pygame.sndarray.make_sound(death_samples)

        # ========== MARCHA DE LEGIÓN ==========
        duration = 0.8
        num_samples = int(sample_rate * duration)
        march_samples = np.zeros((num_samples, 2), dtype=np.int16)

        # Dos pasos (izquierdo-derecho)
        step_times = [0.0, 0.4]

        for step_time in step_times:
            step_start = int(step_time * sample_rate)
            step_duration = int(0.15 * sample_rate)

            for i in range(step_duration):
                if step_start + i < num_samples:
                    t = i / sample_rate

                    # Impacto del paso
                    impact = np.sin(2 * np.pi * 80 * t) * 8000 * np.exp(-t * 30)
                    # Ruido de armadura
                    armor = np.sin(2 * np.pi * 2000 * t) * 2000 * np.exp(-t * 50)
                    # Tierra/arena
                    ground = np.random.randint(-1500, 1500) * np.exp(-t * 20)

                    value = impact + armor + ground

                    # Pan estéreo para simular marcha
                    if step_time == 0.0:  # Paso izquierdo
                        left = int(np.clip(value * 1.2, -32768, 32767))
                        right = int(np.clip(value * 0.8, -32768, 32767))
                        march_samples[step_start + i] += np.array([left, right], dtype=np.int16)
                    else:  # Paso derecho
                        left = int(np.clip(value * 0.8, -32768, 32767))
                        right = int(np.clip(value * 1.2, -32768, 32767))
                        march_samples[step_start + i] += np.array([left, right], dtype=np.int16)

        self.sounds["march"] = pygame.sndarray.make_sound(march_samples)

        # ========== CUERNO DE GUERRA ==========
        duration = 1.5
        num_samples = int(sample_rate * duration)
        horn_samples = np.zeros((num_samples, 2), dtype=np.int16)

        for i in range(num_samples):
            t = i / sample_rate

            # Frecuencia fundamental del cuerno
            freq = 220  # La3

            # Envolvente ADSR
            if t < 0.1:  # Attack
                envelope = t * 10
            elif t < 0.3:  # Decay
                envelope = 1.0 - (t - 0.1) * 2
            elif t < 1.2:  # Sustain
                envelope = 0.6
            else:  # Release
                envelope = 0.6 * (1 - (t - 1.2) / 0.3)

            # Tono principal con armónicos
            fundamental = np.sin(2 * np.pi * freq * t)
            harmonic2 = np.sin(2 * np.pi * freq * 2 * t) * 0.5
            harmonic3 = np.sin(2 * np.pi * freq * 3 * t) * 0.3
            harmonic4 = np.sin(2 * np.pi * freq * 4 * t) * 0.2

            # Vibrato ligero
            vibrato = np.sin(2 * np.pi * 4 * t) * 5

            tone = (fundamental + harmonic2 + harmonic3 + harmonic4) * 10000 * envelope
            tone = np.sin(2 * np.pi * (freq + vibrato) * t) * 10000 * envelope

            # Reverb simple (eco)
            if i > int(0.1 * sample_rate):
                echo_idx = i - int(0.1 * sample_rate)
                tone += horn_samples[echo_idx][0] * 0.3

            value = int(np.clip(tone, -32768, 32767))
            horn_samples[i] = [value, value]

        self.sounds["horn"] = pygame.sndarray.make_sound(horn_samples)

        # ========== GRITO DE BATALLA ==========
        duration = 0.8
        num_samples = int(sample_rate * duration)
        warcry_samples = np.zeros((num_samples, 2), dtype=np.int16)

        for i in range(num_samples):
            t = i / sample_rate

            # Grito ascendente y luego sostenido
            if t < 0.2:
                freq = 300 + t * 2000  # Subiendo
                volume = t * 5 * 10000
            else:
                freq = 700  # Sostenido
                volume = 10000 * np.exp(-(t - 0.2) * 2)

            # Voz con mucho vibrato y roughness
            vibrato = np.sin(2 * np.pi * 6 * t) * 30
            roughness = np.random.randn() * 2000

            voice = np.sin(2 * np.pi * (freq + vibrato) * t) * volume
            voice += roughness

            # Múltiples voces (coro)
            voice2 = np.sin(2 * np.pi * (freq * 1.01 + vibrato) * t) * volume * 0.7
            voice3 = np.sin(2 * np.pi * (freq * 0.99 + vibrato) * t) * volume * 0.7

            value = int(np.clip(voice + voice2 + voice3, -32768, 32767))
            warcry_samples[i] = [value, value]

        self.sounds["battle_cry"] = pygame.sndarray.make_sound(warcry_samples)

        # ========== SONIDOS AMBIENTALES ==========
        # Viento
        duration = 3.0
        num_samples = int(sample_rate * duration)
        wind_samples = np.zeros((num_samples, 2), dtype=np.int16)

        for i in range(num_samples):
            t = i / sample_rate

            # Ruido filtrado para viento
            wind = np.random.randn() * 2000
            # Modulación lenta
            modulation = np.sin(2 * np.pi * 0.3 * t) * 0.5 + 0.5

            value = int(np.clip(wind * modulation, -32768, 32767))
            wind_samples[i] = [value, int(value * 1.1) if value * 1.1 <= 32767 else 32767]

        self.sounds["wind"] = pygame.sndarray.make_sound(wind_samples)

        # Batalla distante
        duration = 2.0
        num_samples = int(sample_rate * duration)
        distant_samples = np.zeros((num_samples, 2), dtype=np.int16)

        for i in range(num_samples):
            t = i / sample_rate

            # Mezcla de frecuencias bajas
            rumble = np.sin(2 * np.pi * 40 * t) * 1000
            rumble += np.sin(2 * np.pi * 60 * t) * 800
            rumble += np.sin(2 * np.pi * 80 * t) * 600

            # Ocasionales "golpes" aleatorios
            if random.random() < 0.01:
                rumble += np.random.randint(-3000, 3000)

            # Envolvente ondulante
            envelope = np.sin(2 * np.pi * 0.5 * t) * 0.3 + 0.7

            value = int(np.clip(rumble * envelope, -32768, 32767))
            distant_samples[i] = [value, value]

        self.sounds["distant_battle"] = pygame.sndarray.make_sound(distant_samples)

        print("[SOUND] Epic synthetic sounds created successfully!")

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