"""
Tests for Unidad entity behavior
"""

import pytest
from src.domain.value_objects import Posicion
from src.domain.entities import Tablero, Ejercito
from src.domain.constants import (
    UMBRAL_PANICO, MORAL_REGENERACION_POR_TURNO,
    MORAL_MAXIMA, MORAL_PERDIDA_POR_PUNTO_DANIO
)


@pytest.mark.unit
@pytest.mark.domain
class TestUnidad:
    """Tests for Unidad entity"""

    def test_unidad_inicia_con_vida_completa(self, unidad_legionario):
        """Test que una unidad nueva tiene vida completa"""
        assert unidad_legionario.esta_viva
        assert unidad_legionario.vida_actual == unidad_legionario.estadisticas.vida_maxima
        assert unidad_legionario.porcentaje_vida == 1.0

    def test_unidad_inicia_sin_panico(self, unidad_legionario):
        """Test que una unidad nueva no está en pánico"""
        assert not unidad_legionario.esta_en_panico
        assert unidad_legionario.moral_actual >= UMBRAL_PANICO

    def test_unidad_puede_actuar_al_inicio(self, unidad_legionario):
        """Test que una unidad puede actuar y moverse al inicio"""
        assert unidad_legionario.puede_actuar
        assert unidad_legionario.puede_moverse

    def test_mover_unidad_marca_como_movida(self, unidad_legionario):
        """Test que mover una unidad la marca como movida"""
        assert unidad_legionario.puede_moverse

        unidad_legionario.mover_a(Posicion(4, 3))

        assert not unidad_legionario.puede_moverse
        assert unidad_legionario._ha_movido
        assert unidad_legionario.posicion == Posicion(4, 3)

    def test_recibir_danio_reduce_vida(self, unidad_legionario):
        """Test que recibir daño reduce la vida"""
        vida_inicial = unidad_legionario.vida_actual

        unidad_legionario.recibir_danio(20)

        assert unidad_legionario.vida_actual == vida_inicial - 20
        assert unidad_legionario.esta_viva

    def test_recibir_danio_reduce_moral(self, unidad_legionario):
        """Test que recibir daño también reduce la moral"""
        moral_inicial = unidad_legionario.moral_actual

        unidad_legionario.recibir_danio(20)

        # Moral se reduce: perdida = min(10, danio // 2) = min(10, 10) = 10
        assert unidad_legionario.moral_actual < moral_inicial

    def test_recibir_danio_letal_mata_unidad(self, unidad_legionario):
        """Test que recibir daño mayor a la vida mata la unidad"""
        unidad_legionario.recibir_danio(1000)

        assert not unidad_legionario.esta_viva
        assert unidad_legionario.vida_actual == 0

    def test_vida_no_baja_de_cero(self, unidad_legionario):
        """Test que la vida no puede ser negativa"""
        unidad_legionario.recibir_danio(1000)

        assert unidad_legionario.vida_actual >= 0

    def test_unidad_en_panico_cuando_moral_baja(self, unidad_legionario):
        """Test que una unidad entra en pánico con moral baja"""
        unidad_legionario._moral_actual = UMBRAL_PANICO - 1

        assert unidad_legionario.esta_en_panico

    def test_unidad_en_panico_no_puede_actuar(self, unidad_en_panico):
        """Test que una unidad en pánico no puede actuar"""
        assert unidad_en_panico.esta_en_panico
        assert not unidad_en_panico.puede_actuar

    def test_unidad_en_panico_no_puede_moverse(self, unidad_en_panico):
        """Test que una unidad en pánico no puede moverse"""
        assert unidad_en_panico.esta_en_panico
        assert not unidad_en_panico.puede_moverse

    def test_restaurar_moral_aumenta_moral(self, unidad_herida):
        """Test que restaurar moral la aumenta"""
        moral_inicial = unidad_herida.moral_actual

        unidad_herida.restaurar_moral(20)

        assert unidad_herida.moral_actual == moral_inicial + 20

    def test_moral_no_supera_maximo(self, unidad_legionario):
        """Test que la moral no puede superar el máximo"""
        unidad_legionario._moral_actual = MORAL_MAXIMA

        unidad_legionario.restaurar_moral(50)

        assert unidad_legionario.moral_actual == MORAL_MAXIMA

    def test_marcar_como_actuada(self, unidad_legionario):
        """Test marcar unidad como que actuó"""
        unidad_legionario.marcar_como_actuada()

        assert not unidad_legionario.puede_actuar
        assert not unidad_legionario.puede_moverse
        assert unidad_legionario._ha_actuado
        assert unidad_legionario._ha_movido

    def test_reiniciar_turno_resetea_estados(self, unidad_legionario):
        """Test que reiniciar turno resetea los estados de acción"""
        unidad_legionario.marcar_como_actuada()
        assert not unidad_legionario.puede_actuar

        unidad_legionario.reiniciar_turno()

        assert unidad_legionario.puede_actuar
        assert unidad_legionario.puede_moverse

    def test_reiniciar_turno_regenera_moral(self, unidad_herida):
        """Test que reiniciar turno regenera un poco de moral"""
        moral_inicial = unidad_herida.moral_actual

        unidad_herida.reiniciar_turno()

        assert unidad_herida.moral_actual == moral_inicial + MORAL_REGENERACION_POR_TURNO

    def test_obtener_posiciones_movimiento_validas(self, unidad_legionario):
        """Test obtener posiciones de movimiento válidas"""
        tablero = Tablero()
        tablero.registrar_ejercito(Ejercito(unidad_legionario.bando))

        movimientos = unidad_legionario.obtener_posiciones_movimiento_validas(tablero)

        assert isinstance(movimientos, list)
        assert all(isinstance(pos, Posicion) for pos in movimientos)
        # Legionario tiene rango_movimiento=2
        assert len(movimientos) > 0

    def test_no_movimientos_validos_si_ya_movio(self, unidad_legionario):
        """Test que no hay movimientos válidos si ya se movió"""
        tablero = Tablero()
        unidad_legionario._ha_movido = True

        movimientos = unidad_legionario.obtener_posiciones_movimiento_validas(tablero)

        assert movimientos == []

    def test_no_movimientos_validos_si_en_panico(self, unidad_en_panico):
        """Test que no hay movimientos válidos si está en pánico"""
        tablero = Tablero()

        movimientos = unidad_en_panico.obtener_posiciones_movimiento_validas(tablero)

        assert movimientos == []

    def test_obtener_objetivos_atacables(self, unidad_legionario, unidad_enemiga):
        """Test obtener objetivos atacables en rango"""
        # Colocar enemigo en rango (adyacente)
        unidad_legionario._posicion = Posicion(3, 3)
        unidad_enemiga._posicion = Posicion(3, 4)

        objetivos = unidad_legionario.obtener_objetivos_atacables([unidad_enemiga])

        assert len(objetivos) == 1
        assert unidad_enemiga in objetivos

    def test_no_objetivos_atacables_fuera_de_rango(self, unidad_legionario, unidad_enemiga):
        """Test que no hay objetivos atacables fuera de rango"""
        # Colocar enemigo lejos
        unidad_legionario._posicion = Posicion(8, 0)
        unidad_enemiga._posicion = Posicion(0, 6)

        objetivos = unidad_legionario.obtener_objetivos_atacables([unidad_enemiga])

        assert len(objetivos) == 0

    def test_no_objetivos_atacables_si_ya_actuo(self, unidad_legionario, unidad_enemiga):
        """Test que no puede atacar si ya actuó"""
        unidad_legionario.marcar_como_actuada()

        objetivos = unidad_legionario.obtener_objetivos_atacables([unidad_enemiga])

        assert objetivos == []

    def test_porcentaje_vida_correcto(self, unidad_legionario):
        """Test que el porcentaje de vida se calcula correctamente"""
        assert unidad_legionario.porcentaje_vida == 1.0

        unidad_legionario.recibir_danio(50)  # 50 de 100 = 50%

        assert unidad_legionario.porcentaje_vida == 0.5

    def test_calcular_danio_contra_incluye_defensa(self, unidad_legionario, unidad_enemiga):
        """Test que el cálculo de daño considera la defensa del objetivo"""
        # Sin varianza para ser determinista
        danio = unidad_legionario.calcular_danio_contra(unidad_enemiga, varianza=0)

        # Fórmula: ataque - (defensa_objetivo // 2)
        # 20 - (10 // 2) = 20 - 5 = 15
        assert danio == 15

    def test_equites_tiene_mayor_rango_movimiento(self, unidad_equites, unidad_legionario):
        """Test que los Equites tienen más rango de movimiento"""
        assert unidad_equites.estadisticas.rango_movimiento > unidad_legionario.estadisticas.rango_movimiento
        # Equites: 3, Legionario: 2
        assert unidad_equites.estadisticas.rango_movimiento == 3
        assert unidad_legionario.estadisticas.rango_movimiento == 2
