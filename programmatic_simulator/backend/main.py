# programmatic_simulator/backend/main.py
from flask import Flask, request, jsonify
from flask_cors import CORS # Importar CORS
from simulator.campaign_logic import simular_campana
from data.market_data import MARCAS_COLOMBIANAS, AUDIENCIAS_COLOMBIANAS

app = Flask(__name__)
CORS(app) # Habilitar CORS para todas las rutas y orígenes

@app.route('/')
def home():
    return "Backend del Simulador Programático funcionando."

@app.route('/api/market-data', methods=['GET'])
def get_market_data():
    """Endpoint para obtener los datos de mercado (marcas y audiencias)."""
    return jsonify({
        "marcas": MARCAS_COLOMBIANAS,
        "audiencias": AUDIENCIAS_COLOMBIANAS
    })

@app.route('/api/simular', methods=['POST'])
def api_simular_campana():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se recibieron datos."}), 400

    marca_id = data.get('marcaId')
    audiencia_id = data.get('audienciaId')
    presupuesto_str = data.get('presupuesto')

    if not marca_id or not audiencia_id or not presupuesto_str:
        return jsonify({"error": "Faltan datos: marcaId, audienciaId o presupuesto son requeridos."}), 400

    try:
        presupuesto = float(presupuesto_str)
        if presupuesto < 0:
            raise ValueError("El presupuesto no puede ser negativo.")
    except ValueError as e:
        return jsonify({"error": f"Presupuesto inválido: {e}"}), 400

    # Aquí llamas a tu lógica de simulación
    # from simulator.campaign_logic import simular_campana
    resultado_simulacion = simular_campana(marca_id, audiencia_id, presupuesto)

    if resultado_simulacion.get("error"):
         return jsonify(resultado_simulacion), 404 # Si la marca/audiencia no se encuentra

    return jsonify(resultado_simulacion)

if __name__ == '__main__':
    # Puerto 5001 para evitar conflictos comunes con el puerto 5000
    app.run(debug=True, port=5001)
