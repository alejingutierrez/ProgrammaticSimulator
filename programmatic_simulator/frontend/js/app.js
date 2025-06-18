// programmatic_simulator/frontend/js/app.js

document.addEventListener('DOMContentLoaded', () => {
    const campaignForm = document.getElementById('campaignForm');
    const marcaSelect = document.getElementById('marca');
    const audienciaSelect = document.getElementById('audiencia');
    const resultsContainer = document.getElementById('resultsContainer');

    const originalResultsHTML = `
            <h2>Resultados de la Simulación</h2>
            <p><strong>Marca:</strong> <span id="resMarca"></span></p>
            <p><strong>Audiencia:</strong> <span id="resAudiencia"></span></p>
            <p><strong>Presupuesto Inicial (COP):</strong> <span id="resPresupuestoInicial"></span></p>
            <hr>
            <p class="score"><strong>Puntuación de la Campaña:</strong> <span id="resPuntuacion"></span> / 10</p>
            <hr>
            <p><strong>Impresiones Estimadas:</strong> <span id="resImpresiones"></span></p>
            <p><strong>Clics Estimados:</strong> <span id="resClics"></span></p>
            <p><strong>CPM Calculado (COP):</strong> <span id="resCPM"></span></p>
            <p><strong>CPC Calculado (COP):</strong> <span id="resCPC"></span></p>
            <p><strong>Presupuesto Gastado (COP):</strong> <span id="resPresupuestoGastado"></span></p>
            <hr>
            <p><em><span id="resMensaje"></span></em></p>
    `;

    function cargarSelect(selectElement, data, defaultOptionText) {
        selectElement.innerHTML = `<option value="">${defaultOptionText}</option>`; // Limpiar y poner placeholder
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            option.textContent = item.nombre;
            selectElement.appendChild(option);
        });
    }

    campaignForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const marcaId = marcaSelect.value;
        const audienciaId = audienciaSelect.value;
        const presupuesto = document.getElementById('presupuesto').value;

        if (!marcaId || !audienciaId) {
            alert("Por favor, selecciona una marca y una audiencia.");
            return;
        }

        resultsContainer.style.display = 'none'; // Ocultar resultados anteriores
        resultsContainer.innerHTML = '<p>Simulando...</p>'; // Mensaje de carga
        resultsContainer.style.display = 'block';


        try {
            const response = await fetch('http://localhost:5001/api/simular', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    marcaId: marcaId,
                    audienciaId: audienciaId,
                    presupuesto: presupuesto
                }),
            });

            if (!response.ok) {
                // Si el servidor responde con un error (4xx, 5xx)
                const errorData = await response.json().catch(() => ({ error: "Error desconocido del servidor" }));
                throw new Error(errorData.error || `Error del servidor: ${response.status}`);
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            console.error('Error al simular campaña:', error);
            displayResults({ error: error.message || "No se pudo conectar con el servidor de simulación." });
        }
    });

    // Modifica la carga inicial de datos para que use el nuevo endpoint del backend
    async function cargarDatosIniciales() {
        try {
            const response = await fetch('http://localhost:5001/api/market-data');
            if (!response.ok) {
                throw new Error(`Error al cargar datos de mercado: ${response.status}`);
            }
            const data = await response.json();
            cargarSelect(marcaSelect, data.marcas, "Selecciona una marca");
            cargarSelect(audienciaSelect, data.audiencias, "Selecciona una audiencia");
        } catch (error) {
            console.error('Error al cargar datos iniciales:', error);
            marcaSelect.innerHTML = '<option value="">Error al cargar marcas</option>';
            audienciaSelect.innerHTML = '<option value="">Error al cargar audiencias</option>';
            alert("No se pudieron cargar los datos de marcas y audiencias desde el servidor. Verifica que el backend esté funcionando.\n" + error.message);
        }
    }

    function displayResults(data) {
        if (data.error) {
            resultsContainer.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
        } else {
            // Restaurar la estructura original antes de poblar
            resultsContainer.innerHTML = originalResultsHTML;

            document.getElementById('resMarca').textContent = data.marca_nombre;
        document.getElementById('resAudiencia').textContent = data.audiencia_nombre;
        document.getElementById('resPresupuestoInicial').textContent = data.presupuesto_inicial?.toLocaleString('es-CO', { style: 'currency', currency: 'COP' }) || 'N/A';
        document.getElementById('resPuntuacion').textContent = data.puntuacion;
        document.getElementById('resImpresiones').textContent = data.impresiones?.toLocaleString('es-CO') || 'N/A';
        document.getElementById('resClics').textContent = data.clics?.toLocaleString('es-CO') || 'N/A';
        document.getElementById('resCPM').textContent = data.cpm_calculado?.toLocaleString('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }) || 'N/A';
        document.getElementById('resCPC').textContent = data.cpc_calculado?.toLocaleString('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }) || 'N/A';
        document.getElementById('resPresupuestoGastado').textContent = data.presupuesto_gastado?.toLocaleString('es-CO', { style: 'currency', currency: 'COP' }) || 'N/A';
        document.getElementById('resMensaje').textContent = data.mensaje;
        }
        resultsContainer.style.display = 'block';
    }

    // Llama a la nueva función para cargar datos al inicio
    cargarDatosIniciales();
});
