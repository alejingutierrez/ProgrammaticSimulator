// programmatic_simulator/frontend/js/app.js

document.addEventListener('DOMContentLoaded', () => {
    const campaignForm = document.getElementById('campaignForm');
    const marcaSelect = document.getElementById('marca');
    const audienciaSelect = document.getElementById('audiencia');
    const interesesSelect = document.getElementById('intereses');
    const campaignGoalSelect = document.getElementById('campaignGoal'); // Nueva referencia
    const resultsContainer = document.getElementById('resultsContainer');

    // Actualizado para coincidir con los nuevos campos en index.html
    const originalResultsHTML = `
            <h2>Resultados de la Simulación</h2>
            <p><strong>Marca:</strong> <span id="resMarca"></span></p>
            <p><strong>Audiencia:</strong> <span id="resAudiencia"></span></p>
            <p><strong>Objetivo de Campaña:</strong> <span id="resCampaignGoal"></span></p>
            <p><strong>Presupuesto Inicial (COP):</strong> <span id="resPresupuestoInicial"></span></p>
            <hr>
            <p class="score"><strong>Puntuación de la Campaña:</strong> <span id="resPuntuacion"></span> / 10</p>
            <p><strong>Afinidad Marca-Audiencia:</strong> <span id="resAfinidad"></span></p>
            <p><strong>Coincidencia de Intereses:</strong> <span id="resMatchIntereses"></span></p>
            <p><strong>Intereses Seleccionados:</strong> <span id="resInteresesSeleccionados"></span></p>
            <hr>
            <p><strong>Impresiones Estimadas:</strong> <span id="resImpresiones"></span></p>
            <p><strong>Clics Estimados:</strong> <span id="resClics"></span></p>
            <p><strong>CTR Calculado:</strong> <span id="resCTR"></span>%</p>
            <p><strong>Interacciones Estimadas:</strong> <span id="resInteracciones"></span></p>
            <p><strong>Conversiones Estimadas:</strong> <span id="resConversiones"></span></p>
            <p><strong>CPM Calculado (COP):</strong> <span id="resCPM"></span></p>
            <p><strong>CPC Calculado (COP):</strong> <span id="resCPC"></span></p>
            <p><strong>Presupuesto Gastado (COP):</strong> <span id="resPresupuestoGastado"></span></p>

            <div id="detailedFeedbackSection" style="display:none; margin-top: 15px;">
                <hr>
                <h4>Sugerencias y Comentarios Detallados:</h4>
                <ul id="feedbackList" class="feedback-list">
                    <!-- Feedback messages will be populated here by JavaScript -->
                </ul>
            </div>
            <hr>
            <p><em><span id="resMensaje"></span></em></p>
    `;

    function cargarSelect(selectElement, data, defaultOptionText, isMultiple = false) {
        if (!isMultiple) {
            selectElement.innerHTML = `<option value="">${defaultOptionText}</option>`; // Limpiar y poner placeholder
        } else {
            selectElement.innerHTML = `<option value="" disabled>${defaultOptionText}</option>`; // Para selectores múltiples, el placeholder puede ser solo informativo
        }
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            // Para intereses, podríamos querer mostrar la categoría también, o un nombre más descriptivo.
            // Por ahora, solo el nombre.
            option.textContent = item.nombre + (item.categoria_interes ? ` (${item.categoria_interes})` : "");
            selectElement.appendChild(option);
        });
    }

    async function cargarIntereses() {
        try {
            const response = await fetch('http://localhost:5001/api/interests-data');
            if (!response.ok) {
                throw new Error(`Error al cargar intereses: ${response.status}`);
            }
            const intereses = await response.json();
            // Usar la función cargarSelect, adaptada o una nueva si es necesario para 'multiple'
            // Aquí reutilizamos cargarSelect, el placeholder "Cargando intereses..." se reemplazará.
            // El tercer argumento es el texto para la opción deshabilitada si el select está vacío al inicio.
            cargarSelect(interesesSelect, intereses, "Cargando intereses...", true);
            // Habilitar el select si antes estaba deshabilitado por no tener opciones.
            interesesSelect.querySelector('option[disabled]').textContent = 'Selecciona uno o más intereses (opcional)';
        } catch (error) {
            console.error('Error al cargar intereses:', error);
            interesesSelect.innerHTML = '<option value="">Error al cargar intereses</option>';
            // Opcional: alertar al usuario
            // alert("No se pudieron cargar los intereses desde el servidor.\n" + error.message);
        }
    }


    campaignForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const marcaId = marcaSelect.value;
        const audienciaId = audienciaSelect.value;
        const campaignGoalId = campaignGoalSelect.value; // Obtener el objetivo seleccionado
        const presupuesto = document.getElementById('presupuesto').value;

        const selectedInteresIds = Array.from(interesesSelect.options)
            .filter(option => option.selected && option.value !== "")
            .map(option => option.value);

        if (!marcaId || !audienciaId || !campaignGoalId) { // Asegurarse que el objetivo también esté seleccionado
            alert("Por favor, selecciona una marca, una audiencia y un objetivo de campaña.");
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
                    presupuesto: presupuesto,
                    selectedInteresIds: selectedInteresIds,
                    campaignGoalId: campaignGoalId // Enviar el objetivo de campaña
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

    async function cargarDatosIniciales() {
        try {
            const response = await fetch('http://localhost:5001/api/market-data');
            if (!response.ok) {
                throw new Error(`Error al cargar datos de mercado: ${response.status}`);
            }
            const data = await response.json();
            cargarSelect(marcaSelect, data.marcas, "Selecciona una marca");
            cargarSelect(audienciaSelect, data.audiencias, "Selecciona una audiencia");
            if (data.campaign_goals) { // Cargar objetivos de campaña
                cargarSelect(campaignGoalSelect, data.campaign_goals, "Selecciona un objetivo");
            } else {
                campaignGoalSelect.innerHTML = '<option value="">Error al cargar objetivos</option>';
            }
        } catch (error) {
            console.error('Error al cargar datos iniciales:', error);
            marcaSelect.innerHTML = '<option value="">Error al cargar marcas</option>';
            audienciaSelect.innerHTML = '<option value="">Error al cargar audiencias</option>';
            campaignGoalSelect.innerHTML = '<option value="">Error al cargar objetivos</option>';
            alert("No se pudieron cargar todos los datos iniciales desde el servidor. Verifica que el backend esté funcionando.\n" + error.message);
        }
    }

    function displayResults(data) {
        resultsContainer.innerHTML = originalResultsHTML;

        if (data.error) {
            resultsContainer.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
        } else {
            document.getElementById('resMarca').textContent = data.marca_nombre || 'N/A';
            document.getElementById('resAudiencia').textContent = data.audiencia_nombre || 'N/A';
            document.getElementById('resCampaignGoal').textContent = data.campaign_goal_nombre || 'N/A';
            document.getElementById('resPresupuestoInicial').textContent = data.presupuesto_inicial?.toLocaleString('es-CO', { style: 'currency', currency: 'COP' }) || 'N/A';
            document.getElementById('resPuntuacion').textContent = data.puntuacion !== undefined ? data.puntuacion : 'N/A';

            document.getElementById('resAfinidad').textContent = data.afinidad_marca_audiencia !== undefined ? (data.afinidad_marca_audiencia * 100).toFixed(0) + '%' : 'N/A';
            document.getElementById('resMatchIntereses').textContent = data.interest_match_score !== undefined ? (data.interest_match_score * 100).toFixed(0) + '%' : 'N/A';
            document.getElementById('resInteresesSeleccionados').textContent = data.selected_intereses_nombres && data.selected_intereses_nombres.length > 0 ? data.selected_intereses_nombres.join(', ') : 'Ninguno';

            document.getElementById('resImpresiones').textContent = data.impresiones?.toLocaleString('es-CO') || 'N/A';
            document.getElementById('resClics').textContent = data.clics?.toLocaleString('es-CO') || 'N/A';
            // Mostrar CTR calculado, interacciones y conversiones
            document.getElementById('resCTR').textContent = data.ctr_calculado !== undefined ? (data.ctr_calculado * 100).toFixed(3) : 'N/A';
            document.getElementById('resInteracciones').textContent = data.interacciones_calculadas?.toLocaleString('es-CO') || 'N/A';
            document.getElementById('resConversiones').textContent = data.conversiones_calculadas?.toLocaleString('es-CO') || 'N/A';

            document.getElementById('resCPM').textContent = data.cpm_calculado?.toLocaleString('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }) || 'N/A';
            document.getElementById('resCPC').textContent = data.cpc_calculado?.toLocaleString('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }) || 'N/A';
            document.getElementById('resPresupuestoGastado').textContent = data.presupuesto_gastado?.toLocaleString('es-CO', { style: 'currency', currency: 'COP' }) || 'N/A';
            document.getElementById('resMensaje').textContent = data.mensaje || '';

            // Populate Feedback List
            const feedbackListUl = document.getElementById('feedbackList');
            const feedbackSectionDiv = document.getElementById('detailedFeedbackSection');

            if (feedbackListUl && feedbackSectionDiv) { // Ensure elements exist
                feedbackListUl.innerHTML = ''; // Clear previous feedback
                if (data.mensajes_feedback && data.mensajes_feedback.length > 0) {
                    data.mensajes_feedback.forEach(message => {
                        const listItem = document.createElement('li');
                        listItem.textContent = message;
                        feedbackListUl.appendChild(listItem);
                    });
                    feedbackSectionDiv.style.display = 'block'; // Show the section
                } else {
                    feedbackSectionDiv.style.display = 'none'; // Hide if no feedback
                }
            }
        }
        resultsContainer.style.display = 'block';
    }

    cargarDatosIniciales();
    cargarIntereses(); // Cargar los intereses al iniciar
});
