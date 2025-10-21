"""
Formation calculation domain service
Handles formation effects and bonuses
"""


class FormationCalculator:
    """Domain service for calculating formation effects"""

    FORMATIONS = {
        "linea": {
            "description": "Standard line formation",
            "attack_bonus": 0,
            "defense_bonus": 0,
            "morale_bonus": 5
        },
        "testudo": {
            "description": "Defensive turtle formation",
            "attack_bonus": -5,
            "defense_bonus": 10,
            "morale_bonus": 15
        },
        "cuneus": {
            "description": "Offensive wedge formation",
            "attack_bonus": 8,
            "defense_bonus": -3,
            "morale_bonus": 10
        },
        "orbis": {
            "description": "Defensive circular formation",
            "attack_bonus": -2,
            "defense_bonus": 8,
            "morale_bonus": 20
        }
    }

    @staticmethod
    def get_bonuses(formation: str) -> dict:
        """Gets the bonuses for a formation"""
        return FormationCalculator.FORMATIONS.get(
            formation,
            FormationCalculator.FORMATIONS["linea"]
        )

    @staticmethod
    def is_valid_formation(formation: str) -> bool:
        """Checks if a formation is valid"""
        return formation in FormationCalculator.FORMATIONS
