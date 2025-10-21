"""
Priority calculation domain service
Calculates target priorities for AI decision making
"""

from typing import List, Optional
from src.domain.entities import Unidad
from src.domain.value_objects import TipoUnidad
from src.domain.constants import (
    UMBRAL_VIDA_CRITICA, UMBRAL_VIDA_HERIDO,
    PRIORIDAD_CASI_MUERTO, PRIORIDAD_HERIDO,
    PRIORIDAD_SAGITTARII, PRIORIDAD_EQUITES,
    PRIORIDAD_HASTATI, PRIORIDAD_LEGIONARIO,
    PRIORIDAD_TRIARII, PRIORIDAD_GENERICA,
    PRIORIDAD_UNIDAD_PANICO
)


class PriorityCalculator:
    """Domain service for calculating target priorities (AI enemies)"""

    @staticmethod
    def calculate_target_priority(attacker: Unidad, target: Unidad) -> float:
        """Calculates the priority of attacking a specific target"""
        priority = 0.0

        # 1. Prioritize low health units (finish them off)
        health_percentage = target.porcentaje_vida
        if health_percentage < UMBRAL_VIDA_CRITICA:
            priority += PRIORIDAD_CASI_MUERTO  # Nearly dead = maximum priority
        elif health_percentage < UMBRAL_VIDA_HERIDO:
            priority += PRIORIDAD_HERIDO  # Wounded = high priority

        # 2. Prioritize high-value units
        type_priorities = {
            TipoUnidad.SAGITTARII: PRIORIDAD_SAGITTARII,  # Archers are dangerous
            TipoUnidad.EQUITES: PRIORIDAD_EQUITES,  # Cavalry is valuable
            TipoUnidad.HASTATI: PRIORIDAD_HASTATI,  # Heavy infantry
            TipoUnidad.LEGIONARIO: PRIORIDAD_LEGIONARIO,  # Basic infantry
            TipoUnidad.TRIARII: PRIORIDAD_TRIARII  # Pikemen
        }
        priority += type_priorities.get(target.tipo, PRIORIDAD_GENERICA)

        # 3. Tactical bonus: Triarii prioritize cavalry
        if attacker.tipo == TipoUnidad.TRIARII and target.tipo == TipoUnidad.EQUITES:
            priority += 60

        # 4. Cavalry prioritizes archers
        if attacker.tipo == TipoUnidad.EQUITES and target.tipo == TipoUnidad.SAGITTARII:
            priority += 50

        # 5. Bonus for potential damage
        potential_damage = attacker.calcular_danio_contra(target)
        priority += potential_damage * 0.5

        # 6. Prioritize panicked units
        if target.esta_en_panico:
            priority += PRIORIDAD_UNIDAD_PANICO

        return priority

    @staticmethod
    def select_best_target(
        attacker: Unidad,
        available_targets: List[Unidad]
    ) -> Optional[Unidad]:
        """Selects the best target based on priority"""
        if not available_targets:
            return None

        targets_with_priority = [
            (target, PriorityCalculator.calculate_target_priority(attacker, target))
            for target in available_targets
        ]

        targets_with_priority.sort(key=lambda x: x[1], reverse=True)
        return targets_with_priority[0][0]

    # Spanish method name aliases for backward compatibility
    @staticmethod
    def calcular_prioridad_objetivo(atacante: Unidad, objetivo: Unidad) -> float:
        """Alias in Spanish for calculate_target_priority"""
        return PriorityCalculator.calculate_target_priority(atacante, objetivo)

    @staticmethod
    def seleccionar_mejor_objetivo(
        atacante: Unidad,
        objetivos_disponibles: List[Unidad]
    ) -> Optional[Unidad]:
        """Alias in Spanish for select_best_target"""
        return PriorityCalculator.select_best_target(atacante, objetivos_disponibles)
