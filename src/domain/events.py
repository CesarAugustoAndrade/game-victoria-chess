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
class EventoCriticoRealizado(EventoDominio):
    """Evento cuando se realiza un golpe crítico ÉPICO"""
    atacante_id: str
    defensor_id: str
    danio_total: int
    multiplicador: float
    posicion: Posicion
    mensaje: str = "¡GOLPE CRÍTICO!"


@dataclass
class EventoKillRegistrado(EventoDominio):
    """Evento cuando una unidad elimina a otra (para Kill Feed)"""
    asesino_id: str
    victima_id: str
    asesino_tipo: str
    victima_tipo: str
    asesino_bando: Bando
    victima_bando: Bando
    fue_critico: bool
    posicion: Posicion


@dataclass
class EventoCamaraLenta(EventoDominio):
    """Evento que solicita activar cámara lenta para momento épico"""
    duracion_ms: int  # Duración en milisegundos
    motivo: str  # "critico", "kill", "ultima_unidad", etc.
    intensidad: float = 0.3  # 0.3 = 30% velocidad normal