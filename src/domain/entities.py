"""
Entidades del dominio de Legio Romana
"""

from typing import List, Optional
from src.domain.value_objects import (
    TipoUnidad, Bando, Posicion, EstadisticasUnidad,
    VisualizacionUnidad, ResultadoAtaque, TurnoActual
)
from src.domain.exceptions import (
    ExcepcionMovimientoInvalido, ExcepcionAccionInvalida,
    ExcepcionDominio
)


class Unidad:
    """Entidad que representa una unidad militar en el campo de batalla"""

    def __init__(
        self,
        id: str,
        tipo: TipoUnidad,
        bando: Bando,
        estadisticas: EstadisticasUnidad,
        visualizacion: VisualizacionUnidad,
        posicion: Posicion
    ):
        self._id = id
        self._tipo = tipo
        self._bando = bando
        self._estadisticas = estadisticas
        self._visualizacion = visualizacion
        self._posicion = posicion
        self._vida_actual = estadisticas.vida_maxima
        self._moral_actual = estadisticas.moral
        self._ha_movido = False
        self._ha_actuado = False

    # Propiedades de solo lectura
    @property
    def id(self) -> str:
        return self._id

    @property
    def tipo(self) -> TipoUnidad:
        return self._tipo

    @property
    def bando(self) -> Bando:
        return self._bando

    @property
    def posicion(self) -> Posicion:
        return self._posicion

    @property
    def vida_actual(self) -> int:
        return self._vida_actual

    @property
    def moral_actual(self) -> int:
        return self._moral_actual

    @property
    def estadisticas(self) -> EstadisticasUnidad:
        return self._estadisticas

    @property
    def visualizacion(self) -> VisualizacionUnidad:
        return self._visualizacion

    @property
    def esta_viva(self) -> bool:
        return self._vida_actual > 0

    @property
    def esta_en_panico(self) -> bool:
        """Unidad en pánico si moral < 30%"""
        return self._moral_actual < 30

    @property
    def puede_actuar(self) -> bool:
        return not self._ha_actuado and self.esta_viva and not self.esta_en_panico

    @property
    def puede_moverse(self) -> bool:
        return not self._ha_movido and self.esta_viva and not self.esta_en_panico

    @property
    def porcentaje_vida(self) -> float:
        return self._vida_actual / self._estadisticas.vida_maxima

    def mover_a(self, nueva_posicion: Posicion) -> None:
        """Mueve la unidad a una nueva posición"""
        if not self.puede_moverse:
            raise ExcepcionMovimientoInvalido("La unidad no puede moverse")

        self._posicion = nueva_posicion
        self._ha_movido = True

    def recibir_danio(self, cantidad: int) -> None:
        """Aplica daño a la unidad"""
        self._vida_actual = max(0, self._vida_actual - cantidad)
        # Perder moral al recibir daño
        perdida_moral = min(10, cantidad // 2)
        self._moral_actual = max(0, self._moral_actual - perdida_moral)

    def restaurar_moral(self, cantidad: int) -> None:
        """Restaura moral de la unidad"""
        self._moral_actual = min(100, self._moral_actual + cantidad)

    def marcar_como_actuada(self) -> None:
        """Marca la unidad como que ya actuó en este turno"""
        self._ha_actuado = True
        self._ha_movido = True

    def reiniciar_turno(self) -> None:
        """Reinicia los estados de movimiento y acción para nuevo turno"""
        self._ha_movido = False
        self._ha_actuado = False
        # Recuperar un poco de moral cada turno
        if self.esta_viva and not self.esta_en_panico:
            self.restaurar_moral(5)

    def calcular_danio_contra(self, objetivo: 'Unidad', varianza: float = 0) -> int:
        """Calcula el daño que esta unidad haría contra el objetivo"""
        danio_base = self._estadisticas.calcular_danio_base(
            objetivo._estadisticas.defensa
        )

        # Bonus especial: Triarii (Piqueros) vs Equites (Caballería)
        if self._tipo == TipoUnidad.TRIARII and objetivo._tipo == TipoUnidad.EQUITES:
            danio_base += self._estadisticas.bonus_contra_caballeria

        # Penalización por moral baja
        if self.esta_en_panico:
            danio_base = danio_base // 2

        # Aplicar varianza aleatoria
        danio_final = danio_base + varianza

        return max(1, int(danio_final))

    def obtener_posiciones_movimiento_validas(self, tablero) -> List[Posicion]:
        """Retorna lista de posiciones válidas donde puede moverse"""
        if not self.puede_moverse:
            return []

        posiciones_validas = []
        rango = self._estadisticas.rango_movimiento

        for fila in range(
            max(0, self._posicion.fila - rango),
            min(tablero.filas, self._posicion.fila + rango + 1)
        ):
            for columna in range(
                max(0, self._posicion.columna - rango),
                min(tablero.columnas, self._posicion.columna + rango + 1)
            ):
                nueva_pos = Posicion(fila, columna)
                distancia = self._posicion.distancia_manhattan(nueva_pos)

                if 0 < distancia <= rango:
                    if not tablero.esta_ocupada(nueva_pos):
                        posiciones_validas.append(nueva_pos)

        return posiciones_validas

    def obtener_objetivos_atacables(self, unidades_enemigas: List['Unidad']) -> List['Unidad']:
        """Retorna lista de unidades enemigas que puede atacar"""
        if not self.puede_actuar:
            return []

        objetivos = []
        rango = self._estadisticas.rango_ataque

        for enemigo in unidades_enemigas:
            if enemigo.esta_viva:
                distancia = self._posicion.distancia_manhattan(enemigo.posicion)
                if distancia <= rango:
                    objetivos.append(enemigo)

        return objetivos


class Ejercito:
    """Agregado que representa un ejército completo"""

    def __init__(self, bando: Bando):
        self._bando = bando
        self._unidades: List[Unidad] = []
        self._formacion = "linea"  # Formación actual

    @property
    def bando(self) -> Bando:
        return self._bando

    @property
    def unidades_vivas(self) -> List[Unidad]:
        return [u for u in self._unidades if u.esta_viva]

    @property
    def unidades_en_panico(self) -> List[Unidad]:
        return [u for u in self.unidades_vivas if u.esta_en_panico]

    @property
    def cantidad_unidades(self) -> int:
        return len(self.unidades_vivas)

    @property
    def esta_derrotado(self) -> bool:
        return self.cantidad_unidades == 0

    @property
    def moral_promedio(self) -> float:
        """Calcula la moral promedio del ejército"""
        if not self.unidades_vivas:
            return 0
        return sum(u.moral_actual for u in self.unidades_vivas) / len(self.unidades_vivas)

    def agregar_unidad(self, unidad: Unidad) -> None:
        """Agrega una unidad al ejército"""
        if unidad.bando != self._bando:
            raise ExcepcionDominio("La unidad no pertenece a este bando")
        self._unidades.append(unidad)

    def remover_unidades_muertas(self) -> List[Unidad]:
        """Remueve unidades muertas y retorna las eliminadas"""
        unidades_muertas = [u for u in self._unidades if not u.esta_viva]
        self._unidades = self.unidades_vivas
        return unidades_muertas

    def reiniciar_turno_todas_unidades(self) -> None:
        """Reinicia el estado de turno de todas las unidades"""
        for unidad in self.unidades_vivas:
            unidad.reiniciar_turno()

    def obtener_unidad_por_id(self, id: str) -> Optional[Unidad]:
        """Busca una unidad por su ID"""
        for unidad in self._unidades:
            if unidad.id == id:
                return unidad
        return None

    def obtener_unidad_en_posicion(self, posicion: Posicion) -> Optional[Unidad]:
        """Busca una unidad en una posición específica"""
        for unidad in self.unidades_vivas:
            if unidad.posicion == posicion:
                return unidad
        return None

    def aplicar_formacion(self, formacion: str) -> None:
        """Aplica una formación al ejército"""
        self._formacion = formacion
        # Aquí se aplicarían bonificaciones según la formación
        if formacion == "testudo":
            # Formación tortuga: +defensa, -movimiento
            for unidad in self.unidades_vivas:
                unidad.restaurar_moral(10)
        elif formacion == "cuneus":
            # Formación en cuña: +ataque, -defensa
            for unidad in self.unidades_vivas:
                if unidad.tipo in [TipoUnidad.LEGIONARIO, TipoUnidad.HASTATI]:
                    unidad.restaurar_moral(15)


class Tablero:
    """Agregado que representa el campo de batalla"""

    def __init__(self, filas: int = 9, columnas: int = 7):
        self._filas = filas
        self._columnas = columnas
        self._ejercitos: List[Ejercito] = []

    @property
    def filas(self) -> int:
        return self._filas

    @property
    def columnas(self) -> int:
        return self._columnas

    def registrar_ejercito(self, ejercito: Ejercito) -> None:
        """Registra un ejército en el tablero"""
        self._ejercitos.append(ejercito)

    def esta_ocupada(self, posicion: Posicion) -> bool:
        """Verifica si una posición está ocupada por alguna unidad"""
        for ejercito in self._ejercitos:
            if ejercito.obtener_unidad_en_posicion(posicion) is not None:
                return True
        return False

    def obtener_unidad_en(self, posicion: Posicion) -> Optional[Unidad]:
        """Obtiene la unidad en una posición específica"""
        for ejercito in self._ejercitos:
            unidad = ejercito.obtener_unidad_en_posicion(posicion)
            if unidad:
                return unidad
        return None

    def obtener_todas_las_posiciones(self) -> List[Posicion]:
        """Obtiene todas las posiciones del tablero"""
        posiciones = []
        for fila in range(self._filas):
            for columna in range(self._columnas):
                posiciones.append(Posicion(fila, columna))
        return posiciones