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
    const resultsContainer = document.getElementById('resultsContainer');
    const estimatedAudienceDisplay = document.getElementById('estimatedAudienceDisplay'); // Nueva referencia
    const audienceDescriptionDisplay = document.getElementById('audienceDescriptionDisplay'); // Referencia para descripción

    let allAudiencesData = []; // Variable para almacenar datos de audiencias
    let allBrandsData = []; // Variable para almacenar datos de marcas con sus productos

    // Actualizado para coincidir con los nuevos campos en index.html
    const originalResultsHTML = `
            <h2>Resultados de la Simulación</h2>
            <p><strong>Marca:</strong> <span id="resMarca"></span></p>
            <p><strong>Audiencia:</strong> <span id="resAudiencia"></span></p>
            <p><strong>Productos Seleccionados:</strong> <span id="resProductosSeleccionados"></span></p>
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
            const response = await fetch('http://localhost:5001/api/interests-data');
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
                // Add event listener to each checkbox for updating audience estimate
                checkbox.addEventListener('change', updateEstimatedAudienceSize);


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
        const campaignGoalId = campaignGoalSelect.value; // Obtener el objetivo seleccionado
        const presupuesto = document.getElementById('presupuesto').value;

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
                    campaignGoalId: campaignGoalId, // Enviar el objetivo de campaña
                    selected_product_ids: selectedProductIds // Enviar productos seleccionados
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

    function displayResults(data) {
        resultsContainer.innerHTML = originalResultsHTML;

        if (data.error) {
            resultsContainer.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
        } else {
            document.getElementById('resMarca').textContent = data.marca_nombre || 'N/A';
            document.getElementById('resAudiencia').textContent = data.audiencia_nombre || 'N/A';

            // Mostrar productos seleccionados
            const resProductosSeleccionadosSpan = document.getElementById('resProductosSeleccionados');
            const formSelectedProductIds = Array.from(productosSelect.options)
                                           .filter(option => option.selected && option.value !== "")
                                           .map(option => option.value);
            if (formSelectedProductIds.length > 0 && allBrandsData.length > 0) {
                const selectedBrand = allBrandsData.find(brand => brand.id === marcaSelect.value);
                if (selectedBrand && selectedBrand.productos) {
                    const productNames = formSelectedProductIds.map(pId => {
                        const product = selectedBrand.productos.find(prod => prod.id === pId);
                        return product ? product.nombre : pId;
                    });
                    resProductosSeleccionadosSpan.textContent = productNames.join(', ');
                } else {
                    resProductosSeleccionadosSpan.textContent = formSelectedProductIds.join(', '); // Fallback a IDs si no se encuentran nombres
                }
            } else {
                resProductosSeleccionadosSpan.textContent = 'Ninguno';
            }

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

    // Función para actualizar el tamaño estimado de la audiencia
    async function updateEstimatedAudienceSize() {
        const audienciaId = audienciaSelect.value;

        const selectedInteresCheckboxes = document.querySelectorAll('#interesesCheckboxContainer input[type="checkbox"]:checked');
        const selectedInteresIds = Array.from(selectedInteresCheckboxes).map(cb => cb.value);

        if (!audienciaId) {
            estimatedAudienceDisplay.textContent = "Select an audience";
            return;
        }

        let url = `http://localhost:5001/api/estimate-audience-size?audienciaId=${encodeURIComponent(audienciaId)}`;
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
                    throw new Error(`Error fetching audience size: ${response.status}`);
                }
                return;
            }
            const data = await response.json();

            if (data.refined_potential_audience_size !== undefined) {
                let displayText = data.refined_potential_audience_size.toLocaleString('es-CO');
                if (selectedInteresIds.length > 0 && data.potential_audience_size_from_segment && data.potential_audience_size_from_segment !== data.refined_potential_audience_size) {
                    displayText += ` (refined from ${data.potential_audience_size_from_segment.toLocaleString('es-CO')})`;
                }
                estimatedAudienceDisplay.textContent = displayText;
            } else if (data.error) {
                estimatedAudienceDisplay.textContent = data.error;
            }
             else {
                estimatedAudienceDisplay.textContent = "N/A";
            }
        } catch (error) {
            console.error('Error updating estimated audience size:', error);
            estimatedAudienceDisplay.textContent = "Could not estimate";
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
        updateAudienceDescription(); // Añadir llamada para actualizar descripción
    });
    // interesesSelect.addEventListener('change', updateEstimatedAudienceSize); // Removed, individual checkboxes have listeners now

    marcaSelect.addEventListener('change', () => {
        const selectedBrandId = marcaSelect.value;
        productosSelect.innerHTML = ''; // Clear previous product options

        if (selectedBrandId && allBrandsData.length > 0) {
            const brand = allBrandsData.find(b => b.id === selectedBrandId);
            if (brand && brand.productos && brand.productos.length > 0) {
                productSelectionContainer.style.display = 'block'; // Or 'flex' if using flexbox for layout
                const placeholderOption = document.createElement('option');
                placeholderOption.value = "";
                placeholderOption.textContent = "Selecciona uno o más productos";
                placeholderOption.disabled = true; // Keep it disabled as it's a placeholder
                productosSelect.appendChild(placeholderOption);

                brand.productos.forEach(producto => {
                    const option = document.createElement('option');
                    option.value = producto.id;
                    option.textContent = producto.nombre;
                    productosSelect.appendChild(option);
                });
            } else {
                const noProductsOption = document.createElement('option');
                noProductsOption.value = "";
                noProductsOption.textContent = "No hay productos para esta marca";
                noProductsOption.disabled = true;
                productosSelect.appendChild(noProductsOption);
                productSelectionContainer.style.display = 'block'; // Still show, but with "no products"
            }
        } else {
            const defaultOption = document.createElement('option');
            defaultOption.value = "";
            defaultOption.textContent = "Selecciona una marca primero...";
            defaultOption.disabled = true;
            productosSelect.appendChild(defaultOption);
            productSelectionContainer.style.display = 'none';
        }
    });


    // cargarDatosIniciales unificada y correcta
    async function cargarDatosIniciales() {
        try {
            const response = await fetch('http://localhost:5001/api/market-data');
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
            marcaSelect.dispatchEvent(new Event('change'));
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
    cargarDatosIniciales();
    cargarIntereses(); // Cargar los intereses al iniciar (esto ya estaba, se mantiene)
});
