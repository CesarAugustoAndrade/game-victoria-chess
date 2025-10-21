"""
Pytest fixtures and configuration for Legio Romana tests
"""

import pytest
from src.domain.entities import Unidad, Ejercito, Tablero
from src.domain.batalla import Batalla
from src.domain.value_objects import (
    TipoUnidad, Bando, Posicion, EstadisticasUnidad, VisualizacionUnidad
)
from src.domain.strategies import IAAgresiva


@pytest.fixture
def stats_legionario():
    """Estadísticas de legionario para tests"""
    return EstadisticasUnidad(
        vida_maxima=100,
        ataque=20,
        defensa=10,
        rango_movimiento=2,
        rango_ataque=1,
        bonus_contra_caballeria=0,
        moral=80
    )


@pytest.fixture
def stats_triarii():
    """Estadísticas de triarii para tests"""
    return EstadisticasUnidad(
        vida_maxima=90,
        ataque=23,
        defensa=12,
        rango_movimiento=1,
        rango_ataque=1,
        bonus_contra_caballeria=20,
        moral=100
    )


@pytest.fixture
def stats_equites():
    """Estadísticas de equites para tests"""
    return EstadisticasUnidad(
        vida_maxima=120,
        ataque=35,
        defensa=8,
        rango_movimiento=3,
        rango_ataque=1,
        bonus_contra_caballeria=0,
        moral=85
    )


@pytest.fixture
def visual_romano():
    """Visualización romana genérica para tests"""
    return VisualizacionUnidad(
        nombre="Legionario Test",
        nombre_latino="Legionarius Test",
        icono="⚔",
        color_principal=(180, 20, 20),
        color_secundario=(255, 215, 0),
        grito_guerra="ROMA AETERNA!"
    )


@pytest.fixture
def visual_barbaro():
    """Visualización bárbara genérica para tests"""
    return VisualizacionUnidad(
        nombre="Guerrero Test",
        nombre_latino="Barbarus Test",
        icono="⚔",
        color_principal=(50, 100, 50),
        color_secundario=(139, 69, 19),
        grito_guerra="AAAAARGH!"
    )


@pytest.fixture
def unidad_legionario(stats_legionario, visual_romano):
    """Crea una unidad legionario de prueba"""
    return Unidad(
        id="test-leg-1",
        tipo=TipoUnidad.LEGIONARIO,
        bando=Bando.ROMA,
        estadisticas=stats_legionario,
        visualizacion=visual_romano,
        posicion=Posicion(5, 3)
    )


@pytest.fixture
def unidad_triarii(stats_triarii, visual_romano):
    """Crea una unidad triarii de prueba"""
    return Unidad(
        id="test-tri-1",
        tipo=TipoUnidad.TRIARII,
        bando=Bando.ROMA,
        estadisticas=stats_triarii,
        visualizacion=visual_romano,
        posicion=Posicion(6, 3)
    )


@pytest.fixture
def unidad_equites(stats_equites, visual_romano):
    """Crea una unidad equites de prueba"""
    return Unidad(
        id="test-eq-1",
        tipo=TipoUnidad.EQUITES,
        bando=Bando.ROMA,
        estadisticas=stats_equites,
        visualizacion=visual_romano,
        posicion=Posicion(7, 0)
    )


@pytest.fixture
def unidad_enemiga(stats_legionario, visual_barbaro):
    """Crea una unidad enemiga de prueba"""
    return Unidad(
        id="test-enemy-1",
        tipo=TipoUnidad.LEGIONARIO,
        bando=Bando.BARBAROS,
        estadisticas=stats_legionario,
        visualizacion=visual_barbaro,
        posicion=Posicion(2, 3)
    )


@pytest.fixture
def ejercito_jugador_pequeno(unidad_legionario, unidad_triarii):
    """Crea un ejército pequeño del jugador para tests"""
    ejercito = Ejercito(Bando.ROMA)
    ejercito.agregar_unidad(unidad_legionario)
    ejercito.agregar_unidad(unidad_triarii)
    return ejercito


@pytest.fixture
def ejercito_enemigo_pequeno(unidad_enemiga):
    """Crea un ejército pequeño enemigo para tests"""
    ejercito = Ejercito(Bando.BARBAROS)
    ejercito.agregar_unidad(unidad_enemiga)
    return ejercito


@pytest.fixture
def tablero_vacio():
    """Crea un tablero vacío de 9x7"""
    return Tablero(9, 7)


@pytest.fixture
def batalla_simple(ejercito_jugador_pequeno, ejercito_enemigo_pequeno, tablero_vacio):
    """Crea una batalla simple para tests"""
    estrategia_ia = IAAgresiva()
    batalla = Batalla(
        ejercito_jugador_pequeno,
        ejercito_enemigo_pequeno,
        tablero_vacio,
        estrategia_ia
    )
    batalla.iniciar()
    return batalla


@pytest.fixture
def unidad_en_panico(stats_legionario, visual_romano):
    """Crea una unidad en pánico para tests"""
    unidad = Unidad(
        id="test-panic-1",
        tipo=TipoUnidad.LEGIONARIO,
        bando=Bando.ROMA,
        estadisticas=stats_legionario,
        visualizacion=visual_romano,
        posicion=Posicion(5, 5)
    )
    unidad._moral_actual = 20  # Por debajo del umbral de pánico (30)
    return unidad


@pytest.fixture
def unidad_herida(stats_legionario, visual_romano):
    """Crea una unidad herida para tests"""
    unidad = Unidad(
        id="test-wounded-1",
        tipo=TipoUnidad.LEGIONARIO,
        bando=Bando.ROMA,
        estadisticas=stats_legionario,
        visualizacion=visual_romano,
        posicion=Posicion(4, 4)
    )
    unidad._vida_actual = 30  # 30% de vida
    unidad._moral_actual = 40  # Moral baja pero no en pánico
    return unidad
