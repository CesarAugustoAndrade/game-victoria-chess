"""
Estado de batalla táctica romana
"""

import pygame
from src.core.state import State
from src.application.servicio_juego import ServicioJuego
from src.presentation.battle_renderer import BattleRenderer
from src.domain.value_objects import TurnoActual, Bando
from src.domain.events import *


class BatallaState(State):
    """Estado de batalla táctica"""

    def __init__(self, game):
        super().__init__(game)
        self.servicio_juego = ServicioJuego()
        self.renderer = BattleRenderer()
        self.eventos_pendientes = []
        self.mensaje_actual = ""
        self.tiempo_mensaje = 0

    def on_enter(self):
        """Inicia la batalla cuando se entra al estado"""
        eventos = self.servicio_juego.iniciar_nueva_batalla("normal")
        self._procesar_eventos(eventos)

    def handle_event(self, event):
        """Maneja eventos de pygame"""
        batalla = self.servicio_juego.obtener_batalla_actual()
        if not batalla:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Volver al menú
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
                eventos = self.servicio_juego.seleccionar_unidad(unidad_en_pos.id)
                self._procesar_eventos(eventos)
                self._actualizar_highlights()
        else:
            # Mover unidad seleccionada si el movimiento es válido
            if batalla.unidad_seleccionada:
                movimientos = batalla.obtener_movimientos_validos_unidad_seleccionada()
                if posicion in movimientos:
                    eventos = self.servicio_juego.mover_unidad(posicion.fila, posicion.columna)
                    self._procesar_eventos(eventos)
                    self._actualizar_highlights()
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
                    eventos = self.servicio_juego.atacar_enemigo(unidad.id)
                    self._procesar_eventos(eventos)
                    self._actualizar_highlights()
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
        """Procesa eventos del dominio"""
        for evento in eventos:
            # Mostrar mensajes según el tipo de evento
            if isinstance(evento, EventoBatallaIniciada):
                self._mostrar_mensaje(evento.mensaje)

            elif isinstance(evento, EventoAtaqueRealizado):
                if evento.grito_guerra:
                    self._mostrar_mensaje(evento.grito_guerra)

            elif isinstance(evento, EventoUnidadEliminada):
                self._mostrar_mensaje(evento.mensaje)

            elif isinstance(evento, EventoBatallaTerminada):
                self._mostrar_mensaje(evento.mensaje)
                if evento.ganador == Bando.ROMA:
                    self._mostrar_mensaje("¡VICTORIA! Presiona R para jugar de nuevo")
                else:
                    self._mostrar_mensaje("¡DERROTA! Presiona R para intentar de nuevo")

            elif isinstance(evento, EventoFormacionAplicada):
                self._mostrar_mensaje(evento.mensaje)

            elif isinstance(evento, EventoUnidadEnPanico):
                self._mostrar_mensaje(evento.mensaje)

            # Aquí se pueden agregar animaciones para cada evento

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