# Implementation Plan: Classic Rules Integration
## Divided into 3 Development Prompts

---

## PROMPT 1: Core Morale System & Combat Formula
**Objective**: Transform the victory condition from unit elimination to army morale collapse, and update combat mechanics to use classic damage formula.

### Tasks:

#### 1.1 Army Morale System (Priority: CRITICAL)
**Files to modify:**
- `src/domain/entities.py`
- `src/domain/value_objects.py`
- `src/domain/batalla.py`
- `src/domain/events.py`

**Implementation:**
```python
# Add to Ejercito class
class Ejercito:
    def __init__(self, bando: Bando):
        self._bando = bando
        self._unidades: List[Unidad] = []
        self._formacion = "linea"
        self._moral_general = 100  # NEW: Army morale pool

    def perder_moral_por_unidad(self, unidad: Unidad):
        """Deduct unit's COSTO_MORAL when eliminated"""
        self._moral_general -= unidad.estadisticas.costo_moral
        self._moral_general = max(0, self._moral_general)

    @property
    def esta_derrotado(self) -> bool:
        # OLD: return self.cantidad_unidades == 0
        return self._moral_general <= 0  # NEW: Victory by morale
```

**Add COSTO_MORAL to all units:**
```python
# Update EstadisticasUnidad
@dataclass(frozen=True)
class EstadisticasUnidad:
    # Existing fields...
    costo_moral: int  # NEW: Moral cost when unit dies

# Update unit configurations
ESTADISTICAS_UNIDADES = {
    TipoUnidad.LEGIONARIO: EstadisticasUnidad(
        # existing stats...
        costo_moral=9  # NEW
    ),
    TipoUnidad.HASTATI: EstadisticasUnidad(
        # existing stats...
        costo_moral=6  # NEW
    ),
    # etc...
}
```

#### 1.2 Combat Formula Update (Priority: HIGH)
**Files to modify:**
- `src/domain/value_objects.py`
- `src/domain/services/combat_calculator.py`

**Implementation:**
```python
# Update damage calculation
def calcular_danio_base(self, defensa_objetivo: int) -> int:
    """Classic formula: ATQ - DEF (can be 0)"""
    # OLD: return max(1, self.ataque - (defensa_objetivo // 2))
    return max(0, self.ataque - defensa_objetivo)  # NEW: Full defense

# Update combat service
class CalculadorCombate:
    @staticmethod
    def ejecutar_ataque(atacante: Unidad, objetivo: Unidad) -> ResultadoAtaque:
        danio_base = atacante.estadisticas.calcular_danio_base(
            objetivo.estadisticas.defensa
        )

        # NEW: Handle blocked attacks
        if danio_base == 0:
            return ResultadoAtaque(
                atacante_id=atacante.id,
                objetivo_id=objetivo.id,
                danio=0,
                bloqueado=True,  # NEW field
                objetivo_eliminado=False
            )

        # Apply damage and morale as before
        # ...
```

#### 1.3 Attack Patterns System (Priority: HIGH)
**Files to modify:**
- `src/domain/value_objects.py`
- `src/domain/entities.py`

**Implementation:**
```python
# Add attack pattern enum
class PatronAtaque(Enum):
    FRONTAL = "frontal"  # Heavy infantry
    FRONTAL_DIAGONAL = "frontal_diagonal"  # Light/Medium/Cavalry
    RANGO = "rango"  # Archers

# Update EstadisticasUnidad
@dataclass(frozen=True)
class EstadisticasUnidad:
    # existing fields...
    patron_ataque: PatronAtaque  # NEW

# Update unit attack validation
def obtener_objetivos_atacables(self, unidades_enemigas: List['Unidad']) -> List['Unidad']:
    objetivos = []
    for enemigo in unidades_enemigas:
        if self._validar_patron_ataque(enemigo):
            objetivos.append(enemigo)
    return objetivos

def _validar_patron_ataque(self, objetivo: 'Unidad') -> bool:
    """Validate attack based on unit's pattern"""
    direccion = self._calcular_direccion(objetivo)

    if self.estadisticas.patron_ataque == PatronAtaque.FRONTAL:
        return direccion in ['norte', 'sur', 'este', 'oeste']
    elif self.estadisticas.patron_ataque == PatronAtaque.FRONTAL_DIAGONAL:
        return True  # All directions valid
    elif self.estadisticas.patron_ataque == PatronAtaque.RANGO:
        distancia = self.posicion.distancia_manhattan(objetivo.posicion)
        return 2 <= distancia <= 5
```

#### 1.4 Domain Events for New System
**Files to create/modify:**
- `src/domain/events.py`

```python
@dataclass
class EventoMoralGeneralCambiada(EventoDominio):
    bando: Bando
    moral_anterior: int
    moral_nueva: int
    causa: str

@dataclass
class EventoAtaqueBloqueado(EventoDominio):
    atacante_id: str
    defensor_id: str
    mensaje: str = "¡Ataque bloqueado por la defensa!"
```

#### 1.5 UI Updates for Army Morale
**Files to modify:**
- `src/states/batalla_state.py`
- `src/presentation/battle_renderer.py`

```python
# Add morale bar display
def _dibujar_moral_ejercitos(self, screen):
    """Draw army morale bars"""
    # Roma morale bar
    moral_roma = self.servicio_juego.obtener_moral_ejercito(Bando.ROMA)
    self._dibujar_barra_moral(screen, 10, 10, moral_roma, "ROMA")

    # Barbaros morale bar
    moral_barbaros = self.servicio_juego.obtener_moral_ejercito(Bando.BARBAROS)
    self._dibujar_barra_moral(screen, ANCHO - 210, 10, moral_barbaros, "BARBAROS")
```

### Testing Checklist:
- [ ] Units die → Army morale decreases by COSTO_MORAL
- [ ] Army morale reaches 0 → Battle ends with victory
- [ ] High DEF units can completely block low ATQ attacks
- [ ] Attack patterns restrict valid targets
- [ ] UI shows army morale bars
- [ ] Victory/defeat messages reflect morale collapse

### Expected Outcome:
After Prompt 1, the game will have:
1. Victory by morale depletion instead of unit elimination
2. More tactical combat where defense matters more
3. Attack patterns that encourage positioning
4. Visual feedback for army morale status

---

## PROMPT 2: Abilities System & Turn Phases
**Objective**: Implement special abilities with cooldowns 

### Tasks:

#### 2.1 Abilities Framework (Priority: CRITICAL)
**Files to create:**
- `src/domain/abilities.py`
- `src/domain/ability_effects.py`

**Implementation:**
```python
# abilities.py
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

    def usar(self):
        self.cooldown_actual = self.cooldown_maximo
        if self.usos_restantes is not None:
            self.usos_restantes -= 1

class GestorHabilidades:
    def __init__(self, unidad: Unidad):
        self.unidad = unidad
        self.habilidades_activas: List[HabilidadActiva] = []
        self.habilidades_pasivas: List[str] = []

    def reducir_cooldowns(self):
        """Called each turn"""
        for habilidad in self.habilidades_activas:
            if habilidad.cooldown_actual > 0:
                habilidad.cooldown_actual -= 1
```

#### 2.2 Ability Catalog Implementation
**Files to modify:**
- `src/domain/factories.py`
- `src/domain/entities.py`

```python
# Define abilities for each unit type
HABILIDADES_POR_TIPO = {
    TipoUnidad.LEGIONARIO: {
        "activas": [
            HabilidadActiva("Disciplina Romana",
                          "Recupera a 7 MOR si <5",
                          cooldown_maximo=999, usos_maximos=1)
        ],
        "pasivas": ["gladius_hispaniensis"]  # +2 ATQ vs DEF 5+
    },
    TipoUnidad.EQUITES: {
        "activas": [
            HabilidadActiva("Impacto Demoledor",
                          "50% aturdir enemigo",
                          cooldown_maximo=2)
        ],
        "pasivas": ["carga"]  # Can move + attack, +3 ATQ if moved 2+
    },
    TipoUnidad.SAGITTARII: {
        "activas": [
            HabilidadActiva("Lluvia de Flechas",
                          "Ataca línea 3 casillas ATQ-1",
                          cooldown_maximo=2),
            HabilidadActiva("Disparo Preciso",
                          "Ignora DEF",
                          cooldown_maximo=3)
        ],
        "pasivas": ["ataque_distancia"]  # RNG 2-5
    }
}
```

class TipoAccion(Enum):
    MOVER = "mover"
    ATACAR = "atacar"
    DEFENDER = "defender"
    HABILIDAD = "habilidad"

# Update Batalla class
class Batalla:
    def __init__(self, ...):
        # existing...
        self._fase_actual = FaseTurno.INICIATIVA
        self._acciones_pendientes: Dict[str, TipoAccion] = {}

    def asignar_accion_unidad(self, unidad_id: str, accion: TipoAccion):
        """Player assigns action to unit during DECISION phase"""
        self._acciones_pendientes[unidad_id] = accion

    def ejecutar_fase_actual(self) -> List[EventoDominio]:
        """Execute current phase and advance"""
        eventos = []

        if self._fase_actual == FaseTurno.ATAQUE_DISTANCIA:
            eventos.extend(self._ejecutar_ataques_distancia())
        elif self._fase_actual == FaseTurno.COMBATE_CUERPO:
            eventos.extend(self._ejecutar_combate_cuerpo())
        elif self._fase_actual == FaseTurno.RESOLUCION:
            eventos.extend(self._resolver_turno())

        self._avanzar_fase()
        return eventos
```

#### 2.4 Movement/Attack Restriction
**Files to modify:**
- `src/domain/entities.py`

```python
class Unidad:
    def __init__(self, ...):
        # existing...
        self._accion_turno: Optional[TipoAccion] = None

    def puede_realizar_accion(self, accion: TipoAccion) -> bool:
        """Check if unit can perform action based on type"""
        if self._accion_turno is not None:
            return False  # Already acted

        # Cavalry exception: can MOVE then ATTACK
        if self.tipo == TipoUnidad.EQUITES:
            if accion == TipoAccion.ATACAR and self._ha_movido:
                return True  # Cavalry charge

        # Normal units: MOVE OR ATTACK, not both
        if accion == TipoAccion.MOVER:
            return self.puede_moverse
        elif accion == TipoAccion.ATACAR:
            return self.puede_actuar and not self._ha_movido
        elif accion == TipoAccion.DEFENDER:
            return True  # Always can defend

        return False
```

#### 2.5 Ability UI Integration
**Files to modify:**
- `src/states/batalla_state.py`
- `src/presentation/ability_panel.py` (new)

```python
# ability_panel.py
class PanelHabilidades:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.botones_habilidad = []

    def actualizar(self, unidad: Unidad):
        """Update panel for selected unit"""
        self.botones_habilidad.clear()

        if not unidad or not unidad.gestor_habilidades:
            return

        for i, habilidad in enumerate(unidad.gestor_habilidades.habilidades_activas):
            boton = BotonHabilidad(
                x=self.x,
                y=self.y + i * 40,
                habilidad=habilidad,
                habilitado=habilidad.puede_usar()
            )
            self.botones_habilidad.append(boton)

    def dibujar(self, screen):
        for boton in self.botones_habilidad:
            boton.dibujar(screen)
```

### Testing Checklist:
- [ ] Units have abilities based on type
- [ ] Cooldowns decrease each turn
- [ ] One-use abilities work correctly
- [ ] Cavalry can move + attack
- [ ] Other units must choose move OR attack
- [ ] Turn phases execute in order
- [ ] UI shows ability buttons with cooldowns

### Expected Outcome:
After Prompt 2, the game will have:
1. Special abilities for tactical depth
2. Cooldown management system
3. Structured turn phases
4. Move/Attack/Defend choice system
5. Visual ability panel

---

## PROMPT 3: Strategic Mechanics & Polish
**Objective**: Add center control, tactical massacre, General unit, and balance the complete system.

### Tasks:

#### 3.1 Center Control Mechanic (Priority: HIGH)
**Files to create/modify:**
- `src/domain/services/center_control.py` (new)
- `src/domain/batalla.py`

```python
# center_control.py
class ControlCentro:
    def __init__(self, tablero: Tablero):
        self.tablero = tablero
        self._definir_centro()
        self.turnos_sin_control = {
            Bando.ROMA: 0,
            Bando.BARBAROS: 0
        }

    def _definir_centro(self):
        """Define 4 center tiles for 9x7 board"""
        filas_centro = self.tablero.filas // 2
        cols_centro = self.tablero.columnas // 2

        self.casillas_centro = [
            Posicion(filas_centro, cols_centro),
            Posicion(filas_centro, cols_centro + 1),
            Posicion(filas_centro + 1, cols_centro),
            Posicion(filas_centro + 1, cols_centro + 1)
        ]

    def verificar_control(self, bando: Bando) -> bool:
        """Check if bando controls any center tile"""
        for casilla in self.casillas_centro:
            unidad = self.tablero.obtener_unidad_en(casilla)
            if unidad and unidad.bando == bando:
                return True
        return False

    def aplicar_penalizacion(self, ejercito: Ejercito) -> Optional[EventoDominio]:
        """Apply -3 morale if no center control"""
        if not self.verificar_control(ejercito.bando):
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

#### 3.2 Tactical Massacre System
**Files to modify:**
- `src/domain/batalla.py`
- `src/domain/events.py`

```python
# Add to Batalla class
class Batalla:
    def __init__(self, ...):
        # existing...
        self._eliminaciones_turno = 0
        self._bando_atacante = None

    def _registrar_eliminacion(self, unidad: Unidad):
        """Track eliminations for massacre bonus"""
        self._eliminaciones_turno += 1

        # Check for tactical massacre (3+ kills)
        if self._eliminaciones_turno >= 3:
            self._aplicar_masacre_tactica()

    def _aplicar_masacre_tactica(self):
        """Apply morale bonus/penalty for massacre"""
        if self._bando_atacante == Bando.ROMA:
            self._ejercito_enemigo.perder_moral(10)
            self._ejercito_jugador.ganar_moral(5)
        else:
            self._ejercito_jugador.perder_moral(10)
            self._ejercito_enemigo.ganar_moral(5)

        self._eventos_pendientes.append(
            EventoMasacreTactica(
                bando_atacante=self._bando_atacante,
                unidades_eliminadas=self._eliminaciones_turno
            )
        )

    def _iniciar_nuevo_turno_jugador(self):
        # existing...
        self._eliminaciones_turno = 0  # Reset counter
```

#### 3.3 General Unit Implementation
**Files to modify:**
- `src/domain/value_objects.py`
- `src/domain/factories.py`

```python
# Add to TipoUnidad enum
class TipoUnidad(Enum):
    # existing...
    GENERAL = "general"

# Add General stats
ESTADISTICAS_UNIDADES[TipoUnidad.GENERAL] = EstadisticasUnidad(
    vida_maxima=96,  # 12 * 8
    ataque=32,  # 4 * 8
    defensa=48,  # 6 * 8
    rango_movimiento=2,
    rango_ataque=1,
    costo_moral=30,  # DEVASTATING loss
    patron_ataque=PatronAtaque.FRONTAL
)

# General ability selection
class FabricaGeneral:
    HABILIDADES_DISPONIBLES = [
        "reagrupar",  # +10 MOR units, +5 army
        "a_la_carga",  # +3 ATQ allies
        "mantened_linea",  # +2 DEF allies
        "envolvimiento",  # Units move twice
        "formacion_escudo"  # +3 DEF, -1 ATQ
    ]

    @staticmethod
    def crear_general(bando: Bando, habilidades_elegidas: List[str]) -> Unidad:
        """Create General with 2 chosen abilities"""
        if len(habilidades_elegidas) != 2:
            raise ValueError("General must have exactly 2 abilities")

        general = Unidad(
            id=f"general_{bando.value}",
            tipo=TipoUnidad.GENERAL,
            bando=bando,
            # ... rest of initialization
        )

        # Add chosen abilities
        for hab_nombre in habilidades_elegidas:
            habilidad = CATALOGO_HABILIDADES[hab_nombre]
            general.gestor_habilidades.agregar_habilidad(habilidad)

        return general
```

#### 3.4 Visual Indicators
**Files to modify:**
- `src/presentation/battle_renderer.py`
- `src/states/batalla_state.py`

```python
# Add center control visualization
def _dibujar_control_centro(self, screen):
    """Highlight center tiles with control status"""
    centro = self.servicio_juego.obtener_casillas_centro()

    for casilla in centro:
        x, y = self._grid_a_pantalla(casilla)
        unidad = self.tablero.obtener_unidad_en(casilla)

        if unidad:
            color = AZUL if unidad.bando == Bando.ROMA else ROJO
        else:
            color = GRIS

        # Draw highlight
        pygame.draw.rect(screen, color,
                        (x-2, y-2, TILE_SIZE+4, TILE_SIZE+4), 3)

# Add massacre counter
def _dibujar_contador_masacre(self, screen):
    """Show kill counter for tactical massacre"""
    kills = self.servicio_juego.obtener_eliminaciones_turno()

    # Draw counter
    texto = f"Kills: {kills}/3"
    color = VERDE if kills >= 3 else BLANCO

    self._dibujar_texto(screen, texto,
                        ANCHO - 150, 50, color)
```

#### 3.5 Balance & Configuration
**Files to create:**
- `src/domain/balance_config.py`

```python
# balance_config.py
class ConfiguracionBalance:
    """Central configuration for game balance"""

    # Morale settings
    MORAL_INICIAL = 100
    MORAL_CENTRO_PERDIDO = 3
    MORAL_MASACRE_ENEMIGO = 10
    MORAL_MASACRE_PROPIO = 5

    # Combat modifiers
    BONUS_FLANQUEO = 2
    BONUS_CARGA_CABALLERIA = 3
    BONUS_TERRENO_ELEVADO = 1
    BONUS_FORMACION_LINEA = 1

    # Ability cooldowns
    COOLDOWN_REAGRUPAR = 3
    COOLDOWN_A_LA_CARGA = 4
    COOLDOWN_LLUVIA_FLECHAS = 2
    COOLDOWN_DISPARO_PRECISO = 3

    # Victory conditions
    UMBRAL_MASACRE = 3  # Units for massacre
    CASILLAS_CENTRO = 4  # Center tiles to control

    # Scaling factor (classic to current)
    FACTOR_ESCALA_STATS = 8
```

#### 3.6 Feature Flags
**Files to create:**
- `src/domain/feature_flags.py`

```python
# feature_flags.py
@dataclass
class ConfiguracionReglas:
    """Toggle classic vs legacy rules"""
    usar_moral_ejercito: bool = True
    usar_formula_clasica: bool = True
    usar_patrones_ataque: bool = True
    usar_habilidades: bool = True
    usar_control_centro: bool = True
    usar_masacre_tactica: bool = True
    usar_general: bool = True

    @classmethod
    def modo_clasico_completo(cls):
        """All classic rules enabled"""
        return cls(
            usar_moral_ejercito=True,
            usar_formula_clasica=True,
            usar_patrones_ataque=True,
            usar_habilidades=True,
            usar_control_centro=True,
            usar_masacre_tactica=True,
            usar_general=True
        )

    @classmethod
    def modo_hibrido(cls):
        """Mix of old and new"""
        return cls(
            usar_moral_ejercito=True,  # New victory
            usar_formula_clasica=False,  # Keep old damage
            usar_patrones_ataque=True,  # Add patterns
            usar_habilidades=True,  # Add abilities
            usar_control_centro=False,  # No center
            usar_masacre_tactica=True,  # Add massacre
            usar_general=False  # No general yet
        )
```

### Testing Checklist:
- [ ] Center tiles highlighted correctly
- [ ] -3 morale applied when center lost
- [ ] 3+ kills triggers massacre bonus
- [ ] General death causes -30 morale
- [ ] General abilities work with cooldowns
- [ ] Feature flags toggle mechanics correctly
- [ ] Game balanced (50-50 win rate)

### Expected Outcome:
After Prompt 3, the game will have:
1. Complete classic rules integration
2. Strategic center control mechanic
3. Tactical massacre rewards
4. General unit with chosen abilities
5. Configurable rule sets
6. Balanced and polished gameplay

---

## Final Integration Testing

### System Integration Tests:
```python
def test_complete_battle_flow():
    """Test all systems working together"""
    # Setup
    batalla = crear_batalla_con_reglas_clasicas()

    # Test morale victory
    assert batalla.ejercito_enemigo.moral_general == 100

    # Kill expensive unit (General)
    eliminar_unidad(batalla.ejercito_enemigo.general)
    assert batalla.ejercito_enemigo.moral_general == 70

    # Test center control
    mover_todas_unidades_fuera_centro(batalla.ejercito_jugador)
    batalla.finalizar_turno()
    assert batalla.ejercito_jugador.moral_general == 97

    # Test massacre
    eliminar_multiples_unidades(batalla.ejercito_enemigo, count=3)
    assert batalla.ejercito_enemigo.moral_general == 50
    assert batalla.ejercito_jugador.moral_general == 102  # Capped at 100

    # Test abilities
    usar_habilidad(batalla.general_jugador, "reagrupar")
    assert batalla.general_jugador.habilidades[0].cooldown_actual == 3

    # Test victory
    batalla.ejercito_enemigo.moral_general = 0
    assert batalla.ganador == Bando.ROMA
```

### Performance Benchmarks:
- Turn processing: < 100ms
- Ability calculation: < 50ms
- UI update: 60 FPS maintained
- Memory usage: < 500MB

---

## Summary

This 3-prompt implementation plan transforms Legio Romana from a unit-elimination tactical game into a strategic morale-based battle system with:

1. **Prompt 1**: Core morale victory + improved combat formula + attack patterns
2. **Prompt 2**: Abilities system + turn phases + movement restrictions
3. **Prompt 3**: Center control + massacre bonus + General unit + polish

Each prompt builds on the previous one, ensuring stable incremental development while maintaining the existing DDD architecture and unit variety. The final result will be a more strategically deep game that rewards positioning, timing, and resource management over simple unit elimination.

**Total estimated effort**: 7-10 days of development
**Risk level**: Low (incremental, backwards-compatible)
**Impact**: High (completely transforms gameplay depth)