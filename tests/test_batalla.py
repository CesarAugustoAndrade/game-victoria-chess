"""
Tests for Batalla aggregate root and turn-based state machine
"""

import pytest
from src.domain.batalla import Batalla
from src.domain.value_objects import TurnoActual, Bando, Posicion
from src.domain.events import (
    EventoBatallaIniciada, EventoUnidadSeleccionada,
    EventoUnidadMovida, EventoAtaqueRealizado,
    EventoBatallaTerminada, EventoTurnoFinalizado
)
from src.domain.exceptions import (
    ExcepcionTurnoInvalido, ExcepcionAccionInvalida,
    ExcepcionMovimientoInvalido, ExcepcionUnidadNoEncontrada
)


@pytest.mark.unit
@pytest.mark.turn
@pytest.mark.domain
class TestBatalla:
    """Tests for Batalla aggregate root"""

    def test_iniciar_batalla_genera_evento(self, batalla_simple):
        """Test que iniciar una batalla genera el evento correcto"""
        # batalla_simple ya está iniciada, crear una nueva
        from src.domain.entities import Ejercito, Tablero
        from src.domain.strategies import IAAgresiva

        ejercito_j = Ejercito(Bando.ROMA)
        ejercito_e = Ejercito(Bando.BARBAROS)
        tablero = Tablero()
        batalla = Batalla(ejercito_j, ejercito_e, tablero, IAAgresiva())

        eventos = batalla.iniciar()

        assert len(eventos) > 0
        assert isinstance(eventos[0], EventoBatallaIniciada)
        assert eventos[0].ronda == 1

    def test_batalla_inicia_en_turno_jugador(self, batalla_simple):
        """Test que la batalla inicia en el turno del jugador"""
        assert batalla_simple.turno_actual == TurnoActual.JUGADOR
        assert batalla_simple.ronda_actual == 1

    def test_seleccionar_unidad_jugador(self, batalla_simple):
        """Test seleccionar una unidad del jugador"""
        unidad = batalla_simple.ejercito_jugador.unidades_vivas[0]

        eventos = batalla_simple.seleccionar_unidad(unidad.id)

        assert batalla_simple.unidad_seleccionada == unidad
        assert any(isinstance(e, EventoUnidadSeleccionada) for e in eventos)

    def test_no_seleccionar_unidad_en_turno_enemigo(self, batalla_simple):
        """Test que no se puede seleccionar unidad en turno enemigo"""
        batalla_simple._turno_actual = TurnoActual.ENEMIGO
        unidad = batalla_simple.ejercito_jugador.unidades_vivas[0]

        with pytest.raises(ExcepcionTurnoInvalido):
            batalla_simple.seleccionar_unidad(unidad.id)

    def test_no_seleccionar_unidad_que_ya_actuo(self, batalla_simple):
        """Test que no se puede seleccionar unidad que ya actuó"""
        unidad = batalla_simple.ejercito_jugador.unidades_vivas[0]
        unidad.marcar_como_actuada()

        with pytest.raises(ExcepcionAccionInvalida):
            batalla_simple.seleccionar_unidad(unidad.id)

    def test_no_seleccionar_unidad_inexistente(self, batalla_simple):
        """Test que seleccionar unidad inexistente lanza excepción"""
        with pytest.raises(ExcepcionUnidadNoEncontrada):
            batalla_simple.seleccionar_unidad("unidad-inexistente")

    def test_mover_unidad_seleccionada(self, batalla_simple):
        """Test mover una unidad seleccionada"""
        unidad = batalla_simple.ejercito_jugador.unidades_vivas[0]
        batalla_simple.seleccionar_unidad(unidad.id)

        posicion_inicial = unidad.posicion
        movimientos_validos = batalla_simple.obtener_movimientos_validos_unidad_seleccionada()

        if movimientos_validos:
            nueva_posicion = movimientos_validos[0]
            eventos = batalla_simple.mover_unidad_seleccionada(nueva_posicion)

            assert unidad.posicion == nueva_posicion
            assert unidad.posicion != posicion_inicial
            assert any(isinstance(e, EventoUnidadMovida) for e in eventos)

    def test_no_mover_sin_unidad_seleccionada(self, batalla_simple):
        """Test que no se puede mover sin seleccionar unidad"""
        with pytest.raises(ExcepcionAccionInvalida):
            batalla_simple.mover_unidad_seleccionada(Posicion(4, 4))

    def test_no_mover_a_posicion_invalida(self, batalla_simple):
        """Test que no se puede mover a posición inválida"""
        unidad = batalla_simple.ejercito_jugador.unidades_vivas[0]
        batalla_simple.seleccionar_unidad(unidad.id)

        # Posición muy lejana (fuera del rango de movimiento)
        posicion_lejana = Posicion(0, 0)

        with pytest.raises(ExcepcionMovimientoInvalido):
            batalla_simple.mover_unidad_seleccionada(posicion_lejana)

    def test_atacar_con_unidad_seleccionada(self, batalla_simple):
        """Test atacar con una unidad seleccionada"""
        unidad_atacante = batalla_simple.ejercito_jugador.unidades_vivas[0]
        unidad_objetivo = batalla_simple.ejercito_enemigo.unidades_vivas[0]

        # Colocar unidades cerca para que puedan atacarse
        unidad_atacante._posicion = Posicion(3, 3)
        unidad_objetivo._posicion = Posicion(3, 4)  # Adyacente

        batalla_simple.seleccionar_unidad(unidad_atacante.id)

        vida_inicial = unidad_objetivo.vida_actual
        eventos = batalla_simple.atacar_con_unidad_seleccionada(unidad_objetivo.id)

        assert unidad_objetivo.vida_actual < vida_inicial
        assert any(isinstance(e, EventoAtaqueRealizado) for e in eventos)
        assert not unidad_atacante.puede_actuar

    def test_finalizar_turno_jugador_inicia_turno_enemigo_y_regresa(self, batalla_simple):
        """Test que finalizar turno ejecuta IA y regresa al jugador"""
        assert batalla_simple.turno_actual == TurnoActual.JUGADOR
        assert batalla_simple.ronda_actual == 1

        eventos = batalla_simple.finalizar_turno_jugador()

        # Después de finalizar turno, la IA ejecuta y regresa al jugador
        assert batalla_simple.turno_actual == TurnoActual.JUGADOR
        assert batalla_simple.ronda_actual == 2  # Nueva ronda

    def test_finalizar_turno_reinicia_estados_unidades(self, batalla_simple):
        """Test que finalizar turno reinicia estados de las unidades"""
        unidad = batalla_simple.ejercito_jugador.unidades_vivas[0]
        unidad.marcar_como_actuada()

        assert not unidad.puede_actuar
        assert not unidad.puede_moverse

        batalla_simple.finalizar_turno_jugador()

        # Después de un turno completo, las unidades se reinician
        assert unidad.puede_actuar
        assert unidad.puede_moverse

    def test_victoria_jugador_cuando_enemigo_derrotado(self, batalla_simple):
        """Test que el jugador gana cuando elimina todos los enemigos"""
        # Eliminar todos los enemigos
        for unidad in batalla_simple.ejercito_enemigo.unidades_vivas:
            unidad._vida_actual = 0

        batalla_simple._ejercito_enemigo.remover_unidades_muertas()

        # Simular ataque que verifica condición de victoria
        batalla_simple._finalizar_batalla(Bando.ROMA)

        assert batalla_simple.batalla_terminada
        assert batalla_simple.ganador == Bando.ROMA

    def test_derrota_jugador_cuando_eliminado(self, batalla_simple):
        """Test que el jugador pierde cuando pierde todas sus unidades"""
        # Eliminar todas las unidades del jugador
        for unidad in batalla_simple.ejercito_jugador.unidades_vivas:
            unidad._vida_actual = 0

        batalla_simple._ejercito_jugador.remover_unidades_muertas()

        batalla_simple._finalizar_batalla(Bando.BARBAROS)

        assert batalla_simple.batalla_terminada
        assert batalla_simple.ganador == Bando.BARBAROS

    def test_obtener_movimientos_validos_unidad_seleccionada(self, batalla_simple):
        """Test obtener movimientos válidos de unidad seleccionada"""
        unidad = batalla_simple.ejercito_jugador.unidades_vivas[0]
        batalla_simple.seleccionar_unidad(unidad.id)

        movimientos = batalla_simple.obtener_movimientos_validos_unidad_seleccionada()

        assert isinstance(movimientos, list)
        assert all(isinstance(pos, Posicion) for pos in movimientos)

    def test_obtener_objetivos_atacables_unidad_seleccionada(self, batalla_simple):
        """Test obtener objetivos atacables de unidad seleccionada"""
        unidad_atacante = batalla_simple.ejercito_jugador.unidades_vivas[0]
        unidad_objetivo = batalla_simple.ejercito_enemigo.unidades_vivas[0]

        # Colocar unidades cerca
        unidad_atacante._posicion = Posicion(3, 3)
        unidad_objetivo._posicion = Posicion(3, 4)

        batalla_simple.seleccionar_unidad(unidad_atacante.id)

        objetivos = batalla_simple.obtener_objetivos_atacables_unidad_seleccionada()

        assert len(objetivos) > 0
        assert unidad_objetivo in objetivos

    def test_deseleccionar_unidad(self, batalla_simple):
        """Test deseleccionar unidad"""
        unidad = batalla_simple.ejercito_jugador.unidades_vivas[0]
        batalla_simple.seleccionar_unidad(unidad.id)

        assert batalla_simple.unidad_seleccionada is not None

        batalla_simple.deseleccionar_unidad()

        assert batalla_simple.unidad_seleccionada is None

    def test_aplicar_formacion(self, batalla_simple):
        """Test aplicar formación al ejército"""
        from src.domain.events import EventoFormacionAplicada

        eventos = batalla_simple.aplicar_formacion("testudo")

        assert any(isinstance(e, EventoFormacionAplicada) for e in eventos)

    def test_no_aplicar_formacion_en_turno_enemigo(self, batalla_simple):
        """Test que no se puede cambiar formación en turno enemigo"""
        batalla_simple._turno_actual = TurnoActual.ENEMIGO

        with pytest.raises(ExcepcionTurnoInvalido):
            batalla_simple.aplicar_formacion("testudo")
