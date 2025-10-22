"""
Entidad raíz Batalla - Agregado principal del dominio
"""

from typing import List, Optional
from src.domain.entities import Ejercito, Tablero, Unidad
from src.domain.value_objects import (
    Bando, TurnoActual, Posicion
)
from src.domain.events import *
from src.domain.exceptions import *
from src.domain.services import CalculadorCombate
from src.domain.strategies import EstrategiaIA
from src.domain.abilities import TipoAccion, ContextoHabilidad
from src.domain.ability_effects import obtener_efecto, EventoHabilidadUsada
from src.domain.services.center_control import ControlCentro


class Batalla:
    """Agregado raíz que representa una batalla completa"""

    def __init__(
        self,
        ejercito_jugador: Ejercito,
        ejercito_enemigo: Ejercito,
        tablero: Tablero,
        estrategia_ia: EstrategiaIA
    ):
        self._ejercito_jugador = ejercito_jugador
        self._ejercito_enemigo = ejercito_enemigo
        self._tablero = tablero
        self._estrategia_ia = estrategia_ia
        self._ronda_actual = 1
        self._turno_actual = TurnoActual.JUGADOR
        self._unidad_seleccionada: Optional[Unidad] = None
        self._eventos_pendientes: List[EventoDominio] = []
        self._batalla_terminada = False
        self._ganador: Optional[Bando] = None

        # Strategic mechanics
        self._control_centro = ControlCentro(tablero)
        self._eliminaciones_turno = 0
        self._bando_atacante_turno = None

        # Registrar ejércitos en el tablero
        tablero.registrar_ejercito(ejercito_jugador)
        tablero.registrar_ejercito(ejercito_enemigo)

    # Propiedades de solo lectura
    @property
    def ronda_actual(self) -> int:
        return self._ronda_actual

    @property
    def turno_actual(self) -> TurnoActual:
        return self._turno_actual

    @property
    def batalla_terminada(self) -> bool:
        return self._batalla_terminada

    @property
    def ganador(self) -> Optional[Bando]:
        return self._ganador

    @property
    def ejercito_jugador(self) -> Ejercito:
        return self._ejercito_jugador

    @property
    def ejercito_enemigo(self) -> Ejercito:
        return self._ejercito_enemigo

    @property
    def tablero(self) -> Tablero:
        return self._tablero

    @property
    def unidad_seleccionada(self) -> Optional[Unidad]:
        return self._unidad_seleccionada

    def iniciar(self) -> List[EventoDominio]:
        """Inicia la batalla"""
        evento = EventoBatallaIniciada(
            self._ronda_actual,
            "¡ROMA INVICTA! ¡La batalla comienza!"
        )
        self._eventos_pendientes.append(evento)
        return self._consumir_eventos()

    def seleccionar_unidad(self, id_unidad: str) -> List[EventoDominio]:
        """Selecciona una unidad del jugador"""
        if self._turno_actual != TurnoActual.JUGADOR:
            raise ExcepcionTurnoInvalido("No es el turno del jugador")

        if self._batalla_terminada:
            raise ExcepcionEstadoInvalido("La batalla ha terminado")

        unidad = self._ejercito_jugador.obtener_unidad_por_id(id_unidad)

        if unidad is None:
            # Intentar seleccionar unidad enemiga para ver información
            unidad_enemiga = self._ejercito_enemigo.obtener_unidad_por_id(id_unidad)
            if unidad_enemiga:
                # Solo mostrar información, no seleccionar
                return []
            raise ExcepcionUnidadNoEncontrada(f"Unidad {id_unidad} no encontrada")

        if not unidad.puede_actuar and not unidad.puede_moverse:
            raise ExcepcionAccionInvalida("La unidad ya actuó este turno")

        self._unidad_seleccionada = unidad

        evento = EventoUnidadSeleccionada(
            unidad.id,
            unidad.tipo.value,
            unidad.posicion
        )
        self._eventos_pendientes.append(evento)

        return self._consumir_eventos()

    def deseleccionar_unidad(self) -> None:
        """Deselecciona la unidad actual"""
        self._unidad_seleccionada = None

    def mover_unidad_seleccionada(self, posicion: Posicion) -> List[EventoDominio]:
        """Mueve la unidad seleccionada a una posición"""
        if self._unidad_seleccionada is None:
            raise ExcepcionAccionInvalida("No hay unidad seleccionada")

        if not self._unidad_seleccionada.puede_moverse:
            raise ExcepcionMovimientoInvalido("La unidad ya se movió")

        # Validar que el movimiento sea válido
        movimientos_validos = self._unidad_seleccionada.obtener_posiciones_movimiento_validas(
            self._tablero
        )

        if posicion not in movimientos_validos:
            raise ExcepcionMovimientoInvalido("Movimiento inválido")

        posicion_origen = self._unidad_seleccionada.posicion
        self._unidad_seleccionada.mover_a(posicion)

        evento = EventoUnidadMovida(
            self._unidad_seleccionada.id,
            posicion_origen,
            posicion
        )
        self._eventos_pendientes.append(evento)

        # Si la unidad ya no puede actuar, deseleccionarla
        if not self._unidad_seleccionada.puede_actuar:
            self._unidad_seleccionada = None

        return self._consumir_eventos()

    def atacar_con_unidad_seleccionada(self, id_objetivo: str) -> List[EventoDominio]:
        """Ataca con la unidad seleccionada"""
        if self._unidad_seleccionada is None:
            raise ExcepcionAccionInvalida("No hay unidad seleccionada")

        if not self._unidad_seleccionada.puede_actuar:
            raise ExcepcionAccionInvalida("La unidad ya actuó")

        objetivo = self._ejercito_enemigo.obtener_unidad_por_id(id_objetivo)

        if objetivo is None:
            raise ExcepcionUnidadNoEncontrada("Objetivo no encontrado")

        # Validar que el ataque sea válido
        objetivos_validos = self._unidad_seleccionada.obtener_objetivos_atacables(
            self._ejercito_enemigo.unidades_vivas
        )

        if objetivo not in objetivos_validos:
            raise ExcepcionAtaqueInvalido("Objetivo fuera de rango")

        # Ejecutar ataque
        resultado = CalculadorCombate.ejecutar_ataque(
            self._unidad_seleccionada,
            objetivo
        )

        # Si el ataque fue bloqueado, emitir evento especial
        if resultado.bloqueado:
            self._eventos_pendientes.append(EventoAtaqueBloqueado(
                self._unidad_seleccionada.id,
                objetivo.id,
                self._unidad_seleccionada.estadisticas.ataque,
                objetivo.estadisticas.defensa
            ))

        # Añadir grito de guerra
        grito = self._unidad_seleccionada.visualizacion.grito_guerra
        self._eventos_pendientes.append(
            EventoAtaqueRealizado(resultado, grito)
        )

        if resultado.objetivo_eliminado:
            # Track elimination for massacre
            self._eliminaciones_turno += 1
            if self._bando_atacante_turno != Bando.ROMA:
                self._bando_atacante_turno = Bando.ROMA

            # Deducir moral del ejército por la pérdida
            moral_anterior = self._ejercito_enemigo.moral_general
            self._ejercito_enemigo.perder_moral_por_unidad(objetivo)
            moral_nueva = self._ejercito_enemigo.moral_general

            self._eventos_pendientes.append(EventoUnidadEliminada(
                objetivo.id,
                objetivo.bando,
                objetivo.tipo.value,
                f"¡{objetivo.visualizacion.nombre} ha caído!"
            ))

            # Emitir evento de cambio de moral
            self._eventos_pendientes.append(EventoMoralGeneralCambiada(
                objetivo.bando,
                moral_anterior,
                moral_nueva,
                "unidad_eliminada",
                f"¡El ejército enemigo pierde {objetivo.estadisticas.costo_moral} de moral!"
            ))

            self._ejercito_enemigo.remover_unidades_muertas()

            # Check for tactical massacre (3+ kills in one turn)
            self._verificar_masacre_tactica()

        # Verificar pánico
        if objetivo.esta_viva and objetivo.esta_en_panico:
            self._eventos_pendientes.append(EventoUnidadEnPanico(
                objetivo.id,
                objetivo.moral_actual,
                f"¡{objetivo.visualizacion.nombre} está en pánico!"
            ))

        # Verificar si el enemigo fue derrotado
        if self._ejercito_enemigo.esta_derrotado:
            self._finalizar_batalla(Bando.ROMA)

        self._unidad_seleccionada = None
        return self._consumir_eventos()

    def finalizar_turno_jugador(self) -> List[EventoDominio]:
        """Finaliza el turno del jugador e inicia turno enemigo"""
        if self._turno_actual != TurnoActual.JUGADOR:
            raise ExcepcionTurnoInvalido("No es el turno del jugador")

        if self._batalla_terminada:
            return []

        self._unidad_seleccionada = None
        self._turno_actual = TurnoActual.ENEMIGO

        # Ejecutar turno de IA
        eventos_ia = self._estrategia_ia.ejecutar_turno(
            self._ejercito_enemigo,
            self._ejercito_jugador,
            self._tablero
        )

        self._eventos_pendientes.extend(eventos_ia)

        # Remover unidades muertas del jugador y ajustar moral
        unidades_eliminadas = self._ejercito_jugador.remover_unidades_muertas()

        for unidad in unidades_eliminadas:
            # Deducir moral del ejército
            moral_anterior = self._ejercito_jugador.moral_general
            self._ejercito_jugador.perder_moral_por_unidad(unidad)
            moral_nueva = self._ejercito_jugador.moral_general

            self._eventos_pendientes.append(EventoUnidadEliminada(
                unidad.id,
                unidad.bando,
                unidad.tipo.value,
                f"¡{unidad.visualizacion.nombre} ha caído!"
            ))

            # Emitir evento de cambio de moral
            self._eventos_pendientes.append(EventoMoralGeneralCambiada(
                unidad.bando,
                moral_anterior,
                moral_nueva,
                "unidad_eliminada",
                f"¡Tu ejército pierde {unidad.estadisticas.costo_moral} de moral!"
            ))

        # Verificar si el jugador fue derrotado
        if self._ejercito_jugador.esta_derrotado:
            self._finalizar_batalla(Bando.BARBAROS)
        else:
            # Iniciar nuevo turno del jugador
            self._iniciar_nuevo_turno_jugador()

        return self._consumir_eventos()

    def aplicar_formacion(self, formacion: str) -> List[EventoDominio]:
        """Aplica una formación al ejército del jugador"""
        if self._turno_actual != TurnoActual.JUGADOR:
            raise ExcepcionTurnoInvalido("No es el turno del jugador")

        self._ejercito_jugador.aplicar_formacion(formacion)

        descripcion_formacion = {
            "testudo": "¡Formación Tortuga! Defensa aumentada",
            "cuneus": "¡Formación en Cuña! Ataque aumentado",
            "orbis": "¡Formación Circular! Moral restaurada",
            "linea": "¡Formación en Línea! Posición estándar"
        }

        evento = EventoFormacionAplicada(
            Bando.ROMA,
            formacion,
            descripcion_formacion.get(formacion, "Formación aplicada")
        )
        self._eventos_pendientes.append(evento)

        return self._consumir_eventos()

    def obtener_movimientos_validos_unidad_seleccionada(self) -> List[Posicion]:
        """Obtiene movimientos válidos de la unidad seleccionada"""
        if self._unidad_seleccionada is None:
            return []

        if not self._unidad_seleccionada.puede_moverse:
            return []

        return self._unidad_seleccionada.obtener_posiciones_movimiento_validas(
            self._tablero
        )

    def obtener_objetivos_atacables_unidad_seleccionada(self) -> List[Unidad]:
        """Obtiene objetivos atacables de la unidad seleccionada"""
        if self._unidad_seleccionada is None:
            return []

        if not self._unidad_seleccionada.puede_actuar:
            return []

        return self._unidad_seleccionada.obtener_objetivos_atacables(
            self._ejercito_enemigo.unidades_vivas
        )

    def usar_habilidad_con_unidad_seleccionada(self, nombre_habilidad: str, objetivo: Optional[Posicion] = None) -> List[EventoDominio]:
        """Usa una habilidad de la unidad seleccionada"""
        if self._unidad_seleccionada is None:
            raise ExcepcionAccionInvalida("No hay unidad seleccionada")

        if not self._unidad_seleccionada.puede_realizar_accion(TipoAccion.HABILIDAD):
            raise ExcepcionAccionInvalida("La unidad no puede usar habilidades ahora")

        # Get the ability
        habilidad = self._unidad_seleccionada.gestor_habilidades.obtener_habilidad_activa(nombre_habilidad)
        if not habilidad:
            raise ExcepcionAccionInvalida(f"La unidad no tiene la habilidad {nombre_habilidad}")

        if not habilidad.puede_usar():
            raise ExcepcionAccionInvalida(f"La habilidad {nombre_habilidad} está en cooldown o sin usos")

        # Get the effect implementation
        efecto = obtener_efecto(nombre_habilidad.lower().replace(" ", "_").replace("¡", "").replace("!", ""))
        if not efecto:
            # No specific effect, just use the ability and generate event
            habilidad.usar()
            self._unidad_seleccionada.marcar_como_actuada()

            evento = EventoHabilidadUsada(
                unidad_id=self._unidad_seleccionada.id,
                habilidad_nombre=nombre_habilidad,
                cooldown=habilidad.cooldown_maximo,
                descripcion=habilidad.descripcion
            )
            self._eventos_pendientes.append(evento)
            self._unidad_seleccionada = None
            return self._consumir_eventos()

        # Prepare context for ability effect
        contexto = ContextoHabilidad(
            unidad_origen=self._unidad_seleccionada,
            ejercito_aliado=self._ejercito_jugador,
            ejercito_enemigo=self._ejercito_enemigo,
            tablero=self._tablero,
            objetivo=objetivo
        )

        # Apply the effect
        try:
            eventos_habilidad = efecto.aplicar(contexto)
            self._eventos_pendientes.extend(eventos_habilidad)

            # Use the ability (set cooldown)
            habilidad.usar()
            self._unidad_seleccionada.marcar_como_actuada()

        except Exception as e:
            raise ExcepcionAccionInvalida(f"Error al usar habilidad: {str(e)}")

        self._unidad_seleccionada = None
        return self._consumir_eventos()

    def _iniciar_nuevo_turno_jugador(self) -> None:
        """Inicia un nuevo turno del jugador"""
        self._ejercito_jugador.reiniciar_turno_todas_unidades()
        self._ejercito_enemigo.reiniciar_turno_todas_unidades()
        self._ronda_actual += 1
        self._turno_actual = TurnoActual.JUGADOR

        # Reset massacre counter for new turn
        self._eliminaciones_turno = 0
        self._bando_atacante_turno = None

        # Check center control and apply penalties
        eventos_centro = self._control_centro.evaluar_control_al_final_turno(
            self._ejercito_jugador,
            self._ejercito_enemigo
        )
        self._eventos_pendientes.extend(eventos_centro)

        evento = EventoTurnoFinalizado(
            TurnoActual.ENEMIGO,
            TurnoActual.JUGADOR,
            self._ronda_actual
        )
        self._eventos_pendientes.append(evento)

    def _finalizar_batalla(self, ganador: Bando) -> None:
        """Finaliza la batalla"""
        self._batalla_terminada = True
        self._ganador = ganador

        ejercito_superviviente = (
            self._ejercito_jugador if ganador == Bando.ROMA
            else self._ejercito_enemigo
        )

        ejercito_derrotado = (
            self._ejercito_enemigo if ganador == Bando.ROMA
            else self._ejercito_jugador
        )

        # Determinar la razón de la victoria
        if ejercito_derrotado.moral_general <= 0:
            razon = "¡La moral enemiga se ha roto!"
        else:
            razon = "¡El enemigo ha sido aniquilado!"

        mensaje = (f"¡VICTORIA! {razon} ¡Roma es eterna!" if ganador == Bando.ROMA
                  else f"¡DERROTA! {razon} Los bárbaros han vencido...")

        evento = EventoBatallaTerminada(
            ganador,
            len(ejercito_superviviente.unidades_vivas),
            mensaje
        )
        self._eventos_pendientes.append(evento)

    def _consumir_eventos(self) -> List[EventoDominio]:
        """Consume y retorna los eventos pendientes"""
        eventos = self._eventos_pendientes.copy()
        self._eventos_pendientes.clear()
        return eventos

    def _verificar_masacre_tactica(self) -> None:
        """Check and apply tactical massacre bonus/penalty"""
        UMBRAL_MASACRE = 3
        MORAL_PERDIDA_ENEMIGO = 10
        MORAL_GANADA_PROPIA = 5

        if self._eliminaciones_turno >= UMBRAL_MASACRE:
            if self._bando_atacante_turno == Bando.ROMA:
                # Player achieved massacre
                self._ejercito_enemigo.perder_moral(MORAL_PERDIDA_ENEMIGO)
                self._ejercito_jugador.ganar_moral(MORAL_GANADA_PROPIA)
            else:
                # AI achieved massacre
                self._ejercito_jugador.perder_moral(MORAL_PERDIDA_ENEMIGO)
                self._ejercito_enemigo.ganar_moral(MORAL_GANADA_PROPIA)

            self._eventos_pendientes.append(EventoMasacreTactica(
                bando_atacante=self._bando_atacante_turno,
                unidades_eliminadas=self._eliminaciones_turno,
                moral_enemiga_perdida=MORAL_PERDIDA_ENEMIGO,
                moral_propia_ganada=MORAL_GANADA_PROPIA
            ))

    def obtener_casillas_centro(self) -> List[Posicion]:
        """Get center tiles for UI display"""
        return self._control_centro.casillas_centrales

    def obtener_eliminaciones_turno(self) -> int:
        """Get current turn eliminations for UI counter"""
        return self._eliminaciones_turno

    def obtener_control_centro_estado(self) -> dict:
        """Get center control status"""
        return self._control_centro.obtener_estadisticas_control()