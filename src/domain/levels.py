"""
Sistema de niveles progresivos para Legio Romana
Introduce al jugador a las unidades y mecánicas del juego
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from src.domain.value_objects import TipoUnidad, Posicion, Bando


@dataclass
class ConfiguracionUnidad:
    """Configuración de una unidad en un nivel"""
    tipo: TipoUnidad
    posicion: Posicion


@dataclass
class Nivel:
    """Configuración de un nivel"""
    numero: int
    nombre: str
    descripcion: str
    objetivo: str
    unidades_jugador: List[ConfiguracionUnidad]
    unidades_enemigo: List[ConfiguracionUnidad]
    tutorial_messages: List[str]
    dificultad: str  # "facil", "medio", "dificil"

    @property
    def es_tutorial(self) -> bool:
        """Indica si el nivel es tutorial"""
        return self.numero <= 3


class CampaniaNiveles:
    """Gestiona la campaña de niveles progresivos"""

    def __init__(self):
        self.niveles = self._crear_niveles()
        self.nivel_actual = 0
        self.niveles_completados = set()

    def obtener_nivel(self, numero: int) -> Optional[Nivel]:
        """Obtiene un nivel por su número"""
        if 0 < numero <= len(self.niveles):
            return self.niveles[numero - 1]
        return None

    def obtener_nivel_actual(self) -> Nivel:
        """Obtiene el nivel actual"""
        return self.niveles[self.nivel_actual]

    def avanzar_nivel(self):
        """Avanza al siguiente nivel"""
        self.niveles_completados.add(self.nivel_actual)
        if self.nivel_actual < len(self.niveles) - 1:
            self.nivel_actual += 1

    def reiniciar_campania(self):
        """Reinicia la campaña desde el principio"""
        self.nivel_actual = 0
        self.niveles_completados.clear()

    def seleccionar_nivel(self, numero: int) -> bool:
        """Selecciona un nivel específico (si está desbloqueado)"""
        if numero <= 1 or (numero - 2) in self.niveles_completados:
            if 0 < numero <= len(self.niveles):
                self.nivel_actual = numero - 1
                return True
        return False

    @property
    def progreso_campania(self) -> float:
        """Retorna el progreso de la campaña (0.0 a 1.0)"""
        return len(self.niveles_completados) / len(self.niveles)

    def _crear_niveles(self) -> List[Nivel]:
        """Crea todos los niveles de la campaña"""
        return [
            self._crear_nivel_1(),
            self._crear_nivel_2(),
            self._crear_nivel_3(),
            self._crear_nivel_4(),
            self._crear_nivel_5(),
            self._crear_nivel_6(),
            self._crear_nivel_7(),
            self._crear_nivel_8(),
            self._crear_nivel_9(),
        ]

    # ========== NIVELES TUTORIAL (1-3) ==========

    def _crear_nivel_1(self) -> Nivel:
        """Nivel 1: Introducción - Princeps vs Guerreros"""
        return Nivel(
            numero=1,
            nombre="Primera Línea",
            descripcion="Aprende los fundamentos del combate",
            objetivo="Derrota a los 2 guerreros enemigos",
            dificultad="facil",
            tutorial_messages=[
                "¡Bienvenido a Legio Romana!",
                "Click izquierdo: Seleccionar unidad y moverse",
                "Click derecho: Atacar enemigos",
                "Barra verde: Vida de tus unidades",
                "Barra roja: Vida de enemigos",
                "¡Derrota a todos los enemigos para ganar!"
            ],
            unidades_jugador=[
                # 2 Princeps para el jugador
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 2)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 4)),
            ],
            unidades_enemigo=[
                # 2 Guerreros básicos
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 4)),
            ]
        )

    def _crear_nivel_2(self) -> Nivel:
        """Nivel 2: Movimiento y Posicionamiento - Introducción a Velites"""
        return Nivel(
            numero=2,
            nombre="Escaramuzadores",
            descripcion="Aprende a usar unidades rápidas y de rango",
            objetivo="Usa los Velites para atacar desde distancia",
            dificultad="facil",
            tutorial_messages=[
                "Los VELITES son infantería ligera con jabalinas",
                "Movimiento: 3 casillas (muy móviles)",
                "Ataque: Rango 2 (pueden atacar desde lejos)",
                "Usa su movilidad para flanquear al enemigo",
                "¡Mantén distancia y ataca desde rango seguro!"
            ],
            unidades_jugador=[
                # 2 Velites + 1 Hastati
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(7, 1)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(7, 5)),
            ],
            unidades_enemigo=[
                # 3 Guerreros en formación
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 4)),
            ]
        )

    def _crear_nivel_3(self) -> Nivel:
        """Nivel 3: Moral y Formaciones"""
        return Nivel(
            numero=3,
            nombre="Moral de Hierro",
            descripcion="Aprende sobre moral y formaciones",
            objetivo="Usa formaciones para mantener alta moral",
            dificultad="facil",
            tutorial_messages=[
                "La MORAL es crucial en batalla",
                "Moral < 30: Unidad en PÁNICO (no puede actuar)",
                "Presiona 'F': Cambiar formación",
                "Testudo: +Defensa, +Moral",
                "Cuneus: +Ataque, +Moral",
                "¡La moral se recupera cada turno!"
            ],
            unidades_jugador=[
                # Formación mixta
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(7, 2)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(7, 4)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(8, 1)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(8, 5)),
            ],
            unidades_enemigo=[
                # Enemigos más fuertes
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(2, 4)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(1, 3)),
            ]
        )

    # ========== NIVELES INTERMEDIOS (4-6) ==========

    def _crear_nivel_4(self) -> Nivel:
        """Nivel 4: Caballería - Introducción a Equites"""
        return Nivel(
            numero=4,
            nombre="Alas de la Victoria",
            descripcion="Domina la caballería romana",
            objetivo="Usa la caballería para flanquear",
            dificultad="medio",
            tutorial_messages=[
                "Los EQUITES son tu caballería de élite",
                "Movimiento: 3 casillas + Alto ataque",
                "Perfectos para flanquear y atacar arqueros",
                "¡Usa su velocidad para golpear los flancos enemigos!"
            ],
            unidades_jugador=[
                # Caballería en los flancos
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(7, 0)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 4)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(7, 6)),
            ],
            unidades_enemigo=[
                # Línea defensiva con arqueros
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 4)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(1, 1)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(1, 5)),
            ]
        )

    def _crear_nivel_5(self) -> Nivel:
        """Nivel 5: Arqueros y Rango - Introducción a Sagittarii"""
        return Nivel(
            numero=5,
            nombre="Lluvia de Flechas",
            descripcion="Domina el combate a distancia",
            objetivo="Usa arqueros para debilitar al enemigo",
            dificultad="medio",
            tutorial_messages=[
                "Los SAGITTARII son tus arqueros de élite",
                "Rango de ataque: 3 casillas",
                "Bajo HP y defensa - mantén protegidos",
                "¡Ataca desde la retaguardia!",
                "Combina con infantería pesada al frente"
            ],
            unidades_jugador=[
                # Línea mixta con arqueros atrás
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 4)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(7, 1)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(7, 5)),
            ],
            unidades_enemigo=[
                # Horda bárbara
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 1)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 4)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 5)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(1, 0)),
            ]
        )

    def _crear_nivel_6(self) -> Nivel:
        """Nivel 6: Veteranos - Introducción a Triarii"""
        return Nivel(
            numero=6,
            nombre="Cuando Llegan los Triarii",
            descripcion="Los veteranos de élite entran en batalla",
            objetivo="Usa los Triarii contra caballería enemiga",
            dificultad="medio",
            tutorial_messages=[
                "Los TRIARII son la élite veterana",
                "Moral 100 - Nunca entran en pánico",
                "Bonus vs Caballería: +20 daño",
                "Proverbio romano: 'Ad Triarios redisse'",
                "(Cuando las cosas se ponen difíciles)"
            ],
            unidades_jugador=[
                # Triplex Acies clásica
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(6, 1)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 3)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(6, 5)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 2)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 4)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 2)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 3)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 4)),
            ],
            unidades_enemigo=[
                # Ataque de caballería pesada
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(2, 1)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(2, 4)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(2, 5)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(1, 0)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(1, 6)),
            ]
        )

    # ========== NIVELES AVANZADOS (7-9) ==========

    def _crear_nivel_7(self) -> Nivel:
        """Nivel 7: Batalla Campal"""
        return Nivel(
            numero=7,
            nombre="Batalla Campal",
            descripcion="Enfrenta un ejército completo",
            objetivo="Derrota al ejército enemigo completo",
            dificultad="dificil",
            tutorial_messages=[
                "¡Batalla a gran escala!",
                "Coordina todas tus unidades",
                "Usa formaciones estratégicamente",
                "Protege tus arqueros",
                "¡Victoria o muerte!"
            ],
            unidades_jugador=[
                # Ejército completo
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(6, 1)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 4)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(6, 5)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 2)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 4)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 2)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 3)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 4)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(7, 0)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(7, 6)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(8, 1)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(8, 5)),
            ],
            unidades_enemigo=[
                # Horda bárbara masiva
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 1)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(2, 4)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 5)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(1, 2)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(1, 3)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(1, 4)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(1, 0)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(1, 6)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(0, 2)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(0, 3)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(0, 4)),
            ]
        )

    def _crear_nivel_8(self) -> Nivel:
        """Nivel 8: Defensa Desesperada"""
        return Nivel(
            numero=8,
            nombre="El Último Bastión",
            descripcion="Defiende contra oleadas enemigas",
            objetivo="Sobrevive y contraataca",
            dificultad="dificil",
            tutorial_messages=[
                "¡Estás rodeado!",
                "Usa la formación Orbis (circular)",
                "Los enemigos son superiores en número",
                "Mantén alta la moral de tus tropas",
                "¡Roma no cae este día!"
            ],
            unidades_jugador=[
                # Formación defensiva compacta
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(5, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 4)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(7, 2)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(7, 4)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(7, 1)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(7, 5)),
            ],
            unidades_enemigo=[
                # Rodeando al jugador
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(3, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(3, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(3, 4)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(4, 1)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(4, 5)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(2, 0)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(2, 6)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(5, 1)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(5, 5)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(2, 4)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(3, 1)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(3, 5)),
            ]
        )

    def _crear_nivel_9(self) -> Nivel:
        """Nivel 9: El Desafío Final"""
        return Nivel(
            numero=9,
            nombre="Gloria Immortalis",
            descripcion="La batalla definitiva por la gloria de Roma",
            objetivo="Demuestra tu maestría táctica",
            dificultad="dificil",
            tutorial_messages=[
                "¡La batalla final!",
                "El enemigo es numeroso y experimentado",
                "Usa todas las tácticas que aprendiste",
                "Combina formaciones, flanqueos y moral",
                "¡POR LA GLORIA ETERNA DE ROMA!",
                "ROMA INVICTA!"
            ],
            unidades_jugador=[
                # Ejército de élite
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(6, 1)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 4)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(6, 5)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 2)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 4)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 2)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 3)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 4)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(7, 0)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(7, 6)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(8, 1)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(8, 5)),
            ],
            unidades_enemigo=[
                # Ejército enemigo masivo y balanceado
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 1)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(2, 4)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(2, 5)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(1, 2)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(1, 3)),
                ConfiguracionUnidad(TipoUnidad.LEGIONARIO, Posicion(1, 4)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(1, 0)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(1, 6)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(0, 2)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(0, 3)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(0, 4)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(0, 1)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(0, 5)),
            ]
        )
