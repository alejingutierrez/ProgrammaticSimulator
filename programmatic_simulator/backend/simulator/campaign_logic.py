# programmatic_simulator/backend/simulator/campaign_logic.py
import random
import math
from ..data import market_data

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
PUNTOS_PRESUESTO_BAJO = -0.25        # Halved from -0.5
PUNTOS_PRESUESTO_ALTO = 0.25         # Halved from 0.5
PUNTOS_PRESUESTO_MUY_BAJO = -0.5     # Halved from -1.0 (Si es demasiado bajo para el objetivo)

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


def _calculate_audience_size_details(audiencia_id, selected_interes_ids=None):
    """
    Calcula el tamaño potencial y refinado de la audiencia.
    Retorna un diccionario con los detalles del tamaño o un error.
    """
    audiencia = market_data.obtener_audiencia_por_id(audiencia_id)
    feedback_messages = []

    if not audiencia:
        return {
            "audience_found": False,
            "error_message": "Audiencia no encontrada",
            "status_code": 404,
            "potential_audience_size_from_segment": 0,
            "refined_potential_audience_size": 0,
            "feedback_messages": ["ERROR: Audiencia ID no válida o no encontrada."]
        }

    # --- Determinación del Tamaño de Audiencia Potencial por Segmento ---
    potential_audience_size_from_segment = 20000000  # Default grande si no se encuentra específico
    all_population_segments = market_data.obtener_todos_los_segmentos_poblacion()

    if all_population_segments:
        relevant_segments = [
            seg for seg in all_population_segments
            if audiencia["id"] in seg.get("relates_to_audience_ids", [])
        ]
        if relevant_segments:
            relevant_segments.sort(key=lambda s: s["size"])
            potential_audience_size_from_segment = relevant_segments[0]["size"]
            feedback_messages.append(f"INFO: Segmento de población '{relevant_segments[0]['nombre_segmento']}' (tamaño: {potential_audience_size_from_segment:,}) usado para estimar alcance máximo.")
            if potential_audience_size_from_segment < 1000000:
                 feedback_messages.append("INFO: El segmento de audiencia seleccionado es bastante específico, lo que podría limitar el alcance máximo.")
        else:
            total_col_segment = next((s for s in all_population_segments if s["segment_id"] == "total_colombia"), None)
            if total_col_segment:
                potential_audience_size_from_segment = int(total_col_segment["size"] * 0.25)
                feedback_messages.append(f"INFO: No se encontró un segmento de población directamente relacionado. Usando estimación basada en población total ({potential_audience_size_from_segment:,}).")
            else: # Fallback si ni siquiera total_colombia está
                feedback_messages.append(f"WARNING: No se encontró segmento de población específico ni 'total_colombia'. Usando default amplio: {potential_audience_size_from_segment:,}.")


    # --- Refinar Audiencia por Intereses ---
    num_selected_intereses = len(selected_interes_ids) if selected_interes_ids else 0
    if num_selected_intereses > 0:
        # Aplicar reducción por cada capa de interés
        # La fórmula original era: (INTEREST_PENETRATION_ESTIMATE ** (num_selected_intereses * 0.5))
        # Se ajusta para ser un poco menos agresiva y más interpretable.
        # Cada grupo de intereses reduce, pero no exponencialmente tan drástico.
        # Por ejemplo, si hay 1-2 intereses, se aplica una vez. Si hay 3-4, dos veces, etc.
        # Factor de reducción basado en el número de intereses.
        reduction_factor_power = math.ceil(num_selected_intereses / 2.0) # Grupos de 2 intereses
        refined_potential_audience_size = potential_audience_size_from_segment * (INTEREST_PENETRATION_ESTIMATE ** reduction_factor_power)
        refined_potential_audience_size = max(1000, int(refined_potential_audience_size)) # Mínimo 1000 personas
        feedback_messages.append(f"INFO: Audiencia refinada por {num_selected_intereses} intereses a ~{refined_potential_audience_size:,} personas.")
    else:
        refined_potential_audience_size = potential_audience_size_from_segment
        feedback_messages.append("INFO: No se seleccionaron intereses, el tamaño refinado es igual al potencial del segmento.")

    return {
        "potential_audience_size_from_segment": potential_audience_size_from_segment,
        "refined_potential_audience_size": refined_potential_audience_size,
        "audience_found": True,
        "feedback_messages": feedback_messages,
        "status_code": 200
    }

def _normalize_text_for_matching(text):
    if not text: return ""
    text = str(text).lower()
    text = text.replace('_', ' ')
    accent_map = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u'}
    for accented, unaccented in accent_map.items():
        text = text.replace(accented, unaccented)
    return " ".join(text.split()) # Collapse multiple spaces and strip leading/trailing


def calculate_total_affinity(marca_id, audiencia_id, selected_interes_ids=None, selected_product_ids=None):
    marca = market_data.obtener_marca_por_id(marca_id)
    audiencia = market_data.obtener_audiencia_por_id(audiencia_id)

    if not marca:
        return {"error": f"Marca con ID '{marca_id}' no encontrada.", "overall_affinity": 0, "afinidad_marca_audiencia": 0, "interest_match_score": 0}
    if not audiencia:
        return {"error": f"Audiencia con ID '{audiencia_id}' no encontrada.", "overall_affinity": 0, "afinidad_marca_audiencia": 0, "interest_match_score": 0}

    # --- Cálculo de Afinidad Marca-Audiencia (con posible sobreescritura por producto) ---
    afinidad_marca_audiencia_component = 0.0 # Initialize
    afinidad_calculada_por_producto = False

    if selected_product_ids and marca and audiencia:
        product_affinities_for_audience = []
        for prod_id in selected_product_ids:
            producto_encontrado = None
            for p in marca.get("productos", []):
                if p["id"] == prod_id:
                    producto_encontrado = p
                    break

            if producto_encontrado:
                if audiencia_id in producto_encontrado.get("afinidad_audiencia", {}):
                    product_affinities_for_audience.append(producto_encontrado["afinidad_audiencia"][audiencia_id])

        if product_affinities_for_audience:
            afinidad_marca_audiencia_component = sum(product_affinities_for_audience) / len(product_affinities_for_audience)
            afinidad_calculada_por_producto = True

    if not afinidad_calculada_por_producto:
        marca_categoria = marca.get("categoria") if marca else None
        if audiencia and marca_categoria:
            afinidad_marca_audiencia_component = audiencia.get("afinidad_marca_categoria", {}).get(marca_categoria, 0.05)
        elif audiencia and not marca_categoria:
            afinidad_marca_audiencia_component = 0.05
        else:
            afinidad_marca_audiencia_component = 0.05

    afinidad_marca_audiencia_component = float(afinidad_marca_audiencia_component)

    # --- Cálculo de Interest Match Score ---
    interest_match_score_component = 0.0
    num_selected_intereses = len(selected_interes_ids) if selected_interes_ids else 0

    if num_selected_intereses > 0:
        total_interest_affinity_score = 0.0
        num_relevant_interests = 0

        for interes_id in selected_interes_ids:
            interes_obj = market_data.obtener_interes_por_id(interes_id)
            if interes_obj:
                num_relevant_interests += 1
                current_interest_score = 0.1  # Default low score

                product_affinity_found_for_this_interest = False
                if selected_product_ids:
                    if "afinidad_producto" in interes_obj and isinstance(interes_obj["afinidad_producto"], dict):
                        matched_product_scores = []
                        for prod_id in selected_product_ids:
                            if prod_id in interes_obj["afinidad_producto"]:
                                matched_product_scores.append(float(interes_obj["afinidad_producto"][prod_id]))
                        if matched_product_scores:
                            current_interest_score = sum(matched_product_scores) / len(matched_product_scores)
                            product_affinity_found_for_this_interest = True

                if not product_affinity_found_for_this_interest:
                    if "afinidad_marca" in interes_obj and isinstance(interes_obj["afinidad_marca"], dict):
                        if marca_id in interes_obj["afinidad_marca"]:
                            current_interest_score = float(interes_obj["afinidad_marca"][marca_id])

                total_interest_affinity_score += current_interest_score

        if num_relevant_interests > 0:
            interest_match_score_component = total_interest_affinity_score / num_relevant_interests
        else:
            interest_match_score_component = 0.1 # Fallback if IDs provided but none found
    else: # No selected_interes_ids
        interest_match_score_component = 0.3 # Default for campaigns without specific interest targeting

    interest_match_score_component = float(interest_match_score_component)

    # --- Calculate Overall Affinity ---
    overall_affinity = (afinidad_marca_audiencia_component + interest_match_score_component) / 2.0
    overall_affinity = max(0.0, min(1.0, overall_affinity))

    return {
        "overall_affinity": round(overall_affinity, 3),
        "afinidad_marca_audiencia": round(afinidad_marca_audiencia_component, 3),
        "interest_match_score": round(interest_match_score_component, 3)
    }


def simular_campana(marca_id, audiencia_id, presupuesto, selected_interes_ids=None, campaign_goal_id=None, selected_product_ids=None, campaign_duration_days=None):
    marca = market_data.obtener_marca_por_id(marca_id)
    audiencia = market_data.obtener_audiencia_por_id(audiencia_id)

    goal_id_to_use = campaign_goal_id or DEFAULT_CAMPAIGN_GOAL_ID
    campaign_goal = market_data.obtener_campaign_goal_por_id(goal_id_to_use)
    if not campaign_goal:
        campaign_goal = market_data.obtener_campaign_goal_por_id(DEFAULT_CAMPAIGN_GOAL_ID)

    mensajes_feedback = [] # Initialize messages for simular_campana

    if campaign_duration_days:
        try:
            # Ensure campaign_duration_days is an int for calculations if it comes as string/float
            duration_days_int = int(campaign_duration_days)
            mensajes_feedback.append(f"INFO: La campaña está configurada para una duración de {duration_days_int} día(s).")

            # Calculate equivalent monthly budget for comparison thresholds
            # If campaign is 15 days, its budget is compared as if it were for 30 days (budget * 2)
            # If campaign is 60 days, its budget is compared as if it were for 30 days (budget / 2)
            # This helps normalize budget perception against thresholds like PRESUPUESTO_ALTO/BAJO which are implicitly for a typical month.
            # Or, more simply, calculate a daily budget and compare that.
            # Daily budget = presupuesto / duration_days_int
            # Threshold daily high = PRESUPUESTO_ALTO / 30
            # Threshold daily low = PRESUPUESTO_BAJO / 30

            if duration_days_int > 0: # Avoid division by zero
                daily_budget = presupuesto / duration_days_int
                threshold_daily_high = PRESUPUESTO_ALTO / 30
                threshold_daily_low = PRESUPUESTO_MINIMO_IMPACTO / 30 # Use MINIMO_IMPACTO for "too low" daily check

                if duration_days_int > 30 and daily_budget < threshold_daily_low * 1.5: # Extended campaign, low daily budget
                    mensajes_feedback.append(f"SUGERENCIA: Para una campaña larga ({duration_days_int} días), el presupuesto diario ({daily_budget:,.0f} COP) parece bajo para mantener una presencia efectiva y constante.")
                elif duration_days_int < 7 and daily_budget > threshold_daily_high * 0.75: # Short campaign, high daily budget
                    mensajes_feedback.append(f"INFO: El presupuesto diario ({daily_budget:,.0f} COP) es considerable para una campaña corta ({duration_days_int} días), lo que podría permitir una alta intensidad.")
        except ValueError:
            mensajes_feedback.append(f"WARNING: Duración de campaña '{campaign_duration_days}' no es un número válido.")


    # --- Obtener detalles del tamaño de la audiencia ---
    audience_size_details = _calculate_audience_size_details(audiencia_id, selected_interes_ids)

    if not audience_size_details["audience_found"]:
        # Propagate error if audience not found by the detail function
        return {
            "error": audience_size_details["error_message"],
            "puntuacion": 0, "impresiones": 0, "clics": 0, "ctr_calculado":0,
            "cpm_calculado": 0, "cpc_calculado": 0, "presupuesto_gastado": 0,
            "interest_match_score": 0, "selected_intereses_nombres": [],
            "campaign_goal_nombre": campaign_goal["nombre"] if campaign_goal else "N/A",
            "interacciones_calculadas":0, "conversiones_calculadas":0, "afinidad_marca_audiencia":0,
            "mensajes_feedback": audience_size_details.get("feedback_messages", ["Error: Audiencia no encontrada."]),
            "potential_audience_size_from_segment": 0,
            "refined_potential_audience_size": 0
        }

    potential_audience_size_from_segment = audience_size_details["potential_audience_size_from_segment"]
    refined_potential_audience_size = audience_size_details["refined_potential_audience_size"]
    if audience_size_details.get("feedback_messages"):
        mensajes_feedback.extend(audience_size_details["feedback_messages"])

    # Retrieve audiencia object again, as _calculate_audience_size_details already fetched it
    # This is slightly redundant but ensures simular_campana has its own reference if needed beyond size.
    # Alternatively, _calculate_audience_size_details could return the audiencia object. For now, keeping it simple.
    audiencia = market_data.obtener_audiencia_por_id(audiencia_id)
    if not marca: # Audiencia check is implicitly done by audience_size_details
        return { "error": "Marca no encontrada.", "puntuacion": 0, "impresiones": 0, "clics": 0,
                 "mensajes_feedback": ["Error crítico: Marca no encontrada."],
                 "potential_audience_size_from_segment": potential_audience_size_from_segment,
                 "refined_potential_audience_size": refined_potential_audience_size}

    puntuacion_actual = PUNTUACION_INICIAL

    # --- Cálculo de Afinidad Marca-Audiencia y de Intereses ---
    # Utilizar la nueva función para obtener los componentes de afinidad
    affinity_data = calculate_total_affinity(marca_id, audiencia_id, selected_interes_ids, selected_product_ids)

    if "error" in affinity_data:
        # Si calculate_total_affinity devuelve un error (e.g., marca o audiencia no encontrada),
        # se podría propagar este error o manejarlo como un caso de muy baja afinidad.
        # Por simplicidad aquí, asumimos que las verificaciones previas de marca y audiencia
        # en simular_campana ya han ocurrido o que el error es crítico.
        # O, podríamos usar los valores de afinidad 0 que devuelve en caso de error.
        # Este path debería ser raro si marca/audiencia ya fueron validados.
         return { "error": affinity_data["error"], "puntuacion": 0, "impresiones": 0, "clics": 0,
                 "mensajes_feedback": [affinity_data["error"]],
                 "potential_audience_size_from_segment": potential_audience_size_from_segment,
                 "refined_potential_audience_size": refined_potential_audience_size}


    afinidad_marca_audiencia = affinity_data["afinidad_marca_audiencia"]
    interest_match_score = affinity_data["interest_match_score"]

    # Generar feedback para afinidad marca-audiencia (similar a como estaba antes)
    if afinidad_marca_audiencia >= 0.7:
        mensajes_feedback.append(f"INFO: Afinidad marca-audiencia calculada: {afinidad_marca_audiencia:.2f} (Alta).")
    elif afinidad_marca_audiencia >=0.4:
        mensajes_feedback.append(f"INFO: Afinidad marca-audiencia calculada: {afinidad_marca_audiencia:.2f} (Moderada).")
    else:
        mensajes_feedback.append(f"INFO: Afinidad marca-audiencia calculada: {afinidad_marca_audiencia:.2f} (Baja).")

    # Scoring para afinidad_marca_audiencia
    if afinidad_marca_audiencia >= 0.7: puntuacion_actual += BONUS_BUEN_TARGETING
    elif afinidad_marca_audiencia >= 0.4: puntuacion_actual += (BONUS_BUEN_TARGETING / 2)
    elif afinidad_marca_audiencia < 0.2: puntuacion_actual += PENALIDAD_FUERTE_TARGETING
    else: puntuacion_actual += PENALIDAD_SUAVE_TARGETING

    selected_intereses_nombres = []
    if selected_interes_ids: # Poblar nombres si hay IDs
        for interes_id in selected_interes_ids:
            interes_obj = market_data.obtener_interes_por_id(interes_id)
            if interes_obj:
                selected_intereses_nombres.append(interes_obj["nombre"])
            # No es necesario añadir "WARNING" aquí si el interés no se encuentra,
            # ya que calculate_total_affinity ya maneja la lógica de afinidad con los intereses existentes.

    num_selected_intereses = len(selected_interes_ids) if selected_interes_ids else 0 # Recalcular para lógica de scoring

    # Generar feedback para interest_match_score (similar a como estaba antes)
    if num_selected_intereses > 0:
        mensajes_feedback.append(f"INFO: Puntuación de afinidad de intereses calculada: {interest_match_score:.2f}.")
        if interest_match_score >= 0.7:
            mensajes_feedback.append(f"POSITIVO: La afinidad de los intereses seleccionados con la marca/productos es muy alta ({interest_match_score:.2f}).")
        elif interest_match_score >= 0.4:
            mensajes_feedback.append(f"INFO: La afinidad de los intereses seleccionados con la marca/productos es moderada ({interest_match_score:.2f}).")
        elif interest_match_score < 0.15:
            mensajes_feedback.append(f"ALERTA: La afinidad de los intereses seleccionados con la marca/productos es críticamente baja ({interest_match_score:.2f}).")
        else:
            mensajes_feedback.append(f"SUGERENCIA: La afinidad de los intereses seleccionados con la marca/productos es baja ({interest_match_score:.2f}).")
    else:
        mensajes_feedback.append(f"INFO: No se seleccionaron intereses. Puntuación de afinidad de interés base: {interest_match_score:.2f}.")


    # Scoring para interest_match_score
    if num_selected_intereses > 0: # Aplicar bonus/penalty solo si intereses fueron parte de la estrategia
        if interest_match_score >= 0.7: puntuacion_actual += BONUS_BUEN_TARGETING
        elif interest_match_score >= 0.4: puntuacion_actual += (BONUS_BUEN_TARGETING / 2)
        elif interest_match_score < 0.15: puntuacion_actual += PENALIDAD_FUERTE_TARGETING
        else: puntuacion_actual += PENALIDAD_SUAVE_TARGETING
    # else: No specific penalty here if no interests are selected, as it's a valid strategy (broad campaign)
    # puntuacion_actual += PENALIDAD_SUAVE_TARGETING # Old logic for no interests selected, removing as it might be too punitive if broad is intentional

    efectividad_targeting_combinada = (afinidad_marca_audiencia + interest_match_score) / 2.0

    # Adjust combined effectiveness if either component is very low, especially if interests were selected
    if afinidad_marca_audiencia < 0.2:
        efectividad_targeting_combinada *= 0.7 # General brand mismatch always hurts
    if num_selected_intereses > 0 and interest_match_score < 0.15:
        efectividad_targeting_combinada *= 0.5 # Very poor interest selection hurts more
    elif num_selected_intereses == 0 and interest_match_score <= 0.3: # Baseline for no interests
         efectividad_targeting_combinada *= 0.9 # Slight reduction if no interests, as it's less targeted

    efectividad_targeting_combinada = max(0.05, min(1.0, efectividad_targeting_combinada))

    impresiones_posibles_brutas = (presupuesto / COSTO_POR_MIL_IMPRESIONES_BASE) * 1000
    impresion_goal_modifier = GOAL_IMPRESSION_MODIFIERS.get(campaign_goal["id"], 1.0)
    factor_alcance_efectivo = efectividad_targeting_combinada * 0.7 + 0.2
    if presupuesto > PRESUPUESTO_ALTO: factor_alcance_efectivo = min(1.0, factor_alcance_efectivo * 1.1)
    impresiones_efectivas = int(impresiones_posibles_brutas * factor_alcance_efectivo * impresion_goal_modifier)

    # Limitar Impresiones por Población (refined_potential_audience_size ya está calculado)
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
        # Feedback messages for interest affinity are now generated during the calculation and scoring of interest_match_score
        if interest_match_score < 0.15: # This is a duplicate of the one generated during scoring, but kept for emphasis
            mensajes_feedback.append("ALERTA CRÍTICA: La afinidad de los intereses seleccionados con los productos/marca es extremadamente baja. Considera cambiar los intereses o la oferta.")
        elif interest_match_score < 0.35:
            mensajes_feedback.append("SUGERENCIA: La afinidad de los intereses seleccionados con los productos/marca es baja. Revisa si estos intereses realmente se alinean con lo que ofreces.")
        elif interest_match_score >= 0.7:
            mensajes_feedback.append("POSITIVO: ¡Excelente alineación! Los intereses seleccionados tienen una alta afinidad con tus productos/marca.")

        if num_selected_intereses > 6 and interest_match_score < 0.5 :
            mensajes_feedback.append("INFO: Has seleccionado muchos intereses, pero la afinidad general no es muy alta. Considera enfocar en menos intereses pero más afines, o revisar la relevancia de cada uno para la marca/producto.")
        elif num_selected_intereses > 6 :
             mensajes_feedback.append("INFO: Has seleccionado muchos intereses. Asegúrate de que todos sean altamente afines a la marca/productos para mantener la efectividad.")
    else:
        mensajes_feedback.append("INFO: No seleccionaste intereses específicos. La campaña se dirigirá de forma más amplia. Para mejorar la precisión, considera añadir intereses afines a tus productos/marca.")

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

    # --- Feedback for underspending ---
    if presupuesto_gastado < presupuesto:
        explanation_message = f"NOTA SOBRE EL PRESUPUESTO: Se gastó {presupuesto_gastado:,.0f} COP de un total de {presupuesto:,.0f} COP. "
        underspend_ratio = (presupuesto - presupuesto_gastado) / presupuesto if presupuesto > 0 else 0

        # Ensure refined_potential_audience_size is not zero to avoid division by zero or misleading ratios
        audience_reached_ratio = 0
        if refined_potential_audience_size > 0:
            audience_reached_ratio = impresiones / refined_potential_audience_size

        if audience_reached_ratio >= 0.9: # Reached most of the targetable audience
            explanation_message += "Esto puede ser porque se alcanzó a la mayoría de la audiencia objetivo estimada con la configuración actual. "
        elif efectividad_targeting_combinada < 0.35 and puntuacion_final_con_ruido < 5: # Low targeting effectiveness and low score
            explanation_message += "La baja efectividad de la segmentación o un bajo atractivo general de la campaña podrían haber limitado el gasto para optimizar los resultados dentro del presupuesto asignado. "
        elif underspend_ratio > 0.5 and presupuesto > PRESUPUESTO_ALTO : # Significant underspend on a large budget
            explanation_message += "El sistema puede haber limitado el gasto para evitar una saturación excesiva de la audiencia o si se estimó que un gasto adicional no mejoraría significativamente los resultados. "
        else: # Generic message
            explanation_message += "Esto puede ocurrir si el tamaño de la audiencia alcanzable es limitado por la segmentación, o si el sistema optimiza el gasto para no exceder el punto de retornos decrecientes. "

        mensajes_feedback.append(explanation_message)

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
        "campaign_duration_days": campaign_duration_days, # Return duration
        "selected_product_ids": selected_product_ids if selected_product_ids else [], # Return selected products
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
    # Example call with product_ids (assuming prod_006_01 and prod_006_03 are relevant for aud_familias_id)
    # For this test to be meaningful, market_data.py should have these products for marca_006 and relevant affinities for aud_004
    # e.g., prod_006_01: {"aud_004": 0.8}, prod_006_03: {} (no specific affinity or not for aud_004)
    # Let's assume prod_006_01 ("Mercado Básico") for Éxito has high affinity for aud_004 ("Familias Consolidadas")
    # And prod_006_02 ("Electrodomésticos") also has good affinity.
    # We would need to update market_data.py for these specific affinities for a full test.
    # For now, this call demonstrates the new parameter.
    selected_products_exito_familias = ["prod_006_01", "prod_006_02"] # Example product IDs
    resultado_ideal = simular_campana(marca_retail_id, aud_familias_id, presupuesto_alto, intereses_familia_relevantes, "traffic", selected_product_ids=selected_products_exito_familias)
    print(f"  PUNTUACIÓN FINAL: {resultado_ideal['puntuacion']}")
    print(f"  Afinidad Marca-Audiencia: {resultado_ideal['afinidad_marca_audiencia']:.2%} (Puede ser de producto o categoría), Match Intereses: {resultado_ideal['interest_match_score']:.2%}")
    print(f"  Impresiones: {resultado_ideal['impresiones']:,}, Clics: {resultado_ideal['clics']:,}, CTR: {resultado_ideal['ctr_calculado']:.3%}")
    print(f"  Mensajes de Feedback:")
    for msg in resultado_ideal.get("mensajes_feedback", []): print(f"    - {msg}")

    print(f"\n--- ESCENARIO DEBUG: POOR AFFINITY (Tech on Familias, no specific product affinity expected) ---")
    resultado_poor_affinity = simular_campana(marca_tech_id, aud_familias_id, presupuesto_medio, intereses_familia_relevantes, "traffic", selected_product_ids=["prod_012_01"]) # Rappi Prime for families
    print(f"  PUNTUACIÓN FINAL: {resultado_poor_affinity['puntuacion']}")
    print(f"  Afinidad Marca-Audiencia: {resultado_poor_affinity['afinidad_marca_audiencia']:.2%}, Match Intereses: {resultado_poor_affinity['interest_match_score']:.2%}")
    print(f"  Mensajes de Feedback:")
    for msg in resultado_poor_affinity.get("mensajes_feedback", []): print(f"    - {msg}")

    print(f"\n--- ESCENARIO DEBUG: MISMATCHED GOAL (Banco a Jóvenes para Conversión, with a product) ---")
    # Assuming prod_001_01 (Cuenta de Ahorros) might have some affinity for aud_001 (Jóvenes)
    selected_products_banco_jovenes = ["prod_001_01"]
    resultado_mismatched = simular_campana(marca_banco_id, aud_jovenes_id, presupuesto_medio, intereses_jovenes_relevantes, "conversion", selected_product_ids=selected_products_banco_jovenes)
    print(f"  PUNTUACIÓN FINAL: {resultado_mismatched['puntuacion']}")
    print(f"  Afinidad Marca-Audiencia: {resultado_mismatched['afinidad_marca_audiencia']:.2%}, Match Intereses: {resultado_mismatched['interest_match_score']:.2%}")
    print(f"  Conversiones: {resultado_mismatched['conversiones_calculadas']}")
    print(f"  Mensajes de Feedback:")
    for msg in resultado_mismatched.get("mensajes_feedback", []): print(f"    - {msg}")

    print(f"\n--- ESCENARIO DEBUG: Banco a Jóvenes para Conversión, NO productos seleccionados ---")
    resultado_mismatched_no_prod = simular_campana(marca_banco_id, aud_jovenes_id, presupuesto_medio, intereses_jovenes_relevantes, "conversion")
    print(f"  PUNTUACIÓN FINAL: {resultado_mismatched_no_prod['puntuacion']}")
    print(f"  Afinidad Marca-Audiencia (Categoría): {resultado_mismatched_no_prod['afinidad_marca_audiencia']:.2%}, Match Intereses: {resultado_mismatched_no_prod['interest_match_score']:.2%}")
    print(f"  Conversiones: {resultado_mismatched_no_prod['conversiones_calculadas']}")
    print(f"  Mensajes de Feedback:")
    for msg in resultado_mismatched_no_prod.get("mensajes_feedback", []): print(f"    - {msg}")
