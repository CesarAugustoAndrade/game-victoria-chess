"""
Servicio de aplicación que coordina los casos de uso
"""

import logging
from typing import List, Optional
from src.domain.batalla import Batalla
from src.domain.events import EventoDominio
from src.domain.exceptions import ExcepcionEstadoInvalido
from src.application.use_cases import (
    CasoUsoIniciarBatalla,
    CasoUsoSeleccionarUnidad,
    CasoUsoMoverUnidad,
    CasoUsoAtacarEnemigo,
    CasoUsoFinalizarTurno,
    CasoUsoAplicarFormacion,
    CasoUsoObtenerEstadoBatalla
)

logger = logging.getLogger(__name__)


class ServicioJuego:
    """Servicio de aplicación que coordina los casos de uso"""

    def __init__(self):
        self._batalla_actual: Optional[Batalla] = None
        self._caso_iniciar = CasoUsoIniciarBatalla()
        self._caso_seleccionar = CasoUsoSeleccionarUnidad()
        self._caso_mover = CasoUsoMoverUnidad()
        self._caso_atacar = CasoUsoAtacarEnemigo()
        self._caso_finalizar = CasoUsoFinalizarTurno()
        self._caso_formacion = CasoUsoAplicarFormacion()
        self._caso_estado = CasoUsoObtenerEstadoBatalla()
        self._eventos_procesados = []

    def iniciar_nueva_batalla(self, dificultad: str = "normal") -> List[EventoDominio]:
        """Inicia una nueva batalla"""
        # Validar dificultad
        dificultades_validas = ["facil", "normal", "dificil"]
        if dificultad not in dificultades_validas:
            logger.warning(f"Dificultad '{dificultad}' no válida. Usando 'normal'")
            dificultad = "normal"

        logger.info(f"Iniciando batalla con dificultad: {dificultad}")

        self._batalla_actual, eventos = self._caso_iniciar.ejecutar(dificultad)
        self._eventos_procesados.extend(eventos)
        return eventos

    def iniciar_batalla_desde_nivel(self, nivel) -> List[EventoDominio]:
        """Inicia una batalla desde un nivel de la campaña"""
        from src.domain.factories import FabricaEjercito
        from src.domain.entities import Tablero
        from src.domain.strategies import IAAgresiva
        from src.domain.value_objects import Bando, TipoUnidad

        # Crear ejército del jugador
        ejercito_jugador = FabricaEjercito.crear_ejercito_desde_nivel(
            Bando.ROMA,
            nivel.unidades_jugador
        )

        # Detectar el bando enemigo según el tipo de unidades
        # Si hay unidades galas, usar Bando.GALIA, sino usar Bando.BARBAROS
        unidades_galas = {
            TipoUnidad.GUERRERO_TRIBAL,
            TipoUnidad.ESPADAS_ELEGIDAS,
            TipoUnidad.FANATICOS_DESNUDOS,
            TipoUnidad.ESCARAMUZADORES,
            TipoUnidad.CABALLERIA_BARBARA,
            TipoUnidad.CABALLERIA_NOBLE,
            TipoUnidad.CARROS_GUERRA
        }

        # Verificar si hay al menos una unidad gala en el nivel
        tiene_unidades_galas = any(
            config.tipo in unidades_galas
            for config in nivel.unidades_enemigo
        )

        bando_enemigo = Bando.GALIA if tiene_unidades_galas else Bando.BARBAROS

        # Crear ejército enemigo con el bando correcto
        ejercito_enemigo = FabricaEjercito.crear_ejercito_desde_nivel(
            bando_enemigo,
            nivel.unidades_enemigo
        )

        # Crear tablero
        tablero = Tablero()

        # Crear batalla con estrategia IA
        estrategia_ia = IAAgresiva()
        self._batalla_actual = Batalla(
            ejercito_jugador,
            ejercito_enemigo,
            tablero,
            estrategia_ia
        )

        # Iniciar batalla
        eventos = self._batalla_actual.iniciar()
        self._eventos_procesados.extend(eventos)
        return eventos

    def seleccionar_unidad(self, id_unidad: str) -> List[EventoDominio]:
        """Selecciona una unidad"""
        self._validar_batalla_activa()
        eventos = self._caso_seleccionar.ejecutar(self._batalla_actual, id_unidad)
        self._eventos_procesados.extend(eventos)
        return eventos

    def mover_unidad(self, fila: int, columna: int) -> List[EventoDominio]:
        """Mueve la unidad seleccionada"""
        self._validar_batalla_activa()
        eventos = self._caso_mover.ejecutar(self._batalla_actual, fila, columna)
        self._eventos_procesados.extend(eventos)
        return eventos

    def atacar_enemigo(self, id_objetivo: str) -> List[EventoDominio]:
        """Ataca a un enemigo"""
        self._validar_batalla_activa()
        eventos = self._caso_atacar.ejecutar(self._batalla_actual, id_objetivo)
        self._eventos_procesados.extend(eventos)
        return eventos

    def finalizar_turno(self) -> List[EventoDominio]:
        """Finaliza el turno"""
        self._validar_batalla_activa()
        eventos = self._caso_finalizar.ejecutar(self._batalla_actual)
        self._eventos_procesados.extend(eventos)
        return eventos

    def aplicar_formacion(self, formacion: str) -> List[EventoDominio]:
        """Aplica una formación"""
        self._validar_batalla_activa()
        eventos = self._caso_formacion.ejecutar(self._batalla_actual, formacion)
        self._eventos_procesados.extend(eventos)
        return eventos

    def obtener_estado_batalla(self) -> dict:
        """Obtiene el estado actual de la batalla para la UI"""
        return self._caso_estado.ejecutar(self._batalla_actual)

    def obtener_batalla_actual(self) -> Optional[Batalla]:
        """Obtiene la batalla actual"""
        return self._batalla_actual

    def deseleccionar_unidad(self):
        """Deselecciona la unidad actual"""
        if self._batalla_actual:
            self._batalla_actual.deseleccionar_unidad()

    def reiniciar_juego(self):
        """Reinicia el juego"""
        self._batalla_actual = None
        self._eventos_procesados.clear()

    def obtener_historial_eventos(self) -> List[EventoDominio]:
        """Obtiene el historial de eventos procesados"""
        return self._eventos_procesados.copy()

    def _validar_batalla_activa(self):
        """Valida que exista una batalla activa"""
        if self._batalla_actual is None:
            raise ExcepcionEstadoInvalido("No hay batalla activa")

    def cambiar_turno_a_enemigo(self):
        """Cambia el turno a enemigo sin ejecutar IA"""
        from src.domain.value_objects import TurnoActual
        self._validar_batalla_activa()
        self._batalla_actual._turno_actual = TurnoActual.ENEMIGO
        self._batalla_actual._unidad_seleccionada = None

    def cambiar_turno_a_jugador(self):
        """Cambia el turno a jugador"""
        from src.domain.value_objects import TurnoActual
        self._validar_batalla_activa()
        # Remover unidades muertas
        self._batalla_actual._ejercito_enemigo.remover_unidades_muertas()
        self._batalla_actual._ejercito_jugador.remover_unidades_muertas()

        # Verificar si el jugador fue derrotado
        if self._batalla_actual._ejercito_jugador.esta_derrotado:
            from src.domain.value_objects import Bando
            self._batalla_actual._finalizar_batalla(Bando.BARBAROS)
        elif self._batalla_actual._ejercito_enemigo.esta_derrotado:
            from src.domain.value_objects import Bando
            self._batalla_actual._finalizar_batalla(Bando.ROMA)
        else:
            # Iniciar nuevo turno del jugador
            self._batalla_actual._iniciar_nuevo_turno_jugador()