# programmatic_simulator/backend/data/market_data.py

MARCAS_COLOMBIANAS = [
    {"id": "marca_001", "nombre": "Bancolombia", "categoria": "Finanzas"},
    {"id": "marca_002", "nombre": "Ecopetrol", "categoria": "Energía"},
    {"id": "marca_003", "nombre": "Alpina", "categoria": "Alimentos y Bebidas"},
    {"id": "marca_004", "nombre": "Avianca", "categoria": "Transporte"},
    {"id": "marca_005", "nombre": "Postobón", "categoria": "Alimentos y Bebidas"},
]

AUDIENCIAS_COLOMBIANAS = [
    {
        "id": "aud_001",
        "nombre": "Jóvenes Universitarios (18-24)",
        "descripcion": "Estudiantes de pregrado interesados en tecnología, entretenimiento y viajes.",
        "intereses_clave": ["tecnologia", "videojuegos", "musica", "viajes", "redes_sociales"],
        "afinidad_marca_categoria": { # Afinidad base de esta audiencia con categorías de marcas (0-1)
            "Finanzas": 0.3,
            "Energía": 0.1,
            "Alimentos y Bebidas": 0.7,
            "Transporte": 0.6,
            "Tecnología": 0.8
        }
    },
    {
        "id": "aud_002",
        "nombre": "Profesionales Jóvenes (25-34)",
        "descripcion": "Profesionales iniciando su carrera, interesados en desarrollo profesional, finanzas personales y estilo de vida.",
        "intereses_clave": ["desarrollo_profesional", "inversiones", "viajes_negocios", "restaurantes", "fitness"],
        "afinidad_marca_categoria": {
            "Finanzas": 0.7,
            "Energía": 0.2,
            "Alimentos y Bebidas": 0.5,
            "Transporte": 0.5,
            "Tecnología": 0.6
        }
    },
    {
        "id": "aud_003",
        "nombre": "Amantes de la Tecnología (20-45)",
        "descripcion": "Personas con alto interés en gadgets, software y nuevas tecnologías.",
        "intereses_clave": ["gadgets", "software", "ia", "videojuegos_pc", "ecommerce_tecnologia"],
        "afinidad_marca_categoria": {
            "Finanzas": 0.4,
            "Energía": 0.3,
            "Alimentos y Bebidas": 0.2,
            "Transporte": 0.3,
            "Tecnología": 0.9 # Afinidad alta con marcas de tecnología, que no están en la lista de marcas aún
        }
    },
    {
        "id": "aud_004",
        "nombre": "Familias con Hijos Pequeños (30-45)",
        "descripcion": "Padres de familia interesados en productos y servicios para niños, hogar y entretenimiento familiar.",
        "intereses_clave": ["productos_infantiles", "educacion", "viajes_familiares", "seguros_hogar", "alimentacion_saludable"],
        "afinidad_marca_categoria": {
            "Finanzas": 0.6, # Seguros, créditos educativos
            "Energía": 0.1,
            "Alimentos y Bebidas": 0.8,
            "Transporte": 0.4, # Vehículos familiares, viajes
            "Tecnología": 0.4
        }
    },
    {
        "id": "aud_005",
        "nombre": "Adultos Mayores Activos (60+)",
        "descripcion": "Personas jubiladas o cerca de la jubilación, interesadas en salud, viajes de placer y finanzas para el retiro.",
        "intereses_clave": ["salud_bienestar", "viajes_culturales", "seguros_medicos", "inversiones_retiro", "hobbies"],
        "afinidad_marca_categoria": {
            "Finanzas": 0.8,
            "Energía": 0.1,
            "Alimentos y Bebidas": 0.6,
            "Transporte": 0.7,
            "Tecnología": 0.2
        }
    }
]

# Podríamos añadir más parámetros aquí en el futuro, como:
# - CANALES_DISPONIBLES (Display, Video, Social, Search)
# - FORMATOS_ANUNCIO_POR_CANAL
# - COSTOS_BASE_CPM_POR_CANAL_AUDIENCIA
# - MODIFICADORES_CONTEXTO (Noticias, Entretenimiento, Deportes, etc.)
# - EVENTOS_ESPECIALES_COLOMBIA (Amor y Amistad, Navidad, Black Friday Colombia)

def obtener_marca_por_id(marca_id):
    for marca in MARCAS_COLOMBIANAS:
        if marca["id"] == marca_id:
            return marca
    return None

def obtener_audiencia_por_id(audiencia_id):
    for audiencia in AUDIENCIAS_COLOMBIANAS:
        if audiencia["id"] == audiencia_id:
            return audiencia
    return None
