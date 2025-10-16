"""
Estrategias de IA para el enemigo
"""

from abc import ABC, abstractmethod
from typing import List
import random
from src.domain.entities import Ejercito, Tablero
from src.domain.events import (
    EventoDominio, EventoAccionIA, EventoUnidadMovida,
    EventoAtaqueRealizado, EventoUnidadEliminada
)
from src.domain.services import (
    CalculadorCombate, CalculadorPrioridad, CalculadorMovimiento
)
from src.domain.value_objects import TipoUnidad


class EstrategiaIA(ABC):
    """Interfaz para estrategias de IA"""

    @abstractmethod
    def ejecutar_turno(
        self,
        ejercito_controlado: Ejercito,
        ejercito_enemigo: Ejercito,
        tablero: Tablero
    ) -> List[EventoDominio]:
        """Ejecuta el turno de la IA y retorna eventos generados"""
        pass


class IAAgresiva(EstrategiaIA):
    """Estrategia de IA agresiva que prioriza ataque sobre movimiento"""

    def ejecutar_turno(
        self,
        ejercito_controlado: Ejercito,
        ejercito_enemigo: Ejercito,
        tablero: Tablero
    ) -> List[EventoDominio]:
        eventos = []

        # Ordenar unidades: Caballería y arqueros primero (más agresivos)
        unidades_ordenadas = self._ordenar_por_agresividad(
            ejercito_controlado.unidades_vivas
        )

        for unidad in unidades_ordenadas:
            if unidad.esta_en_panico:
                continue  # Las unidades en pánico no actúan

            # Prioridad 1: Atacar si es posible
            objetivos = unidad.obtener_objetivos_atacables(
                ejercito_enemigo.unidades_vivas
            )

            if objetivos and unidad.puede_actuar:
                mejor_objetivo = CalculadorPrioridad.seleccionar_mejor_objetivo(
                    unidad, objetivos
                )

                if mejor_objetivo:
                    # Añadir evento de acción IA
                    eventos.append(EventoAccionIA(
                        f"{unidad.visualizacion.nombre} ataca a {mejor_objetivo.visualizacion.nombre}",
                        "atacar"
                    ))

                    resultado = CalculadorCombate.ejecutar_ataque(
                        unidad, mejor_objetivo
                    )
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

            # Prioridad 2: Moverse hacia enemigos si no puede atacar
            # NOTA: Cambiado de elif a if para permitir moverse Y luego atacar
            if not objetivos and unidad.puede_moverse:
                movimientos = unidad.obtener_posiciones_movimiento_validas(tablero)

                if movimientos:
                    mejor_movimiento = CalculadorMovimiento.seleccionar_mejor_movimiento(
                        unidad, movimientos, ejercito_enemigo.unidades_vivas
                    )

                    if mejor_movimiento:
                        posicion_origen = unidad.posicion
                        unidad.mover_a(mejor_movimiento)

                        eventos.append(EventoAccionIA(
                            f"{unidad.visualizacion.nombre} avanza",
                            "mover"
                        ))

                        eventos.append(EventoUnidadMovida(
                            unidad.id,
                            posicion_origen,
                            mejor_movimiento
                        ))

                        # Prioridad 3: Intentar atacar después de moverse
                        objetivos_despues_mover = unidad.obtener_objetivos_atacables(
                            ejercito_enemigo.unidades_vivas
                        )

                        if objetivos_despues_mover and unidad.puede_actuar:
                            mejor_objetivo = CalculadorPrioridad.seleccionar_mejor_objetivo(
                                unidad, objetivos_despues_mover
                            )

                            if mejor_objetivo:
                                eventos.append(EventoAccionIA(
                                    f"{unidad.visualizacion.nombre} ataca a {mejor_objetivo.visualizacion.nombre}",
                                    "atacar"
                                ))

                                resultado = CalculadorCombate.ejecutar_ataque(
                                    unidad, mejor_objetivo
                                )
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

        return eventos

    def _ordenar_por_agresividad(self, unidades: List) -> List:
        """Ordena unidades por nivel de agresividad"""
        def prioridad(unidad) -> int:
            prioridades = {
                TipoUnidad.EQUITES: 5,      # Caballería muy agresiva
                TipoUnidad.SAGITTARII: 4,   # Arqueros atacan desde lejos
                TipoUnidad.HASTATI: 3,      # Infantería pesada
                TipoUnidad.LEGIONARIO: 2,   # Infantería básica
                TipoUnidad.TRIARII: 1       # Piqueros defensivos
            }
            return prioridades.get(unidad.tipo, 0)

        return sorted(unidades, key=prioridad, reverse=True)


class IADefensiva(EstrategiaIA):
    """Estrategia de IA defensiva que prioriza supervivencia"""

    def ejecutar_turno(
        self,
        ejercito_controlado: Ejercito,
        ejercito_enemigo: Ejercito,
        tablero: Tablero
    ) -> List[EventoDominio]:
        eventos = []

        # Aplicar formación defensiva si la moral es baja
        if ejercito_controlado.moral_promedio < 50:
            ejercito_controlado.aplicar_formacion("testudo")

        for unidad in ejercito_controlado.unidades_vivas:
            if unidad.esta_en_panico:
                # Las unidades en pánico intentan retirarse
                self._retirar_unidad(unidad, tablero, eventos)
                continue

            # Si tiene poca vida, priorizar retirada
            if unidad.porcentaje_vida < 0.3 and unidad.puede_moverse:
                self._retirar_unidad(unidad, tablero, eventos)
                continue

            # Atacar solo si es seguro
            objetivos = unidad.obtener_objetivos_atacables(
                ejercito_enemigo.unidades_vivas
            )

            if objetivos and unidad.puede_actuar:
                # Seleccionar el objetivo más débil
                objetivo_debil = min(objetivos, key=lambda u: u.vida_actual)

                if objetivo_debil.porcentaje_vida < 0.5:  # Solo atacar heridos
                    resultado = CalculadorCombate.ejecutar_ataque(
                        unidad, objetivo_debil
                    )
                    eventos.append(EventoAtaqueRealizado(resultado))

                    if resultado.objetivo_eliminado:
                        eventos.append(EventoUnidadEliminada(
                            objetivo_debil.id,
                            objetivo_debil.bando,
                            objetivo_debil.tipo.value,
                            "¡Enemigo eliminado!"
                        ))

        return eventos

    def _retirar_unidad(self, unidad, tablero, eventos):
        """Hace que una unidad se retire del combate"""
        movimientos = unidad.obtener_posiciones_movimiento_validas(tablero)
        if movimientos:
            # Elegir la posición más alejada de los enemigos
            posicion_segura = max(movimientos, key=lambda p: p.fila)
            posicion_origen = unidad.posicion
            unidad.mover_a(posicion_segura)

            eventos.append(EventoAccionIA(
                f"{unidad.visualizacion.nombre} se retira",
                "mover"
            ))

            eventos.append(EventoUnidadMovida(
                unidad.id,
                posicion_origen,
                posicion_segura
            ))


class IATactica(EstrategiaIA):
    """Estrategia de IA táctica que usa formaciones y maniobras"""

    def ejecutar_turno(
        self,
        ejercito_controlado: Ejercito,
        ejercito_enemigo: Ejercito,
        tablero: Tablero
    ) -> List[EventoDominio]:
        eventos = []

        # Analizar situación táctica
        balance_fuerzas = len(ejercito_controlado.unidades_vivas) / max(1, len(ejercito_enemigo.unidades_vivas))

        # Elegir formación según situación
        if balance_fuerzas > 1.5:
            # Superioridad numérica: formación agresiva
            ejercito_controlado.aplicar_formacion("cuneus")
            estrategia = "agresiva"
        elif balance_fuerzas < 0.7:
            # Inferioridad numérica: formación defensiva
            ejercito_controlado.aplicar_formacion("orbis")
            estrategia = "defensiva"
        else:
            # Fuerzas equilibradas: formación estándar
            ejercito_controlado.aplicar_formacion("linea")
            estrategia = "equilibrada"

        # Ejecutar según estrategia elegida
        if estrategia == "agresiva":
            eventos.extend(self._ejecutar_ataque_coordinado(
                ejercito_controlado, ejercito_enemigo, tablero
            ))
        elif estrategia == "defensiva":
            eventos.extend(self._ejecutar_defensa_coordinada(
                ejercito_controlado, ejercito_enemigo, tablero
            ))
        else:
            eventos.extend(self._ejecutar_maniobra_tactica(
                ejercito_controlado, ejercito_enemigo, tablero
            ))

        return eventos

    def _ejecutar_ataque_coordinado(self, ejercito_controlado, ejercito_enemigo, tablero):
        """Ejecuta un ataque coordinado con todas las unidades"""
        eventos = []
        # Implementación simplificada
        ia_agresiva = IAAgresiva()
        return ia_agresiva.ejecutar_turno(ejercito_controlado, ejercito_enemigo, tablero)

    def _ejecutar_defensa_coordinada(self, ejercito_controlado, ejercito_enemigo, tablero):
        """Ejecuta una defensa coordinada"""
        eventos = []
        ia_defensiva = IADefensiva()
        return ia_defensiva.ejecutar_turno(ejercito_controlado, ejercito_enemigo, tablero)

    def _ejecutar_maniobra_tactica(self, ejercito_controlado, ejercito_enemigo, tablero):
        """Ejecuta maniobras tácticas complejas"""
        # Por ahora, usar estrategia agresiva
        ia_agresiva = IAAgresiva()
        return ia_agresiva.ejecutar_turno(ejercito_controlado, ejercito_enemigo, tablero)