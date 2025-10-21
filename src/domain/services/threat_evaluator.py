"""
Threat evaluation domain service
Evaluates enemy threats and prioritizes defensive responses
"""

from typing import List, Tuple
from src.domain.entities import Unidad, Ejercito
from src.domain.value_objects import TipoUnidad
from src.domain.constants import (
    AMENAZA_PUEDE_MATAR,
    AMENAZA_HERIDA_GRAVE,
    UMBRAL_VIDA_HERIDO
)


class ThreatEvaluator:
    """Domain service for evaluating enemy threats"""

    @staticmethod
    def evaluate_threat(
        enemy_unit: Unidad,
        my_units: List[Unidad]
    ) -> float:
        """Evaluates how dangerous an enemy unit is"""
        threat = 0.0

        # If it cannot act, it's not an immediate threat
        if not enemy_unit.puede_actuar:
            return threat

        # Evaluate danger to each of my units
        for my_unit in my_units:
            # Can it reach me?
            distance = enemy_unit.posicion.distancia_manhattan(my_unit.posicion)

            # Threat from movement + attack
            if distance <= enemy_unit.estadisticas.rango_movimiento + enemy_unit.estadisticas.rango_ataque:
                potential_damage = enemy_unit.calcular_danio_contra(my_unit, 0)

                # CRITICAL: can kill me
                if potential_damage >= my_unit.vida_actual:
                    threat += AMENAZA_PUEDE_MATAR
                # HIGH: can seriously wound me
                elif potential_damage >= my_unit.vida_actual * UMBRAL_VIDA_HERIDO:
                    threat += AMENAZA_HERIDA_GRAVE
                else:
                    threat += potential_damage

        # Threat by unit type
        type_threats = {
            TipoUnidad.SAGITTARII: 100,  # Archers are very dangerous
            TipoUnidad.EQUITES: 80,      # Cavalry is mobile
            TipoUnidad.HASTATI: 60,      # Heavy infantry
        }
        threat += type_threats.get(enemy_unit.tipo, 30)

        # Healthy units are more dangerous
        threat *= enemy_unit.porcentaje_vida

        return threat

    @staticmethod
    def identify_critical_threats(
        enemy_army: Ejercito,
        allied_army: Ejercito
    ) -> List[Tuple[Unidad, float]]:
        """Identifies and sorts the most critical threats"""
        threats = []

        for enemy in enemy_army.unidades_vivas:
            threat_level = ThreatEvaluator.evaluate_threat(
                enemy,
                allied_army.unidades_vivas
            )
            if threat_level > 0:
                threats.append((enemy, threat_level))

        # Sort by threat level
        threats.sort(key=lambda x: x[1], reverse=True)
        return threats
