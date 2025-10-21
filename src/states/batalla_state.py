"""
Estado de batalla táctica romana
"""

import pygame
from src.core.state import State
from src.application.servicio_juego import ServicioJuego
from src.presentation.battle_renderer import BattleRenderer
from src.domain.value_objects import TurnoActual, Bando
from src.domain.events import *
from src.utils.save_manager import save_manager


class BatallaState(State):
    """Estado de batalla táctica"""

    def __init__(self, game, nivel=None, campania=None):
        super().__init__(game)
        self.servicio_juego = ServicioJuego()
        self.renderer = BattleRenderer()
        self.eventos_pendientes = []
        self.mensaje_actual = ""
        self.tiempo_mensaje = 0
        self.nivel = nivel  # Nivel opcional para campaña
        self.campania = campania  # Referencia a la campaña para guardar progreso
        self.tutorial_index = 0  # Índice para mensajes de tutorial
        self.nivel_completado = False  # Flag para saber si ya se marcó como completado

        # ===== SISTEMA DE AUTO-PLAY CON IA =====
        self.auto_play_enabled = False  # Modo auto-play desactivado por defecto
        self.auto_play_timer = 0  # Timer para retraso entre acciones
        self.auto_play_delay = 0.5  # Segundos entre acciones de IA

        # ===== SISTEMA DE BLOQUEO/SINCRONIZACIÓN =====
        self.processing_state = "READY"  # Estados: READY, PROCESSING_ENEMY_TURN

        # ===== NUEVO SISTEMA DE TURNO ENEMIGO PASO A PASO =====
        self.enemy_turn_active = False  # Si el turno enemigo está activo
        self.enemy_turn_timer = 0  # Timer para acciones enemigas
        self.enemy_turn_delay = 0.8  # Delay entre acciones enemigas (más lento para ver mejor)

    def on_enter(self):
        """Inicia la batalla cuando se entra al estado"""
        if self.nivel:
            # Iniciar batalla desde nivel
            eventos = self.servicio_juego.iniciar_batalla_desde_nivel(self.nivel)
            self._procesar_eventos(eventos)

            # Mostrar primer mensaje de tutorial si es un nivel tutorial
            if self.nivel.es_tutorial and self.nivel.tutorial_messages:
                self._mostrar_tutorial()
        else:
            # Batalla normal (ejércitos completos)
            # Obtener dificultad del game o usar normal por defecto
            dificultad = getattr(self.game, 'dificultad', 'normal')
            print(f"Iniciando batalla con dificultad: {dificultad.upper()}")

            eventos = self.servicio_juego.iniciar_nueva_batalla(dificultad)
            self._procesar_eventos(eventos)

    def handle_event(self, event):
        """Maneja eventos de pygame"""
        batalla = self.servicio_juego.obtener_batalla_actual()
        if not batalla:
            return

        # ===== BLOQUEAR INPUT SI NO ESTÁ READY =====
        # Solo permitir ESC para salir siempre
        if self.processing_state != "READY":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Permitir salir siempre
                if self.nivel and self.campania:
                    from src.states.nivel_selector_state import NivelSelectorState
                    self.game.change_state(NivelSelectorState(self.game, self.campania))
                else:
                    from src.states.menu_state import MenuState
                    self.game.change_state(MenuState(self.game))
            return  # Ignorar todos los demás inputs

        # Manejar eventos de timer de cámara
        if event.type == pygame.USEREVENT + 1:
            # Reset slow motion
            self.renderer.camera.target_time_scale = 1.0
        elif event.type == pygame.USEREVENT + 2:
            # Remover efecto de sangre
            from src.presentation.camera_effects import ScreenEffect
            self.renderer.camera.remove_effect(ScreenEffect.BLOOD_OVERLAY)
        elif event.type == pygame.USEREVENT + 3:
            # ARREGLO: Resetear zoom después de muerte de unidad
            from src.presentation.camera_effects import ZoomMode
            self.renderer.camera.set_zoom(ZoomMode.NORMAL.value)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Volver al selector de niveles si es campaña, o al menú si no
                if self.nivel and self.campania:
                    from src.states.nivel_selector_state import NivelSelectorState
                    # Volver al selector con la misma campaña (progreso guardado)
                    self.game.change_state(NivelSelectorState(self.game, self.campania))
                else:
                    from src.states.menu_state import MenuState
                    self.game.change_state(MenuState(self.game))

            elif event.key == pygame.K_SPACE:
                # Finalizar turno del jugador y activar turno enemigo
                if batalla.turno_actual == TurnoActual.JUGADOR:
                    # Cambiar turno en el dominio
                    self.servicio_juego.cambiar_turno_a_enemigo()

                    # Activar sistema de turno enemigo paso a paso
                    self.enemy_turn_active = True
                    self.enemy_turn_timer = 0
                    self.processing_state = "PROCESSING_ENEMY_TURN"  # Bloquear input

                    self._mostrar_mensaje("Turno Enemigo...")

            elif event.key == pygame.K_f:
                # Cambiar formación
                self._cambiar_formacion()

            elif event.key == pygame.K_r and batalla.batalla_terminada:
                # Reiniciar batalla
                self.servicio_juego.reiniciar_juego()
                self.on_enter()

            elif event.key == pygame.K_t and self.nivel and self.nivel.es_tutorial:
                # Mostrar siguiente mensaje de tutorial
                self._mostrar_tutorial()

            elif event.key == pygame.K_a:
                # Activar/desactivar auto-play con IA agresiva
                self.auto_play_enabled = not self.auto_play_enabled
                if self.auto_play_enabled:
                    self._mostrar_mensaje("🤖 AUTO-PLAY ACTIVADO - IA Agresiva jugando")
                    self.renderer.notification_system.add_notification(
                        "IA AGRESIVA ACTIVADA",
                        (100, 255, 100),
                        duration=2.0
                    )
                else:
                    self._mostrar_mensaje("👤 AUTO-PLAY DESACTIVADO - Control manual")
                    self.renderer.notification_system.add_notification(
                        "CONTROL MANUAL",
                        (255, 255, 100),
                        duration=2.0
                    )

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if batalla.turno_actual == TurnoActual.JUGADOR and not batalla.batalla_terminada:
                mouse_pos = pygame.mouse.get_pos()
                board_pos = self.renderer.get_board_position(mouse_pos)

                if board_pos:
                    if event.button == 1:  # Click izquierdo
                        self._handle_left_click(board_pos)
                    elif event.button == 3:  # Click derecho
                        self._handle_right_click(board_pos)

    def _handle_left_click(self, posicion):
        """Maneja click izquierdo"""
        batalla = self.servicio_juego.obtener_batalla_actual()
        if not batalla:
            return

        # Buscar unidad en la posición
        unidad_en_pos = None

        # Verificar unidades del jugador
        for unidad in batalla.ejercito_jugador.unidades_vivas:
            if unidad.posicion == posicion:
                unidad_en_pos = unidad
                break

        # Si no hay unidad del jugador, verificar enemigos para información
        if not unidad_en_pos:
            for unidad in batalla.ejercito_enemigo.unidades_vivas:
                if unidad.posicion == posicion:
                    # Solo mostrar información, no seleccionar
                    self._mostrar_mensaje(f"Enemigo: {unidad.visualizacion.nombre}")
                    return

        if unidad_en_pos:
            # Seleccionar unidad del jugador
            if unidad_en_pos.bando == Bando.ROMA:
                try:
                    eventos = self.servicio_juego.seleccionar_unidad(unidad_en_pos.id)
                    self._procesar_eventos(eventos)
                    self._actualizar_highlights()
                except Exception as e:
                    # Mostrar mensaje si no se puede seleccionar
                    self._mostrar_mensaje(str(e))
        else:
            # Mover unidad seleccionada si el movimiento es válido
            if batalla.unidad_seleccionada:
                movimientos = batalla.obtener_movimientos_validos_unidad_seleccionada()
                if posicion in movimientos:
                    try:
                        eventos = self.servicio_juego.mover_unidad(posicion.fila, posicion.columna)
                        self._procesar_eventos(eventos)
                        self._actualizar_highlights()
                    except Exception as e:
                        self._mostrar_mensaje(f"Error al mover: {e}")
                else:
                    # Deseleccionar si no es movimiento válido
                    self.servicio_juego.deseleccionar_unidad()
                    self._actualizar_highlights()

    def _handle_right_click(self, posicion):
        """Maneja click derecho para atacar"""
        batalla = self.servicio_juego.obtener_batalla_actual()
        if not batalla or not batalla.unidad_seleccionada:
            return

        # Buscar enemigo en la posición
        for unidad in batalla.ejercito_enemigo.unidades_vivas:
            if unidad.posicion == posicion:
                # Intentar atacar
                objetivos = batalla.obtener_objetivos_atacables_unidad_seleccionada()
                if unidad in objetivos:
                    try:
                        eventos = self.servicio_juego.atacar_enemigo(unidad.id)
                        self._procesar_eventos(eventos)
                        self._actualizar_highlights()
                    except Exception as e:
                        self._mostrar_mensaje(f"Error al atacar: {e}")
                else:
                    self._mostrar_mensaje("¡Objetivo fuera de alcance!")
                break

    def _cambiar_formacion(self):
        """Cambia la formación del ejército"""
        formaciones = ["linea", "testudo", "cuneus", "orbis"]
        # Rotar entre formaciones (simplificado)
        formacion_actual = "linea"
        idx = formaciones.index(formacion_actual)
        nueva_formacion = formaciones[(idx + 1) % len(formaciones)]

        eventos = self.servicio_juego.aplicar_formacion(nueva_formacion)
        self._procesar_eventos(eventos)

    def _procesar_eventos(self, eventos):
        """Procesa eventos del dominio con EFECTOS ÉPICOS"""
        batalla = self.servicio_juego.obtener_batalla_actual()
        if not batalla:
            return

        # Procesar todos los eventos inmediatamente
        for evento in eventos:
            # Mostrar mensajes según el tipo de evento
            if isinstance(evento, EventoBatallaIniciada):
                self._mostrar_mensaje(evento.mensaje)
                # Grito de guerra inicial!
                self.renderer.trigger_war_cry("ROMA INVICTA!")

            elif isinstance(evento, EventoAtaqueRealizado):
                if evento.grito_guerra:
                    self._mostrar_mensaje(evento.grito_guerra)

                # EFECTOS DE COMBATE ÉPICOS
                # Buscar las unidades para obtener sus posiciones
                atacante = None
                defensor = None

                # Buscar en ambos ejércitos
                for unidad in batalla.ejercito_jugador.unidades_vivas + batalla.ejercito_enemigo.unidades_vivas:
                    if unidad.id == evento.resultado.atacante_id:
                        atacante = unidad
                    if unidad.id == evento.resultado.defensor_id:
                        defensor = unidad

                if atacante and defensor:
                    self.renderer.trigger_attack_effect(
                        atacante.posicion,
                        defensor.posicion,
                        atacante.tipo,
                        evento.resultado.danio_infligido
                    )

            elif isinstance(evento, EventoUnidadEliminada):
                self._mostrar_mensaje(evento.mensaje)

                # Efectos de muerte épicos
                # Buscar la unidad eliminada para su posición
                for ejercito in [batalla.ejercito_jugador, batalla.ejercito_enemigo]:
                    for unidad in ejercito._unidades:  # Incluir muertas
                        if unidad.id == evento.unidad_id:
                            self.renderer.trigger_unit_death(unidad.posicion, unidad.tipo)
                            break

            elif isinstance(evento, EventoUnidadMovida):
                # Efectos de movimiento
                unidad_movida = None
                for unidad in batalla.ejercito_jugador.unidades_vivas + batalla.ejercito_enemigo.unidades_vivas:
                    if unidad.id == evento.unidad_id:
                        unidad_movida = unidad
                        break

                if unidad_movida:
                    self.renderer.trigger_unit_move(evento.posicion_destino, unidad_movida.tipo)

            elif isinstance(evento, EventoBatallaTerminada):
                self._mostrar_mensaje(evento.mensaje)
                if evento.ganador == Bando.ROMA:
                    if self.nivel and self.campania and not self.nivel_completado:
                        # Marcar nivel como completado
                        self.campania.niveles_completados.add(self.nivel.numero - 1)
                        self.campania.registrar_victoria()
                        self.nivel_completado = True

                        # GUARDAR PROGRESO AUTOMÁTICAMENTE
                        self._guardar_progreso()

                        self._mostrar_mensaje(f"¡NIVEL {self.nivel.numero} COMPLETADO! Presiona ESC para continuar")
                    elif self.nivel:
                        self._mostrar_mensaje(f"¡NIVEL {self.nivel.numero} COMPLETADO! Presiona ESC para continuar")
                    else:
                        self._mostrar_mensaje("¡VICTORIA! Presiona R para jugar de nuevo")
                    # Trigger epic victory effects
                    self.renderer.trigger_victory_effects()
                else:
                    # Registrar derrota en estadísticas
                    if self.campania:
                        self.campania.registrar_derrota()
                        self._guardar_progreso()

                    self._mostrar_mensaje("¡DERROTA! Presiona R para intentar de nuevo")
                    self.renderer.trigger_defeat_effects()

            elif isinstance(evento, EventoFormacionAplicada):
                self._mostrar_mensaje(evento.mensaje)
                self.renderer.trigger_formation_change(evento.formacion)

            elif isinstance(evento, EventoUnidadEnPanico):
                self._mostrar_mensaje(evento.mensaje)
                # Efecto de pánico - partículas de miedo
                import random
                self.renderer.screen_shake = 3

    def _actualizar_highlights(self):
        """Actualiza las casillas resaltadas"""
        batalla = self.servicio_juego.obtener_batalla_actual()
        if batalla:
            movimientos = batalla.obtener_movimientos_validos_unidad_seleccionada()
            objetivos = batalla.obtener_objetivos_atacables_unidad_seleccionada()
            self.renderer.set_highlights(movimientos, objetivos)
        else:
            self.renderer.set_highlights([], [])

    def _mostrar_mensaje(self, mensaje):
        """Muestra un mensaje temporal"""
        self.mensaje_actual = mensaje
        self.tiempo_mensaje = pygame.time.get_ticks() + 3000  # 3 segundos

    def update(self, dt):
        """Actualiza el estado"""
        # Limpiar mensaje si ha pasado el tiempo
        if self.tiempo_mensaje > 0 and pygame.time.get_ticks() > self.tiempo_mensaje:
            self.mensaje_actual = ""
            self.tiempo_mensaje = 0

        # ===== NUEVO SISTEMA DE TURNO ENEMIGO PASO A PASO =====
        if self.enemy_turn_active:
            self.enemy_turn_timer += dt

            # Ejecutar siguiente acción enemiga cuando pase el delay
            if self.enemy_turn_timer >= self.enemy_turn_delay:
                self._ejecutar_ia_enemigo()
                self.enemy_turn_timer = 0  # Reset timer

        # ===== SISTEMA DE AUTO-PLAY =====
        elif self.auto_play_enabled and self.processing_state == "READY":
            batalla = self.servicio_juego.obtener_batalla_actual()

            # Solo ejecutar auto-play en turno del jugador y si la batalla no ha terminado
            if batalla and batalla.turno_actual == TurnoActual.JUGADOR and not batalla.batalla_terminada:
                self.auto_play_timer += dt

                # Ejecutar acción de IA cuando pase el delay
                if self.auto_play_timer >= self.auto_play_delay:
                    self._ejecutar_ia_jugador()
                    self.auto_play_timer = 0  # Reset timer

    def render(self, screen):
        """Renderiza la batalla"""
        batalla = self.servicio_juego.obtener_batalla_actual()
        self.renderer.render(screen, batalla)

        # Renderizar mensaje si hay uno
        if self.mensaje_actual:
            self._render_mensaje(screen)

        # Renderizar indicador de procesamiento
        if self.processing_state != "READY":
            self._render_processing_indicator(screen)

    def _render_mensaje(self, screen):
        """Renderiza un mensaje en pantalla"""
        font = pygame.font.Font(None, 36)
        text = font.render(self.mensaje_actual, True, (255, 255, 255))
        text_rect = text.get_rect(centerx=screen.get_width() // 2, y=50)

        # Fondo para el texto
        padding = 10
        bg_rect = text_rect.inflate(padding * 2, padding)
        pygame.draw.rect(screen, (139, 69, 19), bg_rect)
        pygame.draw.rect(screen, (255, 215, 0), bg_rect, 2)

        screen.blit(text, text_rect)

        # Renderizar información de tutorial si es un nivel tutorial
        if self.nivel and self.nivel.es_tutorial:
            info_font = pygame.font.Font(None, 20)
            tutorial_text = info_font.render("Presiona T para más consejos", True, (100, 200, 255))
            screen.blit(tutorial_text, (screen.get_width() - 250, screen.get_height() - 30))

    def _render_processing_indicator(self, screen):
        """Renderiza indicador de procesamiento del turno enemigo"""
        # Overlay semi-transparente
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Texto simple para turno enemigo
        text = "Turno Enemigo en progreso..."

        # Renderizar texto principal
        font = pygame.font.Font(None, 48)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2))

        # Fondo para el texto
        padding = 20
        bg_rect = text_rect.inflate(padding * 2, padding)
        pygame.draw.rect(screen, (50, 0, 0), bg_rect)
        pygame.draw.rect(screen, (200, 50, 50), bg_rect, 3)

        screen.blit(text_surface, text_rect)

        # Instrucción
        font_small = pygame.font.Font(None, 24)
        inst_text = "Por favor espere..."
        inst_surface = font_small.render(inst_text, True, (200, 200, 200))
        inst_rect = inst_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 80))
        screen.blit(inst_surface, inst_rect)

    def _mostrar_tutorial(self):
        """Muestra mensajes de tutorial secuencialmente"""
        if not self.nivel or not self.nivel.tutorial_messages:
            return

        if self.tutorial_index < len(self.nivel.tutorial_messages):
            mensaje = self.nivel.tutorial_messages[self.tutorial_index]
            self._mostrar_mensaje(f"📖 TUTORIAL: {mensaje}")
            self.tutorial_index += 1
        else:
            self._mostrar_mensaje("📖 No hay más consejos. ¡Adelante soldado!")
            self.tutorial_index = 0  # Reiniciar

    def _guardar_progreso(self):
        """Guarda el progreso de la campaña automáticamente"""
        if self.campania:
            campaign_data = self.campania.to_dict()
            if save_manager.save_campaign(campaign_data):
                print(f"[BATALLA] Progreso guardado - Nivel {self.campania.nivel_actual + 1}")
            else:
                print("[BATALLA] ERROR: No se pudo guardar el progreso")

    def _ejecutar_ia_jugador(self):
        """Ejecuta UNA acción de IA (como humano: un movimiento a la vez)"""
        from src.domain.services import CalculadorPrioridad, CalculadorCombate, CalculadorMovimiento

        batalla = self.servicio_juego.obtener_batalla_actual()
        if not batalla:
            return

        # Buscar la primera unidad que pueda actuar
        unidades_disponibles = [u for u in batalla.ejercito_jugador.unidades_vivas
                               if not u.esta_en_panico]

        # Ordenar por agresividad (igual que IAAgresiva)
        def agresividad(unidad):
            if unidad.tipo.value == "equites":
                return 3
            elif unidad.tipo.value == "sagittarii":
                return 2
            else:
                return 1

        unidades_disponibles.sort(key=agresividad, reverse=True)

        # Buscar primera unidad que pueda hacer algo
        for unidad in unidades_disponibles:
            eventos = []

            # Prioridad 1: Atacar si puede
            if unidad.puede_actuar:
                objetivos = unidad.obtener_objetivos_atacables(
                    batalla.ejercito_enemigo.unidades_vivas
                )

                if objetivos:
                    mejor_objetivo = CalculadorPrioridad.seleccionar_mejor_objetivo(
                        unidad, objetivos
                    )

                    if mejor_objetivo:
                        print(f"[AUTO-PLAY] {unidad.visualizacion.nombre} ataca a {mejor_objetivo.visualizacion.nombre}")

                        resultado = CalculadorCombate.ejecutar_ataque(unidad, mejor_objetivo)
                        eventos.append(EventoAtaqueRealizado(
                            resultado,
                            grito_guerra=unidad.visualizacion.grito_guerra
                        ))

                        if resultado.objetivo_eliminado:
                            eventos.append(EventoUnidadEliminada(
                                mejor_objetivo.id,
                                mejor_objetivo.bando,
                                mejor_objetivo.tipo.value,
                                "¡Enemigo eliminado!"
                            ))

                        # ARREGLO: Verificar si el enemigo fue completamente derrotado
                        if batalla.ejercito_enemigo.esta_derrotado:
                            from src.domain.events import EventoBatallaTerminada
                            mensaje = "¡VICTORIA! ¡Roma es eterna!"
                            eventos.append(EventoBatallaTerminada(
                                Bando.ROMA,
                                len(batalla.ejercito_jugador.unidades_vivas),
                                mensaje
                            ))
                            batalla._batalla_terminada = True
                            batalla._ganador = Bando.ROMA

                        # Procesar y salir (solo una acción)
                        self._procesar_eventos(eventos)
                        self._actualizar_highlights()
                        return

            # Prioridad 2: Moverse si puede
            if unidad.puede_moverse:
                movimientos = unidad.obtener_posiciones_movimiento_validas(batalla.tablero)

                if movimientos:
                    mejor_movimiento = CalculadorMovimiento.seleccionar_mejor_movimiento(
                        unidad, movimientos, batalla.ejercito_enemigo.unidades_vivas
                    )

                    if mejor_movimiento:
                        print(f"[AUTO-PLAY] {unidad.visualizacion.nombre} se mueve")

                        posicion_origen = unidad.posicion
                        unidad.mover_a(mejor_movimiento)

                        eventos.append(EventoUnidadMovida(
                            unidad.id,
                            posicion_origen,
                            mejor_movimiento
                        ))

                        # Procesar y salir (solo una acción)
                        self._procesar_eventos(eventos)
                        self._actualizar_highlights()
                        return

        # Si llegamos aquí, ninguna unidad puede actuar -> finalizar turno
        print("[AUTO-PLAY] No hay más acciones, finalizando turno...")

        # Cambiar turno a enemigo y activar sistema de turno enemigo
        self.servicio_juego.cambiar_turno_a_enemigo()

        # Activar sistema de turno enemigo paso a paso
        self.enemy_turn_active = True
        self.enemy_turn_timer = 0
        self.processing_state = "PROCESSING_ENEMY_TURN"

        self._mostrar_mensaje("Turno Enemigo...")

        self._actualizar_highlights()

    def _ejecutar_ia_enemigo(self):
        """Ejecuta UNA acción de IA enemiga (igual que el jugador: una acción a la vez)"""
        from src.domain.services import CalculadorPrioridad, CalculadorCombate, CalculadorMovimiento

        batalla = self.servicio_juego.obtener_batalla_actual()
        if not batalla:
            return

        # Buscar la primera unidad enemiga que pueda actuar
        unidades_disponibles = [u for u in batalla.ejercito_enemigo.unidades_vivas
                               if not u.esta_en_panico]

        # Ordenar por agresividad (igual que IAAgresiva)
        def agresividad(unidad):
            if unidad.tipo.value == "equites" or unidad.tipo.value == "caballeria_barbara":
                return 3
            elif unidad.tipo.value == "sagittarii" or unidad.tipo.value == "escaramuzadores":
                return 2
            else:
                return 1

        unidades_disponibles.sort(key=agresividad, reverse=True)

        # Buscar primera unidad que pueda hacer algo
        for unidad in unidades_disponibles:
            eventos = []

            # Prioridad 1: Atacar si puede
            if unidad.puede_actuar:
                objetivos = unidad.obtener_objetivos_atacables(
                    batalla.ejercito_jugador.unidades_vivas
                )

                if objetivos:
                    mejor_objetivo = CalculadorPrioridad.seleccionar_mejor_objetivo(
                        unidad, objetivos
                    )

                    if mejor_objetivo:
                        self._mostrar_mensaje(f"{unidad.visualizacion.nombre} ataca a {mejor_objetivo.visualizacion.nombre}")

                        resultado = CalculadorCombate.ejecutar_ataque(unidad, mejor_objetivo)
                        eventos.append(EventoAtaqueRealizado(
                            resultado,
                            grito_guerra=unidad.visualizacion.grito_guerra
                        ))

                        if resultado.objetivo_eliminado:
                            eventos.append(EventoUnidadEliminada(
                                mejor_objetivo.id,
                                mejor_objetivo.bando,
                                mejor_objetivo.tipo.value,
                                f"¡{mejor_objetivo.visualizacion.nombre} ha caído!"
                            ))

                        # Verificar si el jugador fue derrotado
                        if batalla.ejercito_jugador.esta_derrotado:
                            from src.domain.events import EventoBatallaTerminada
                            from src.domain.value_objects import Bando
                            mensaje = "¡DERROTA! Los bárbaros han vencido..."
                            eventos.append(EventoBatallaTerminada(
                                Bando.BARBAROS,
                                len(batalla.ejercito_enemigo.unidades_vivas),
                                mensaje
                            ))
                            batalla._batalla_terminada = True
                            batalla._ganador = Bando.BARBAROS

                        # Procesar eventos y retornar (solo una acción)
                        self._procesar_eventos(eventos)
                        self._actualizar_highlights()
                        return

            # Prioridad 2: Moverse si puede
            if unidad.puede_moverse:
                movimientos = unidad.obtener_posiciones_movimiento_validas(batalla.tablero)

                if movimientos:
                    mejor_movimiento = CalculadorMovimiento.seleccionar_mejor_movimiento(
                        unidad, movimientos, batalla.ejercito_jugador.unidades_vivas
                    )

                    if mejor_movimiento:
                        self._mostrar_mensaje(f"{unidad.visualizacion.nombre} avanza")

                        posicion_origen = unidad.posicion
                        unidad.mover_a(mejor_movimiento)

                        eventos.append(EventoUnidadMovida(
                            unidad.id,
                            posicion_origen,
                            mejor_movimiento
                        ))

                        # Procesar eventos y retornar (solo una acción)
                        self._procesar_eventos(eventos)
                        self._actualizar_highlights()
                        return

        # Si llegamos aquí, ninguna unidad enemiga puede actuar -> finalizar turno enemigo
        print("[IA ENEMIGA] No hay más acciones, volviendo a turno jugador...")

        # Cambiar turno de vuelta al jugador
        self.servicio_juego.cambiar_turno_a_jugador()

        # Restaurar estado READY
        self.enemy_turn_active = False
        self.processing_state = "READY"

        self._mostrar_mensaje("Tu turno")
        self._actualizar_highlights()