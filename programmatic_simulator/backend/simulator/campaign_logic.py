# programmatic_simulator/backend/simulator/campaign_logic.py
import random
from programmatic_simulator.backend.data import market_data

# Constantes base para la simulación (simplificadas por ahora)
COSTO_POR_MIL_IMPRESIONES_BASE = 10000  # COP
CTR_BASE = 0.01  # Click-Through Rate base (1%)

def simular_campana(marca_id, audiencia_id, presupuesto):
    """
    Simula una campaña programática básica.
    Devuelve un diccionario con la puntuación y las métricas.
    """
    marca = market_data.obtener_marca_por_id(marca_id)
    audiencia = market_data.obtener_audiencia_por_id(audiencia_id)

    if not marca or not audiencia:
        return {
            "error": "Marca o audiencia no encontrada.",
            "puntuacion": 0,
            "impresiones": 0,
            "clics": 0,
            "cpm_calculado": 0,
            "cpc_calculado": 0,
            "presupuesto_gastado": 0
        }

    # Lógica de puntuación muy simple (mejorable)
    puntuacion = 5 # Puntuación base

    # Ajustar puntuación basada en la afinidad de la audiencia con la categoría de la marca
    afinidad = audiencia["afinidad_marca_categoria"].get(marca["categoria"], 0.1) # Afinidad base si no está la categoría

    if afinidad >= 0.7:
        puntuacion += 3
    elif afinidad >= 0.4:
        puntuacion += 1
    else:
        puntuacion -= 2

    # Simular gasto y métricas
    # Por ahora, asumimos que se gasta todo el presupuesto si es posible

    impresiones_posibles_brutas = (presupuesto / COSTO_POR_MIL_IMPRESIONES_BASE) * 1000

    # Ajustar impresiones por afinidad (más afinidad, mejor alcance efectivo)
    impresiones_efectivas = int(impresiones_posibles_brutas * (afinidad + 0.5)) # El +0.5 es para que no sea tan bajo

    # Asegurar que la puntuación no baje demasiado solo por presupuesto bajo
    if presupuesto < 50000: # Presupuesto muy bajo
        puntuacion -= 1
    elif presupuesto > 1000000: # Presupuesto alto
        puntuacion +=1

    # Limitar puntuación entre 1 y 10
    puntuacion = max(1, min(10, puntuacion))

    # Calcular clics basados en un CTR ajustado por afinidad
    ctr_ajustado = CTR_BASE * (1 + afinidad) # Mejor afinidad, mejor CTR
    clics = int(impresiones_efectivas * ctr_ajustado * random.uniform(0.8, 1.2)) # Pequeña variabilidad

    impresiones = impresiones_efectivas # En esta simulación simple, todas las efectivas se consideran "entregadas"

    presupuesto_gastado = (impresiones / 1000) * COSTO_POR_MIL_IMPRESIONES_BASE

    # Si el presupuesto gastado excede el presupuesto inicial (por ajustes de afinidad), limitarlo.
    if presupuesto_gastado > presupuesto:
        presupuesto_gastado = presupuesto
        # Recalcular impresiones si el presupuesto es el limitante
        impresiones = int((presupuesto_gastado / COSTO_POR_MIL_IMPRESIONES_BASE) * 1000)
        clics = int(impresiones * ctr_ajustado * random.uniform(0.8, 1.2))


    cpm_calculado = (presupuesto_gastado / impresiones * 1000) if impresiones > 0 else 0
    cpc_calculado = (presupuesto_gastado / clics) if clics > 0 else 0

    # Añadir un pequeño factor aleatorio a la puntuación final para simular "ruido" del mercado
    puntuacion += random.choice([-1, 0, 0, 1]) # Más probabilidad de 0
    puntuacion = max(1, min(10, puntuacion))


    return {
        "marca_nombre": marca["nombre"],
        "audiencia_nombre": audiencia["nombre"],
        "presupuesto_inicial": presupuesto,
        "puntuacion": puntuacion,
        "impresiones": impresiones,
        "clics": clics,
        "cpm_calculado": round(cpm_calculado, 2), # Costo Por Mil impresiones
        "cpc_calculado": round(cpc_calculado, 2),   # Costo Por Clic
        "presupuesto_gastado": round(presupuesto_gastado, 2),
        "mensaje": f"Campaña para {marca['nombre']} dirigida a {audiencia['nombre']} con presupuesto {presupuesto}."
    }

if __name__ == '__main__':
    # Ejemplo de uso (esto no se ejecutará cuando se importe desde Flask)
    marca_ejemplo = market_data.MARCAS_COLOMBIANAS[0]["id"]
    audiencia_ejemplo = market_data.AUDIENCIAS_COLOMBIANAS[0]["id"]
    presupuesto_ejemplo = 200000  # 200,000 COP

    resultado = simular_campana(marca_ejemplo, audiencia_ejemplo, presupuesto_ejemplo)
    print(resultado)

    marca_ejemplo_2 = market_data.MARCAS_COLOMBIANAS[2]["id"] # Alpina
    audiencia_ejemplo_2 = market_data.AUDIENCIAS_COLOMBIANAS[3]["id"] # Familias con Hijos
    presupuesto_ejemplo_2 = 500000
    resultado_2 = simular_campana(marca_ejemplo_2, audiencia_ejemplo_2, presupuesto_ejemplo_2)
    print(resultado_2)

    # Ejemplo con baja afinidad
    marca_ejemplo_3 = market_data.MARCAS_COLOMBIANAS[1]["id"] # Ecopetrol
    audiencia_ejemplo_3 = market_data.AUDIENCIAS_COLOMBIANAS[0]["id"] # Jovenes Universitarios
    presupuesto_ejemplo_3 = 100000
    resultado_3 = simular_campana(marca_ejemplo_3, audiencia_ejemplo_3, presupuesto_ejemplo_3)
    print(resultado_3)
