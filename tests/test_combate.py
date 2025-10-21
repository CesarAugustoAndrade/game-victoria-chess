"""
Tests for combat calculations and damage system
"""

import pytest
from src.domain.services import CalculadorCombate
from src.domain.value_objects import TipoUnidad
from src.domain.constants import (
    VARIANZA_DANIO_MIN, VARIANZA_DANIO_MAX,
    DANIO_MINIMO, MORAL_PERDIDA_MAX_POR_DANIO
)


@pytest.mark.unit
@pytest.mark.combat
@pytest.mark.domain
class TestCalculadorCombate:
    """Tests for CalculadorCombate domain service"""

    def test_calcular_danio_aplica_varianza(self, unidad_legionario, unidad_enemiga):
        """Test que el daño calculado incluye varianza aleatoria"""
        # Ejecutar múltiples cálculos para verificar varianza
        danios = [
            CalculadorCombate.calcular_danio(unidad_legionario, unidad_enemiga)
            for _ in range(10)
        ]

        # Verificar que hay variación en los resultados
        assert len(set(danios)) > 1, "Debería haber varianza en el daño"

        # Verificar que todos los daños son positivos
        assert all(d >= DANIO_MINIMO for d in danios)

    def test_ejecutar_ataque_reduce_vida_objetivo(self, unidad_legionario, unidad_enemiga):
        """Test que atacar reduce la vida del objetivo"""
        vida_inicial = unidad_enemiga.vida_actual

        resultado = CalculadorCombate.ejecutar_ataque(unidad_legionario, unidad_enemiga)

        assert unidad_enemiga.vida_actual < vida_inicial
        assert resultado.danio_infligido > 0
        assert resultado.atacante_id == unidad_legionario.id
        assert resultado.defensor_id == unidad_enemiga.id

    def test_ejecutar_ataque_reduce_moral(self, unidad_legionario, unidad_enemiga):
        """Test que atacar reduce la moral del objetivo"""
        moral_inicial = unidad_enemiga.moral_actual

        CalculadorCombate.ejecutar_ataque(unidad_legionario, unidad_enemiga)

        assert unidad_enemiga.moral_actual < moral_inicial

    def test_ejecutar_ataque_marca_atacante_como_actuado(self, unidad_legionario, unidad_enemiga):
        """Test que el atacante queda marcado como que actuó"""
        assert unidad_legionario.puede_actuar

        CalculadorCombate.ejecutar_ataque(unidad_legionario, unidad_enemiga)

        assert not unidad_legionario.puede_actuar
        assert unidad_legionario._ha_actuado
        assert unidad_legionario._ha_movido

    def test_ejecutar_ataque_puede_eliminar_objetivo(self, unidad_legionario, unidad_enemiga):
        """Test que un ataque puede eliminar al objetivo si hace suficiente daño"""
        # Reducir vida del enemigo a casi nada
        unidad_enemiga._vida_actual = 1

        resultado = CalculadorCombate.ejecutar_ataque(unidad_legionario, unidad_enemiga)

        assert not unidad_enemiga.esta_viva
        assert resultado.objetivo_eliminado

    def test_triarii_bonus_contra_equites(self, unidad_triarii, unidad_equites, unidad_legionario):
        """Test que Triarii tienen bonus de daño contra Equites"""
        # Calcular daño contra equites (con bonus)
        danio_vs_equites = unidad_triarii.calcular_danio_contra(unidad_equites, varianza=0)

        # Calcular daño contra legionario (sin bonus)
        danio_vs_legionario = unidad_triarii.calcular_danio_contra(unidad_legionario, varianza=0)

        # El daño contra equites debe ser mayor debido al bonus
        assert danio_vs_equites > danio_vs_legionario
        # La diferencia debe ser mayor al bonus base (bonus_contra_caballeria = 20)
        # El bonus se suma ANTES del cálculo de defensa, por lo que la diferencia final
        # depende de cómo se aplica la defensa de cada unidad
        diferencia = danio_vs_equites - danio_vs_legionario
        assert diferencia >= 20, f"Diferencia de daño {diferencia} debe ser al menos 20"

    def test_unidad_en_panico_hace_menos_danio(self, unidad_legionario, unidad_enemiga):
        """Test que las unidades en pánico hacen la mitad de daño"""
        # Calcular daño normal
        danio_normal = unidad_legionario.calcular_danio_contra(unidad_enemiga, varianza=0)

        # Poner unidad en pánico
        unidad_legionario._moral_actual = 20  # Bajo umbral de pánico (30)

        # Calcular daño en pánico
        danio_panico = unidad_legionario.calcular_danio_contra(unidad_enemiga, varianza=0)

        # El daño en pánico debe ser aproximadamente la mitad
        assert danio_panico < danio_normal
        assert danio_panico == danio_normal // 2

    def test_calcular_bonificacion_formacion_cuneus(self, unidad_legionario):
        """Test bonificación de formación Cuneus para legionarios"""
        bonus_cuneus = CalculadorCombate.calcular_bonificacion_formacion(
            unidad_legionario, "cuneus"
        )

        assert bonus_cuneus == 5

    def test_calcular_bonificacion_formacion_testudo(self, unidad_legionario):
        """Test penalización de formación Testudo al ataque"""
        bonus_testudo = CalculadorCombate.calcular_bonificacion_formacion(
            unidad_legionario, "testudo"
        )

        assert bonus_testudo == -3  # Penalización al ataque

    def test_moral_perdida_limitada(self, unidad_legionario, unidad_enemiga):
        """Test que la pérdida de moral está limitada"""
        # Hacer mucho daño
        unidad_enemiga._vida_actual = 1000  # Mucha vida para que no muera

        resultado = CalculadorCombate.ejecutar_ataque(unidad_legionario, unidad_enemiga)

        # La moral perdida no debe exceder el máximo
        assert resultado.moral_perdida <= MORAL_PERDIDA_MAX_POR_DANIO

    def test_danio_minimo_siempre_es_uno(self, unidad_legionario):
        """Test que el daño mínimo es siempre 1, incluso con alta defensa"""
        from src.domain.entities import Unidad
        from src.domain.value_objects import EstadisticasUnidad, VisualizacionUnidad, Bando, Posicion

        # Crear unidad con defensa muy alta
        stats_super_defensa = EstadisticasUnidad(
            vida_maxima=200,
            ataque=5,
            defensa=1000,  # Defensa extremadamente alta
            rango_movimiento=1,
            rango_ataque=1,
            bonus_contra_caballeria=0,
            moral=100
        )

        visual = VisualizacionUnidad(
            nombre="Tanque", nombre_latino="Tanqueus",
            icono="🛡", color_principal=(100, 100, 100),
            color_secundario=(150, 150, 150), grito_guerra="INVENCIBLE!"
        )

        tanque = Unidad(
            id="tanque-1", tipo=TipoUnidad.HASTATI, bando=Bando.BARBAROS,
            estadisticas=stats_super_defensa, visualizacion=visual,
            posicion=Posicion(1, 1)
        )

        danio = unidad_legionario.calcular_danio_contra(tanque, varianza=0)

        assert danio >= DANIO_MINIMO
