# 🛡️ UNIDADES GALAS - Legio Romana

## Especificación Completa de Ejército Galo

Este documento detalla todas las unidades del ejército galo disponibles en Legio Romana, incluyendo estadísticas, características tácticas, y el pseudo-código para renderizar sus sprites.

---

## 📊 RESUMEN DE UNIDADES

| Unidad | Tipo | Vida | Ataque | Defensa | Movimiento | Rango | Moral |
|--------|------|------|--------|---------|------------|-------|-------|
| Guerrero Tribal | Infantería Básica | 90 | 22 | 8 | 2 | 1 | 70 |
| Espadas Elegidas | Infantería Pesada | 140 | 26 | 14 | 2 | 1 | 90 |
| Fanáticos Desnudos | Berserker | 60 | 40 | 2 | 3 | 1 | 100 |
| Escaramuzadores | Infantería Ligera | 55 | 20 | 4 | 3 | 2 | 60 |
| Caballería Bárbara | Caballería Ligera | 100 | 30 | 6 | 4 | 1 | 75 |
| Caballería Noble | Caballería Pesada | 130 | 38 | 12 | 3 | 1 | 95 |
| Carros de Guerra | Especial | 110 | 32 | 8 | 4 | 1 | 85 |

---

## 1. GUERRERO TRIBAL (Galatae Bellator)

### 📋 Descripción
Infantería básica gala. Guerreros con espadas largas (spatha) y escudos ovalados que forman la masa principal del ejército. Agresivos pero poco disciplinados.

### 📊 Estadísticas
```python
EstadisticasUnidad(
    vida_maxima=90,
    ataque=22,
    defensa=8,
    rango_movimiento=2,
    rango_ataque=1,
    bonus_contra_caballeria=0,
    moral=70  # Agresivos pero poco disciplinados
)
```

### 🎨 Visualización
```python
VisualizacionUnidad(
    nombre="Guerrero Tribal",
    nombre_latino="Galatae Bellator",
    icono="⚔",
    color_principal=(70, 120, 70),     # Verde bosque
    color_secundario=(139, 90, 43),    # Marrón cuero
    grito_guerra="GAULOIS!"
)
```

### 🎯 Rol Táctico
- **Línea frontal**: Absorbe daño y mantiene posición
- **Flanqueo**: Movimiento decente permite maniobras básicas
- **Apoyo**: Refuerza posiciones de élite

### 🖼️ Pseudo-código del Sprite
```pseudocode
FUNCIÓN dibujar_guerrero_tribal(superficie, centro, tamaño):
    // Colores
    DEFINIR verde_bosque = (70, 120, 70)
    DEFINIR marron_cuero = (139, 90, 43)
    DEFINIR piel = (200, 150, 100)
    DEFINIR metal = (150, 150, 150)

    // 1. CUERPO - Túnica con pantalones (braies - característico galo)
    DIBUJAR rectángulo_relleno(
        posición: (centro - 11, centro - 7),
        tamaño: (22, 18),
        color: verde_bosque
    )
    DIBUJAR rectángulo_borde(
        posición: (centro - 11, centro - 7),
        tamaño: (22, 18),
        color: marron_cuero,
        grosor: 2
    )

    // 2. PATRÓN TRIBAL en túnica (líneas diagonales)
    PARA i = 0 HASTA 2:
        DIBUJAR línea(
            inicio: (centro - 8 + i*5, centro - 5),
            fin: (centro - 5 + i*5, centro + 5),
            color: (50, 90, 50),
            grosor: 2
        )
    FIN_PARA

    // 3. ESCUDO OVALADO característico galo
    DEFINIR puntos_escudo = [
        (centro - 16, centro - 2),
        (centro - 18, centro + 5),
        (centro - 12, centro + 8),
        (centro - 10, centro + 1)
    ]
    DIBUJAR polígono_relleno(puntos_escudo, marron_cuero)
    DIBUJAR polígono_borde(puntos_escudo, verde_bosque, 2)
    // Umbo del escudo (centro metálico protector)
    DIBUJAR círculo(centro - 14, centro + 3, radio: 3, metal)

    // 4. ESPADA LARGA GALA (Spatha - más larga que gladius romana)
    DIBUJAR línea_gruesa(
        inicio: (centro + 8, centro + 8),
        fin: (centro + 17, centro - 15),
        color: metal,
        grosor: 3
    )
    // Empuñadura
    DIBUJAR línea_gruesa(
        inicio: (centro + 11, centro - 5),
        fin: (centro + 14, centro - 8),
        color: marron_cuero,
        grosor: 3
    )
    // Pomo circular
    DIBUJAR círculo(centro + 17, centro - 15, radio: 2, (100, 80, 20))

    // 5. CABEZA con características galas
    DIBUJAR círculo(centro, centro - 13, radio: 7, piel)

    // Cabello largo con trenzas (costumbre gala)
    PARA desplazamiento EN [-6, 6]:
        DIBUJAR línea(
            inicio: (centro + desplazamiento, centro - 13),
            fin: (centro + desplazamiento, centro - 5),
            color: (120, 80, 40),
            grosor: 3
        )
    FIN_PARA

    // Bigote galo prominente (muy característico)
    DIBUJAR arco(
        rectángulo: (centro - 5, centro - 13, 10, 6),
        inicio_ángulo: π,
        fin_ángulo: 2π,
        color: (120, 80, 40),
        grosor: 2
    )

    // 6. TORQUES (collar de oro - símbolo de estatus galo)
    DIBUJAR arco(
        rectángulo: (centro - 6, centro - 8, 12, 8),
        inicio_ángulo: 0,
        fin_ángulo: π,
        color: (218, 165, 32),  // Oro
        grosor: 3
    )

    // 7. PANTALONES (braies - distintivo galo vs. túnicas romanas)
    DIBUJAR línea(
        inicio: (centro - 5, centro + 10),
        fin: (centro - 5, centro + 20),
        color: verde_bosque,
        grosor: 4
    )
    DIBUJAR línea(
        inicio: (centro + 5, centro + 10),
        fin: (centro + 5, centro + 20),
        color: verde_bosque,
        grosor: 4
    )
FIN_FUNCIÓN
```

---

## 2. ESPADAS ELEGIDAS (Soldurii)

### 📋 Descripción
Infantería pesada de élite. Los mejores guerreros galos con cota de malla y espadas de calidad superior. Guardia personal de jefes tribales. Pueden enfrentarse a legionarios romanos en igualdad de condiciones.

### 📊 Estadísticas
```python
EstadisticasUnidad(
    vida_maxima=140,
    ataque=26,
    defensa=14,
    rango_movimiento=2,
    rango_ataque=1,
    bonus_contra_caballeria=0,
    moral=90  # Élite gala
)
```

### 🎨 Visualización
```python
VisualizacionUnidad(
    nombre="Espadas Elegidas",
    nombre_latino="Soldurii",
    icono="⚔",
    color_principal=(40, 80, 120),     # Azul oscuro
    color_secundario=(192, 192, 192),  # Plata (cota de malla)
    grito_guerra="TEUTATES!"  # Dios galo de la guerra
)
```

### 🎯 Rol Táctico
- **Núcleo de batalla**: Centro de formación, absorben ataques enemigos
- **Contraataque**: Alta defensa y ataque balanceado
- **Duelo de élite**: Enfrentan infantería pesada romana

### 🖼️ Pseudo-código del Sprite
```pseudocode
FUNCIÓN dibujar_espadas_elegidas(superficie, centro, tamaño):
    // Colores
    DEFINIR azul_oscuro = (40, 80, 120)
    DEFINIR plata = (192, 192, 192)
    DEFINIR oro = (218, 165, 32)

    // 1. COTA DE MALLA (lorica hamata)
    DIBUJAR rectángulo(centro - 13, centro - 9, 26, 22, plata)

    // Patrón de malla (anillos entrelazados)
    PARA i = 0 HASTA 2:
        PARA j = 0 HASTA 3:
            x = centro - 10 + j*6
            y = centro - 7 + i*6
            DIBUJAR círculo_pequeño(x, y, radio: 1, (150, 150, 150))
        FIN_PARA
    FIN_PARA

    // 2. SOBREVESTE con decoración tribal
    DIBUJAR rectángulo(centro - 11, centro - 8, 22, 18, azul_oscuro)
    DIBUJAR rectángulo_borde(centro - 11, centro - 8, 22, 18, oro, 2)

    // 3. ESCUDO GRANDE HEXAGONAL
    DEFINIR puntos_escudo = [
        (centro - 20, centro - 4),
        (centro - 18, centro - 10),
        (centro - 9, centro - 10),
        (centro - 7, centro - 4),
        (centro - 9, centro + 14),
        (centro - 18, centro + 14)
    ]
    DIBUJAR polígono(puntos_escudo, azul_oscuro)
    DIBUJAR polígono_borde(puntos_escudo, oro, 3)

    // Umbo grande elaborado
    DIBUJAR círculo(centro - 14, centro + 2, radio: 4, plata)
    DIBUJAR círculo_borde(centro - 14, centro + 2, radio: 4, oro, 2)

    // 4. ESPADA LARGA DE CALIDAD (spatha de élite)
    DIBUJAR línea(
        inicio: (centro + 10, centro + 5),
        fin: (centro + 18, centro - 14),
        color: plata,
        grosor: 4
    )
    // Empuñadura decorada con oro
    DIBUJAR rectángulo(centro + 13, centro - 6, 3, 8, oro)
    // Pomo elaborado
    DIBUJAR círculo(centro + 18, centro - 14, radio: 3, oro)

    // 5. CASCO CELTA con adornos
    DIBUJAR elipse(centro - 9, centro - 18, 18, 11, plata)
    DIBUJAR elipse_borde(centro - 9, centro - 18, 18, 11, oro, 2)

    // Cresta o penacho
    PARA i = 0 HASTA 3:
        x = centro - 4 + i*2
        DIBUJAR línea(
            inicio: (x, centro - 19),
            fin: (x, centro - 24),
            color: (150, 50, 50),  // Rojo
            grosor: 2
        )
    FIN_PARA

    // Protectores de mejillas
    DIBUJAR línea(centro - 8, centro - 13, centro - 6, centro - 8, plata, 2)
    DIBUJAR línea(centro + 8, centro - 13, centro + 6, centro - 8, plata, 2)

    // 6. PIERNAS con grebas (protección de élite)
    DIBUJAR rectángulo(centro - 6, centro + 11, 4, 11, plata)
    DIBUJAR rectángulo(centro + 2, centro + 11, 4, 11, plata)
    DIBUJAR rectángulo_borde(centro - 6, centro + 11, 4, 11, oro, 1)
    DIBUJAR rectángulo_borde(centro + 2, centro + 11, 4, 11, oro, 1)
FIN_FUNCIÓN
```

---

## 3. FANÁTICOS DESNUDOS (Gaesatae)

### 📋 Descripción
Guerreros berserker que luchan completamente desnudos para mostrar valentía absoluta. Causan terror y son devastadores en la carga inicial, pero mueren fácilmente por falta de armadura. Mercenarios de los Alpes conocidos por su ferocidad.

### 📊 Estadísticas
```python
EstadisticasUnidad(
    vida_maxima=60,              # MUY frágiles
    ataque=40,                   # ¡DEVASTADORES!
    defensa=2,                   # Sin armadura
    rango_movimiento=3,          # Rápidos en la carga
    rango_ataque=1,
    bonus_contra_caballeria=0,
    moral=100                    # Intrépidos, no sienten miedo
)
```

### 🎨 Visualización
```python
VisualizacionUnidad(
    nombre="Fanáticos Desnudos",
    nombre_latino="Gaesatae",
    icono="🪓",
    color_principal=(180, 140, 100),   # Piel bronceada
    color_secundario=(150, 40, 40),    # Rojo guerra
    grito_guerra="MORTE AUT GLORIA!"   # ¡Muerte o gloria!
)
```

### 🎯 Rol Táctico
- **Carga inicial**: Primera línea devastadora
- **Shock y temor**: Alto ataque causa pánico
- **Sacrificio**: Absorben primeros ataques antes de élite
- **Muy arriesgado**: Alta recompensa pero fácil de eliminar

### 🖼️ Pseudo-código del Sprite
```pseudocode
FUNCIÓN dibujar_fanaticos_desnudos(superficie, centro, tamaño):
    // Colores
    DEFINIR piel = (180, 140, 100)
    DEFINIR pintura_guerra = (150, 40, 40)
    DEFINIR metal = (150, 150, 150)

    // 1. CUERPO DESNUDO MUSCULOSO (sin armadura - histórico)
    DEFINIR puntos_torso = [
        (centro - 10, centro - 8),
        (centro + 10, centro - 8),
        (centro + 12, centro + 6),
        (centro - 12, centro + 6)
    ]
    DIBUJAR polígono(puntos_torso, piel)

    // 2. PINTURA DE GUERRA (espirales celtas)
    // Espiral en el pecho (símbolo celta)
    PARA radio EN [3, 5, 7]:
        DIBUJAR círculo_borde(
            centro - 4, centro - 2,
            radio: radio,
            color: pintura_guerra,
            grosor: 1
        )
    FIN_PARA

    // Líneas tribales horizontales
    DIBUJAR línea(centro - 8, centro - 5, centro + 8, centro - 5, pintura_guerra, 2)
    DIBUJAR línea(centro - 6, centro, centro + 6, centro, pintura_guerra, 2)
    DIBUJAR línea(centro - 4, centro + 4, centro + 4, centro + 4, pintura_guerra, 2)

    // 3. GRAN ESPADA DE DOS MANOS (claymore primitiva)
    DIBUJAR línea_gruesa(
        inicio: (centro + 15, centro + 10),
        fin: (centro + 22, centro - 20),
        color: metal,
        grosor: 5  // Espada grande
    )
    // Empuñadura larga para dos manos
    DIBUJAR rectángulo(centro + 17, centro - 8, 3, 12, (101, 67, 33))
    // Pomo grande
    DIBUJAR círculo(centro + 22, centro - 20, radio: 3, (100, 80, 20))

    // 4. SEGUNDA ARMA (dual wield)
    DIBUJAR línea(
        inicio: (centro - 12, centro + 8),
        fin: (centro - 18, centro - 15),
        color: metal,
        grosor: 3
    )

    // 5. CABEZA con cabello salvaje erizado
    DIBUJAR círculo(centro, centro - 14, radio: 7, piel)

    // Cabello erizado con cal (tradición gala para intimidar)
    PARA i = 0 HASTA 6:
        ángulo = (i - 3) * 0.4
        x = centro + ENTERO(6 * SEN(ángulo))
        y = centro - 14 + ENTERO(-6 * COS(ángulo))
        DIBUJAR línea(
            inicio: (centro, centro - 14),
            fin: (x, y),
            color: (220, 220, 180),  // Cabello con cal (blanco)
            grosor: 2
        )
    FIN_PARA

    // 6. OJOS FURIOSOS
    DIBUJAR círculo(centro - 2, centro - 14, radio: 2, pintura_guerra)
    DIBUJAR círculo(centro + 2, centro - 14, radio: 2, pintura_guerra)

    // 7. BOCA GRITANDO (berserker en furia)
    DIBUJAR arco(
        rectángulo: (centro - 3, centro - 12, 6, 4),
        inicio: 0,
        fin: π,
        color: pintura_guerra,
        grosor: 2
    )

    // 8. PIERNAS DESNUDAS
    DIBUJAR línea(centro - 5, centro + 6, centro - 5, centro + 20, piel, 5)
    DIBUJAR línea(centro + 5, centro + 6, centro + 5, centro + 20, piel, 5)
FIN_FUNCIÓN
```

---

## 4. ESCARAMUZADORES (Funditores)

### 📋 Descripción
Infantería ligera con hondas y jabalinas. Útiles para hostigamiento a distancia antes del combate cuerpo a cuerpo. Muy frágiles en combate directo pero móviles.

### 📊 Estadísticas
```python
EstadisticasUnidad(
    vida_maxima=55,
    ataque=20,
    defensa=4,
    rango_movimiento=3,
    rango_ataque=2,              # Hondas y jabalinas
    bonus_contra_caballeria=0,
    moral=60                     # Frágiles moralmente
)
```

### 🎨 Visualización
```python
VisualizacionUnidad(
    nombre="Escaramuzadores",
    nombre_latino="Funditores",
    icono="🎯",
    color_principal=(90, 100, 70),     # Verde oliva
    color_secundario=(160, 140, 100),  # Cuero claro
    grito_guerra="SAGITTA!"
)
```

### 🎯 Rol Táctico
- **Hostigamiento**: Ataque a distancia antes del choque
- **Movilidad**: Flanqueo rápido y reposicionamiento
- **Apoyo**: Debilita enemigos antes de carga principal
- **Evasión**: Evita combate directo

### 🖼️ Pseudo-código del Sprite
```pseudocode
FUNCIÓN dibujar_escaramuzadores(superficie, centro, tamaño):
    // Colores
    DEFINIR verde_oliva = (90, 100, 70)
    DEFINIR cuero_claro = (160, 140, 100)
    DEFINIR piel = (180, 140, 100)

    // 1. CUERPO LIGERO con ropa simple
    DIBUJAR rectángulo(centro - 9, centro - 6, 18, 15, verde_oliva)
    DIBUJAR rectángulo_borde(centro - 9, centro - 6, 18, 15, cuero_claro, 1)

    // 2. MOCHILA con piedras/jabalinas
    DEFINIR puntos_mochila = [
        (centro + 8, centro - 4),
        (centro + 12, centro - 6),
        (centro + 12, centro + 2),
        (centro + 8, centro + 4)
    ]
    DIBUJAR polígono(puntos_mochila, cuero_claro)

    // 3. HONDA EN LA MANO (característica distintiva)
    // Cuerda de la honda
    DIBUJAR arco(
        rectángulo: (centro - 20, centro - 10, 15, 20),
        inicio: -π/3,
        fin: π/3,
        color: (139, 90, 43),
        grosor: 2
    )
    // Piedra en la honda
    DIBUJAR círculo(centro - 15, centro, radio: 3, (100, 100, 100))

    // 4. JABALINAS en la espalda
    PARA i = 0 HASTA 2:
        x_offset = i * 2
        // Asta de jabalina
        DIBUJAR línea(
            inicio: (centro + 6 + x_offset, centro - 5),
            fin: (centro + 8 + x_offset, centro - 16),
            color: (101, 67, 33),
            grosor: 2
        )
        // Punta metálica
        DIBUJAR círculo(
            centro + 8 + x_offset, centro - 16,
            radio: 2,
            (120, 120, 120)
        )
    FIN_PARA

    // 5. ESCUDO PEQUEÑO de mimbre (en espalda)
    DIBUJAR círculo(centro + 10, centro + 2, radio: 5, (139, 90, 43))
    DIBUJAR círculo_borde(centro + 10, centro + 2, radio: 5, cuero_claro, 1)

    // 6. CABEZA con gorro simple
    DIBUJAR círculo(centro, centro - 12, radio: 6, piel)
    // Gorro de cuero
    DEFINIR puntos_gorro = [
        (centro - 6, centro - 11),
        (centro, centro - 15),
        (centro + 6, centro - 11)
    ]
    DIBUJAR polígono(puntos_gorro, cuero_claro)

    // 7. PIERNAS LIGERAS (corredor rápido)
    DIBUJAR línea(centro - 4, centro + 8, centro - 4, centro + 18, verde_oliva, 3)
    DIBUJAR línea(centro + 4, centro + 8, centro + 4, centro + 18, verde_oliva, 3)
FIN_FUNCIÓN
```

---

## 5. CABALLERÍA BÁRBARA (Equites Gallici)

### 📋 Descripción
Caballería ligera para escaramuzas y persecución. Muy rápida pero poco protegida. Excelente para flanqueo y ataques rápidos.

### 📊 Estadísticas
```python
EstadisticasUnidad(
    vida_maxima=100,
    ataque=30,
    defensa=6,
    rango_movimiento=4,          # Muy rápida
    rango_ataque=1,
    bonus_contra_caballeria=0,
    moral=75
)
```

### 🎨 Visualización
```python
VisualizacionUnidad(
    nombre="Caballería Bárbara",
    nombre_latino="Equites Gallici",
    icono="🐴",
    color_principal=(100, 70, 40),     # Marrón
    color_secundario=(160, 130, 90),   # Cuero
    grito_guerra="AD VICTORIAM!"
)
```

### 🎯 Rol Táctico
- **Flanqueo rápido**: Movimiento 4 permite maniobras
- **Persecución**: Elimina unidades en retirada
- **Hostigamiento**: Ataca retaguardia enemiga
- **Movilidad táctica**: Reposicionamiento rápido

### 🖼️ Pseudo-código del Sprite
```pseudocode
FUNCIÓN dibujar_caballeria_barbara(superficie, centro, tamaño):
    // Colores
    DEFINIR marron = (100, 70, 40)
    DEFINIR cuero = (160, 130, 90)
    DEFINIR caballo_oscuro = (80, 50, 30)
    DEFINIR metal = (150, 150, 150)

    // 1. CABALLO - cuerpo detallado
    DIBUJAR elipse(centro - 16, centro + 2, 32, 14, caballo_oscuro)
    DIBUJAR elipse_borde(centro - 16, centro + 2, 32, 14, (60, 40, 20), 1)

    // 2. CABEZA DEL CABALLO con detalle
    DEFINIR puntos_cabeza = [
        (centro - 18, centro + 4),
        (centro - 24, centro - 2),
        (centro - 23, centro - 6),
        (centro - 17, centro - 3)
    ]
    DIBUJAR polígono(puntos_cabeza, caballo_oscuro)

    // Ojo del caballo
    DIBUJAR círculo(centro - 20, centro - 2, radio: 2, (255, 255, 255))
    DIBUJAR círculo(centro - 20, centro - 2, radio: 1, (0, 0, 0))

    // 3. CRIN DEL CABALLO
    PARA i = 0 HASTA 4:
        x = centro - 18 + i*3
        DIBUJAR línea(
            inicio: (x, centro - 3),
            fin: (x, centro - 8),
            color: (60, 40, 20),
            grosor: 2
        )
    FIN_PARA

    // 4. PATAS DEL CABALLO (en movimiento)
    DEFINIR posiciones_patas = [
        (centro - 12, centro + 14, centro - 12, centro + 22),
        (centro - 6, centro + 14, centro - 7, centro + 20),
        (centro + 6, centro + 14, centro + 5, centro + 21),
        (centro + 12, centro + 14, centro + 12, centro + 22)
    ]
    PARA CADA (x1, y1, x2, y2) EN posiciones_patas:
        DIBUJAR línea(inicio: (x1, y1), fin: (x2, y2), caballo_oscuro, 3)
    FIN_PARA

    // 5. JINETE - cuerpo con ropa ligera
    DIBUJAR rectángulo(centro - 9, centro - 10, 18, 16, marron)
    DIBUJAR rectángulo_borde(centro - 9, centro - 10, 18, 16, cuero, 2)

    // 6. LANZA LARGA de caballería
    DIBUJAR línea(
        inicio: (centro + 8, centro - 6),
        fin: (centro + 22, centro - 22),
        color: (101, 67, 33),
        grosor: 3
    )
    // Punta de lanza brillante
    DEFINIR puntos_punta = [
        (centro + 22, centro - 24),
        (centro + 20, centro - 22),
        (centro + 24, centro - 22)
    ]
    DIBUJAR polígono(puntos_punta, metal)

    // 7. ESCUDO OVALADO en el brazo
    DIBUJAR elipse(centro - 16, centro - 6, 8, 14, cuero)
    DIBUJAR elipse_borde(centro - 16, centro - 6, 8, 14, marron, 2)

    // 8. CASCO SIMPLE
    DIBUJAR elipse(centro - 7, centro - 17, 14, 9, (120, 100, 80))

    // 9. COLA DEL CABALLO (en movimiento)
    DEFINIR puntos_cola = [
        (centro + 16, centro + 6),
        (centro + 24, centro + 10),
        (centro + 22, centro + 14)
    ]
    DIBUJAR líneas(puntos_cola, (60, 40, 20), grosor: 3)
FIN_FUNCIÓN
```

---

## 6. CABALLERÍA NOBLE (Equites Nobilis)

### 📋 Descripción
Caballería pesada de élite. Aristocratas galos con cota de malla y caballos de guerra. Históricamente considerados superiores a la caballería romana por su carga devastadora.

### 📊 Estadísticas
```python
EstadisticasUnidad(
    vida_maxima=130,
    ataque=38,                   # Superior a caballería romana (35)
    defensa=12,
    rango_movimiento=3,
    rango_ataque=1,
    bonus_contra_caballeria=0,
    moral=95                     # Aristocratas galos
)
```

### 🎨 Visualización
```python
VisualizacionUnidad(
    nombre="Caballería Noble",
    nombre_latino="Equites Nobilis",
    icono="🐴",
    color_principal=(80, 40, 100),     # Púrpura noble
    color_secundario=(218, 165, 32),   # Oro
    grito_guerra="PRO PATRIA GALLIA!"  # ¡Por la patria gala!
)
```

### 🎯 Rol Táctico
- **Carga devastadora**: Ataque 38 rompe líneas enemigas
- **Flanqueo de élite**: Ataca arqueros y retaguardia
- **Duelo de caballería**: Supera a Equites romanos
- **Reserva estratégica**: Alta moral mantiene lucha

### 🖼️ Pseudo-código del Sprite
```pseudocode
FUNCIÓN dibujar_caballeria_noble(superficie, centro, tamaño):
    // Colores
    DEFINIR purpura = (80, 40, 100)
    DEFINIR oro = (218, 165, 32)
    DEFINIR caballo_noble = (60, 60, 80)  // Gris oscuro
    DEFINIR plata = (192, 192, 192)

    // 1. CABALLO DE GUERRA - más grande con armadura
    DIBUJAR elipse(centro - 17, centro + 1, 34, 16, caballo_noble)
    // Armadura de caballo (bardas metálicas)
    DIBUJAR elipse_borde(centro - 17, centro + 1, 34, 16, plata, 2)

    // 2. CABEZA DEL CABALLO con armadura
    DEFINIR puntos_cabeza = [
        (centro - 19, centro + 3),
        (centro - 26, centro - 4),
        (centro - 24, centro - 8),
        (centro - 17, centro - 4)
    ]
    DIBUJAR polígono(puntos_cabeza, caballo_noble)
    DIBUJAR polígono_borde(puntos_cabeza, plata, 2)

    // Protector de cabeza (chamfron dorado)
    DIBUJAR círculo(centro - 22, centro - 4, radio: 3, oro)

    // 3. CRIN TRENZADA con decoraciones doradas
    PARA i = 0 HASTA 3:
        x = centro - 19 + i*3
        DIBUJAR línea(
            inicio: (x, centro - 4),
            fin: (x, centro - 10),
            color: (40, 40, 60),
            grosor: 3
        )
        DIBUJAR círculo(x, centro - 10, radio: 1, oro)
    FIN_PARA

    // 4. PATAS DEL CABALLO con protección
    PARA x_offset EN [-13, -7, 7, 13]:
        x = centro + x_offset
        DIBUJAR línea(x, centro + 15, x, centro + 23, caballo_noble, 4)
        DIBUJAR línea(x, centro + 15, x, centro + 19, plata, 2)
    FIN_PARA

    // 5. JINETE ARISTOCRÁTICO - armadura de cota de malla
    DIBUJAR rectángulo(centro - 10, centro - 12, 20, 18, plata)
    // Sobreveste púrpura con decoración dorada
    DIBUJAR rectángulo(centro - 8, centro - 11, 16, 16, purpura)
    DIBUJAR rectángulo_borde(centro - 8, centro - 11, 16, 16, oro, 2)

    // 6. ESPADA NOBLE LARGA
    DIBUJAR línea(
        inicio: (centro + 9, centro - 2),
        fin: (centro + 19, centro - 16),
        color: plata,
        grosor: 4
    )
    // Empuñadura decorada con oro
    DIBUJAR rectángulo(centro + 13, centro - 10, 3, 8, oro)
    // Pomo elaborado con gema
    DIBUJAR círculo(centro + 19, centro - 16, radio: 3, oro)
    DIBUJAR círculo(centro + 19, centro - 16, radio: 1, (200, 50, 50))  // Gema roja

    // 7. ESCUDO NOBLE con heráldica
    DIBUJAR elipse(centro - 18, centro - 8, 10, 18, purpura)
    DIBUJAR elipse_borde(centro - 18, centro - 8, 10, 18, oro, 3)
    // Símbolo heráldico (jabalí galo - animal sagrado)
    DIBUJAR elipse(centro - 15, centro - 2, 4, 6, oro)

    // 8. CASCO NOBLE con cresta transversal
    DIBUJAR elipse(centro - 8, centro - 20, 16, 10, plata)
    DIBUJAR elipse_borde(centro - 8, centro - 20, 16, 10, oro, 2)
    // Cresta de plumas nobles
    PARA i = 0 HASTA 4:
        x = centro - 6 + i*3
        DIBUJAR línea(
            inicio: (x, centro - 21),
            fin: (x, centro - 26),
            color: (150, 50, 50),  // Plumas rojas
            grosor: 2
        )
    FIN_PARA

    // Protectores faciales dorados
    DIBUJAR línea(centro - 7, centro - 16, centro - 5, centro - 12, oro, 2)
    DIBUJAR línea(centro + 7, centro - 16, centro + 5, centro - 12, oro, 2)

    // 9. COLA DEL CABALLO decorada
    DEFINIR puntos_cola = [
        (centro + 17, centro + 7),
        (centro + 25, centro + 11),
        (centro + 23, centro + 16)
    ]
    DIBUJAR líneas(puntos_cola, (40, 40, 60), grosor: 4)
FIN_FUNCIÓN
```

---

## 7. CARROS DE GUERRA (Esseda)

### 📋 Descripción
Carros de guerra britanos tirados por dos caballos. Utilizados para ataques rápidos y disrupción de formaciones enemigas. El conductor maneja mientras guerreros lanzan jabalinas y saltan para combatir.

### 📊 Estadísticas
```python
EstadisticasUnidad(
    vida_maxima=110,
    ataque=32,
    defensa=8,
    rango_movimiento=4,          # Muy rápidos
    rango_ataque=1,
    bonus_contra_caballeria=0,
    moral=85
)
```

### 🎨 Visualización
```python
VisualizacionUnidad(
    nombre="Carros de Guerra",
    nombre_latino="Esseda",
    icono="🏇",
    color_principal=(60, 90, 120),     # Azul acero
    color_secundario=(200, 150, 100),  # Madera
    grito_guerra="BRITANNI INVICTI!"   # ¡Britanos invictos!
)
```

### 🎯 Rol Táctico
- **Disrupción**: Rompe formaciones enemigas
- **Movilidad extrema**: Movimiento 4 para flanqueos
- **Intimidación**: Causa desorden psicológico
- **Ataque y retirada**: Golpea y se retira rápidamente

### 🖼️ Pseudo-código del Sprite
```pseudocode
FUNCIÓN dibujar_carros_guerra(superficie, centro, tamaño):
    // Colores
    DEFINIR azul_acero = (60, 90, 120)
    DEFINIR madera = (101, 67, 33)
    DEFINIR metal = (150, 150, 150)
    DEFINIR caballo = (80, 60, 40)

    // 1. RUEDAS DEL CARRO (dos visibles)
    DEFINIR rueda_izq = (centro - 10, centro + 12)
    DEFINIR rueda_der = (centro + 10, centro + 12)

    // Rueda izquierda
    DIBUJAR círculo(rueda_izq, radio: 8, madera)
    DIBUJAR círculo_borde(rueda_izq, radio: 8, metal, 2)
    // Radios de la rueda (6 radios)
    PARA ángulo EN [0, π/3, 2π/3, π, 4π/3, 5π/3]:
        x_fin = rueda_izq.x + ENTERO(7 * COS(ángulo))
        y_fin = rueda_izq.y + ENTERO(7 * SEN(ángulo))
        DIBUJAR línea(rueda_izq, (x_fin, y_fin), madera, 1)
    FIN_PARA

    // Rueda derecha (mismo proceso)
    DIBUJAR círculo(rueda_der, radio: 8, madera)
    DIBUJAR círculo_borde(rueda_der, radio: 8, metal, 2)
    PARA ángulo EN [0, π/3, 2π/3, π, 4π/3, 5π/3]:
        x_fin = rueda_der.x + ENTERO(7 * COS(ángulo))
        y_fin = rueda_der.y + ENTERO(7 * SEN(ángulo))
        DIBUJAR línea(rueda_der, (x_fin, y_fin), madera, 1)
    FIN_PARA

    // 2. PLATAFORMA DEL CARRO
    DIBUJAR rectángulo(centro - 14, centro - 2, 28, 12, madera)
    DIBUJAR rectángulo_borde(centro - 14, centro - 2, 28, 12, metal, 2)
    // Barandilla frontal
    DIBUJAR arco(
        rectángulo: (centro - 14, centro - 8, 28, 10),
        inicio: 0,
        fin: π,
        color: metal,
        grosor: 3
    )

    // 3. EJE DEL CARRO
    DIBUJAR línea(
        inicio: (centro - 12, centro + 12),
        fin: (centro + 12, centro + 12),
        color: metal,
        grosor: 4
    )

    // 4. CABALLOS (dos caballos tirando)
    // Caballo izquierdo
    DIBUJAR elipse(centro - 22, centro - 6, 14, 8, caballo)
    DIBUJAR círculo(centro - 26, centro - 8, radio: 4, caballo)  // Cabeza
    // Patas delanteras
    DIBUJAR línea(centro - 20, centro + 2, centro - 20, centro + 10, caballo, 2)
    DIBUJAR línea(centro - 24, centro + 2, centro - 24, centro + 10, caballo, 2)

    // Caballo derecho
    DIBUJAR elipse(centro + 8, centro - 6, 14, 8, caballo)
    DIBUJAR círculo(centro + 26, centro - 8, radio: 4, caballo)  // Cabeza
    // Patas delanteras
    DIBUJAR línea(centro + 20, centro + 2, centro + 20, centro + 10, caballo, 2)
    DIBUJAR línea(centro + 24, centro + 2, centro + 24, centro + 10, caballo, 2)

    // 5. RIENDAS
    DIBUJAR línea(centro - 26, centro - 8, centro - 5, centro - 4, (139, 90, 43), 1)
    DIBUJAR línea(centro + 26, centro - 8, centro + 5, centro - 4, (139, 90, 43), 1)

    // 6. GUERRERO EN EL CARRO
    DIBUJAR rectángulo(centro - 6, centro - 12, 12, 14, azul_acero)
    DIBUJAR rectángulo_borde(centro - 6, centro - 12, 12, 14, metal, 1)

    // 7. CASCO DEL GUERRERO
    DIBUJAR elipse(centro - 5, centro - 18, 10, 8, metal)

    // 8. LANZA LARGA del guerrero
    DIBUJAR línea(
        inicio: (centro + 6, centro - 8),
        fin: (centro + 18, centro - 22),
        color: madera,
        grosor: 2
    )
    // Punta de lanza
    DEFINIR puntos_punta = [
        (centro + 18, centro - 24),
        (centro + 16, centro - 22),
        (centro + 20, centro - 22)
    ]
    DIBUJAR polígono(puntos_punta, metal)

    // 9. ESCUDO en el carro
    DIBUJAR círculo(centro - 10, centro - 6, radio: 5, azul_acero)
    DIBUJAR círculo_borde(centro - 10, centro - 6, radio: 5, metal, 1)

    // 10. DECORACIONES CELTAS del carro (símbolos circulares)
    DIBUJAR círculo(centro - 8, centro + 3, radio: 2, oro)
    DIBUJAR círculo(centro + 8, centro + 3, radio: 2, oro)
FIN_FUNCIÓN
```

---

## 📈 COMPARATIVA CON UNIDADES ROMANAS

| Aspecto | Galos | Romanos |
|---------|-------|---------|
| **Estilo** | Agresivo, carga frontal | Disciplinado, formaciones |
| **Ataque** | Mayor (40 máx Fanáticos) | Moderado (35 máx Equites) |
| **Defensa** | Menor (2-14) | Mayor (8-15) |
| **Movilidad** | Superior (4 máx) | Moderada (3 máx) |
| **Moral** | Variable (60-100) | Estable (70-100) |
| **Caballería** | Superior (38 ataque) | Inferior (35 ataque) |
| **Disciplina** | Baja | Alta |
| **Rango** | Limitado (2 máx) | Mejor (3 máx Sagittarii) |

---

## 🎮 ESTRATEGIAS RECOMENDADAS

### Para Jugador Romano contra Galos:

1. **Contra Fanáticos Desnudos**: Mantén distancia, usa arqueros
2. **Contra Caballería Noble**: Usa Triarii (bonus contra caballería)
3. **Contra Carros**: Formación compacta, evita dispersión
4. **Contra Espadas Elegidas**: Usa Princeps o Hastati, igualdad táctica
5. **General**: Mantén formación, explota baja disciplina gala

### Para IA Gala:

1. **Carga agresiva** con Fanáticos Desnudos primera línea
2. **Flanqueo con caballería** en ambos lados
3. **Escaramuzadores** hostigan retaguardia romana
4. **Espadas Elegidas** mantienen centro
5. **Carros** rompen formaciones cuando surja oportunidad

---

## 🎨 PALETA DE COLORES

### Unidades Galas
- **Verde bosque**: (70, 120, 70) - Guerreros Tribales
- **Azul oscuro**: (40, 80, 120) - Espadas Elegidas
- **Piel bronceada**: (180, 140, 100) - Fanáticos Desnudos
- **Verde oliva**: (90, 100, 70) - Escaramuzadores
- **Marrón**: (100, 70, 40) - Caballería Bárbara
- **Púrpura noble**: (80, 40, 100) - Caballería Noble
- **Azul acero**: (60, 90, 120) - Carros de Guerra

### Materiales Comunes
- **Oro**: (218, 165, 32) - Torques, decoraciones nobles
- **Plata/Metal**: (150-192, 150-192, 150-192) - Armas, armaduras
- **Madera**: (101, 67, 33) - Astas, carros
- **Cuero**: (139-160, 90-140, 43-100) - Armaduras ligeras

---

## 📚 NOTAS HISTÓRICAS

1. **Torques**: Collar de oro distintivo galo, símbolo de estatus
2. **Braies**: Pantalones galos vs. túnicas romanas
3. **Gaesatae**: Mercenarios alpinos que luchaban desnudos
4. **Spatha**: Espada larga gala, adoptada luego por romanos
5. **Soldurii**: Guardia personal que juraba morir con su jefe
6. **Esseda**: Carros britanos usados por Julio César en sus campañas

---

**Documento generado con Claude Code**
**Versión: 1.0**
**Fecha: 2025-10-17**
