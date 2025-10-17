"""
Value Objects para el dominio de Legio Romana
"""

from dataclasses import dataclass
from enum import Enum


class TipoUnidad(Enum):
    """Tipos de unidades militares romanas"""
    LEGIONARIO = "legionario"          # Infantería básica
    HASTATI = "hastati"                # Infantería pesada
    TRIARII = "triarii"                # Piqueros veteranos
    EQUITES = "equites"                # Caballería
    SAGITTARII = "sagittarii"          # Arqueros
    VELITES = "velites"                # Infantería ligera con jabalinas
    PRINCEPS = "princeps"              # Infantería veterana


class Bando(Enum):
    """Identificación de bandos en batalla"""
    ROMA = "roma"           # Jugador
    BARBAROS = "barbaros"   # Enemigo


class EstadoJuego(Enum):
    """Estados posibles del juego"""
    MENU = "menu"
    BATALLA = "battle"
    VICTORIA = "victory"
    DERROTA = "defeat"


class TurnoActual(Enum):
    """Identificación de turno activo"""
    JUGADOR = "player"
    ENEMIGO = "enemy"


@dataclass(frozen=True)
class Posicion:
    """Objeto de valor que representa coordenadas en el tablero"""
    fila: int
    columna: int

    def distancia_manhattan(self, otra: 'Posicion') -> int:
        """Calcula distancia Manhattan entre dos posiciones"""
        return abs(self.fila - otra.fila) + abs(self.columna - otra.columna)

    def esta_adyacente(self, otra: 'Posicion') -> bool:
        """Verifica si dos posiciones son adyacentes"""
        return self.distancia_manhattan(otra) == 1

    def esta_dentro_del_tablero(self, max_filas: int = 9, max_columnas: int = 7) -> bool:
        """Valida que la posición esté dentro del tablero"""
        return 0 <= self.fila < max_filas and 0 <= self.columna < max_columnas

    def obtener_adyacentes(self) -> list['Posicion']:
        """Obtiene todas las posiciones adyacentes"""
        adyacentes = []
        for df, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nueva = Posicion(self.fila + df, self.columna + dc)
            if nueva.esta_dentro_del_tablero():
                adyacentes.append(nueva)
        return adyacentes

    def __hash__(self):
        return hash((self.fila, self.columna))

    def __eq__(self, other):
        if not isinstance(other, Posicion):
            return False
        return self.fila == other.fila and self.columna == other.columna


@dataclass(frozen=True)
class EstadisticasUnidad:
    """Objeto de valor con las estadísticas base de una unidad"""
    vida_maxima: int
    ataque: int
    defensa: int
    rango_movimiento: int
    rango_ataque: int
    bonus_contra_caballeria: int = 0
    moral: int = 100  # Nueva estadística romana

    def calcular_danio_base(self, defensa_objetivo: int) -> int:
        """Calcula el daño base considerando defensa del objetivo"""
        return max(1, self.ataque - (defensa_objetivo // 2))


@dataclass(frozen=True)
class VisualizacionUnidad:
    """Objeto de valor para propiedades visuales de unidades"""
    nombre: str
    nombre_latino: str  # Nombre en latín
    icono: str
    color_principal: tuple  # RGB
    color_secundario: tuple  # RGB
    grito_guerra: str  # Grito de batalla en latín


@dataclass(frozen=True)
class ResultadoAtaque:
    """Objeto de valor con el resultado de un ataque"""
    atacante_id: str
    defensor_id: str
    danio_infligido: int
    objetivo_eliminado: bool
    moral_perdida: int = 0  # Pérdida de moral