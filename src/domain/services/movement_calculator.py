"""
Movement calculation domain service
Calculates optimal movements for AI units
"""

from typing import List, Optional
from src.domain.entities import Unidad
from src.domain.value_objects import Posicion, TipoUnidad


class MovementCalculator:
    """Domain service for calculating optimal movements (AI enemies)"""

    @staticmethod
    def calculate_movement_score(
        unit: Unidad,
        destination_position: Posicion,
        targets: List[Unidad]
    ) -> float:
        """Calculates the score of moving to a specific position"""
        if not targets:
            return 0

        best_score = -1

        for target in targets:
            # Distance to target from new position
            distance = destination_position.distancia_manhattan(target.posicion)

            # Base score: shorter distance = better
            score = 100 - distance * 10

            # Bonus by unit type
            type_bonus = {
                TipoUnidad.EQUITES: 40,      # Cavalry wants to close quickly
                TipoUnidad.TRIARII: 30,      # Pikemen advance cautiously
                TipoUnidad.HASTATI: 20,      # Heavy infantry advances firmly
                TipoUnidad.LEGIONARIO: 15,   # Basic infantry
                TipoUnidad.SAGITTARII: 5     # Archers keep distance
            }
            score += type_bonus.get(unit.tipo, 10)

            # Bonus for chasing valuable targets
            if target.tipo == TipoUnidad.SAGITTARII:
                score += 35
            elif target.tipo == TipoUnidad.EQUITES:
                score += 30

            # Tactical bonus
            if unit.tipo == TipoUnidad.TRIARII and target.tipo == TipoUnidad.EQUITES:
                score += 45
            if unit.tipo == TipoUnidad.EQUITES and target.tipo == TipoUnidad.SAGITTARII:
                score += 40

            # Bonus for chasing wounded
            if target.porcentaje_vida < 0.5:
                score += 25

            # Bonus for chasing panicked units
            if target.esta_en_panico:
                score += 35

            best_score = max(best_score, score)

        return best_score

    @staticmethod
    def select_best_movement(
        unit: Unidad,
        valid_movements: List[Posicion],
        targets: List[Unidad]
    ) -> Optional[Posicion]:
        """Selects the best movement to approach targets"""
        if not valid_movements or not targets:
            return None

        movements_with_score = [
            (pos, MovementCalculator.calculate_movement_score(unit, pos, targets))
            for pos in valid_movements
        ]

        movements_with_score.sort(key=lambda x: x[1], reverse=True)

        # If the best score is very low, don't move
        if movements_with_score[0][1] < 0:
            return None

        return movements_with_score[0][0]

    # Spanish method name aliases for backward compatibility
    @staticmethod
    def calcular_puntuacion_movimiento(
        unidad: Unidad,
        posicion_destino: Posicion,
        objetivos: List[Unidad]
    ) -> float:
        """Alias in Spanish for calculate_movement_score"""
        return MovementCalculator.calculate_movement_score(unidad, posicion_destino, objetivos)

    @staticmethod
    def seleccionar_mejor_movimiento(
        unidad: Unidad,
        movimientos_validos: List[Posicion],
        objetivos: List[Unidad]
    ) -> Optional[Posicion]:
        """Alias in Spanish for select_best_movement"""
        return MovementCalculator.select_best_movement(unidad, movimientos_validos, objetivos)
