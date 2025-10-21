"""
Combat calculation domain service
Handles damage calculations and combat resolution
"""

import random
from src.domain.entities import Unidad
from src.domain.value_objects import TipoUnidad, ResultadoAtaque
from src.domain.constants import (
    VARIANZA_DANIO_MIN, VARIANZA_DANIO_MAX,
    MORAL_PERDIDA_MAX_POR_DANIO
)


class CalculadorCombate:
    """Servicio de dominio para cálculos de combate"""

    @staticmethod
    def calcular_danio(atacante: Unidad, defensor: Unidad) -> int:
        """Calcula el daño de un ataque con varianza aleatoria"""
        varianza = random.uniform(VARIANZA_DANIO_MIN, VARIANZA_DANIO_MAX)
        return atacante.calcular_danio_contra(defensor, varianza)

    @staticmethod
    def ejecutar_ataque(atacante: Unidad, defensor: Unidad) -> ResultadoAtaque:
        """Ejecuta un ataque y retorna el resultado"""
        danio = CalculadorCombate.calcular_danio(atacante, defensor)

        vida_antes = defensor.vida_actual
        defensor.recibir_danio(danio)
        atacante.marcar_como_actuada()

        # Calcular pérdida de moral
        moral_perdida = min(MORAL_PERDIDA_MAX_POR_DANIO, danio)

        return ResultadoAtaque(
            atacante_id=atacante.id,
            defensor_id=defensor.id,
            danio_infligido=danio,
            objetivo_eliminado=not defensor.esta_viva,
            moral_perdida=moral_perdida
        )

    @staticmethod
    def calcular_bonificacion_formacion(atacante: Unidad, formacion: str) -> int:
        """Calcula bonificación de ataque según formación"""
        bonus = 0
        if formacion == "cuneus":  # Formación en cuña
            if atacante.tipo in [TipoUnidad.LEGIONARIO, TipoUnidad.HASTATI]:
                bonus = 5
        elif formacion == "testudo":  # Formación tortuga
            bonus = -3  # Penalización al ataque, pero mejor defensa
        return bonus
