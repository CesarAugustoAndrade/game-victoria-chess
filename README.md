# Strategy / Simulation Game

A tile-based strategy/simulation game built with Pygame. It features a procedurally generated terrain map, selectable units, a pan/zoom camera, resource tracking, and a state-driven menu/gameplay loop.

## Features

- **Tile-based map system**: procedurally generated maps with several terrain types (grass, forest, water, mountains, sand); water and mountains are non-walkable.
- **Entity system**: units with movement, selection and health, managed by an entity manager.
- **Camera system**: pan (arrow keys / WASD), edge scrolling and zoom.
- **Resource management**: tracks gold, food, wood and stone, with configurable starting amounts and gather rates.
- **State management**: menu and gameplay states via a state manager.
- **HUD**: displays resources, unit information and controls.
- **Data-driven constants**: unit costs/stats, building costs/stats and terrain movement costs are defined in `src/utils/constants.py` (ready for buildings and combat to be wired up).

## Tech Stack

- **Python 3.7+**
- **[Pygame](https://www.pygame.org/)** 2.5.2 (see `requirements.txt`)

## Getting Started

### Prerequisites

- Python 3.7 or newer

### Installation

```bash
pip install -r requirements.txt
```

### Running the Game

```bash
python main.py
```

### Controls

**Menu**
- Click buttons to navigate

**In-Game**
- Arrow keys or WASD: move camera
- Mouse wheel: zoom in/out
- Left click: select units
- Right click: move selected units
- ESC: return to menu

## Project Structure

```
├── main.py                     # Entry point (Pygame loop, delta-time update/render)
├── requirements.txt            # Dependencies (pygame)
└── src/
    ├── core/                   # Core game systems
    │   ├── game.py             # Main game class
    │   ├── state.py            # Base state class
    │   └── state_manager.py    # State stack/transitions
    ├── entities/               # Game entities
    │   ├── entity.py           # Base entity class
    │   └── unit.py             # Unit class
    ├── states/                 # Game states
    │   ├── menu_state.py       # Main menu
    │   └── game_state.py       # Gameplay state
    ├── systems/                # Game systems
    │   ├── camera.py           # Camera / viewport (pan + zoom)
    │   ├── entity_manager.py   # Entity registry / updates
    │   ├── map_system.py       # Tile map + terrain generation
    │   └── resource_manager.py # Resource tracking
    ├── ui/                     # UI components
    │   ├── button.py
    │   └── hud.py              # Heads-up display
    └── utils/
        └── constants.py        # Window, camera, unit/building, terrain & resource config
```

## Extending the Game

The codebase is structured to make these additions straightforward; constants for several of them already live in `src/utils/constants.py`.

### Adding New Unit Types

1. Add the type to `UNIT_COSTS` and `UNIT_STATS` in `src/utils/constants.py`.
2. Extend the `Unit` class in `src/entities/unit.py` if new behavior is needed.

### Adding Buildings

`BUILDING_COSTS` and `BUILDING_HEALTH` are already defined in constants. To implement buildings:

1. Add a `Building` entity in `src/entities/`.
2. Handle placement and updates in the entity manager.

### Adding New Terrain Types

1. Add the value to the `TileType` enum in `src/systems/map_system.py`.
2. Add a color in `Tile.get_color()`.
3. Add a movement cost in `TERRAIN_MOVE_COSTS` in constants.

### Implementing Pathfinding

Terrain movement costs and per-tile `walkable` flags are already available:

1. Add `src/systems/pathfinding.py` (e.g. A*).
2. Use the map system's walkability/cost data.
3. Integrate with unit movement.

## Future Enhancements

- [ ] Pathfinding (A*)
- [ ] Building placement system
- [ ] Combat system
- [ ] Fog of war / minimap
- [ ] Save / load
- [ ] Sound effects and music
- [ ] AI opponents

## License

Open source — feel free to use and modify it for your own projects.
