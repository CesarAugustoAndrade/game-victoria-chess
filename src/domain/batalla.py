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

        # Ejecutar ataque (ahora retorna info de crítico)
        resultado, es_critico, multiplicador = CalculadorCombate.ejecutar_ataque(
            self._unidad_seleccionada,
            objetivo
        )

        # Añadir grito de guerra
        grito = self._unidad_seleccionada.visualizacion.grito_guerra
        self._eventos_pendientes.append(
            EventoAtaqueRealizado(resultado, grito)
        )

        # Si fue crítico, emitir evento épico
        if es_critico:
            mensaje_critico = "¡GOLPE CRÍTICO!" if multiplicador == 2.0 else "¡¡¡CRÍTICO DEVASTADOR!!!"
            self._eventos_pendientes.append(EventoCriticoRealizado(
                atacante_id=self._unidad_seleccionada.id,
                defensor_id=objetivo.id,
                danio_total=resultado.danio_infligido,
                multiplicador=multiplicador,
                posicion=objetivo.posicion,
                mensaje=mensaje_critico
            ))

            # Activar cámara lenta para críticos
            duracion = 800 if multiplicador == 2.0 else 1200  # Más lento para devastadores
            self._eventos_pendientes.append(EventoCamaraLenta(
                duracion_ms=duracion,
                motivo="critico",
                intensidad=0.3 if multiplicador == 2.0 else 0.2  # Más lento para devastadores
            ))

        if resultado.objetivo_eliminado:
            # Registrar kill para el feed
            self._eventos_pendientes.append(EventoKillRegistrado(
                asesino_id=self._unidad_seleccionada.id,
                victima_id=objetivo.id,
                asesino_tipo=self._unidad_seleccionada.tipo.value,
                victima_tipo=objetivo.tipo.value,
                asesino_bando=self._unidad_seleccionada.bando,
                victima_bando=objetivo.bando,
                fue_critico=es_critico,
                posicion=objetivo.posicion
            ))

            self._eventos_pendientes.append(EventoUnidadEliminada(
                objetivo.id,
                objetivo.bando,
                objetivo.tipo.value,
                f"¡{objetivo.visualizacion.nombre} ha caído!"
            ))
            self._ejercito_enemigo.remover_unidades_muertas()

            # Cámara lenta para última unidad enemiga
            if len(self._ejercito_enemigo.unidades_vivas) == 0:
                self._eventos_pendientes.append(EventoCamaraLenta(
                    duracion_ms=1500,
                    motivo="ultima_unidad",
                    intensidad=0.25
                ))

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

        # Remover unidades muertas del jugador
        unidades_eliminadas = self._ejercito_jugador.remover_unidades_muertas()

        for unidad in unidades_eliminadas:
            self._eventos_pendientes.append(EventoUnidadEliminada(
                unidad.id,
                unidad.bando,
                unidad.tipo.value,
                f"¡{unidad.visualizacion.nombre} ha caído!"
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

    def _iniciar_nuevo_turno_jugador(self) -> None:
        """Inicia un nuevo turno del jugador"""
        self._ejercito_jugador.reiniciar_turno_todas_unidades()
        self._ejercito_enemigo.reiniciar_turno_todas_unidades()
        self._ronda_actual += 1
        self._turno_actual = TurnoActual.JUGADOR

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

        mensaje = ("¡VICTORIA! ¡Roma es eterna!" if ganador == Bando.ROMA
                  else "¡DERROTA! Los bárbaros han vencido...")

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