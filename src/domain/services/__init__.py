"""
Domain services package
Provides specialized calculation and coordination services
"""

# Import with actual class names from the modules
from src.domain.services.combat_calculator import CalculadorCombate
from src.domain.services.priority_calculator import PriorityCalculator
from src.domain.services.movement_calculator import MovementCalculator
from src.domain.services.formation_calculator import FormationCalculator
from src.domain.services.focus_fire_system import FocusFireSystem
from src.domain.services.threat_evaluator import ThreatEvaluator
from src.domain.services.tactical_position_calculator import TacticalPositionCalculator
from src.domain.services.dynamic_formation_manager import DynamicFormationManager

# Maintain all Spanish class names that exist in old monolithic services.py
CalculadorPrioridad = PriorityCalculator
CalculadorMovimiento = MovementCalculator
CalculadorFormacion = FormationCalculator
SistemaFocusFire = FocusFireSystem
EvaluadorAmenazas = ThreatEvaluator
CalculadorPosicionTactica = TacticalPositionCalculator
GestorFormacionesDinamico = DynamicFormationManager

# English aliases for future use
CombatCalculator = CalculadorCombate

__all__ = [
    # Spanish class names (maintain backward compatibility)
    'CalculadorCombate',
    'CalculadorPrioridad',
    'CalculadorMovimiento',
    'CalculadorFormacion',
    'SistemaFocusFire',
    'EvaluadorAmenazas',
    'CalculadorPosicionTactica',
    'GestorFormacionesDinamico',
    # English aliases
    'CombatCalculator',
    'PriorityCalculator',
    'MovementCalculator',
    'FormationCalculator',
    'FocusFireSystem',
    'ThreatEvaluator',
    'TacticalPositionCalculator',
    'DynamicFormationManager',
]
