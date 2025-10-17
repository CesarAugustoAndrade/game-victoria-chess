"""
Renderizador de batalla táctica ÉPICO para pygame
"""

import pygame
import math
import random
from typing import Optional, List, Tuple
from src.domain.batalla import Batalla
from src.domain.value_objects import Posicion, Bando, TipoUnidad
from src.domain.entities import Unidad
from src.presentation.sprite_loader import EpicSpriteLoader, SpriteEffects
from src.presentation.particle_system import ParticleSystem, ParticleEffects
from src.presentation.sound_system import EpicSoundSystem, WarCryGenerator
from src.presentation.animation_system import AnimationManager, Tween, EaseType, FloatingText
from src.presentation.camera_effects import CinematicCamera, CombatZoomController, ScreenEffect
from src.presentation.ui_effects import ModernTooltip, TooltipData, NotificationSystem, DamageNumberSystem
from src.presentation.weather_system import WeatherSystem, WeatherType, TimeOfDay


class BattleRenderer:
    """Renderiza la batalla táctica en el tablero"""

    def __init__(self, screen_width: int = 1280, screen_height: int = 720):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Configuración del tablero
        self.board_width = 7
        self.board_height = 9
        self.tile_size = 70
        self.board_offset_x = (screen_width - (self.board_width * self.tile_size)) // 2
        self.board_offset_y = 100

        # Colores
        self.TILE_LIGHT = (240, 217, 181)
        self.TILE_DARK = (181, 136, 99)
        self.TILE_HIGHLIGHT = (255, 255, 150)
        self.TILE_VALID_MOVE = (150, 255, 150)
        self.TILE_ATTACKABLE = (255, 150, 150)
        self.BORDER_COLOR = (100, 60, 20)

        # Fuentes
        pygame.font.init()
        self.font_unit = pygame.font.Font(None, 36)
        self.font_stats = pygame.font.Font(None, 20)
        self.font_title = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 16)

        # Estado de renderizado
        self.selected_unit_id = None
        self.movimientos_validos = []
        self.objetivos_atacables = []
        self.animaciones = []

        # ===== SISTEMAS ÉPICOS MEJORADOS =====
        self.sprite_loader = EpicSpriteLoader()
        self.particle_system = ParticleSystem(max_particles=2000)
        self.sound_system = EpicSoundSystem()
        self.sprite_effects = SpriteEffects()

        # Nuevos sistemas épicos
        self.animation_manager = AnimationManager()
        self.camera = CinematicCamera(screen_width, screen_height)
        self.combat_zoom = CombatZoomController(self.camera)
        self.tooltip_system = ModernTooltip(self.font_stats, self.font_small)
        self.notification_system = NotificationSystem(screen_width, screen_height)
        self.damage_numbers = DamageNumberSystem()
        self.weather_system = WeatherSystem(screen_width, screen_height)

        # Configuración inicial épica
        self.weather_system.set_weather(WeatherType.CLEAR, 0.5)
        self.weather_system.set_time_of_day(TimeOfDay.AFTERNOON)

        # Animaciones activas
        self.active_animations = []
        self.combat_effects = []
        self.floating_texts = []

        # Estado de batalla épico
        self.battle_intensity = 0  # 0-100 intensidad de batalla
        self.screen_shake = 0  # Temblor de pantalla (legacy, ahora usa camera)
        self.last_war_cry_time = 0

        # Animaciones de unidades
        self.unit_animations = {}  # unit_id -> animation_state

    def render(self, screen: pygame.Surface, batalla: Optional[Batalla]):
        """Renderiza la batalla completa con efectos épicos mejorados"""
        if not batalla:
            self._render_no_battle(screen)
            return

        delta_time = 0.016  # ~60 FPS

        # Actualizar todos los sistemas
        self.camera.update(delta_time)
        self.animation_manager.update(delta_time)
        self.weather_system.update(delta_time)
        self.notification_system.update(delta_time)
        self.tooltip_system.update(delta_time)
        self.damage_numbers.update(delta_time)
        self.particle_system.update(delta_time)

        # Crear superficie de renderizado con transformación de cámara
        render_surface = pygame.Surface((self.screen_width, self.screen_height))

        # ===== CAPAS DE RENDERIZADO =====

        # 1. Fondo y clima
        self._render_background(render_surface)
        self.weather_system.render(render_surface)

        # 2. Tablero con efectos de cámara
        camera_surface = pygame.Surface((self.screen_width, self.screen_height))
        self._render_board(camera_surface)
        self._render_special_tiles(camera_surface, batalla)

        # 3. Sistema de partículas (detrás de las unidades)
        self.particle_system.render(camera_surface)

        # 4. Unidades con animaciones
        self._render_units(camera_surface, batalla)

        # 5. Efectos de combate
        self._render_combat_effects(camera_surface)

        # 6. Números de daño flotantes
        self.damage_numbers.render(camera_surface)

        # Aplicar transformaciones de cámara
        transformed_surface = self.camera.apply_transform(camera_surface)
        render_surface.blit(transformed_surface, (0, 0))

        # 7. Efectos de post-procesamiento (después de cámara)
        self.camera.render_effects(render_surface)

        # 8. UI (no afectada por cámara)
        self._render_ui(render_surface, batalla)

        # 9. Notificaciones flotantes
        self.notification_system.render(render_surface)

        # 10. Tooltips (siempre arriba)
        self.tooltip_system.render(render_surface)

        # 11. Animaciones de UI
        self._render_animations(render_surface)

        # Actualizar ambiente de batalla
        self.update_battle_ambience()

        # Blit final a pantalla
        screen.blit(render_surface, (0, 0))

    def _render_background(self, screen: pygame.Surface):
        """Renderiza el fondo"""
        # Fondo tipo pergamino
        screen.fill((230, 210, 180))

        # Bordes decorativos
        pygame.draw.rect(screen, (150, 100, 50), (0, 0, self.screen_width, 50))
        pygame.draw.rect(screen, (150, 100, 50), (0, self.screen_height - 50, self.screen_width, 50))

    def _render_board(self, screen: pygame.Surface):
        """Renderiza el tablero de juego"""
        # Borde del tablero
        border_rect = pygame.Rect(
            self.board_offset_x - 5,
            self.board_offset_y - 5,
            self.board_width * self.tile_size + 10,
            self.board_height * self.tile_size + 10
        )
        pygame.draw.rect(screen, self.BORDER_COLOR, border_rect, 3)

        # Casillas del tablero
        for row in range(self.board_height):
            for col in range(self.board_width):
                x = self.board_offset_x + col * self.tile_size
                y = self.board_offset_y + row * self.tile_size

                # Color alternado
                color = self.TILE_LIGHT if (row + col) % 2 == 0 else self.TILE_DARK

                pygame.draw.rect(screen, color, (x, y, self.tile_size, self.tile_size))
                pygame.draw.rect(screen, self.BORDER_COLOR, (x, y, self.tile_size, self.tile_size), 1)

                # Coordenadas para debug
                if row == 0:
                    coord_text = self.font_stats.render(str(col), True, (80, 60, 40))
                    screen.blit(coord_text, (x + 5, y - 20))
                if col == 0:
                    coord_text = self.font_stats.render(str(row), True, (80, 60, 40))
                    screen.blit(coord_text, (x - 20, y + 5))

    def _render_special_tiles(self, screen: pygame.Surface, batalla: Batalla):
        """Renderiza casillas especiales (movimientos, ataques)"""
        # Movimientos válidos
        for posicion in self.movimientos_validos:
            self._render_tile_overlay(screen, posicion, self.TILE_VALID_MOVE, 100)

        # Objetivos atacables
        for unidad in self.objetivos_atacables:
            self._render_tile_overlay(screen, unidad.posicion, self.TILE_ATTACKABLE, 120)

        # Unidad seleccionada
        if batalla.unidad_seleccionada:
            self._render_tile_overlay(
                screen,
                batalla.unidad_seleccionada.posicion,
                self.TILE_HIGHLIGHT,
                150
            )

    def _render_tile_overlay(self, screen: pygame.Surface, posicion: Posicion, color: tuple, alpha: int):
        """Renderiza un overlay sobre una casilla"""
        x = self.board_offset_x + posicion.columna * self.tile_size
        y = self.board_offset_y + posicion.fila * self.tile_size

        overlay = pygame.Surface((self.tile_size, self.tile_size))
        overlay.set_alpha(alpha)
        overlay.fill(color)
        screen.blit(overlay, (x, y))

    def _render_units(self, screen: pygame.Surface, batalla: Batalla):
        """Renderiza todas las unidades"""
        # Renderizar primero las unidades enemigas
        for unidad in batalla.ejercito_enemigo.unidades_vivas:
            self._render_unit(screen, unidad)

        # Luego las unidades del jugador
        for unidad in batalla.ejercito_jugador.unidades_vivas:
            self._render_unit(screen, unidad)

    def _render_unit(self, screen: pygame.Surface, unidad: Unidad):
        """Renderiza una unidad individual con sprite personalizado"""
        x = self.board_offset_x + unidad.posicion.columna * self.tile_size
        y = self.board_offset_y + unidad.posicion.fila * self.tile_size

        # Obtener sprite de la unidad (ahora con soporte de imágenes!)
        sprite = self.sprite_loader.get_unit_sprite(
            unidad.tipo,
            unidad.bando,
            size=self.tile_size - 10  # Un poco más pequeño que la casilla
        )

        # Posicionar sprite centrado en la casilla
        sprite_x = x + (self.tile_size - sprite.get_width()) // 2
        sprite_y = y + (self.tile_size - sprite.get_height()) // 2
        screen.blit(sprite, (sprite_x, sprite_y))

        # Indicadores de estado
        self._render_unit_status_indicators(screen, unidad, x, y)

        # Barra de vida
        self._render_health_bar(screen, unidad, x, y)

        # Barra de moral (si está por debajo del 100%)
        if unidad.moral_actual < 100:
            self._render_morale_bar(screen, unidad, x, y)

    def _render_unit_status_indicators(self, screen: pygame.Surface, unidad: Unidad, x: int, y: int):
        """Renderiza indicadores de estado de la unidad"""
        # Indicador de acción disponible (solo para romanos)
        if unidad.bando == Bando.ROMA:
            indicator_x = x + 3
            indicator_y = y + 3

            if unidad.puede_actuar:
                # Punto verde - puede actuar completamente
                pygame.draw.circle(screen, (0, 255, 0), (indicator_x, indicator_y), 4)
                pygame.draw.circle(screen, (0, 150, 0), (indicator_x, indicator_y), 4, 1)
            elif unidad.puede_moverse:
                # Punto amarillo - solo puede moverse
                pygame.draw.circle(screen, (255, 255, 0), (indicator_x, indicator_y), 4)
                pygame.draw.circle(screen, (150, 150, 0), (indicator_x, indicator_y), 4, 1)
            else:
                # Punto gris - ya actuó
                pygame.draw.circle(screen, (100, 100, 100), (indicator_x, indicator_y), 3)

        # Indicador de pánico
        if unidad.esta_en_panico:
            panic_x = x + self.tile_size - 15
            panic_y = y + 5

            # Símbolo de pánico (!)
            panic_surface = self.font_stats.render("!", True, (255, 0, 0))
            screen.blit(panic_surface, (panic_x, panic_y))

            # Animación de temblor (efecto visual)
            import random
            if random.random() > 0.5:
                offset = random.randint(-1, 1)
                panic_surface = self.font_stats.render("!", True, (200, 0, 0))
                screen.blit(panic_surface, (panic_x + offset, panic_y))

    def _render_health_bar(self, screen: pygame.Surface, unidad: Unidad, x: int, y: int):
        """Renderiza la barra de vida de una unidad"""
        bar_width = self.tile_size - 14
        bar_height = 4
        bar_x = x + 7
        bar_y = y + self.tile_size - 12

        # Fondo de la barra
        pygame.draw.rect(screen, (40, 40, 40), (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2))
        pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))

        # Vida actual
        health_percentage = unidad.porcentaje_vida
        current_width = int(bar_width * health_percentage)

        # Color según bando
        if unidad.bando == Bando.BARBAROS:
            # Enemigos siempre rojos
            health_color = (255, 0, 0)
        else:
            # Aliados con colores según vida
            if health_percentage > 0.6:
                health_color = (0, 200, 0)
            elif health_percentage > 0.3:
                health_color = (255, 200, 0)
            else:
                health_color = (255, 0, 0)

        if current_width > 0:
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, current_width, bar_height))

        # Texto de vida (opcional, para unidades seleccionadas)
        if unidad.bando == Bando.ROMA and health_percentage < 1.0:
            health_text = f"{unidad.vida_actual}/{unidad.estadisticas.vida_maxima}"
            text_surface = self.font_small.render(health_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(centerx=x + self.tile_size // 2, y=bar_y - 15)
            screen.blit(text_surface, text_rect)

    def _render_morale_bar(self, screen: pygame.Surface, unidad: Unidad, x: int, y: int):
        """Renderiza la barra de moral de una unidad"""
        bar_width = self.tile_size - 14
        bar_height = 3
        bar_x = x + 7
        bar_y = y + self.tile_size - 6

        # Solo mostrar si la moral no está al máximo
        morale_percentage = unidad.moral_actual / 100.0

        # Fondo de la barra
        pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height))

        # Moral actual
        current_width = int(bar_width * morale_percentage)

        # Color según moral
        if morale_percentage > 0.7:
            morale_color = (100, 100, 255)  # Azul - buena moral
        elif morale_percentage > 0.3:
            morale_color = (255, 255, 100)  # Amarillo - moral media
        else:
            morale_color = (200, 100, 100)  # Rojo oscuro - moral baja

        if current_width > 0:
            pygame.draw.rect(screen, morale_color, (bar_x, bar_y, current_width, bar_height))

    def _render_ui(self, screen: pygame.Surface, batalla: Batalla):
        """Renderiza la interfaz de usuario"""
        # Título
        title = "LEGIO ROMANA - BATALLA TÁCTICA"
        title_text = self.font_title.render(title, True, (139, 69, 19))
        title_rect = title_text.get_rect(centerx=self.screen_width // 2, y=20)
        screen.blit(title_text, title_rect)

        # Información de turno
        turno_text = f"Ronda {batalla.ronda_actual} - Turno: {'ROMA' if batalla.turno_actual.value == 'player' else 'BÁRBAROS'}"
        turno_surface = self.font_stats.render(turno_text, True, (80, 60, 40))
        screen.blit(turno_surface, (20, 70))

        # Estado del ejército
        self._render_army_status(screen, batalla)

        # Unidad seleccionada
        if batalla.unidad_seleccionada:
            self._render_unit_info(screen, batalla.unidad_seleccionada)

        # Controles
        self._render_controls(screen)

    def _render_army_status(self, screen: pygame.Surface, batalla: Batalla):
        """Renderiza el estado de los ejércitos"""
        # Ejército Romano
        roma_text = f"ROMA: {len(batalla.ejercito_jugador.unidades_vivas)} unidades | Moral: {batalla.ejercito_jugador.moral_promedio:.0f}%"
        roma_surface = self.font_stats.render(roma_text, True, (180, 20, 20))
        screen.blit(roma_surface, (20, 100))

        # Ejército Bárbaro
        barbaro_text = f"BÁRBAROS: {len(batalla.ejercito_enemigo.unidades_vivas)} unidades | Moral: {batalla.ejercito_enemigo.moral_promedio:.0f}%"
        barbaro_surface = self.font_stats.render(barbaro_text, True, (50, 100, 50))
        screen.blit(barbaro_surface, (20, 125))

    def _render_unit_info(self, screen: pygame.Surface, unidad: Unidad):
        """Renderiza información de la unidad seleccionada"""
        info_x = self.screen_width - 250
        info_y = 100

        # Fondo
        info_rect = pygame.Rect(info_x - 10, info_y - 10, 240, 200)
        pygame.draw.rect(screen, (200, 180, 150), info_rect)
        pygame.draw.rect(screen, self.BORDER_COLOR, info_rect, 2)

        # Nombre
        name_text = self.font_stats.render(unidad.visualizacion.nombre, True, (60, 40, 20))
        screen.blit(name_text, (info_x, info_y))

        # Nombre latino
        latin_text = self.font_stats.render(f"({unidad.visualizacion.nombre_latino})", True, (80, 60, 40))
        screen.blit(latin_text, (info_x, info_y + 25))

        # Estadísticas
        stats = [
            f"Vida: {unidad.vida_actual}/{unidad.estadisticas.vida_maxima}",
            f"Ataque: {unidad.estadisticas.ataque}",
            f"Defensa: {unidad.estadisticas.defensa}",
            f"Moral: {unidad.moral_actual}%",
            f"Movimiento: {unidad.estadisticas.rango_movimiento}",
            f"Alcance: {unidad.estadisticas.rango_ataque}"
        ]

        y_offset = 60
        for stat in stats:
            stat_text = self.font_stats.render(stat, True, (60, 40, 20))
            screen.blit(stat_text, (info_x, info_y + y_offset))
            y_offset += 20

    def _render_controls(self, screen: pygame.Surface):
        """Renderiza los controles del juego"""
        controls = [
            "Click izq: Seleccionar/Mover",
            "Click der: Atacar",
            "Espacio: Finalizar turno",
            "F: Cambiar formación",
            "ESC: Menú"
        ]

        y = self.screen_height - 150
        for control in controls:
            control_text = self.font_stats.render(control, True, (80, 60, 40))
            screen.blit(control_text, (20, y))
            y += 25

    def _render_no_battle(self, screen: pygame.Surface):
        """Renderiza cuando no hay batalla activa"""
        screen.fill((230, 210, 180))
        text = self.font_title.render("LEGIO ROMANA", True, (139, 69, 19))
        rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(text, rect)

    def _render_animations(self, screen: pygame.Surface):
        """Renderiza animaciones activas épicas"""
        for animation in self.active_animations[:]:
            animation.update(0.016)
            if not animation.finished:
                frame = animation.get_current_frame()
                if frame:
                    screen.blit(frame, animation.position)
            else:
                self.active_animations.remove(animation)

    def _render_combat_effects(self, screen: pygame.Surface):
        """Renderiza efectos de combate épicos"""
        for effect in self.combat_effects[:]:
            effect['duration'] -= 0.016
            if effect['duration'] > 0:
                # Renderizar según tipo de efecto
                if effect['type'] == 'slash':
                    self._render_slash_effect(screen, effect)
                elif effect['type'] == 'impact':
                    self._render_impact_effect(screen, effect)
            else:
                self.combat_effects.remove(effect)


    def _render_slash_effect(self, screen: pygame.Surface, effect: dict):
        """Renderiza efecto de corte"""
        alpha = int(255 * effect['duration'] / effect['max_duration'])
        slash_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.arc(slash_surface, (255, 255, 255, alpha),
                       pygame.Rect(10, 10, 60, 60),
                       effect['start_angle'], effect['end_angle'], 3)
        screen.blit(slash_surface, effect['position'])

    def _render_impact_effect(self, screen: pygame.Surface, effect: dict):
        """Renderiza efecto de impacto"""
        alpha = int(255 * effect['duration'] / effect['max_duration'])
        radius = int(20 * (1 - effect['duration'] / effect['max_duration']))
        pygame.draw.circle(screen, (*effect['color'], alpha),
                          effect['position'], radius, 2)

    def set_highlights(self, movimientos: List[Posicion], objetivos: List[Unidad]):
        """Establece las casillas resaltadas"""
        self.movimientos_validos = movimientos
        self.objetivos_atacables = objetivos

    def get_board_position(self, mouse_pos: tuple) -> Optional[Posicion]:
        """Convierte posición del mouse a coordenadas del tablero"""
        x, y = mouse_pos
        col = (x - self.board_offset_x) // self.tile_size
        row = (y - self.board_offset_y) // self.tile_size

        if 0 <= row < self.board_height and 0 <= col < self.board_width:
            return Posicion(row, col)
        return None

    # ========== MÉTODOS ÉPICOS PARA EFECTOS ==========

    def trigger_attack_effect(self, attacker_pos: Posicion, target_pos: Posicion,
                             attacker_type: TipoUnidad, damage: int):
        """Dispara efectos visuales y sonoros de ataque ÉPICOS"""
        # Posición en pantalla
        ax = self.board_offset_x + attacker_pos.columna * self.tile_size + self.tile_size // 2
        ay = self.board_offset_y + attacker_pos.fila * self.tile_size + self.tile_size // 2
        tx = self.board_offset_x + target_pos.columna * self.tile_size + self.tile_size // 2
        ty = self.board_offset_y + target_pos.fila * self.tile_size + self.tile_size // 2

        # Zoom cinematográfico en combate
        self.combat_zoom.start_combat((ax, ay), (tx, ty))

        # Efectos según tipo de atacante
        if attacker_type == TipoUnidad.SAGITTARII:
            # Flecha volando con trayectoria animada
            ParticleEffects.create_arrow_trail(self.particle_system, ax, ay)
            self.sound_system.play_battle_sound("arrow_shot", (ax, ay))

            # Animación de flecha
            arrow_tween_x = Tween(ax, tx, 0.3, ease_type=EaseType.LINEAR)
            arrow_tween_y = Tween(ay, ty - 30, 0.15, ease_type=EaseType.EASE_OUT)
            arrow_tween_y2 = Tween(ty - 30, ty, 0.15, ease_type=EaseType.EASE_IN)
            self.animation_manager.add_tween("arrow_x", arrow_tween_x)
            self.animation_manager.add_tween("arrow_y", arrow_tween_y)

        elif attacker_type == TipoUnidad.EQUITES:
            # Carga de caballería épica
            self.camera.shake_camera(15, 0.5, 40)
            ParticleEffects.create_dust_cloud(self.particle_system, tx, ty)
            self.sound_system.play_battle_sound("horse_gallop", (ax, ay))

            # Speed lines para sensación de velocidad
            self.camera.create_speed_lines(math.atan2(ty - ay, tx - ax), 0.8)

        else:
            # Ataque cuerpo a cuerpo mejorado
            self.combat_effects.append({
                'type': 'slash',
                'position': (tx - 40, ty - 40),
                'start_angle': -0.5,
                'end_angle': 1.0,
                'duration': 0.3,
                'max_duration': 0.3
            })
            self.sound_system.play_battle_sound("sword_hit", (tx, ty))

            # Pequeño shake para impacto
            self.camera.add_trauma(0.2)

        # Efectos de impacto mejorados
        is_critical = damage > 30
        if is_critical:
            # GOLPE CRÍTICO - Efectos épicos
            self.combat_zoom.critical_hit()
            ParticleEffects.create_blood_explosion(self.particle_system, tx, ty)
            self.camera.screen_flash((255, 0, 0), 100)

            # Notificación épica
            self.notification_system.add_notification(
                f"¡GOLPE CRÍTICO! {damage} daño",
                (255, 50, 50),
                duration=2.0
            )
        elif damage > 20:
            # Daño alto
            ParticleEffects.create_blood_explosion(self.particle_system, tx, ty)
            self.camera.add_trauma(0.3)
        else:
            # Daño normal
            ParticleEffects.create_spark_burst(self.particle_system, tx, ty)

        # Número de daño flotante
        self.damage_numbers.add_damage_number(tx, ty, damage, is_critical)

        # Incrementar intensidad de batalla
        self.battle_intensity = min(100, self.battle_intensity + 10)

        # Clima más intenso durante batalla
        if self.battle_intensity > 50:
            self.weather_system.create_battle_atmosphere()

    def trigger_unit_death(self, unit_pos: Posicion, unit_type: TipoUnidad):
        """Efectos cuando muere una unidad"""
        x = self.board_offset_x + unit_pos.columna * self.tile_size + self.tile_size // 2
        y = self.board_offset_y + unit_pos.fila * self.tile_size + self.tile_size // 2

        # Explosión de partículas rojas
        ParticleEffects.create_blood_explosion(self.particle_system, x, y)

        # Sonido de muerte
        self.sound_system.play_unit_sound(unit_type, "death")

        # Screen shake proporcional
        self.screen_shake = 8

        # Efecto de impacto
        self.combat_effects.append({
            'type': 'impact',
            'position': (x, y),
            'color': (180, 0, 0),
            'duration': 0.5,
            'max_duration': 0.5
        })

    def trigger_unit_move(self, unit_pos: Posicion, unit_type: TipoUnidad):
        """Efectos cuando se mueve una unidad"""
        x = self.board_offset_x + unit_pos.columna * self.tile_size + self.tile_size // 2
        y = self.board_offset_y + unit_pos.fila * self.tile_size + self.tile_size // 2

        # Polvo al moverse
        if unit_type == TipoUnidad.EQUITES:
            ParticleEffects.create_dust_cloud(self.particle_system, x, y + 20)
            self.sound_system.play_battle_sound("horse_gallop", (x, y))
        else:
            # Sonido de marcha
            if random.random() < 0.3:  # No siempre, para no saturar
                self.sound_system.play_battle_sound("march", (x, y))

    def trigger_formation_change(self, formation: str):
        """Efectos al cambiar formación"""
        # Sonido de cuerno
        self.sound_system.play_formation_sound(formation)

        # Efecto visual en todas las unidades romanas
        self.battle_intensity = min(100, self.battle_intensity + 20)

        # Mensaje épico
        if formation == "testudo":
            self.trigger_war_cry("TESTUDO FORMATION!")
        elif formation == "cuneus":
            self.trigger_war_cry("CUNEUS! CHARGE!")

    def trigger_war_cry(self, message: str = None):
        """Dispara un grito de guerra épico"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_war_cry_time > 3000:  # Max uno cada 3 segundos
            self.last_war_cry_time = current_time

            # Sonido
            self.sound_system.play_war_cry(True)

            # Screen shake leve
            self.screen_shake = 5

            # Partículas en centro de pantalla
            cx = self.screen_width // 2
            cy = self.screen_height // 3
            ParticleEffects.create_magic_aura(self.particle_system, cx, cy, (255, 215, 0))

    def trigger_victory_effects(self):
        """Efectos épicos de victoria mejorados"""
        # Modo cinemático
        self.camera.enter_cinematic_mode()
        self.camera.set_zoom(0.9, instant=False)

        # Fuegos artificiales múltiples
        for i in range(5):
            x = random.randint(200, self.screen_width - 200)
            y = random.randint(100, 300)
            # Delay escalonado para fuegos artificiales
            pygame.time.set_timer(pygame.USEREVENT + 10 + i, i * 500)
            ParticleEffects.create_victory_celebration(self.particle_system, x, y)

        # Efectos visuales de victoria
        self.camera.add_effect(ScreenEffect.VICTORY_GLOW)

        # Notificación épica
        self.notification_system.add_notification(
            "¡VICTORIA! ¡Gloria a Roma!",
            (255, 215, 0),
            duration=5.0
        )

        # Música de victoria
        self.sound_system.play_music("victory")

        # Clima despejado para celebración
        self.weather_system.set_weather(WeatherType.CLEAR, 0.2)
        self.weather_system.set_time_of_day(TimeOfDay.DUSK)

        # Gritos de victoria
        self.sound_system.play_war_cry(True)

        # Reset intensidad
        self.battle_intensity = 0

    def trigger_defeat_effects(self):
        """Efectos de derrota dramáticos"""
        # Modo cinemático oscuro
        self.camera.enter_cinematic_mode()
        self.camera.add_effect(ScreenEffect.DEFEAT_DARKNESS)

        # Zoom out lento
        self.camera.set_zoom(0.7, instant=False)

        # Lluvia triste
        self.weather_system.set_weather(WeatherType.RAIN, 0.8)
        self.weather_system.set_time_of_day(TimeOfDay.NIGHT)

        # Música triste
        self.sound_system.play_music("defeat")

        # Notificación de derrota
        self.notification_system.add_notification(
            "Derrota... Las águilas han caído",
            (150, 50, 50),
            duration=5.0
        )

        # Partículas de ceniza cayendo
        for _ in range(10):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height // 2)
            ParticleEffects.create_dust_cloud(self.particle_system, x, y)

        # Camera shake suave de desesperación
        self.camera.shake_camera(5, 2.0, 5)

    def update_battle_ambience(self):
        """Actualiza el ambiente de batalla"""
        if self.battle_intensity > 0:
            self.battle_intensity -= 0.1

            # Sonidos ambientales según intensidad
            if self.battle_intensity > 50 and random.random() < 0.01:
                self.sound_system.play_ambient_battle()