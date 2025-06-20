// programmatic_simulator/frontend/js/app.js

document.addEventListener('DOMContentLoaded', () => {
    const campaignForm = document.getElementById('campaignForm');
    const marcaSelect = document.getElementById('marca');
    const audienciaSelect = document.getElementById('audiencia');
    // const interesesSelect = document.getElementById('intereses'); // Replaced by interesesCheckboxContainer
    const interesesCheckboxContainer = document.getElementById('interesesCheckboxContainer'); // New reference for checkboxes
    const campaignGoalSelect = document.getElementById('campaignGoal'); // Nueva referencia
    const productSelectionContainer = document.getElementById('productSelectionContainer'); // New reference
    const productosSelect = document.getElementById('productos'); // New reference
    const presupuestoInput = document.getElementById('presupuesto'); // Referencia para el input de presupuesto
    const resultsContainer = document.getElementById('resultsContainer');
    const estimatedAudienceDisplay = document.getElementById('estimatedAudienceDisplay'); // Nueva referencia
    const audienceDescriptionDisplay = document.getElementById('audienceDescriptionDisplay'); // Referencia para descripción
    const audienceSizeChangeIndicator = document.getElementById('audienceSizeChangeIndicator'); // For displaying size changes
    const totalAffinityDisplay = document.getElementById('totalAffinityDisplay'); // For displaying total affinity
    const presupuestoValueDisplay = document.getElementById('presupuestoValueDisplay'); // For budget slider value
    const fechaInicioInput = document.getElementById('fechaInicio');
    const fechaFinInput = document.getElementById('fechaFin');
    const campaignDurationDisplay = document.getElementById('campaignDurationDisplay');
    const totalCampaignBudgetDisplay = document.getElementById('totalCampaignBudgetDisplay');
    const resetFormBtn = document.getElementById('resetFormBtn');
    const stepConfig = document.getElementById('stepConfig');
    const stepResults = document.getElementById('stepResults');
    const backToConfigBtn = document.getElementById('backToConfigBtn');


    let allAudiencesData = []; // Variable para almacenar datos de audiencias
    let allBrandsData = []; // Variable para almacenar datos de marcas con sus productos
    let previousAudienceSize = null; // Variable to store the previous audience size

    function showConfigStep() {
        if (stepConfig) stepConfig.classList.add('active');
        if (stepResults) stepResults.classList.remove('active');
    }

    function showResultsStep() {
        if (stepConfig) stepConfig.classList.remove('active');
        if (stepResults) stepResults.classList.add('active');
    }

    // Ensure initial state
    showConfigStep();

    // Actualizado para coincidir con los nuevos campos en index.html
    const originalResultsHTML = `
            <h2>Resultados de la Simulación</h2>
            <div class="summary">
                <p><strong>Marca:</strong> <span id="resMarca"></span></p>
                <p><strong>Audiencia:</strong> <span id="resAudiencia"></span></p>
                <p><strong>Objetivo de Campaña:</strong> <span id="resCampaignGoal"></span></p>
            </div>
            <div class="metrics-dashboard">
                <div class="metric-card" id="scoreCard">
                    <div class="metric-title">Puntuación</div>
                    <div class="metric-circle"><span id="resPuntuacion"></span></div>
                </div>
                <div class="metric-card" id="affinityCard">
                    <div class="metric-title">Afinidad</div>
                    <div class="metric-circle"><span id="resAfinidad"></span></div>
                </div>
                <div class="metric-card" id="impressionsCard">
                    <div class="metric-title">Impresiones</div>
                    <div class="metric-bar"><div class="metric-bar-fill" id="impressionsFill"></div></div>
                    <div class="metric-number" id="resImpresiones"></div>
                </div>
                <div class="metric-card" id="ctrCard">
                    <div class="metric-title">CTR</div>
                    <div class="metric-bar"><div class="metric-bar-fill" id="ctrFill"></div></div>
                    <div class="metric-number"><span id="resCTR"></span>%</div>
                </div>
                <div class="metric-card" id="budgetCard">
                    <div class="metric-title">Presupuesto Gastado</div>
                    <div class="metric-bar"><div class="metric-bar-fill" id="budgetFill"></div></div>
                    <div class="metric-number" id="resPresupuestoGastado"></div>
                </div>
            </div>
            <div id="detailedFeedbackSection" style="display:none; margin-top: 15px;">
                <h4>Sugerencias y Comentarios Detallados:</h4>
                <ul id="feedbackList" class="feedback-list">
                    <!-- Feedback messages will be populated here by JavaScript -->
                </ul>
            </div>
            <p><em><span id="resMensaje"></span></em></p>
    `;

    function cargarSelect(selectElement, data, defaultOptionText, isMultiple = false) {
        if (!isMultiple) {
            selectElement.innerHTML = `<option value="">${defaultOptionText}</option>`; // Limpiar y poner placeholder
        } else {
            // This 'else' block might not be strictly necessary if no multi-selects are left after this change
            selectElement.innerHTML = `<option value="" disabled>${defaultOptionText}</option>`;
        }
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            option.textContent = item.nombre + (item.categoria_interes ? ` (${item.categoria_interes})` : "");
            selectElement.appendChild(option);
        });
    }

    async function cargarIntereses() {
        interesesCheckboxContainer.innerHTML = '<p>Cargando intereses...</p>'; // Show loading message
        try {
            const response = await fetch('/api/interests-data');
            if (!response.ok) {
                throw new Error(`Error al cargar intereses: ${response.status}`);
            }
            const intereses = await response.json();
            interesesCheckboxContainer.innerHTML = ''; // Clear loading message

            if (!intereses || intereses.length === 0) {
                interesesCheckboxContainer.innerHTML = '<p>No hay intereses disponibles.</p>';
                return;
            }

            intereses.forEach(interes => {
                const itemDiv = document.createElement('div');
                itemDiv.classList.add('checkbox-item');

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = `interes-${interes.id}`;
                checkbox.value = interes.id;
                checkbox.name = 'interes_selection';
                // Add event listener to each checkbox for updating audience estimate and total affinity
                checkbox.addEventListener('change', () => {
                    updateEstimatedAudienceSize();
                    updateTotalAffinity();
                });

                const label = document.createElement('label');
                label.htmlFor = `interes-${interes.id}`;
                label.textContent = interes.nombre + (interes.categoria_interes ? ` (${interes.categoria_interes})` : "");

                itemDiv.appendChild(checkbox);
                itemDiv.appendChild(label);
                interesesCheckboxContainer.appendChild(itemDiv);
            });
        } catch (error) {
            console.error('Error al cargar intereses:', error);
            interesesCheckboxContainer.innerHTML = '<p>Error al cargar intereses. Intenta recargar.</p>';
        }
    }


    campaignForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const marcaId = marcaSelect.value;
        const audienciaId = audienciaSelect.value;
        const campaignGoalId = campaignGoalSelect.value;
        const dailyInvestment = parseInt(presupuestoInput.value, 10);
        const startDate = fechaInicioInput.value;
        const endDate = fechaFinInput.value;

        if (!marcaId || !audienciaId || !campaignGoalId || !startDate || !endDate) {
            alert("Por favor, completa todos los campos requeridos, incluyendo marca, audiencia, objetivo y fechas de campaña.");
            return;
        }

        const date1 = new Date(startDate);
        const date2 = new Date(endDate);

        if (date2 < date1) {
            alert("La fecha de fin no puede ser anterior a la fecha de inicio.");
            return;
        }

        const diffTime = Math.abs(date2 - date1);
        const campaignDurationDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
        const totalBudget = dailyInvestment * campaignDurationDays;

        // Store these for displayResults
        const dailyInvestmentFromForm = dailyInvestment;
        const durationFromForm = campaignDurationDays;


        const selectedInteresCheckboxes = document.querySelectorAll('#interesesCheckboxContainer input[type="checkbox"]:checked');
        const selectedInteresIds = Array.from(selectedInteresCheckboxes).map(cb => cb.value);

        const selectedProductIds = Array.from(productosSelect.options)
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
            const response = await fetch('/api/simular', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    marcaId: marcaId,
                    audienciaId: audienciaId,
                    presupuesto: totalBudget, // Send total budget
                    selectedInteresIds: selectedInteresIds,
                    campaignGoalId: campaignGoalId,
                    selected_product_ids: selectedProductIds,
                    campaignDurationDays: campaignDurationDays // Send duration
                }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: "Error desconocido del servidor" }));
                throw new Error(errorData.error || `Error del servidor: ${response.status}`);
            }

            const data = await response.json();
            displayResults(data, dailyInvestmentFromForm, durationFromForm);
            showResultsStep();

        } catch (error) {
            console.error('Error al simular campaña:', error);
            // Pass null or undefined for extra params if error occurs before they are set
            displayResults({ error: error.message || "No se pudo conectar con el servidor de simulación." }, dailyInvestmentFromForm, durationFromForm);
            showResultsStep();
        }
    });

    async function cargarDatosIniciales() {
        try {
            const response = await fetch('/api/market-data');
            if (!response.ok) {
                throw new Error(`Error al cargar datos de mercado: ${response.status}`);
            }
            const data = await response.json();

            allBrandsData = data.marcas || []; // Guardar todas las marcas con sus productos
            allAudiencesData = data.audiencias || []; // Guardar datos de audiencias (ya estaba)

            cargarSelect(marcaSelect, allBrandsData, "Selecciona una marca");
            cargarSelect(audienciaSelect, allAudiencesData, "Selecciona una audiencia");
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

    function displayResults(data, dailyInvestment, campaignDuration) { // Added dailyInvestment, campaignDuration
        resultsContainer.innerHTML = originalResultsHTML;

        if (data.error) {
            resultsContainer.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
        } else {
            document.getElementById('resMarca').textContent = data.marca_nombre || 'N/A';
            document.getElementById('resAudiencia').textContent = data.audiencia_nombre || 'N/A';

            document.getElementById('resCampaignGoal').textContent = data.campaign_goal_nombre || 'N/A';

            document.getElementById('resPuntuacion').textContent = data.puntuacion !== undefined ? data.puntuacion : 'N/A';
            document.getElementById('resAfinidad').textContent = data.afinidad_marca_audiencia !== undefined ? (data.afinidad_marca_audiencia * 100).toFixed(0) + '%' : 'N/A';
            document.getElementById('resImpresiones').textContent = data.impresiones?.toLocaleString('es-CO') || 'N/A';
            document.getElementById('resCTR').textContent = data.ctr_calculado !== undefined ? (data.ctr_calculado * 100).toFixed(3) : 'N/A';
            document.getElementById('resPresupuestoGastado').textContent = data.presupuesto_gastado?.toLocaleString('es-CO', { style: 'currency', currency: 'COP' }) || 'N/A';
            document.getElementById('resMensaje').textContent = data.mensaje || '';

            const scoreCard = document.getElementById('scoreCard');
            const affinityCard = document.getElementById('affinityCard');
            const impressionsCard = document.getElementById('impressionsCard');
            const ctrCard = document.getElementById('ctrCard');
            const budgetCard = document.getElementById('budgetCard');

            const impressionsFill = document.getElementById('impressionsFill');
            const ctrFill = document.getElementById('ctrFill');
            const budgetFill = document.getElementById('budgetFill');

            function getPerfClass(val, good, regular) {
                if (val === undefined || val === null || isNaN(val)) return '';
                if (val >= good) return 'metric-good';
                if (val >= regular) return 'metric-regular';
                return 'metric-bad';
            }

            const score = data.puntuacion;
            if (scoreCard) {
                scoreCard.classList.remove('metric-good','metric-regular','metric-bad');
                scoreCard.classList.add(getPerfClass(score, 8, 5));
            }

            const affinity = data.afinidad_marca_audiencia;
            if (affinityCard) {
                affinityCard.classList.remove('metric-good','metric-regular','metric-bad');
                affinityCard.classList.add(getPerfClass(affinity, 0.7, 0.4));
            }

            const impressionsRatio = data.refined_potential_audience_size ? data.impresiones / data.refined_potential_audience_size : 0;
            if (impressionsFill) impressionsFill.style.width = Math.min(100, Math.max(0, impressionsRatio * 100)) + '%';
            if (impressionsCard) {
                impressionsCard.classList.remove('metric-good','metric-regular','metric-bad');
                impressionsCard.classList.add(getPerfClass(impressionsRatio, 0.7, 0.4));
            }

            const ctr = data.ctr_calculado;
            if (ctrFill) ctrFill.style.width = Math.min(100, Math.max(0, ctr * 4000)) + '%';
            if (ctrCard) {
                ctrCard.classList.remove('metric-good','metric-regular','metric-bad');
                ctrCard.classList.add(getPerfClass(ctr, 0.02, 0.01));
            }

            const budgetRatio = data.presupuesto_inicial ? data.presupuesto_gastado / data.presupuesto_inicial : 0;
            if (budgetFill) budgetFill.style.width = Math.min(100, Math.max(0, budgetRatio * 100)) + '%';
            if (budgetCard) {
                budgetCard.classList.remove('metric-good','metric-regular','metric-bad');
                budgetCard.classList.add(getPerfClass(budgetRatio, 0.8, 0.5));
            }

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

    // Función para actualizar el tamaño estimado de la audiencia
    async function updateEstimatedAudienceSize() {
        // Store previous size
        const currentDisplayValue = estimatedAudienceDisplay.textContent;
        let currentNumericSize = null;
        if (currentDisplayValue && currentDisplayValue !== "N/A" && currentDisplayValue !== "Estimating..." && currentDisplayValue !== "Could not estimate" && currentDisplayValue !== "Select an audience" && !currentDisplayValue.includes("Error") && !currentDisplayValue.includes("Audience not found")) {
            const parts = currentDisplayValue.split(' ');
            const numericString = parts[0].replace(/[,.]/g, ''); // Remove commas and dots (for thousands)
            if (!isNaN(numericString) && numericString.trim() !== '') {
                currentNumericSize = parseInt(numericString, 10);
            }
        }
        previousAudienceSize = currentNumericSize;

        const audienciaId = audienciaSelect.value;
        const selectedInteresCheckboxes = document.querySelectorAll('#interesesCheckboxContainer input[type="checkbox"]:checked');
        const selectedInteresIds = Array.from(selectedInteresCheckboxes).map(cb => cb.value);

        // Clear indicator initially and remove classes
        audienceSizeChangeIndicator.textContent = '';
        audienceSizeChangeIndicator.className = '';

        if (!audienciaId) {
            estimatedAudienceDisplay.textContent = "Select an audience";
            previousAudienceSize = null; // Reset if no audience is selected
            return;
        }

        let url = `/api/estimate-audience-size?audienciaId=${encodeURIComponent(audienciaId)}`;
        if (selectedInteresIds.length > 0) {
            selectedInteresIds.forEach(id => {
                url += `&selectedInteresIds=${encodeURIComponent(id)}`;
            });
        }

        try {
            estimatedAudienceDisplay.textContent = "Estimating...";
            const response = await fetch(url);
            if (!response.ok) {
                if (response.status === 404) {
                    const errorData = await response.json().catch(() => null);
                    estimatedAudienceDisplay.textContent = errorData?.error || "Audience not found";
                } else {
                    estimatedAudienceDisplay.textContent = "Error fetching size"; // Generic error
                    throw new Error(`Error fetching audience size: ${response.status}`);
                }
                audienceSizeChangeIndicator.textContent = ''; // Clear on error
                previousAudienceSize = null; // Reset on error
                return;
            }
            const data = await response.json();

            if (data.refined_potential_audience_size !== undefined) {
                const newAudienceSize = data.refined_potential_audience_size;
                let displayText = newAudienceSize.toLocaleString('es-CO');
                if (selectedInteresIds.length > 0 && data.potential_audience_size_from_segment && data.potential_audience_size_from_segment !== newAudienceSize) {
                    displayText += ` (refined from ${data.potential_audience_size_from_segment.toLocaleString('es-CO')})`;
                }
                estimatedAudienceDisplay.textContent = displayText;

                if (previousAudienceSize !== null) {
                    if (newAudienceSize > previousAudienceSize) {
                        audienceSizeChangeIndicator.textContent = ' (Increased ↑)';
                        audienceSizeChangeIndicator.className = 'size-increased';
                    } else if (newAudienceSize < previousAudienceSize) {
                        audienceSizeChangeIndicator.textContent = ' (Decreased ↓)';
                        audienceSizeChangeIndicator.className = 'size-decreased';
                    } else {
                        audienceSizeChangeIndicator.textContent = ' (No change)';
                        audienceSizeChangeIndicator.className = 'size-no-change';
                    }
                } else {
                     audienceSizeChangeIndicator.textContent = ''; // No previous size, so no change text
                }

            } else if (data.error) {
                estimatedAudienceDisplay.textContent = data.error;
                audienceSizeChangeIndicator.textContent = '';
                previousAudienceSize = null;
            } else {
                estimatedAudienceDisplay.textContent = "N/A";
                audienceSizeChangeIndicator.textContent = '';
                previousAudienceSize = null;
            }
        } catch (error) {
            console.error('Error updating estimated audience size:', error);
            estimatedAudienceDisplay.textContent = "Could not estimate";
            audienceSizeChangeIndicator.textContent = '';
            previousAudienceSize = null;
        }
    }

    // Función para actualizar la descripción de la audiencia
    function updateAudienceDescription() {
        const selectedAudienceId = audienciaSelect.value;
        if (selectedAudienceId && allAudiencesData.length > 0) {
            const selectedAudience = allAudiencesData.find(aud => aud.id === selectedAudienceId);
            if (selectedAudience && selectedAudience.descripcion) {
                audienceDescriptionDisplay.textContent = selectedAudience.descripcion;
            } else if (selectedAudience) { // Audience found but no description
                audienceDescriptionDisplay.textContent = "Descripción no disponible para esta audiencia.";
            } else { // Audience ID selected but not found in data (should not happen if data is consistent)
                audienceDescriptionDisplay.textContent = "Detalles de audiencia no encontrados.";
            }
        } else {
            audienceDescriptionDisplay.textContent = "Select an audience to see its description.";
        }
    }

    // Event listeners para actualizar la estimación de audiencia Y la descripción
    audienciaSelect.addEventListener('change', () => {
        updateEstimatedAudienceSize();
        updateAudienceDescription();
        // updateFormAccess(); // This is already called by the main select listeners
        // updateTotalAffinity(); // This will be called by updateFormAccess if appropriate
    });
    // interesesSelect.addEventListener('change', updateEstimatedAudienceSize); // Removed, individual checkboxes have listeners now


    // --- Function to update Total Affinity display ---
    async function updateTotalAffinity() {
        if (!totalAffinityDisplay) return; // Guard clause if element not found

        const marcaId = marcaSelect.value;
        const audienciaId = audienciaSelect.value;

        if (!marcaId || !audienciaId) {
            totalAffinityDisplay.textContent = 'N/A';
            return;
        }

        const selectedProductOptions = Array.from(productosSelect.options).filter(option => option.selected && option.value !== "");
        const selectedProductIds = selectedProductOptions.map(option => option.value);

        const selectedInteresCheckboxes = document.querySelectorAll('#interesesCheckboxContainer input[type="checkbox"]:checked');
        const selectedInteresIds = Array.from(selectedInteresCheckboxes).map(cb => cb.value);

        totalAffinityDisplay.textContent = 'Calculating...';

        try {
            const response = await fetch('/api/calculate-affinity', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    marcaId: marcaId,
                    audienciaId: audienciaId,
                    selectedProductIds: selectedProductIds,
                    selectedInteresIds: selectedInteresIds
                })
            });

            if (response.ok) {
                const affinityData = await response.json();
                if (affinityData.error) {
                    totalAffinityDisplay.textContent = 'Error: ' + affinityData.error;
                    console.error('Affinity calculation error:', affinityData.error);
                } else if (affinityData.overall_affinity !== undefined) {
                    const formattedAffinity = (affinityData.overall_affinity * 100).toFixed(1) + '%';
                    totalAffinityDisplay.textContent = formattedAffinity;
                } else {
                    totalAffinityDisplay.textContent = 'Invalid data';
                    console.error('Invalid affinity data received:', affinityData);
                }
            } else {
                const errorText = await response.text();
                totalAffinityDisplay.textContent = 'Error calculating affinity';
                console.error('Error fetching affinity:', response.status, errorText);
            }
        } catch (error) {
            totalAffinityDisplay.textContent = 'API error';
            console.error('Failed to fetch total affinity:', error);
        }
    }


    // Helper function to disable/enable interest checkboxes
    function disableInteresCheckboxes(disabled) {
        const checkboxes = interesesCheckboxContainer.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(cb => cb.disabled = disabled);
    }

    // Helper function to clear interest checkbox selections
    function clearInteresCheckboxes() {
        const checkboxes = interesesCheckboxContainer.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(cb => cb.checked = false);
        // Optionally, call updateEstimatedAudienceSize if clearing interests should affect the estimate display immediately
        // updateEstimatedAudienceSize();
    }

    // Core function to update form access based on selections
    function updateFormAccess() {
        const marcaSelected = marcaSelect.value !== "";
        const audienciaSelected = audienciaSelect.value !== "";
        const campaignGoalSelected = campaignGoalSelect.value !== "";

        // --- Default states: Disable all dependent fields first ---
        // Products:
        productosSelect.disabled = true;
        // productSelectionContainer visibility is handled in marcaSelect's listener.

        // Audience:
        audienciaSelect.disabled = true;

        // Campaign Goal:
        campaignGoalSelect.disabled = true;

        // Interests:
        interesesCheckboxContainer.classList.add('disabled-selection-area');
        disableInteresCheckboxes(true);

        // Budget & Dates:
        presupuestoInput.disabled = true;
        fechaInicioInput.disabled = true;
        fechaFinInput.disabled = true;


        // --- Enable fields based on progression ---
        if (marcaSelected) {
            productosSelect.disabled = false; // Enable product selection
            audienciaSelect.disabled = false; // Enable Audience select
        }

        if (marcaSelected && audienciaSelected) {
            campaignGoalSelect.disabled = false; // Enable Campaign Goal
        }

        if (marcaSelected && audienciaSelected && campaignGoalSelected) {
            interesesCheckboxContainer.classList.remove('disabled-selection-area');
            disableInteresCheckboxes(false); // Enable Interest checkboxes
            presupuestoInput.disabled = false; // Enable Daily Budget input
            fechaInicioInput.disabled = false; // Enable Start Date input
            fechaFinInput.disabled = false;    // Enable End Date input
        }

        // --- Reset logic for fields if a preceding selection is cleared ---
        if (!marcaSelected) {
            productosSelect.innerHTML = '<option value="" disabled>Selecciona una marca primero...</option>';
            if(productSelectionContainer) productSelectionContainer.style.display = 'none';
            audienciaSelect.value = "";
            audienceDescriptionDisplay.textContent = "Select an audience to see its description.";
            estimatedAudienceDisplay.textContent = "N/A";
            if(audienceSizeChangeIndicator) audienceSizeChangeIndicator.textContent = '';
            if(totalAffinityDisplay) totalAffinityDisplay.textContent = 'N/A';
            previousAudienceSize = null;
            campaignGoalSelect.value = "";
            clearInteresCheckboxes();
            // Reset dates and summary
            fechaInicioInput.value = "";
            fechaFinInput.value = "";
            updateCampaignSummary(); // This will set summary to N/A
        } else if (!audienciaSelected) { // marcaSelected is true
            campaignGoalSelect.value = "";
            clearInteresCheckboxes();
            if(totalAffinityDisplay) totalAffinityDisplay.textContent = 'N/A';
            fechaInicioInput.value = "";
            fechaFinInput.value = "";
            updateCampaignSummary();
        } else if (!campaignGoalSelected) { // marcaSelected and audienciaSelected are true
            clearInteresCheckboxes();
            // Disable budget and dates if goal is cleared
            presupuestoInput.disabled = true;
            fechaInicioInput.disabled = true;
            fechaFinInput.disabled = true;
            // fechaInicioInput.value = ""; // Optionally clear dates
            // fechaFinInput.value = "";
            updateCampaignSummary(); // Update summary, possibly to N/A if dates are cleared or dependent on budget
        }

        // Call updateTotalAffinity whenever form access might change and inputs are valid
        if(marcaSelected && audienciaSelected){
            updateTotalAffinity();
        } else {
            if(totalAffinityDisplay) totalAffinityDisplay.textContent = 'N/A';
        }
        // updateCampaignSummary(); // Call at the end to ensure summary reflects current state
        // This is called by date/budget listeners, and also needs to be called if disabling fields resets them
    }

    function updateCampaignSummary() {
        if (!campaignDurationDisplay || !totalCampaignBudgetDisplay || !presupuestoInput || !fechaInicioInput || !fechaFinInput) return;

        const dailyInvestment = parseInt(presupuestoInput.value, 10);
        const startDate = fechaInicioInput.value;
        const endDate = fechaFinInput.value;

        if (!startDate || !endDate || isNaN(dailyInvestment) || dailyInvestment <= 0) {
            campaignDurationDisplay.textContent = 'N/A';
            totalCampaignBudgetDisplay.textContent = 'N/A';
            return;
        }

        const date1 = new Date(startDate);
        const date2 = new Date(endDate);

        if (date2 < date1) {
            campaignDurationDisplay.textContent = 'Fechas inválidas';
            totalCampaignBudgetDisplay.textContent = 'N/A'; // Or 'Fechas inválidas'
            return;
        }

        const diffTime = Math.abs(date2 - date1);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1; // Add 1 to include both start and end day

        const totalBudget = dailyInvestment * diffDays;

        campaignDurationDisplay.textContent = diffDays;
        totalCampaignBudgetDisplay.textContent = totalBudget.toLocaleString('es-CO');
    }


    marcaSelect.addEventListener('change', () => {
        const selectedBrandId = marcaSelect.value;
        productosSelect.innerHTML = ''; // Clear previous product options

        if (selectedBrandId && allBrandsData.length > 0) {
            const brand = allBrandsData.find(b => b.id === selectedBrandId);
            // Populate products if available
            if (brand && brand.productos && brand.productos.length > 0) {
                productSelectionContainer.style.display = 'block';
                const placeholderOption = document.createElement('option');
                placeholderOption.value = "";
                placeholderOption.textContent = "Selecciona uno o más productos (opcional)";
                // placeholderOption.disabled = true; // Not strictly needed if it's just a label
                productosSelect.appendChild(placeholderOption);

                brand.productos.forEach(producto => {
                    const option = document.createElement('option');
                    option.value = producto.id;
                    option.textContent = producto.nombre;
                    productosSelect.appendChild(option);
                });
            } else {
                // No products for this brand
                productSelectionContainer.style.display = 'block'; // Show container
                const noProductsOption = document.createElement('option');
                noProductsOption.value = "";
                noProductsOption.textContent = "No hay productos para esta marca";
                noProductsOption.disabled = true;
                productosSelect.appendChild(noProductsOption);
            }
        } else {
            // No brand selected
            const defaultOption = document.createElement('option');
            defaultOption.value = "";
            defaultOption.textContent = "Selecciona una marca primero...";
            defaultOption.disabled = true;
            productosSelect.appendChild(defaultOption);
            productSelectionContainer.style.display = 'none';
        }
        updateFormAccess(); // Update access rules after brand change
        // updateTotalAffinity(); // updateFormAccess will call it if conditions are met
    });

    productosSelect.addEventListener('change', () => {
        updateFormAccess(); // Call after product selection changes
        // updateTotalAffinity(); // updateFormAccess will call it
    });

    audienciaSelect.addEventListener('change', () => {
        updateEstimatedAudienceSize(); // This now also calls updateTotalAffinity if interests are involved
        updateAudienceDescription();
        updateFormAccess(); // Call after audience selection changes
        // updateTotalAffinity(); // updateFormAccess will call it
    });

    campaignGoalSelect.addEventListener('change', () => {
        updateFormAccess(); // Call after campaign goal selection changes
        // updateTotalAffinity(); // updateFormAccess will call it if needed (e.g. if goal affected affinity logic)
    });


    // cargarDatosIniciales unificada y correcta
    async function cargarDatosIniciales() {
        try {
            const response = await fetch('/api/market-data');
            if (!response.ok) {
                throw new Error(`Error al cargar datos de mercado: ${response.status}`);
            }
            const data = await response.json();

            allBrandsData = data.marcas || []; // Guardar todas las marcas con sus productos
            allAudiencesData = data.audiencias || []; // Guardar datos de audiencias

            cargarSelect(marcaSelect, allBrandsData, "Selecciona una marca");
            // Usar allAudiencesData para poblar el select, ya que contiene la info completa
            cargarSelect(audienciaSelect, allAudiencesData, "Selecciona una audiencia");

            if (data.campaign_goals) {
                cargarSelect(campaignGoalSelect, data.campaign_goals, "Selecciona un objetivo");
            } else {
                campaignGoalSelect.innerHTML = '<option value="">Error al cargar objetivos</option>';
            }
            // Llamadas iniciales después de cargar los datos y selectores
            updateAudienceDescription();
            updateEstimatedAudienceSize();
            // Trigger change on marcaSelect to potentially populate products if a brand is pre-selected (or to set initial state)
            // marcaSelect.dispatchEvent(new Event('change')); // This will be handled by final updateFormAccess call
            updateFormAccess(); // Set initial form accessibility
            // updateTotalAffinity(); // updateFormAccess will call this if marca & audiencia are selected.
        } catch (error) {
            console.error('Error al cargar datos iniciales:', error);
            marcaSelect.innerHTML = '<option value="">Error al cargar marcas</option>';
            audienciaSelect.innerHTML = '<option value="">Error al cargar audiencias</option>';
            campaignGoalSelect.innerHTML = '<option value="">Error al cargar objetivos</option>';
            if(audienceDescriptionDisplay) audienceDescriptionDisplay.textContent = "Error al cargar datos de audiencias.";
            productSelectionContainer.style.display = 'none';
            alert("No se pudieron cargar todos los datos iniciales desde el servidor. Verifica que el backend esté funcionando.\n" + error.message);
        }
    }

    // Iniciar la carga de datos
    cargarDatosIniciales().then(() => {
        cargarIntereses().then(() => {
            updateFormAccess();
            updateCampaignSummary(); // Initial call to set N/A or based on defaults

            if (presupuestoInput && presupuestoValueDisplay) {
                presupuestoValueDisplay.textContent = parseInt(presupuestoInput.value, 10).toLocaleString('es-CO');
            }

            // Set min for start date and add listener for end date min
            const today = new Date().toISOString().split('T')[0];
            if(fechaInicioInput) fechaInicioInput.setAttribute('min', today);
            if(fechaFinInput && fechaInicioInput.value) fechaFinInput.setAttribute('min', fechaInicioInput.value);


        });
    });

    if (presupuestoInput) {
        presupuestoInput.addEventListener('input', () => {
            if(presupuestoValueDisplay) presupuestoValueDisplay.textContent = parseInt(presupuestoInput.value, 10).toLocaleString('es-CO');
            updateCampaignSummary();
        });
    }
    if (fechaInicioInput) {
        fechaInicioInput.addEventListener('change', () => {
            if (fechaInicioInput.value && fechaFinInput) {
                fechaFinInput.setAttribute('min', fechaInicioInput.value);
                if (fechaFinInput.value && fechaFinInput.value < fechaInicioInput.value) {
                    fechaFinInput.value = ""; // Clear end date if it's now before start date
                }
            }
            updateCampaignSummary();
            updateFormAccess(); // Re-check access in case date validation affects other fields (though not currently implemented)
        });
    }
    if (fechaFinInput) {
        fechaFinInput.addEventListener('change', () => {
            updateCampaignSummary();
            updateFormAccess(); // Re-check access
        });
    }

    if (resetFormBtn) {
        resetFormBtn.addEventListener('click', () => {
            campaignForm.reset();
            productosSelect.innerHTML = '<option value="" disabled>Selecciona una marca primero...</option>';
            productSelectionContainer.style.display = 'none';
            clearInteresCheckboxes();
            estimatedAudienceDisplay.textContent = 'N/A';
            audienceSizeChangeIndicator.textContent = '';
            audienceDescriptionDisplay.textContent = 'Select an audience to see its description.';
            totalAffinityDisplay.textContent = 'N/A';
            resultsContainer.style.display = 'none';
            if (presupuestoValueDisplay) {
                presupuestoValueDisplay.textContent = parseInt(presupuestoInput.value, 10).toLocaleString('es-CO');
            }
            updateCampaignSummary();
            updateFormAccess();
            showConfigStep();
        });
    }

    if (backToConfigBtn) {
        backToConfigBtn.addEventListener('click', () => {
            showConfigStep();
        });
    }

});
