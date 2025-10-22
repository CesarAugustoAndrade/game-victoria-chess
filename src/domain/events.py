"""
Eventos de dominio para Legio Romana
"""

from abc import ABC
from dataclasses import dataclass
from typing import Optional
from src.domain.value_objects import Bando, Posicion, ResultadoAtaque, TurnoActual


class EventoDominio(ABC):
    """Clase base para eventos de dominio"""
    pass


@dataclass
class EventoBatallaIniciada(EventoDominio):
    """Evento cuando inicia una batalla"""
    ronda: int
    mensaje: str = "¡ROMA INVICTA! La batalla comienza"


@dataclass
class EventoUnidadSeleccionada(EventoDominio):
    """Evento cuando se selecciona una unidad"""
    unidad_id: str
    tipo_unidad: str
    posicion: Posicion


@dataclass
class EventoUnidadMovida(EventoDominio):
    """Evento cuando una unidad se mueve"""
    unidad_id: str
    posicion_origen: Posicion
    posicion_destino: Posicion


@dataclass
class EventoAtaqueRealizado(EventoDominio):
    """Evento cuando se realiza un ataque"""
    resultado: ResultadoAtaque
    grito_guerra: Optional[str] = None


@dataclass
class EventoUnidadEliminada(EventoDominio):
    """Evento cuando una unidad es eliminada"""
    unidad_id: str
    bando: Bando
    tipo_unidad: str
    mensaje: str = ""


@dataclass
class EventoUnidadEnPanico(EventoDominio):
    """Evento cuando una unidad entra en pánico"""
    unidad_id: str
    moral_actual: int
    mensaje: str = "¡La unidad está en pánico!"


@dataclass
class EventoFormacionAplicada(EventoDominio):
    """Evento cuando se aplica una formación"""
    bando: Bando
    formacion: str
    mensaje: str = ""


@dataclass
class EventoTurnoFinalizado(EventoDominio):
    """Evento cuando finaliza un turno"""
    turno_finalizado: TurnoActual
    proximo_turno: TurnoActual
    nueva_ronda: int


@dataclass
class EventoBatallaTerminada(EventoDominio):
    """Evento cuando termina una batalla"""
    ganador: Bando
    unidades_supervivientes: int
    mensaje: str = ""


@dataclass
class EventoMoralRecuperada(EventoDominio):
    """Evento cuando se recupera moral"""
    unidad_id: str
    moral_nueva: int
    mensaje: str = "La unidad recupera moral"


@dataclass
class EventoAccionIA(EventoDominio):
    """Evento cuando la IA realiza una acción"""
    descripcion: str
    tipo_accion: str  # "mover" o "atacar"


@dataclass
class EventoMoralGeneralCambiada(EventoDominio):
    """Evento cuando cambia la moral del ejército"""
    bando: Bando
    moral_anterior: int
    moral_nueva: int
    causa: str  # "unidad_eliminada", "centro_perdido", "masacre", etc.
    mensaje: str = ""


@dataclass
class EventoAtaqueBloqueado(EventoDominio):
    """Evento cuando un ataque es completamente bloqueado"""
    atacante_id: str
    defensor_id: str
    ataque: int
    defensa: int
    mensaje: str = "¡Ataque bloqueado por la defensa!"


@dataclass
class EventoMasacreTactica(EventoDominio):
    """Evento cuando se logra una masacre táctica (3+ kills)"""
    bando_atacante: Bando
    unidades_eliminadas: int
    moral_enemiga_perdida: int
    moral_propia_ganada: int
    mensaje: str = ""

    def __post_init__(self):
        if not self.mensaje:
            self.mensaje = f"¡Masacre Táctica! {self.bando_atacante.value} elimina {self.unidades_eliminadas} unidades"