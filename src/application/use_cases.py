"""
Casos de uso de la aplicación
"""

from typing import List, Tuple, Optional
from src.domain.batalla import Batalla
from src.domain.events import EventoDominio
from src.domain.factories import FabricaEjercito
from src.domain.strategies import IAAgresiva, IADefensiva, IATactica
from src.domain.entities import Tablero
from src.domain.value_objects import Posicion


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
        except Exception as e:
            print(f"Error seleccionando unidad: {e}")
            return []


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
        except Exception as e:
            print(f"Error moviendo unidad: {e}")
            return []


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
        except Exception as e:
            print(f"Error atacando: {e}")
            return []


class CasoUsoFinalizarTurno:
    """Caso de uso: Finalizar turno del jugador"""

    def ejecutar(self, batalla: Batalla) -> List[EventoDominio]:
        """Ejecuta el caso de uso"""
        try:
            return batalla.finalizar_turno_jugador()
        except Exception as e:
            print(f"Error finalizando turno: {e}")
            return []


class CasoUsoAplicarFormacion:
    """Caso de uso: Aplicar una formación"""

    def ejecutar(self, batalla: Batalla, formacion: str) -> List[EventoDominio]:
        """Ejecuta el caso de uso"""
        try:
            return batalla.aplicar_formacion(formacion)
        except Exception as e:
            print(f"Error aplicando formación: {e}")
            return []


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