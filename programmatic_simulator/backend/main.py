# programmatic_simulator/backend/main.py
from flask import Flask, request, jsonify
from flask_cors import CORS # Importar CORS
from simulator.campaign_logic import simular_campana, _calculate_audience_size_details # Importar la nueva función
from data.market_data import MARCAS_COLOMBIANAS, AUDIENCIAS_COLOMBIANAS, obtener_todos_los_intereses, obtener_todos_los_campaign_goals

app = Flask(__name__)
CORS(app) # Habilitar CORS para todas las rutas y orígenes

# Dummy function calculate_audience_size has been removed.

@app.route('/')
def home():
    return "Backend del Simulador Programático funcionando."

@app.route('/api/market-data', methods=['GET'])
def get_market_data():
    """Endpoint para obtener los datos de mercado (marcas, audiencias y objetivos de campaña)."""
    return jsonify({
        "marcas": MARCAS_COLOMBIANAS,
        "audiencias": AUDIENCIAS_COLOMBIANAS,
        "campaign_goals": obtener_todos_los_campaign_goals() # Añadir objetivos de campaña
    })

@app.route('/api/interests-data', methods=['GET'])
# Este endpoint podría quedar obsoleto si los intereses se sirven desde /api/market-data,
# pero se mantiene por ahora según el plan original de la tarea anterior.
# Considerar unificar en el futuro si es conveniente.
def get_interests_data():
    """Endpoint para obtener todos los intereses detallados."""
    intereses = obtener_todos_los_intereses()
    return jsonify(intereses)

@app.route('/api/simular', methods=['POST'])
def api_simular_campana():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se recibieron datos."}), 400

    marca_id = data.get('marcaId')
    audiencia_id = data.get('audienciaId')
    presupuesto_str = data.get('presupuesto')
    selected_interes_ids = data.get('selectedInteresIds', [])
    campaign_goal_id = data.get('campaignGoalId', None) # Nuevo: obtener ID del objetivo de campaña

    if not marca_id or not audiencia_id or not presupuesto_str:
        return jsonify({"error": "Faltan datos: marcaId, audienciaId o presupuesto son requeridos."}), 400

    try:
        presupuesto = float(presupuesto_str)
        if presupuesto < 0:
            raise ValueError("El presupuesto no puede ser negativo.")
    except ValueError as e:
        return jsonify({"error": f"Presupuesto inválido: {e}"}), 400

    # Llamada a la lógica de simulación actualizada con el objetivo de campaña
    resultado_simulacion = simular_campana(
        marca_id,
        audiencia_id,
        presupuesto,
        selected_interes_ids,
        campaign_goal_id
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
    # Puerto 5001 para evitar conflictos comunes con el puerto 5000
    app.run(debug=True, port=5001)
