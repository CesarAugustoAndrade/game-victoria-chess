"""
Tactical position calculation domain service
Evaluates optimal tactical positions for units
"""

from typing import List
from src.domain.entities import Unidad
from src.domain.value_objects import Posicion, TipoUnidad
from src.domain.constants import (
    DISTANCIA_COHESION_ALIADOS,
    PESO_ALIADOS_CERCANOS,
    PESO_OPORTUNIDAD_ATAQUE,
    PESO_FLANQUEO,
    PESO_RODEADO_PENALIZACION,
    PESO_INFANTERIA_DELANTE,
    PESO_DISTANCIA_SEGURA,
    PESO_ESPACIOS_LIBRES,
    PESO_LINEA_FRONTAL
)


class TacticalPositionCalculator:
    """Domain service for calculating optimal tactical positions"""

    @staticmethod
    def evaluate_position(
        position: Posicion,
        unit: Unidad,
        allies: List[Unidad],
        enemies: List[Unidad]
    ) -> float:
        """Evaluates how good a position is tactically"""
        score = 0.0

        # 1. Maintain cohesion with allies (formation)
        nearby_allies = sum(
            1 for a in allies
            if a.posicion.distancia_manhattan(position) <= DISTANCIA_COHESION_ALIADOS
            and a.id != unit.id
        )
        score += nearby_allies * PESO_ALIADOS_CERCANOS

        # 2. Evaluate flanking opportunities
        for enemy in enemies:
            enemy_distance = position.distancia_manhattan(enemy.posicion)

            # If we can attack from this position
            if enemy_distance <= unit.estadisticas.rango_ataque:
                score += PESO_OPORTUNIDAD_ATAQUE

                # Bonus for flanking (enemy between us and ally)
                for ally in allies:
                    if ally.id != unit.id:
                        if TacticalPositionCalculator._is_flanking(
                            position, ally.posicion, enemy.posicion
                        ):
                            score += PESO_FLANQUEO

        # 3. Avoid being surrounded
        adjacent_enemies = sum(
            1 for e in enemies
            if position.distancia_manhattan(e.posicion) <= 1
        )
        if adjacent_enemies > nearby_allies:
            score -= PESO_RODEADO_PENALIZACION  # Penalty for being surrounded

        # 4. Unit-type specific positioning
        if unit.tipo == TipoUnidad.SAGITTARII:
            # Archers prefer rear with infantry in front
            infantry_in_front = any(
                a.tipo in [TipoUnidad.LEGIONARIO, TipoUnidad.HASTATI, TipoUnidad.TRIARII]
                and a.posicion.fila < position.fila
                for a in allies
            )
            if infantry_in_front:
                score += PESO_INFANTERIA_DELANTE

            # Maintain distance from enemies
            closest_enemy_distance = min(
                (position.distancia_manhattan(e.posicion) for e in enemies),
                default=10
            )
            if closest_enemy_distance >= 3:
                score += PESO_DISTANCIA_SEGURA

        elif unit.tipo == TipoUnidad.EQUITES:
            # Cavalry seeks open flanks
            free_spaces = TacticalPositionCalculator._count_free_spaces(
                position, allies, enemies
            )
            score += free_spaces * PESO_ESPACIOS_LIBRES

        elif unit.tipo in [TipoUnidad.TRIARII, TipoUnidad.HASTATI]:
            # Heavy infantry forms front line
            # Bonus for being on front line with support
            enemy_nearby = any(
                e.posicion.fila < position.fila for e in enemies
            )
            if enemy_nearby and nearby_allies >= 2:
                score += PESO_LINEA_FRONTAL

        return score

    @staticmethod
    def _is_flanking(pos1: Posicion, pos2: Posicion, enemy: Posicion) -> bool:
        """Checks if two positions flank an enemy"""
        # Simplified: flanking if they are on opposite sides
        return (
            (pos1.fila < enemy.fila and pos2.fila > enemy.fila) or
            (pos1.fila > enemy.fila and pos2.fila < enemy.fila) or
            (pos1.columna < enemy.columna and pos2.columna > enemy.columna) or
            (pos1.columna > enemy.columna and pos2.columna < enemy.columna)
        )

    @staticmethod
    def _count_free_spaces(
        position: Posicion,
        allies: List[Unidad],
        enemies: List[Unidad]
    ) -> int:
        """Counts free spaces around a position"""
        spaces = 0
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if df == 0 and dc == 0:
                    continue
                new_pos = Posicion(position.fila + df, position.columna + dc)
                if new_pos.esta_dentro_del_tablero():
                    occupied = any(
                        u.posicion == new_pos
                        for u in allies + enemies
                    )
                    if not occupied:
                        spaces += 1
        return spaces
