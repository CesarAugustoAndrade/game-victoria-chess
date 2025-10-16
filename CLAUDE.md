# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Legio Romana** is a turn-based tactical battle game built with Pygame featuring Roman military units. The game combines a generic tile-based strategy/simulation framework with a Domain-Driven Design (DDD) battle system for tactical Roman warfare.

## Running the Game

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## Architecture

### Dual Architecture Pattern

The codebase has **two distinct architectures** that coexist:

1. **Generic Strategy Game Framework** (`src/entities`, `src/systems`, `src/ui`)
   - Entity-Component style system
   - General-purpose map, camera, resource management
   - Intended for extensible strategy/simulation games

2. **Domain-Driven Battle System** (`src/domain`, `src/application`, `src/presentation`)
   - Clean architecture with DDD principles
   - Roman battle-specific tactical combat
   - Event-sourced battle mechanics

### Core Architecture Components

#### State Management System
- **StateManager** (`src/core/state_manager.py`): Stack-based state management
- States have lifecycle hooks: `on_enter()`, `on_exit()`, `on_pause()`, `on_resume()`
- Main game loop coordinates through `Game` class which delegates to current state

#### Domain Layer (DDD - Battle System)
- **Batalla** (`src/domain/batalla.py`): Aggregate root managing complete battles
  - Enforces turn-based gameplay (Player → AI → new round)
  - Manages unit selection, movement, and combat
  - Emits domain events for all actions
  - Validates all operations through business rules

- **Entities** (`src/domain/entities.py`):
  - `Unidad`: Military unit with stats, morale, position, and combat capabilities
  - `Ejercito`: Army aggregate managing collection of units and formations
  - `Tablero`: Battlefield board (9x7 grid) tracking positions and occupancy

- **Value Objects** (`src/domain/value_objects.py`):
  - `TipoUnidad`: Unit types (Legionario, Hastati, Principes, Triarii, Equites, etc.)
  - `Bando`: Factions (ROMA vs BARBAROS)
  - `Posicion`: Grid position with Manhattan distance calculation
  - `EstadisticasUnidad`: Combat stats (health, attack, defense, movement/attack range)
  - `VisualizacionUnidad`: UI representation (name, color, war cry)

- **Domain Events** (`src/domain/events.py`): Event-driven architecture
  - All actions produce events (unit moved, attack performed, battle ended, etc.)
  - Events drive UI updates and game state changes

- **Domain Services** (`src/domain/services.py`):
  - `CalculadorCombate`: Centralized combat calculation with random variance
  - Handles damage, morale loss, and unit elimination

#### Application Layer
- **ServicioJuego** (`src/application/servicio_juego.py`): Application service coordinating use cases
- **Use Cases** (`src/application/use_cases.py`): Individual business operations
  - Each use case encapsulates one game action (select unit, move, attack, end turn, etc.)

#### Presentation Layer
- **BatallaState** (`src/states/batalla_state.py`): Game state managing battle UI and input
  - Translates Pygame events to domain commands
  - Processes domain events into visual feedback
  - Manages highlights for valid moves and attackable targets

- **BattleRenderer** (`src/presentation/battle_renderer.py`): Renders battlefield visuals
- **UnitSprites** (`src/presentation/unit_sprites.py`): Unit visual representations

### Game Flow

1. **Menu** → Click "Play" → **BatallaState** initializes
2. **BatallaState** → Creates **ServicioJuego** → Executes `CasoUsoIniciarBatalla`
3. **Use Case** → Creates **Batalla** aggregate with armies, board, and AI strategy
4. **Player Turn**: Select unit → Move/Attack → End turn
5. **AI Turn**: AI strategy executes automatically → Returns to player turn
6. **Battle End**: One army eliminated → Victory/Defeat screen

### Important Patterns

#### Event-Driven Combat
All domain actions return `List[EventoDominio]`. These events:
- Drive UI updates (messages, animations, highlights)
- Maintain battle history
- Decouple domain logic from presentation

#### Turn-Based State Machine
```python
TurnoActual.JUGADOR → Player actions → finalizar_turno_jugador()
→ TurnoActual.ENEMIGO → AI executes → Auto-finalizes
→ New round → TurnoActual.JUGADOR (increment ronda_actual)
```

#### Morale System
- Units have morale (0-100)
- Lose morale when damaged
- Units with morale < 30 are "in panic" and cannot act
- Formations and turn regeneration restore morale

#### Formation System
- **Testudo** (Tortuga): +defense, restores morale
- **Cuneus** (Cuña): +attack for legionaries
- **Orbis** (Círculo): restores morale
- **Linea**: Default formation

## Key Files

- `main.py`: Entry point, game loop
- `src/core/game.py`: Main game coordinator
- `src/utils/constants.py`: All game configuration (resources, units, terrain, UI dimensions)
- `src/domain/batalla.py`: Battle aggregate root (primary domain logic)
- `src/application/servicio_juego.py`: Application service facade
- `src/states/batalla_state.py`: Battle UI state and input handling

## Adding New Features

### Adding New Unit Types
1. Add to `TipoUnidad` enum in `src/domain/value_objects.py`
2. Add stats to `ESTADISTICAS_UNIDADES` dict in `src/domain/value_objects.py`
3. Add visualization to `VISUALIZACIONES_UNIDADES` in `src/domain/value_objects.py`
4. Update factories in `src/domain/factories.py` if creating preset armies

### Adding New Battle Mechanics
1. Add logic to `Batalla` aggregate (`src/domain/batalla.py`)
2. Create new domain events if needed (`src/domain/events.py`)
3. Create use case in `src/application/use_cases.py`
4. Expose through `ServicioJuego` (`src/application/servicio_juego.py`)
5. Wire up UI input in `BatallaState` (`src/states/batalla_state.py`)

### AI Strategies
- Implement `EstrategiaIA` interface (`src/domain/strategies.py`)
- AI gets full access to both armies and board
- Must return list of domain events from actions taken

## Game Controls

**Menu**: Click buttons
**Battle**:
- Left click: Select friendly unit / Move to valid position
- Right click: Attack enemy unit (if in range)
- Space: End turn
- F: Change formation
- R: Restart battle (when finished)
- ESC: Return to menu

## Testing

No test suite currently exists in the repository.
