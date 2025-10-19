# 📊 FLUJO COMPLETO DEL SISTEMA DE CAMPAÑAS

## Resumen de Arquitectura

El sistema de campañas de Legio Romana permite múltiples campañas simultáneas con progreso independiente.

## Flujo de Estados

```
MenuState
    ├── "Continuar Campaña" → SelectorCampaniaState(es_continuar=True)
    └── "Nueva Campaña" → SelectorCampaniaState(es_continuar=False)

SelectorCampaniaState
    ├── Seleccionar Tutorial → NivelSelectorState(tipo='tutorial', cargar=es_continuar)
    └── Seleccionar César → NivelSelectorState(tipo='galia', cargar=es_continuar)

NivelSelectorState
    ├── Cargar guardado específico de campaña
    ├── Mostrar niveles desbloqueados
    └── Seleccionar nivel → BatallaState(nivel, campania)

BatallaState
    ├── Jugar batalla
    ├── Victoria → Guardar progreso automático
    └── ESC → Volver a NivelSelectorState
```

## Sistema de Guardado

### Archivos de Guardado

```
saves/
├── campaign_tutorial.json    # Progreso campaña Tutorial
└── campaign_galia.json       # Progreso campaña César en la Galia
```

### Estructura de Guardado

```json
{
  "version": "1.0",
  "last_save": "2025-10-19T15:30:00",
  "tipo_campania": "galia",  // o "tutorial"
  "nivel_actual": 2,
  "niveles_completados": [0, 1, 2],
  "progreso": 0.3333,  // 33.33%
  "estadisticas": {
    "batallas_ganadas": 3,
    "batallas_perdidas": 0,
    "unidades_galas_eliminadas": 50,
    "tiempo_total_jugado": 0,
    "uso_formaciones": 5
  }
}
```

## Flujo de Nueva Campaña

1. **MenuState**: Usuario elige "Nueva Campaña" (o "Campaña" si no hay guardados)
2. **SelectorCampaniaState**: Muestra 2 tarjetas de campaña con progreso individual
3. **Usuario selecciona campaña**: Se pasa `tipo_campania` y `es_continuar=False`
4. **NivelSelectorState**:
   - Si `es_continuar=False`: Crea nueva campaña del tipo especificado
   - Si `es_continuar=True`: Intenta cargar guardado del tipo especificado
5. **Selecciona nivel**: Solo puede elegir niveles desbloqueados
6. **BatallaState**: Inicia batalla con nivel y referencia a campaña
7. **Al ganar**:
   - Marca nivel como completado
   - Registra victoria en estadísticas
   - **Guarda automáticamente** en archivo correcto

## Flujo de Continuar Campaña

1. **MenuState**: Botón "Continuar Campaña" (solo visible si hay guardados)
2. **SelectorCampaniaState**: Muestra campañas con progreso actual
   - Tutorial: Muestra % y nivel actual si hay guardado
   - César: Muestra % y nivel actual si hay guardado
3. **Usuario selecciona campaña**: Carga desde archivo específico
4. **NivelSelectorState**: Carga campaña desde JSON
5. **Continúa desde donde quedó**

## Migración de Guardados Legacy

Si existe `campaign_progress.json`:
1. SaveManager detecta archivo legacy
2. Lee el tipo_campania del archivo
3. Normaliza "cesar_galia" → "galia"
4. Copia a archivo nuevo (campaign_galia.json o campaign_tutorial.json)
5. Elimina archivo legacy

## Características del Sistema

### ✅ Ventajas

1. **Progreso Independiente**: Puedes jugar Tutorial y César simultáneamente
2. **Sin Pérdida de Datos**: Nueva campaña NO borra otros guardados
3. **Visual de Progreso**: Cada campaña muestra su % completado
4. **Migración Automática**: Guardados antiguos se convierten automáticamente
5. **Guardado Automático**: Al ganar se guarda sin intervención del usuario

### 🎮 Controles

- **Menú Principal**:
  - "Continuar Campaña": Aparece si hay algún guardado
  - "Nueva Campaña" / "Campaña": Ir al selector

- **Selector de Campañas**:
  - Click en tarjeta: Seleccionar campaña
  - ESC: Volver al menú

- **Selector de Niveles**:
  - Click en nivel desbloqueado: Jugar
  - ESC: Volver al selector de campañas

- **Batalla**:
  - ESC: Volver a selector de niveles (progreso guardado)
  - R (al terminar): Reiniciar batalla
  - A: Activar AUTO-PLAY (IA juega por ti)

## Debugging

### Ver guardados actuales
```bash
ls saves/*.json
```

### Ver contenido de guardado
```bash
cat saves/campaign_galia.json
```

### Borrar guardado específico
```bash
rm saves/campaign_tutorial.json
```

### Forzar migración
```bash
# Renombrar archivo nuevo a legacy
mv saves/campaign_galia.json saves/campaign_progress.json
# Ejecutar juego - migración automática
```

## Posibles Mejoras Futuras

1. **Botón "Reiniciar Campaña"** en selector de niveles
2. **Múltiples slots de guardado** por campaña
3. **Estadísticas detalladas** por campaña
4. **Logros/Achievements** desbloqueables
5. **Modo Nueva Partida+** con unidades mejoradas
6. **Sincronización en la nube** de guardados