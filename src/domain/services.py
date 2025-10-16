"""
Servicios de dominio para cálculos complejos
"""

import random
from typing import List, Optional, Tuple
from src.domain.entities import Unidad, Ejercito
from src.domain.value_objects import (
    TipoUnidad, Posicion, ResultadoAtaque
)


class CalculadorCombate:
    """Servicio de dominio para cálculos de combate"""

    @staticmethod
    def calcular_danio(atacante: Unidad, defensor: Unidad) -> int:
        """Calcula el daño de un ataque con varianza aleatoria"""
        varianza = random.uniform(-5, 5)
        return atacante.calcular_danio_contra(defensor, varianza)

    @staticmethod
    def ejecutar_ataque(atacante: Unidad, defensor: Unidad) -> ResultadoAtaque:
        """Ejecuta un ataque y retorna el resultado"""
        danio = CalculadorCombate.calcular_danio(atacante, defensor)

        vida_antes = defensor.vida_actual
        defensor.recibir_danio(danio)
        atacante.marcar_como_actuada()

        # Calcular pérdida de moral
        moral_perdida = min(15, danio)  # Más daño = más pérdida de moral

        return ResultadoAtaque(
            atacante_id=atacante.id,
            defensor_id=defensor.id,
            danio_infligido=danio,
            objetivo_eliminado=not defensor.esta_viva,
            moral_perdida=moral_perdida
        )

    @staticmethod
    def calcular_bonificacion_formacion(atacante: Unidad, formacion: str) -> int:
        """Calcula bonificación de ataque según formación"""
        bonus = 0
        if formacion == "cuneus":  # Formación en cuña
            if atacante.tipo in [TipoUnidad.LEGIONARIO, TipoUnidad.HASTATI]:
                bonus = 5
        elif formacion == "testudo":  # Formación tortuga
            bonus = -3  # Penalización al ataque, pero mejor defensa
        return bonus


class CalculadorPrioridad:
    """Servicio para calcular prioridad de objetivos (IA enemiga)"""

    @staticmethod
    def calcular_prioridad_objetivo(atacante: Unidad, objetivo: Unidad) -> float:
        """Calcula la prioridad de atacar un objetivo específico"""
        prioridad = 0.0

        # 1. Priorizar unidades con poca vida (rematar)
        porcentaje_vida = objetivo.porcentaje_vida
        if porcentaje_vida < 0.3:
            prioridad += 100  # Casi muertos = máxima prioridad
        elif porcentaje_vida < 0.5:
            prioridad += 50   # Heridos = alta prioridad

        # 2. Priorizar unidades de alto valor
        prioridades_tipo = {
            TipoUnidad.SAGITTARII: 45,     # Arqueros son peligrosos
            TipoUnidad.EQUITES: 40,         # Caballería es valiosa
            TipoUnidad.HASTATI: 30,         # Infantería pesada
            TipoUnidad.LEGIONARIO: 20,      # Infantería básica
            TipoUnidad.TRIARII: 25          # Piqueros
        }
        prioridad += prioridades_tipo.get(objetivo.tipo, 15)

        # 3. Bonus táctico: Triarii priorizan caballería
        if atacante.tipo == TipoUnidad.TRIARII and objetivo.tipo == TipoUnidad.EQUITES:
            prioridad += 60

        # 4. Caballería prioriza arqueros
        if atacante.tipo == TipoUnidad.EQUITES and objetivo.tipo == TipoUnidad.SAGITTARII:
            prioridad += 50

        # 5. Bonus por daño potencial
        danio_potencial = atacante.calcular_danio_contra(objetivo)
        prioridad += danio_potencial * 0.5

        # 6. Priorizar unidades en pánico
        if objetivo.esta_en_panico:
            prioridad += 30

        return prioridad

    @staticmethod
    def seleccionar_mejor_objetivo(
        atacante: Unidad,
        objetivos_disponibles: List[Unidad]
    ) -> Optional[Unidad]:
        """Selecciona el mejor objetivo basado en prioridad"""
        if not objetivos_disponibles:
            return None

        objetivos_con_prioridad = [
            (objetivo, CalculadorPrioridad.calcular_prioridad_objetivo(atacante, objetivo))
            for objetivo in objetivos_disponibles
        ]

        objetivos_con_prioridad.sort(key=lambda x: x[1], reverse=True)
        return objetivos_con_prioridad[0][0]


class CalculadorMovimiento:
    """Servicio para calcular movimientos óptimos (IA enemiga)"""

    @staticmethod
    def calcular_puntuacion_movimiento(
        unidad: Unidad,
        posicion_destino: Posicion,
        objetivos: List[Unidad]
    ) -> float:
        """Calcula la puntuación de mover a una posición específica"""
        if not objetivos:
            return 0

        mejor_puntuacion = -1

        for objetivo in objetivos:
            # Distancia al objetivo desde la nueva posición
            distancia = posicion_destino.distancia_manhattan(objetivo.posicion)

            # Puntuación base: menor distancia = mejor
            puntuacion = 100 - distancia * 10

            # Bonus por tipo de unidad
            bonus_tipo = {
                TipoUnidad.EQUITES: 40,      # Caballería quiere acercarse rápido
                TipoUnidad.TRIARII: 30,      # Piqueros avanzan con cautela
                TipoUnidad.HASTATI: 20,      # Infantería pesada avanza firme
                TipoUnidad.LEGIONARIO: 15,   # Infantería básica
                TipoUnidad.SAGITTARII: 5     # Arqueros mantienen distancia
            }
            puntuacion += bonus_tipo.get(unidad.tipo, 10)

            # Bonus por perseguir objetivos valiosos
            if objetivo.tipo == TipoUnidad.SAGITTARII:
                puntuacion += 35
            elif objetivo.tipo == TipoUnidad.EQUITES:
                puntuacion += 30

            # Bonus táctico
            if unidad.tipo == TipoUnidad.TRIARII and objetivo.tipo == TipoUnidad.EQUITES:
                puntuacion += 45
            if unidad.tipo == TipoUnidad.EQUITES and objetivo.tipo == TipoUnidad.SAGITTARII:
                puntuacion += 40

            # Bonus por perseguir heridos
            if objetivo.porcentaje_vida < 0.5:
                puntuacion += 25

            # Bonus por perseguir unidades en pánico
            if objetivo.esta_en_panico:
                puntuacion += 35

            mejor_puntuacion = max(mejor_puntuacion, puntuacion)

        return mejor_puntuacion

    @staticmethod
    def seleccionar_mejor_movimiento(
        unidad: Unidad,
        movimientos_validos: List[Posicion],
        objetivos: List[Unidad]
    ) -> Optional[Posicion]:
        """Selecciona el mejor movimiento para acercarse a objetivos"""
        if not movimientos_validos or not objetivos:
            return None

        movimientos_con_puntuacion = [
            (pos, CalculadorMovimiento.calcular_puntuacion_movimiento(unidad, pos, objetivos))
            for pos in movimientos_validos
        ]

        movimientos_con_puntuacion.sort(key=lambda x: x[1], reverse=True)

        # Si la mejor puntuación es muy baja, no moverse
        if movimientos_con_puntuacion[0][1] < 0:
            return None

        return movimientos_con_puntuacion[0][0]


class CalculadorFormacion:
    """Servicio para calcular efectos de formaciones"""

    FORMACIONES = {
        "linea": {
            "descripcion": "Formación en línea estándar",
            "bonus_ataque": 0,
            "bonus_defensa": 0,
            "bonus_moral": 5
        },
        "testudo": {
            "descripcion": "Formación tortuga defensiva",
            "bonus_ataque": -5,
            "bonus_defensa": 10,
            "bonus_moral": 15
        },
        "cuneus": {
            "descripcion": "Formación en cuña ofensiva",
            "bonus_ataque": 8,
            "bonus_defensa": -3,
            "bonus_moral": 10
        },
        "orbis": {
            "descripcion": "Formación circular defensiva",
            "bonus_ataque": -2,
            "bonus_defensa": 8,
            "bonus_moral": 20
        }
    }

    @staticmethod
    def obtener_bonificaciones(formacion: str) -> dict:
        """Obtiene las bonificaciones de una formación"""
        return CalculadorFormacion.FORMACIONES.get(
            formacion,
            CalculadorFormacion.FORMACIONES["linea"]
        )

    @staticmethod
    def es_formacion_valida(formacion: str) -> bool:
        """Verifica si una formación es válida"""
        return formacion in CalculadorFormacion.FORMACIONES


class SistemaFocusFire:
    """Sistema para coordinar ataques múltiples contra objetivos prioritarios"""

    @staticmethod
    def seleccionar_objetivo_focus(
        atacantes_disponibles: List[Unidad],
        enemigos: List[Unidad]
    ) -> Optional[Tuple[Unidad, List[Unidad]]]:
        """
        Selecciona el mejor objetivo y qué unidades deben atacarlo
        Retorna: (objetivo, lista_de_atacantes) o None
        """
        if not atacantes_disponibles or not enemigos:
            return None

        mejores_opciones = []

        for enemigo in enemigos:
            # Filtrar atacantes que pueden alcanzar este enemigo
            atacantes_alcance = [
                a for a in atacantes_disponibles
                if enemigo in a.obtener_objetivos_atacables(enemigos)
            ]

            if not atacantes_alcance:
                continue

            # Calcular daño total posible
            danio_total = sum(
                a.calcular_danio_contra(enemigo, 0)
                for a in atacantes_alcance[:3]  # Max 3 unidades
            )

            # Prioridad para focus fire
            prioridad = 0

            # Máxima prioridad si podemos eliminar
            if danio_total >= enemigo.vida_actual:
                prioridad += 1000

            # Alta prioridad para unidades casi muertas
            if enemigo.porcentaje_vida < 0.3:
                prioridad += 200

            # Prioridad por tipo de unidad
            prioridades_tipo = {
                TipoUnidad.SAGITTARII: 150,  # Arqueros muy peligrosos
                TipoUnidad.EQUITES: 120,     # Caballería móvil
                TipoUnidad.HASTATI: 80,       # Infantería pesada
            }
            prioridad += prioridades_tipo.get(enemigo.tipo, 50)

            # Bonus por eficiencia del daño
            if danio_total > 0:
                prioridad += (danio_total / max(1, enemigo.vida_actual)) * 100

            mejores_opciones.append((
                prioridad,
                enemigo,
                atacantes_alcance[:3]  # Limitar a 3 atacantes
            ))

        if not mejores_opciones:
            return None

        # Seleccionar la mejor opción
        mejores_opciones.sort(key=lambda x: x[0], reverse=True)
        _, objetivo, atacantes = mejores_opciones[0]

        return (objetivo, atacantes)


class EvaluadorAmenazas:
    """Servicio para evaluar amenazas del enemigo"""

    @staticmethod
    def evaluar_amenaza(
        unidad_enemiga: Unidad,
        mis_unidades: List[Unidad]
    ) -> float:
        """Evalúa qué tan peligrosa es una unidad enemiga"""
        amenaza = 0.0

        # Si no puede actuar, no es amenaza inmediata
        if not unidad_enemiga.puede_actuar:
            return amenaza

        # Evaluar peligro para cada una de mis unidades
        for mi_unidad in mis_unidades:
            # ¿Puede alcanzarme?
            distancia = unidad_enemiga.posicion.distancia_manhattan(mi_unidad.posicion)

            # Amenaza por movimiento + ataque
            if distancia <= unidad_enemiga.estadisticas.rango_movimiento + unidad_enemiga.estadisticas.rango_ataque:
                danio_potencial = unidad_enemiga.calcular_danio_contra(mi_unidad, 0)

                # CRÍTICO: puede matarme
                if danio_potencial >= mi_unidad.vida_actual:
                    amenaza += 500
                # ALTO: puede herirme gravemente
                elif danio_potencial >= mi_unidad.vida_actual * 0.5:
                    amenaza += 200
                else:
                    amenaza += danio_potencial

        # Amenaza por tipo de unidad
        amenazas_tipo = {
            TipoUnidad.SAGITTARII: 100,  # Arqueros son muy peligrosos
            TipoUnidad.EQUITES: 80,      # Caballería es móvil
            TipoUnidad.HASTATI: 60,      # Infantería pesada
        }
        amenaza += amenazas_tipo.get(unidad_enemiga.tipo, 30)

        # Unidades sanas son más peligrosas
        amenaza *= unidad_enemiga.porcentaje_vida

        return amenaza

    @staticmethod
    def identificar_amenazas_criticas(
        ejercito_enemigo: Ejercito,
        ejercito_aliado: Ejercito
    ) -> List[Tuple[Unidad, float]]:
        """Identifica y ordena las amenazas más críticas"""
        amenazas = []

        for enemigo in ejercito_enemigo.unidades_vivas:
            nivel_amenaza = EvaluadorAmenazas.evaluar_amenaza(
                enemigo,
                ejercito_aliado.unidades_vivas
            )
            if nivel_amenaza > 0:
                amenazas.append((enemigo, nivel_amenaza))

        # Ordenar por nivel de amenaza
        amenazas.sort(key=lambda x: x[1], reverse=True)
        return amenazas


class CalculadorPosicionTactica:
    """Servicio para calcular posiciones tácticas óptimas"""

    @staticmethod
    def evaluar_posicion(
        posicion: Posicion,
        unidad: Unidad,
        aliados: List[Unidad],
        enemigos: List[Unidad]
    ) -> float:
        """Evalúa qué tan buena es una posición tácticamente"""
        puntuacion = 0.0

        # 1. Mantener cohesión con aliados (formación)
        aliados_cercanos = sum(
            1 for a in aliados
            if a.posicion.distancia_manhattan(posicion) <= 2
            and a.id != unidad.id
        )
        puntuacion += aliados_cercanos * 20

        # 2. Evaluar oportunidades de flanqueo
        for enemigo in enemigos:
            dist_enemigo = posicion.distancia_manhattan(enemigo.posicion)

            # Si podemos atacar desde esta posición
            if dist_enemigo <= unidad.estadisticas.rango_ataque:
                puntuacion += 50

                # Bonus por flanqueo (enemigo entre nosotros y aliado)
                for aliado in aliados:
                    if aliado.id != unidad.id:
                        if CalculadorPosicionTactica._esta_flanqueando(
                            posicion, aliado.posicion, enemigo.posicion
                        ):
                            puntuacion += 100

        # 3. Evitar ser rodeado
        enemigos_adyacentes = sum(
            1 for e in enemigos
            if posicion.distancia_manhattan(e.posicion) <= 1
        )
        if enemigos_adyacentes > aliados_cercanos:
            puntuacion -= 150  # Penalización por estar rodeado

        # 4. Posicionamiento específico por tipo
        if unidad.tipo == TipoUnidad.SAGITTARII:
            # Arqueros prefieren retaguardia con infantería delante
            infanteria_delante = any(
                a.tipo in [TipoUnidad.LEGIONARIO, TipoUnidad.HASTATI, TipoUnidad.TRIARII]
                and a.posicion.fila < posicion.fila
                for a in aliados
            )
            if infanteria_delante:
                puntuacion += 80

            # Mantener distancia de enemigos
            distancia_enemigo_cercano = min(
                (posicion.distancia_manhattan(e.posicion) for e in enemigos),
                default=10
            )
            if distancia_enemigo_cercano >= 3:
                puntuacion += 60

        elif unidad.tipo == TipoUnidad.EQUITES:
            # Caballería busca flancos abiertos
            espacios_libres = CalculadorPosicionTactica._contar_espacios_libres(
                posicion, aliados, enemigos
            )
            puntuacion += espacios_libres * 15

        elif unidad.tipo in [TipoUnidad.TRIARII, TipoUnidad.HASTATI]:
            # Infantería pesada forma línea frontal
            # Bonus por estar en primera línea con apoyo
            enemigo_cercano = any(
                e.posicion.fila < posicion.fila for e in enemigos
            )
            if enemigo_cercano and aliados_cercanos >= 2:
                puntuacion += 70

        return puntuacion

    @staticmethod
    def _esta_flanqueando(pos1: Posicion, pos2: Posicion, enemigo: Posicion) -> bool:
        """Verifica si dos posiciones flanquean a un enemigo"""
        # Simplificado: flanqueo si están en lados opuestos
        return (
            (pos1.fila < enemigo.fila and pos2.fila > enemigo.fila) or
            (pos1.fila > enemigo.fila and pos2.fila < enemigo.fila) or
            (pos1.columna < enemigo.columna and pos2.columna > enemigo.columna) or
            (pos1.columna > enemigo.columna and pos2.columna < enemigo.columna)
        )

    @staticmethod
    def _contar_espacios_libres(
        posicion: Posicion,
        aliados: List[Unidad],
        enemigos: List[Unidad]
    ) -> int:
        """Cuenta espacios libres alrededor de una posición"""
        espacios = 0
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if df == 0 and dc == 0:
                    continue
                nueva_pos = Posicion(posicion.fila + df, posicion.columna + dc)
                if nueva_pos.esta_dentro_del_tablero():
                    ocupada = any(
                        u.posicion == nueva_pos
                        for u in aliados + enemigos
                    )
                    if not ocupada:
                        espacios += 1
        return espacios


class GestorFormacionesDinamico:
    """Gestor inteligente de formaciones basado en contexto"""

    @staticmethod
    def seleccionar_formacion_optima(
        ejercito: Ejercito,
        ejercito_enemigo: Ejercito,
        historial_danio: dict = None
    ) -> str:
        """Selecciona la formación óptima según el contexto de batalla"""

        # Análisis de situación
        balance_numerico = len(ejercito.unidades_vivas) / max(1, len(ejercito_enemigo.unidades_vivas))
        moral_promedio = ejercito.moral_promedio

        # Contar tipos de unidades enemigas
        arqueros_enemigos = sum(
            1 for u in ejercito_enemigo.unidades_vivas
            if u.tipo == TipoUnidad.SAGITTARII
        )

        # Si estamos recibiendo mucho daño -> Testudo
        if historial_danio and historial_danio.get('ultimo_turno', 0) > 100:
            return "testudo"

        # Si hay muchos arqueros enemigos -> Testudo
        if arqueros_enemigos >= 3:
            return "testudo"

        # Moral muy baja -> Orbis para recuperar
        if moral_promedio < 35:
            return "orbis"

        # Superioridad numérica clara -> Cuneus para ataque
        if balance_numerico > 1.5 and moral_promedio > 60:
            return "cuneus"

        # Inferioridad numérica -> Orbis defensivo
        if balance_numerico < 0.7:
            return "orbis"

        # Por defecto, línea estándar
        return "linea"