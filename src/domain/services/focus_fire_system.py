"""
Focus fire system domain service
Coordinates multiple attacks against priority targets
"""

from typing import List, Optional, Tuple
from src.domain.entities import Unidad
from src.domain.value_objects import TipoUnidad
from src.domain.constants import (
    MAX_ATACANTES_FOCUS_FIRE,
    PRIORIDAD_ELIMINACION_GARANTIZADA,
    UMBRAL_VIDA_CRITICA,
    PRIORIDAD_AMENAZA_CRITICA
)


class FocusFireSystem:
    """System for coordinating multiple attacks against priority targets"""

    @staticmethod
    def select_focus_target(
        available_attackers: List[Unidad],
        enemies: List[Unidad]
    ) -> Optional[Tuple[Unidad, List[Unidad]]]:
        """
        Selects the best target and which units should attack it
        Returns: (target, list_of_attackers) or None
        """
        if not available_attackers or not enemies:
            return None

        best_options = []

        for enemy in enemies:
            # Filter attackers that can reach this enemy
            attackers_in_range = [
                a for a in available_attackers
                if enemy in a.obtener_objetivos_atacables(enemies)
            ]

            if not attackers_in_range:
                continue

            # Calculate total possible damage
            total_damage = sum(
                a.calcular_danio_contra(enemy, 0)
                for a in attackers_in_range[:MAX_ATACANTES_FOCUS_FIRE]
            )

            # Priority for focus fire
            priority = 0

            # Maximum priority if we can eliminate
            if total_damage >= enemy.vida_actual:
                priority += PRIORIDAD_ELIMINACION_GARANTIZADA

            # High priority for nearly dead units
            if enemy.porcentaje_vida < UMBRAL_VIDA_CRITICA:
                priority += PRIORIDAD_AMENAZA_CRITICA

            # Priority by unit type
            type_priorities = {
                TipoUnidad.SAGITTARII: 150,  # Archers very dangerous
                TipoUnidad.EQUITES: 120,     # Mobile cavalry
                TipoUnidad.HASTATI: 80,      # Heavy infantry
            }
            priority += type_priorities.get(enemy.tipo, 50)

            # Bonus for damage efficiency
            if total_damage > 0:
                priority += (total_damage / max(1, enemy.vida_actual)) * 100

            best_options.append((
                priority,
                enemy,
                attackers_in_range[:MAX_ATACANTES_FOCUS_FIRE]
            ))

        if not best_options:
            return None

        # Select the best option
        best_options.sort(key=lambda x: x[0], reverse=True)
        _, target, attackers = best_options[0]

        return (target, attackers)
