"""
Excepciones de dominio para Legio Romana
"""


class ExcepcionDominio(Exception):
    """Excepción base para el dominio"""
    pass


class ExcepcionMovimientoInvalido(ExcepcionDominio):
    """Excepción cuando un movimiento no es válido"""
    pass


class ExcepcionAtaqueInvalido(ExcepcionDominio):
    """Excepción cuando un ataque no es válido"""
    pass


class ExcepcionAccionInvalida(ExcepcionDominio):
    """Excepción cuando una acción no es válida"""
    pass


class ExcepcionTurnoInvalido(ExcepcionDominio):
    """Excepción cuando se intenta actuar fuera de turno"""
    pass


class ExcepcionUnidadNoEncontrada(ExcepcionDominio):
    """Excepción cuando no se encuentra una unidad"""
    pass


class ExcepcionEstadoInvalido(ExcepcionDominio):
    """Excepción cuando el estado del juego es inválido"""
    pass


class ExcepcionFormacionInvalida(ExcepcionDominio):
    """Excepción cuando se intenta aplicar una formación inválida"""
    pass