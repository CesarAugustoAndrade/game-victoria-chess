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
                # Finalizar turno
                if batalla.turno_actual == TurnoActual.JUGADOR:
                    eventos = self.servicio_juego.finalizar_turno()
                    self._procesar_eventos(eventos)

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

    def render(self, screen):
        """Renderiza la batalla"""
        batalla = self.servicio_juego.obtener_batalla_actual()
        self.renderer.render(screen, batalla)

        # Renderizar mensaje si hay uno
        if self.mensaje_actual:
            self._render_mensaje(screen)

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