"""
Campaña "César en la Galia" - 9 Capítulos Históricos
Basada en las Guerras Gálicas (58-50 a.C.) de Julio César
Roma vs Vercingétorix y las tribus galas
"""

from dataclasses import dataclass
from typing import List, Optional
from src.domain.value_objects import TipoUnidad, Posicion, Bando
from src.domain.levels import ConfiguracionUnidad, Nivel


@dataclass
class ObjetivoEspecial:
    """Objetivos especiales para batallas históricas"""
    tipo: str  # "defender_posicion", "eliminar_lider", "sobrevivir_turnos", "capturar_zona"
    descripcion: str
    parametros: dict


class CampaniaCesarGalia:
    """
    Campaña histórica César en la Galia (58-50 a.C.)

    9 Capítulos siguiendo la conquista de la Galia por Julio César
    culminando en la épica batalla de Alesia
    """

    def __init__(self):
        self.niveles = self._crear_campania_galia()
        self.nivel_actual = 0
        self.niveles_completados = set()
        self.estadisticas = {
            "batallas_ganadas": 0,
            "batallas_perdidas": 0,
            "unidades_galas_eliminadas": 0,
            "tiempo_total_jugado": 0,
            "uso_formaciones": 0
        }

    def obtener_nivel(self, numero: int) -> Optional[Nivel]:
        """Obtiene un nivel por su número (1-9)"""
        if 0 < numero <= len(self.niveles):
            return self.niveles[numero - 1]
        return None

    def obtener_nivel_actual(self) -> Nivel:
        """Obtiene el nivel actual"""
        return self.niveles[self.nivel_actual]

    def avanzar_nivel(self):
        """Avanza al siguiente capítulo"""
        self.niveles_completados.add(self.nivel_actual)
        if self.nivel_actual < len(self.niveles) - 1:
            self.nivel_actual += 1

    def seleccionar_nivel(self, numero_nivel: int) -> bool:
        """
        Selecciona un nivel específico si está desbloqueado

        Args:
            numero_nivel: Número del nivel (1-9)

        Returns:
            True si se pudo seleccionar, False si está bloqueado
        """
        # Convertir de número (1-9) a índice (0-8)
        indice = numero_nivel - 1

        # Verificar que el nivel existe
        if indice < 0 or indice >= len(self.niveles):
            return False

        # Primer nivel siempre está desbloqueado
        if indice == 0:
            self.nivel_actual = indice
            return True

        # Resto requiere haber completado el anterior
        if (indice - 1) in self.niveles_completados:
            self.nivel_actual = indice
            return True

        return False

    def reiniciar_campania(self):
        """Reinicia la campaña desde el principio"""
        self.nivel_actual = 0
        self.niveles_completados.clear()

    def registrar_victoria(self):
        """Registra una victoria en las estadísticas"""
        self.estadisticas["batallas_ganadas"] += 1

    def registrar_derrota(self):
        """Registra una derrota en las estadísticas"""
        self.estadisticas["batallas_perdidas"] += 1

    def registrar_unidad_eliminada(self):
        """Registra una unidad gala eliminada en las estadísticas"""
        self.estadisticas["unidades_galas_eliminadas"] += 1

    @property
    def progreso_campania(self) -> float:
        """Progreso de la campaña (0.0 a 1.0)"""
        return len(self.niveles_completados) / len(self.niveles)

    def _crear_campania_galia(self) -> List[Nivel]:
        """Crea los 9 capítulos históricos de la conquista de la Galia"""
        return [
            self._capitulo_1_bibracte(),
            self._capitulo_2_ariovisto(),
            self._capitulo_3_belgae(),
            self._capitulo_4_venetii(),
            self._capitulo_5_britannia(),
            self._capitulo_6_avaricum(),
            self._capitulo_7_gergovia(),
            self._capitulo_8_vingetorix_rebelion(),
            self._capitulo_9_alesia(),
        ]

    # ========== CAPÍTULO 1: BIBRACTE (58 a.C.) ==========

    def _capitulo_1_bibracte(self) -> Nivel:
        """
        Capítulo 1: Batalla de Bibracte (58 a.C.)

        Primera gran batalla de César en la Galia contra los Helvecios
        que migraban hacia el oeste. César los intercepta y derrota.
        """
        return Nivel(
            numero=1,
            nombre="Bibracte - La Primera Prueba",
            descripcion="58 a.C. - Los Helvecios migran hacia el oeste. César los intercepta.",
            objetivo="Derrota a los guerreros Helvecios y detén su migración",
            dificultad="facil",
            tutorial_messages=[
                "¡Bienvenido a la Guerra de las Galias!",
                "Eres Julio César, enfrentando a los Helvecios",
                "Los galos son agresivos pero poco disciplinados",
                "Usa la disciplina romana a tu favor",
                "¡Demuestra la superioridad de las legiones!"
            ],
            unidades_jugador=[
                # Legión romana clásica
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(7, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(7, 4)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(8, 2)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(8, 4)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(6, 1)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(6, 5)),
            ],
            unidades_enemigo=[
                # Guerreros tribales galos
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(2, 4)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 2)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 4)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(0, 1)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(0, 5)),
            ]
        )

    # ========== CAPÍTULO 2: ARIOVISTO (58 a.C.) ==========

    def _capitulo_2_ariovisto(self) -> Nivel:
        """
        Capítulo 2: Batalla contra Ariovisto (58 a.C.)

        Derrota del rey germano Ariovisto y sus guerreros.
        Primera confrontación con caballería pesada.
        """
        return Nivel(
            numero=2,
            nombre="Ariovisto - Rey Germano",
            descripcion="58 a.C. - El rey germano Ariovisto amenaza la Galia",
            objetivo="Derrota a Ariovisto y su caballería germana",
            dificultad="facil",
            tutorial_messages=[
                "Ariovisto comanda guerreros germanos y galos",
                "Su caballería es peligrosa",
                "Usa tus Velites para hostigar",
                "Mantén formación contra la carga",
                "¡La disciplina vencerá a la furia!"
            ],
            unidades_jugador=[
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 4)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(7, 1)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(7, 5)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(8, 2)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(8, 4)),
            ],
            unidades_enemigo=[
                # Mezcla germano-gala
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(2, 4)),
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(1, 3)),  # Guardia de Ariovisto
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_BARBARA, Posicion(2, 0)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_BARBARA, Posicion(2, 6)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(1, 1)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(1, 5)),
            ]
        )

    # ========== CAPÍTULO 3: NERVIOS BELGAE (57 a.C.) ==========

    def _capitulo_3_belgae(self) -> Nivel:
        """
        Capítulo 3: Guerra contra los Belgae (57 a.C.)

        Los Belgae, las tribus más feroces de la Galia, atacan.
        Primera aparición de los Fanáticos Desnudos (Gaesatae).
        """
        return Nivel(
            numero=3,
            nombre="Belgae - Los Más Bravos",
            descripcion="57 a.C. - Los feroces Belgae declaran la guerra",
            objetivo="Sobrevive a la carga de los Fanáticos y derrota a los Belgae",
            dificultad="medio",
            tutorial_messages=[
                "¡Los Belgae son los más bravos de la Galia!",
                "FANÁTICOS DESNUDOS: Ataque 40 pero Defensa 2",
                "Extremadamente peligrosos en la primera carga",
                "Usa arqueros para eliminarlos a distancia",
                "¡No dejes que lleguen a tu línea!"
            ],
            unidades_jugador=[
                # Defensa romana contra carga
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 4)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 2)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 4)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 3)),  # Reserva
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(7, 1)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(7, 5)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(8, 0)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(8, 6)),
            ],
            unidades_enemigo=[
                # Carga belga con fanáticos
                ConfiguracionUnidad(TipoUnidad.FANATICOS_DESNUDOS, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.FANATICOS_DESNUDOS, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.FANATICOS_DESNUDOS, Posicion(2, 4)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 1)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 3)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 5)),
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(0, 3)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_BARBARA, Posicion(1, 0)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_BARBARA, Posicion(1, 6)),
            ]
        )

    # ========== CAPÍTULO 4: VENETII (56 a.C.) ==========

    def _capitulo_4_venetii(self) -> Nivel:
        """
        Capítulo 4: Guerra contra los Venetii (56 a.C.)

        Tribu marítima con aliados britanos.
        Aparecen los Carros de Guerra.
        """
        return Nivel(
            numero=4,
            nombre="Venetii - Guerra Naval y Terrestre",
            descripcion="56 a.C. - Los Venetii y sus aliados britanos se rebelan",
            objetivo="Derrota a los Venetii y sus temibles Carros de Guerra",
            dificultad="medio",
            tutorial_messages=[
                "Los Venetii han traído aliados britanos",
                "CARROS DE GUERRA: Rápidos (Mov 4) y poderosos",
                "Pueden romper formaciones",
                "Usa piqueros (Triarii) para detenerlos",
                "¡Coordina infantería y caballería!"
            ],
            unidades_jugador=[
                # Legión reforzada
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(6, 1)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 4)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(6, 5)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 2)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 4)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 2)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 4)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(7, 0)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(7, 6)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(8, 3)),
            ],
            unidades_enemigo=[
                # Venetii + aliados britanos
                ConfiguracionUnidad(TipoUnidad.CARROS_GUERRA, Posicion(2, 1)),
                ConfiguracionUnidad(TipoUnidad.CARROS_GUERRA, Posicion(2, 5)),
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 2)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 4)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_BARBARA, Posicion(1, 0)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_BARBARA, Posicion(1, 6)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(0, 1)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(0, 3)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(0, 5)),
            ]
        )

    # ========== CAPÍTULO 5: PRIMERA INVASIÓN DE BRITANIA (55 a.C.) ==========

    def _capitulo_5_britannia(self) -> Nivel:
        """
        Capítulo 5: Primera invasión de Britania (55 a.C.)

        César cruza el canal y se enfrenta a los britanos.
        Batalla con muchos carros de guerra y caballería.
        """
        return Nivel(
            numero=5,
            nombre="Britania - Más Allá del Océano",
            descripcion="55 a.C. - César cruza al misterioso Norte",
            objetivo="Establece una cabeza de playa en Britania",
            dificultad="medio",
            tutorial_messages=[
                "¡Primer romano en pisar Britania!",
                "Los britanos confían en carros y caballería",
                "Terreno desconocido y enemigo agresivo",
                "Mantén la cohesión de tus unidades",
                "¡Gloria eterna te espera!"
            ],
            unidades_jugador=[
                # Fuerza expedicionaria
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(7, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(7, 4)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(8, 2)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(8, 4)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 3)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(6, 1)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(6, 5)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(7, 1)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(7, 5)),
            ],
            unidades_enemigo=[
                # Ejército britano
                ConfiguracionUnidad(TipoUnidad.CARROS_GUERRA, Posicion(2, 0)),
                ConfiguracionUnidad(TipoUnidad.CARROS_GUERRA, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.CARROS_GUERRA, Posicion(2, 6)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 2)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 4)),
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(0, 3)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_BARBARA, Posicion(1, 1)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_BARBARA, Posicion(1, 5)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(0, 0)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(0, 6)),
            ]
        )

    # ========== CAPÍTULO 6: AVARICUM (52 a.C.) ==========

    def _capitulo_6_avaricum(self) -> Nivel:
        """
        Capítulo 6: Asedio de Avaricum (52 a.C.)

        Primera batalla de la Gran Rebelión de Vercingétorix.
        Asalto final a la ciudad fortificada gala.
        """
        return Nivel(
            numero=6,
            nombre="Avaricum - La Ciudad Fortificada",
            descripcion="52 a.C. - Vercingétorix se alza. Asedio de Avaricum",
            objetivo="Conquista las defensas de Avaricum",
            dificultad="dificil",
            tutorial_messages=[
                "¡Vercingétorix lidera la rebelión gala!",
                "Avaricum es una ciudad fuertemente defendida",
                "Los galos lucharán con ferocidad",
                "Combina todas tus tácticas",
                "¡El asedio final comienza!"
            ],
            unidades_jugador=[
                # Fuerza de asalto romana
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(6, 4)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 1)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(7, 5)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 2)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(8, 4)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(7, 0)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(7, 6)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(8, 1)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(8, 3)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(8, 5)),
            ],
            unidades_enemigo=[
                # Defensores galos de élite
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(2, 4)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 1)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 3)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 5)),
                ConfiguracionUnidad(TipoUnidad.FANATICOS_DESNUDOS, Posicion(0, 2)),
                ConfiguracionUnidad(TipoUnidad.FANATICOS_DESNUDOS, Posicion(0, 4)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(0, 0)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(0, 6)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_NOBLE, Posicion(1, 0)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_NOBLE, Posicion(1, 6)),
            ]
        )

    # ========== CAPÍTULO 7: GERGOVIA (52 a.C.) ==========

    def _capitulo_7_gergovia(self) -> Nivel:
        """
        Capítulo 7: Batalla de Gergovia (52 a.C.)

        ¡La única derrota de César en la Galia!
        Batalla defensiva donde debes retirarte con honor.
        """
        return Nivel(
            numero=7,
            nombre="Gergovia - El Revés de César",
            descripcion="52 a.C. - Ataque fallido. ¡Debes retirarte con honor!",
            objetivo="Sobrevive y retira tus legiones ordenadamente",
            dificultad="dificil",
            tutorial_messages=[
                "¡El ataque a Gergovia ha fallado!",
                "Vercingétorix contraataca con furia",
                "Tu objetivo: SOBREVIVIR y retirarte",
                "Mantén la disciplina romana",
                "¡Una retirada ordenada es también una victoria!"
            ],
            unidades_jugador=[
                # Legión en retirada (posición central/defensiva)
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(5, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(5, 4)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(6, 2)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(6, 3)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(6, 4)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(7, 2)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(7, 4)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(6, 0)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(6, 6)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(7, 1)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(7, 5)),
            ],
            unidades_enemigo=[
                # Ejército galo en pleno contraataque
                ConfiguracionUnidad(TipoUnidad.FANATICOS_DESNUDOS, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.FANATICOS_DESNUDOS, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.FANATICOS_DESNUDOS, Posicion(2, 4)),
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(1, 2)),
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(1, 4)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 1)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 5)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_NOBLE, Posicion(2, 0)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_NOBLE, Posicion(2, 6)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_BARBARA, Posicion(1, 0)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_BARBARA, Posicion(1, 6)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(0, 1)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(0, 3)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(0, 5)),
            ]
        )

    # ========== CAPÍTULO 8: LA GRAN REBELIÓN (52 a.C.) ==========

    def _capitulo_8_vingetorix_rebelion(self) -> Nivel:
        """
        Capítulo 8: La Gran Rebelión de Vercingétorix (52 a.C.)

        Vercingétorix une todas las tribus galas.
        Batalla previa a Alesia con ejército galo completo.
        """
        return Nivel(
            numero=8,
            nombre="La Gran Rebelión - Galia Unida",
            descripcion="52 a.C. - Todas las tribus galas se unen bajo Vercingétorix",
            objetivo="Derrota al ejército unificado de Vercingétorix",
            dificultad="dificil",
            tutorial_messages=[
                "¡TODA la Galia se ha levantado!",
                "Vercingétorix comanda un ejército masivo",
                "Todas las unidades galas están presentes",
                "Esta es la batalla decisiva",
                "¡Demuestra por qué Roma es invencible!"
            ],
            unidades_jugador=[
                # Ejército romano completo
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
                # EJÉRCITO COMPLETO GALO
                ConfiguracionUnidad(TipoUnidad.FANATICOS_DESNUDOS, Posicion(2, 2)),
                ConfiguracionUnidad(TipoUnidad.FANATICOS_DESNUDOS, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.FANATICOS_DESNUDOS, Posicion(2, 4)),
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(1, 2)),
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(1, 3)),
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(1, 4)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(0, 2)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(0, 4)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_NOBLE, Posicion(2, 0)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_NOBLE, Posicion(2, 6)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_BARBARA, Posicion(1, 0)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_BARBARA, Posicion(1, 6)),
                ConfiguracionUnidad(TipoUnidad.CARROS_GUERRA, Posicion(0, 0)),
                ConfiguracionUnidad(TipoUnidad.CARROS_GUERRA, Posicion(0, 6)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(0, 1)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(0, 5)),
            ]
        )

    # ========== CAPÍTULO 9: ALESIA (52 a.C.) ==========

    def _capitulo_9_alesia(self) -> Nivel:
        """
        Capítulo 9: Asedio de Alesia (52 a.C.)

        ¡LA BATALLA ÉPICA FINAL!
        César asedia a Vercingétorix en Alesia con doble muralla.
        Debes defender contra ataques desde dentro Y fuera.

        Mecánica especial: Defensa de doble muralla
        """
        return Nivel(
            numero=9,
            nombre="ALESIA - El Destino de la Galia",
            descripcion="52 a.C. - ¡La batalla que decidirá el futuro de la Galia!",
            objetivo="Resiste el doble asalto galo y conquista Alesia",
            dificultad="dificil",
            tutorial_messages=[
                "¡ALESIA - La batalla más épica de la historia!",
                "César ha construido DOBLE MURALLA",
                "Muralla interior: asedia a Vercingétorix",
                "Muralla exterior: contra ejército de rescate",
                "¡Defiende en DOS FRENTES simultáneos!",
                "Esta batalla cambiará la historia",
                "¡POR ROMA! ¡POR CÉSAR! ¡POR LA GLORIA ETERNA!"
            ],
            unidades_jugador=[
                # Legiones de César en posición defensiva central
                # Simula estar entre dos murallas
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(5, 2)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(5, 3)),
                ConfiguracionUnidad(TipoUnidad.HASTATI, Posicion(5, 4)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(6, 1)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(6, 3)),
                ConfiguracionUnidad(TipoUnidad.PRINCEPS, Posicion(6, 5)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(7, 2)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(7, 3)),
                ConfiguracionUnidad(TipoUnidad.TRIARII, Posicion(7, 4)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(6, 0)),
                ConfiguracionUnidad(TipoUnidad.EQUITES, Posicion(6, 6)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(7, 1)),
                ConfiguracionUnidad(TipoUnidad.SAGITTARII, Posicion(7, 5)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(5, 0)),
                ConfiguracionUnidad(TipoUnidad.VELITES, Posicion(5, 6)),
            ],
            unidades_enemigo=[
                # DOBLE ATAQUE GALO
                # Grupo 1: Vercingétorix desde Alesia (Norte)
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(2, 2)),  # Vercingétorix
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(2, 3)),
                ConfiguracionUnidad(TipoUnidad.ESPADAS_ELEGIDAS, Posicion(2, 4)),
                ConfiguracionUnidad(TipoUnidad.FANATICOS_DESNUDOS, Posicion(1, 2)),
                ConfiguracionUnidad(TipoUnidad.FANATICOS_DESNUDOS, Posicion(1, 4)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 1)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(1, 5)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_NOBLE, Posicion(0, 3)),

                # Grupo 2: Ejército de rescate (Sur/Flancos)
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(8, 2)),
                ConfiguracionUnidad(TipoUnidad.GUERRERO_TRIBAL, Posicion(8, 4)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_NOBLE, Posicion(8, 0)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_NOBLE, Posicion(8, 6)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_BARBARA, Posicion(7, 0)),
                ConfiguracionUnidad(TipoUnidad.CABALLERIA_BARBARA, Posicion(7, 6)),
                ConfiguracionUnidad(TipoUnidad.CARROS_GUERRA, Posicion(8, 1)),
                ConfiguracionUnidad(TipoUnidad.CARROS_GUERRA, Posicion(8, 5)),
                ConfiguracionUnidad(TipoUnidad.ESCARAMUZADORES, Posicion(8, 3)),
            ]
        )

    def to_dict(self) -> dict:
        """Serializa la campaña para guardado"""
        return {
            "tipo_campania": "cesar_galia",
            "nivel_actual": self.nivel_actual,
            "niveles_completados": list(self.niveles_completados),
            "progreso": self.progreso_campania,
            "estadisticas": self.estadisticas.copy()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CampaniaCesarGalia':
        """Carga campaña desde diccionario"""
        campania = cls()
        campania.nivel_actual = data.get("nivel_actual", 0)
        campania.niveles_completados = set(data.get("niveles_completados", []))
        campania.estadisticas = data.get("estadisticas", {
            "batallas_ganadas": 0,
            "batallas_perdidas": 0,
            "unidades_galas_eliminadas": 0,
            "tiempo_total_jugado": 0,
            "uso_formaciones": 0
        })
        return campania
