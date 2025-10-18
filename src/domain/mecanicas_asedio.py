"""
Mecánicas Especiales de Asedio para la Batalla de Alesia

Sistema de doble muralla, fortificaciones y asedio histórico
"""

from dataclasses import dataclass
from typing import List, Set, Optional
from enum import Enum
from src.domain.value_objects import Posicion, Bando


class TipoMuralla(Enum):
    """Tipos de muralla en Alesia"""
    INTERIOR = "interior"  # Asedia a Vercingétorix
    EXTERIOR = "exterior"  # Contra ejército de rescate
    FORTIFICACION = "fortificacion"  # Torres y puntos fuertes


class TipoTerreno(Enum):
    """Tipos especiales de terreno de asedio"""
    MURALLA = "muralla"
    FOSO = "foso"
    TRAMPA = "trampa"  # Lilia, cippi (trampas romanas)
    TORRE = "torre"
    PUERTA = "puerta"
    NORMAL = "normal"


@dataclass
class ElementoAsedio:
    """Elemento de fortificación o asedio"""
    tipo: TipoTerreno
    posicion: Posicion
    vida: int = 100
    defensa_bonus: int = 0
    permite_paso: bool = True
    bando_controlador: Optional[Bando] = None

    @property
    def esta_destruido(self) -> bool:
        """Indica si el elemento está destruido"""
        return self.vida <= 0


@dataclass
class ZonaAsedio:
    """Zona del mapa con características especiales de asedio"""
    nombre: str
    posiciones: Set[Posicion]
    tipo_zona: str  # "muralla_interior", "muralla_exterior", "tierra_de_nadie"
    bonus_defensa: int = 0
    restringe_movimiento: bool = False


class SistemaAsedioAlesia:
    """
    Sistema especial para la Batalla de Alesia

    Características históricas:
    - Doble muralla romana (circunvalación y contravalación)
    - Fosos y trampas
    - Torres de vigilancia
    - Ataques simultáneos desde dentro y fuera
    """

    def __init__(self, filas: int = 9, columnas: int = 7):
        self.filas = filas
        self.columnas = columnas
        self.elementos_asedio: List[ElementoAsedio] = []
        self.zonas: List[ZonaAsedio] = []
        self.turnos_asedio = 0
        self.murallas_breacheadas = {"interior": False, "exterior": False}

        # Inicializar fortificaciones de Alesia
        self._construir_fortificaciones_alesia()

    def _construir_fortificaciones_alesia(self):
        """
        Construye las fortificaciones históricas de Alesia

        Layout del tablero 9x7:
        - Filas 0-2: Zona de Vercingétorix (dentro de Alesia)
        - Filas 3-4: MURALLA INTERIOR (circunvalación)
        - Filas 5-6: Posición romana (entre murallas)
        - Fila 7: MURALLA EXTERIOR (contravalación)
        - Fila 8: Ejército de rescate galo
        """

        # === MURALLA INTERIOR (Fila 4) - Asedia a Vercingétorix ===
        muralla_interior_posiciones = set()
        for col in range(self.columnas):
            pos = Posicion(4, col)
            muralla_interior_posiciones.add(pos)

            # Murallas cada 2 posiciones
            if col % 2 == 0:
                self.elementos_asedio.append(
                    ElementoAsedio(
                        tipo=TipoTerreno.MURALLA,
                        posicion=pos,
                        vida=150,
                        defensa_bonus=10,
                        permite_paso=False,
                        bando_controlador=Bando.ROMA
                    )
                )
            # Puertas fortificadas
            else:
                self.elementos_asedio.append(
                    ElementoAsedio(
                        tipo=TipoTerreno.PUERTA,
                        posicion=pos,
                        vida=100,
                        defensa_bonus=5,
                        permite_paso=True,
                        bando_controlador=Bando.ROMA
                    )
                )

        # Foso delante de muralla interior (Fila 3)
        foso_interior = set()
        for col in range(self.columnas):
            pos = Posicion(3, col)
            foso_interior.add(pos)
            self.elementos_asedio.append(
                ElementoAsedio(
                    tipo=TipoTerreno.FOSO,
                    posicion=pos,
                    vida=50,
                    defensa_bonus=0,
                    permite_paso=True,  # Pero penaliza movimiento
                    bando_controlador=Bando.ROMA
                )
            )

        # === MURALLA EXTERIOR (Fila 7) - Contra ejército de rescate ===
        muralla_exterior_posiciones = set()
        for col in range(self.columnas):
            pos = Posicion(7, col)
            muralla_exterior_posiciones.add(pos)

            if col % 2 == 0:
                self.elementos_asedio.append(
                    ElementoAsedio(
                        tipo=TipoTerreno.MURALLA,
                        posicion=pos,
                        vida=150,
                        defensa_bonus=10,
                        permite_paso=False,
                        bando_controlador=Bando.ROMA
                    )
                )
            else:
                self.elementos_asedio.append(
                    ElementoAsedio(
                        tipo=TipoTerreno.PUERTA,
                        posicion=pos,
                        vida=100,
                        defensa_bonus=5,
                        permite_paso=True,
                        bando_controlador=Bando.ROMA
                    )
                )

        # Torres de vigilancia en esquinas (visión mejorada)
        torres_posiciones = [
            Posicion(4, 0),  # Torre muralla interior izquierda
            Posicion(4, 6),  # Torre muralla interior derecha
            Posicion(7, 0),  # Torre muralla exterior izquierda
            Posicion(7, 6),  # Torre muralla exterior derecha
        ]

        for pos in torres_posiciones:
            self.elementos_asedio.append(
                ElementoAsedio(
                    tipo=TipoTerreno.TORRE,
                    posicion=pos,
                    vida=200,
                    defensa_bonus=15,
                    permite_paso=False,
                    bando_controlador=Bando.ROMA
                )
            )

        # Trampas romanas (Lilia, Cippi) en tierra de nadie
        trampas = [
            Posicion(3, 1), Posicion(3, 3), Posicion(3, 5),  # Delante muralla interior
            Posicion(8, 1), Posicion(8, 3), Posicion(8, 5),  # Delante ejército rescate
        ]

        for pos in trampas:
            self.elementos_asedio.append(
                ElementoAsedio(
                    tipo=TipoTerreno.TRAMPA,
                    posicion=pos,
                    vida=30,
                    defensa_bonus=0,
                    permite_paso=True,
                    bando_controlador=Bando.ROMA
                )
            )

        # === DEFINIR ZONAS ===
        self.zonas = [
            ZonaAsedio(
                nombre="Alesia (Interior)",
                posiciones={(Posicion(r, c) for r in range(0, 3) for c in range(self.columnas))},
                tipo_zona="alesia_interior",
                bonus_defensa=5,
                restringe_movimiento=False
            ),
            ZonaAsedio(
                nombre="Muralla Interior",
                posiciones=muralla_interior_posiciones,
                tipo_zona="muralla_interior",
                bonus_defensa=10,
                restringe_movimiento=True
            ),
            ZonaAsedio(
                nombre="Campamento Romano",
                posiciones={(Posicion(r, c) for r in range(5, 7) for c in range(self.columnas))},
                tipo_zona="campamento_romano",
                bonus_defensa=0,
                restringe_movimiento=False
            ),
            ZonaAsedio(
                nombre="Muralla Exterior",
                posiciones=muralla_exterior_posiciones,
                tipo_zona="muralla_exterior",
                bonus_defensa=10,
                restringe_movimiento=True
            ),
            ZonaAsedio(
                nombre="Ejército de Rescate",
                posiciones={(Posicion(8, c) for c in range(self.columnas))},
                tipo_zona="ejercito_rescate",
                bonus_defensa=0,
                restringe_movimiento=False
            ),
        ]

    def obtener_elemento_en_posicion(self, posicion: Posicion) -> Optional[ElementoAsedio]:
        """Obtiene elemento de asedio en una posición"""
        for elemento in self.elementos_asedio:
            if elemento.posicion == posicion and not elemento.esta_destruido:
                return elemento
        return None

    def puede_moverse_a(self, posicion: Posicion, bando: Bando) -> bool:
        """
        Verifica si una unidad puede moverse a una posición

        Args:
            posicion: Posición destino
            bando: Bando que intenta moverse

        Returns:
            True si el movimiento es válido
        """
        elemento = self.obtener_elemento_en_posicion(posicion)

        if elemento is None:
            return True

        # Murallas bloquean movimiento
        if elemento.tipo == TipoTerreno.MURALLA:
            return False

        # Torres bloquean movimiento
        if elemento.tipo == TipoTerreno.TORRE:
            return False

        # Puertas permiten paso pero dan bonus defensivo al controlador
        if elemento.tipo == TipoTerreno.PUERTA:
            return elemento.permite_paso

        # Fosos y trampas permiten paso pero causan daño/penalización
        return True

    def obtener_bonus_defensa(self, posicion: Posicion, bando: Bando) -> int:
        """
        Obtiene bonus de defensa por estar en una posición fortificada

        Args:
            posicion: Posición de la unidad
            bando: Bando de la unidad

        Returns:
            Bonus de defensa
        """
        bonus_total = 0

        # Bonus del elemento de asedio
        elemento = self.obtener_elemento_en_posicion(posicion)
        if elemento and elemento.bando_controlador == bando:
            bonus_total += elemento.defensa_bonus

        # Bonus de zona
        for zona in self.zonas:
            if posicion in zona.posiciones:
                if (zona.tipo_zona in ["muralla_interior", "muralla_exterior", "campamento_romano"]
                        and bando == Bando.ROMA):
                    bonus_total += zona.bonus_defensa
                elif zona.tipo_zona == "alesia_interior" and bando == Bando.GALIA:
                    bonus_total += zona.bonus_defensa

        return bonus_total

    def recibir_danio_estructura(self, posicion: Posicion, danio: int) -> Optional[str]:
        """
        Una estructura recibe daño (por arietes, asalto, etc.)

        Args:
            posicion: Posición de la estructura
            danio: Daño infligido

        Returns:
            Mensaje describiendo el resultado
        """
        elemento = self.obtener_elemento_en_posicion(posicion)

        if elemento is None:
            return None

        elemento.vida -= danio

        if elemento.esta_destruido:
            # Marcar muralla como breacheada
            if elemento.tipo == TipoTerreno.MURALLA:
                if posicion.fila == 4:
                    self.murallas_breacheadas["interior"] = True
                    return f"¡BRECHA EN MURALLA INTERIOR! Los galos pueden pasar"
                elif posicion.fila == 7:
                    self.murallas_breacheadas["exterior"] = True
                    return f"¡BRECHA EN MURALLA EXTERIOR! El ejército de rescate avanza"

            return f"{elemento.tipo.value.upper()} destruido en {posicion}"

        return f"{elemento.tipo.value.upper()} dañado ({elemento.vida} HP restantes)"

    def aplicar_efecto_trampa(self, posicion: Posicion) -> Optional[int]:
        """
        Aplica efecto de trampa si la unidad entra en una

        Args:
            posicion: Posición donde entró la unidad

        Returns:
            Daño causado por la trampa (None si no hay trampa)
        """
        elemento = self.obtener_elemento_en_posicion(posicion)

        if elemento and elemento.tipo == TipoTerreno.TRAMPA:
            danio = 20  # Daño fijo de trampas
            elemento.vida = 0  # Trampa se consume
            return danio

        # Fosos causan penalización menor
        if elemento and elemento.tipo == TipoTerreno.FOSO:
            return 5

        return None

    def obtener_estado_murallas(self) -> dict:
        """Obtiene el estado de las murallas"""
        return {
            "muralla_interior_breacheada": self.murallas_breacheadas["interior"],
            "muralla_exterior_breacheada": self.murallas_breacheadas["exterior"],
            "turnos_asedio": self.turnos_asedio
        }

    def avanzar_turno(self):
        """Avanza el turno del asedio"""
        self.turnos_asedio += 1

    def verificar_condicion_victoria_alesia(
        self,
        unidades_galia_alesia: int,
        unidades_galia_rescate: int,
        unidades_romanas: int
    ) -> Optional[str]:
        """
        Verifica condiciones especiales de victoria en Alesia

        Args:
            unidades_galia_alesia: Unidades galas dentro de Alesia
            unidades_galia_rescate: Unidades del ejército de rescate
            unidades_romanas: Unidades romanas

        Returns:
            "ROMA" si Roma gana, "GALIA" si Galia gana, None si continúa
        """

        # Victoria romana: Eliminar AMBOS ejércitos galos
        if unidades_galia_alesia == 0 and unidades_galia_rescate == 0:
            return "ROMA"

        # Derrota romana: Quedar sin unidades
        if unidades_romanas == 0:
            return "GALIA"

        # Derrota romana: Ambas murallas breacheadas y superioridad gala
        if (self.murallas_breacheadas["interior"] and
                self.murallas_breacheadas["exterior"] and
                (unidades_galia_alesia + unidades_galia_rescate) > unidades_romanas * 1.5):
            return "GALIA"

        # Asedio muy largo favorece a los galos (moral romana baja)
        if self.turnos_asedio > 30:
            if (unidades_galia_alesia + unidades_galia_rescate) > unidades_romanas:
                return "GALIA"

        return None


class VisualizadorAsedio:
    """Renderiza elementos de asedio en el battlefield"""

    COLORES = {
        TipoTerreno.MURALLA: (100, 100, 100),      # Gris piedra
        TipoTerreno.FOSO: (101, 67, 33),           # Marrón tierra
        TipoTerreno.TRAMPA: (139, 69, 19),         # Marrón oscuro
        TipoTerreno.TORRE: (150, 150, 150),        # Gris claro
        TipoTerreno.PUERTA: (160, 82, 45),         # Madera
    }

    @staticmethod
    def obtener_color_elemento(elemento: ElementoAsedio) -> tuple:
        """Obtiene color para renderizar un elemento"""
        color_base = VisualizadorAsedio.COLORES.get(
            elemento.tipo,
            (200, 200, 200)
        )

        # Oscurecer si está dañado
        if elemento.vida < 50:
            return tuple(int(c * 0.5) for c in color_base)
        elif elemento.vida < 100:
            return tuple(int(c * 0.75) for c in color_base)

        return color_base

    @staticmethod
    def obtener_simbolo_elemento(elemento: ElementoAsedio) -> str:
        """Obtiene símbolo textual para un elemento"""
        simbolos = {
            TipoTerreno.MURALLA: "▓",
            TipoTerreno.FOSO: "≈",
            TipoTerreno.TRAMPA: "✕",
            TipoTerreno.TORRE: "♜",
            TipoTerreno.PUERTA: "▒",
        }
        return simbolos.get(elemento.tipo, "?")
