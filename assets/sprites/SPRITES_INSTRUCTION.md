# 🎨 CÓMO AÑADIR TUS PROPIOS SPRITES AL JUEGO

## 📁 Estructura de Carpetas

Coloca tus sprites en estas carpetas:

```
assets/sprites/
├── roman/           # 🦅 Sprites de unidades romanas
│   ├── legionario.png
│   ├── hastati.png
│   ├── triarii.png
│   ├── equites.png
│   └── sagittarii.png
│
└── barbarian/       # 🪓 Sprites de unidades bárbaras
    ├── legionario.png  # (guerrero bárbaro)
    ├── hastati.png     # (berserker)
    ├── triarii.png     # (lancero bárbaro)
    ├── equites.png     # (jinete bárbaro)
    └── sagittarii.png  # (arquero bárbaro)
```

## 🖼️ Requisitos de las Imágenes

### Formato
- **Tipo de archivo**: PNG (recomendado por transparencia)
- **También acepta**: JPG, JPEG, GIF

### Tamaño
- **Recomendado**: 64x64, 128x128 o 256x256 píxeles
- **El juego escala automáticamente** al tamaño necesario
- Mantén **proporciones cuadradas** para mejores resultados

### Diseño
- **Fondo**: Transparente (PNG con alpha channel)
- **Orientación**: Vista desde arriba o isométrica
- **Estilo**: Puede ser pixel art, realista, cartoon, etc.

## 🚀 Pasos para Añadir Sprites

### Método Rápido:
1. **Descarga o crea** tu sprite
2. **Renombra** el archivo según la unidad (ej: `legionario.png`)
3. **Coloca** en la carpeta correcta (`roman/` o `barbarian/`)
4. **Ejecuta** el juego - ¡Los sprites aparecerán automáticamente!

### Ejemplo:
```
1. Descargas un sprite de soldado romano
2. Lo guardas como: assets/sprites/roman/legionario.png
3. Ejecutas el juego
4. ¡Tu sprite aparece en el juego!
```

## 🎮 Dónde Conseguir Sprites GRATIS

### Sitios Recomendados:
1. **OpenGameArt.org**
   - Miles de sprites gratuitos
   - Busca: "roman soldier", "medieval warrior", "top-down units"

2. **Itch.io**
   - Assets gratuitos y de pago
   - Busca: "strategy game sprites", "RTS units"

3. **CraftPix.net**
   - Sprites de alta calidad (algunos gratis)

4. **Kenney.nl**
   - Assets gratuitos de alta calidad

### Búsquedas Recomendadas:
- "top down soldier sprites"
- "RTS unit sprites"
- "roman soldier pixel art"
- "medieval warrior sprites"
- "strategy game units"

## 🎨 Crear Tus Propios Sprites

### Herramientas Gratuitas:
1. **Piskel** (piskelapp.com)
   - Editor online de pixel art
   - Gratis y fácil de usar

2. **Aseprite**
   - Profesional para pixel art
   - De pago pero excelente

3. **GIMP**
   - Editor de imágenes gratuito
   - Para sprites más detallados

4. **Paint.NET**
   - Simple y efectivo
   - Gratuito para Windows

### Con IA:
1. **DALL-E 2/3**
   - Prompt: "top-down view roman soldier sprite, transparent background"

2. **Midjourney**
   - Prompt: "pixel art roman legionary, game sprite, top view"

3. **Stable Diffusion**
   - Usa modelos entrenados para pixel art

## 🔧 Tips y Trucos

### Para Mejores Resultados:
- ✅ Usa **colores distintivos** para cada bando
- ✅ Mantén un **estilo consistente** entre sprites
- ✅ Prueba con **diferentes tamaños** (64x64 es un buen inicio)
- ✅ Asegúrate de que el sprite esté **centrado** en la imagen

### Sistema de Fallback:
- Si no hay sprite personalizado, el juego usa sprites programáticos
- Puedes mezclar: algunos custom, otros programáticos
- Experimenta con diferentes combinaciones

## 📝 Nombres de Archivo Exactos

### Unidades Romanas (carpeta `roman/`):
- `legionario.png` - Infantería básica
- `hastati.png` - Infantería pesada
- `triarii.png` - Piqueros veteranos
- `equites.png` - Caballería
- `sagittarii.png` - Arqueros

### Unidades Bárbaras (carpeta `barbarian/`):
- `legionario.png` - Guerrero bárbaro
- `hastati.png` - Berserker
- `triarii.png` - Lancero
- `equites.png` - Jinete
- `sagittarii.png` - Arquero

## 🎯 Ejemplo Completo

### Quiero añadir un sprite de centurión romano:

1. **Busco** en OpenGameArt.org: "roman centurion"
2. **Descargo** un PNG de 128x128
3. **Lo renombro** a `hastati.png` (infantería pesada)
4. **Lo coloco** en `assets/sprites/roman/hastati.png`
5. **Ejecuto** el juego
6. ¡Mi centurión aparece como infantería pesada!

## ❓ Solución de Problemas

### El sprite no aparece:
- Verifica el nombre del archivo (debe ser exacto)
- Verifica la carpeta (roman/ o barbarian/)
- Verifica el formato (PNG recomendado)

### El sprite se ve mal:
- Usa imágenes cuadradas
- Evita imágenes muy pequeñas (<32x32)
- Asegúrate de que tenga fondo transparente

### Quiero más tipos de unidades:
- Modifica `src/domain/value_objects.py` para añadir nuevos tipos
- Añade las estadísticas en `src/domain/factories.py`

---

## 🎮 ¡Disfruta personalizando tu Legio Romana!

**ROMA INVICTA!** 🦅