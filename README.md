# Strategy/Simulation Game

A tile-based strategy/simulation game built with Pygame.

## Features

- **Tile-based map system**: Procedurally generated maps with different terrain types (grass, forest, water, mountains, sand)
- **Entity system**: Units with movement, selection, and health systems
- **Camera system**: Pan and zoom functionality
- **Resource management**: Track and manage resources (gold, food, wood, stone)
- **State management**: Menu system and game states
- **HUD**: Display resources, unit information, and controls

## Installation

1. Make sure you have Python 3.7+ installed
2. Install Pygame:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python main.py
```

## Controls

### Menu
- Click buttons to navigate

### In-Game
- **Camera Movement**:
  - Arrow keys or WASD: Move camera
  - Mouse wheel: Zoom in/out

- **Unit Control**:
  - Left click: Select units
  - Right click: Move selected units
  - ESC: Return to menu

## Project Structure

```
├── main.py                 # Entry point
├── src/
│   ├── core/              # Core game systems
│   │   ├── game.py        # Main game class
│   │   ├── state.py       # Base state class
│   │   └── state_manager.py
│   ├── entities/          # Game entities
│   │   ├── entity.py      # Base entity class
│   │   └── unit.py        # Unit class
│   ├── states/            # Game states
│   │   ├── menu_state.py  # Main menu
│   │   └── game_state.py  # Gameplay state
│   ├── systems/           # Game systems
│   │   ├── camera.py      # Camera/viewport
│   │   ├── entity_manager.py
│   │   ├── map_system.py  # Tile map
│   │   └── resource_manager.py
│   ├── ui/                # UI components
│   │   ├── button.py
│   │   └── hud.py         # Heads-up display
│   └── utils/
│       └── constants.py   # Game configuration
├── assets/                # Game assets
│   ├── sprites/
│   ├── sounds/
│   └── fonts/
└── data/                  # Game data files
```

## Extending the Game

### Adding New Unit Types

1. Add unit configuration to `src/utils/constants.py`:
   - Add to `UNIT_COSTS` dictionary
   - Add to `UNIT_STATS` dictionary

2. Update the `Unit` class in `src/entities/unit.py` if needed

### Adding New Buildings

1. Create a new `Building` class in `src/entities/building.py`
2. Add building costs to `BUILDING_COSTS` in constants
3. Update the entity manager to handle buildings

### Adding New Terrain Types

1. Add new terrain type to `TileType` enum in `src/systems/map_system.py`
2. Add color mapping in `Tile.get_color()`
3. Update terrain movement costs in constants

### Implementing Pathfinding

The game structure is ready for A* pathfinding:
1. Create `src/systems/pathfinding.py`
2. Use the map system's walkability data
3. Integrate with unit movement

### Adding Combat System

1. Create `src/systems/combat.py`
2. Add attack methods to units
3. Implement damage calculation
4. Add combat animations

## Future Enhancements

- [ ] Pathfinding (A* algorithm)
- [ ] Building placement system
- [ ] Combat system
- [ ] Fog of war
- [ ] Minimap
- [ ] Save/Load system
- [ ] Sound effects and music
- [ ] Particle effects
- [ ] Multiplayer support
- [ ] AI opponents
- [ ] Resource gathering animations
- [ ] Day/night cycle
- [ ] Weather effects
- [ ] Unit formations
- [ ] Technology tree

## License

This project is open source. Feel free to use and modify it for your own projects.