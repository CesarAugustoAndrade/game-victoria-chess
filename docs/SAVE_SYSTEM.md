# Sistema de Guardado de Progreso - Legio Romana

## 📋 Descripción

El juego Legio Romana ahora incluye un sistema completo de guardado automático que permite a los jugadores mantener su progreso entre sesiones.

## ✨ Características

### Auto-Guardado
- **Guardado automático** al completar cada nivel
- **Guardado al finalizar batalla** (victoria o derrota)
- No requiere intervención del jugador

### Persistencia de Datos
- Niveles completados
- Nivel actual
- Progreso de campaña (porcentaje)
- Estadísticas del jugador:
  - Batallas ganadas
  - Batallas perdidas
  - Unidades eliminadas
  - Tiempo total jugado (preparado para futuras actualizaciones)

## 🎮 Experiencia del Usuario

### Primera Vez (Sin Guardado)
1. Usuario inicia el juego
2. Menú muestra: **"Campaña"**
3. Comienza desde el Nivel 1
4. Al completar nivel → **Guardado automático**

### Sesiones Posteriores (Con Guardado)
1. Usuario inicia el juego
2. Menú muestra dos opciones:
   - **"Continuar Campaña"** - Carga progreso guardado
   - **"Nueva Campaña"** - Reinicia desde cero (elimina guardado anterior)
3. Selector de niveles muestra progreso con niveles desbloqueados
4. Puede continuar desde donde lo dejó

### Reiniciar Campaña
- Seleccionar **"Nueva Campaña"** desde el menú
- El guardado anterior se elimina automáticamente
- Comienza nueva campaña desde Nivel 1

## 📁 Estructura de Archivos

### Archivo de Guardado
```
saves/campaign_progress.json
```

### Formato JSON
```json
{
  "version": "1.0",
  "last_save": "2025-10-17T10:30:00",
  "nivel_actual": 3,
  "niveles_completados": [0, 1, 2],
  "progreso": 0.33,
  "estadisticas": {
    "batallas_ganadas": 3,
    "batallas_perdidas": 1,
    "unidades_eliminadas": 45,
    "tiempo_total_jugado": 0
  }
}
```

## 🔧 Arquitectura Técnica

### Componentes Principales

#### 1. SaveManager (`src/utils/save_manager.py`)
Gestor central del sistema de guardado:
- `save_campaign(data)` - Guarda progreso
- `load_campaign()` - Carga progreso
- `delete_save()` - Elimina guardado
- `save_exists()` - Verifica existencia
- `get_save_info()` - Info rápida del guardado

#### 2. CampaniaNiveles (`src/domain/levels.py`)
Sistema de serialización:
- `to_dict()` - Convierte campaña a diccionario
- `from_dict(data)` - Crea campaña desde diccionario
- `registrar_victoria()` - Actualiza estadísticas
- `registrar_derrota()` - Actualiza estadísticas

#### 3. BatallaState (`src/states/batalla_state.py`)
Auto-guardado al completar batalla:
- Guarda al ganar nivel de campaña
- Guarda estadísticas al perder
- Método `_guardar_progreso()`

#### 4. NivelSelectorState (`src/states/nivel_selector_state.py`)
Carga progreso al iniciar:
- Parámetro `cargar_guardado=True`
- Carga desde SaveManager
- Muestra niveles desbloqueados

#### 5. MenuState (`src/states/menu_state.py`)
UI adaptativa:
- Detecta guardado existente
- Muestra "Continuar" si existe guardado
- Opción "Nueva Campaña" elimina guardado

## 🚀 Flujo de Guardado

### Al Completar Nivel
```
Victoria en BatallaState
  ↓
campania.niveles_completados.add()
  ↓
campania.registrar_victoria()
  ↓
_guardar_progreso()
  ↓
save_manager.save_campaign(campania.to_dict())
  ↓
Archivo JSON creado/actualizado
```

### Al Cargar Progreso
```
MenuState detecta guardado
  ↓
Usuario selecciona "Continuar Campaña"
  ↓
NivelSelectorState(cargar_guardado=True)
  ↓
save_manager.load_campaign()
  ↓
CampaniaNiveles.from_dict(data)
  ↓
Campaña restaurada con progreso
```

## 📊 Estadísticas Rastreadas

### Implementadas
- ✅ Batallas ganadas
- ✅ Batallas perdidas
- ✅ Niveles completados
- ✅ Progreso de campaña (%)

### Preparadas para Futuro
- 📋 Tiempo total jugado
- 📋 Mejor puntuación por nivel
- 📋 Achievements/Logros
- 📋 Unidades favoritas usadas

## 🔐 Seguridad y Validación

- Validación de versión en JSON
- Manejo de errores en carga/guardado
- Backup automático (futuro)
- Detección de corrupción de archivo

## 🎯 Mejoras Futuras

### Fase 2 - Múltiples Slots
- 3 slots de guardado simultáneos
- Selector de slot en menú
- Comparación de progreso

### Fase 3 - Cloud Save
- Sincronización en la nube
- Backup automático
- Recuperación de progreso

### Fase 4 - Logros
- Sistema de achievements
- Desbloqueos especiales
- Tabla de clasificación

## 🐛 Troubleshooting

### El guardado no se carga
1. Verificar existencia: `saves/campaign_progress.json`
2. Validar formato JSON
3. Revisar logs en consola: `[SAVE]` y `[SELECTOR]`

### El progreso se pierde
1. Verificar permisos de escritura en carpeta `saves/`
2. Revisar logs de error: `[ERROR]`
3. Verificar que se llama `_guardar_progreso()` al completar nivel

### Nueva campaña no reinicia
1. Verificar que se elimina guardado en `new_campaign()`
2. Comprobar logs: `[MENU] Guardado anterior eliminado`

## 📝 Notas de Desarrollo

- El sistema usa JSON para legibilidad y debugging
- Formato extensible para futuras características
- Compatible con sistema de niveles existente
- No rompe compatibilidad con batallas rápidas (sin guardado)
