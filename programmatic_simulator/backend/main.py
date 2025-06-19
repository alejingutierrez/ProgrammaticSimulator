# programmatic_simulator/backend/main.py
import os
import sys
import logging
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar CORS

# Permitir ejecutar este archivo directamente sin usar "-m".
if __package__ in (None, ""):
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    __package__ = "programmatic_simulator.backend"
from .simulator.campaign_logic import (
    simular_campana,
    _calculate_audience_size_details,
    calculate_total_affinity,
)
from .data.market_data import (
    MARCAS_COLOMBIANAS,
    AUDIENCIAS_COLOMBIANAS,
    obtener_todos_los_intereses,
    obtener_todos_los_campaign_goals,
    obtener_marca_por_id,
)

app = Flask(__name__)
CORS(app) # Habilitar CORS para todas las rutas y orígenes

logging.basicConfig(level=logging.DEBUG)

# Dummy function calculate_audience_size has been removed.

@app.route('/')
def home():
    return "Backend del Simulador Programático funcionando."

@app.route('/api/market-data', methods=['GET'])
def get_market_data():
    """Endpoint para obtener los datos de mercado (marcas, audiencias y objetivos de campaña)."""
    try:
        data_to_return = {
            "marcas": MARCAS_COLOMBIANAS,
            "audiencias": AUDIENCIAS_COLOMBIANAS,
            "campaign_goals": obtener_todos_los_campaign_goals()
        }
        # Optionally, you could try to jsonify parts of the data here for more granular logging
        # For example:
        # jsonify({"marcas": MARSAS_COLOMBIANAS}) # Test this
        # jsonify({"audiencias": AUDIENCIAS_COLOMBIANAS}) # Test this
        # jsonify({"campaign_goals": obtener_todos_los_campaign_goals()}) # Test this
        return jsonify(data_to_return)
    except Exception as e:
        logging.error(f"Error in get_market_data: {str(e)}")
        logging.error(traceback.format_exc())
        # You could try to identify which part failed if you broke it down
        # For now, just return a more informative error
        return jsonify({"error": "Server error during JSON serialization in get_market_data", "details": str(e)}), 500

@app.route('/api/interests-data', methods=['GET'])
# Este endpoint podría quedar obsoleto si los intereses se sirven desde /api/market-data,
# pero se mantiene por ahora según el plan original de la tarea anterior.
# Considerar unificar en el futuro si es conveniente.
def get_interests_data():
    """Endpoint para obtener todos los intereses detallados."""
    try:
        intereses = obtener_todos_los_intereses()
        return jsonify(intereses)
    except Exception as e:
        logging.error(f"Error in get_interests_data: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({"error": "Server error during JSON serialization in get_interests_data", "details": str(e)}), 500

@app.route('/api/simular', methods=['POST'])
def api_simular_campana():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se recibieron datos."}), 400

    marca_id = data.get('marcaId')
    audiencia_id = data.get('audienciaId')
    presupuesto_str = data.get('presupuesto') # This is now total_budget from frontend
    selected_interes_ids = data.get('selectedInteresIds', [])
    campaign_goal_id = data.get('campaignGoalId', None)
    selected_product_ids = data.get('selected_product_ids', []) # Get selected product IDs
    campaign_duration_days = data.get('campaignDurationDays', None) # Get campaign duration

    if not marca_id or not audiencia_id or not presupuesto_str: # campaign_duration_days is optional for now from backend view
        return jsonify({"error": "Faltan datos: marcaId, audienciaId o presupuesto son requeridos."}), 400

    try:
        presupuesto = float(presupuesto_str)
        if presupuesto < 0:
            raise ValueError("El presupuesto no puede ser negativo.")
    except ValueError as e:
        return jsonify({"error": f"Presupuesto inválido: {e}"}), 400

    # Llamada a la lógica de simulación actualizada con el objetivo de campaña
    resultado_simulacion = simular_campana(
        marca_id=marca_id,
        audiencia_id=audiencia_id,
        presupuesto=presupuesto, # This is total_budget
        selected_interes_ids=selected_interes_ids,
        campaign_goal_id=campaign_goal_id,
        selected_product_ids=selected_product_ids, # Pass product IDs
        campaign_duration_days=campaign_duration_days # Pass duration
    )

    if resultado_simulacion.get("error"):
         return jsonify(resultado_simulacion), 404

    return jsonify(resultado_simulacion)

@app.route('/api/estimate-audience-size', methods=['GET'])
def estimate_audience_size_endpoint():
    audiencia_id = request.args.get('audienciaId')
    selected_interes_ids = request.args.getlist('selectedInteresIds') # Use getlist for multiple values

    if not audiencia_id:
        return jsonify({"error": "El parámetro 'audienciaId' es requerido."}), 400

    # Call the new function from campaign_logic
    result = _calculate_audience_size_details(audiencia_id, selected_interes_ids)

    if not result.get("audience_found"):
        # The status_code should be present if audience_found is False
        status_code = result.get("status_code", 404)
        return jsonify({"error": result.get("error_message", "Error al calcular la audiencia.")}), status_code

    # Return only the relevant sizing details for this endpoint, not internal flags like 'audience_found'
    response_data = {
        "potential_audience_size_from_segment": result.get("potential_audience_size_from_segment"),
        "refined_potential_audience_size": result.get("refined_potential_audience_size"),
        # Optionally, include some feedback messages if they are relevant for this specific endpoint
        # "feedback": result.get("feedback_messages")
    }
    return jsonify(response_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, port=port)


@app.route('/api/products/<brand_id>', methods=['GET'])
def get_products_by_brand(brand_id):
    """Endpoint para obtener los productos de una marca específica."""
    marca = obtener_marca_por_id(brand_id)
    if marca:
        return jsonify(marca.get("productos", []))
    else:
        return jsonify({"error": "Brand not found"}), 404

@app.route('/api/calculate-affinity', methods=['POST'])
def api_calculate_total_affinity():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided."}), 400

    marca_id = data.get('marcaId')
    audiencia_id = data.get('audienciaId')

    if not marca_id or not audiencia_id:
        return jsonify({"error": "marcaId and audienciaId are required."}), 400

    selected_interes_ids = data.get('selectedInteresIds', [])
    selected_product_ids = data.get('selectedProductIds', [])

    affinity_results = calculate_total_affinity(
        marca_id=marca_id,
        audiencia_id=audiencia_id,
        selected_interes_ids=selected_interes_ids,
        selected_product_ids=selected_product_ids
    )

    if affinity_results.get("error"):
        # Determine status code based on error message or keep it generic
        # For "not found" errors from calculate_total_affinity, 404 is appropriate.
        # Other errors might be 400 if they relate to bad input not caught above.
        status_code = 404 if "no encontrada" in affinity_results["error"] else 400
        return jsonify(affinity_results), status_code

    return jsonify(affinity_results), 200
