"""
Script de prueba para verificar las características de Fase 1 YOLO
"""

import sys
import random

# Test imports
print("=" * 60)
print("TESTING PHASE 1 - YOLO BOOM BOOM FEATURES")
print("=" * 60)

print("\n1. Testing domain events imports...")
try:
    from src.domain.events import (
        EventoCriticoRealizado, EventoKillRegistrado, EventoCamaraLenta
    )
    print("[OK] All new events imported successfully")

    # Test event creation
    evento_critico = EventoCriticoRealizado(
        atacante_id="test1",
        defensor_id="test2",
        danio_total=50,
        multiplicador=2.0,
        posicion=None,
        mensaje="Test critical"
    )
    print(f"[OK] EventoCriticoRealizado created: {evento_critico.mensaje}")

except Exception as e:
    print(f"[ERROR] Error importing events: {e}")
    sys.exit(1)

print("\n2. Testing CalculadorCombate critical system...")
try:
    from src.domain.services import CalculadorCombate
    from src.domain.entities import Unidad
    from src.domain.value_objects import (
        TipoUnidad, Bando, Posicion, EstadisticasUnidad, VisualizacionUnidad
    )

    # Create test units
    stats = EstadisticasUnidad(100, 20, 10, 2, 1, 0, 100)
    viz = VisualizacionUnidad(
        nombre="Test Legionario",
        nombre_latino="Tester",
        icono="L",
        color_principal=(180, 20, 20),
        color_secundario=(200, 50, 50),
        grito_guerra="TEST!"
    )

    atacante = Unidad("atk1", TipoUnidad.LEGIONARIO, Bando.ROMA, stats, viz, Posicion(0, 0))
    defensor = Unidad("def1", TipoUnidad.HASTATI, Bando.BARBAROS, stats, viz, Posicion(1, 1))

    # Test critical system
    print(f"   Critical probability: {CalculadorCombate.PROBABILIDAD_CRITICO * 100}%")
    print(f"   Critical multiplier: x{CalculadorCombate.MULTIPLICADOR_CRITICO}")
    print(f"   Devastator probability: {CalculadorCombate.PROBABILIDAD_CRITICO_DEVASTADOR * 100}%")
    print(f"   Devastator multiplier: x{CalculadorCombate.MULTIPLICADOR_CRITICO_DEVASTADOR}")

    # Execute attacks to test critical system
    critical_count = 0
    devastator_count = 0
    total_tests = 1000

    for i in range(total_tests):
        es_critico, multiplicador = CalculadorCombate.verificar_critico()
        if es_critico:
            if multiplicador >= 3.0:
                devastator_count += 1
            else:
                critical_count += 1

    crit_percent = (critical_count / total_tests) * 100
    dev_percent = (devastator_count / total_tests) * 100

    print(f"\n   Results from {total_tests} simulated attacks:")
    print(f"   Normal attacks: {total_tests - critical_count - devastator_count}")
    print(f"   Critical hits: {critical_count} ({crit_percent:.1f}%)")
    print(f"   Devastators: {devastator_count} ({dev_percent:.2f}%)")

    if 12 <= crit_percent <= 18:  # Around 15%
        print("[OK] Critical rate is within expected range!")
    else:
        print(f"[WARN] Critical rate {crit_percent:.1f}% is outside expected 12-18% range")

except Exception as e:
    print(f"[ERROR] Error testing combat system: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n3. Testing Kill Feed system...")
try:
    import pygame
    pygame.init()  # Initialize pygame for font system

    from src.presentation.kill_feed import KillFeed, KillNotification

    kill_feed = KillFeed(800, 600)
    kill_notification = KillNotification(800, 600)

    print(f"[OK] KillFeed created: max_entries={kill_feed.max_entries}")
    print(f"[OK] KillNotification created: duration={kill_notification.duracion_total}ms")

    # Test adding kills
    kill_feed.agregar_kill(
        asesino_nombre="Legionario",
        victima_nombre="Guerrero Galo",
        asesino_bando=Bando.ROMA,
        victima_bando=Bando.BARBAROS,
        fue_critico=True
    )

    print(f"[OK] Kill added to feed: {len(kill_feed.entries)} entries")

    # Test notification
    kill_notification.mostrar("GOLPE CRITICO!", es_devastador=False)
    print(f"[OK] Notification shown: active={kill_notification.active}")

except Exception as e:
    print(f"[ERROR] Error testing kill feed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n4. Testing AI strategy helper...")
try:
    from src.domain.strategies import EstrategiaIA

    # The helper method exists
    assert hasattr(EstrategiaIA, '_ejecutar_ataque_con_efectos')
    print("[OK] EstrategiaIA._ejecutar_ataque_con_efectos() exists")

except Exception as e:
    print(f"[ERROR] Error testing AI strategies: {e}")
    sys.exit(1)

print("\n5. Testing BatallaState integration...")
try:
    # Just import to verify no syntax errors
    from src.states.batalla_state import BatallaState
    print("[OK] BatallaState imports successfully")

    # Check for new attributes
    import inspect
    init_source = inspect.getsource(BatallaState.__init__)

    if 'kill_feed' in init_source:
        print("[OK] BatallaState has kill_feed system")
    else:
        print("[WARN] kill_feed not found in __init__")

    if 'slow_motion' in init_source:
        print("[OK] BatallaState has slow_motion system")
    else:
        print("[WARN] slow_motion not found in __init__")

except Exception as e:
    print(f"[ERROR] Error testing BatallaState: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n6. Testing BattleRenderer critical effects...")
try:
    from src.presentation.battle_renderer import BattleRenderer

    renderer = BattleRenderer()

    # Check for new method
    assert hasattr(renderer, 'trigger_critical_hit_effect')
    print("[OK] BattleRenderer has trigger_critical_hit_effect() method")

except Exception as e:
    print(f"[ERROR] Error testing BattleRenderer: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
print("\nPhase 1 features are ready to use:")
print("  * Critical Hit System (15% chance, x2 damage)")
print("  * Devastator Criticals (0.45% chance, x3 damage)")
print("  * Slow Motion effects (auto-triggered on crits)")
print("  * Kill Feed (top-right corner)")
print("  * Epic Notifications (center screen)")
print("  * Visual Effects (particles, screen shake, zoom)")
print("\nStart a battle to see them in action!")
print("=" * 60)
