# Sprint 2-3 Roadmap: Short-term Clean Code Improvements

## Overview
This document provides a detailed implementation plan for the next phase of Clean Code improvements for Legio Romana.

**Estimated Time**: 19-25 hours (2-3 weeks at 10 hours/week)
**Priority**: Medium (Foundation from Sprint 1 is complete)
**Status**: Ready to start

---

## Prerequisites (✅ Completed in Sprint 1)

- ✅ 55 passing unit tests
- ✅ Logging system in place
- ✅ 50+ named constants extracted
- ✅ No silent failures (proper error propagation)

---

## Task 1: Split services.py into Separate Files (6-8 hours)

### Current State
- **File**: `src/domain/services.py`
- **Size**: 555 lines
- **Classes**: 8 domain services in one file
- **Problem**: Violates Single Responsibility Principle at file level

### Target Structure
```
src/domain/services/
├── __init__.py                        # Central export point
├── combat_calculator.py               # CalculadorCombate
├── priority_calculator.py             # CalculadorPrioridad
├── movement_calculator.py             # CalculadorMovimiento
├── formation_calculator.py            # CalculadorFormacion
├── focus_fire_system.py               # SistemaFocusFire
├── threat_evaluator.py                # EvaluadorAmenazas
├── tactical_position_calculator.py    # CalculadorPosicionTactica
└── formation_manager.py               # GestorFormacionesDinamico
```

### Implementation Steps

#### Step 1.1: Create Directory & Extract CombatCalculator (1 hour)
```python
# src/domain/services/combat_calculator.py
import random
from src.domain.entities import Unidad
from src.domain.value_objects import TipoUnidad, ResultadoAtaque
from src.domain.constants import (
    VARIANZA_DANIO_MIN, VARIANZA_DANIO_MAX,
    MORAL_PERDIDA_MAX_POR_DANIO
)

class CalculadorCombate:
    """Combat calculation domain service"""

    @staticmethod
    def calcular_danio(atacante: Unidad, defensor: Unidad) -> int:
        # ... existing implementation

    @staticmethod
    def ejecutar_ataque(atacante: Unidad, defensor: Unidad) -> ResultadoAtaque:
        # ... existing implementation

    @staticmethod
    def calcular_bonificacion_formacion(atacante: Unidad, formacion: str) -> int:
        # ... existing implementation
```

**Commands:**
```bash
mkdir -p src/domain/services
# Copy-paste CalculadorCombate class to combat_calculator.py
# Test: python -m pytest tests/test_combate.py -v
```

#### Step 1.2: Extract PriorityCalculator (30 min)
```python
# src/domain/services/priority_calculator.py
from typing import List, Optional
from src.domain.entities import Unidad
from src.domain.value_objects import TipoUnidad
from src.domain.constants import (
    UMBRAL_VIDA_CRITICA, UMBRAL_VIDA_HERIDO,
    PRIORIDAD_CASI_MUERTO, PRIORIDAD_HERIDO,
    PRIORIDAD_SAGITTARII, PRIORIDAD_EQUITES, etc.
)

class CalculadorPrioridad:
    """Target prioritization service for AI"""
    # ... move implementation
```

#### Step 1.3: Extract Remaining Services (2-3 hours)
Repeat for:
- `movement_calculator.py` (CalculadorMovimiento)
- `formation_calculator.py` (CalculadorFormacion)
- `focus_fire_system.py` (SistemaFocusFire)
- `threat_evaluator.py` (EvaluadorAmenazas)
- `tactical_position_calculator.py` (CalculadorPosicionTactica)
- `formation_manager.py` (GestorFormacionesDinamico)

#### Step 1.4: Create __init__.py (30 min)
```python
# src/domain/services/__init__.py
"""
Domain services package
Exports all domain service classes for easy importing
"""

from .combat_calculator import CalculadorCombate
from .priority_calculator import CalculadorPrioridad
from .movement_calculator import CalculadorMovimiento
from .formation_calculator import CalculadorFormacion
from .focus_fire_system import SistemaFocusFire
from .threat_evaluator import EvaluadorAmenazas
from .tactical_position_calculator import CalculadorPosicionTactica
from .formation_manager import GestorFormacionesDinamico

__all__ = [
    'CalculadorCombate',
    'CalculadorPrioridad',
    'CalculadorMovimiento',
    'CalculadorFormacion',
    'SistemaFocusFire',
    'EvaluadorAmenazas',
    'CalculadorPosicionTactica',
    'GestorFormacionesDinamico',
]
```

#### Step 1.5: Update Imports (2-3 hours)
**Files to update:**

1. **`src/domain/strategies.py`** (imports 6 services)
```python
# Before
from src.domain.services import (
    CalculadorCombate, CalculadorPrioridad, CalculadorMovimiento,
    SistemaFocusFire, EvaluadorAmenazas, CalculadorPosicionTactica,
    GestorFormacionesDinamico
)

# After (unchanged - __init__.py exports everything)
from src.domain.services import (
    CalculadorCombate, CalculadorPrioridad, CalculadorMovimiento,
    SistemaFocusFire, EvaluadorAmenazas, CalculadorPosicionTactica,
    GestorFormacionesDinamico
)
```

2. **`src/states/batalla_state.py`** (imports 2 services)
```python
from src.domain.services import CalculadorPrioridad, CalculadorMovimiento
```

3. **Test files** (if any directly import services)

#### Step 1.6: Delete Old services.py & Verify (30 min)
```bash
# Run all tests
python -m pytest tests/ -v

# If all pass, delete old file
rm src/domain/services.py  # or rename to services.py.backup

# Final test
python -m pytest tests/ -v
python main.py  # Manual smoke test
```

### Success Criteria
- ✅ 8 separate service files created
- ✅ `services/__init__.py` exports all classes
- ✅ All imports updated (no breaking changes)
- ✅ All 55 tests pass
- ✅ Old `services.py` deleted
- ✅ Game runs without errors

---

## Task 2: Improve Use Case Exception Handling (2-3 hours)

### Current State (Partial - from Sprint 1)
```python
# use_cases.py
try:
    return batalla.seleccionar_unidad(id_unidad)
except ExcepcionDominio as e:
    logger.warning(f"Acción inválida: {e}")
    return []  # ⚠️ UI gets empty list, no error context
```

### Improvement: Return Error Events

#### Step 2.1: Create EventoError (30 min)
```python
# src/domain/events.py

@dataclass(frozen=True)
class EventoError(EventoDominio):
    """Evento que representa un error del dominio"""
    mensaje: str
    codigo_error: str  # e.g., "UNIT_NOT_FOUND", "INVALID_MOVE"
    detalles: Optional[dict] = None

    def __str__(self):
        return f"Error [{self.codigo_error}]: {self.mensaje}"
```

#### Step 2.2: Update Use Cases (1 hour)
```python
# src/application/use_cases.py

class CasoUsoSeleccionarUnidad:
    def ejecutar(self, batalla: Batalla, id_unidad: str) -> List[EventoDominio]:
        try:
            return batalla.seleccionar_unidad(id_unidad)
        except ExcepcionTurnoInvalido as e:
            logger.warning(f"Turno inválido: {e}")
            return [EventoError(str(e), "INVALID_TURN")]
        except ExcepcionUnidadNoEncontrada as e:
            logger.warning(f"Unidad no encontrada: {e}")
            return [EventoError(str(e), "UNIT_NOT_FOUND")]
        except ExcepcionAccionInvalida as e:
            logger.warning(f"Acción inválida: {e}")
            return [EventoError(str(e), "INVALID_ACTION")]
        except Exception as e:
            logger.error(f"Error inesperado: {e}", exc_info=True)
            raise

# Repeat for all use cases:
# - CasoUsoMoverUnidad
# - CasoUsoAtacarEnemigo
# - CasoUsoFinalizarTurno
# - CasoUsoAplicarFormacion
```

#### Step 2.3: Handle in BatallaState (30 min)
```python
# src/states/batalla_state.py

def _procesar_eventos(self, eventos):
    for evento in eventos:
        if isinstance(evento, EventoError):
            self._mostrar_mensaje(f"⚠️ {evento.mensaje}")
            self.renderer.notification_system.add_notification(
                evento.mensaje,
                (255, 100, 100),  # Red color for errors
                duration=3.0
            )
        # ... rest of event processing
```

#### Step 2.4: Add Tests (30 min)
```python
# tests/test_use_cases.py

def test_seleccionar_unidad_invalida_retorna_evento_error():
    """Test que seleccionar unidad inválida retorna EventoError"""
    batalla = crear_batalla_test()
    caso_uso = CasoUsoSeleccionarUnidad()

    eventos = caso_uso.ejecutar(batalla, "unidad-inexistente")

    assert len(eventos) == 1
    assert isinstance(eventos[0], EventoError)
    assert eventos[0].codigo_error == "UNIT_NOT_FOUND"
```

### Success Criteria
- ✅ `EventoError` domain event created
- ✅ All 5 use cases return error events
- ✅ BatallaState displays errors to user
- ✅ Tests cover error scenarios
- ✅ No silent failures

---

## Task 3: Apply Dependency Injection to ServicioJuego (3-4 hours)

### Current Problem
```python
class ServicioJuego:
    def __init__(self):
        # ❌ Hard-coded dependencies - cannot mock for testing
        self._caso_iniciar = CasoUsoIniciarBatalla()
        self._caso_seleccionar = CasoUsoSeleccionarUnidad()
        # ...
```

### Solution: Constructor Injection with Defaults

#### Step 3.1: Refactor Constructor (1 hour)
```python
# src/application/servicio_juego.py

class ServicioJuego:
    """Application service coordinating use cases"""

    def __init__(
        self,
        caso_iniciar: Optional[CasoUsoIniciarBatalla] = None,
        caso_seleccionar: Optional[CasoUsoSeleccionarUnidad] = None,
        caso_mover: Optional[CasoUsoMoverUnidad] = None,
        caso_atacar: Optional[CasoUsoAtacarEnemigo] = None,
        caso_finalizar: Optional[CasoUsoFinalizarTurno] = None,
        caso_formacion: Optional[CasoUsoAplicarFormacion] = None,
        caso_estado: Optional[CasoUsoObtenerEstadoBatalla] = None
    ):
        """
        Constructor with dependency injection.

        Args:
            caso_*: Use case instances (optional, defaults provided)
        """
        self._batalla_actual: Optional[Batalla] = None

        # Inject dependencies or use defaults
        self._caso_iniciar = caso_iniciar or CasoUsoIniciarBatalla()
        self._caso_seleccionar = caso_seleccionar or CasoUsoSeleccionarUnidad()
        self._caso_mover = caso_mover or CasoUsoMoverUnidad()
        self._caso_atacar = caso_atacar or CasoUsoAtacarEnemigo()
        self._caso_finalizar = caso_finalizar or CasoUsoFinalizarTurno()
        self._caso_formacion = caso_formacion or CasoUsoAplicarFormacion()
        self._caso_estado = caso_estado or CasoUsoObtenerEstadoBatalla()

        self._eventos_procesados = []

        logger.info("ServicioJuego initialized with use cases")
```

#### Step 3.2: Add Factory Methods (30 min)
```python
class ServicioJuego:
    # ... __init__ above

    @classmethod
    def crear_para_produccion(cls):
        """Factory method for production use (default behavior)"""
        return cls()

    @classmethod
    def crear_para_testing(
        cls,
        batalla_mock: Optional[Batalla] = None,
        **use_case_mocks
    ):
        """Factory method for testing with mocks"""
        return cls(**use_case_mocks)
```

#### Step 3.3: Create Test Demonstrating Mockability (1 hour)
```python
# tests/test_servicio_juego_di.py

from unittest.mock import Mock, MagicMock
from src.application.servicio_juego import ServicioJuego
from src.domain.events import EventoBatallaIniciada

def test_servicio_juego_dependency_injection():
    """Test that ServicioJuego accepts injected dependencies"""
    # Create mock use case
    mock_caso_iniciar = Mock()
    mock_batalla = Mock()
    mock_evento = EventoBatallaIniciada(ronda=1, mensaje="Test")
    mock_caso_iniciar.ejecutar.return_value = (mock_batalla, [mock_evento])

    # Inject mock into service
    servicio = ServicioJuego(caso_iniciar=mock_caso_iniciar)

    # Execute
    eventos = servicio.iniciar_nueva_batalla("normal")

    # Verify mock was called
    mock_caso_iniciar.ejecutar.assert_called_once_with("normal")
    assert len(eventos) == 1
    assert eventos[0] == mock_evento


def test_servicio_juego_defaults_work():
    """Test that default use cases work without injection"""
    servicio = ServicioJuego()  # No args - should use defaults

    # Should work normally
    eventos = servicio.iniciar_nueva_batalla("normal")

    assert len(eventos) > 0
    assert servicio.obtener_batalla_actual() is not None
```

#### Step 3.4: Update Documentation (30 min)
Add to docstrings, README, and code comments explaining the DI pattern.

### Success Criteria
- ✅ Constructor accepts optional dependencies
- ✅ Defaults preserve existing behavior (backward compatible)
- ✅ Factory methods created
- ✅ Tests demonstrate mockability
- ✅ All existing tests pass

---

## Task 4: Standardize Naming to English (8-10 hours)

### Translation Reference

#### Core Classes
| Spanish | English |
|---------|---------|
| ServicioJuego | GameService |
| CasoUsoIniciarBatalla | StartBattleUseCase |
| CalculadorCombate | CombatCalculator |
| FabricaEjercito | ArmyFactory |
| Batalla | Battle |
| Unidad | Unit |
| Ejercito | Army |
| Tablero | Board |

#### Method Names (Most Common)
| Spanish | English |
|---------|---------|
| obtener_* | get_* |
| seleccionar_unidad | select_unit |
| mover_unidad | move_unit |
| atacar_con_unidad | attack_with_unit |
| finalizar_turno | end_turn |
| aplicar_formacion | apply_formation |
| reiniciar_turno | reset_turn |
| calcular_danio | calculate_damage |
| ejecutar_ataque | execute_attack |
| evaluar_amenaza | evaluate_threat |

#### Variables
| Spanish | English |
|---------|---------|
| batalla_actual | current_battle |
| ejercito_jugador | player_army |
| ejercito_enemigo | enemy_army |
| unidad_seleccionada | selected_unit |
| ronda_actual | current_round |
| turno_actual | current_turn |
| batalla_terminada | battle_ended |

### Implementation Strategy

**Recommended Approach: IDE Refactoring + Systematic Testing**

#### Step 4.1: Preparation (1 hour)
```bash
# Create feature branch
git checkout -b feat/english-naming

# Run tests to establish baseline
python -m pytest tests/ -v > tests_before.txt

# Create backup
git add -A
git commit -m "Backup before English naming refactoring"
```

#### Step 4.2: Phase 1 - Domain Entities (2 hours)
**File: `src/domain/entities.py`**

Use IDE "Rename Symbol" feature (F2 in VSCode) for each:
```python
# Unidad class
obtener_posiciones_movimiento_validas → get_valid_movement_positions
obtener_objetivos_atacables → get_attackable_targets
calcular_danio_contra → calculate_damage_against
recibir_danio → receive_damage
restaurar_moral → restore_morale
marcar_como_actuada → mark_as_acted
reiniciar_turno → reset_turn

# Ejercito class
obtener_unidad_por_id → get_unit_by_id
obtener_unidad_en_posicion → get_unit_at_position
remover_unidades_muertas → remove_dead_units
reiniciar_turno_todas_unidades → reset_all_units_turn
aplicar_formacion → apply_formation

# Tablero class
esta_ocupada → is_occupied
obtener_unidad_en → get_unit_at
obtener_todas_las_posiciones → get_all_positions
registrar_ejercito → register_army
```

**After each rename:**
```bash
python -m pytest tests/ -v  # Verify tests still pass
git add -A
git commit -m "Rename: obtener_* → get_* in entities.py"
```

#### Step 4.3: Phase 2 - Application Layer (2 hours)
**File: `src/application/servicio_juego.py`**
```python
# Rename class
ServicioJuego → GameService

# Rename methods
iniciar_nueva_batalla → start_new_battle
iniciar_batalla_desde_nivel → start_battle_from_level
seleccionar_unidad → select_unit
mover_unidad → move_unit
atacar_enemigo → attack_enemy
finalizar_turno → end_turn
aplicar_formacion → apply_formation
obtener_estado_batalla → get_battle_state
obtener_batalla_actual → get_current_battle
deseleccionar_unidad → deselect_unit
reiniciar_juego → reset_game
obtener_historial_eventos → get_event_history
```

**File: `src/application/use_cases.py`**
```python
CasoUsoIniciarBatalla → StartBattleUseCase
CasoUsoSeleccionarUnidad → SelectUnitUseCase
CasoUsoMoverUnidad → MoveUnitUseCase
CasoUsoAtacarEnemigo → AttackEnemyUseCase
CasoUsoFinalizarTurno → EndTurnUseCase
CasoUsoAplicarFormacion → ApplyFormationUseCase
CasoUsoObtenerEstadoBatalla → GetBattleStateUseCase
```

#### Step 4.4: Phase 3 - Supporting Files (2 hours)
- `src/domain/batalla.py`
- `src/domain/strategies.py`
- `src/domain/factories.py`

#### Step 4.5: Phase 4 - Update Tests (1-2 hours)
Update fixtures and test methods to use new names.

```python
# tests/conftest.py
@pytest.fixture
def unidad_legionario():  # Keep Spanish for now, or rename to legionary_unit
    ...
```

#### Step 4.6: Final Verification (1 hour)
```bash
# Run full test suite
python -m pytest tests/ -v > tests_after.txt

# Compare results
diff tests_before.txt tests_after.txt

# Verify game runs
python main.py

# Search for remaining Spanish (should find minimal results)
grep -r "obtener_\|seleccionar_\|mover_\|atacar_\|finalizar_" src/ --include="*.py" | wc -l

# Commit final changes
git add -A
git commit -m "Complete: English naming standardization"
git checkout main
git merge feat/english-naming
```

### Success Criteria
- ✅ All 154 Spanish method names renamed
- ✅ All test names updated
- ✅ All 55 tests pass
- ✅ Game runs without errors
- ✅ grep finds 0 Spanish naming patterns
- ✅ Code more accessible to international developers

---

## Testing Strategy

### After Each Task
```bash
# Run full test suite
python -m pytest tests/ -v --tb=short

# Run with coverage (optional)
python -m pytest tests/ --cov=src --cov-report=term

# Manual smoke test
python main.py
```

### Regression Prevention
- ✅ Use git branches for each task
- ✅ Commit after each working state
- ✅ Run tests before and after each change
- ✅ Keep Sprint 1's 55 tests as safety net

---

## Timeline

### Week 1: Services & Exceptions
- **Monday-Tuesday**: Task 1 - Split services.py (6-8h)
- **Wednesday-Thursday**: Task 2 - Exception events (2-3h)
- **Friday**: Review & catch up

### Week 2: DI & Naming Prep
- **Monday**: Task 3 - Dependency Injection (3-4h)
- **Tuesday-Thursday**: Task 4 Phase 1-2 - Domain & Application naming (4h)
- **Friday**: Review & testing

### Week 3: Complete Naming
- **Monday-Wednesday**: Task 4 Phase 3-4 - Remaining files & tests (4-6h)
- **Thursday**: Final verification & documentation
- **Friday**: Buffer for unexpected issues

---

## Next Steps

1. **Review this plan** with team/stakeholders
2. **Create git branch** for Sprint 2-3 work
3. **Start with Task 1** (highest priority - services split)
4. **Update SPRINT2_3_SUMMARY.md** as you complete tasks

---

## Questions to Resolve Before Starting

1. **English naming**: Keep "Unidad" as "Unit" or "Unidad"? (Recommend: Unit)
2. **Breaking changes**: Acceptable for major version bump?
3. **Testing**: Need more integration tests before refactoring?
4. **Timeline**: Can dedicate 10 hours/week consistently?

---

## Success Metrics

**Sprint 2-3 will be considered successful when:**

- ✅ `services.py` split into 8 focused files
- ✅ All use cases return error events
- ✅ `ServicioJuego` supports dependency injection
- ✅ All Spanish naming converted to English
- ✅ All 55+ tests pass
- ✅ No regressions in game functionality
- ✅ Code easier to navigate and understand

**Architecture Score Improvement:**
- Before Sprint 2-3: 7.5/10
- Target After Sprint 2-3: 8.5/10

---

## Resources

- Sprint 1 Summary: `SPRINT1_SUMMARY.md`
- Clean Code Review: Original review document
- Test suite: `tests/` directory (55 tests)
- Naming reference: This document, Task 4 section

---

**Ready to start? Begin with Task 1: Split services.py**

Good luck! 🚀
