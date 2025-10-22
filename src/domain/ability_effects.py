"""
Concrete implementations of ability effects for Classic Battle Rules
"""

from typing import List, Optional
from dataclasses import dataclass
import random

from src.domain.abilities import EfectoHabilidad, ContextoHabilidad
from src.domain.events import EventoDominio
from src.domain.value_objects import Bando


# Custom events for abilities
@dataclass
class EventoHabilidadUsada(EventoDominio):
    """Event when an ability is used"""
    unidad_id: str
    habilidad_nombre: str
    cooldown: int
    descripcion: str


@dataclass
class EventoMoralRestaurada(EventoDominio):
    """Event when morale is restored"""
    unidad_id: str
    moral_restaurada: int
    fuente: str


@dataclass
class EventoModificadorAplicado(EventoDominio):
    """Event when a temporary modifier is applied"""
    unidad_id: str
    tipo_modificador: str  # 'ataque' or 'defensa'
    valor: int
    duracion: int
    fuente: str


@dataclass
class EventoUnidadAturdida(EventoDominio):
    """Event when a unit is stunned"""
    unidad_id: str
    atacante_id: str


# General Abilities

class EfectoReagrupar(EfectoHabilidad):
    """Reagrupar: +10 MOR to units in range 2, +5 Army Morale"""

    def aplicar(self, contexto: ContextoHabilidad) -> List[EventoDominio]:
        eventos = []

        # Restore morale to nearby units
        unidades_afectadas = contexto.obtener_unidades_en_rango(2)
        for unidad in unidades_afectadas:
            moral_anterior = unidad.moral_actual
            unidad.restaurar_moral(10)
            eventos.append(EventoMoralRestaurada(
                unidad_id=unidad.id,
                moral_restaurada=10,
                fuente="Reagrupar"
            ))

        # Also restore army morale
        contexto.ejercito_aliado.ganar_moral(5)

        eventos.append(EventoHabilidadUsada(
            unidad_id=contexto.unidad_origen.id,
            habilidad_nombre="Reagrupar",
            cooldown=3,
            descripcion=f"Restauró moral a {len(unidades_afectadas)} unidades"
        ))

        return eventos


class EfectoALaCarga(EfectoHabilidad):
    """¡A la carga!: +3 ATQ to allies in range 3 for their next attack"""

    def aplicar(self, contexto: ContextoHabilidad) -> List[EventoDominio]:
        eventos = []

        # Apply attack bonus to nearby units
        unidades_afectadas = contexto.obtener_unidades_en_rango(3)
        for unidad in unidades_afectadas:
            unidad.gestor_habilidades.agregar_efecto_temporal('a_la_carga', 1)
            eventos.append(EventoModificadorAplicado(
                unidad_id=unidad.id,
                tipo_modificador='ataque',
                valor=3,
                duracion=1,
                fuente="¡A la carga!"
            ))

        eventos.append(EventoHabilidadUsada(
            unidad_id=contexto.unidad_origen.id,
            habilidad_nombre="¡A la carga!",
            cooldown=4,
            descripcion=f"Inspiró a {len(unidades_afectadas)} unidades"
        ))

        return eventos


class EfectoMantenedLinea(EfectoHabilidad):
    """¡Mantened la línea!: +2 DEF to units in range 2 for 2 turns"""

    def aplicar(self, contexto: ContextoHabilidad) -> List[EventoDominio]:
        eventos = []

        # Apply defense bonus to nearby units
        unidades_afectadas = contexto.obtener_unidades_en_rango(2)
        for unidad in unidades_afectadas:
            unidad.gestor_habilidades.agregar_efecto_temporal('mantened_linea', 2)
            eventos.append(EventoModificadorAplicado(
                unidad_id=unidad.id,
                tipo_modificador='defensa',
                valor=2,
                duracion=2,
                fuente="¡Mantened la línea!"
            ))

        eventos.append(EventoHabilidadUsada(
            unidad_id=contexto.unidad_origen.id,
            habilidad_nombre="¡Mantened la línea!",
            cooldown=5,
            descripcion=f"Reforzó a {len(unidades_afectadas)} unidades"
        ))

        return eventos


# Cavalry Abilities

class EfectoImpactoDemoledor(EfectoHabilidad):
    """Impacto Demoledor: 50% chance to stun target (loses next turn)"""

    def aplicar(self, contexto: ContextoHabilidad) -> List[EventoDominio]:
        eventos = []

        if not contexto.objetivo:
            raise ValueError("Impacto Demoledor requires a target")

        # 50% chance to stun
        if random.random() < 0.5:
            contexto.objetivo.aturdido = True
            contexto.objetivo.puede_actuar = False
            eventos.append(EventoUnidadAturdida(
                unidad_id=contexto.objetivo.id,
                atacante_id=contexto.unidad_origen.id
            ))
            descripcion = f"¡Aturdió a {contexto.objetivo.visualizacion.nombre}!"
        else:
            descripcion = f"Falló el aturdimiento contra {contexto.objetivo.visualizacion.nombre}"

        eventos.append(EventoHabilidadUsada(
            unidad_id=contexto.unidad_origen.id,
            habilidad_nombre="Impacto Demoledor",
            cooldown=2,
            descripcion=descripcion
        ))

        return eventos


# Archer Abilities

class EfectoLluviaFlechas(EfectoHabilidad):
    """Lluvia de Flechas: Attack 3-tile line with ATQ-1"""

    def aplicar(self, contexto: ContextoHabilidad) -> List[EventoDominio]:
        from src.domain.services.combat_calculator import CalculadorCombate

        eventos = []

        if not contexto.objetivo:  # objetivo should be a position
            raise ValueError("Lluvia de Flechas requires a target position")

        # Get enemies in a 3-tile line from origin toward target
        direccion = contexto.unidad_origen.posicion.direccion_hacia(contexto.objetivo)
        enemigos_afectados = []

        # Check 3 positions in the direction
        for i in range(1, 4):
            pos_check = contexto.unidad_origen.posicion.mover_en_direccion(direccion, i)
            for enemigo in contexto.ejercito_enemigo.unidades_vivas:
                if enemigo.posicion == pos_check:
                    enemigos_afectados.append(enemigo)

        # Attack each enemy with reduced damage
        ataque_reducido = max(1, contexto.unidad_origen.estadisticas.ataque - 1)
        for enemigo in enemigos_afectados:
            # Simple damage calculation for area effect
            danio = max(1, ataque_reducido - enemigo.estadisticas.defensa)
            enemigo.recibir_danio(danio)

        eventos.append(EventoHabilidadUsada(
            unidad_id=contexto.unidad_origen.id,
            habilidad_nombre="Lluvia de Flechas",
            cooldown=2,
            descripcion=f"Golpeó a {len(enemigos_afectados)} enemigos"
        ))

        return eventos


class EfectoDisparoPreciso(EfectoHabilidad):
    """Disparo Preciso: Ignores target's defense"""

    def aplicar(self, contexto: ContextoHabilidad) -> List[EventoDominio]:
        eventos = []

        if not contexto.objetivo:
            raise ValueError("Disparo Preciso requires a target")

        # Deal full attack damage ignoring defense
        danio = contexto.unidad_origen.estadisticas.ataque
        contexto.objetivo.recibir_danio(danio)

        eventos.append(EventoHabilidadUsada(
            unidad_id=contexto.unidad_origen.id,
            habilidad_nombre="Disparo Preciso",
            cooldown=3,
            descripcion=f"Atravesó la defensa de {contexto.objetivo.visualizacion.nombre}"
        ))

        return eventos


# Infantry Abilities

class EfectoDisciplinaRomana(EfectoHabilidad):
    """Disciplina Romana: Recover to 7 MOR if below 5 (once per battle)"""

    def aplicar(self, contexto: ContextoHabilidad) -> List[EventoDominio]:
        eventos = []

        unidad = contexto.unidad_origen
        if unidad.moral_actual < 5:
            moral_anterior = unidad.moral_actual
            unidad._moral_actual = 7
            eventos.append(EventoMoralRestaurada(
                unidad_id=unidad.id,
                moral_restaurada=7 - moral_anterior,
                fuente="Disciplina Romana"
            ))
            descripcion = "¡La disciplina romana prevaleció!"
        else:
            descripcion = "La moral ya es suficientemente alta"

        eventos.append(EventoHabilidadUsada(
            unidad_id=contexto.unidad_origen.id,
            habilidad_nombre="Disciplina Romana",
            cooldown=999,  # Once per battle
            descripcion=descripcion
        ))

        return eventos


# Effect Registry
EFECTOS_HABILIDADES = {
    "reagrupar": EfectoReagrupar(),
    "a_la_carga": EfectoALaCarga(),
    "mantened_linea": EfectoMantenedLinea(),
    "impacto_demoledor": EfectoImpactoDemoledor(),
    "lluvia_flechas": EfectoLluviaFlechas(),
    "disparo_preciso": EfectoDisparoPreciso(),
    "disciplina_romana": EfectoDisciplinaRomana(),
}


def obtener_efecto(nombre: str) -> Optional[EfectoHabilidad]:
    """Get ability effect by name"""
    return EFECTOS_HABILIDADES.get(nombre)