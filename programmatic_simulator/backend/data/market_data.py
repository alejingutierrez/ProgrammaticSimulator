# programmatic_simulator/backend/data/market_data.py

MARCAS_COLOMBIANAS = [
    {"id": "marca_001", "nombre": "Bancolombia", "categoria": "Banca", "productos": ["Cuenta de Ahorros", "Tarjeta de Crédito Gold", "Crédito Hipotecario"]},
    {"id": "marca_002", "nombre": "Ecopetrol", "categoria": "Energía", "productos": ["Gasolina Corriente", "ACPM", "Petroquímicos"]},
    {"id": "marca_003", "nombre": "Alpina", "categoria": "CPG", "productos": ["Leche Entera", "Yogurt Finesse", "Arequipe"]},
    {"id": "marca_004", "nombre": "Avianca", "categoria": "Airlines", "productos": ["Tiquetes Nacionales", "Tiquetes Internacionales", "Programa LifeMiles"]},
    {"id": "marca_005", "nombre": "Postobón", "categoria": "CPG", "productos": ["Gaseosa Manzana", "Agua Cristal", "Jugo Hit"]},
    {"id": "marca_006", "nombre": "Éxito", "categoria": "Retail", "productos": ["Mercado Básico", "Electrodomésticos", "Ropa Casual"]},
    {"id": "marca_007", "nombre": "Claro", "categoria": "Telecom", "productos": ["Plan Pospago 5G", "Internet Fibra Óptica", "Claro Video"]},
    {"id": "marca_008", "nombre": "Davivienda", "categoria": "Banca", "productos": ["Cuenta Móvil", "Tarjeta de Crédito Diners", "Seguro de Vida"]},
    {"id": "marca_009", "nombre": "Nutresa", "categoria": "CPG", "productos": ["Chocolatinas Jet", "Galletas Noel", "Café Sello Rojo"]},
    {"id": "marca_010", "nombre": "LATAM Airlines", "categoria": "Airlines", "productos": ["Vuelos a Suramérica", "Paquetes Turísticos", "Transporte de Carga"]},
    {"id": "marca_011", "nombre": "Movistar", "categoria": "Telecom", "productos": ["Plan Prepago", "Internet Hogar", "Movistar TV"]},
    {"id": "marca_012", "nombre": "Rappi", "categoria": "Tech", "productos": ["Rappi Prime", "Entrega Restaurantes", "Rappi Favor"]},
    {"id": "marca_013", "nombre": "Mercado Libre", "categoria": "Tech", "productos": ["Envíos Full", "Moda y Accesorios", "Tecnología"]},
    {"id": "marca_014", "nombre": "Cementos Argos", "categoria": "Construcción", "productos": ["Cemento Gris Uso General", "Concreto Premezclado", "Soluciones Viales"]},
    {"id": "marca_015", "nombre": "Terpel", "categoria": "Energía", "productos": ["Gasolina Extra G-Prix", "Lubricantes Mobil", "Tiendas Altoque"]},
    {"id": "marca_016", "nombre": "Falabella", "categoria": "Retail", "productos": ["Moda Mujer", "Tecnología Apple", "Muebles y Decoración"]},
    {"id": "marca_017", "nombre": "Tigo", "categoria": "Telecom", "productos": ["Plan Internet Residencial", "Tigo Money", "Roaming Internacional"]},
    {"id": "marca_018", "nombre": "Grupo Aval", "categoria": "Banca", "productos": ["Crédito de Libranza", "Fondos de Inversión Colectiva", "Banca Virtual AvalPay"]},
    {"id": "marca_019", "nombre": "Bavaria", "categoria": "CPG", "productos": ["Cerveza Aguila", "Pony Malta", "Cerveza Club Colombia"]},
    {"id": "marca_020", "nombre": "Wingo", "categoria": "Airlines", "productos": ["Vuelos Bajo Costo Caribe", "Promociones Flash", "Equipaje Adicional"]}
]

AUDIENCIAS_COLOMBIANAS = [
    {
        "id": "aud_001",
        "nombre": "Jóvenes Universitarios (18-24)",
        "descripcion": "Estudiantes de pregrado activos en redes sociales, interesados en tecnología emergente, entretenimiento digital, moda accesible y viajes económicos.",
        "intereses_clave": ["tecnologia_emergente", "videojuegos_online", "musica_streaming", "viajes_mochilero", "redes_sociales_tendencias", "moda_rapida", "eventos_universitarios"],
        "afinidad_marca_categoria": {
            "Banca": 0.4, "Energía": 0.1, "CPG": 0.7, "Airlines": 0.6, "Retail": 0.6, "Telecom": 0.8, "Tech": 0.9, "Construcción": 0.05
        }
    },
    {
        "id": "aud_002",
        "nombre": "Profesionales Jóvenes (25-34)",
        "descripcion": "Profesionales en crecimiento, enfocados en desarrollo de carrera, finanzas personales, bienestar, y experiencias como cenas y viajes.",
        "intereses_clave": ["desarrollo_profesional_liderazgo", "inversiones_cripto", "viajes_experiencias", "restaurantes_gourmet", "fitness_wellness", "networking", "educacion_continua"],
        "afinidad_marca_categoria": {
            "Banca": 0.7, "Energía": 0.2, "CPG": 0.5, "Airlines": 0.7, "Retail": 0.5, "Telecom": 0.6, "Tech": 0.7, "Construcción": 0.1
        }
    },
    {
        "id": "aud_003",
        "nombre": "Entusiastas de la Tecnología (20-45)",
        "descripcion": "Individuos apasionados por los últimos gadgets, software, inteligencia artificial y el ecosistema de startups tecnológicas.",
        "intereses_clave": ["gadgets_innovadores", "software_productividad", "inteligencia_artificial_aplicada", "videojuegos_consola_pc", "ecommerce_tecnologia_especializada", "realidad_virtual_aumentada", "domotica"],
        "afinidad_marca_categoria": {
            "Banca": 0.4, "Energía": 0.3, "CPG": 0.2, "Airlines": 0.3, "Retail": 0.4, "Telecom": 0.7, "Tech": 0.95, "Construcción": 0.1
        }
    },
    {
        "id": "aud_004",
        "nombre": "Familias Consolidadas (35-55)",
        "descripcion": "Padres de familia con hijos en edad escolar o adolescente, interesados en productos para el hogar, educación, salud familiar, vehículos y planificación financiera a largo plazo.",
        "intereses_clave": ["productos_hogar_familia", "educacion_hijos_universitaria", "viajes_familiares_vacaciones", "seguros_vida_salud", "alimentacion_organica", "vehiculos_familiares_suv", "mejoras_hogar"], # "universidad" changed to "universitaria"
        "afinidad_marca_categoria": {
            "Banca": 0.8, "Energía": 0.2, "CPG": 0.8, "Airlines": 0.5, "Retail": 0.7, "Telecom": 0.5, "Tech": 0.4, "Construcción": 0.3
        }
    },
    {
        "id": "aud_005",
        "nombre": "Adultos Mayores Activos (60+)",
        "descripcion": "Personas jubiladas o próximas a jubilarse, enfocadas en salud, bienestar, viajes culturales, hobbies y gestión de patrimonio.",
        "intereses_clave": ["salud_preventiva_bienestar", "viajes_culturales_cruceros", "seguros_medicos_complementarios", "inversiones_conservadoras_retiro", "hobbies_manualidades_jardineria", "tecnologia_simplificada", "actividades_comunitarias"],
        "afinidad_marca_categoria": {
            "Banca": 0.8, "Energía": 0.1, "CPG": 0.6, "Airlines": 0.7, "Retail": 0.5, "Telecom": 0.3, "Tech": 0.2, "Construcción": 0.2
        }
    },
    {
        "id": "aud_006",
        "nombre": "Emprendedores Digitales (28-45)",
        "descripcion": "Fundadores y empleados de startups y negocios online, interesados en herramientas de marketing, productividad, SaaS y crecimiento empresarial.",
        "intereses_clave": ["marketing_digital_seo_sem", "herramientas_saas", "productividad_gestion_proyectos", "ecommerce_plataformas", "inversion_semilla_escalamiento", "eventos_networking_emprendimiento", "tecnologia_nube"],
        "afinidad_marca_categoria": {
            "Banca": 0.6, "Energía": 0.1, "CPG": 0.3, "Airlines": 0.4, "Retail": 0.3, "Telecom": 0.8, "Tech": 0.9, "Construcción": 0.1
        }
    },
    {
        "id": "aud_007",
        "nombre": "Amantes del Lujo (30-55)",
        "descripcion": "Individuos con alto poder adquisitivo, interesados en marcas premium, experiencias exclusivas, viajes de lujo y artículos de alta gama.",
        "intereses_clave": ["marcas_lujo_moda_joyeria", "experiencias_exclusivas_hoteles_boutique", "viajes_primera_clase_destinos_exoticos", "autos_deportivos_lujo", "arte_coleccionables", "gastronomia_michelin", "inversiones_alto_riesgo"],
        "afinidad_marca_categoria": {
            "Banca": 0.7, "Energía": 0.2, "CPG": 0.4, "Airlines": 0.8, "Retail": 0.6, "Telecom": 0.5, "Tech": 0.6, "Construcción": 0.3 # Podrían estar interesados en propiedades de lujo
        }
    },
    {
        "id": "aud_008",
        "nombre": "Gamers Hardcore (16-30)",
        "descripcion": "Jugadores dedicados que invierten tiempo y dinero en videojuegos, hardware especializado y competencias de eSports.",
        "intereses_clave": ["videojuegos_aaa_competitivos", "hardware_gaming_pc_perifericos", "esports_torneos_equipos", "streaming_videojuegos_twitch_youtube", "comunidades_gaming_discord", "realidad_virtual_gaming", "bebidas_energeticas_snacks_gaming"],
        "afinidad_marca_categoria": {
            "Banca": 0.2, "Energía": 0.1, "CPG": 0.6, "Airlines": 0.2, "Retail": 0.4, "Telecom": 0.8, "Tech": 0.9, "Construcción": 0.05
        }
    },
    {
        "id": "aud_009",
        "nombre": "Viajeros Frecuentes por Negocios (35-55)",
        "descripcion": "Profesionales que viajan constantemente por trabajo, valoran la eficiencia, comodidad y programas de lealtad.",
        "intereses_clave": ["programas_lealtad_aerolineas_hoteles", "viajes_negocios_eficientes", "hoteles_ejecutivos", "alquiler_autos_corporativo", "equipaje_funcional", "apps_viajes_productividad", "salas_vip_aeropuertos"],
        "afinidad_marca_categoria": {
            "Banca": 0.7, "Energía": 0.1, "CPG": 0.3, "Airlines": 0.9, "Retail": 0.4, "Telecom": 0.6, "Tech": 0.5, "Construcción": 0.1
        }
    },
    {
        "id": "aud_010",
        "nombre": "Conscientes del Medio Ambiente (25-50)",
        "descripcion": "Personas preocupadas por la sostenibilidad, productos ecológicos, energías renovables y prácticas de consumo responsable.",
        "intereses_clave": ["sostenibilidad_productos_eco", "energias_renovables_hogar", "consumo_responsable_local", "transporte_sostenible_bicicleta_electrico", "moda_etica", "reciclaje_zero_waste", "activismo_ambiental"],
        "afinidad_marca_categoria": {
            "Banca": 0.5, # Inversiones éticas
            "Energía": 0.8, # Interés en empresas con prácticas sostenibles
            "CPG": 0.7, # Productos orgánicos, empaques sostenibles
            "Airlines": 0.3, # Críticos con la huella de carbono, pero pueden viajar
            "Retail": 0.6, # Marcas con políticas de sostenibilidad
            "Telecom": 0.4,
            "Tech": 0.5, # Tecnología para eficiencia energética
            "Construcción": 0.4 # Construcciones sostenibles
        }
    },
    {
        "id": "aud_011",
        "nombre": "Amantes de la Cocina y Gastronomía (28-55)",
        "descripcion": "Aficionados a cocinar, probar nuevas recetas, ingredientes de calidad y explorar la escena gastronómica.",
        "intereses_clave": ["cocina_gourmet_casera", "recetas_internacionales_locales", "ingredientes_organicos_artesanales", "utensilios_cocina_profesionales", "vinos_maridajes", "restaurantes_criticas_blogs", "clases_cocina"],
        "afinidad_marca_categoria": {
            "Banca": 0.3, "Energía": 0.1, "CPG": 0.9, "Airlines": 0.4, "Retail": 0.7, "Telecom": 0.2, "Tech": 0.3, "Construcción": 0.1
        }
    },
    {
        "id": "aud_012",
        "nombre": "Deportistas Aficionados (20-40)",
        "descripcion": "Personas que practican deportes regularmente, interesados en ropa deportiva, equipamiento, nutrición y eventos deportivos.",
        "intereses_clave": ["running_ciclismo_gimnasio", "ropa_deportiva_tecnica", "equipamiento_deportivo_especializado", "nutricion_deportiva_suplementos", "eventos_deportivos_maratones_carreras", "tecnologia_wearables_deporte", "prevencion_lesiones"],
        "afinidad_marca_categoria": {
            "Banca": 0.3, "Energía": 0.2, "CPG": 0.7, "Airlines": 0.4, "Retail": 0.6, "Telecom": 0.3, "Tech": 0.5, "Construcción": 0.1
        }
    },
    {
        "id": "aud_013",
        "nombre": "Propietarios de Vivienda Recientes (30-45)",
        "descripcion": "Individuos que han adquirido una propiedad recientemente, interesados en mejoras del hogar, muebles, decoración y servicios relacionados.",
        "intereses_clave": ["mejoras_hogar_remodelacion", "muebles_decoracion_interiores", "electrodomesticos_eficientes", "jardineria_paisajismo", "seguros_hogar_hipotecas", "servicios_limpieza_mantenimiento", "comunidades_vecinos_propietarios"],
        "afinidad_marca_categoria": {
            "Banca": 0.8, "Energía": 0.3, "CPG": 0.5, "Airlines": 0.2, "Retail": 0.8, "Telecom": 0.4, "Tech": 0.4, "Construcción": 0.7
        }
    },
    {
        "id": "aud_014",
        "nombre": "Estudiantes de Posgrado y MBA (26-35)",
        "descripcion": "Individuos cursando estudios superiores, enfocados en networking, oportunidades laborales, herramientas de estudio y gestión del tiempo.",
        "intereses_clave": ["networking_profesional_alumni", "oportunidades_laborales_ferias_empleo", "herramientas_colaboracion_online", "gestion_tiempo_productividad_personal", "finanzas_personales_estudiantes_posgrado", "viajes_academicos_conferencias", "software_analisis_datos"],
        "afinidad_marca_categoria": {
            "Banca": 0.7, "Energía": 0.1, "CPG": 0.4, "Airlines": 0.5, "Retail": 0.4, "Telecom": 0.6, "Tech": 0.8, "Construcción": 0.1
        }
    },
    {
        "id": "aud_015",
        "nombre": "Artistas y Creativos (22-40)",
        "descripcion": "Profesionales y aficionados al arte, diseño, música y otras disciplinas creativas, buscan inspiración y herramientas para su trabajo.",
        "intereses_clave": ["software_diseño_edicion_video_audio", "materiales_arte_manualidades", "eventos_culturales_exposiciones_conciertos", "plataformas_venta_arte_online", "networking_comunidades_creativas", "inspiracion_viajes_naturaleza", "derechos_autor_propiedad_intelectual"],
        "afinidad_marca_categoria": {
            "Banca": 0.3, "Energía": 0.1, "CPG": 0.5, "Airlines": 0.4, "Retail": 0.5, "Telecom": 0.5, "Tech": 0.7, "Construcción": 0.1
        }
    }
]

INTERESES_DETALLADOS = [
    {"id": "int_001", "nombre": "Tecnología Emergente", "categoria_interes": "Tecnología"},
    {"id": "int_002", "nombre": "Videojuegos Online", "categoria_interes": "Entretenimiento"},
    {"id": "int_003", "nombre": "Música en Streaming", "categoria_interes": "Entretenimiento"},
    {"id": "int_004", "nombre": "Viajes de Mochilero", "categoria_interes": "Viajes"},
    {"id": "int_005", "nombre": "Tendencias en Redes Sociales", "categoria_interes": "Tecnología"},
    {"id": "int_006", "nombre": "Moda Rápida y Urbana", "categoria_interes": "Moda"},
    {"id": "int_007", "nombre": "Eventos Universitarios y Festivales", "categoria_interes": "Entretenimiento"},
    {"id": "int_008", "nombre": "Desarrollo Profesional y Liderazgo", "categoria_interes": "Carrera"},
    {"id": "int_009", "nombre": "Inversiones y Criptomonedas", "categoria_interes": "Finanzas Personales"},
    {"id": "int_010", "nombre": "Viajes de Experiencias Únicas", "categoria_interes": "Viajes"},
    {"id": "int_011", "nombre": "Restaurantes Gourmet y Alta Cocina", "categoria_interes": "Gastronomía"},
    {"id": "int_012", "nombre": "Fitness y Bienestar Holístico", "categoria_interes": "Salud y Bienestar"},
    {"id": "int_013", "nombre": "Networking Estratégico", "categoria_interes": "Carrera"},
    {"id": "int_014", "nombre": "Educación Continua y Masters", "categoria_interes": "Educación"},
    {"id": "int_015", "nombre": "Gadgets Innovadores y Wearables", "categoria_interes": "Tecnología"},
    {"id": "int_016", "nombre": "Software de Productividad y Colaboración", "categoria_interes": "Tecnología"},
    {"id": "int_017", "nombre": "Inteligencia Artificial Aplicada", "categoria_interes": "Tecnología"},
    {"id": "int_018", "nombre": "Videojuegos de Consola y PC", "categoria_interes": "Entretenimiento"},
    {"id": "int_019", "nombre": "Ecommerce Especializado en Tecnología", "categoria_interes": "Compras Online"},
    {"id": "int_020", "nombre": "Realidad Virtual y Aumentada", "categoria_interes": "Tecnología"},
    {"id": "int_021", "nombre": "Domótica y Hogar Inteligente", "categoria_interes": "Tecnología"},
    {"id": "int_022", "nombre": "Productos para el Hogar y Familia", "categoria_interes": "Hogar"},
    {"id": "int_023", "nombre": "Educación de Hijos y Planificación Universitaria", "categoria_interes": "Familia"},
    {"id": "int_024", "nombre": "Viajes Familiares y Vacaciones Escolares", "categoria_interes": "Viajes"},
    {"id": "int_025", "nombre": "Seguros de Vida y Salud", "categoria_interes": "Finanzas Personales"},
    {"id": "int_026", "nombre": "Alimentación Orgánica y Saludable", "categoria_interes": "Salud y Bienestar"},
    {"id": "int_027", "nombre": "Vehículos Familiares y SUVs", "categoria_interes": "Automotriz"},
    {"id": "int_028", "nombre": "Mejoras del Hogar y Remodelación", "categoria_interes": "Hogar"},
    {"id": "int_029", "nombre": "Salud Preventiva y Bienestar Senior", "categoria_interes": "Salud y Bienestar"},
    {"id": "int_030", "nombre": "Viajes Culturales y Cruceros", "categoria_interes": "Viajes"},
    {"id": "int_031", "nombre": "Marketing Digital (SEO/SEM)", "categoria_interes": "Negocios"},
    {"id": "int_032", "nombre": "Herramientas SaaS para Empresas", "categoria_interes": "Negocios"},
    {"id": "int_033", "nombre": "Running y Ciclismo", "categoria_interes": "Deportes"},
    {"id": "int_034", "nombre": "Ropa Deportiva Técnica", "categoria_interes": "Moda"},
    {"id": "int_035", "nombre": "Nutrición Deportiva y Suplementos", "categoria_interes": "Salud y Bienestar"}
]

# Podríamos añadir más parámetros aquí en el futuro, como:
# - CANALES_DISPONIBLES (Display, Video, Social, Search)
# - FORMATOS_ANUNCIO_POR_CANAL
# - COSTOS_BASE_CPM_POR_CANAL_AUDIENCIA
# - MODIFICADORES_CONTEXTO (Noticias, Entretenimiento, Deportes, etc.)
# - EVENTOS_ESPECIALES_COLOMBIA (Amor y Amistad, Navidad, Black Friday Colombia)

COLOMBIAN_POPULATION_SEGMENTS = [
    {"segment_id": "total_colombia", "nombre_segmento": "Población Total Colombia", "size": 52000000, "fuente_dato": "Estimado DANE 2023 (Placeholder)"},
    {"segment_id": "jovenes_18_24_col", "nombre_segmento": "Jóvenes (18-24 años) Colombia", "size": 5500000, "relates_to_audience_ids": ["aud_001", "aud_008"], "fuente_dato": "Estimado (Placeholder)"},
    {"segment_id": "profesionales_jovenes_25_34_col", "nombre_segmento": "Profesionales Jóvenes (25-34 años) Colombia", "size": 7000000, "relates_to_audience_ids": ["aud_002", "aud_003", "aud_006", "aud_014"], "fuente_dato": "Estimado (Placeholder)"},
    {"segment_id": "familias_35_55_col", "nombre_segmento": "Familias Consolidadas (35-55 años) Colombia", "size": 10000000, "relates_to_audience_ids": ["aud_004", "aud_007", "aud_009", "aud_013"], "fuente_dato": "Estimado (Placeholder)"},
    {"segment_id": "adultos_mayores_60_mas_col", "nombre_segmento": "Adultos Mayores (60+ años) Colombia", "size": 7500000, "relates_to_audience_ids": ["aud_005"], "fuente_dato": "Estimado (Placeholder)"},
    {"segment_id": "norte_colombia_urbano", "nombre_segmento": "Región Norte Urbana (Barranquilla, Cartagena, Santa Marta)", "size": 4000000, "fuente_dato": "Estimado (Placeholder)"},
    {"segment_id": "centro_colombia_urbano", "nombre_segmento": "Región Centro Urbana (Bogotá, Medellín, Cali)", "size": 15000000, "fuente_dato": "Estimado (Placeholder)"},
    {"segment_id": "trabajadores_ingresos_medios", "nombre_segmento": "Trabajadores con Ingresos Medios (2-5 SMMLV)", "size": 12000000, "fuente_dato": "Estimado (Placeholder)"}
]

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

def obtener_interes_por_id(interes_id):
    for interes in INTERESES_DETALLADOS:
        if interes["id"] == interes_id:
            return interes
    return None

def obtener_todos_los_intereses():
    return INTERESES_DETALLADOS

def obtener_todas_las_marcas():
    return MARCAS_COLOMBIANAS

def obtener_todas_las_audiencias():
    return AUDIENCIAS_COLOMBIANAS

CAMPAIGN_GOALS = [
    {
        "id": "awareness",
        "nombre": "Reconocimiento de Marca",
        "descripcion": "Maximizar la visibilidad y el recuerdo de la marca entre la audiencia objetivo.",
        "kpi_primario": "impresiones"
    },
    {
        "id": "traffic",
        "nombre": "Tráfico al Sitio Web",
        "descripcion": "Generar la mayor cantidad de visitas de calidad al sitio web de la campaña.",
        "kpi_primario": "clics"
    },
    {
        "id": "engagement",
        "nombre": "Interacción con la Marca",
        "descripcion": "Fomentar la participación activa de la audiencia con el contenido de la marca.",
        "kpi_primario": "interacciones_calculadas" # Este KPI es un placeholder, necesitaría una métrica real
    },
    {
        "id": "conversion",
        "nombre": "Conversiones",
        "descripcion": "Impulsar acciones específicas valiosas en el sitio web (e.g., compras, registros).",
        "kpi_primario": "conversiones_calculadas" # Este KPI es un placeholder
    }
]

def obtener_todos_los_campaign_goals():
    return CAMPAIGN_GOALS

def obtener_campaign_goal_por_id(goal_id):
    for goal in CAMPAIGN_GOALS:
        if goal["id"] == goal_id:
            return goal
    return None

def obtener_segmento_poblacion_por_id(segment_id):
    for segmento in COLOMBIAN_POPULATION_SEGMENTS:
        if segmento["segment_id"] == segment_id:
            return segmento
    return None

def obtener_todos_los_segmentos_poblacion():
    return COLOMBIAN_POPULATION_SEGMENTS
