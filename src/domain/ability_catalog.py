"""
Ability catalog for all unit types
Defines which abilities each unit type has access to
"""

from src.domain.abilities import HabilidadActiva, HabilidadPasiva
from src.domain.value_objects import TipoUnidad


# Define all available abilities
CATALOGO_HABILIDADES_ACTIVAS = {
    # General abilities
    "reagrupar": HabilidadActiva(
        nombre="Reagrupar",
        descripcion="+10 MOR unidades rango 2, +5 Moral General",
        cooldown_maximo=3,
        rango=2
    ),
    "a_la_carga": HabilidadActiva(
        nombre="¡A la carga!",
        descripcion="+3 ATQ aliados en rango 3 por 1 turno",
        cooldown_maximo=4,
        rango=3
    ),
    "mantened_linea": HabilidadActiva(
        nombre="¡Mantened la línea!",
        descripcion="+2 DEF rango 2 por 2 turnos",
        cooldown_maximo=5,
        rango=2
    ),

    # Infantry abilities
    "disciplina_romana": HabilidadActiva(
        nombre="Disciplina Romana",
        descripcion="Recupera a 7 MOR si está bajo 5",
        cooldown_maximo=999,  # Once per battle
        usos_maximos=1
    ),
    "pila": HabilidadActiva(
        nombre="Lanzamiento de Pila",
        descripcion="Ataque a distancia 2 antes del combate",
        cooldown_maximo=3,
        rango=2
    ),
    "empuje_escudo": HabilidadActiva(
        nombre="Empuje de Escudo",
        descripcion="Empuja al enemigo 1 casilla hacia atrás",
        cooldown_maximo=2,
        rango=1
    ),
    "ultima_linea": HabilidadActiva(
        nombre="Última Línea",
        descripcion="+4 DEF, +2 ATQ cuando moral < 30",
        cooldown_maximo=999,
        usos_maximos=1
    ),

    # Cavalry abilities
    "impacto_demoledor": HabilidadActiva(
        nombre="Impacto Demoledor",
        descripcion="50% aturdir enemigo (pierde turno)",
        cooldown_maximo=2,
        rango=1
    ),
    "carga_devastadora": HabilidadActiva(
        nombre="Carga Devastadora",
        descripcion="+5 ATQ si se movió 2+ casillas",
        cooldown_maximo=3
    ),

    # Archer abilities
    "lluvia_flechas": HabilidadActiva(
        nombre="Lluvia de Flechas",
        descripcion="Ataca línea de 3 casillas con ATQ-1",
        cooldown_maximo=2,
        rango=5
    ),
    "disparo_preciso": HabilidadActiva(
        nombre="Disparo Preciso",
        descripcion="Ignora DEF del objetivo",
        cooldown_maximo=3,
        rango=3
    ),
    "fuego_supresivo": HabilidadActiva(
        nombre="Fuego Supresivo",
        descripcion="-2 MOV enemigos en rango 3",
        cooldown_maximo=4,
        rango=3
    ),

    # Skirmisher abilities
    "escaramuza": HabilidadActiva(
        nombre="Escaramuza",
        descripcion="Ataca y retrocede 1 casilla",
        cooldown_maximo=2
    ),
    "movimiento_agil": HabilidadActiva(
        nombre="Movimiento Ágil",
        descripcion="+2 MOV este turno",
        cooldown_maximo=3
    ),
}


CATALOGO_HABILIDADES_PASIVAS = {
    # Infantry passives
    "gladius_hispaniensis": HabilidadPasiva(
        nombre="Gladius Hispaniensis",
        descripcion="+2 ATQ contra unidades con DEF 5+",
        modificadores={}  # Conditional modifier
    ),
    "veterano": HabilidadPasiva(
        nombre="Veterano",
        descripcion="+1 ATQ, +1 DEF",
        modificadores={"ataque": 1, "defensa": 1}
    ),
    "muro_escudos": HabilidadPasiva(
        nombre="Muro de Escudos",
        descripcion="3+ unidades en línea: +3 DEF",
        modificadores={}  # Conditional modifier
    ),
    "formacion_tortuga": HabilidadPasiva(
        nombre="Formación Tortuga",
        descripcion="+4 DEF contra ataques a distancia",
        modificadores={}  # Conditional modifier
    ),

    # Cavalry passives
    "carga": HabilidadPasiva(
        nombre="Carga",
        descripcion="Puede mover y atacar. Si mueve 2+: +3 ATQ",
        modificadores={}  # Special rules
    ),
    "movilidad_superior": HabilidadPasiva(
        nombre="Movilidad Superior",
        descripcion="+1 MOV",
        modificadores={"movimiento": 1}
    ),

    # Archer passives
    "ataque_distancia": HabilidadPasiva(
        nombre="Ataque a Distancia",
        descripcion="Puede atacar a rango 2-5",
        modificadores={}  # Already in base stats
    ),
    "ojo_aguila": HabilidadPasiva(
        nombre="Ojo de Águila",
        descripcion="+1 rango de ataque",
        modificadores={"rango_ataque": 1}
    ),

    # Light infantry passives
    "movimiento_ligero": HabilidadPasiva(
        nombre="Movimiento Ligero",
        descripcion="Ignora penalización de terreno",
        modificadores={}  # Special rules
    ),
    "esquiva": HabilidadPasiva(
        nombre="Esquiva",
        descripcion="20% probabilidad de evitar daño",
        modificadores={}  # Special calculation
    ),
}


# Map abilities to unit types
HABILIDADES_POR_TIPO = {
    TipoUnidad.LEGIONARIO: {
        "activas": ["disciplina_romana", "empuje_escudo"],
        "pasivas": ["gladius_hispaniensis", "veterano"]
    },
    TipoUnidad.HASTATI: {
        "activas": ["pila", "empuje_escudo"],
        "pasivas": ["muro_escudos"]
    },
    TipoUnidad.PRINCEPS: {
        "activas": ["disciplina_romana", "mantened_linea"],
        "pasivas": ["veterano", "muro_escudos"]
    },
    TipoUnidad.TRIARII: {
        "activas": ["ultima_linea", "mantened_linea"],
        "pasivas": ["veterano", "formacion_tortuga"]
    },
    TipoUnidad.EQUITES: {
        "activas": ["impacto_demoledor", "carga_devastadora"],
        "pasivas": ["carga", "movilidad_superior"]
    },
    TipoUnidad.VELITES: {
        "activas": ["escaramuza", "movimiento_agil"],
        "pasivas": ["movimiento_ligero", "esquiva"]
    },
    TipoUnidad.SAGITTARII: {
        "activas": ["lluvia_flechas", "disparo_preciso"],
        "pasivas": ["ataque_distancia", "ojo_aguila"]
    },

    # Gallic units
    TipoUnidad.GUERRERO_TRIBAL: {
        "activas": ["a_la_carga"],
        "pasivas": []
    },
    TipoUnidad.ESPADAS_ELEGIDAS: {
        "activas": ["mantened_linea", "disciplina_romana"],
        "pasivas": ["veterano"]
    },
    TipoUnidad.FANATICOS_DESNUDOS: {
        "activas": ["a_la_carga"],
        "pasivas": ["esquiva"]  # Ironically hard to hit
    },
    TipoUnidad.ESCARAMUZADORES: {
        "activas": ["escaramuza", "movimiento_agil"],
        "pasivas": ["movimiento_ligero"]
    },
    TipoUnidad.CABALLERIA_BARBARA: {
        "activas": ["carga_devastadora"],
        "pasivas": ["carga", "movilidad_superior"]
    },
    TipoUnidad.CABALLERIA_NOBLE: {
        "activas": ["impacto_demoledor", "carga_devastadora"],
        "pasivas": ["carga", "veterano"]
    },
    TipoUnidad.CARROS_GUERRA: {
        "activas": ["impacto_demoledor"],
        "pasivas": ["movilidad_superior"]
    },
    TipoUnidad.GENERAL: {
        "activas": ["reagrupar", "a_la_carga"],  # General gets 2 powerful command abilities
        "pasivas": ["veterano"]  # Experienced leader
    },
}


def obtener_habilidades_para_tipo(tipo: TipoUnidad) -> tuple[list[HabilidadActiva], list[HabilidadPasiva]]:
    """Get abilities for a unit type"""
    if tipo not in HABILIDADES_POR_TIPO:
        return [], []

    config = HABILIDADES_POR_TIPO[tipo]
    activas = []
    pasivas = []

    # Get active abilities
    for nombre_hab in config.get("activas", []):
        if nombre_hab in CATALOGO_HABILIDADES_ACTIVAS:
            # Create a copy so each unit has its own cooldown tracking
            hab_original = CATALOGO_HABILIDADES_ACTIVAS[nombre_hab]
            hab_copia = HabilidadActiva(
                nombre=hab_original.nombre,
                descripcion=hab_original.descripcion,
                cooldown_maximo=hab_original.cooldown_maximo,
                cooldown_actual=0,
                usos_maximos=hab_original.usos_maximos,
                usos_restantes=hab_original.usos_restantes,
                rango=hab_original.rango
            )
            activas.append(hab_copia)

    # Get passive abilities
    for nombre_hab in config.get("pasivas", []):
        if nombre_hab in CATALOGO_HABILIDADES_PASIVAS:
            pasivas.append(CATALOGO_HABILIDADES_PASIVAS[nombre_hab])

    return activas, pasivas