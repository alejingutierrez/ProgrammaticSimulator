# programmatic_simulator/backend/simulator/campaign_logic.py
import random
import math
from data import market_data

# --- Constantes de Simulación y Puntuación ---
COSTO_POR_MIL_IMPRESIONES_BASE = 12000  # COP
CTR_BASE_DEFAULT = 0.008               # Click-Through Rate base (0.8%)
DEFAULT_CAMPAIGN_GOAL_ID = "traffic"   # Objetivo por defecto si no se especifica
INTEREST_PENETRATION_ESTIMATE = 0.3    # 30% - Estimado de penetración de un interés en un segmento de audiencia

# Puntuación
PUNTUACION_INICIAL = 3.0             # Puntuación base antes de modificadores
MAX_PUNTOS_POR_FACTOR = 2.5          # Máx puntos que afinidad, intereses u objetivo pueden sumar individualmente
PENALIDAD_FUERTE_TARGETING = -2.0    # Penalización por muy mala afinidad o selección de intereses
PENALIDAD_SUAVE_TARGETING = -1.0     # Penalización por afinidad/intereses mediocres
BONUS_BUEN_TARGETING = 1.5           # Bonus por excelente afinidad/intereses

# Presupuesto
PRESUPUESTO_MINIMO_IMPACTO = 50000   # Por debajo de esto, la campaña podría ser inefectiva
PRESUPUESTO_BAJO = 150000            # Umbral para considerar presupuesto bajo
PRESUPUESTO_ALTO = 1000000           # Umbral para considerar presupuesto alto
PUNTOS_PRESUESTO_BAJO = -0.5
PUNTOS_PRESUESTO_ALTO = 0.5
PUNTOS_PRESUESTO_MUY_BAJO = -1.0     # Si es demasiado bajo para el objetivo

# Modificadores de Métricas por Objetivo
GOAL_CTR_MODIFIERS = {
    "traffic": 1.15,    # Aumenta el CTR base para objetivo de tráfico
    "engagement": 1.1,
    "conversion": 1.2,  # Aumenta más el CTR para conversiones
    "awareness": 0.9    # Reduce ligeramente el CTR si el foco es solo impresiones
}
GOAL_IMPRESSION_MODIFIERS = {
    "awareness": 1.1 # Ligero aumento de impresiones si el objetivo es reconocimiento
}

# Tasas base para Interacción y Conversión (estos son placeholders y muy simplificados)
BASE_ENGAGEMENT_RATE_PER_CLICK = 0.06  # 6% de los clics generan alguna interacción base
BASE_CONVERSION_RATE_PER_CLICK = 0.0075 # 0.75% de los clics convierten base

def _normalize_text_for_matching(text):
    if not text: return ""
    text = str(text).lower()
    text = text.replace('_', ' ')
    accent_map = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u'}
    for accented, unaccented in accent_map.items():
        text = text.replace(accented, unaccented)
    return " ".join(text.split()) # Collapse multiple spaces and strip leading/trailing

def simular_campana(marca_id, audiencia_id, presupuesto, selected_interes_ids=None, campaign_goal_id=None):
    marca = market_data.obtener_marca_por_id(marca_id)
    audiencia = market_data.obtener_audiencia_por_id(audiencia_id)

    goal_id_to_use = campaign_goal_id or DEFAULT_CAMPAIGN_GOAL_ID
    campaign_goal = market_data.obtener_campaign_goal_por_id(goal_id_to_use)
    if not campaign_goal:
        campaign_goal = market_data.obtener_campaign_goal_por_id(DEFAULT_CAMPAIGN_GOAL_ID)

    mensajes_feedback = []

    if not marca or not audiencia:
        mensajes_feedback.append("Error crítico: Marca o audiencia no encontrada.")
        return {
            "error": "Marca o audiencia no encontrada.", "puntuacion": 0, "impresiones": 0,
            "clics": 0, "ctr_calculado":0, "cpm_calculado": 0, "cpc_calculado": 0,
            "presupuesto_gastado": 0, "interest_match_score": 0, "selected_intereses_nombres": [],
            "campaign_goal_nombre": campaign_goal["nombre"] if campaign_goal else "N/A",
            "interacciones_calculadas":0, "conversiones_calculadas":0, "afinidad_marca_audiencia":0,
            "mensajes_feedback": mensajes_feedback,
            "potential_audience_size_from_segment": 0, # Ensure key exists even in error
            "refined_potential_audience_size": 0 # Ensure key exists even in error
        }

    # --- Determinación del Tamaño de Audiencia Potencial por Segmento ---
    potential_audience_size_from_segment = 20000000 # Default grande
    all_population_segments = market_data.obtener_todos_los_segmentos_poblacion()
    found_segment = False
    if all_population_segments:
        relevant_segments = [
            seg for seg in all_population_segments
            if audiencia["id"] in seg.get("relates_to_audience_ids", [])
        ]
        if relevant_segments:
            # Usar el segmento más pequeño como el más específico
            relevant_segments.sort(key=lambda s: s["size"])
            potential_audience_size_from_segment = relevant_segments[0]["size"]
            mensajes_feedback.append(f"INFO: Segmento de población '{relevant_segments[0]['nombre_segmento']}' (tamaño: {potential_audience_size_from_segment:,}) usado para estimar alcance máximo.")
            found_segment = True
            if potential_audience_size_from_segment < 1000000:
                 mensajes_feedback.append("INFO: El segmento de audiencia seleccionado es bastante específico, lo que podría limitar el alcance máximo.")
        else:
            # Si no hay segmento directo, usar una porción de la población total si está disponible
            total_col_segment = next((s for s in all_population_segments if s["segment_id"] == "total_colombia"), None)
            if total_col_segment:
                potential_audience_size_from_segment = int(total_col_segment["size"] * 0.25) # Estimación general
                mensajes_feedback.append(f"INFO: No se encontró un segmento de población directamente relacionado. Usando estimación basada en población total ({potential_audience_size_from_segment:,}).")


    puntuacion_actual = PUNTUACION_INICIAL
    afinidad_marca_audiencia = audiencia["afinidad_marca_categoria"].get(marca["categoria"], 0.05)

    if afinidad_marca_audiencia >= 0.7: puntuacion_actual += BONUS_BUEN_TARGETING
    elif afinidad_marca_audiencia >= 0.4: puntuacion_actual += (BONUS_BUEN_TARGETING / 2)
    elif afinidad_marca_audiencia < 0.2: puntuacion_actual += PENALIDAD_FUERTE_TARGETING
    else: puntuacion_actual += PENALIDAD_SUAVE_TARGETING

    selected_intereses_nombres = []
    num_selected_intereses = len(selected_interes_ids) if selected_interes_ids else 0

    if num_selected_intereses > 0:
        audiencia_intereses_clave_orig = audiencia.get("intereses_clave", [])
        audiencia_intereses_clave_set_orig = set(audiencia_intereses_clave_orig)

        if not audiencia_intereses_clave_orig:
            interest_match_score = 0.1
        else:
            matched_count = 0
            for interes_id_from_selection in selected_interes_ids:
                interes_obj = market_data.obtener_interes_por_id(interes_id_from_selection)
                if interes_obj:
                    selected_intereses_nombres.append(interes_obj["nombre"])

                    interes_nombre_normalized_tokens = set(_normalize_text_for_matching(interes_obj["nombre"]).split())
                    if "" in interes_nombre_normalized_tokens: interes_nombre_normalized_tokens.remove("")
                    if not interes_nombre_normalized_tokens:
                        interes_nombre_normalized_tokens = set(["__EMPTY_INTEREST_NAME_TOKEN_AVOID_FALSE_POSITIVE__"])

                    matched_this_interest = False
                    if interes_obj["id"] in audiencia_intereses_clave_set_orig:
                        matched_this_interest = True
                    else:
                        for aud_clave_orig_text in audiencia_intereses_clave_orig:
                            aud_clave_normalized_tokens = set(_normalize_text_for_matching(aud_clave_orig_text).split())
                            if "" in aud_clave_normalized_tokens: aud_clave_normalized_tokens.remove("")

                            if not aud_clave_normalized_tokens:
                                continue

                            if aud_clave_normalized_tokens.issubset(interes_nombre_normalized_tokens):
                                matched_this_interest = True
                                break
                    if matched_this_interest:
                        matched_count += 1

            if num_selected_intereses == 0: interest_match_score = 0.3
            else:
                raw_match_prop = matched_count / num_selected_intereses
                if num_selected_intereses > 6 and raw_match_prop < 0.4: interest_match_score = raw_match_prop * 0.6
                elif num_selected_intereses > 0 and num_selected_intereses < 2 and raw_match_prop < 0.5 : interest_match_score = raw_match_prop * 0.7
                else: interest_match_score = raw_match_prop
                if matched_count == 0 and num_selected_intereses > 0: interest_match_score = 0.05
                elif matched_count > 0 and interest_match_score < 0.15: interest_match_score = 0.15
    else:
        interest_match_score = 0.35

    if num_selected_intereses > 0:
        if interest_match_score >= 0.7: puntuacion_actual += BONUS_BUEN_TARGETING
        elif interest_match_score >= 0.4: puntuacion_actual += (BONUS_BUEN_TARGETING / 2)
        elif interest_match_score < 0.15: puntuacion_actual += PENALIDAD_FUERTE_TARGETING
        else: puntuacion_actual += PENALIDAD_SUAVE_TARGETING
    else: puntuacion_actual += PENALIDAD_SUAVE_TARGETING

    efectividad_targeting_combinada = (afinidad_marca_audiencia + interest_match_score) / 2
    if afinidad_marca_audiencia < 0.2 or \
       (num_selected_intereses > 0 and interest_match_score < 0.15) or \
       (num_selected_intereses == 0 and interest_match_score <= 0.35):
        efectividad_targeting_combinada *= 0.6
    efectividad_targeting_combinada = max(0.05, min(1.0, efectividad_targeting_combinada))

    impresiones_posibles_brutas = (presupuesto / COSTO_POR_MIL_IMPRESIONES_BASE) * 1000
    impresion_goal_modifier = GOAL_IMPRESSION_MODIFIERS.get(campaign_goal["id"], 1.0)
    factor_alcance_efectivo = efectividad_targeting_combinada * 0.7 + 0.2
    if presupuesto > PRESUPUESTO_ALTO: factor_alcance_efectivo = min(1.0, factor_alcance_efectivo * 1.1)
    impresiones_efectivas = int(impresiones_posibles_brutas * factor_alcance_efectivo * impresion_goal_modifier)

    # --- Refinar Audiencia por Intereses y Limitar Impresiones por Población ---
    if num_selected_intereses > 0:
        # Aplicar reducción por cada capa de interés (placeholder)
        refined_potential_audience_size = potential_audience_size_from_segment * (INTEREST_PENETRATION_ESTIMATE ** (num_selected_intereses * 0.5))
        refined_potential_audience_size = max(1000, int(refined_potential_audience_size)) # Mínimo 1000 personas
    else:
        refined_potential_audience_size = potential_audience_size_from_segment

    if impresiones_efectivas > refined_potential_audience_size:
        impresiones_efectivas = refined_potential_audience_size
        mensajes_feedback.append("INFO: El alcance de la campaña (impresiones) ha sido limitado por el tamaño estimado del segmento de audiencia y los intereses seleccionados.")

    impresiones_efectivas = max(0, impresiones_efectivas)

    ctr_actual = CTR_BASE_DEFAULT * GOAL_CTR_MODIFIERS.get(campaign_goal["id"], 1.0)
    ctr_final_calculado = ctr_actual * (1 + (efectividad_targeting_combinada * 1.5))
    ctr_final_calculado = max(0.0001, ctr_final_calculado)
    clics = int(impresiones_efectivas * ctr_final_calculado * random.uniform(0.85, 1.15))
    impresiones = impresiones_efectivas

    interacciones_calculadas = 0
    conversiones_calculadas = 0
    if campaign_goal["id"] == "engagement":
        # Nueva fórmula de engagement_rate
        engagement_rate = BASE_ENGAGEMENT_RATE_PER_CLICK * \
                          (1 + (afinidad_marca_audiencia * 0.5) + \
                           (interest_match_score * 0.75) + \
                           (GOAL_CTR_MODIFIERS.get(campaign_goal["id"], 1.0) - 1.0) * 0.5)
        interacciones_calculadas = int(clics * engagement_rate * random.uniform(0.8, 1.2))
    elif campaign_goal["id"] == "conversion":
        # Nueva fórmula de conversion_rate
        conversion_rate_base_multiplier = 1.0
        if campaign_goal["id"] == "conversion": conversion_rate_base_multiplier = 1.5 # Stronger push for conversion goal

        conversion_rate = BASE_CONVERSION_RATE_PER_CLICK * conversion_rate_base_multiplier
        conversion_rate *= (1 + (afinidad_marca_audiencia * 0.8) + (interest_match_score * 1.2)) # Affinity and interest match have strong impact

        if afinidad_marca_audiencia < 0.3:
            conversion_rate *= 0.4
        if interest_match_score < 0.3 and num_selected_intereses > 0:
            conversion_rate *= 0.4
        elif efectividad_targeting_combinada < 0.5: # General poor targeting (catches cases where one is low but not both, or no interests)
             conversion_rate *= 0.7

        conversiones_calculadas = int(clics * conversion_rate * random.uniform(0.7, 1.3))
        conversiones_calculadas = max(0, conversiones_calculadas)

    puntos_objetivo = 0
    if campaign_goal["id"] == "traffic":
        ctr_esperado_min = CTR_BASE_DEFAULT * 1.2; ctr_esperado_bueno = CTR_BASE_DEFAULT * 1.8
        if ctr_final_calculado >= ctr_esperado_bueno: puntos_objetivo += MAX_PUNTOS_POR_FACTOR
        elif ctr_final_calculado >= ctr_esperado_min: puntos_objetivo += MAX_PUNTOS_POR_FACTOR / 2
        else: puntos_objetivo -= MAX_PUNTOS_POR_FACTOR / 2
        clics_esperados_min_por_millon_presupuesto = (1000000 / COSTO_POR_MIL_IMPRESIONES_BASE * 1000) * ctr_esperado_min * 0.5
        if presupuesto > PRESUPUESTO_BAJO and clics < clics_esperados_min_por_millon_presupuesto * (presupuesto/1000000):
            puntos_objetivo -= 0.5
    elif campaign_goal["id"] == "awareness":
        reach_percentage_of_potential = impresiones_efectivas / refined_potential_audience_size if refined_potential_audience_size > 0 else 0
        if reach_percentage_of_potential >= 0.7 and impresiones_efectivas > refined_potential_audience_size * 0.1: # Asegurar que no es un % alto de un número muy pequeño de impresiones
            puntos_objetivo += MAX_PUNTOS_POR_FACTOR
        elif reach_percentage_of_potential >= 0.4 and impresiones_efectivas > refined_potential_audience_size * 0.05:
            puntos_objetivo += MAX_PUNTOS_POR_FACTOR / 2
        else:
            puntos_objetivo -= MAX_PUNTOS_POR_FACTOR / 2 # Penalización más suave que antes si no se alcanza buen %

        # Bonus/Penalización por presupuesto vs alcance potencial
        # Estimación de impresiones máximas que el presupuesto podría comprar (sin considerar efectividad de targeting aún)
        max_impressions_budget_could_buy = (presupuesto / COSTO_POR_MIL_IMPRESIONES_BASE) * 1000
        if max_impressions_budget_could_buy > refined_potential_audience_size * 1.5 and reach_percentage_of_potential < 0.5:
            puntos_objetivo -= 0.5 # Penalize if budget was high but reach was low relative to potential
            mensajes_feedback.append("INFO: El presupuesto parecía suficiente para un mayor alcance del segmento potencial. La segmentación o el atractivo de la campaña podrían haber limitado las impresiones.")
        elif max_impressions_budget_could_buy < refined_potential_audience_size * 0.5 and reach_percentage_of_potential > 0.3:
            puntos_objetivo += 0.5 # Bonus if budget was low but still achieved decent relative reach
            mensajes_feedback.append("INFO: Buen aprovechamiento del presupuesto para alcanzar un porcentaje considerable del segmento potencial.")

    elif campaign_goal["id"] == "engagement":
        if clics > 0 :
            tasa_interaccion_efectiva = interacciones_calculadas / clics
            if tasa_interaccion_efectiva >= BASE_ENGAGEMENT_RATE_PER_CLICK*2.5: puntos_objetivo += MAX_PUNTOS_POR_FACTOR
            elif tasa_interaccion_efectiva >= BASE_ENGAGEMENT_RATE_PER_CLICK*1.5: puntos_objetivo += MAX_PUNTOS_POR_FACTOR/2
            else: puntos_objetivo -= MAX_PUNTOS_POR_FACTOR / 2
        else: puntos_objetivo -= MAX_PUNTOS_POR_FACTOR
    elif campaign_goal["id"] == "conversion":
        if clics > 0:
            tasa_conversion_efectiva = conversiones_calculadas / clics
            if tasa_conversion_efectiva >= BASE_CONVERSION_RATE_PER_CLICK*3: puntos_objetivo += MAX_PUNTOS_POR_FACTOR
            elif tasa_conversion_efectiva >= BASE_CONVERSION_RATE_PER_CLICK*1.5: puntos_objetivo += MAX_PUNTOS_POR_FACTOR/2
            else: puntos_objetivo -= MAX_PUNTOS_POR_FACTOR /1.5
            if conversiones_calculadas == 0 and presupuesto > PRESUPUESTO_BAJO: puntos_objetivo -= 1.0
        else: puntos_objetivo -= MAX_PUNTOS_POR_FACTOR
    puntuacion_actual += puntos_objetivo

    if presupuesto < PRESUPUESTO_MINIMO_IMPACTO :
        puntuacion_actual += PUNTOS_PRESUESTO_MUY_BAJO
        if campaign_goal['id'] in ['awareness', 'conversion']: puntuacion_actual -= 0.5
    elif presupuesto < PRESUPUESTO_BAJO: puntuacion_actual += PUNTOS_PRESUESTO_BAJO
    elif presupuesto > PRESUPUESTO_ALTO: puntuacion_actual += PUNTOS_PRESUESTO_ALTO

    puntuacion_actual = max(1.0, min(10.0, puntuacion_actual))
    ruido_mercado = random.choice([-0.5, 0, 0, 0, 0.5])
    puntuacion_final_con_ruido = round(max(1.0, min(10.0, puntuacion_actual + ruido_mercado)))

    # --- Feedback generation ---
    if afinidad_marca_audiencia >= 0.7:
        mensajes_feedback.append("POSITIVO: ¡Buena elección! La audiencia parece tener una alta afinidad con la categoría de la marca.")
    elif afinidad_marca_audiencia >= 0.4: # Catches 0.4 to 0.69
        mensajes_feedback.append("SUGERENCIA: La afinidad marca-audiencia es moderada. Podrías explorar audiencias con mayor afinidad natural o refinar intereses.")
    elif afinidad_marca_audiencia >= 0.2: # Catches 0.2 to 0.39
        mensajes_feedback.append("SUGERENCIA: La afinidad marca-audiencia es baja pero no crítica. Considera mejorarla o asegurar un excelente targeting de intereses.")
    else: # Less than 0.2
        mensajes_feedback.append("ALERTA: La afinidad entre la marca y la audiencia es muy baja. Considera si esta es la audiencia adecuada o si necesitas un targeting de intereses extremadamente preciso.")

    if num_selected_intereses > 0:
        if interest_match_score < 0.15: mensajes_feedback.append("ALERTA: Los intereses seleccionados no coinciden NADA con los intereses clave de la audiencia. Esto está afectando muy negativamente el rendimiento.")
        elif interest_match_score < 0.35: mensajes_feedback.append("SUGERENCIA: Los intereses seleccionados tienen una coincidencia baja con la audiencia. Revisa los intereses clave de tu audiencia para optimizar.")
        elif interest_match_score >= 0.7: mensajes_feedback.append("POSITIVO: ¡Excelente segmentación por intereses! Los intereses seleccionados son muy relevantes para la audiencia.")
        if num_selected_intereses > 6 : mensajes_feedback.append("INFO: Has seleccionado muchos intereses. Esto podría ampliar demasiado el público y diluir el enfoque, a menos que todos sean altamente relevantes.")
    else: mensajes_feedback.append("INFO: No seleccionaste intereses específicos. Aunque esto puede dar un alcance amplio, refinar los intereses suele mejorar el rendimiento y la puntuación, especialmente si la afinidad no es muy alta.")

    if presupuesto < PRESUPUESTO_MINIMO_IMPACTO :
        msg_presupuesto = "ALERTA: El presupuesto es muy bajo y probablemente esté limitando severamente el alcance y la efectividad de la campaña"
        if campaign_goal['id'] in ['awareness', 'conversion']: msg_presupuesto += f", especialmente para un objetivo de '{campaign_goal['nombre']}'."
        else: msg_presupuesto += "."
        mensajes_feedback.append(msg_presupuesto)
    elif presupuesto < PRESUPUESTO_BAJO: mensajes_feedback.append("SUGERENCIA: El presupuesto es algo ajustado. Considera aumentarlo para mejorar los resultados si el rendimiento inicial es bueno.")

    kpi_primario = campaign_goal.get("kpi_primario", "ninguno")
    if kpi_primario == "impresiones" and puntos_objetivo < MAX_PUNTOS_POR_FACTOR/2: mensajes_feedback.append(f"SUGERENCIA: Para el objetivo de '{campaign_goal['nombre']}', las impresiones son más bajas de lo ideal. Revisa tu presupuesto y la efectividad de tu segmentación.")
    elif kpi_primario == "clics" and puntos_objetivo < MAX_PUNTOS_POR_FACTOR/2: mensajes_feedback.append(f"SUGERENCIA: El rendimiento de clics (CTR o volumen) es bajo para el objetivo de '{campaign_goal['nombre']}'. Considera optimizar la audiencia, intereses o creativos.")
    elif kpi_primario == "interacciones_calculadas" and puntos_objetivo < MAX_PUNTOS_POR_FACTOR/2: mensajes_feedback.append(f"SUGERENCIA: Las interacciones estimadas son bajas. Para '{campaign_goal['nombre']}', busca audiencias e intereses que naturalmente generen más participación.")
    elif kpi_primario == "conversiones_calculadas" and puntos_objetivo < MAX_PUNTOS_POR_FACTOR/2:
        msg_conversion = f"SUGERENCIA: Las conversiones son bajas para el objetivo '{campaign_goal['nombre']}'. Este es un objetivo desafiante."
        if presupuesto < PRESUPUESTO_ALTO : msg_conversion += " Lograr conversiones a menudo requiere una inversión mayor y una segmentación muy precisa."
        else: msg_conversion += " Asegúrate de que la audiencia y los intereses estén perfectamente alineados con la oferta."
        mensajes_feedback.append(msg_conversion)
        if conversiones_calculadas == 0 and clics > 10 : mensajes_feedback.append("ALERTA: A pesar de obtener clics, no se generó ninguna conversión. Revisa la página de destino y la relevancia de la oferta para esta audiencia.")

    if puntuacion_final_con_ruido >= 8: mensajes_feedback.append("¡Excelente trabajo! La configuración general de tu campaña es muy sólida y ha obtenido una alta puntuación. ¡Sigue así!")
    elif puntuacion_final_con_ruido <= 3: mensajes_feedback.append("La puntuación de la campaña es baja. Revisa cuidadosamente todas las sugerencias anteriores para identificar áreas clave de mejora en tu estrategia.")
    elif puntuacion_final_con_ruido <=5: mensajes_feedback.append("La puntuación es mejorable. Hay varios aspectos que puedes optimizar. Revisa los mensajes de feedback para guiarte.")

    presupuesto_gastado = (impresiones / 1000) * COSTO_POR_MIL_IMPRESIONES_BASE if impresiones > 0 else 0
    if presupuesto_gastado > presupuesto:
        presupuesto_gastado = presupuesto; impresiones_originales = impresiones
        impresiones = int((presupuesto_gastado/COSTO_POR_MIL_IMPRESIONES_BASE)*1000) if COSTO_POR_MIL_IMPRESIONES_BASE > 0 else 0
        if impresiones_originales > 0:
            factor_reduccion = impresiones / impresiones_originales
            clics = int(clics * factor_reduccion); interacciones_calculadas = int(interacciones_calculadas * factor_reduccion); conversiones_calculadas = int(conversiones_calculadas * factor_reduccion)
        else: clics = 0; interacciones_calculadas = 0; conversiones_calculadas = 0
    clics = max(0, clics); interacciones_calculadas = max(0, interacciones_calculadas); conversiones_calculadas = max(0, conversiones_calculadas)
    cpm_calculado = (presupuesto_gastado / impresiones * 1000) if impresiones > 0 else 0
    cpc_calculado = (presupuesto_gastado / clics) if clics > 0 else 0
    ctr_final_reportado = clics / impresiones if impresiones > 0 else 0

    return {
        "marca_nombre": marca["nombre"], "audiencia_nombre": audiencia["nombre"],
        "campaign_goal_nombre": campaign_goal["nombre"], "presupuesto_inicial": presupuesto,
        "puntuacion": puntuacion_final_con_ruido,
        "puntuacion_detalle_base": round(PUNTUACION_INICIAL,1),
        "puntuacion_detalle_afinidad_contrib": round(afinidad_marca_audiencia * MAX_PUNTOS_POR_FACTOR if afinidad_marca_audiencia >=0.4 else (PENALIDAD_FUERTE_TARGETING if afinidad_marca_audiencia <0.2 else PENALIDAD_SUAVE_TARGETING),1),
        "puntuacion_detalle_interes_contrib": round(interest_match_score * MAX_PUNTOS_POR_FACTOR if interest_match_score >=0.4 else (PENALIDAD_FUERTE_TARGETING if interest_match_score <0.15 and num_selected_intereses >0 else PENALIDAD_SUAVE_TARGETING),1),
        "puntuacion_detalle_objetivo_contrib": round(puntos_objetivo,1),
        "puntuacion_detalle_presupuesto_contrib": round((PUNTOS_PRESUESTO_MUY_BAJO if presupuesto < PRESUPUESTO_MINIMO_IMPACTO else (PUNTOS_PRESUESTO_BAJO if presupuesto < PRESUPUESTO_BAJO else (PUNTOS_PRESUESTO_ALTO if presupuesto > PRESUPUESTO_ALTO else 0))),1),
        "puntuacion_sin_ruido": round(puntuacion_actual,1),
        "impresiones": impresiones, "clics": clics, "ctr_calculado": round(ctr_final_reportado, 5),
        "interacciones_calculadas": interacciones_calculadas, "conversiones_calculadas": conversiones_calculadas,
        "cpm_calculado": round(cpm_calculado, 2), "cpc_calculado": round(cpc_calculado, 2),
        "presupuesto_gastado": round(presupuesto_gastado, 2),
        "afinidad_marca_audiencia": round(afinidad_marca_audiencia, 3),
        "interest_match_score": round(interest_match_score, 3),
        "selected_intereses_nombres": selected_intereses_nombres,
        "mensajes_feedback": mensajes_feedback,
        "potential_audience_size_from_segment": potential_audience_size_from_segment,
        "refined_potential_audience_size": refined_potential_audience_size,
        "mensaje": f"Campaña para {marca['nombre']} ({marca['categoria']}) con objetivo '{campaign_goal['nombre']}', dirigida a {audiencia['nombre']}."
    }

if __name__ == '__main__':
    marca_banco_id = "marca_001"; marca_retail_id = "marca_006"; marca_tech_id = "marca_012"
    aud_jovenes_id = "aud_001"; aud_familias_id = "aud_004"; aud_tech_id = "aud_003"
    intereses_jovenes_relevantes = ["int_001", "int_002", "int_005"]
    intereses_tech_relevantes = ["int_015", "int_016", "int_017"]
    intereses_familia_relevantes = ["int_022", "int_023", "int_028"]
    intereses_irrelevantes_para_jovenes = ["int_028", "int_029"]
    presupuesto_muy_bajo = 30000; presupuesto_bajo = 100000; presupuesto_medio = 500000; presupuesto_alto = 2000000

    print(f"\n--- ESCENARIO DEBUG: IDEAL Retail a Familias ---")
    resultado_ideal = simular_campana(marca_retail_id, aud_familias_id, presupuesto_alto, intereses_familia_relevantes, "traffic")
    print(f"  PUNTUACIÓN FINAL: {resultado_ideal['puntuacion']}")
    print(f"  Afinidad Marca-Audiencia: {resultado_ideal['afinidad_marca_audiencia']:.2%}, Match Intereses: {resultado_ideal['interest_match_score']:.2%}")
    print(f"  Impresiones: {resultado_ideal['impresiones']:,}, Clics: {resultado_ideal['clics']:,}, CTR: {resultado_ideal['ctr_calculado']:.3%}")
    print(f"  Mensajes de Feedback:")
    for msg in resultado_ideal.get("mensajes_feedback", []): print(f"    - {msg}")

    print(f"\n--- ESCENARIO DEBUG: POOR AFFINITY (Tech on Familias) ---")
    resultado_poor_affinity = simular_campana(marca_tech_id, aud_familias_id, presupuesto_medio, intereses_familia_relevantes, "traffic")
    print(f"  PUNTUACIÓN FINAL: {resultado_poor_affinity['puntuacion']}")
    print(f"  Afinidad Marca-Audiencia: {resultado_poor_affinity['afinidad_marca_audiencia']:.2%}, Match Intereses: {resultado_poor_affinity['interest_match_score']:.2%}")
    print(f"  Mensajes de Feedback:")
    for msg in resultado_poor_affinity.get("mensajes_feedback", []): print(f"    - {msg}")

    print(f"\n--- ESCENARIO DEBUG: MISMATCHED GOAL (Banco a Jóvenes para Conversión) ---")
    resultado_mismatched = simular_campana(marca_banco_id, aud_jovenes_id, presupuesto_medio, intereses_jovenes_relevantes, "conversion")
    print(f"  PUNTUACIÓN FINAL: {resultado_mismatched['puntuacion']}")
    print(f"  Afinidad Marca-Audiencia: {resultado_mismatched['afinidad_marca_audiencia']:.2%}, Match Intereses: {resultado_mismatched['interest_match_score']:.2%}")
    print(f"  Conversiones: {resultado_mismatched['conversiones_calculadas']}")
    print(f"  Mensajes de Feedback:")
    for msg in resultado_mismatched.get("mensajes_feedback", []): print(f"    - {msg}")
