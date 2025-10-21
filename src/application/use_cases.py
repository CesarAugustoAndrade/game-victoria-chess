"""
Casos de uso de la aplicación
"""

import logging
from typing import List, Tuple, Optional
from src.domain.batalla import Batalla
from src.domain.events import EventoDominio
from src.domain.factories import FabricaEjercito
from src.domain.strategies import IAAgresiva, IADefensiva, IATactica
from src.domain.entities import Tablero
from src.domain.value_objects import Posicion
from src.domain.exceptions import ExcepcionDominio

logger = logging.getLogger(__name__)


class CasoUsoIniciarBatalla:
    """Caso de uso: Iniciar una nueva batalla"""

    def ejecutar(self, dificultad: str = "normal") -> Tuple[Batalla, List[EventoDominio]]:
        """Ejecuta el caso de uso"""
        # Crear componentes
        ejercito_jugador = FabricaEjercito.crear_ejercito_romano()
        ejercito_enemigo = FabricaEjercito.crear_ejercito_barbaro()
        tablero = Tablero(9, 7)

        # Seleccionar estrategia según dificultad
        estrategias = {
            "facil": IADefensiva(),
            "normal": IAAgresiva(),
            "dificil": IATactica()
        }
        estrategia_ia = estrategias.get(dificultad, IAAgresiva())

        # Crear batalla
        batalla = Batalla(
            ejercito_jugador,
            ejercito_enemigo,
            tablero,
            estrategia_ia
        )

        # Iniciar batalla
        eventos = batalla.iniciar()

        return batalla, eventos


class CasoUsoSeleccionarUnidad:
    """Caso de uso: Seleccionar una unidad"""

    def ejecutar(self, batalla: Batalla, id_unidad: str) -> List[EventoDominio]:
        """Ejecuta el caso de uso"""
        try:
            return batalla.seleccionar_unidad(id_unidad)
        except ExcepcionDominio as e:
            logger.warning(f"Acción inválida al seleccionar unidad {id_unidad}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado seleccionando unidad {id_unidad}: {e}", exc_info=True)
            raise


class CasoUsoMoverUnidad:
    """Caso de uso: Mover una unidad"""

    def ejecutar(
        self,
        batalla: Batalla,
        fila: int,
        columna: int
    ) -> List[EventoDominio]:
        """Ejecuta el caso de uso"""
        try:
            posicion = Posicion(fila, columna)
            return batalla.mover_unidad_seleccionada(posicion)
        except ExcepcionDominio as e:
            logger.warning(f"Movimiento inválido a ({fila}, {columna}): {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado moviendo unidad a ({fila}, {columna}): {e}", exc_info=True)
            raise


class CasoUsoAtacarEnemigo:
    """Caso de uso: Atacar a un enemigo"""

    def ejecutar(
        self,
        batalla: Batalla,
        id_objetivo: str
    ) -> List[EventoDominio]:
        """Ejecuta el caso de uso"""
        try:
            return batalla.atacar_con_unidad_seleccionada(id_objetivo)
        except ExcepcionDominio as e:
            logger.warning(f"Ataque inválido a {id_objetivo}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado atacando a {id_objetivo}: {e}", exc_info=True)
            raise


class CasoUsoFinalizarTurno:
    """Caso de uso: Finalizar turno del jugador"""

    def ejecutar(self, batalla: Batalla) -> List[EventoDominio]:
        """Ejecuta el caso de uso"""
        try:
            return batalla.finalizar_turno_jugador()
        except ExcepcionDominio as e:
            logger.warning(f"No se puede finalizar turno: {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado finalizando turno: {e}", exc_info=True)
            raise


class CasoUsoAplicarFormacion:
    """Caso de uso: Aplicar una formación"""

    def ejecutar(self, batalla: Batalla, formacion: str) -> List[EventoDominio]:
        """Ejecuta el caso de uso"""
        try:
            return batalla.aplicar_formacion(formacion)
        except ExcepcionDominio as e:
            logger.warning(f"No se puede aplicar formación '{formacion}': {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado aplicando formación '{formacion}': {e}", exc_info=True)
            raise


class CasoUsoObtenerEstadoBatalla:
    """Caso de uso: Obtener estado actual de la batalla"""

    def ejecutar(self, batalla: Optional[Batalla]) -> dict:
        """Ejecuta el caso de uso"""
        if batalla is None:
            return {
                'activa': False,
                'ronda': 0,
                'turno': None,
                'terminada': True,
                'ganador': None
            }

        return {
            'activa': True,
            'ronda': batalla.ronda_actual,
            'turno': batalla.turno_actual,
            'terminada': batalla.batalla_terminada,
            'ganador': batalla.ganador,
            'unidad_seleccionada': batalla.unidad_seleccionada,
            'ejercito_jugador': batalla.ejercito_jugador,
            'ejercito_enemigo': batalla.ejercito_enemigo,
            'movimientos_validos': batalla.obtener_movimientos_validos_unidad_seleccionada(),
            'objetivos_atacables': batalla.obtener_objetivos_atacables_unidad_seleccionada()
        }