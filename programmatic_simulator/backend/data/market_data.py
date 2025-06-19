# programmatic_simulator/backend/data/market_data.py

MARCAS_COLOMBIANAS = [
    {
        "id": "marca_001", "nombre": "Bancolombia", "categoria": "Banca",
        "productos": [
            {"id": "prod_001_01", "nombre": "Cuenta de Ahorros", "afinidad_audiencia": {"aud_002": 0.7, "aud_004": 0.8, "aud_013": 0.8}},
            {"id": "prod_001_02", "nombre": "Tarjeta de Crédito Gold", "afinidad_audiencia": {"aud_002": 0.8, "aud_007": 0.6}},
            {"id": "prod_001_03", "nombre": "Crédito Hipotecario", "afinidad_audiencia": {"aud_004": 0.7, "aud_013": 0.9}}
        ]
    },
    {
        "id": "marca_002", "nombre": "Ecopetrol", "categoria": "Energía",
        "productos": [
            {"id": "prod_002_01", "nombre": "Gasolina Corriente", "afinidad_audiencia": {"aud_004": 0.5, "aud_010": 0.2}}, # General use
            {"id": "prod_002_02", "nombre": "ACPM", "afinidad_audiencia": {"aud_004": 0.5, "aud_009": 0.4}}, # Transport related
            {"id": "prod_002_03", "nombre": "Petroquímicos", "afinidad_audiencia": {}} # B2B, less direct consumer affinity
        ]
    },
    {
        "id": "marca_003", "nombre": "Alpina", "categoria": "CPG",
        "productos": [
            {"id": "prod_003_01", "nombre": "Leche Entera", "afinidad_audiencia": {"aud_004": 0.9, "aud_011": 0.7}},
            {"id": "prod_003_02", "nombre": "Yogurt Finesse", "afinidad_audiencia": {"aud_002": 0.6, "aud_012": 0.7}},
            {"id": "prod_003_03", "nombre": "Arequipe", "afinidad_audiencia": {"aud_001": 0.5, "aud_011": 0.6}}
        ]
    },
    {
        "id": "marca_004", "nombre": "Avianca", "categoria": "Airlines",
        "productos": [
            {"id": "prod_004_01", "nombre": "Tiquetes Nacionales", "afinidad_audiencia": {"aud_001": 0.7, "aud_002": 0.7, "aud_004": 0.6, "aud_009": 0.8}},
            {"id": "prod_004_02", "nombre": "Tiquetes Internacionales", "afinidad_audiencia": {"aud_002": 0.8, "aud_005": 0.7, "aud_007": 0.8, "aud_009": 0.9}},
            {"id": "prod_004_03", "nombre": "Programa LifeMiles", "afinidad_audiencia": {"aud_002": 0.7, "aud_007": 0.7, "aud_009": 0.9}}
        ]
    },
    {
        "id": "marca_005", "nombre": "Postobón", "categoria": "CPG",
        "productos": [
            {"id": "prod_005_01", "nombre": "Gaseosa Manzana", "afinidad_audiencia": {"aud_001": 0.8, "aud_004": 0.7, "aud_008": 0.6}},
            {"id": "prod_005_02", "nombre": "Agua Cristal", "afinidad_audiencia": {"aud_002": 0.5, "aud_010": 0.6, "aud_012": 0.7}},
            {"id": "prod_005_03", "nombre": "Jugo Hit", "afinidad_audiencia": {"aud_001": 0.7, "aud_004": 0.6}}
        ]
    },
    {
        "id": "marca_006", "nombre": "Éxito", "categoria": "Retail",
        "productos": [
            {"id": "prod_006_01", "nombre": "Mercado Básico", "afinidad_audiencia": {"aud_004": 0.9, "aud_005": 0.7, "aud_013": 0.6}},
            {"id": "prod_006_02", "nombre": "Electrodomésticos", "afinidad_audiencia": {"aud_004": 0.7, "aud_007": 0.5, "aud_013": 0.8}},
            {"id": "prod_006_03", "nombre": "Ropa Casual", "afinidad_audiencia": {"aud_001": 0.6, "aud_002": 0.5}}
        ]
    },
    {
        "id": "marca_007", "nombre": "Claro", "categoria": "Telecom",
        "productos": [
            {"id": "prod_007_01", "nombre": "Plan Pospago 5G", "afinidad_audiencia": {"aud_001": 0.8, "aud_002": 0.7, "aud_003": 0.8, "aud_006": 0.7}},
            {"id": "prod_007_02", "nombre": "Internet Fibra Óptica", "afinidad_audiencia": {"aud_003": 0.9, "aud_004": 0.6, "aud_006": 0.8, "aud_008": 0.7}},
            {"id": "prod_007_03", "nombre": "Claro Video", "afinidad_audiencia": {"aud_001": 0.6, "aud_004": 0.5}}
        ]
    },
    {
        "id": "marca_008", "nombre": "Davivienda", "categoria": "Banca",
        "productos": [
            {"id": "prod_008_01", "nombre": "Cuenta Móvil", "afinidad_audiencia": {"aud_001": 0.7, "aud_002": 0.6}},
            {"id": "prod_008_02", "nombre": "Tarjeta de Crédito Diners", "afinidad_audiencia": {"aud_007": 0.7, "aud_009": 0.6}},
            {"id": "prod_008_03", "nombre": "Seguro de Vida", "afinidad_audiencia": {"aud_004": 0.8, "aud_005": 0.7}}
        ]
    },
    {
        "id": "marca_009", "nombre": "Nutresa", "categoria": "CPG",
        "productos": [
            {"id": "prod_009_01", "nombre": "Chocolatinas Jet", "afinidad_audiencia": {"aud_001": 0.9, "aud_004": 0.7}},
            {"id": "prod_009_02", "nombre": "Galletas Noel", "afinidad_audiencia": {"aud_004": 0.8, "aud_011": 0.6}},
            {"id": "prod_009_03", "nombre": "Café Sello Rojo", "afinidad_audiencia": {"aud_002": 0.5, "aud_004": 0.7, "aud_005": 0.6}}
        ]
    },
    {
        "id": "marca_010", "nombre": "LATAM Airlines", "categoria": "Airlines",
        "productos": [
            {"id": "prod_010_01", "nombre": "Vuelos a Suramérica", "afinidad_audiencia": {"aud_001": 0.6, "aud_002": 0.7, "aud_005": 0.6}},
            {"id": "prod_010_02", "nombre": "Paquetes Turísticos", "afinidad_audiencia": {"aud_004": 0.6, "aud_005": 0.7, "aud_007": 0.5}},
            {"id": "prod_010_03", "nombre": "Transporte de Carga", "afinidad_audiencia": {}} # B2B
        ]
    },
    {
        "id": "marca_011", "nombre": "Movistar", "categoria": "Telecom",
        "productos": [
            {"id": "prod_011_01", "nombre": "Plan Prepago", "afinidad_audiencia": {"aud_001": 0.8, "aud_005": 0.4}},
            {"id": "prod_011_02", "nombre": "Internet Hogar", "afinidad_audiencia": {"aud_004": 0.7, "aud_013": 0.6}},
            {"id": "prod_011_03", "nombre": "Movistar TV", "afinidad_audiencia": {"aud_004": 0.6, "aud_005": 0.5}}
        ]
    },
    {
        "id": "marca_012", "nombre": "Rappi", "categoria": "Tech",
        "productos": [
            {"id": "prod_012_01", "nombre": "Rappi Prime", "afinidad_audiencia": {"aud_001": 0.7, "aud_002": 0.8, "aud_006": 0.7}},
            {"id": "prod_012_02", "nombre": "Entrega Restaurantes", "afinidad_audiencia": {"aud_001": 0.8, "aud_002": 0.7, "aud_011": 0.6}},
            {"id": "prod_012_03", "nombre": "Rappi Favor", "afinidad_audiencia": {"aud_002": 0.6, "aud_004": 0.5}}
        ]
    },
    {
        "id": "marca_013", "nombre": "Mercado Libre", "categoria": "Tech",
        "productos": [
            {"id": "prod_013_01", "nombre": "Envíos Full", "afinidad_audiencia": {"aud_001": 0.7, "aud_002": 0.8, "aud_006": 0.7}},
            {"id": "prod_013_02", "nombre": "Moda y Accesorios", "afinidad_audiencia": {"aud_001": 0.8, "aud_002": 0.6, "aud_015": 0.5}},
            {"id": "prod_013_03", "nombre": "Tecnología", "afinidad_audiencia": {"aud_001": 0.7, "aud_003": 0.9, "aud_008": 0.6}}
        ]
    },
    {
        "id": "marca_014", "nombre": "Cementos Argos", "categoria": "Construcción",
        "productos": [
            {"id": "prod_014_01", "nombre": "Cemento Gris Uso General", "afinidad_audiencia": {"aud_013": 0.7, "aud_004": 0.5, "aud_010": 0.2}}, # Home owners
            {"id": "prod_014_02", "nombre": "Concreto Premezclado", "afinidad_audiencia": {"aud_013": 0.4, "aud_006": 0.2}}, # B2B focus
            {"id": "prod_014_03", "nombre": "Soluciones Viales", "afinidad_audiencia": {}} # B2B/B2G focus
        ]
    },
    {
        "id": "marca_015", "nombre": "Terpel", "categoria": "Energía",
        "productos": [
            {"id": "prod_015_01", "nombre": "Gasolina Extra G-Prix", "afinidad_audiencia": {"aud_002": 0.5, "aud_007": 0.4, "aud_009": 0.4}}, # Higher income, car enthusiasts
            {"id": "prod_015_02", "nombre": "Lubricantes Mobil", "afinidad_audiencia": {"aud_004": 0.4, "aud_009": 0.5, "aud_013": 0.3, "aud_002": 0.2}},
            {"id": "prod_015_03", "nombre": "Tiendas Altoque", "afinidad_audiencia": {"aud_001": 0.5, "aud_009": 0.6, "aud_002": 0.4, "aud_004": 0.3, "aud_008": 0.2}}
        ]
    },
    {
        "id": "marca_016", "nombre": "Falabella", "categoria": "Retail",
        "productos": [
            {"id": "prod_016_01", "nombre": "Moda Mujer", "afinidad_audiencia": {"aud_001": 0.7, "aud_002": 0.8, "aud_007": 0.6}},
            {"id": "prod_016_02", "nombre": "Tecnología Apple", "afinidad_audiencia": {"aud_001": 0.6, "aud_002": 0.7, "aud_003": 0.8, "aud_007": 0.5}},
            {"id": "prod_016_03", "nombre": "Muebles y Decoración", "afinidad_audiencia": {"aud_004": 0.7, "aud_007": 0.5, "aud_013": 0.8}}
        ]
    },
    {
        "id": "marca_017", "nombre": "Tigo", "categoria": "Telecom",
        "productos": [
            {"id": "prod_017_01", "nombre": "Plan Internet Residencial", "afinidad_audiencia": {"aud_004": 0.7, "aud_013": 0.6, "aud_001": 0.5, "aud_002": 0.6, "aud_006": 0.5}},
            {"id": "prod_017_02", "nombre": "Tigo Money", "afinidad_audiencia": {"aud_001": 0.5, "aud_002": 0.4, "aud_004": 0.3, "aud_005": 0.3, "aud_006": 0.4}}, # Broader appeal, potentially unbanked
            {"id": "prod_017_03", "nombre": "Roaming Internacional", "afinidad_audiencia": {"aud_002": 0.6, "aud_007": 0.7, "aud_009": 0.8}}
        ]
    },
    {
        "id": "marca_018", "nombre": "Grupo Aval", "categoria": "Banca", # This is a holding, products are via its banks. For simplicity, generic products.
        "productos": [
            {"id": "prod_018_01", "nombre": "Crédito de Libranza", "afinidad_audiencia": {"aud_002": 0.6, "aud_004": 0.7, "aud_005": 0.5, "aud_014": 0.4}},
            {"id": "prod_018_02", "nombre": "Fondos de Inversión Colectiva", "afinidad_audiencia": {"aud_002": 0.7, "aud_005": 0.5, "aud_014": 0.6}},
            {"id": "prod_018_03", "nombre": "Banca Virtual AvalPay", "afinidad_audiencia": {"aud_001": 0.6, "aud_002": 0.7, "aud_006": 0.6, "aud_003": 0.5, "aud_014": 0.5}}
        ]
    },
    {
        "id": "marca_019", "nombre": "Bavaria", "categoria": "CPG",
        "productos": [
            {"id": "prod_019_01", "nombre": "Cerveza Aguila", "afinidad_audiencia": {"aud_001": 0.7, "aud_002": 0.6, "aud_004": 0.5}}, # Broad appeal
            {"id": "prod_019_02", "nombre": "Pony Malta", "afinidad_audiencia": {"aud_001": 0.8, "aud_004": 0.6}}, # Younger, families
            {"id": "prod_019_03", "nombre": "Cerveza Club Colombia", "afinidad_audiencia": {"aud_002": 0.7, "aud_007": 0.5, "aud_011": 0.4}} # More premium
        ]
    },
    {
        "id": "marca_020", "nombre": "Wingo", "categoria": "Airlines",
        "productos": [
            {"id": "prod_020_01", "nombre": "Vuelos Bajo Costo Caribe", "afinidad_audiencia": {"aud_001": 0.8, "aud_002": 0.6, "aud_005":0.4}},
            {"id": "prod_020_02", "nombre": "Promociones Flash", "afinidad_audiencia": {"aud_001": 0.9, "aud_006": 0.5}},
            {"id": "prod_020_03", "nombre": "Equipaje Adicional", "afinidad_audiencia": {"aud_001": 0.4, "aud_004": 0.3, "aud_002": 0.3, "aud_005": 0.2, "aud_009": 0.2}}
        ]
    },
    {
        "id": "marca_021", "nombre": "CasaMax", "categoria": "Home Improvement Retail",
        "productos": [
            {"id": "prod_021_01", "nombre": "Kit Herramientas Básico", "afinidad_audiencia": {"aud_004": 0.7, "aud_013": 0.8, "aud_002": 0.4, "aud_005": 0.5, "aud_010": 0.3}},
            {"id": "prod_021_02", "nombre": "Pintura Interior Premium (Galón)", "afinidad_audiencia": {"aud_013": 0.9, "aud_004": 0.8, "aud_007": 0.5, "aud_005": 0.4, "aud_015": 0.3}},
            {"id": "prod_021_03", "nombre": "Organizador de Armario Modular", "afinidad_audiencia": {"aud_004": 0.6, "aud_013": 0.7, "aud_002": 0.5, "aud_001": 0.3, "aud_007": 0.4}}
        ]
    },
    {
        "id": "marca_022", "nombre": "RapidiArepa", "categoria": "Local Fast Food",
        "productos": [
            {"id": "prod_022_01", "nombre": "Arepa 'La Original' (Carne Mechada y Queso)", "afinidad_audiencia": {"aud_001": 0.8, "aud_002": 0.7, "aud_004": 0.6, "aud_008": 0.5, "aud_011": 0.4}},
            {"id": "prod_022_02", "nombre": "Combo Ejecutivo (Arepa + Sopa + Bebida)", "afinidad_audiencia": {"aud_002": 0.7, "aud_004": 0.5, "aud_006": 0.6, "aud_009": 0.4, "aud_014": 0.5}},
            {"id": "prod_022_03", "nombre": "Empanadas Colombianas (x3)", "afinidad_audiencia": {"aud_001": 0.7, "aud_004": 0.6, "aud_008": 0.6, "aud_005": 0.4, "aud_012": 0.5}}
        ]
    },
    {
        "id": "marca_023", "nombre": "PantallaCriolla", "categoria": "Streaming Services",
        "productos": [
            {"id": "prod_023_01", "nombre": "Suscripción Mensual Cine Colombiano", "afinidad_audiencia": {"aud_001": 0.6, "aud_002": 0.7, "aud_005": 0.5, "aud_015": 0.8, "aud_011": 0.4}},
            {"id": "prod_023_02", "nombre": "Alquiler Estreno Película Nacional", "afinidad_audiencia": {"aud_001": 0.5, "aud_002": 0.6, "aud_004": 0.4, "aud_015": 0.7, "aud_010": 0.3}},
            {"id": "prod_023_03", "nombre": "Paquete Series Web Colombianas", "afinidad_audiencia": {"aud_001": 0.7, "aud_006": 0.5, "aud_003": 0.4, "aud_015": 0.6, "aud_008": 0.3}}
        ]
    },
    {
        "id": "marca_024", "nombre": "EducaMásOnline", "categoria": "Educational Platforms",
        "productos": [
            {"id": "prod_024_01", "nombre": "Curso Online: Marketing Digital para Emprendedores", "afinidad_audiencia": {"aud_006": 0.9, "aud_002": 0.7, "aud_014": 0.8, "aud_001": 0.5, "aud_003": 0.4}},
            {"id": "prod_024_02", "nombre": "Suscripción Premium: Acceso Total a Cursos", "afinidad_audiencia": {"aud_014": 0.8, "aud_006": 0.7, "aud_002": 0.6, "aud_003": 0.5, "aud_009": 0.4}},
            {"id": "prod_024_03", "nombre": "Taller Virtual: Finanzas Personales para Jóvenes", "afinidad_audiencia": {"aud_001": 0.8, "aud_014": 0.7, "aud_002": 0.6, "aud_004": 0.3, "aud_005": 0.2}}
        ]
    },
    {
        "id": "marca_025", "nombre": "MascotasFelicesCol", "categoria": "Pet Supplies",
        "productos": [
            {"id": "prod_025_01", "nombre": "Alimento Premium para Perros Adultos (10kg)", "afinidad_audiencia": {"aud_004": 0.8, "aud_013": 0.7, "aud_002": 0.5, "aud_005": 0.6, "aud_012": 0.4}},
            {"id": "prod_025_02", "nombre": "Arena Sanitaria para Gatos Aglutinante (5kg)", "afinidad_audiencia": {"aud_004": 0.7, "aud_013": 0.6, "aud_001": 0.4, "aud_002": 0.5, "aud_010": 0.3}},
            {"id": "prod_025_03", "nombre": "Juguete Interactivo para Gatos con Hierba Gatera", "afinidad_audiencia": {"aud_001": 0.5, "aud_004": 0.6, "aud_002": 0.4, "aud_015": 0.3, "aud_011": 0.2}}
        ]
    },
    {
        "id": "marca_026", "nombre": "EcoModaBogota", "categoria": "Sustainable Fashion",
        "productos": [
            {"id": "prod_026_01", "nombre": "Camiseta Algodón Orgánico Certificado", "afinidad_audiencia": {"aud_010": 0.8, "aud_001": 0.5, "aud_002": 0.6, "aud_015": 0.4, "aud_007": 0.3}},
            {"id": "prod_026_02", "nombre": "Jeans Reciclados de Diseño Local", "afinidad_audiencia": {"aud_010": 0.9, "aud_002": 0.7, "aud_006": 0.5, "aud_015": 0.6, "aud_001": 0.4}},
            {"id": "prod_026_03", "nombre": "Accesorios Hechos a Mano con Materiales Reutilizados", "afinidad_audiencia": {"aud_010": 0.7, "aud_015": 0.8, "aud_001": 0.4, "aud_007": 0.5, "aud_011": 0.3}}
        ]
    }
]

AUDIENCIAS_COLOMBIANAS = [
    {
        "id": "aud_001",
        "nombre": "Jóvenes Universitarios (18-24)",
        "descripcion": "Estudiantes de pregrado activos en redes sociales, interesados en tecnología emergente, entretenimiento digital, moda accesible y viajes económicos.",
        "intereses_clave": ["tecnologia_emergente", "videojuegos_online", "musica_streaming", "viajes_mochilero", "redes_sociales_tendencias", "moda_rapida", "eventos_universitarios"],
        "afinidad_marca_categoria": { # Adjusted some affinities slightly
            "Banca": 0.5, "Energía": 0.1, "CPG": 0.8, "Airlines": 0.7, "Retail": 0.7, "Telecom": 0.9, "Tech": 0.9, "Construcción": 0.05
        }
    },
    {
        "id": "aud_002",
        "nombre": "Profesionales Jóvenes (25-34)",
        "descripcion": "Profesionales en crecimiento, enfocados en desarrollo de carrera, finanzas personales, bienestar, y experiencias como cenas y viajes.",
        "intereses_clave": ["desarrollo_profesional_liderazgo", "inversiones_cripto", "viajes_experiencias", "restaurantes_gourmet", "fitness_wellness", "networking", "educacion_continua"],
        "afinidad_marca_categoria": {
            "Banca": 0.75, "Energía": 0.2, "CPG": 0.6, "Airlines": 0.75, "Retail": 0.6, "Telecom": 0.7, "Tech": 0.8, "Construcción": 0.1
        }
    },
    {
        "id": "aud_003",
        "nombre": "Entusiastas de la Tecnología (20-45)",
        "descripcion": "Individuos apasionados por los últimos gadgets, software, inteligencia artificial y el ecosistema de startups tecnológicas.",
        "intereses_clave": ["gadgets_innovadores", "software_productividad", "inteligencia_artificial_aplicada", "videojuegos_consola_pc", "ecommerce_tecnologia_especializada", "realidad_virtual_aumentada", "domotica", "int_052", "int_053"],
        "afinidad_marca_categoria": {
            "Banca": 0.4, "Energía": 0.3, "CPG": 0.2, "Airlines": 0.4, "Retail": 0.5, "Telecom": 0.8, "Tech": 0.95, "Construcción": 0.1,
            "Home Improvement Retail": 0.3, "Local Fast Food": 0.2, "Streaming Services": 0.7, "Educational Platforms": 0.6, "Pet Supplies": 0.1, "Sustainable Fashion": 0.2
        }
    },
    {
        "id": "aud_004",
        "nombre": "Familias Consolidadas (35-55)",
        "descripcion": "Padres de familia con hijos en edad escolar o adolescente, interesados en productos para el hogar, educación, salud familiar, vehículos y planificación financiera a largo plazo.",
        "intereses_clave": ["productos_hogar_familia", "educacion_hijos_universitaria", "viajes_familiares_vacaciones", "seguros_vida_salud", "alimentacion_organica", "vehiculos_familiares_suv", "mejoras_hogar"],
        "afinidad_marca_categoria": {
            "Banca": 0.8, "Energía": 0.25, "CPG": 0.85, "Airlines": 0.6, "Retail": 0.75, "Telecom": 0.6, "Tech": 0.4, "Construcción": 0.35
        }
    },
    {
        "id": "aud_005",
        "nombre": "Adultos Mayores Activos (60+)",
        "descripcion": "Personas jubiladas o próximas a jubilarse, enfocadas en salud, bienestar, viajes culturales, hobbies y gestión de patrimonio.",
        "intereses_clave": ["salud_preventiva_bienestar", "viajes_culturales_cruceros", "seguros_medicos_complementarios", "inversiones_conservadoras_retiro", "hobbies_manualidades_jardineria", "tecnologia_simplificada", "actividades_comunitarias", "int_054", "int_055"],
        "afinidad_marca_categoria": {
            "Banca": 0.85, "Energía": 0.1, "CPG": 0.65, "Airlines": 0.7, "Retail": 0.6, "Telecom": 0.4, "Tech": 0.2, "Construcción": 0.2,
            "Home Improvement Retail": 0.3, "Local Fast Food": 0.4, "Streaming Services": 0.3, "Educational Platforms": 0.2, "Pet Supplies": 0.4, "Sustainable Fashion": 0.1
        }
    },
    {
        "id": "aud_006",
        "nombre": "Emprendedores Digitales (28-45)",
        "descripcion": "Fundadores y empleados de startups y negocios online, interesados en herramientas de marketing, productividad, SaaS y crecimiento empresarial.",
        "intereses_clave": ["marketing_digital_seo_sem", "herramientas_saas", "productividad_gestion_proyectos", "ecommerce_plataformas", "inversion_semilla_escalamiento", "eventos_networking_emprendimiento", "tecnologia_nube"],
        "afinidad_marca_categoria": {
            "Banca": 0.65, "Energía": 0.1, "CPG": 0.3, "Airlines": 0.5, "Retail": 0.4, "Telecom": 0.85, "Tech": 0.9, "Construcción": 0.1
        }
    },
    {
        "id": "aud_007",
        "nombre": "Amantes del Lujo (30-55)",
        "descripcion": "Individuos con alto poder adquisitivo, interesados en marcas premium, experiencias exclusivas, viajes de lujo y artículos de alta gama.",
        "intereses_clave": ["marcas_lujo_moda_joyeria", "experiencias_exclusivas_hoteles_boutique", "viajes_primera_clase_destinos_exoticos", "autos_deportivos_lujo", "arte_coleccionables", "gastronomia_michelin", "inversiones_alto_riesgo"],
        "afinidad_marca_categoria": {
            "Banca": 0.75, "Energía": 0.2, "CPG": 0.4, "Airlines": 0.85, "Retail": 0.7, "Telecom": 0.5, "Tech": 0.6, "Construcción": 0.3
        }
    },
    {
        "id": "aud_008",
        "nombre": "Gamers Hardcore (16-30)",
        "descripcion": "Jugadores dedicados que invierten tiempo y dinero en videojuegos, hardware especializado y competencias de eSports.",
        "intereses_clave": ["videojuegos_aaa_competitivos", "hardware_gaming_pc_perifericos", "esports_torneos_equipos", "streaming_videojuegos_twitch_youtube", "comunidades_gaming_discord", "realidad_virtual_gaming", "bebidas_energeticas_snacks_gaming"],
        "afinidad_marca_categoria": {
            "Banca": 0.2, "Energía": 0.1, "CPG": 0.7, "Airlines": 0.2, "Retail": 0.5, "Telecom": 0.9, "Tech": 0.9, "Construcción": 0.05
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
        "intereses_clave": ["sostenibilidad_productos_eco", "energias_renovables_hogar", "consumo_responsable_local", "transporte_sostenible_bicicleta_electrico", "moda_etica", "reciclaje_zero_waste", "activismo_ambiental", "int_056", "int_057"],
        "afinidad_marca_categoria": {
            "Banca": 0.55, "Energía": 0.8, "CPG": 0.75, "Airlines": 0.25, "Retail": 0.65, "Telecom": 0.4, "Tech": 0.5, "Construcción": 0.45,
            "Home Improvement Retail": 0.5, "Local Fast Food": 0.3, "Streaming Services": 0.4, "Educational Platforms": 0.6, "Pet Supplies": 0.4, "Sustainable Fashion": 0.9
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
    },
    {
        "id": "aud_016",
        "nombre": "Padres Jóvenes Urbanos (28-38 años)",
        "descripcion": "Padres y madres con hijos pequeños (0-7 años), residentes en ciudades principales. Buscan conveniencia, productos de calidad para sus hijos y familia, y balancear vida laboral con familiar. Activos digitalmente.",
        "intereses_clave": ["productos_hogar_familia", "int_036", "int_039", "int_040", "int_041", "int_042", "int_043"],
        "afinidad_marca_categoria": {
            "Banca": 0.7, "Energía": 0.2, "CPG": 0.9, "Airlines": 0.5, "Retail": 0.8, "Telecom": 0.7, "Tech": 0.6, "Construcción": 0.3,
            "Home Improvement Retail": 0.6, "Local Fast Food": 0.7, "Streaming Services": 0.6, "Educational Platforms": 0.5, "Pet Supplies": 0.7, "Sustainable Fashion": 0.4
        }
    },
    {
        "id": "aud_017",
        "nombre": "Nómadas Digitales en Colombia (24-40 años)",
        "descripcion": "Profesionales y creativos que trabajan de forma remota mientras viajan por Colombia. Valoran la flexibilidad, buena conexión a internet, espacios de coworking, y experiencias culturales locales. Presupuesto variable.",
        "intereses_clave": ["int_037", "int_044", "int_045", "int_046", "int_047", "int_014", "int_007"],
        "afinidad_marca_categoria": {
            "Banca": 0.6, "Energía": 0.1, "CPG": 0.5, "Airlines": 0.8, "Retail": 0.5, "Telecom": 0.9, "Tech": 0.9, "Construcción": 0.05,
            "Home Improvement Retail": 0.1, "Local Fast Food": 0.6, "Streaming Services": 0.7, "Educational Platforms": 0.8, "Pet Supplies": 0.2, "Sustainable Fashion": 0.5
        }
    },
    {
        "id": "aud_018",
        "nombre": "Adultos Mayores Tech-Savvy (65+ años)",
        "descripcion": "Adultos mayores que han adoptado la tecnología para comunicarse, entretenerse, gestionar su salud y finanzas. Activos en redes sociales (Facebook, WhatsApp) y usan apps de servicios.",
        "intereses_clave": ["tecnologia_simplificada", "int_048", "int_038", "int_049", "noticias_online_actualidad", "int_050", "int_051"],
        "afinidad_marca_categoria": {
            "Banca": 0.8, "Energía": 0.15, "CPG": 0.6, "Airlines": 0.6, "Retail": 0.7, "Telecom": 0.7, "Tech": 0.5, "Construcción": 0.25,
            "Home Improvement Retail": 0.3, "Local Fast Food": 0.4, "Streaming Services": 0.5, "Educational Platforms": 0.4, "Pet Supplies": 0.3, "Sustainable Fashion": 0.2
        }
    }
]

INTERESES_DETALLADOS = [
    {
        "id": "int_001", "nombre": "Tecnología Emergente", "categoria_interes": "Tecnología",
        "afinidad_marca": {
            "marca_012": 0.7, "marca_013": 0.8, "marca_007": 0.6, "marca_024": 0.5, "marca_026": 0.3, # Added Rappi, ML, Claro, EducaMas, EcoModa
            "marca_001": 0.2, "marca_006": 0.4, "marca_021": 0.2
        },
        "afinidad_producto": {
            "prod_007_01": 0.75, "prod_013_03": 0.85, "prod_012_01": 0.65, "prod_024_02": 0.5, # Added Claro Pospago, ML Tech, Rappi Prime, EducaMas Subs
            "prod_026_01": 0.3, "prod_001_01": 0.2, "prod_006_02": 0.4, "prod_021_01": 0.2
        }
    },
    {
        "id": "int_002", "nombre": "Videojuegos Online", "categoria_interes": "Entretenimiento",
        "afinidad_marca": {"marca_012": 0.7, "marca_013": 0.6, "marca_007": 0.5, "marca_023": 0.8, "marca_005": 0.4, "marca_017": 0.5, "marca_006": 0.3, "marca_022": 0.2},
        "afinidad_producto": {"prod_012_01": 0.6, "prod_013_03": 0.7, "prod_007_01": 0.5, "prod_023_03": 0.8, "prod_005_01": 0.5, "prod_017_01": 0.4, "prod_006_02": 0.2, "prod_022_01": 0.1}
    },
    {
        "id": "int_003", "nombre": "Música en Streaming", "categoria_interes": "Entretenimiento",
        "afinidad_marca": {"marca_023": 0.9, "marca_007": 0.6, "marca_011": 0.6, "marca_012": 0.5, "marca_013": 0.4, "marca_005": 0.3, "marca_017": 0.5, "marca_019": 0.2},
        "afinidad_producto": {"prod_023_01": 0.9, "prod_007_03": 0.7, "prod_011_03": 0.6, "prod_012_02": 0.4, "prod_013_01": 0.3, "prod_005_02": 0.2, "prod_019_01": 0.1, "prod_016_02": 0.3}
    },
    {
        "id": "int_004", "nombre": "Viajes de Mochilero", "categoria_interes": "Viajes",
        "afinidad_marca": {"marca_004": 0.7, "marca_010": 0.7, "marca_020": 0.8, "marca_022": 0.3, "marca_026": 0.4, "marca_012": 0.2, "marca_001": 0.1, "marca_006": 0.2},
        "afinidad_producto": {"prod_004_01": 0.7, "prod_010_01": 0.7, "prod_020_01": 0.8, "prod_022_01": 0.2, "prod_026_01": 0.3, "prod_012_03": 0.1, "prod_001_01": 0.1, "prod_006_03": 0.2}
    },
    {
        "id": "int_005", "nombre": "Tendencias en Redes Sociales", "categoria_interes": "Tecnología",
        "afinidad_marca": {"marca_012": 0.8, "marca_013": 0.7, "marca_007": 0.6, "marca_011": 0.6, "marca_023": 0.5, "marca_024": 0.4, "marca_026": 0.3, "marca_022": 0.2},
        "afinidad_producto": {"prod_012_01": 0.7, "prod_013_02": 0.6, "prod_007_01": 0.5, "prod_011_01": 0.5, "prod_023_03": 0.4, "prod_024_01": 0.3, "prod_026_02": 0.2, "prod_022_03": 0.1}
    },
    {"id": "int_006", "nombre": "Moda Rápida y Urbana", "categoria_interes": "Moda"},
    {"id": "int_007", "nombre": "Eventos Universitarios y Festivales", "categoria_interes": "Entretenimiento"},
    {
        "id": "int_008", "nombre": "Desarrollo Profesional y Liderazgo", "categoria_interes": "Carrera",
        "afinidad_marca": {"marca_024": 0.8, "marca_001": 0.5, "marca_018": 0.6, "marca_013": 0.4, "marca_007": 0.3, "marca_004": 0.2, "marca_006": 0.3, "marca_012": 0.4},
        "afinidad_producto": {"prod_024_01": 0.8, "prod_024_02": 0.7, "prod_001_02": 0.4, "prod_018_02": 0.5, "prod_013_01": 0.3, "prod_007_02": 0.2, "prod_006_02": 0.2, "prod_012_01": 0.3}
    },
    {
        "id": "int_009", "nombre": "Inversiones y Criptomonedas", "categoria_interes": "Finanzas Personales",
        "afinidad_marca": {
            "marca_001": 0.8, "marca_008": 0.7, "marca_018": 0.75, "marca_013": 0.5, "marca_024": 0.3, # Added Bancolombia, Davivienda, Aval, ML, EducaMas
            "marca_012": 0.2, "marca_006": 0.1, "marca_007": 0.2
        },
        "afinidad_producto": {
            "prod_001_02": 0.6, "prod_008_02": 0.5, "prod_018_02": 0.9, "prod_013_03": 0.4, # Added Tarjeta Gold, Diners, Fondos Aval, ML Tech
            "prod_024_03": 0.3, "prod_012_01": 0.1, "prod_007_01": 0.1, "prod_001_01":0.5
        }
    },
    {
        "id": "int_010", "nombre": "Viajes de Experiencias Únicas", "categoria_interes": "Viajes",
        "afinidad_marca": {"marca_004": 0.8, "marca_010": 0.8, "marca_007": 0.4, "marca_019": 0.3, "marca_012": 0.5, "marca_020": 0.6, "marca_022": 0.2, "marca_026": 0.3},
        "afinidad_producto": {"prod_004_02": 0.8, "prod_010_02": 0.8, "prod_007_03": 0.3, "prod_019_03": 0.2, "prod_012_02": 0.4, "prod_020_01": 0.5, "prod_022_01": 0.1, "prod_026_03": 0.2}
    },
    {
        "id": "int_011", "nombre": "Restaurantes Gourmet y Alta Cocina", "categoria_interes": "Gastronomía",
        "afinidad_marca": {
            "marca_003": 0.4, "marca_019": 0.7, "marca_004": 0.6, "marca_008": 0.5, "marca_012": 0.8, # Added Alpina, Bavaria, Avianca, Davivienda, Rappi
            "marca_022": 0.3, "marca_001": 0.2, "marca_006": 0.1
        },
        "afinidad_producto": {
            "prod_003_02": 0.3, "prod_019_03": 0.8, "prod_004_02": 0.7, "prod_008_02": 0.5, "prod_012_02": 0.9, # Added Yogurt Finesse, Club Colombia, Tiquetes Int, Tarjeta Diners, Rappi Restaurantes
            "prod_022_01": 0.4, "prod_001_02": 0.2, "prod_006_01": 0.1
        }
    },
    {
        "id": "int_012", "nombre": "Fitness y Bienestar Holístico", "categoria_interes": "Salud y Bienestar",
        "afinidad_marca": {"marca_003": 0.7, "marca_005": 0.6, "marca_012": 0.5, "marca_026": 0.4, "marca_006": 0.3, "marca_025":0.2, "marca_024":0.3, "marca_016":0.4},
        "afinidad_producto": {"prod_003_02":0.7, "prod_005_02":0.6, "prod_012_01":0.4, "prod_026_01":0.5, "prod_006_03":0.3, "prod_025_01":0.1, "prod_024_03":0.2, "prod_016_01":0.3}
    },
    {"id": "int_013", "nombre": "Networking Estratégico", "categoria_interes": "Carrera"},
    {"id": "int_014", "nombre": "Educación Continua y Masters", "categoria_interes": "Educación"},
    {"id": "int_015", "nombre": "Gadgets Innovadores y Wearables", "categoria_interes": "Tecnología"},
    {"id": "int_016", "nombre": "Software de Productividad y Colaboración", "categoria_interes": "Tecnología"},
    {"id": "int_017", "nombre": "Inteligencia Artificial Aplicada", "categoria_interes": "Tecnología"},
    {"id": "int_018", "nombre": "Videojuegos de Consola y PC", "categoria_interes": "Entretenimiento"},
    {"id": "int_019", "nombre": "Ecommerce Especializado en Tecnología", "categoria_interes": "Compras Online"},
    {"id": "int_020", "nombre": "Realidad Virtual y Aumentada", "categoria_interes": "Tecnología"},
    {"id": "int_021", "nombre": "Domótica y Hogar Inteligente", "categoria_interes": "Tecnología"},
    {
        "id": "int_022", "nombre": "Productos para el Hogar y Familia", "categoria_interes": "Hogar",
        "afinidad_marca": {"marca_006": 0.8, "marca_012": 0.6},
        "afinidad_producto": {"prod_006_01": 0.75, "prod_006_02": 0.6}
    },
    {
        "id": "int_023", "nombre": "Educación de Hijos y Planificación Universitaria", "categoria_interes": "Familia",
        "afinidad_marca": {"marca_006": 0.7, "marca_012": 0.5},
        "afinidad_producto": {"prod_006_03": 0.65}
    },
    {"id": "int_024", "nombre": "Viajes Familiares y Vacaciones Escolares", "categoria_interes": "Viajes"},
    {"id": "int_025", "nombre": "Seguros de Vida y Salud", "categoria_interes": "Finanzas Personales"},
    {"id": "int_026", "nombre": "Alimentación Orgánica y Saludable", "categoria_interes": "Salud y Bienestar"},
    {"id": "int_027", "nombre": "Vehículos Familiares y SUVs", "categoria_interes": "Automotriz"},
    {
        "id": "int_028", "nombre": "Mejoras del Hogar y Remodelación", "categoria_interes": "Hogar",
        "afinidad_marca": {"marca_006": 0.75, "marca_012": 0.55},
        "afinidad_producto": {"prod_006_02": 0.7, "prod_006_01": 0.6}
    },
    {"id": "int_029", "nombre": "Salud Preventiva y Bienestar Senior", "categoria_interes": "Salud y Bienestar"},
    {"id": "int_030", "nombre": "Viajes Culturales y Cruceros", "categoria_interes": "Viajes"},
    {"id": "int_031", "nombre": "Marketing Digital (SEO/SEM)", "categoria_interes": "Negocios"},
    {"id": "int_032", "nombre": "Herramientas SaaS para Empresas", "categoria_interes": "Negocios"},
    {"id": "int_033", "nombre": "Running y Ciclismo", "categoria_interes": "Deportes"},
    {"id": "int_034", "nombre": "Ropa Deportiva Técnica", "categoria_interes": "Moda"},
    {"id": "int_035", "nombre": "Nutrición Deportiva y Suplementos", "categoria_interes": "Salud y Bienestar"},
    {"id": "int_036", "nombre": "Educación Infantil y Preescolar", "categoria_interes": "Familia",
        "afinidad_marca": {"marca_024": 0.8, "marca_003": 0.6, "marca_006": 0.7, "marca_016": 0.5, "marca_025": 0.4, "marca_012": 0.3, "marca_022": 0.2, "marca_001": 0.1},
        "afinidad_producto": {"prod_024_03": 0.8, "prod_003_01": 0.7, "prod_006_01": 0.6, "prod_016_03": 0.4, "prod_025_03": 0.3, "prod_012_02": 0.2, "prod_022_03": 0.1, "prod_001_01": 0.1}
    },
    {"id": "int_037", "nombre": "Herramientas para Trabajo Remoto", "categoria_interes": "Tecnología",
        "afinidad_marca": {"marca_013": 0.8, "marca_007": 0.7, "marca_011": 0.7, "marca_024": 0.6, "marca_012": 0.5, "marca_006": 0.4, "marca_001": 0.3, "marca_016": 0.5},
        "afinidad_producto": {"prod_013_03": 0.8, "prod_007_02": 0.7, "prod_011_02": 0.7, "prod_024_02": 0.6, "prod_012_01": 0.5, "prod_006_02": 0.3, "prod_001_02": 0.2, "prod_016_02": 0.4}
    },
    {"id": "int_038", "nombre": "Salud Digital y Telemedicina", "categoria_interes": "Salud y Bienestar",
        "afinidad_marca": {"marca_007": 0.7, "marca_011": 0.6, "marca_017": 0.7, "marca_024": 0.5, "marca_012": 0.4, "marca_013": 0.3, "marca_001": 0.5, "marca_008": 0.5},
        "afinidad_producto": {"prod_007_01": 0.6, "prod_011_01": 0.5, "prod_017_02": 0.7, "prod_024_02": 0.4, "prod_012_01": 0.3, "prod_013_01": 0.2, "prod_001_01": 0.5, "prod_008_03": 0.6}
    },
    {"id": "int_039", "nombre": "Juguetes Didácticos", "categoria_interes": "Familia",
        "afinidad_marca": {"marca_006": 0.8, "marca_016": 0.7, "marca_013": 0.6, "marca_003": 0.5, "marca_025": 0.4, "marca_021": 0.3, "marca_022": 0.2, "marca_012": 0.1},
        "afinidad_producto": {"prod_006_01": 0.7, "prod_016_01": 0.6, "prod_013_02": 0.5, "prod_003_03": 0.4, "prod_025_03": 0.3, "prod_021_03": 0.2, "prod_022_03": 0.1, "prod_012_02": 0.1}
    },
    {"id": "int_040", "nombre": "Alimentación Infantil Saludable", "categoria_interes": "Familia",
        "afinidad_marca": {"marca_003": 0.9, "marca_006": 0.8, "marca_009": 0.7, "marca_016": 0.6, "marca_025": 0.5, "marca_022": 0.4, "marca_005": 0.3, "marca_021": 0.2},
        "afinidad_producto": {"prod_003_01": 0.9, "prod_006_01": 0.8, "prod_009_02": 0.7, "prod_016_01": 0.5, "prod_025_01": 0.4, "prod_022_01": 0.3, "prod_005_03": 0.2, "prod_021_01": 0.1}
    },
    {"id": "int_041", "nombre": "Salud Pediátrica y Vacunación", "categoria_interes": "Salud y Bienestar",
        "afinidad_marca": {"marca_008": 0.7, "marca_001": 0.6, "marca_018": 0.6, "marca_003": 0.4, "marca_006": 0.3, "marca_012": 0.2, "marca_017": 0.5, "marca_024": 0.3},
        "afinidad_producto": {"prod_008_03": 0.7, "prod_001_01": 0.5, "prod_018_01": 0.5, "prod_003_01": 0.3, "prod_006_01": 0.2, "prod_012_03": 0.1, "prod_017_02": 0.4, "prod_024_03": 0.2}
    },
    {"id": "int_042", "nombre": "Eventos Familiares y Recreación Urbana", "categoria_interes": "Entretenimiento",
        "afinidad_marca": {"marca_022": 0.7, "marca_012": 0.6, "marca_006": 0.5, "marca_023": 0.4, "marca_005": 0.5, "marca_019": 0.3, "marca_004": 0.2, "marca_020": 0.3},
        "afinidad_producto": {"prod_022_01": 0.7, "prod_012_02": 0.6, "prod_006_03": 0.4, "prod_023_01": 0.3, "prod_005_01": 0.5, "prod_019_01": 0.2, "prod_004_01": 0.1, "prod_020_02": 0.2}
    },
    {"id": "int_043", "nombre": "Apps de Organización Familiar y Productividad", "categoria_interes": "Tecnología",
        "afinidad_marca": {"marca_013": 0.7, "marca_012": 0.6, "marca_007": 0.5, "marca_011": 0.5, "marca_024": 0.4, "marca_006": 0.3, "marca_016": 0.4, "marca_001": 0.2},
        "afinidad_producto": {"prod_013_01": 0.6, "prod_012_01": 0.5, "prod_007_02": 0.4, "prod_011_02": 0.4, "prod_024_02": 0.3, "prod_006_02": 0.2, "prod_016_02": 0.3, "prod_001_01": 0.1}
    },
    {"id": "int_044", "nombre": "Viajes por Colombia (Internos)", "categoria_interes": "Viajes",
        "afinidad_marca": {"marca_004": 0.8, "marca_010": 0.8, "marca_020": 0.9, "marca_022": 0.4, "marca_012": 0.5, "marca_006": 0.3, "marca_015": 0.2, "marca_001": 0.1},
        "afinidad_producto": {"prod_004_01": 0.8, "prod_010_01": 0.8, "prod_020_01": 0.9, "prod_022_02": 0.3, "prod_012_03": 0.4, "prod_006_01": 0.2, "prod_015_03": 0.1, "prod_001_01": 0.1}
    },
    {"id": "int_045", "nombre": "Espacios de Coworking y Networking", "categoria_interes": "Negocios",
        "afinidad_marca": {"marca_012": 0.7, "marca_013": 0.6, "marca_024": 0.5, "marca_007": 0.4, "marca_001": 0.3, "marca_008": 0.3, "marca_006": 0.2, "marca_018": 0.4},
        "afinidad_producto": {"prod_012_01": 0.6, "prod_013_01": 0.5, "prod_024_01": 0.4, "prod_007_02": 0.3, "prod_001_02": 0.2, "prod_008_01": 0.2, "prod_006_02": 0.1, "prod_018_03": 0.3}
    },
    {"id": "int_046", "nombre": "Comunidades de Nómadas Digitales", "categoria_interes": "Estilo de Vida",
        "afinidad_marca": {"marca_012": 0.8, "marca_023": 0.7, "marca_020": 0.6, "marca_026": 0.5, "marca_013": 0.4, "marca_004": 0.3, "marca_022": 0.4, "marca_024": 0.5},
        "afinidad_producto": {"prod_012_01": 0.7, "prod_023_01": 0.6, "prod_020_02": 0.5, "prod_026_02": 0.4, "prod_013_02": 0.3, "prod_004_01": 0.2, "prod_022_01": 0.3, "prod_024_02": 0.4}
    },
    {"id": "int_047", "nombre": "Seguros de Viaje y Asistencia Médica Internacional", "categoria_interes": "Finanzas Personales",
        "afinidad_marca": {"marca_001": 0.7, "marca_008": 0.7, "marca_018": 0.6, "marca_004": 0.5, "marca_010": 0.5, "marca_012": 0.3, "marca_007": 0.2, "marca_017": 0.3},
        "afinidad_producto": {"prod_001_02": 0.6, "prod_008_03": 0.7, "prod_018_01": 0.5, "prod_004_02": 0.4, "prod_010_02": 0.4, "prod_012_01": 0.2, "prod_007_03": 0.1, "prod_017_03": 0.3}
    },
    {"id": "int_048", "nombre": "Redes Sociales para Conexión Familiar", "categoria_interes": "Tecnología",
        "afinidad_marca": {"marca_007": 0.8, "marca_011": 0.8, "marca_017": 0.7, "marca_012": 0.6, "marca_013": 0.5, "marca_023": 0.4, "marca_006": 0.3, "marca_024": 0.2},
        "afinidad_producto": {"prod_007_01": 0.7, "prod_011_01": 0.7, "prod_017_01": 0.6, "prod_012_02": 0.5, "prod_013_01": 0.4, "prod_023_01": 0.3, "prod_006_01": 0.2, "prod_024_03": 0.1}
    },
    {"id": "int_049", "nombre": "Cursos Online para Hobbies (Mayores)", "categoria_interes": "Educación",
        "afinidad_marca": {"marca_024": 0.9, "marca_023": 0.7, "marca_013": 0.6, "marca_006": 0.5, "marca_012": 0.4, "marca_007": 0.3, "marca_021": 0.2, "marca_003": 0.4},
        "afinidad_producto": {"prod_024_02": 0.9, "prod_023_01": 0.6, "prod_013_02": 0.5, "prod_006_03": 0.4, "prod_012_01": 0.3, "prod_007_03": 0.2, "prod_021_01": 0.1, "prod_003_02": 0.3}
    },
    {"id": "int_050", "nombre": "Servicios a Domicilio por Apps", "categoria_interes": "Estilo de Vida",
        "afinidad_marca": {"marca_012": 0.9, "marca_022": 0.8, "marca_006": 0.7, "marca_016": 0.6, "marca_005": 0.5, "marca_013": 0.4, "marca_025": 0.3, "marca_003": 0.2},
        "afinidad_producto": {"prod_012_02": 0.9, "prod_022_01": 0.8, "prod_006_01": 0.7, "prod_016_01": 0.5, "prod_005_01": 0.4, "prod_013_01": 0.3, "prod_025_01": 0.2, "prod_003_01": 0.1}
    },
    {"id": "int_051", "nombre": "Viajes Culturales Adaptados (Mayores)", "categoria_interes": "Viajes",
        "afinidad_marca": {"marca_004": 0.8, "marca_010": 0.8, "marca_008": 0.6, "marca_001": 0.5, "marca_020": 0.4, "marca_012": 0.3, "marca_006": 0.2, "marca_019": 0.3},
        "afinidad_producto": {"prod_004_02": 0.8, "prod_010_02": 0.8, "prod_008_03": 0.5, "prod_001_01": 0.4, "prod_020_01": 0.3, "prod_012_02": 0.2, "prod_006_01": 0.1, "prod_019_03": 0.2}
    },
    {"id": "int_052", "nombre": "Ciberseguridad Personal y Familiar", "categoria_interes": "Tecnología",
        "afinidad_marca": {"marca_007": 0.8, "marca_011": 0.7, "marca_013": 0.6, "marca_001": 0.5, "marca_008": 0.5, "marca_024": 0.4, "marca_012": 0.3, "marca_017": 0.6},
        "afinidad_producto": {"prod_007_02": 0.7, "prod_011_02": 0.6, "prod_013_03": 0.5, "prod_001_01": 0.4, "prod_008_01": 0.4, "prod_024_02": 0.3, "prod_012_01": 0.2, "prod_017_01": 0.5}
    },
    {"id": "int_053", "nombre": "Blockchain, NFTs y Web3", "categoria_interes": "Tecnología",
        "afinidad_marca": {"marca_013": 0.8, "marca_012": 0.7, "marca_024": 0.6, "marca_001": 0.4, "marca_008": 0.3, "marca_007": 0.2, "marca_023": 0.5, "marca_018": 0.2},
        "afinidad_producto": {"prod_013_03": 0.7, "prod_012_01": 0.6, "prod_024_01": 0.5, "prod_001_02": 0.3, "prod_008_02": 0.2, "prod_007_01": 0.1, "prod_023_03": 0.4, "prod_018_02": 0.1}
    },
    {"id": "int_054", "nombre": "Voluntariado Social y Comunitario", "categoria_interes": "Estilo de Vida",
        "afinidad_marca": {"marca_001": 0.6, "marca_008": 0.6, "marca_018": 0.5, "marca_003": 0.4, "marca_024": 0.7, "marca_026": 0.5, "marca_006": 0.3, "marca_005": 0.2},
        "afinidad_producto": {"prod_001_01": 0.5, "prod_008_01": 0.5, "prod_018_02": 0.4, "prod_003_01": 0.3, "prod_024_01": 0.6, "prod_026_01": 0.4, "prod_006_01": 0.2, "prod_005_02": 0.1}
    },
    {"id": "int_055", "nombre": "Juegos Mentales y Agilidad Cognitiva Online", "categoria_interes": "Salud y Bienestar",
        "afinidad_marca": {"marca_024": 0.8, "marca_023": 0.7, "marca_013": 0.6, "marca_007": 0.5, "marca_012": 0.4, "marca_006": 0.3, "marca_011": 0.5, "marca_016": 0.2},
        "afinidad_producto": {"prod_024_02": 0.8, "prod_023_01": 0.7, "prod_013_01": 0.5, "prod_007_03": 0.4, "prod_012_01": 0.3, "prod_006_02": 0.2, "prod_011_03": 0.4, "prod_016_02": 0.1}
    },
    {"id": "int_056", "nombre": "Inversión de Impacto Social y Ambiental", "categoria_interes": "Finanzas Personales",
        "afinidad_marca": {"marca_001": 0.7, "marca_008": 0.6, "marca_018": 0.7, "marca_026": 0.5, "marca_010": 0.4, "marca_024": 0.3, "marca_002": 0.5, "marca_014": 0.2},
        "afinidad_producto": {"prod_001_02": 0.6, "prod_008_03": 0.5, "prod_018_02": 0.7, "prod_026_01": 0.4, "prod_010_02": 0.3, "prod_024_02": 0.2, "prod_002_03": 0.4, "prod_014_01": 0.1}
    },
    {"id": "int_057", "nombre": "Turismo Ecológico y Comunitario", "categoria_interes": "Viajes",
        "afinidad_marca": {"marca_026": 0.8, "marca_004": 0.6, "marca_010": 0.6, "marca_020": 0.5, "marca_012": 0.4, "marca_022": 0.3, "marca_002": 0.7, "marca_003": 0.2},
        "afinidad_producto": {"prod_026_02": 0.8, "prod_004_01": 0.5, "prod_010_01": 0.5, "prod_020_01": 0.4, "prod_012_03": 0.3, "prod_022_02": 0.2, "prod_002_01": 0.6, "prod_003_01": 0.1}
    },
    {"id": "int_058", "nombre": "Inversión en Bienes Raíces", "categoria_interes": "Finanzas Personales",
        "afinidad_marca": {"marca_001": 0.9, "marca_008": 0.8, "marca_018": 0.8, "marca_014": 0.6, "marca_021": 0.7, "marca_013": 0.5, "marca_006": 0.4, "marca_012": 0.3},
        "afinidad_producto": {"prod_001_03": 0.9, "prod_008_03": 0.8, "prod_018_01": 0.7, "prod_014_01": 0.5, "prod_021_02": 0.6, "prod_013_01": 0.4, "prod_006_02": 0.3, "prod_012_01": 0.2}
    },
    {"id": "int_059", "nombre": "Cocina Vegana y Basada en Plantas", "categoria_interes": "Gastronomía",
        "afinidad_marca": {"marca_003": 0.7, "marca_009": 0.6, "marca_006": 0.8, "marca_016": 0.5, "marca_026": 0.8, "marca_022": 0.4, "marca_012": 0.3, "marca_005": 0.2},
        "afinidad_producto": {"prod_003_02": 0.6, "prod_009_02": 0.5, "prod_006_01": 0.8, "prod_016_01": 0.4, "prod_026_01": 0.9, "prod_022_01": 0.3, "prod_012_02": 0.2, "prod_005_02": 0.1}
    },
    {"id": "int_060", "nombre": "Podcasting y Creación de Contenido Audio", "categoria_interes": "Entretenimiento",
        "afinidad_marca": {"marca_023": 0.8, "marca_007": 0.7, "marca_011": 0.6, "marca_013": 0.5, "marca_024": 0.6, "marca_012": 0.4, "marca_017": 0.5, "marca_001": 0.2},
        "afinidad_producto": {"prod_023_03": 0.8, "prod_007_01": 0.6, "prod_011_01": 0.5, "prod_013_03": 0.4, "prod_024_02": 0.5, "prod_012_01": 0.3, "prod_017_01": 0.4, "prod_001_01": 0.1}
    }
]

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
        "kpi_primario": "interacciones_calculadas"
    },
    {
        "id": "conversion",
        "nombre": "Conversiones",
        "descripcion": "Impulsar acciones específicas valiosas en el sitio web (e.g., compras, registros).",
        "kpi_primario": "conversiones_calculadas"
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
