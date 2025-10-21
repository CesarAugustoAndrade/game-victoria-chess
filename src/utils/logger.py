"""
Logging configuration for Legio Romana
"""

import logging
import sys
from pathlib import Path


def configurar_logging(nivel=logging.INFO, archivo_log=None):
    """
    Configura el sistema de logging para la aplicación

    Args:
        nivel: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        archivo_log: Path opcional para guardar logs en archivo
    """
    # Crear formateador
    formato = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Obtener logger raíz
    logger = logging.getLogger()
    logger.setLevel(nivel)

    # Limpiar handlers existentes
    logger.handlers.clear()

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(nivel)
    console_handler.setFormatter(formato)
    logger.addHandler(console_handler)

    # Handler para archivo (opcional)
    if archivo_log:
        # Crear directorio de logs si no existe
        log_path = Path(archivo_log)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(archivo_log, encoding='utf-8')
        file_handler.setLevel(nivel)
        file_handler.setFormatter(formato)
        logger.addHandler(file_handler)

    return logger


def obtener_logger(nombre):
    """
    Obtiene un logger con el nombre especificado

    Args:
        nombre: Nombre del logger (típicamente __name__)

    Returns:
        Logger configurado
    """
    return logging.getLogger(nombre)


# Configurar logging por defecto al importar
configurar_logging(nivel=logging.INFO)
