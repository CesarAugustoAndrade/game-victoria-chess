"""
Center control mechanic for strategic gameplay
Armies lose morale if they don't control the center of the battlefield
"""

from typing import List, Optional, Dict
from dataclasses import dataclass

from src.domain.value_objects import Bando, Posicion
from src.domain.events import EventoDominio


@dataclass
class EventoPerdidaControlCentro(EventoDominio):
    """Event when army loses center control"""
    bando: Bando
    turnos_sin_control: int
    moral_perdida: int
    mensaje: str = ""

    def __post_init__(self):
        if not self.mensaje:
            self.mensaje = f"{self.bando.value} pierde {self.moral_perdida} moral por no controlar el centro"


@dataclass
class EventoControlCentroRecuperado(EventoDominio):
    """Event when army regains center control"""
    bando: Bando
    mensaje: str = ""

    def __post_init__(self):
        if not self.mensaje:
            self.mensaje = f"{self.bando.value} recupera el control del centro"


class ControlCentro:
    """Manages center control mechanics"""

    PENALIZACION_MORAL = 3  # Moral loss per turn without center

    def __init__(self, tablero):
        self.tablero = tablero
        self._casillas_centrales: List[Posicion] = []
        self.turnos_sin_control: Dict[Bando, int] = {
            Bando.ROMA: 0,
            Bando.BARBAROS: 0
        }
        self._definir_casillas_centrales()

    def _definir_casillas_centrales(self):
        """Define the 4 center tiles for a 9x7 board"""
        filas_centro = 4  # Center row (0-indexed, so row 4 is the middle of 9)
        columnas_centro = 3  # Center column (0-indexed, so col 3 is the middle of 7)

        self._casillas_centrales = [
            Posicion(filas_centro - 1, columnas_centro - 1),  # (3, 2)
            Posicion(filas_centro - 1, columnas_centro),      # (3, 3)
            Posicion(filas_centro, columnas_centro - 1),      # (4, 2)
            Posicion(filas_centro, columnas_centro)           # (4, 3)
        ]

    @property
    def casillas_centrales(self) -> List[Posicion]:
        """Get center tiles"""
        return self._casillas_centrales.copy()

    def verificar_control(self, bando: Bando) -> bool:
        """Check if the given side controls any center tile"""
        for casilla in self._casillas_centrales:
            unidad = self.tablero.obtener_unidad_en(casilla)
            if unidad and unidad.bando == bando:
                return True
        return False

    def obtener_bando_controlador(self) -> Optional[Bando]:
        """Get which side controls the center, or None if contested/empty"""
        bandos_en_centro = set()

        for casilla in self._casillas_centrales:
            unidad = self.tablero.obtener_unidad_en(casilla)
            if unidad:
                bandos_en_centro.add(unidad.bando)

        if len(bandos_en_centro) == 1:
            return bandos_en_centro.pop()
        return None  # Either contested or empty

    def aplicar_penalizacion(self, ejercito) -> Optional[EventoDominio]:
        """Apply morale penalty if army doesn't control center"""
        if not self.verificar_control(ejercito.bando):
            self.turnos_sin_control[ejercito.bando] += 1

            # Only apply penalty after first turn without control
            if self.turnos_sin_control[ejercito.bando] > 0:
                ejercito.perder_moral(self.PENALIZACION_MORAL)

                return EventoPerdidaControlCentro(
                    bando=ejercito.bando,
                    turnos_sin_control=self.turnos_sin_control[ejercito.bando],
                    moral_perdida=self.PENALIZACION_MORAL
                )
        else:
            # Army controls center, reset counter
            turnos_anteriores = self.turnos_sin_control[ejercito.bando]
            self.turnos_sin_control[ejercito.bando] = 0

            if turnos_anteriores > 0:
                return EventoControlCentroRecuperado(bando=ejercito.bando)

        return None

    def evaluar_control_al_final_turno(self, ejercito_jugador, ejercito_enemigo) -> List[EventoDominio]:
        """Evaluate center control at end of turn for both armies"""
        eventos = []

        # Check player army
        evento_jugador = self.aplicar_penalizacion(ejercito_jugador)
        if evento_jugador:
            eventos.append(evento_jugador)

        # Check enemy army
        evento_enemigo = self.aplicar_penalizacion(ejercito_enemigo)
        if evento_enemigo:
            eventos.append(evento_enemigo)

        return eventos

    def obtener_estadisticas_control(self) -> Dict:
        """Get statistics about center control"""
        return {
            "casillas_totales": len(self._casillas_centrales),
            "controlador_actual": self.obtener_bando_controlador(),
            "turnos_sin_control": self.turnos_sin_control.copy(),
            "casillas": self._casillas_centrales.copy()
        }

    def reiniciar(self):
        """Reset center control tracking"""
        self.turnos_sin_control = {
            Bando.ROMA: 0,
            Bando.BARBAROS: 0
        }