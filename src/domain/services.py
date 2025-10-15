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