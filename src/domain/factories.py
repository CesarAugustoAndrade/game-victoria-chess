"""
Fábricas para crear ejércitos y unidades romanas
"""

from src.domain.entities import Unidad, Ejercito
from src.domain.value_objects import (
    TipoUnidad, Bando, Posicion, EstadisticasUnidad, VisualizacionUnidad
)


class FabricaEjercito:
    """Fábrica para crear ejércitos con formaciones predefinidas"""

    # Estadísticas de unidades romanas
    STATS = {
        TipoUnidad.LEGIONARIO: EstadisticasUnidad(
            vida_maxima=100,
            ataque=20,
            defensa=10,
            rango_movimiento=2,
            rango_ataque=1,
            bonus_contra_caballeria=0,
            moral=80
        ),
        TipoUnidad.HASTATI: EstadisticasUnidad(
            vida_maxima=150,
            ataque=26,
            defensa=15,
            rango_movimiento=1,
            rango_ataque=1,
            bonus_contra_caballeria=0,
            moral=90
        ),
        TipoUnidad.TRIARII: EstadisticasUnidad(
            vida_maxima=90,
            ataque=23,
            defensa=12,
            rango_movimiento=1,
            rango_ataque=1,
            bonus_contra_caballeria=20,  # Bonus contra caballería
            moral=100  # Veteranos con alta moral
        ),
        TipoUnidad.EQUITES: EstadisticasUnidad(
            vida_maxima=120,
            ataque=35,
            defensa=8,
            rango_movimiento=3,  # Mayor movimiento
            rango_ataque=1,
            bonus_contra_caballeria=0,
            moral=85
        ),
        TipoUnidad.SAGITTARII: EstadisticasUnidad(
            vida_maxima=70,
            ataque=30,
            defensa=5,
            rango_movimiento=2,
            rango_ataque=3,  # Ataque a distancia
            bonus_contra_caballeria=0,
            moral=70
        )
    }

    # Visualización de unidades romanas
    VISUAL_ROMA = {
        TipoUnidad.LEGIONARIO: VisualizacionUnidad(
            nombre="Legionario",
            nombre_latino="Legionarius",
            icono="⚔",
            color_principal=(180, 20, 20),    # Rojo romano
            color_secundario=(255, 215, 0),    # Dorado
            grito_guerra="ROMA AETERNA!"
        ),
        TipoUnidad.HASTATI: VisualizacionUnidad(
            nombre="Hastati",
            nombre_latino="Hastatus",
            icono="🛡",
            color_principal=(150, 20, 20),
            color_secundario=(192, 192, 192),  # Plata
            grito_guerra="PRO ROMA!"
        ),
        TipoUnidad.TRIARII: VisualizacionUnidad(
            nombre="Triarii",
            nombre_latino="Triarius",
            icono="🎯",
            color_principal=(120, 20, 20),
            color_secundario=(205, 127, 50),   # Bronce
            grito_guerra="SENATUS POPULUSQUE ROMANUS!"
        ),
        TipoUnidad.EQUITES: VisualizacionUnidad(
            nombre="Equites",
            nombre_latino="Eques",
            icono="🐎",
            color_principal=(160, 30, 30),
            color_secundario=(255, 255, 255),  # Blanco
            grito_guerra="VICTORIA AUT MORS!"
        ),
        TipoUnidad.SAGITTARII: VisualizacionUnidad(
            nombre="Sagittarii",
            nombre_latino="Sagittarius",
            icono="🏹",
            color_principal=(140, 25, 25),
            color_secundario=(139, 69, 19),    # Marrón
            grito_guerra="SAGITTAE VOLANT!"
        )
    }

    # Visualización de unidades bárbaras (enemigos)
    VISUAL_BARBAROS = {
        TipoUnidad.LEGIONARIO: VisualizacionUnidad(
            nombre="Guerrero",
            nombre_latino="Barbarus",
            icono="⚔",
            color_principal=(50, 100, 50),     # Verde oscuro
            color_secundario=(139, 69, 19),    # Marrón
            grito_guerra="AAAAARGH!"
        ),
        TipoUnidad.HASTATI: VisualizacionUnidad(
            nombre="Berserker",
            nombre_latino="Furiosus",
            icono="🪓",
            color_principal=(80, 80, 80),      # Gris
            color_secundario=(200, 200, 200),
            grito_guerra="SANGRE Y MUERTE!"
        ),
        TipoUnidad.TRIARII: VisualizacionUnidad(
            nombre="Lancero",
            nombre_latino="Hastatus Barbarus",
            icono="🔱",
            color_principal=(60, 60, 120),     # Azul oscuro
            color_secundario=(180, 180, 180),
            grito_guerra="POR LA HORDA!"
        ),
        TipoUnidad.EQUITES: VisualizacionUnidad(
            nombre="Jinete",
            nombre_latino="Equus Barbarus",
            icono="🐴",
            color_principal=(100, 50, 0),      # Marrón oscuro
            color_secundario=(200, 150, 100),
            grito_guerra="CABALGAMOS!"
        ),
        TipoUnidad.SAGITTARII: VisualizacionUnidad(
            nombre="Arquero",
            nombre_latino="Arcus Barbarus",
            icono="🏹",
            color_principal=(50, 80, 50),
            color_secundario=(150, 150, 150),
            grito_guerra="FLECHAS!"
        )
    }

    @staticmethod
    def crear_ejercito_romano() -> Ejercito:
        """Crea el ejército romano (jugador) con formación clásica"""
        ejercito = Ejercito(Bando.ROMA)

        # Formación clásica romana: Triplex Acies (tres líneas)
        formacion = [
            # Primera línea - Hastati (jóvenes)
            (TipoUnidad.HASTATI, Posicion(6, 1)),
            (TipoUnidad.HASTATI, Posicion(6, 2)),
            (TipoUnidad.HASTATI, Posicion(6, 3)),
            (TipoUnidad.HASTATI, Posicion(6, 4)),
            (TipoUnidad.HASTATI, Posicion(6, 5)),

            # Segunda línea - Legionarios (veteranos)
            (TipoUnidad.LEGIONARIO, Posicion(7, 2)),
            (TipoUnidad.LEGIONARIO, Posicion(7, 3)),
            (TipoUnidad.LEGIONARIO, Posicion(7, 4)),

            # Tercera línea - Triarii (élite)
            (TipoUnidad.TRIARII, Posicion(8, 2)),
            (TipoUnidad.TRIARII, Posicion(8, 3)),
            (TipoUnidad.TRIARII, Posicion(8, 4)),

            # Flancos - Equites (caballería)
            (TipoUnidad.EQUITES, Posicion(7, 0)),
            (TipoUnidad.EQUITES, Posicion(7, 6)),

            # Retaguardia - Sagittarii (arqueros)
            (TipoUnidad.SAGITTARII, Posicion(8, 1)),
            (TipoUnidad.SAGITTARII, Posicion(8, 5))
        ]

        for idx, (tipo, posicion) in enumerate(formacion):
            unidad = FabricaEjercito._crear_unidad(
                f"roma-{idx}",
                tipo,
                Bando.ROMA,
                posicion,
                FabricaEjercito.VISUAL_ROMA[tipo]
            )
            ejercito.agregar_unidad(unidad)

        return ejercito

    @staticmethod
    def crear_ejercito_barbaro() -> Ejercito:
        """Crea el ejército bárbaro (enemigo) con formación agresiva"""
        ejercito = Ejercito(Bando.BARBAROS)

        # Formación bárbara: más agresiva y desordenada
        formacion = [
            # Línea frontal - Guerreros y Berserkers
            (TipoUnidad.LEGIONARIO, Posicion(2, 1)),
            (TipoUnidad.HASTATI, Posicion(2, 2)),
            (TipoUnidad.LEGIONARIO, Posicion(2, 3)),
            (TipoUnidad.HASTATI, Posicion(2, 4)),
            (TipoUnidad.LEGIONARIO, Posicion(2, 5)),

            # Segunda línea - Más guerreros y lanceros
            (TipoUnidad.LEGIONARIO, Posicion(1, 2)),
            (TipoUnidad.TRIARII, Posicion(1, 3)),
            (TipoUnidad.LEGIONARIO, Posicion(1, 4)),

            # Flancos - Jinetes
            (TipoUnidad.EQUITES, Posicion(1, 0)),
            (TipoUnidad.EQUITES, Posicion(1, 6)),

            # Arqueros dispersos
            (TipoUnidad.SAGITTARII, Posicion(0, 2)),
            (TipoUnidad.SAGITTARII, Posicion(0, 3)),
            (TipoUnidad.SAGITTARII, Posicion(0, 4)),

            # Reservas
            (TipoUnidad.TRIARII, Posicion(0, 1)),
            (TipoUnidad.TRIARII, Posicion(0, 5))
        ]

        for idx, (tipo, posicion) in enumerate(formacion):
            unidad = FabricaEjercito._crear_unidad(
                f"barbaro-{idx}",
                tipo,
                Bando.BARBAROS,
                posicion,
                FabricaEjercito.VISUAL_BARBAROS[tipo]
            )
            ejercito.agregar_unidad(unidad)

        return ejercito

    @staticmethod
    def _crear_unidad(
        id: str,
        tipo: TipoUnidad,
        bando: Bando,
        posicion: Posicion,
        visualizacion: VisualizacionUnidad
    ) -> Unidad:
        """Crea una unidad individual"""
        return Unidad(
            id=id,
            tipo=tipo,
            bando=bando,
            estadisticas=FabricaEjercito.STATS[tipo],
            visualizacion=visualizacion,
            posicion=posicion
        )

    @staticmethod
    def crear_ejercito_personalizado(
        bando: Bando,
        composicion: list[tuple[TipoUnidad, Posicion]]
    ) -> Ejercito:
        """Crea un ejército con composición personalizada"""
        ejercito = Ejercito(bando)

        visual = (FabricaEjercito.VISUAL_ROMA
                 if bando == Bando.ROMA
                 else FabricaEjercito.VISUAL_BARBAROS)

        for idx, (tipo, posicion) in enumerate(composicion):
            unidad = FabricaEjercito._crear_unidad(
                f"{bando.value}-custom-{idx}",
                tipo,
                bando,
                posicion,
                visual[tipo]
            )
            ejercito.agregar_unidad(unidad)

        return ejercito