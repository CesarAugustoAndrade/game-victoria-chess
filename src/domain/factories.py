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
        ),
        TipoUnidad.VELITES: EstadisticasUnidad(
            vida_maxima=60,
            ataque=18,
            defensa=6,
            rango_movimiento=3,  # Muy móviles
            rango_ataque=2,  # Jabalinas de medio alcance
            bonus_contra_caballeria=0,
            moral=65
        ),
        TipoUnidad.PRINCEPS: EstadisticasUnidad(
            vida_maxima=130,
            ataque=28,
            defensa=14,
            rango_movimiento=2,
            rango_ataque=1,
            bonus_contra_caballeria=0,
            moral=95  # Veteranos experimentados
        ),

        # Estadísticas de unidades galas
        TipoUnidad.GUERRERO_TRIBAL: EstadisticasUnidad(
            vida_maxima=90,
            ataque=22,
            defensa=8,
            rango_movimiento=2,
            rango_ataque=1,
            bonus_contra_caballeria=0,
            moral=70  # Agresivos pero poco disciplinados
        ),
        TipoUnidad.ESPADAS_ELEGIDAS: EstadisticasUnidad(
            vida_maxima=140,
            ataque=26,
            defensa=14,
            rango_movimiento=2,
            rango_ataque=1,
            bonus_contra_caballeria=0,
            moral=90  # Élite gala
        ),
        TipoUnidad.FANATICOS_DESNUDOS: EstadisticasUnidad(
            vida_maxima=60,
            ataque=40,  # DEVASTADORES
            defensa=2,  # Sin armadura
            rango_movimiento=3,
            rango_ataque=1,
            bonus_contra_caballeria=0,
            moral=100  # Intrépidos, no sienten miedo
        ),
        TipoUnidad.ESCARAMUZADORES: EstadisticasUnidad(
            vida_maxima=55,
            ataque=20,
            defensa=4,
            rango_movimiento=3,
            rango_ataque=2,  # Hondas y jabalinas
            bonus_contra_caballeria=0,
            moral=60  # Frágiles moralmente
        ),
        TipoUnidad.CABALLERIA_BARBARA: EstadisticasUnidad(
            vida_maxima=100,
            ataque=30,
            defensa=6,
            rango_movimiento=4,  # Muy rápida
            rango_ataque=1,
            bonus_contra_caballeria=0,
            moral=75
        ),
        TipoUnidad.CABALLERIA_NOBLE: EstadisticasUnidad(
            vida_maxima=130,
            ataque=38,  # Superior a caballería romana
            defensa=12,
            rango_movimiento=3,
            rango_ataque=1,
            bonus_contra_caballeria=0,
            moral=95  # Aristocratas galos
        ),
        TipoUnidad.CARROS_GUERRA: EstadisticasUnidad(
            vida_maxima=110,
            ataque=32,
            defensa=8,
            rango_movimiento=4,  # Muy rápidos
            rango_ataque=1,
            bonus_contra_caballeria=0,
            moral=85
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
        ),
        TipoUnidad.VELITES: VisualizacionUnidad(
            nombre="Velites",
            nombre_latino="Veles",
            icono="🎯",
            color_principal=(170, 40, 40),
            color_secundario=(210, 180, 140),  # Tan (cuero)
            grito_guerra="CELER ET AUDAX!"  # Rápido y audaz
        ),
        TipoUnidad.PRINCEPS: VisualizacionUnidad(
            nombre="Princeps",
            nombre_latino="Princeps",
            icono="⚔",
            color_principal=(160, 20, 20),
            color_secundario=(218, 165, 32),   # Dorado oscuro
            grito_guerra="VIRTUS ET HONOR!"  # Virtud y honor
        )
    }

    # Visualización de unidades galas
    VISUAL_GALIA = {
        TipoUnidad.GUERRERO_TRIBAL: VisualizacionUnidad(
            nombre="Guerrero Tribal",
            nombre_latino="Galatae Bellator",
            icono="⚔",
            color_principal=(70, 120, 70),     # Verde bosque
            color_secundario=(139, 90, 43),    # Marrón cuero
            grito_guerra="GAULOIS!"
        ),
        TipoUnidad.ESPADAS_ELEGIDAS: VisualizacionUnidad(
            nombre="Espadas Elegidas",
            nombre_latino="Soldurii",
            icono="⚔",
            color_principal=(40, 80, 120),     # Azul oscuro
            color_secundario=(192, 192, 192),  # Plata
            grito_guerra="TEUTATES!"  # Dios galo de la guerra
        ),
        TipoUnidad.FANATICOS_DESNUDOS: VisualizacionUnidad(
            nombre="Fanáticos Desnudos",
            nombre_latino="Gaesatae",
            icono="🪓",
            color_principal=(180, 140, 100),   # Piel bronceada
            color_secundario=(150, 40, 40),    # Rojo guerra
            grito_guerra="MORTE AUT GLORIA!"
        ),
        TipoUnidad.ESCARAMUZADORES: VisualizacionUnidad(
            nombre="Escaramuzadores",
            nombre_latino="Funditores",
            icono="🎯",
            color_principal=(90, 100, 70),     # Verde oliva
            color_secundario=(160, 140, 100),  # Cuero claro
            grito_guerra="SAGITTA!"
        ),
        TipoUnidad.CABALLERIA_BARBARA: VisualizacionUnidad(
            nombre="Caballería Bárbara",
            nombre_latino="Equites Gallici",
            icono="🐴",
            color_principal=(100, 70, 40),     # Marrón
            color_secundario=(160, 130, 90),   # Cuero
            grito_guerra="AD VICTORIAM!"
        ),
        TipoUnidad.CABALLERIA_NOBLE: VisualizacionUnidad(
            nombre="Caballería Noble",
            nombre_latino="Equites Nobilis",
            icono="🐴",
            color_principal=(80, 40, 100),     # Púrpura noble
            color_secundario=(218, 165, 32),   # Oro
            grito_guerra="PRO PATRIA GALLIA!"
        ),
        TipoUnidad.CARROS_GUERRA: VisualizacionUnidad(
            nombre="Carros de Guerra",
            nombre_latino="Esseda",
            icono="🏇",
            color_principal=(60, 90, 120),     # Azul acero
            color_secundario=(200, 150, 100),  # Madera
            grito_guerra="BRITANNI INVICTI!"
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
        ),
        TipoUnidad.VELITES: VisualizacionUnidad(
            nombre="Hostigador",
            nombre_latino="Vexator",
            icono="🎯",
            color_principal=(70, 90, 60),
            color_secundario=(160, 140, 100),
            grito_guerra="LANZAS!"
        ),
        TipoUnidad.PRINCEPS: VisualizacionUnidad(
            nombre="Campeón",
            nombre_latino="Praelium",
            icono="⚔",
            color_principal=(90, 70, 50),
            color_secundario=(200, 180, 150),
            grito_guerra="MUERTE A ROMA!"
        )
    }

    @staticmethod
    def crear_ejercito_romano() -> Ejercito:
        """Crea el ejército romano (jugador) con formación clásica"""
        ejercito = Ejercito(Bando.ROMA)

        # Formación clásica romana: Triplex Acies (tres líneas)
        formacion = [
            # Primera línea - Velites (escaramuzadores) y Hastati (jóvenes)
            (TipoUnidad.VELITES, Posicion(6, 1)),
            (TipoUnidad.HASTATI, Posicion(6, 2)),
            (TipoUnidad.HASTATI, Posicion(6, 3)),
            (TipoUnidad.HASTATI, Posicion(6, 4)),
            (TipoUnidad.VELITES, Posicion(6, 5)),

            # Segunda línea - Princeps (veteranos)
            (TipoUnidad.PRINCEPS, Posicion(7, 2)),
            (TipoUnidad.PRINCEPS, Posicion(7, 3)),
            (TipoUnidad.PRINCEPS, Posicion(7, 4)),

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
    def crear_ejercito_galo() -> Ejercito:
        """Crea el ejército galo (enemigo) con formación agresiva celta"""
        ejercito = Ejercito(Bando.GALIA)

        # Formación gala: carga frontal con caballería en flancos
        formacion = [
            # Primera línea - Fanáticos Desnudos (carga shock)
            (TipoUnidad.FANATICOS_DESNUDOS, Posicion(2, 2)),
            (TipoUnidad.FANATICOS_DESNUDOS, Posicion(2, 3)),
            (TipoUnidad.FANATICOS_DESNUDOS, Posicion(2, 4)),

            # Segunda línea - Guerreros Tribales (masa)
            (TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 1)),
            (TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 2)),
            (TipoUnidad.ESPADAS_ELEGIDAS, Posicion(1, 3)),  # Élite en centro
            (TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 4)),
            (TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 5)),

            # Tercera línea - Espadas Elegidas (élite)
            (TipoUnidad.ESPADAS_ELEGIDAS, Posicion(0, 2)),
            (TipoUnidad.ESPADAS_ELEGIDAS, Posicion(0, 4)),

            # Flancos - Caballería (superior a romana)
            (TipoUnidad.CABALLERIA_NOBLE, Posicion(1, 0)),
            (TipoUnidad.CABALLERIA_BARBARA, Posicion(2, 0)),
            (TipoUnidad.CABALLERIA_NOBLE, Posicion(1, 6)),
            (TipoUnidad.CABALLERIA_BARBARA, Posicion(2, 6)),

            # Escaramuzadores (hostigamiento)
            (TipoUnidad.ESCARAMUZADORES, Posicion(0, 1)),
            (TipoUnidad.ESCARAMUZADORES, Posicion(0, 5))
        ]

        for idx, (tipo, posicion) in enumerate(formacion):
            unidad = FabricaEjercito._crear_unidad(
                f"galo-{idx}",
                tipo,
                Bando.GALIA,
                posicion,
                FabricaEjercito.VISUAL_GALIA[tipo]
            )
            ejercito.agregar_unidad(unidad)

        return ejercito

    @staticmethod
    def crear_ejercito_personalizado(
        bando: Bando,
        composicion: list[tuple[TipoUnidad, Posicion]]
    ) -> Ejercito:
        """Crea un ejército con composición personalizada"""
        ejercito = Ejercito(bando)

        if bando == Bando.ROMA:
            visual = FabricaEjercito.VISUAL_ROMA
        elif bando == Bando.GALIA:
            visual = FabricaEjercito.VISUAL_GALIA
        else:
            visual = FabricaEjercito.VISUAL_BARBAROS

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

    @staticmethod
    def crear_ejercito_desde_nivel(
        bando: Bando,
        configuraciones_unidades: list
    ) -> Ejercito:
        """Crea un ejército desde configuraciones de nivel"""
        from src.domain.levels import ConfiguracionUnidad

        ejercito = Ejercito(bando)

        if bando == Bando.ROMA:
            visual = FabricaEjercito.VISUAL_ROMA
        elif bando == Bando.GALIA:
            visual = FabricaEjercito.VISUAL_GALIA
        else:
            visual = FabricaEjercito.VISUAL_BARBAROS

        for idx, config in enumerate(configuraciones_unidades):
            unidad = FabricaEjercito._crear_unidad(
                f"{bando.value}-nivel-{idx}",
                config.tipo,
                bando,
                config.posicion,
                visual[config.tipo]
            )
            ejercito.agregar_unidad(unidad)

        return ejercito