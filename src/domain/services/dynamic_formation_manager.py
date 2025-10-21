"""
Dynamic formation management domain service
Intelligently selects optimal formations based on battle context
"""

from typing import Optional
from src.domain.entities import Ejercito
from src.domain.value_objects import TipoUnidad
from src.domain.constants import (
    BALANCE_SUPERIORIDAD_NUMERICA,
    BALANCE_INFERIORIDAD_NUMERICA,
    UMBRAL_MORAL_BAJA,
    UMBRAL_MORAL_ALTA,
    HISTORIAL_DANIO_ALTO
)


class DynamicFormationManager:
    """Intelligent formation manager based on battle context"""

    @staticmethod
    def select_optimal_formation(
        army: Ejercito,
        enemy_army: Ejercito,
        damage_history: Optional[dict] = None
    ) -> str:
        """Selects the optimal formation based on battle context"""

        # Situation analysis
        numerical_balance = len(army.unidades_vivas) / max(1, len(enemy_army.unidades_vivas))
        average_morale = army.moral_promedio

        # Count enemy unit types
        enemy_archers = sum(
            1 for u in enemy_army.unidades_vivas
            if u.tipo == TipoUnidad.SAGITTARII
        )

        # If we are taking a lot of damage -> Testudo
        if damage_history and damage_history.get('ultimo_turno', 0) > HISTORIAL_DANIO_ALTO:
            return "testudo"

        # If there are many enemy archers -> Testudo
        if enemy_archers >= 3:
            return "testudo"

        # Very low morale -> Orbis to recover
        if average_morale < UMBRAL_MORAL_BAJA:
            return "orbis"

        # Clear numerical superiority -> Cuneus for attack
        if numerical_balance > BALANCE_SUPERIORIDAD_NUMERICA and average_morale > UMBRAL_MORAL_ALTA:
            return "cuneus"

        # Numerical inferiority -> Defensive Orbis
        if numerical_balance < BALANCE_INFERIORIDAD_NUMERICA:
            return "orbis"

        # Default: standard line
        return "linea"
