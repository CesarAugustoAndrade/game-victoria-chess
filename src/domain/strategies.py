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
    CalculadorCombate, CalculadorPrioridad, CalculadorMovimiento,
    SistemaFocusFire, EvaluadorAmenazas, CalculadorPosicionTactica,
    GestorFormacionesDinamico
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

            # Sistema flexible de puntos de acción - hacer múltiples acciones
            while unidad.puntos_accion > 0 and not unidad.esta_en_panico:
                accion_realizada = False

                # Intentar atacar si tiene PA
                if unidad.puede_atacar:
                    objetivos = unidad.obtener_objetivos_atacables(
                        ejercito_enemigo.unidades_vivas
                    )

                    if objetivos:
                        mejor_objetivo = CalculadorPrioridad.seleccionar_mejor_objetivo(
                            unidad, objetivos
                        )

                        if mejor_objetivo:
                            accion_realizada = True
                            # Añadir evento de acción IA
                            eventos.append(EventoAccionIA(
                                f"{unidad.visualizacion.nombre} ataca a {mejor_objetivo.visualizacion.nombre}",
                                "atacar"
                            ))

                            resultado = CalculadorCombate.ejecutar_ataque(
                                unidad, mejor_objetivo
                            )
                            unidad.marcar_ataque_realizado()  # Consumir PA

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
                            continue  # Siguiente iteración del while

                # Si no atacó, intentar moverse
                if not accion_realizada and unidad.puede_moverse:
                    movimientos = unidad.obtener_posiciones_movimiento_validas(tablero)

                    if movimientos:
                        mejor_movimiento = CalculadorMovimiento.seleccionar_mejor_movimiento(
                            unidad, movimientos, ejercito_enemigo.unidades_vivas
                        )

                        if mejor_movimiento:
                            accion_realizada = True
                            posicion_origen = unidad.posicion
                            unidad.mover_a(mejor_movimiento)  # Consume PA

                            eventos.append(EventoAccionIA(
                                f"{unidad.visualizacion.nombre} avanza",
                                "mover"
                            ))

                            eventos.append(EventoUnidadMovida(
                                unidad.id,
                                posicion_origen,
                                mejor_movimiento
                            ))
                            continue  # Siguiente iteración

                # Si no pudo hacer nada, terminar
                if not accion_realizada:
                    break

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
    """Estrategia de IA defensiva mejorada - inteligente pero cautelosa"""

    def __init__(self):
        self._historial_danio = {'ultimo_turno': 0}

    def ejecutar_turno(
        self,
        ejercito_controlado: Ejercito,
        ejercito_enemigo: Ejercito,
        tablero: Tablero
    ) -> List[EventoDominio]:
        eventos = []

        # Análisis de amenazas
        amenazas = EvaluadorAmenazas.identificar_amenazas_criticas(
            ejercito_enemigo, ejercito_controlado
        )

        # Aplicar formación defensiva inteligentemente
        formacion = GestorFormacionesDinamico.seleccionar_formacion_optima(
            ejercito_controlado, ejercito_enemigo, self._historial_danio
        )
        if formacion != "linea":
            ejercito_controlado.aplicar_formacion(formacion)

        # Gestionar unidades en pánico primero
        unidades_panico = ejercito_controlado.unidades_en_panico
        for unidad in unidades_panico:
            self._reagrupar_unidad(unidad, ejercito_controlado, tablero, eventos)

        # Ordenar unidades por prioridad defensiva
        unidades_ordenadas = self._ordenar_por_prioridad_defensiva(
            ejercito_controlado.unidades_vivas
        )

        for unidad in unidades_ordenadas:
            if unidad.esta_en_panico:
                continue  # Ya gestionadas

            # Evaluar si está en peligro crítico real
            en_peligro = self._evaluar_peligro_critico(
                unidad, amenazas, ejercito_enemigo
            )

            # Retirarse solo si realmente es necesario
            if en_peligro and unidad.porcentaje_vida < 0.4:
                if unidad.puede_moverse:
                    self._retirar_inteligentemente(
                        unidad, ejercito_enemigo, ejercito_controlado, tablero, eventos
                    )
                    continue

            # Atacar objetivos prioritarios (no solo heridos)
            objetivos = unidad.obtener_objetivos_atacables(
                ejercito_enemigo.unidades_vivas
            )

            if objetivos and unidad.puede_actuar:
                # Seleccionar objetivo inteligentemente
                objetivo = self._seleccionar_objetivo_defensivo(unidad, objetivos, amenazas)

                if objetivo:
                    eventos.append(EventoAccionIA(
                        f"{unidad.visualizacion.nombre} ataca defensivamente a {objetivo.visualizacion.nombre}",
                        "atacar"
                    ))

                    resultado = CalculadorCombate.ejecutar_ataque(unidad, objetivo)
                    eventos.append(EventoAtaqueRealizado(
                        resultado,
                        grito_guerra=f"¡Por Roma y la supervivencia!"
                    ))

                    if resultado.objetivo_eliminado:
                        eventos.append(EventoUnidadEliminada(
                            objetivo.id,
                            objetivo.bando,
                            objetivo.tipo.value,
                            "¡Amenaza neutralizada!"
                        ))

            # Si no atacó, mantener posición defensiva
            elif unidad.puede_moverse:
                posicion_defensiva = self._encontrar_posicion_defensiva(
                    unidad, ejercito_controlado, ejercito_enemigo, tablero
                )
                if posicion_defensiva and posicion_defensiva != unidad.posicion:
                    posicion_origen = unidad.posicion
                    unidad.mover_a(posicion_defensiva)

                    eventos.append(EventoAccionIA(
                        f"{unidad.visualizacion.nombre} toma posición defensiva",
                        "mover"
                    ))
                    eventos.append(EventoUnidadMovida(
                        unidad.id, posicion_origen, posicion_defensiva
                    ))

        return eventos

    def _evaluar_peligro_critico(self, unidad, amenazas, ejercito_enemigo):
        """Evalúa si una unidad está en peligro real crítico"""
        for amenaza, nivel in amenazas[:3]:  # Top 3 amenazas
            if amenaza.puede_actuar:
                danio = amenaza.calcular_danio_contra(unidad, 0)
                if danio >= unidad.vida_actual * 0.7:
                    return True
        return False

    def _seleccionar_objetivo_defensivo(self, unidad, objetivos, amenazas):
        """Selecciona objetivos prioritarios defensivamente"""
        # Prioridad 1: Amenazas críticas
        for amenaza, _ in amenazas[:5]:
            if amenaza in objetivos:
                return amenaza

        # Prioridad 2: Casi muertos (finiquitar)
        casi_muertos = [o for o in objetivos if o.porcentaje_vida < 0.3]
        if casi_muertos:
            return min(casi_muertos, key=lambda u: u.vida_actual)

        # Prioridad 3: Arqueros (siempre peligrosos)
        arqueros = [o for o in objetivos if o.tipo == TipoUnidad.SAGITTARII]
        if arqueros:
            return min(arqueros, key=lambda u: u.vida_actual)

        # Prioridad 4: Cualquier herido
        heridos = [o for o in objetivos if o.porcentaje_vida < 0.6]
        if heridos:
            return min(heridos, key=lambda u: u.vida_actual)

        # Si no hay buenos objetivos, no atacar (mantener defensiva)
        return None

    def _retirar_inteligentemente(self, unidad, ejercito_enemigo, ejercito_aliado, tablero, eventos):
        """Retirada inteligente manteniendo cohesión"""
        movimientos = unidad.obtener_posiciones_movimiento_validas(tablero)
        if not movimientos:
            return

        # Evaluar cada posición por seguridad
        mejor_posicion = None
        mejor_puntuacion = -float('inf')

        for pos in movimientos:
            puntuacion = 0
            # Alejarse de enemigos
            for enemigo in ejercito_enemigo.unidades_vivas:
                puntuacion += pos.distancia_manhattan(enemigo.posicion) * 10

            # Pero mantenerse cerca de aliados
            for aliado in ejercito_aliado.unidades_vivas:
                if aliado.id != unidad.id:
                    dist_aliado = pos.distancia_manhattan(aliado.posicion)
                    if dist_aliado <= 3:
                        puntuacion += 20

            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_posicion = pos

        if mejor_posicion:
            posicion_origen = unidad.posicion
            unidad.mover_a(mejor_posicion)

            eventos.append(EventoAccionIA(
                f"{unidad.visualizacion.nombre} se retira tácticamente",
                "mover"
            ))
            eventos.append(EventoUnidadMovida(
                unidad.id, posicion_origen, mejor_posicion
            ))

    def _reagrupar_unidad(self, unidad, ejercito, tablero, eventos):
        """Reagrupa unidades en pánico cerca de aliados con buena moral"""
        if not unidad.puede_moverse:
            return

        movimientos = unidad.obtener_posiciones_movimiento_validas(tablero)
        if not movimientos:
            return

        # Buscar posición cerca de aliados con buena moral
        mejor_pos = None
        mejor_moral = 0

        for pos in movimientos:
            moral_cercana = 0
            for aliado in ejercito.unidades_vivas:
                if aliado.id != unidad.id:
                    dist = pos.distancia_manhattan(aliado.posicion)
                    if dist <= 2:
                        moral_cercana += aliado.moral_actual

            if moral_cercana > mejor_moral:
                mejor_moral = moral_cercana
                mejor_pos = pos

        if mejor_pos:
            posicion_origen = unidad.posicion
            unidad.mover_a(mejor_pos)
            eventos.append(EventoAccionIA(
                f"{unidad.visualizacion.nombre} se reagrupa con aliados",
                "mover"
            ))
            eventos.append(EventoUnidadMovida(
                unidad.id, posicion_origen, mejor_pos
            ))

    def _encontrar_posicion_defensiva(self, unidad, ejercito_aliado, ejercito_enemigo, tablero):
        """Encuentra la mejor posición defensiva"""
        movimientos = unidad.obtener_posiciones_movimiento_validas(tablero)
        if not movimientos:
            return None

        mejor_pos = None
        mejor_puntuacion = -float('inf')

        for pos in movimientos:
            puntuacion = CalculadorPosicionTactica.evaluar_posicion(
                pos, unidad,
                ejercito_aliado.unidades_vivas,
                ejercito_enemigo.unidades_vivas
            )

            # Bonus defensivo por estar en retaguardia
            if unidad.tipo == TipoUnidad.SAGITTARII:
                puntuacion += 50

            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_pos = pos

        return mejor_pos if mejor_pos != unidad.posicion else None

    def _ordenar_por_prioridad_defensiva(self, unidades):
        """Ordena unidades por prioridad de acción defensiva"""
        def prioridad(unidad):
            # Arqueros y unidades heridas actúan primero
            prio = 0
            if unidad.tipo == TipoUnidad.SAGITTARII:
                prio += 100
            if unidad.porcentaje_vida < 0.5:
                prio += 80
            return prio

        return sorted(unidades, key=prioridad, reverse=True)


class IATactica(EstrategiaIA):
    """Estrategia de IA táctica avanzada con coordinación real de unidades"""

    def __init__(self):
        self._historial_danio = {'ultimo_turno': 0, 'total': 0}
        self._unidades_procesadas = set()

    def ejecutar_turno(
        self,
        ejercito_controlado: Ejercito,
        ejercito_enemigo: Ejercito,
        tablero: Tablero
    ) -> List[EventoDominio]:
        eventos = []
        self._unidades_procesadas.clear()

        # 1. Análisis táctico completo
        amenazas = EvaluadorAmenazas.identificar_amenazas_criticas(
            ejercito_enemigo, ejercito_controlado
        )

        # 2. Selección inteligente de formación
        formacion = GestorFormacionesDinamico.seleccionar_formacion_optima(
            ejercito_controlado, ejercito_enemigo, self._historial_danio
        )
        if formacion != "linea":
            ejercito_controlado.aplicar_formacion(formacion)

        # 3. Clasificar unidades por rol táctico
        frontline = self._identificar_frontline(ejercito_controlado)
        apoyo = self._identificar_apoyo(ejercito_controlado)
        flanqueadores = self._identificar_flanqueadores(ejercito_controlado)

        # 4. FASE 1: Focus Fire coordinado en amenazas críticas
        eventos_focus = self._ejecutar_focus_fire(
            ejercito_controlado, ejercito_enemigo, amenazas
        )
        eventos.extend(eventos_focus)

        # 5. FASE 2: Maniobras de flanqueo
        eventos_flanqueo = self._ejecutar_flanqueo(
            flanqueadores, ejercito_enemigo, tablero
        )
        eventos.extend(eventos_flanqueo)

        # 6. FASE 3: Mantener línea frontal
        eventos_frontline = self._mantener_linea_frontal(
            frontline, ejercito_enemigo, ejercito_controlado, tablero
        )
        eventos.extend(eventos_frontline)

        # 7. FASE 4: Posicionar unidades de apoyo
        eventos_apoyo = self._posicionar_apoyo(
            apoyo, frontline, ejercito_enemigo, tablero
        )
        eventos.extend(eventos_apoyo)

        # 8. FASE 5: Limpiar unidades restantes
        eventos_restantes = self._procesar_unidades_restantes(
            ejercito_controlado, ejercito_enemigo, tablero
        )
        eventos.extend(eventos_restantes)

        return eventos

    def _ejecutar_focus_fire(self, ejercito_controlado, ejercito_enemigo, amenazas):
        """Ejecuta ataques coordinados contra objetivos prioritarios"""
        eventos = []

        # Obtener unidades disponibles para focus fire
        atacantes_disponibles = [
            u for u in ejercito_controlado.unidades_vivas
            if u.puede_actuar and u.id not in self._unidades_procesadas
        ]

        # Intentar focus fire en las top 2 amenazas
        for amenaza, _ in amenazas[:2]:
            if not amenaza.esta_viva:
                continue

            resultado_focus = SistemaFocusFire.seleccionar_objetivo_focus(
                atacantes_disponibles, [amenaza]
            )

            if resultado_focus:
                objetivo, atacantes = resultado_focus

                # Ejecutar ataques coordinados
                for atacante in atacantes:
                    if atacante.puede_actuar and atacante.id not in self._unidades_procesadas:
                        # Verificar si está en rango
                        if objetivo in atacante.obtener_objetivos_atacables([objetivo]):
                            eventos.append(EventoAccionIA(
                                f"FOCUS FIRE: {atacante.visualizacion.nombre} → {objetivo.visualizacion.nombre}",
                                "atacar"
                            ))

                            resultado = CalculadorCombate.ejecutar_ataque(atacante, objetivo)
                            eventos.append(EventoAtaqueRealizado(
                                resultado,
                                grito_guerra="¡Concentren fuego!"
                            ))

                            self._unidades_procesadas.add(atacante.id)

                            if resultado.objetivo_eliminado:
                                eventos.append(EventoUnidadEliminada(
                                    objetivo.id, objetivo.bando, objetivo.tipo.value,
                                    "¡Objetivo prioritario eliminado!"
                                ))
                                break  # No seguir atacando si ya está muerto

                        # Si no está en rango, intentar acercarse
                        elif atacante.puede_moverse:
                            nueva_pos = self._buscar_posicion_para_atacar(
                                atacante, objetivo, ejercito_controlado, ejercito_enemigo, tablero
                            )
                            if nueva_pos:
                                pos_origen = atacante.posicion
                                atacante.mover_a(nueva_pos)
                                eventos.append(EventoAccionIA(
                                    f"{atacante.visualizacion.nombre} se posiciona para focus fire",
                                    "mover"
                                ))
                                eventos.append(EventoUnidadMovida(
                                    atacante.id, pos_origen, nueva_pos
                                ))

                                # Intentar atacar después de mover
                                if atacante.puede_actuar and objetivo in atacante.obtener_objetivos_atacables([objetivo]):
                                    resultado = CalculadorCombate.ejecutar_ataque(atacante, objetivo)
                                    eventos.append(EventoAtaqueRealizado(
                                        resultado,
                                        grito_guerra="¡Al ataque coordinado!"
                                    ))
                                    self._unidades_procesadas.add(atacante.id)

                # Actualizar lista de atacantes disponibles
                atacantes_disponibles = [
                    a for a in atacantes_disponibles
                    if a.id not in self._unidades_procesadas
                ]

        return eventos

    def _ejecutar_flanqueo(self, flanqueadores, ejercito_enemigo, tablero):
        """Ejecuta maniobras de flanqueo con caballería y unidades móviles"""
        eventos = []

        for unidad in flanqueadores:
            if unidad.id in self._unidades_procesadas or not unidad.puede_moverse:
                continue

            # Buscar posición de flanqueo
            posicion_flanqueo = self._buscar_posicion_flanqueo(
                unidad, ejercito_enemigo, tablero
            )

            if posicion_flanqueo:
                pos_origen = unidad.posicion
                unidad.mover_a(posicion_flanqueo)

                eventos.append(EventoAccionIA(
                    f"{unidad.visualizacion.nombre} ejecuta maniobra de flanqueo",
                    "mover"
                ))
                eventos.append(EventoUnidadMovida(
                    unidad.id, pos_origen, posicion_flanqueo
                ))

                # Atacar desde posición de flanqueo
                if unidad.puede_actuar:
                    objetivos = unidad.obtener_objetivos_atacables(
                        ejercito_enemigo.unidades_vivas
                    )
                    if objetivos:
                        # Priorizar arqueros enemigos desde flanqueo
                        arqueros = [o for o in objetivos if o.tipo == TipoUnidad.SAGITTARII]
                        objetivo = arqueros[0] if arqueros else objetivos[0]

                        resultado = CalculadorCombate.ejecutar_ataque(unidad, objetivo)
                        eventos.append(EventoAtaqueRealizado(
                            resultado,
                            grito_guerra="¡Por el flanco!"
                        ))

                        if resultado.objetivo_eliminado:
                            eventos.append(EventoUnidadEliminada(
                                objetivo.id, objetivo.bando, objetivo.tipo.value,
                                "¡Flanqueo exitoso!"
                            ))

                self._unidades_procesadas.add(unidad.id)

        return eventos

    def _mantener_linea_frontal(self, frontline, ejercito_enemigo, ejercito_aliado, tablero):
        """Mantiene una línea frontal cohesiva"""
        eventos = []

        for unidad in frontline:
            if unidad.id in self._unidades_procesadas:
                continue

            # Atacar si hay objetivos
            if unidad.puede_actuar:
                objetivos = unidad.obtener_objetivos_atacables(
                    ejercito_enemigo.unidades_vivas
                )
                if objetivos:
                    objetivo = CalculadorPrioridad.seleccionar_mejor_objetivo(
                        unidad, objetivos
                    )
                    if objetivo:
                        resultado = CalculadorCombate.ejecutar_ataque(unidad, objetivo)
                        eventos.append(EventoAtaqueRealizado(
                            resultado,
                            grito_guerra="¡Mantened la línea!"
                        ))

                        if resultado.objetivo_eliminado:
                            eventos.append(EventoUnidadEliminada(
                                objetivo.id, objetivo.bando, objetivo.tipo.value,
                                "¡Línea frontal victoriosa!"
                            ))
                        self._unidades_procesadas.add(unidad.id)
                        continue

            # Si no atacó, mantener posición o avanzar
            if unidad.puede_moverse:
                mejor_pos = self._encontrar_posicion_linea(
                    unidad, frontline, ejercito_enemigo, tablero
                )
                if mejor_pos and mejor_pos != unidad.posicion:
                    pos_origen = unidad.posicion
                    unidad.mover_a(mejor_pos)

                    eventos.append(EventoAccionIA(
                        f"{unidad.visualizacion.nombre} mantiene formación",
                        "mover"
                    ))
                    eventos.append(EventoUnidadMovida(
                        unidad.id, pos_origen, mejor_pos
                    ))

                    # Intentar atacar tras avanzar
                    if unidad.puede_actuar:
                        objetivos = unidad.obtener_objetivos_atacables(
                            ejercito_enemigo.unidades_vivas
                        )
                        if objetivos:
                            objetivo = objetivos[0]
                            resultado = CalculadorCombate.ejecutar_ataque(unidad, objetivo)
                            eventos.append(EventoAtaqueRealizado(resultado))

                self._unidades_procesadas.add(unidad.id)

        return eventos

    def _posicionar_apoyo(self, apoyo, frontline, ejercito_enemigo, tablero):
        """Posiciona unidades de apoyo (arqueros) detrás de la línea frontal"""
        eventos = []

        for unidad in apoyo:
            if unidad.id in self._unidades_procesadas:
                continue

            # Atacar si hay objetivos
            if unidad.puede_actuar:
                objetivos = unidad.obtener_objetivos_atacables(
                    ejercito_enemigo.unidades_vivas
                )
                if objetivos:
                    # Arqueros priorizan otros arqueros o unidades débiles
                    objetivo = max(objetivos, key=lambda o: (
                        100 if o.tipo == TipoUnidad.SAGITTARII else 0
                    ) - o.vida_actual)

                    resultado = CalculadorCombate.ejecutar_ataque(unidad, objetivo)
                    eventos.append(EventoAtaqueRealizado(
                        resultado,
                        grito_guerra="¡Lluvia de proyectiles!"
                    ))

                    if resultado.objetivo_eliminado:
                        eventos.append(EventoUnidadEliminada(
                            objetivo.id, objetivo.bando, objetivo.tipo.value,
                            "¡Apoyo efectivo!"
                        ))
                    self._unidades_procesadas.add(unidad.id)
                    continue

            # Buscar posición segura detrás de línea frontal
            if unidad.puede_moverse:
                mejor_pos = self._buscar_posicion_apoyo(
                    unidad, frontline, ejercito_enemigo, tablero
                )
                if mejor_pos and mejor_pos != unidad.posicion:
                    pos_origen = unidad.posicion
                    unidad.mover_a(mejor_pos)

                    eventos.append(EventoAccionIA(
                        f"{unidad.visualizacion.nombre} toma posición de apoyo",
                        "mover"
                    ))
                    eventos.append(EventoUnidadMovida(
                        unidad.id, pos_origen, mejor_pos
                    ))

                self._unidades_procesadas.add(unidad.id)

        return eventos

    def _procesar_unidades_restantes(self, ejercito_controlado, ejercito_enemigo, tablero):
        """Procesa unidades que no fueron asignadas a roles específicos"""
        eventos = []

        for unidad in ejercito_controlado.unidades_vivas:
            if unidad.id in self._unidades_procesadas or unidad.esta_en_panico:
                continue

            # Usar comportamiento agresivo básico
            if unidad.puede_actuar:
                objetivos = unidad.obtener_objetivos_atacables(
                    ejercito_enemigo.unidades_vivas
                )
                if objetivos:
                    objetivo = CalculadorPrioridad.seleccionar_mejor_objetivo(
                        unidad, objetivos
                    )
                    if objetivo:
                        resultado = CalculadorCombate.ejecutar_ataque(unidad, objetivo)
                        eventos.append(EventoAtaqueRealizado(resultado))

                        if resultado.objetivo_eliminado:
                            eventos.append(EventoUnidadEliminada(
                                objetivo.id, objetivo.bando, objetivo.tipo.value,
                                "¡Victoria táctica!"
                            ))

            elif unidad.puede_moverse:
                movimientos = unidad.obtener_posiciones_movimiento_validas(tablero)
                if movimientos:
                    mejor_mov = CalculadorMovimiento.seleccionar_mejor_movimiento(
                        unidad, movimientos, ejercito_enemigo.unidades_vivas
                    )
                    if mejor_mov:
                        pos_origen = unidad.posicion
                        unidad.mover_a(mejor_mov)
                        eventos.append(EventoUnidadMovida(
                            unidad.id, pos_origen, mejor_mov
                        ))

        return eventos

    # Métodos auxiliares para clasificación de unidades
    def _identificar_frontline(self, ejercito):
        """Identifica unidades de línea frontal"""
        return [
            u for u in ejercito.unidades_vivas
            if u.tipo in [TipoUnidad.HASTATI, TipoUnidad.TRIARII, TipoUnidad.LEGIONARIO]
            and not u.esta_en_panico
        ]

    def _identificar_apoyo(self, ejercito):
        """Identifica unidades de apoyo (arqueros)"""
        return [
            u for u in ejercito.unidades_vivas
            if u.tipo == TipoUnidad.SAGITTARII
            and not u.esta_en_panico
        ]

    def _identificar_flanqueadores(self, ejercito):
        """Identifica unidades para flanqueo (caballería)"""
        return [
            u for u in ejercito.unidades_vivas
            if u.tipo == TipoUnidad.EQUITES
            and not u.esta_en_panico
        ]

    # Métodos auxiliares de posicionamiento
    def _buscar_posicion_para_atacar(self, unidad, objetivo, aliados, enemigos, tablero):
        """Busca la mejor posición para atacar un objetivo"""
        movimientos = unidad.obtener_posiciones_movimiento_validas(tablero)
        if not movimientos:
            return None

        posiciones_ataque = []
        for pos in movimientos:
            dist = pos.distancia_manhattan(objetivo.posicion)
            if dist <= unidad.estadisticas.rango_ataque:
                puntuacion = CalculadorPosicionTactica.evaluar_posicion(
                    pos, unidad, aliados.unidades_vivas, enemigos.unidades_vivas
                )
                posiciones_ataque.append((pos, puntuacion))

        if posiciones_ataque:
            posiciones_ataque.sort(key=lambda x: x[1], reverse=True)
            return posiciones_ataque[0][0]

        # Si no hay posición de ataque, acercarse
        return min(movimientos, key=lambda p: p.distancia_manhattan(objetivo.posicion))

    def _buscar_posicion_flanqueo(self, unidad, enemigos, tablero):
        """Busca posición óptima para flanqueo"""
        movimientos = unidad.obtener_posiciones_movimiento_validas(tablero)
        if not movimientos:
            return None

        mejor_pos = None
        mejor_puntuacion = -float('inf')

        for pos in movimientos:
            puntuacion = 0
            # Preferir columnas laterales
            puntuacion += abs(pos.columna - 3) * 30  # Centro es columna 3 en tablero 7x9

            # Bonus por poder atacar arqueros
            for enemigo in enemigos.unidades_vivas:
                if enemigo.tipo == TipoUnidad.SAGITTARII:
                    dist = pos.distancia_manhattan(enemigo.posicion)
                    if dist <= unidad.estadisticas.rango_ataque:
                        puntuacion += 100

            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_pos = pos

        return mejor_pos

    def _encontrar_posicion_linea(self, unidad, frontline, enemigos, tablero):
        """Encuentra posición para mantener línea frontal"""
        movimientos = unidad.obtener_posiciones_movimiento_validas(tablero)
        if not movimientos:
            return None

        mejor_pos = None
        mejor_puntuacion = -float('inf')

        for pos in movimientos:
            puntuacion = 0

            # Mantener alineación horizontal con otros frontline
            for aliado in frontline:
                if aliado.id != unidad.id:
                    if abs(pos.fila - aliado.posicion.fila) <= 1:
                        puntuacion += 30

            # Acercarse a enemigos pero no demasiado
            dist_enemigo_cercano = min(
                (pos.distancia_manhattan(e.posicion) for e in enemigos.unidades_vivas),
                default=10
            )
            if 1 <= dist_enemigo_cercano <= 2:
                puntuacion += 50

            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_pos = pos

        return mejor_pos

    def _buscar_posicion_apoyo(self, unidad, frontline, enemigos, tablero):
        """Busca posición segura para unidades de apoyo"""
        movimientos = unidad.obtener_posiciones_movimiento_validas(tablero)
        if not movimientos:
            return None

        mejor_pos = None
        mejor_puntuacion = -float('inf')

        for pos in movimientos:
            puntuacion = 0

            # Estar detrás de línea frontal
            for front in frontline:
                if pos.fila > front.posicion.fila:  # Asumiendo que enemigo está en filas bajas
                    puntuacion += 40

            # Mantener distancia de enemigos
            dist_enemigo = min(
                (pos.distancia_manhattan(e.posicion) for e in enemigos.unidades_vivas),
                default=10
            )
            if dist_enemigo >= 3:
                puntuacion += 60

            # Poder atacar desde posición segura
            for enemigo in enemigos.unidades_vivas:
                if pos.distancia_manhattan(enemigo.posicion) <= unidad.estadisticas.rango_ataque:
                    puntuacion += 30

            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_pos = pos

        return mejor_pos