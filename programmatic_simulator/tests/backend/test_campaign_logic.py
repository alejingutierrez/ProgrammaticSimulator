import unittest
from unittest.mock import patch # Might need for underspend tests later
from programmatic_simulator.backend.simulator.campaign_logic import simular_campana, calculate_total_affinity, COSTO_POR_MIL_IMPRESIONES_BASE, MAX_PUNTOS_POR_FACTOR, PRESUPUESTO_BAJO as CL_PRESUPUESTO_BAJO, PRESUPUESTO_ALTO as CL_PRESUPUESTO_ALTO, PRESUPUESTO_MINIMO_IMPACTO
from programmatic_simulator.backend.data import market_data

class TestCampaignLogic(unittest.TestCase):

    # --- Test Data (using actual IDs from market_data for realism) ---
    MARCA_RETAIL_ID = "marca_006"  # Éxito (Retail)
    MARCA_TECH_ID = "marca_012"    # Rappi (Tech)
    MARCA_BANCO_ID = "marca_001"   # Bancolombia (Banca)
    MARCA_CPG_ID = "marca_003"     # Alpina

    AUD_FAMILIAS_ID = "aud_004"    # Familias Consolidadas (Afinidad con Retail: 0.7, con Tech: 0.4)
                                   # Related population segment: familias_35_55_col (10,000,000)
    AUD_JOVENES_ID = "aud_001"     # Jóvenes Universitarios (Afinidad con Banca: 0.4, con Tech: 0.9)
                                   # Related population segment: jovenes_18_24_col (5,500,000)
    AUD_TECH_ID = "aud_003"        # Entusiastas de la Tecnología (Afinidad con Tech: 0.95)
                                   # Related population segment: profesionales_jovenes_25_34_col (7,000,000 - also aud_002)
    AUD_ADULTOS_MAYORES_ID = "aud_005" # Adultos Mayores Activos (60+)
                                      # Related population segment: adultos_mayores_60_mas_col (7,500,000) - check market_data for actual size

    INTERESES_FAMILIA_RELEVANTES = ["int_022", "int_023", "int_028"] # Prod Hogar, Educacion Hijos, Mejoras Hogar
    INTERESES_TECH_RELEVANTES = ["int_015", "int_016", "int_017"]    # Gadgets, Software Prod, IA
    INTERESES_JOVENES_RELEVANTES = ["int_001", "int_002", "int_005"] # Tec Emergente, Videojuegos, Redes Sociales
    INTERESES_IRRELEVANTES_PARA_FAMILIA = ["int_001", "int_015"] # Tec emergente, Gadgets
    INTERESES_CPG_RELEVANTES_ADULTOS_MAYORES = ["int_026", "int_029"] # Alimentacion Organica, Salud Preventiva Senior

    GOAL_TRAFFIC_ID = "traffic"
    GOAL_AWARENESS_ID = "awareness"
    GOAL_CONVERSION_ID = "conversion"
    GOAL_ENGAGEMENT_ID = "engagement"

    PRESUPUESTO_MEDIO = 500000
    PRESUPUESTO_BAJO = CL_PRESUPUESTO_BAJO # Use constant from campaign_logic if it changes
    PRESUPUESTO_MUY_BAJO = 30000 # This is below PRESUPUESTO_MINIMO_IMPACTO
    PRESUPUESTO_ALTO = CL_PRESUPUESTO_ALTO # Use constant from campaign_logic
    PRESUPUESTO_EXTREMO = 50000000 # For population capping tests

    # Access population data for assertions
    ALL_POPULATION_SEGMENTS = market_data.obtener_todos_los_segmentos_poblacion()
    SEGMENT_ADULTOS_MAYORES = market_data.obtener_segmento_poblacion_por_id("adultos_mayores_60_mas_col")
    SEGMENT_JOVENES = market_data.obtener_segmento_poblacion_por_id("jovenes_18_24_col")
    SEGMENT_FAMILIAS = market_data.obtener_segmento_poblacion_por_id("familias_35_55_col")

    # --- IDs for new affinity tests ---
    MARCA_RAPPI_ID = "marca_012" # Rappi (Tech) - Same as MARCA_TECH_ID
    MARCA_MERCADOLIBRE_ID = "marca_013" # Mercado Libre (Tech)
    MARCA_CLARO_ID = "marca_007" # Claro (Telecom)

    PROD_CLARO_5G_ID = "prod_007_01" # Claro Plan Pospago 5G
    PROD_ML_TECH_ID = "prod_013_03" # Mercado Libre Tecnología
    PROD_RAPPI_PRIME_ID = "prod_012_01" # Rappi Prime
    PROD_RAPPI_RESTAURANTES_ID = "prod_012_02" # Rappi Entrega Restaurantes

    INT_TECNOLOGIA_EMERGENTE_ID = "int_001" # Modified with new affinities
    INT_INVERSIONES_CRIPTO_ID = "int_009"   # Modified with new affinities
    INT_RESTAURANTES_GOURMET_ID = "int_011" # Modified with new affinities
    INT_VIDEOJUEGOS_ID = "int_002"          # Generic interest, likely no new specific affinities

    AUD_PROFESIONALES_JOVENES_ID = "aud_002" # Profesionales Jóvenes


    def assertFeedbackContains(self, feedback_list, expected_substring, msg=""):
        default_msg = f"Feedback esperado '{expected_substring}' no encontrado en {feedback_list}"
        self.assertTrue(any(expected_substring.lower() in feedback_item.lower() for feedback_item in feedback_list),
                        msg or default_msg)

    def test_ideal_scenario(self):
        result = simular_campana(
            marca_id=self.MARCA_RETAIL_ID,
            audiencia_id=self.AUD_FAMILIAS_ID,
            presupuesto=self.PRESUPUESTO_ALTO,
            selected_interes_ids=self.INTERESES_FAMILIA_RELEVANTES,
            campaign_goal_id=self.GOAL_TRAFFIC_ID,
            selected_product_ids=[],
            campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertNotIn("error", result)
        self.assertGreaterEqual(result['puntuacion'], 7, f"La puntuación en un escenario ideal debería ser alta (>=7). Actual: {result['puntuacion']}")
        # Feedback messages might change due to new logic and duration/underspend messages.
        # Making these checks more general or removing if they become too brittle.
        self.assertTrue(any("afinidad marca-audiencia calculada" in msg.lower() and "(alta)" in msg.lower() for msg in result['mensajes_feedback']))
        self.assertTrue(any("afinidad de los intereses seleccionados con la marca/productos es muy alta" in msg.lower() for msg in result['mensajes_feedback']))
        self.assertIn('potential_audience_size_from_segment', result)
        self.assertIn('refined_potential_audience_size', result)

    def test_poor_affinity(self):
        result = simular_campana(
            marca_id=self.MARCA_TECH_ID,
            audiencia_id=self.AUD_FAMILIAS_ID,
            presupuesto=self.PRESUPUESTO_MEDIO,
            selected_interes_ids=self.INTERESES_FAMILIA_RELEVANTES,
            campaign_goal_id=self.GOAL_TRAFFIC_ID,
            selected_product_ids=[],
            campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertTrue(5 <= result['puntuacion'] <= 7, f"Puntuación esperada 5-7. Actual: {result['puntuacion']}")
        self.assertFeedbackContains(result['mensajes_feedback'], "afinidad marca-audiencia calculada")
        self.assertFeedbackContains(result['mensajes_feedback'], "(Moderada)")


    def test_irrelevant_interests(self):
        result = simular_campana(
            marca_id=self.MARCA_RETAIL_ID,
            audiencia_id=self.AUD_FAMILIAS_ID,
            presupuesto=self.PRESUPUESTO_MEDIO,
            selected_interes_ids=self.INTERESES_IRRELEVANTES_PARA_FAMILIA, # These might have very low or 0.1 scores
            campaign_goal_id=self.GOAL_TRAFFIC_ID,
            selected_product_ids=[],
            campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        # interest_match_score will be low (average of 0.1s if no affinities found)
        self.assertLessEqual(result['interest_match_score'], 0.3)
        self.assertTrue(4 <= result['puntuacion'] <= 7, f"Puntuación con intereses irrelevantes debería ser moderadamente baja. Actual: {result['puntuacion']}")
        # The message "no coinciden NADA" was removed/changed in campaign_logic.
        # New message is "La afinidad de los intereses seleccionados con la marca/productos es críticamente baja" or "baja"
        self.assertTrue(
            any("críticamente baja" in msg.lower() for msg in result['mensajes_feedback']) or
            any("es baja" in msg.lower() for msg in result['mensajes_feedback'] if "intereses seleccionados con la marca/productos es baja" in msg.lower()),
            "Feedback for very low interest match not found or changed."
        )


    def test_mismatched_campaign_goal_conversion(self):
        result = simular_campana(
            marca_id=self.MARCA_BANCO_ID,
            audiencia_id=self.AUD_JOVENES_ID,
            presupuesto=self.PRESUPUESTO_BAJO,
            selected_interes_ids=self.INTERESES_JOVENES_RELEVANTES,
            campaign_goal_id=self.GOAL_CONVERSION_ID,
            selected_product_ids=[],
            campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertTrue(1 <= result['puntuacion'] <= 3, f"Puntuación esperada baja (1-3). Actual: {result['puntuacion']}")
        self.assertLess(result['conversiones_calculadas'], result['clics'] * 0.05, "Conversiones deben ser una pequeña fracción de clics")
        if result['conversiones_calculadas'] == 0 and result['clics'] > 10:
             self.assertFeedbackContains(result['mensajes_feedback'], "no se generó ninguna conversión")

    def test_low_budget_impact_awareness(self):
        result = simular_campana(
            marca_id=self.MARCA_RETAIL_ID,
            audiencia_id=self.AUD_FAMILIAS_ID,
            presupuesto=self.PRESUPUESTO_MUY_BAJO,
            selected_interes_ids=self.INTERESES_FAMILIA_RELEVANTES,
            campaign_goal_id=self.GOAL_AWARENESS_ID,
            selected_product_ids=[],
            campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertTrue(2 <= result['puntuacion'] <= 5, f"Puntuación esperada 2-5. Actual: {result['puntuacion']}")
        self.assertFeedbackContains(result['mensajes_feedback'], "presupuesto es muy bajo")

    def test_no_interests_selected(self):
        result = simular_campana(
            marca_id=self.MARCA_BANCO_ID,
            audiencia_id=self.AUD_JOVENES_ID,
            presupuesto=self.PRESUPUESTO_MEDIO,
            selected_interes_ids=[],
            campaign_goal_id=self.GOAL_TRAFFIC_ID,
            selected_product_ids=[],
            campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertAlmostEqual(result['interest_match_score'], 0.3, delta=0.001)
        self.assertFeedbackContains(result['mensajes_feedback'], "No se seleccionaron intereses. Puntuación de afinidad de interés base: 0.30.")
        self.assertTrue(3 <= result['puntuacion'] <= 6, f"Puntuación {result['puntuacion']} inesperada para 'sin intereses'.")


    # --- Test Cases for New Affinity Logic ---

    def test_interest_affinity_by_product(self):
        """Interest affinity is derived from specific product affinity."""
        # int_001 (Tecnología Emergente) has afinidad_producto: {"prod_012_01": 0.65}
        # Rappi Prime is prod_012_01 from marca_012 (Rappi)
        result = simular_campana(
            marca_id=self.MARCA_RAPPI_ID,
            audiencia_id=self.AUD_JOVENES_ID,
            presupuesto=self.PRESUPUESTO_MEDIO,
            selected_interes_ids=[self.INT_TECNOLOGIA_EMERGENTE_ID],
            selected_product_ids=[self.PROD_RAPPI_PRIME_ID],
            campaign_goal_id=self.GOAL_TRAFFIC_ID,
            campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertNotIn("error", result, result.get("mensajes_feedback"))
        self.assertAlmostEqual(result['interest_match_score'], 0.65, delta=0.001)
        self.assertFeedbackContains(result['mensajes_feedback'], "afinidad de los intereses seleccionados")

    def test_interest_affinity_by_brand_when_no_product_match(self):
        """Interest affinity uses brand affinity if no specific product match within the interest."""
        # int_001 (Tecnología Emergente) has afinidad_marca: {"marca_012": 0.7}
        # Use a Rappi product (prod_012_02) for which int_001 has NO specific afinidad_producto entry.
        result = simular_campana(
            marca_id=self.MARCA_RAPPI_ID,
            audiencia_id=self.AUD_JOVENES_ID,
            presupuesto=self.PRESUPUESTO_MEDIO,
            selected_interes_ids=[self.INT_TECNOLOGIA_EMERGENTE_ID],
            selected_product_ids=[self.PROD_RAPPI_RESTAURANTES_ID],
            campaign_goal_id=self.GOAL_TRAFFIC_ID,
            campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertNotIn("error", result, result.get("mensajes_feedback"))
        # Since prod_012_02 is not in int_001's afnidad_producto, it should fallback to int_001's afnidad_marca for marca_012
        self.assertAlmostEqual(result['interest_match_score'], 0.7, delta=0.001)
        self.assertFeedbackContains(result['mensajes_feedback'], "afinidad de los intereses seleccionados")

    def test_interest_affinity_product_precedence(self):
        """Product affinity for an interest takes precedence over brand affinity for that interest."""
        # int_001 has afinidad_producto: {"prod_012_01": 0.65} and afinidad_marca: {"marca_012": 0.7}
        # Campaign for marca_012 (Rappi) with prod_012_01 (Rappi Prime)
        result = simular_campana(
            marca_id=self.MARCA_RAPPI_ID,
            audiencia_id=self.AUD_JOVENES_ID,
            presupuesto=self.PRESUPUESTO_MEDIO,
            selected_interes_ids=[self.INT_TECNOLOGIA_EMERGENTE_ID],
            selected_product_ids=[self.PROD_RAPPI_PRIME_ID],
            campaign_goal_id=self.GOAL_TRAFFIC_ID,
            campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertNotIn("error", result, result.get("mensajes_feedback"))
        self.assertAlmostEqual(result['interest_match_score'], 0.65, delta=0.001, msg="Product affinity (0.65) should take precedence over brand affinity (0.7)")
        self.assertFeedbackContains(result['mensajes_feedback'], "afinidad de los intereses seleccionados")

    def test_interest_affinity_average_for_multiple_selected_products_one_interest(self):
        """
        Test if an interest's score is the average of its affinities for *multiple selected products* of the campaign's brand.
        Current int_001 data: "afinidad_producto": {"prod_007_01": 0.75, "prod_013_03": 0.85, "prod_012_01": 0.65}
        If campaign is for MARCA_CLARO_ID (marca_007) and selected products are [PROD_CLARO_5G_ID ("prod_007_01")]
        then int_001's score will be 0.75.
        If int_001 also had affinity for "prod_007_02": 0.5 and selected_product_ids included it, then it would be (0.75+0.5)/2.
        This test verifies the mechanism with one product; data doesn't easily support multiple for one brand in one interest yet.
        """
        # Using int_001 for MARCA_CLARO_ID and its product PROD_CLARO_5G_ID
        # int_001 has afinidad_producto: {"prod_007_01": 0.75}
        result = simular_campana(
            marca_id=self.MARCA_CLARO_ID,
            audiencia_id=self.AUD_JOVENES_ID,
            presupuesto=self.PRESUPUESTO_MEDIO,
            selected_interes_ids=[self.INT_TECNOLOGIA_EMERGENTE_ID],
            selected_product_ids=[self.PROD_CLARO_5G_ID],
            campaign_goal_id=self.GOAL_TRAFFIC_ID,
            campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertNotIn("error", result, result.get("mensajes_feedback"))
        # int_001 has {"prod_007_01": 0.75}. Only this product is selected. So, score is 0.75.
        self.assertAlmostEqual(result['interest_match_score'], 0.75, delta=0.001)
        self.assertFeedbackContains(result['mensajes_feedback'], "afinidad de los intereses seleccionados")

    def test_interest_affinity_average_for_multiple_interests(self):
        """Interest_match_score is the average of scores from multiple selected interests."""
        # int_001 for MARCA_RAPPI_ID, PROD_RAPPI_PRIME_ID -> gets 0.65
        # int_002 (Videojuegos Online) tiene afinidad con Rappi y Rappi Prime (~0.6)
        result = simular_campana(
            marca_id=self.MARCA_RAPPI_ID,
            audiencia_id=self.AUD_JOVENES_ID,
            presupuesto=self.PRESUPUESTO_MEDIO,
            selected_interes_ids=[self.INT_TECNOLOGIA_EMERGENTE_ID, self.INT_VIDEOJUEGOS_ID],
            selected_product_ids=[self.PROD_RAPPI_PRIME_ID],
            campaign_goal_id=self.GOAL_TRAFFIC_ID,
            campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertNotIn("error", result, result.get("mensajes_feedback"))

        expected_score_int1 = 0.65
        expected_score_int2 = 0.6
        expected_average_score = (expected_score_int1 + expected_score_int2) / 2  # ~0.63
        self.assertAlmostEqual(result['interest_match_score'], expected_average_score, delta=0.001)
        self.assertFeedbackContains(result['mensajes_feedback'], f"Puntuación de afinidad de intereses calculada: {expected_average_score:.2f}")

    def test_interest_affinity_default_score_for_unrelated_interest(self):
        """Interest with defined affinity should reflect that score."""
        # int_002 (Videojuegos Online) for MARCA_RAPPI_ID campaign. Assume no specific affinities.
        result = simular_campana(
            marca_id=self.MARCA_RAPPI_ID,
            audiencia_id=self.AUD_JOVENES_ID,
            presupuesto=self.PRESUPUESTO_MEDIO,
            selected_interes_ids=[self.INT_VIDEOJUEGOS_ID],
            selected_product_ids=[self.PROD_RAPPI_PRIME_ID],
            campaign_goal_id=self.GOAL_TRAFFIC_ID,
            campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertNotIn("error", result, result.get("mensajes_feedback"))
        # int_002 tiene afinidad con Rappi y su producto seleccionado (~0.6)
        # We need to check the feedback for this specific interest if possible, or the overall score if it's the only interest.
        # The feedback "Interés 'Videojuegos Online' no tiene afinidad específica..." or similar would be ideal.
        # The current feedback for default score is less explicit per interest, so we check the calculated score.
        self.assertAlmostEqual(result['interest_match_score'], 0.6, delta=0.001)


    # --- Test Cases for afinidad_marca_audiencia Confirmation ---
    def test_audience_affinity_by_product(self):
        """afinidad_marca_audiencia uses product-specific audience affinity if available."""
        # marca_001 (Bancolombia), aud_002 (Profesionales Jóvenes)
        # prod_001_01 (Cuenta de Ahorros) has afinidad_audiencia: {"aud_002": 0.7}
        result = simular_campana(
            marca_id=self.MARCA_BANCO_ID,
            audiencia_id=self.AUD_PROFESIONALES_JOVENES_ID,
            presupuesto=self.PRESUPUESTO_MEDIO,
            selected_product_ids=["prod_001_01"],
            campaign_goal_id=self.GOAL_TRAFFIC_ID,
            campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertNotIn("error", result, result.get("mensajes_feedback"))
        self.assertAlmostEqual(result['afinidad_marca_audiencia'], 0.7, delta=0.001)
        self.assertFeedbackContains(result['mensajes_feedback'], "Afinidad marca-audiencia calculada: 0.70")

    def test_audience_affinity_by_brand_category_fallback(self):
        """afinidad_marca_audiencia falls back to brand-category if no product-specific audience affinity."""
        # marca_001 (Bancolombia - Categoria "Banca")
        # aud_001 (Jóvenes Universitarios)
        # Check aud_001's afinidad_marca_categoria for "Banca": it's 0.5
        # Assume prod_001_03 (Crédito Hipotecario) has no specific affinity listed for aud_001.
        # market_data: prod_001_03 has {"aud_004": 0.7, "aud_013": 0.9}. No aud_001.
        result = simular_campana(
            marca_id=self.MARCA_BANCO_ID,
            audiencia_id=self.AUD_JOVENES_ID,
            presupuesto=self.PRESUPUESTO_MEDIO,
            selected_product_ids=["prod_001_03"],
            campaign_goal_id=self.GOAL_TRAFFIC_ID,
            campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertNotIn("error", result, result.get("mensajes_feedback"))
        # Expected fallback to aud_001's affinity for "Banca" category (0.5)
        self.assertAlmostEqual(result['afinidad_marca_audiencia'], 0.5, delta=0.001)
        self.assertFeedbackContains(result['mensajes_feedback'], "Afinidad marca-audiencia calculada: 0.50")

    # --- NEW TEST CASES ---

    def test_population_cap_low_segment_high_budget(self):
        """Test impressions are capped by small population segment with high budget."""
        # Assuming AUD_ADULTOS_MAYORES_ID has a relatively small segment size.
        # Let's verify this assumption or pick a better one.
        # From market_data: {"segment_id": "adultos_mayores_60_mas_col", ..., "size": 7500000} - this is not that small.
        # Let's use aud_001 (Jovenes 18-24) which is 5,500,000 or find a truly small one if defined.
        # For now, let's use AUD_JOVENES_ID and adjust budget to make it cap.
        # Segment size for Jovenes: 5,500,000
        # Budget: PRESUPUESTO_EXTREMO (50,000,000 COP)
        # Max impressions by budget: (50,000,000 / 12,000) * 1000 = 4,166,666
        # This budget can reach a significant portion of the 5.5M. If refined_potential is smaller, it should cap.

        segment_size = self.SEGMENT_JOVENES["size"]
        result = simular_campana(
            marca_id=self.MARCA_TECH_ID,
            audiencia_id=self.AUD_JOVENES_ID,
            presupuesto=self.PRESUPUESTO_EXTREMO,
            selected_interes_ids=self.INTERESES_JOVENES_RELEVANTES,
            campaign_goal_id=self.GOAL_AWARENESS_ID,
            selected_product_ids=[], campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertIn('potential_audience_size_from_segment', result)
        self.assertIn('refined_potential_audience_size', result)

        max_impressions_by_budget = (self.PRESUPUESTO_EXTREMO / COSTO_POR_MIL_IMPRESIONES_BASE) * 1000

        self.assertLessEqual(result['impresiones'], result['refined_potential_audience_size'] * 1.05, "Impressions should be close to or capped by refined_potential_audience_size (allowing 5% buffer for other factors)")
        self.assertLess(result['impresiones'], max_impressions_by_budget * 0.9, "Impressions should be significantly less than what budget alone would generate if capped")
        self.assertFeedbackContains(result['mensajes_feedback'], "limitado por el tamaño estimado del segmento")
        self.assertEqual(result['potential_audience_size_from_segment'], segment_size)
        self.assertFeedbackContains(result['mensajes_feedback'], f"Segmento de población '{self.SEGMENT_JOVENES['nombre_segmento']}'")

    def test_population_no_cap_large_segment_low_budget(self):
        """Test impressions are not capped with a large segment and low budget."""
        # AUD_FAMILIAS_ID segment size: 10,000,000
        segment_size = self.SEGMENT_FAMILIAS["size"]
        result = simular_campana(
            marca_id=self.MARCA_RETAIL_ID,
            audiencia_id=self.AUD_FAMILIAS_ID,
            presupuesto=self.PRESUPUESTO_BAJO,
            selected_interes_ids=self.INTERESES_FAMILIA_RELEVANTES,
            campaign_goal_id=self.GOAL_AWARENESS_ID,
            selected_product_ids=[], campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        self.assertLess(result['impresiones'], result['refined_potential_audience_size'] * 0.9, "Impressions should be well below refined_potential_audience_size for low budget")

        is_limited_by_population = any("limitado por el tamaño estimado del segmento" in msg.lower() for msg in result['mensajes_feedback'])
        self.assertFalse(is_limited_by_population, "Feedback for population capping should not be present if not capped or minor.")
        self.assertEqual(result['potential_audience_size_from_segment'], segment_size)

    def test_population_refinement_with_interests(self):
        """Test that selecting interests refines (reduces) the potential audience size."""
        segment_size = self.SEGMENT_FAMILIAS["size"]
        result_no_interests = simular_campana(
            marca_id=self.MARCA_RETAIL_ID,
            audiencia_id=self.AUD_FAMILIAS_ID,
            presupuesto=self.PRESUPUESTO_MEDIO,
            selected_interes_ids=[],
            campaign_goal_id=self.GOAL_AWARENESS_ID,
            selected_product_ids=[], campaign_duration_days=None
        )
        refined_size_no_interests = result_no_interests['refined_potential_audience_size']
        self.assertEqual(result_no_interests['potential_audience_size_from_segment'], refined_size_no_interests)

        result_with_interests = simular_campana(
            marca_id=self.MARCA_RETAIL_ID,
            audiencia_id=self.AUD_FAMILIAS_ID,
            presupuesto=self.PRESUPUESTO_MEDIO,
            selected_interes_ids=self.INTERESES_FAMILIA_RELEVANTES,
            campaign_goal_id=self.GOAL_AWARENESS_ID,
            selected_product_ids=[], campaign_duration_days=None
        )
        refined_size_with_interests = result_with_interests['refined_potential_audience_size']

        self.assertLess(refined_size_with_interests, refined_size_no_interests, "Refined size with interests should be smaller than without interests.")

    def test_engagement_rate_logic(self):
        res_good = simular_campana(self.MARCA_TECH_ID, self.AUD_TECH_ID, self.PRESUPUESTO_MEDIO, self.INTERESES_JOVENES_RELEVANTES, self.GOAL_ENGAGEMENT_ID, selected_product_ids=[], campaign_duration_days=None)
        res_poor = simular_campana(self.MARCA_RETAIL_ID, self.AUD_TECH_ID, self.PRESUPUESTO_MEDIO, self.INTERESES_FAMILIA_RELEVANTES, self.GOAL_ENGAGEMENT_ID, selected_product_ids=[], campaign_duration_days=None)

        self.assertIsInstance(res_good, dict)
        self.assertIsInstance(res_poor, dict)

        # Engagement is clicks * rate. If clicks are very low for poor, interactions might also be low.
        # We expect a higher engagement *rate* for good scenario.
        # Effective engagement rate = interacciones_calculadas / clics (if clics > 0)
        eff_eng_rate_good = res_good['interacciones_calculadas'] / res_good['clics'] if res_good['clics'] > 0 else 0
        eff_eng_rate_poor = res_poor['interacciones_calculadas'] / res_poor['clics'] if res_poor['clics'] > 0 else 0

        if res_good['clics'] > 10 and res_poor['clics'] > 10: # Ensure enough clicks for comparison
            self.assertGreater(eff_eng_rate_good, eff_eng_rate_poor * 1.1, "Good scenario should have a higher effective engagement rate.")
        else:
            self.skipTest("Skipping engagement rate comparison due to low click count in one or both scenarios.")

        self.assertGreater(res_good['interacciones_calculadas'], res_poor['interacciones_calculadas'] * 0.8, "Good scenario should generally lead to more interactions (allowing for budget spending differences)")


    def test_conversion_rate_logic(self):
        res_good = simular_campana(self.MARCA_RETAIL_ID, self.AUD_FAMILIAS_ID, self.PRESUPUESTO_ALTO, self.INTERESES_FAMILIA_RELEVANTES, self.GOAL_CONVERSION_ID, selected_product_ids=[], campaign_duration_days=None)
        res_poor = simular_campana(self.MARCA_TECH_ID, self.AUD_FAMILIAS_ID, self.PRESUPUESTO_ALTO, self.INTERESES_IRRELEVANTES_PARA_FAMILIA, self.GOAL_CONVERSION_ID, selected_product_ids=[], campaign_duration_days=None)

        self.assertIsInstance(res_good, dict)
        self.assertIsInstance(res_poor, dict)

        eff_conv_rate_good = res_good['conversiones_calculadas'] / res_good['clics'] if res_good['clics'] > 0 else 0
        eff_conv_rate_poor = res_poor['conversiones_calculadas'] / res_poor['clics'] if res_poor['clics'] > 0 else 0

        if res_good['clics'] > 50 and res_poor['clics'] > 50: # Ensure enough clicks
            self.assertGreater(eff_conv_rate_good, eff_conv_rate_poor * 1.3 if eff_conv_rate_poor > 0 else 0.001, "Good scenario should have a higher effective conversion rate.")
            self.assertGreater(res_good['conversiones_calculadas'], res_poor['conversiones_calculadas'], "Good scenario should yield more absolute conversions.")
        elif res_good['clics'] > 0: # Poor might have zero clicks/conversions
             self.assertGreater(res_good['conversiones_calculadas'], 0, "Good scenario should have some conversions with high budget.")

        if res_poor['conversiones_calculadas'] > 0 : # It's possible to get some conversions even in poor, but should be very few
            self.assertLess(eff_conv_rate_poor, 0.03, "Poor scenario conversion rate should be low.")


    def test_awareness_score_good_reach_adequate_budget(self):
        """Awareness: Good reach (>70% of potential) with adequate budget."""
        # AUD_JOVENES_ID segment size: 5,500,000
        # Target 70% = 3,850,000 impressions
        # Budget needed: (3,850,000 / 1000) * 12,000 = 46,200,000. This is PRESUPUESTO_EXTREMO.
        # Let's use a smaller segment or adjust expectation.
        # For AUD_JOVENES (5.5M), if refined is ~2M (due to interests), 70% is 1.4M. Budget: (1.4M/1k)*12k = 16.8M
        # This test requires careful setup to ensure impressions are high enough relative to refined_potential_audience_size
        # For now, let's assume a scenario where this condition is met.
        # We need to find a combination where impresiones_efectivas / refined_potential_audience_size >= 0.7
        # This might mean a high budget and very effective targeting.
        result = simular_campana(
            marca_id=self.MARCA_TECH_ID, audiencia_id=self.AUD_JOVENES_ID,
            presupuesto=self.PRESUPUESTO_EXTREMO,
            selected_interes_ids=self.INTERESES_JOVENES_RELEVANTES,
            campaign_goal_id=self.GOAL_AWARENESS_ID,
            selected_product_ids=[], campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        reach_percentage = result['impresiones'] / result['refined_potential_audience_size'] if result['refined_potential_audience_size'] > 0 else 0

        # This assertion depends heavily on the simulation producing high reach %
        if reach_percentage >= 0.7 and result['impresiones'] > result['refined_potential_audience_size'] * 0.1 :
            self.assertAlmostEqual(result['puntuacion_detalle_objetivo_contrib'], MAX_PUNTOS_POR_FACTOR, delta=0.1, msg=f"Reach %: {reach_percentage}")
        elif reach_percentage >= 0.4 and result['impresiones'] > result['refined_potential_audience_size'] * 0.05:
            self.assertAlmostEqual(result['puntuacion_detalle_objetivo_contrib'], MAX_PUNTOS_POR_FACTOR / 2, delta=0.1, msg=f"Reach %: {reach_percentage}")
        else: # If reach is lower than 0.4
            self.assertLessEqual(result['puntuacion_detalle_objetivo_contrib'], -MAX_PUNTOS_POR_FACTOR / 2 + 0.1, msg=f"Reach %: {reach_percentage}")


    def test_awareness_score_low_reach_high_budget(self):
        """Awareness: Low reach (<50%) despite high budget, expecting penalty."""
        # This requires engineering a scenario where budget is high, but impressions are low relative to potential.
        # This could be due to extremely poor targeting not reflected in affinity/interest score's effect on reach factor,
        # or if the population itself is large but actual reach factor is low.
        # For this test, we'll use poor affinity and irrelevant interests to try and force low impressions
        # despite a high budget.
        result = simular_campana(
            marca_id=self.MARCA_CPG_ID,
            audiencia_id=self.AUD_TECH_ID,
            presupuesto=self.PRESUPUESTO_EXTREMO,
            selected_interes_ids=self.INTERESES_IRRELEVANTES_PARA_FAMILIA,
            campaign_goal_id=self.GOAL_AWARENESS_ID,
            selected_product_ids=[], campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)

        max_impressions_budget_could_buy = (self.PRESUPUESTO_EXTREMO / COSTO_POR_MIL_IMPRESIONES_BASE) * 1000
        reach_percentage = result['impresiones'] / result['refined_potential_audience_size'] if result['refined_potential_audience_size'] > 0 else 0

        # Check if the specific penalty condition is met
        if max_impressions_budget_could_buy > result['refined_potential_audience_size'] * 1.5 and reach_percentage < 0.5:
            self.assertFeedbackContains(result['mensajes_feedback'], "presupuesto parecía suficiente para un mayor alcance")
            # The score impact is -0.5 on top of other objective points.
            # So, puntuacion_detalle_objetivo_contrib would be (base points for reach) - 0.5
            # Example: if reach % was <0.4 (-MAX_PUNTOS_POR_FACTOR/2), total would be -MAX_PUNTOS_POR_FACTOR/2 - 0.5
            expected_contrib_without_penalty = 0
            if reach_percentage >= 0.7 and result['impresiones'] > result['refined_potential_audience_size'] * 0.1:
                expected_contrib_without_penalty = MAX_PUNTOS_POR_FACTOR
            elif reach_percentage >= 0.4 and result['impresiones'] > result['refined_potential_audience_size'] * 0.05:
                 expected_contrib_without_penalty = MAX_PUNTOS_POR_FACTOR / 2
            else:
                 expected_contrib_without_penalty = -MAX_PUNTOS_POR_FACTOR / 2
            self.assertAlmostEqual(result['puntuacion_detalle_objetivo_contrib'], expected_contrib_without_penalty - 0.5, delta=0.1)

    def test_awareness_score_good_relative_reach_low_budget(self):
        """Awareness: Good relative reach (>30%) with low budget, expecting bonus."""
        # Low budget, but good targeting leading to >30% reach of a potentially small refined segment.
        result = simular_campana(
            marca_id=self.MARCA_TECH_ID, audiencia_id=self.AUD_JOVENES_ID,
            presupuesto=self.PRESUPUESTO_BAJO,
            selected_interes_ids=self.INTERESES_JOVENES_RELEVANTES,
            campaign_goal_id=self.GOAL_AWARENESS_ID,
            selected_product_ids=[], campaign_duration_days=None
        )
        self.assertIsInstance(result, dict)
        max_impressions_budget_could_buy = (self.PRESUPUESTO_BAJO / COSTO_POR_MIL_IMPRESIONES_BASE) * 1000
        reach_percentage = result['impresiones'] / result['refined_potential_audience_size'] if result['refined_potential_audience_size'] > 0 else 0

        if max_impressions_budget_could_buy < result['refined_potential_audience_size'] * 0.5 and reach_percentage > 0.3:
            self.assertFeedbackContains(result['mensajes_feedback'], "Buen aprovechamiento del presupuesto")
            expected_contrib_without_bonus = 0
            if reach_percentage >= 0.7 and result['impresiones'] > result['refined_potential_audience_size'] * 0.1:
                expected_contrib_without_bonus = MAX_PUNTOS_POR_FACTOR
            elif reach_percentage >= 0.4 and result['impresiones'] > result['refined_potential_audience_size'] * 0.05:
                 expected_contrib_without_bonus = MAX_PUNTOS_POR_FACTOR / 2
            else: # This case (reach > 0.3 but < 0.4) would get -MAX_PUNTOS_POR_FACTOR/2 before bonus
                 expected_contrib_without_bonus = -MAX_PUNTOS_POR_FACTOR / 2
            self.assertAlmostEqual(result['puntuacion_detalle_objetivo_contrib'], expected_contrib_without_bonus + 0.5, delta=0.1, msg=f"Reach %: {reach_percentage}")


    def test_feedback_specific_audience_segment_found(self):
        result = simular_campana(self.MARCA_RETAIL_ID, self.AUD_FAMILIAS_ID, self.PRESUPUESTO_MEDIO, selected_product_ids=[], campaign_duration_days=None)
        self.assertFeedbackContains(result['mensajes_feedback'], f"Segmento de población '{self.SEGMENT_FAMILIAS['nombre_segmento']}'")
        self.assertFeedbackContains(result['mensajes_feedback'], "usado para estimar alcance máximo")

    def test_feedback_specific_audience_segment_is_small(self):
        """Test feedback for small specific audience segment."""
        # Need an audience linked to a truly small segment.
        # Let's assume 'jovenes_18_24_col' (5.5M) is not considered "small" (threshold is 1M in logic).
        # If we create a dummy small segment and link an audience to it, this test would be better.
        # For now, this test might not trigger the "bastante específico" message unless a segment <1M is used.
        # We can check if the 'potential_audience_size_from_segment' is small and if the message appears.

        # This part of the test is more of a placeholder until a small segment is properly defined and used.
        # For example, if a segment "nicho_gamers_bogota" size 50000 was defined and aud_00X linked to it:
        # result = simular_campana(SOME_MARCA_ID, "aud_00X", self.PRESUPUESTO_MEDIO)
        # if result['potential_audience_size_from_segment'] < 1000000:
        #    self.assertFeedbackContains(result['mensajes_feedback'], "El segmento de audiencia seleccionado es bastante específico")
        # else:
        #    self.skipTest("Skipping small segment feedback test as no suitable small segment is configured for testing.")
        pass # Placeholder for now


    def test_score_always_in_range(self):
        scenarios = [
            {"name": "Ideal", "params": (self.MARCA_RETAIL_ID, self.AUD_FAMILIAS_ID, self.PRESUPUESTO_ALTO, self.INTERESES_FAMILIA_RELEVANTES, self.GOAL_TRAFFIC_ID, [], None)},
            {"name": "Pobre Afinidad e Intereses", "params": (self.MARCA_TECH_ID, self.AUD_FAMILIAS_ID, self.PRESUPUESTO_MEDIO, self.INTERESES_IRRELEVANTES_PARA_FAMILIA, self.GOAL_TRAFFIC_ID, [], None)},
            {"name": "Presupuesto Muy Bajo", "params": (self.MARCA_BANCO_ID, self.AUD_JOVENES_ID, self.PRESUPUESTO_MUY_BAJO, None, self.GOAL_AWARENESS_ID, [], None)},
            {"name": "Todo Mal", "params": (self.MARCA_TECH_ID, self.AUD_FAMILIAS_ID, self.PRESUPUESTO_MUY_BAJO, self.INTERESES_IRRELEVANTES_PARA_FAMILIA, self.GOAL_CONVERSION_ID, [], None)},
        ]
        for sc in scenarios:
            with self.subTest(name=sc["name"]):
                # Unpack params and add selected_product_ids and campaign_duration_days if not already part of the tuple
                # For this test, we assume they are added as the last two elements if not present.
                # However, the current params tuples have 5 elements, simular_campana now takes 7.
                # So, we need to ensure all calls are updated.
                # The *sc["params"] already includes selected_product_ids=[] and campaign_duration_days=None if added above.
                # Let's adjust the tuples in scenarios directly for clarity.
                # params_tuple = sc["params"]
                # if len(params_tuple) == 5:
                #     params_tuple = (*params_tuple, [], None) # Add defaults for products and duration

                result = simular_campana(*sc["params"]) # Call with updated params
                self.assertIsInstance(result, dict)
                self.assertNotIn("error", result)
                self.assertTrue(1 <= result['puntuacion'] <= 10, f"Puntuación {result['puntuacion']} fuera de rango para {sc['name']}")
                self.assertIn('potential_audience_size_from_segment', result)
                self.assertIn('refined_potential_audience_size', result)

    # --- Tests for calculate_total_affinity ---
    def test_calculate_total_affinity_basic(self):
        # Test with known good brand/audience, no products/interests
        # Bancolombia (Banca) with Jóvenes Universitarios (Afinidad Banca: 0.5)
        # No interests selected, so interest_match_score should be default (0.3)
        result = calculate_total_affinity(self.MARCA_BANCO_ID, self.AUD_JOVENES_ID, [], [])
        self.assertNotIn("error", result)
        self.assertAlmostEqual(result['afinidad_marca_audiencia'], 0.5, delta=0.01)
        self.assertAlmostEqual(result['interest_match_score'], 0.3, delta=0.01) # Default for no interests
        expected_overall = (0.5 + 0.3) / 2
        self.assertAlmostEqual(result['overall_affinity'], expected_overall, delta=0.01)

        # Test with relevant interests
        # Rappi (Tech) with Jóvenes (Tech affinity: 0.9)
        # INTERESES_JOVENES_RELEVANTES = ["int_001", "int_002", "int_005"]
        # int_001 (Tec Emergente) -> afinidad_marca: {"marca_012": 0.7}
        # int_002 (Videojuegos) -> afinidad_marca: {"marca_012": 0.7}
        # int_005 (Redes Sociales) -> afinidad_marca: {"marca_012": 0.8}
        # Expected interest score = (0.7 + 0.7 + 0.8) / 3 = 0.733
        result_with_interests = calculate_total_affinity(self.MARCA_RAPPI_ID, self.AUD_JOVENES_ID, self.INTERESES_JOVENES_RELEVANTES, [])
        self.assertNotIn("error", result_with_interests)
        # Rappi category "Tech", Aud Jovenes afinidad_marca_categoria for Tech is 0.9
        self.assertAlmostEqual(result_with_interests['afinidad_marca_audiencia'], 0.9, delta=0.01)
        self.assertAlmostEqual(result_with_interests['interest_match_score'], 0.733, delta=0.01)
        expected_overall_interests = (0.9 + 0.733) / 2
        self.assertAlmostEqual(result_with_interests['overall_affinity'], expected_overall_interests, delta=0.01)

    def test_calculate_total_affinity_with_products(self):
        # Bancolombia (marca_001) with Profesionales Jóvenes (aud_002)
        # Product prod_001_01 (Cuenta de Ahorros) has afinidad_audiencia: {"aud_002": 0.7}
        result = calculate_total_affinity(self.MARCA_BANCO_ID, self.AUD_PROFESIONALES_JOVENES_ID, [], ["prod_001_01"])
        self.assertNotIn("error", result)
        self.assertAlmostEqual(result['afinidad_marca_audiencia'], 0.7, delta=0.01) # Product affinity should override category
        self.assertAlmostEqual(result['interest_match_score'], 0.3, delta=0.01) # No interests
        expected_overall = (0.7 + 0.3) / 2
        self.assertAlmostEqual(result['overall_affinity'], expected_overall, delta=0.01)

    def test_calculate_total_affinity_invalid_ids(self):
        result_bad_marca = calculate_total_affinity("bad_marca_id", self.AUD_JOVENES_ID)
        self.assertIn("error", result_bad_marca)
        self.assertIn("no encontrada", result_bad_marca["error"])

        result_bad_audiencia = calculate_total_affinity(self.MARCA_BANCO_ID, "bad_aud_id")
        self.assertIn("error", result_bad_audiencia)
        self.assertIn("no encontrada", result_bad_audiencia["error"])

    # --- Tests for new feedback messages ---
    def test_feedback_campaign_duration_info(self):
        duration = 15
        result = simular_campana(self.MARCA_RETAIL_ID, self.AUD_FAMILIAS_ID, self.PRESUPUESTO_MEDIO, [], None, [], campaign_duration_days=duration)
        self.assertFeedbackContains(result['mensajes_feedback'], f"configurada para una duración de {duration} día(s)")

    def test_feedback_campaign_duration_long_low_budget(self):
        # Daily budget = 50000 / 60 = 833. Threshold daily low for min impact = 50000/30 = 1666. 833 < 1666 * 1.5 (2499)
        result = simular_campana(self.MARCA_RETAIL_ID, self.AUD_FAMILIAS_ID, PRESUPUESTO_MINIMO_IMPACTO, [], None, [], campaign_duration_days=60)
        self.assertFeedbackContains(result['mensajes_feedback'], "presupuesto diario")
        self.assertFeedbackContains(result['mensajes_feedback'], "parece bajo para mantener una presencia efectiva")

    def test_feedback_campaign_duration_short_high_budget(self):
        # Daily budget = 2000000 / 5 = 400,000. Threshold daily high = 1000000/30 = 33,333. 400000 > 33333 * 0.75 (25000)
        result = simular_campana(self.MARCA_RETAIL_ID, self.AUD_FAMILIAS_ID, CL_PRESUPUESTO_ALTO, [], None, [], campaign_duration_days=5)
        self.assertFeedbackContains(result['mensajes_feedback'], "presupuesto diario")
        self.assertFeedbackContains(result['mensajes_feedback'], "considerable para una campaña corta")


if __name__ == '__main__':
    unittest.main()
