# 🔧 Solución: Error AttributeError 'seleccionar_nivel'

## ❌ Error Encontrado

```python
AttributeError: 'CampaniaCesarGalia' object has no attribute 'seleccionar_nivel'
```

### Causa del Error

La clase `CampaniaCesarGalia` no implementaba el método `seleccionar_nivel()` que sí tiene la clase `CampaniaNiveles`. El `NivelSelectorState` espera que ambas clases de campaña tengan la misma interfaz para poder trabajar con ellas de forma intercambiable.

---

## ✅ Solución Aplicada

### Archivo: `src/domain/campania_galia.py`

Se añadieron los siguientes métodos a la clase `CampaniaCesarGalia` para hacerla completamente compatible con `CampaniaNiveles`:

#### 1. **`seleccionar_nivel(numero_nivel: int) -> bool`**

Selecciona un nivel específico si está desbloqueado.

```python
def seleccionar_nivel(self, numero_nivel: int) -> bool:
    """
    Selecciona un nivel específico si está desbloqueado

    Args:
        numero_nivel: Número del nivel (1-9)

    Returns:
        True si se pudo seleccionar, False si está bloqueado
    """
    # Convertir de número (1-9) a índice (0-8)
    indice = numero_nivel - 1

    # Verificar que el nivel existe
    if indice < 0 or indice >= len(self.niveles):
        return False

    # Primer nivel siempre está desbloqueado
    if indice == 0:
        self.nivel_actual = indice
        return True

    # Resto requiere haber completado el anterior
    if (indice - 1) in self.niveles_completados:
        self.nivel_actual = indice
        return True

    return False
```

**Lógica:**
- Convierte número de nivel (1-9) a índice de array (0-8)
- Nivel 1 siempre desbloqueado
- Niveles 2-9 requieren completar el anterior
- Retorna `True` si se seleccionó correctamente, `False` si está bloqueado

---

#### 2. **`reiniciar_campania()`**

Reinicia el progreso de la campaña.

```python
def reiniciar_campania(self):
    """Reinicia la campaña desde el principio"""
    self.nivel_actual = 0
    self.niveles_completados.clear()
```

---

#### 3. **`registrar_victoria()`**

Registra una victoria en estadísticas.

```python
def registrar_victoria(self):
    """Registra una victoria en las estadísticas"""
    self.estadisticas["batallas_ganadas"] += 1
```

---

#### 4. **`registrar_derrota()`**

Registra una derrota en estadísticas.

```python
def registrar_derrota(self):
    """Registra una derrota en las estadísticas"""
    self.estadisticas["batallas_perdidas"] += 1
```

---

#### 5. **`registrar_unidad_eliminada()`**

Registra una unidad eliminada (específico para galos).

```python
def registrar_unidad_eliminada(self):
    """Registra una unidad gala eliminada en las estadísticas"""
    self.estadisticas["unidades_galas_eliminadas"] += 1
```

---

## 📋 Interface Completa de Campaña

Ambas clases (`CampaniaNiveles` y `CampaniaCesarGalia`) ahora implementan la misma interfaz:

### Métodos Comunes:

| Método | Descripción | Retorno |
|--------|-------------|---------|
| `__init__()` | Constructor | - |
| `obtener_nivel(numero: int)` | Obtiene nivel por número (1-9) | `Optional[Nivel]` |
| `obtener_nivel_actual()` | Obtiene el nivel actual | `Nivel` |
| `avanzar_nivel()` | Avanza al siguiente nivel | - |
| `seleccionar_nivel(numero: int)` | ✅ Selecciona nivel si desbloqueado | `bool` |
| `reiniciar_campania()` | ✅ Reinicia progreso | - |
| `registrar_victoria()` | ✅ Registra victoria | - |
| `registrar_derrota()` | ✅ Registra derrota | - |
| `registrar_unidad_eliminada()` | ✅ Registra unidad eliminada | - |
| `to_dict()` | Serializa para guardado | `dict` |
| `from_dict(data: dict)` | Deserializa desde guardado | `CampaniaNiveles` / `CampaniaCesarGalia` |

### Propiedades Comunes:

| Propiedad | Descripción | Tipo |
|-----------|-------------|------|
| `niveles` | Lista de 9 niveles | `List[Nivel]` |
| `nivel_actual` | Índice del nivel actual (0-8) | `int` |
| `niveles_completados` | Set de índices completados | `Set[int]` |
| `estadisticas` | Diccionario de stats | `dict` |
| `progreso_campania` | Progreso (0.0 - 1.0) | `float` |

---

## 🎯 Por Qué Era Necesario

El `NivelSelectorState` usa polimorfismo para trabajar con cualquier tipo de campaña:

```python
# En nivel_selector_state.py línea 108
def seleccionar_nivel(self, numero_nivel: int):
    """Inicia el nivel seleccionado"""
    if self.campania.seleccionar_nivel(numero_nivel):  # ← REQUIERE este método
        from src.states.batalla_state import BatallaState
        nivel = self.campania.obtener_nivel_actual()
        self.game.change_state(BatallaState(self.game, nivel, self.campania))
```

Sin el método `seleccionar_nivel()`, Python lanzaba `AttributeError` al intentar llamarlo en una instancia de `CampaniaCesarGalia`.

---

## ✅ Verificación

### Antes (❌ Error):
```
CampaniaNiveles:
  ✅ seleccionar_nivel()
  ✅ reiniciar_campania()
  ✅ registrar_victoria()
  ✅ registrar_derrota()
  ✅ registrar_unidad_eliminada()

CampaniaCesarGalia:
  ❌ seleccionar_nivel()          <- FALTABA
  ❌ reiniciar_campania()          <- FALTABA
  ❌ registrar_victoria()          <- FALTABA
  ❌ registrar_derrota()           <- FALTABA
  ❌ registrar_unidad_eliminada()  <- FALTABA
```

### Ahora (✅ Funcionando):
```
CampaniaNiveles:
  ✅ seleccionar_nivel()
  ✅ reiniciar_campania()
  ✅ registrar_victoria()
  ✅ registrar_derrota()
  ✅ registrar_unidad_eliminada()

CampaniaCesarGalia:
  ✅ seleccionar_nivel()          <- AÑADIDO
  ✅ reiniciar_campania()          <- AÑADIDO
  ✅ registrar_victoria()          <- AÑADIDO
  ✅ registrar_derrota()           <- AÑADIDO
  ✅ registrar_unidad_eliminada()  <- AÑADIDO
```

---

## 🚀 Resultado

Ahora ambas campañas son **completamente intercambiables** desde el punto de vista del código. El selector de niveles puede trabajar con cualquiera de ellas sin necesidad de verificar el tipo.

### Flujo Funcional:

```
MenuState
  └─ SelectorCampaniaState
       ├─ Tutorial → NivelSelectorState(CampaniaNiveles)
       │              └─ seleccionar_nivel() ✅ FUNCIONA
       │
       └─ Galia → NivelSelectorState(CampaniaCesarGalia)
                    └─ seleccionar_nivel() ✅ FUNCIONA
```

---

## 📝 Cambios en Archivos

### Modificado:
- ✅ `src/domain/campania_galia.py` - Añadidos 5 métodos

### Sin Cambios:
- ✅ `src/domain/levels.py` - Ya tenía todos los métodos
- ✅ `src/states/nivel_selector_state.py` - No requiere cambios
- ✅ `src/states/selector_campania_state.py` - No requiere cambios

---

## 🎮 Probando

Ahora el juego debería funcionar correctamente:

```bash
python main.py
```

1. Click en **"Campaña"**
2. Selecciona **"CÉSAR EN LA GALIA"**
3. Click en **Capítulo 1: Bibracte**
4. ✅ **La batalla debería iniciar correctamente**

---

**¡Error solucionado! Ambas campañas ahora son totalmente compatibles.**

*Solución aplicada: 2025-10-18*
