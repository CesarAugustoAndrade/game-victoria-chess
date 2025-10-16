# 🏛️ LEGIO ROMANA - Juego de Batalla Táctica

Un juego de estrategia táctica por turnos basado en las legiones romanas, construido con Pygame y arquitectura Domain-Driven Design (DDD).

![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)
![Pygame Version](https://img.shields.io/badge/Pygame-2.5.2-green)
![Architecture](https://img.shields.io/badge/Architecture-DDD-purple)
![Status](https://img.shields.io/badge/Status-Playable-success)

## ⚔️ Descripción

Comanda las legendarias legiones romanas contra hordas bárbaras en batallas tácticas por turnos. El juego presenta combate estratégico en un tablero de 9x7 con unidades históricamente inspiradas, sistema de moral, y formaciones tácticas auténticas.

## 🎮 Características

### Sistema de Batalla
- **Combate por turnos** en tablero táctico 9x7
- **Sistema de moral** que afecta el rendimiento en batalla
- **Formaciones romanas** históricas (Testudo, Cuneus, Orbis)
- **IA enemiga** con 3 niveles de dificultad (Defensiva, Agresiva, Táctica)
- **Gritos de guerra** en latín auténtico

### Unidades Romanas 🦅

| Unidad | Icono | Descripción | Características |
|--------|-------|-------------|-----------------|
| **Legionario** | ⚔️ | Infantería básica | Balanceado, versátil |
| **Hastati** | 🛡️ | Infantería pesada | Alta defensa y ataque |
| **Triarii** | 🎯 | Piqueros veteranos | Bonus vs caballería, alta moral |
| **Equites** | 🐎 | Caballería | Movimiento rápido (3 casillas) |
| **Sagittarii** | 🏹 | Arqueros | Ataque a distancia (alcance 3) |

### Unidades Bárbaras 🪓

| Unidad | Descripción | Características |
|--------|-------------|-----------------|
| **Guerrero** | Infantería bárbara | Hacha, agresivo |
| **Berserker** | Infantería furiosa | Dos hachas, alto daño |
| **Lancero** | Anti-caballería | Lanza larga |
| **Jinete** | Caballería bárbara | Rápido pero menos armado |
| **Arquero** | Tiradores | Arco primitivo |

### Sistema Visual
- **Sprites únicos** detallados para cada tipo de unidad
- **Indicadores de estado** visuales:
  - 🟢 Puede actuar completamente
  - 🟡 Solo puede moverse
  - ⚫ Ya actuó este turno
  - ❗ En pánico (moral baja)
- **Barras de vida y moral** con códigos de color
- **Diferenciación clara** entre romanos (rojos/dorados) y bárbaros (verdes/marrones)

## 🚀 Instalación

### Requisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clonar el repositorio** (o descargar los archivos)
```bash
git clone https://github.com/tu-usuario/legio-romana.git
cd legio-romana
```

2. **Cambiar a la rama del juego**
```bash
git checkout game/legio-romana
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar el juego**
```bash
python main.py
```

## 🎯 Cómo Jugar

### Controles

| Tecla/Acción | Función |
|--------------|---------|
| **Click Izquierdo** | Seleccionar unidad / Mover a casilla válida |
| **Click Derecho** | Atacar enemigo en rango |
| **Espacio** | Finalizar turno |
| **F** | Cambiar formación (Línea/Testudo/Cuneus/Orbis) |
| **R** | Reiniciar batalla (cuando termina) |
| **ESC** | Volver al menú principal |

### Mecánicas de Juego

1. **Selección y Movimiento**
   - Click izquierdo en tu unidad para seleccionarla
   - Las casillas verdes muestran movimientos válidos
   - Click en una casilla verde para mover

2. **Combate**
   - Las casillas rojas muestran enemigos atacables
   - Click derecho en un enemigo para atacar
   - El daño depende del ataque vs defensa

3. **Moral**
   - Las unidades pierden moral al recibir daño
   - Moral < 30% = pánico (no puede actuar)
   - Se recupera 5% de moral por turno

4. **Formaciones**
   - **Línea**: Estándar, balanceada
   - **Testudo** (Tortuga): +Defensa, -Ataque
   - **Cuneus** (Cuña): +Ataque, -Defensa
   - **Orbis** (Círculo): +Moral, defensiva

### Estrategia

- Los **Triarii** (piqueros) son efectivos contra caballería
- La **caballería** es efectiva contra arqueros
- Los **arqueros** pueden atacar a distancia
- Mantén la **moral alta** para evitar el pánico
- Usa **formaciones** según la situación táctica

## 🏗️ Arquitectura

El juego utiliza **Domain-Driven Design (DDD)** con capas claramente separadas:

```
src/
├── domain/              # Lógica de negocio pura
│   ├── entities.py      # Unidad, Ejército, Tablero
│   ├── value_objects.py # Posición, EstadísticasUnidad
│   ├── services.py      # CalculadorCombate, CalculadorPrioridad
│   ├── events.py        # Eventos de dominio
│   ├── strategies.py    # Estrategias de IA
│   ├── factories.py     # Creación de ejércitos
│   ├── batalla.py       # Agregado raíz
│   └── exceptions.py    # Excepciones de dominio
│
├── application/         # Casos de uso y servicios
│   ├── use_cases.py     # IniciarBatalla, MoverUnidad, etc.
│   └── servicio_juego.py # Coordinador principal
│
├── presentation/        # Capa de presentación
│   ├── battle_renderer.py # Renderizado del tablero
│   └── unit_sprites.py    # Sistema de sprites detallados
│
├── states/             # Estados del juego
│   ├── menu_state.py   # Menú principal
│   └── batalla_state.py # Estado de batalla táctica
│
└── core/               # Sistema base
    └── state_manager.py # Gestión de estados
```

### Principios DDD Aplicados

- **Entidades**: Objetos con identidad (Unidad, Ejército)
- **Value Objects**: Objetos inmutables (Posición, Estadísticas)
- **Agregados**: Batalla como raíz agregada
- **Eventos de Dominio**: Comunicación desacoplada
- **Servicios de Dominio**: Lógica compleja (combate, IA)
- **Fábricas**: Creación de objetos complejos

## 🛠️ Desarrollo

### Agregar Nuevas Unidades

1. Definir tipo en `src/domain/value_objects.py`
2. Agregar estadísticas en `src/domain/factories.py`
3. Crear sprite en `src/presentation/unit_sprites.py`

### Agregar Nuevas Estrategias IA

1. Heredar de `EstrategiaIA` en `src/domain/strategies.py`
2. Implementar método `ejecutar_turno()`
3. Registrar en `src/application/use_cases.py`

## 📊 Estadísticas del Juego

- **Tablero**: 9 filas × 7 columnas = 63 casillas
- **Unidades por ejército**: 15 unidades
- **Tipos de unidades**: 5 por bando
- **Formaciones disponibles**: 4
- **Niveles de IA**: 3
- **Rango máximo de ataque**: 3 casillas (arqueros)
- **Rango máximo de movimiento**: 3 casillas (caballería)

## 🎯 Roadmap

### Próximas Características
- [ ] Sistema de campaña con múltiples batallas
- [ ] Experiencia y veteranía de unidades
- [ ] Efectos de sonido y música
- [ ] Animaciones de movimiento y combate
- [ ] Diferentes tipos de terreno
- [ ] Editor de mapas
- [ ] Modo multijugador local
- [ ] Más formaciones tácticas
- [ ] Sistema de logros

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📜 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🏆 Créditos

- **Arquitectura**: Domain-Driven Design por Eric Evans
- **Framework**: Pygame Community
- **Inspiración histórica**: Las legiones romanas y sus tácticas
- **Desarrollado con**: Claude AI Assistant

---

**¡ROMA INVICTA!** 🦅

*"Si vis pacem, para bellum" - Si quieres paz, prepárate para la guerra*