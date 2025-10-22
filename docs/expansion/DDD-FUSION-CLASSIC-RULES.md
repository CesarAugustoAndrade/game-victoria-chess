# DDD Fusion: Classic Battle Rules Integration
## Legio Romana - Architecture Evolution Document

---

## Executive Summary

This document outlines the integration of Classic Battle Rules into the existing Legio Romana DDD architecture. The primary goal is to enhance strategic depth by incorporating an **army-level morale system**, **special abilities with cooldowns**, and **tactical mechanics** while preserving the current unit variety and Domain-Driven Design structure.

### Key Transformations
1. **Morale System**: Shift from per-unit morale to army-level Moral General (100 points)
2. **Victory Conditions**: Win by breaking enemy morale, not just eliminating units
3. **Combat Depth**: Add abilities, cooldowns, and tactical positioning bonuses
4. **Strategic Layers**: Center control, tactical massacre, and formation mechanics

---

## Part 1: Core Domain Model Evolution

### 1.1 Morale System Transformation

#### Current Model (Unit-Centric)
```python
class Unidad:
    _moral_actual: int  # 0-100 per unit
    esta_en_panico: bool  # <30 morale
```

#### Target Model (Army-Centric)
```python
class Ejercito:
    _moral_general: int = 100  # Army morale pool

    def perder_moral_por_unidad(self, unidad: Unidad):
        """Deduct unit's COSTO_MORAL from army morale"""
        self._moral_general -= unidad.estadisticas.costo_moral

    @property
    def esta_derrotado(self) -> bool:
        return self._moral_general <= 0  # New victory condition
```

#### Hybrid Approach (Recommended)
Maintain both systems for maximum flexibility:
- **Army Morale**: Primary victory condition
- **Unit Morale**: Affects individual unit performance
- **Synergy**: Low unit morale causes additional army morale loss

### 1.2 Enhanced Value Objects

```python
@dataclass(frozen=True)
class EstadisticasUnidadMejoradas:
    # Existing stats
    vida_maxima: int
    ataque: int
    defensa: int
    rango_movimiento: int
    rango_ataque: int

    # New classic rules stats
    costo_moral: int  # Moral cost when unit dies (3-30)
    patron_ataque: PatronAtaque  # FRONTAL, FRONTAL_DIAGONAL, RANGO
    tipo_accion: TipoAccion  # What actions unit can perform

    # Abilities
    habilidades_pasivas: List[HabilidadPasiva]
    habilidades_activas: List[HabilidadActiva]

@dataclass
class HabilidadActiva:
    nombre: str
    descripcion: str
    cooldown_maximo: int
    cooldown_actual: int = 0
    usos_maximos: Optional[int] = None
    usos_restantes: Optional[int] = None

    def puede_usar(self) -> bool:
        return (self.cooldown_actual == 0 and
                (self.usos_restantes is None or self.usos_restantes > 0))
```

### 1.3 Attack Pattern System

```python
from enum import Enum

class PatronAtaque(Enum):
    FRONTAL = "frontal"  # Heavy infantry - front only
    FRONTAL_DIAGONAL = "frontal_diagonal"  # Light/medium - front + diagonals
    RANGO = "rango"  # Archers - distance 2-5

class DireccionAtaque(Enum):
    NORTE = (0, -1)
    NORESTE = (1, -1)
    ESTE = (1, 0)
    SURESTE = (1, 1)
    SUR = (0, 1)
    SUROESTE = (-1, 1)
    OESTE = (-1, 0)
    NOROESTE = (-1, -1)

def validar_ataque_segun_patron(
    atacante: Unidad,
    objetivo: Unidad
) -> bool:
    """Validate if attack direction matches unit's pattern"""
    direccion = calcular_direccion(atacante.posicion, objetivo.posicion)

    if atacante.estadisticas.patron_ataque == PatronAtaque.FRONTAL:
        return direccion in [DireccionAtaque.NORTE, DireccionAtaque.SUR,
                            DireccionAtaque.ESTE, DireccionAtaque.OESTE]
    elif atacante.estadisticas.patron_ataque == PatronAtaque.FRONTAL_DIAGONAL:
        return True  # All directions valid
    elif atacante.estadisticas.patron_ataque == PatronAtaque.RANGO:
        distancia = atacante.posicion.distancia_manhattan(objetivo.posicion)
        return 2 <= distancia <= 5
```

---

## Part 2: Combat System Enhancement

### 2.1 Revised Damage Formula

```python
class CalculadorCombateMejorado:
    @staticmethod
    def calcular_danio(
        atacante: Unidad,
        defensor: Unidad,
        contexto: ContextoCombate
    ) -> ResultadoCombate:
        # Base damage: ATQ - DEF (can be 0)
        danio_base = max(0, atacante.estadisticas.ataque - defensor.estadisticas.defensa)

        # Apply modifiers
        modificadores = CalculadorModificadores.calcular(atacante, defensor, contexto)
        danio_final = danio_base + modificadores.total

        # Apply damage
        defensor.recibir_danio(danio_final)

        # Calculate morale impact
        impacto_moral = calcular_impacto_moral(danio_final, defensor)

        return ResultadoCombate(
            danio=danio_final,
            bloqueado=(danio_base == 0),
            impacto_moral=impacto_moral
        )
```

---

## Part 3: Turn Structure & Phases


### 3.2 Action System

```python
class TipoAccion(Enum):
    MOVER = "mover"
    ATACAR = "atacar"
    DEFENDER = "defender"
    HABILIDAD = "habilidad"

class AccionUnidad:
    def __init__(self, unidad: Unidad, tipo: TipoAccion):
        self.unidad = unidad
        self.tipo = tipo
        self.objetivo: Optional[Posicion] = None  # For move
        self.unidad_objetivo: Optional[Unidad] = None  # For attack
        self.habilidad: Optional[HabilidadActiva] = None  # For ability

    def validar(self) -> bool:
        if self.tipo == TipoAccion.MOVER:
            return self.unidad.puede_moverse and self.objetivo is not None
        elif self.tipo == TipoAccion.ATACAR:
            return self.unidad.puede_actuar and self.unidad_objetivo is not None
        elif self.tipo == TipoAccion.DEFENDER:
            return True  # Always can defend
        elif self.tipo == TipoAccion.HABILIDAD:
            return self.habilidad and self.habilidad.puede_usar()
```

---

## Part 4: Strategic Mechanics

### 4.1 Center Control System

```python
class ControlCentro:
    def __init__(self, tablero: Tablero):
        self.tablero = tablero
        self._definir_casillas_centrales()
        self.turnos_sin_control = {Bando.ROMA: 0, Bando.BARBAROS: 0}

    def _definir_casillas_centrales(self):
        """Define 4 center tiles for 9x7 board"""
        filas_centro = self.tablero.filas // 2
        columnas_centro = self.tablero.columnas // 2

        self.casillas_centrales = [
            Posicion(filas_centro, columnas_centro),
            Posicion(filas_centro, columnas_centro + 1),
            Posicion(filas_centro + 1, columnas_centro),
            Posicion(filas_centro + 1, columnas_centro + 1)
        ]

    def verificar_control(self, ejercito: Ejercito) -> bool:
        """Check if army controls any center tile"""
        for casilla in self.casillas_centrales:
            unidad = self.tablero.obtener_unidad_en(casilla)
            if unidad and unidad.bando == ejercito.bando:
                return True
        return False

    def aplicar_penalizacion(self, ejercito: Ejercito) -> EventoDominio:
        """Apply -3 morale per turn without center"""
        if not self.verificar_control(ejercito):
            self.turnos_sin_control[ejercito.bando] += 1
            ejercito.perder_moral(3)

            return EventoPerdidaControlCentro(
                bando=ejercito.bando,
                turnos_perdidos=self.turnos_sin_control[ejercito.bando],
                moral_perdida=3
            )
        else:
            self.turnos_sin_control[ejercito.bando] = 0
            return None
```

### 4.2 Tactical Massacre System

```python
class ContadorMasacre:
    def __init__(self):
        self.eliminaciones_turno_actual = 0

    def registrar_eliminacion(self, unidad: Unidad):
        """Track unit elimination"""
        self.eliminaciones_turno_actual += 1

    def verificar_masacre_tactica(self) -> bool:
        """Check if 3+ units eliminated this turn"""
        return self.eliminaciones_turno_actual >= 3

    def aplicar_bonificacion(
        self,
        ejercito_atacante: Ejercito,
        ejercito_defensor: Ejercito
    ) -> EventoDominio:
        """Apply morale bonus/penalty for massacre"""
        if self.verificar_masacre_tactica():
            ejercito_defensor.perder_moral(10)
            ejercito_atacante.ganar_moral(5)

            return EventoMasacreTactica(
                unidades_eliminadas=self.eliminaciones_turno_actual,
                moral_enemiga_perdida=10,
                moral_propia_ganada=5
            )
        return None

    def reiniciar_contador(self):
        """Reset for new turn"""
        self.eliminaciones_turno_actual = 0
```

---

## Part 5: Abilities Framework

### 5.1 Ability System Architecture

```python
from abc import ABC, abstractmethod

class EfectoHabilidad(ABC):
    """Abstract base for ability effects"""
    @abstractmethod
    def aplicar(self, contexto: ContextoHabilidad) -> List[EventoDominio]:
        pass

class HabilidadReagrupar(EfectoHabilidad):
    """General ability: +10 MOR to units in range 2"""
    def aplicar(self, contexto: ContextoHabilidad) -> List[EventoDominio]:
        eventos = []
        unidades_afectadas = contexto.obtener_unidades_en_rango(2)

        for unidad in unidades_afectadas:
            unidad.restaurar_moral_individual(10)
            eventos.append(EventoMoralRestaurada(
                unidad.id, 10, "Reagrupar"
            ))

        contexto.ejercito.ganar_moral(5)  # +5 army morale
        eventos.append(EventoMoralGeneralAumentada(
            contexto.ejercito.bando, 5
        ))

        return eventos

class GestorHabilidades:
    """Manages ability cooldowns and usage"""
    def __init__(self):
        self.habilidades_activas: Dict[str, HabilidadActiva] = {}

    def usar_habilidad(
        self,
        habilidad: HabilidadActiva,
        contexto: ContextoHabilidad
    ) -> List[EventoDominio]:
        if not habilidad.puede_usar():
            raise ExcepcionHabilidadNoDisponible()

        # Apply effect
        efecto = self._obtener_efecto(habilidad.nombre)
        eventos = efecto.aplicar(contexto)

        # Update cooldown
        habilidad.cooldown_actual = habilidad.cooldown_maximo

        # Update uses if limited
        if habilidad.usos_restantes is not None:
            habilidad.usos_restantes -= 1

        eventos.append(EventoHabilidadUsada(
            habilidad.nombre,
            habilidad.cooldown_maximo
        ))

        return eventos

    def reducir_cooldowns(self):
        """Reduce all cooldowns by 1 each turn"""
        for habilidad in self.habilidades_activas.values():
            if habilidad.cooldown_actual > 0:
                habilidad.cooldown_actual -= 1
```

### 5.2 Ability Catalog

```python
CATALOGO_HABILIDADES = {
    # General abilities
    "reagrupar": HabilidadActiva(
        nombre="Reagrupar",
        descripcion="+10 MOR unidades rango 2, +5 Moral General",
        cooldown_maximo=3
    ),
    "a_la_carga": HabilidadActiva(
        nombre="¡A la carga!",
        descripcion="+3 ATQ aliados en rango 3",
        cooldown_maximo=4
    ),
    "mantened_linea": HabilidadActiva(
        nombre="¡Mantened la línea!",
        descripcion="+2 DEF rango 2 por 2 turnos",
        cooldown_maximo=5
    ),

    # Cavalry abilities
    "carga": HabilidadPasiva(
        nombre="Carga",
        descripcion="Puede mover y atacar. Si mueve 2+: +3 ATQ"
    ),
    "impacto_demoledor": HabilidadActiva(
        nombre="Impacto Demoledor",
        descripcion="50% aturdir enemigo (pierde turno)",
        cooldown_maximo=2
    ),

    # Archer abilities
    "lluvia_flechas": HabilidadActiva(
        nombre="Lluvia de Flechas",
        descripcion="Ataca línea de 3 casillas con ATQ-1",
        cooldown_maximo=2
    ),
    "disparo_preciso": HabilidadActiva(
        nombre="Disparo Preciso",
        descripcion="Ignora DEF del objetivo",
        cooldown_maximo=3
    ),

    # Infantry abilities
    "muro_escudos": HabilidadPasiva(
        nombre="Muro de Escudos",
        descripcion="3+ en línea: +3 DEF"
    ),
    "disciplina_romana": HabilidadActiva(
        nombre="Disciplina Romana",
        descripcion="Recupera a 7 MOR si cae bajo 5",
        cooldown_maximo=float('inf'),  # Once per battle
        usos_maximos=1
    )
}
```

---

## Part 6: Unit Statistics Mapping

### 6.1 Stats Conversion Table

| Unit Type | Classic HP | Classic ATQ | Classic DEF | COSTO_MORAL | Pattern | Abilities |
|-----------|------------|-------------|-------------|-------------|---------|-----------|
| **Legionario** | 12 | 5 | 6 | 9 | Frontal | Disciplina, Gladius |
| **Hastati** | 9 | 4 | 4 | 6 | Frontal | Pila, Empuje |
| **Principes** | 11 | 5 | 5 | 8 | Frontal | Veterano, Muro |
| **Triarii** | 13 | 6 | 7 | 12 | Frontal | Última Línea, Lanza |
| **Equites** | 11 | 7 | 5 | 10 | Front+Diag | Carga, Impacto |
| **Velites** | 5 | 2 | 2 | 3 | Front+Diag | Escaramuza, Ágil |
| **Sagittarii** | 5 | 3 | 2 | 4 | Rango 2-5 | Lluvia, Preciso |
| **General** | 12 | 4 | 6 | 30 | Frontal | 2 chosen abilities |

### 6.2 Scaling Strategy

To maintain compatibility with existing code while adopting classic mechanics:

```python
class EscaladorEstadisticas:
    """Scale between classic (low) and current (high) values"""
    FACTOR_ESCALA = 8  # Current stats ~8x higher than classic

    @staticmethod
    def escalar_a_actual(valor_clasico: int) -> int:
        """Convert classic value to current scale"""
        return valor_clasico * EscaladorEstadisticas.FACTOR_ESCALA

    @staticmethod
    def escalar_a_clasico(valor_actual: int) -> int:
        """Convert current value to classic scale"""
        return valor_actual // EscaladorEstadisticas.FACTOR_ESCALA

    @staticmethod
    def convertir_estadisticas(stats_clasicas: dict) -> EstadisticasUnidad:
        """Convert classic stats dict to current EstadisticasUnidad"""
        return EstadisticasUnidad(
            vida_maxima=EscaladorEstadisticas.escalar_a_actual(
                stats_clasicas['HP']
            ),
            ataque=EscaladorEstadisticas.escalar_a_actual(
                stats_clasicas['ATQ']
            ),
            defensa=EscaladorEstadisticas.escalar_a_actual(
                stats_clasicas['DEF']
            ),
            rango_movimiento=stats_clasicas['MOV'],  # No scaling
            rango_ataque=stats_clasicas['RNG'],  # No scaling
            costo_moral=stats_clasicas['COSTO_MORAL'],  # No scaling
            patron_ataque=stats_clasicas['PATRON']
        )
```

---

## Part 7: Implementation Roadmap

### Phase 1: Foundation (Priority: CRITICAL)
**Estimated effort: 2-3 days**

1. **Add Army Morale System**
   - Add `moral_general` to `Ejercito` class
   - Add `costo_moral` to `EstadisticasUnidad`
   - Create `EventoMoralGeneralCambiada`
   - Modify victory condition

2. **Update Combat Formula**
   - Change to `ATQ - DEF` (full defense)
   - Allow 0-damage (blocked) attacks
   - Add combat modifier system

3. **Add Attack Patterns**
   - Create `PatronAtaque` enum
   - Implement directional validation
   - Update `obtener_objetivos_atacables()`

### Phase 2: Tactical Depth (Priority: HIGH)
**Estimated effort: 3-4 days**

1. **Implement Abilities Framework**
   - Create `Habilidad` value objects
   - Build `GestorHabilidades` system
   - Add cooldown management
   - Wire to UI (ability buttons)



3. **Movement/Attack Choice System**
   - Implement MOVE/ATTACK/DEFEND
   - Add cavalry exception (can do both)
   - Update UI for action selection

### Phase 3: Strategic Mechanics (Priority: MEDIUM)
**Estimated effort: 2-3 days**

1. **Center Control**
   - Define center tiles
   - Track control status
   - Apply -3 morale/turn penalty
   - Add visual indicators

2. **Tactical Massacre**
   - Track kills per turn
   - Apply ±morale at 3+ kills
   - Create event and feedback

3. **General Unit**
   - Add new unit type
   - Implement ability selection
   - Add devastating morale cost

### Phase 4: Polish & Balance (Priority: LOW)
**Estimated effort: 2-3 days**

1. **Formations Enhancement**
   - Line formation bonuses
   - Position-based benefits
   - Visual feedback

2. **Terrain System** (Optional)
   - Add elevation layer
   - Implement elevation bonuses
   - Update pathfinding

3. **Balance & Testing**
   - Playtest all mechanics
   - Adjust stat scaling
   - Fine-tune abilities

---

## Part 8: Migration Strategy

### 8.1 Feature Flags

```python
class ConfiguracionReglas:
    """Toggle between classic and current rules"""
    usar_moral_ejercito: bool = True  # Army morale system
    usar_formula_clasica: bool = True  # ATQ - DEF formula
    usar_patrones_ataque: bool = True  # Attack patterns
    usar_habilidades: bool = True  # Abilities system
    usar_control_centro: bool = True  # Center control
    usar_masacre_tactica: bool = True  # Tactical massacre

    @classmethod
    def modo_clasico(cls):
        """Enable all classic rules"""
        return cls(
            usar_moral_ejercito=True,
            usar_formula_clasica=True,
            usar_patrones_ataque=True,
            usar_habilidades=True,
            usar_control_centro=True,
            usar_masacre_tactica=True
        )

    @classmethod
    def modo_legacy(cls):
        """Use original rules only"""
        return cls(
            usar_moral_ejercito=False,
            usar_formula_clasica=False,
            usar_patrones_ataque=False,
            usar_habilidades=False,
            usar_control_centro=False,
            usar_masacre_tactica=False
        )
```

### 8.2 Backward Compatibility

```python
class BatallaHibrida(Batalla):
    """Battle supporting both rule systems"""

    def __init__(self, configuracion: ConfiguracionReglas = None):
        super().__init__()
        self.config = configuracion or ConfiguracionReglas.modo_clasico()

    def verificar_victoria(self) -> Optional[Bando]:
        if self.config.usar_moral_ejercito:
            # Classic: Check army morale
            if self._ejercito_jugador.moral_general <= 0:
                return Bando.BARBAROS
            if self._ejercito_enemigo.moral_general <= 0:
                return Bando.ROMA
        else:
            # Legacy: Check unit elimination
            if self._ejercito_jugador.esta_derrotado:
                return Bando.BARBAROS
            if self._ejercito_enemigo.esta_derrotado:
                return Bando.ROMA
        return None
```

---

## Part 9: Testing Strategy

### 9.1 Unit Tests

```python
class TestMoralSystem:
    def test_army_morale_deduction(self):
        ejercito = Ejercito(Bando.ROMA)
        ejercito.moral_general = 100

        unidad = crear_legionario()  # costo_moral = 9
        ejercito.perder_moral_por_unidad(unidad)

        assert ejercito.moral_general == 91

    def test_victory_by_morale_collapse(self):
        batalla = Batalla()
        batalla._ejercito_enemigo.moral_general = 5

        # Kill unit with costo_moral = 10
        batalla._ejercito_enemigo.moral_general -= 10

        assert batalla.verificar_victoria() == Bando.ROMA
```

### 9.2 Integration Tests

```python
class TestCombatFlow:
    def test_attack_pattern_validation(self):
        # Heavy infantry can only attack frontally
        hastati = crear_hastati(posicion=Posicion(3, 3))
        enemigo_diagonal = crear_enemigo(posicion=Posicion(4, 4))

        objetivos = hastati.obtener_objetivos_atacables([enemigo_diagonal])
        assert enemigo_diagonal not in objetivos

    def test_cavalry_charge_bonus(self):
        equites = crear_equites()
        equites.mover_a(Posicion(5, 5))  # Move 2 tiles

        danio = equites.calcular_danio_con_carga()
        assert danio.incluye_bonus_carga
        assert danio.bonus == 3
```

### 9.3 Balance Testing

```python
class TestGameBalance:
    scenarios = [
        "3_legionarios_vs_5_barbaros",
        "general_con_caballeria_vs_infanteria",
        "control_centro_prolongado",
        "masacre_tactica_recuperacion"
    ]

    def test_scenario_outcomes(self):
        for scenario in self.scenarios:
            resultados = simular_escenario(scenario, n=100)
            assert 0.4 <= resultados.tasa_victoria_roma <= 0.6
```

---

## Part 10: UI/UX Enhancements

### 10.1 New UI Elements

```python
class ElementosUIClasicos:
    """New UI components for classic rules"""

    def crear_barra_moral_ejercito(self):
        """Army morale bar (0-100)"""
        return BarraMoral(
            posicion=(10, 10),
            ancho=200,
            alto=20,
            color_lleno=VERDE,
            color_vacio=ROJO
        )

    def crear_indicador_centro(self):
        """Center control indicator"""
        return IndicadorCentro(
            casillas_centrales=self.tablero.obtener_centro(),
            color_controlado=AZUL,
            color_perdido=ROJO,
            color_neutral=GRIS
        )

    def crear_panel_habilidades(self):
        """Ability buttons with cooldowns"""
        return PanelHabilidades(
            posicion=(10, 100),
            habilidades=self.unidad_seleccionada.habilidades,
            mostrar_cooldowns=True,
            mostrar_tooltips=True
        )

    def crear_contador_masacre(self):
        """Kill counter for tactical massacre"""
        return ContadorMasacre(
            posicion=(ANCHO - 100, 10),
            kills_actuales=self.batalla.eliminaciones_turno,
            umbral_masacre=3
        )
```

### 10.2 Visual Feedback

```python
class FeedbackVisualMejorado:
    def mostrar_patron_ataque(self, unidad: Unidad):
        """Highlight valid attack tiles based on pattern"""
        if unidad.patron_ataque == PatronAtaque.FRONTAL:
            self.resaltar_casillas_frontales(unidad.posicion)
        elif unidad.patron_ataque == PatronAtaque.FRONTAL_DIAGONAL:
            self.resaltar_casillas_frontales_diagonales(unidad.posicion)
        elif unidad.patron_ataque == PatronAtaque.RANGO:
            self.resaltar_anillo(unidad.posicion, min_dist=2, max_dist=5)

    def animar_habilidad(self, habilidad: str, origen: Posicion):
        """Animate ability effects"""
        if habilidad == "reagrupar":
            self.particulas_moral(origen, radio=2, color=DORADO)
        elif habilidad == "lluvia_flechas":
            self.lluvia_proyectiles(origen, objetivo, cantidad=20)
```

---

## Appendix A: Domain Events Catalog

```python
# New domain events for classic rules
@dataclass
class EventoMoralGeneralCambiada(EventoDominio):
    bando: Bando
    moral_anterior: int
    moral_nueva: int
    causa: str  # "unidad_eliminada", "centro_perdido", "masacre", etc.

@dataclass
class EventoPerdidaControlCentro(EventoDominio):
    bando: Bando
    turnos_sin_control: int
    penalizacion_moral: int

@dataclass
class EventoMasacreTactica(EventoDominio):
    bando_atacante: Bando
    unidades_eliminadas: int
    moral_enemiga_perdida: int
    moral_propia_ganada: int

@dataclass
class EventoHabilidadActivada(EventoDominio):
    unidad_id: str
    habilidad: str
    objetivos_afectados: List[str]
    cooldown: int

@dataclass
class EventoAtaqueBloqueado(EventoDominio):
    atacante_id: str
    defensor_id: str
    ataque: int
    defensa: int
```

---

## Appendix B: Configuration Files

### B.1 Classic Units Configuration

```python
# src/domain/classic_units_config.py

UNIDADES_CLASICAS = {
    TipoUnidad.LEGIONARIO: {
        "stats": EstadisticasUnidadMejoradas(
            vida_maxima=96,  # 12 * 8
            ataque=40,  # 5 * 8
            defensa=48,  # 6 * 8
            rango_movimiento=1,
            rango_ataque=1,
            costo_moral=9,
            patron_ataque=PatronAtaque.FRONTAL,
            habilidades_pasivas=["gladius_hispaniensis"],
            habilidades_activas=["disciplina_romana"]
        ),
        "visualizacion": VisualizacionUnidad(
            nombre="Legionario Romano",
            color=ROJO_ROMANO,
            grito_guerra="¡Por Roma y el Senado!"
        )
    },
    # ... rest of units
}
```

### B.2 Abilities Configuration

```python
# src/domain/abilities_config.py

CONFIGURACION_HABILIDADES = {
    "reagrupar": {
        "efecto": EfectoReagrupar,
        "rango": 2,
        "moral_unidades": 10,
        "moral_ejercito": 5,
        "cooldown": 3,
        "animacion": "particulas_doradas"
    },
    "lluvia_flechas": {
        "efecto": EfectoLluviaFlechas,
        "patron": "linea_3_casillas",
        "modificador_ataque": -1,
        "cooldown": 2,
        "animacion": "proyectiles_multiples"
    },
    # ... rest of abilities
}
```

---

## Conclusion

This fusion document provides a comprehensive roadmap for integrating Classic Battle Rules into the existing Legio Romana DDD architecture. The key principles are:

1. **Preserve DDD Structure**: Maintain clean architecture and domain boundaries
2. **Incremental Integration**: Phase implementation to maintain stability
3. **Backward Compatibility**: Support both rule systems via configuration
4. **Enhanced Strategy**: Add depth without overwhelming complexity
5. **Visual Clarity**: Ensure new mechanics are clearly communicated

The implementation focuses on the most impactful changes first (army morale, abilities) while preserving the existing unit variety and codebase structure. This approach ensures the game evolves toward greater strategic depth while maintaining its tactical combat foundation.

---

*Document Version: 1.0*
*Last Updated: 2025-01-21*
*Author: DDD Fusion Analysis System*