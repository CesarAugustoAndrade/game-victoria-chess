"""
Abilities system for Classic Battle Rules
Implements special abilities with cooldowns for tactical depth
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from enum import Enum

from src.domain.value_objects import Bando, TipoUnidad
from src.domain.events import EventoDominio


class TipoHabilidad(Enum):
    """Types of abilities"""
    ACTIVA = "activa"  # Requires activation, has cooldown
    PASIVA = "pasiva"  # Always active, no cooldown


class TipoAccion(Enum):
    """Action types units can perform in a turn"""
    MOVER = "mover"
    ATACAR = "atacar"
    DEFENDER = "defender"
    HABILIDAD = "habilidad"
    NINGUNA = "ninguna"  # No action yet


@dataclass
class HabilidadActiva:
    """Active ability with cooldown management"""
    nombre: str
    descripcion: str
    cooldown_maximo: int
    cooldown_actual: int = 0
    usos_maximos: Optional[int] = None
    usos_restantes: Optional[int] = None
    rango: int = 0  # Range of effect (0 = self only)

    def __post_init__(self):
        """Initialize uses if limited"""
        if self.usos_maximos is not None and self.usos_restantes is None:
            self.usos_restantes = self.usos_maximos

    def puede_usar(self) -> bool:
        """Check if ability can be used"""
        return (self.cooldown_actual == 0 and
                (self.usos_restantes is None or self.usos_restantes > 0))

    def usar(self):
        """Use the ability, setting cooldown and reducing uses"""
        if not self.puede_usar():
            raise ValueError(f"Ability {self.nombre} cannot be used now")

        self.cooldown_actual = self.cooldown_maximo
        if self.usos_restantes is not None:
            self.usos_restantes -= 1

    def reducir_cooldown(self):
        """Reduce cooldown by 1 (called each turn)"""
        if self.cooldown_actual > 0:
            self.cooldown_actual -= 1

    def resetear(self):
        """Reset ability for new battle"""
        self.cooldown_actual = 0
        if self.usos_maximos is not None:
            self.usos_restantes = self.usos_maximos


@dataclass
class HabilidadPasiva:
    """Passive ability that's always active"""
    nombre: str
    descripcion: str
    modificadores: Dict[str, Any] = field(default_factory=dict)


class EfectoHabilidad(ABC):
    """Abstract base for ability effects"""

    @abstractmethod
    def aplicar(self, contexto: 'ContextoHabilidad') -> List[EventoDominio]:
        """Apply the ability effect"""
        pass


@dataclass
class ContextoHabilidad:
    """Context for applying ability effects"""
    unidad_origen: Any  # The unit using the ability
    ejercito_aliado: Any  # Allied army
    ejercito_enemigo: Any  # Enemy army
    tablero: Any  # The board
    objetivo: Optional[Any] = None  # Target unit/position if applicable

    def obtener_unidades_en_rango(self, rango: int) -> List[Any]:
        """Get all allied units within range"""
        unidades_en_rango = []
        for unidad in self.ejercito_aliado.unidades_vivas:
            if unidad.id == self.unidad_origen.id:
                continue
            distancia = self.unidad_origen.posicion.distancia_manhattan(unidad.posicion)
            if distancia <= rango:
                unidades_en_rango.append(unidad)
        return unidades_en_rango

    def obtener_enemigos_en_rango(self, rango: int) -> List[Any]:
        """Get all enemy units within range"""
        enemigos_en_rango = []
        for unidad in self.ejercito_enemigo.unidades_vivas:
            distancia = self.unidad_origen.posicion.distancia_manhattan(unidad.posicion)
            if distancia <= rango:
                enemigos_en_rango.append(unidad)
        return enemigos_en_rango


class GestorHabilidades:
    """Manages abilities for a unit"""

    def __init__(self):
        self.habilidades_activas: List[HabilidadActiva] = []
        self.habilidades_pasivas: List[HabilidadPasiva] = []
        self._efectos_temporales: Dict[str, int] = {}  # Effect name -> turns remaining

    def agregar_habilidad_activa(self, habilidad: HabilidadActiva):
        """Add an active ability"""
        self.habilidades_activas.append(habilidad)

    def agregar_habilidad_pasiva(self, habilidad: HabilidadPasiva):
        """Add a passive ability"""
        self.habilidades_pasivas.append(habilidad)

    def obtener_habilidad_activa(self, nombre: str) -> Optional[HabilidadActiva]:
        """Get active ability by name"""
        for hab in self.habilidades_activas:
            if hab.nombre == nombre:
                return hab
        return None

    def tiene_habilidad_pasiva(self, nombre: str) -> bool:
        """Check if unit has a passive ability"""
        return any(hab.nombre == nombre for hab in self.habilidades_pasivas)

    def reducir_cooldowns(self):
        """Reduce all cooldowns by 1 (called each turn)"""
        for habilidad in self.habilidades_activas:
            habilidad.reducir_cooldown()

        # Also reduce temporary effect durations
        efectos_a_eliminar = []
        for efecto, turnos in self._efectos_temporales.items():
            self._efectos_temporales[efecto] = turnos - 1
            if self._efectos_temporales[efecto] <= 0:
                efectos_a_eliminar.append(efecto)

        for efecto in efectos_a_eliminar:
            del self._efectos_temporales[efecto]

    def agregar_efecto_temporal(self, nombre: str, duracion: int):
        """Add a temporary effect with duration"""
        self._efectos_temporales[nombre] = duracion

    def tiene_efecto_temporal(self, nombre: str) -> bool:
        """Check if unit has a temporary effect active"""
        return nombre in self._efectos_temporales

    def obtener_modificador_ataque(self) -> int:
        """Get total attack modifier from abilities and effects"""
        modificador = 0

        # Check passive abilities
        for hab in self.habilidades_pasivas:
            if 'ataque' in hab.modificadores:
                modificador += hab.modificadores['ataque']

        # Check temporary effects
        if self.tiene_efecto_temporal('a_la_carga'):
            modificador += 3
        if self.tiene_efecto_temporal('carga_caballeria'):
            modificador += 3

        return modificador

    def obtener_modificador_defensa(self) -> int:
        """Get total defense modifier from abilities and effects"""
        modificador = 0

        # Check passive abilities
        for hab in self.habilidades_pasivas:
            if 'defensa' in hab.modificadores:
                modificador += hab.modificadores['defensa']

        # Check temporary effects
        if self.tiene_efecto_temporal('mantened_linea'):
            modificador += 2
        if self.tiene_efecto_temporal('muro_escudos'):
            modificador += 3

        return modificador