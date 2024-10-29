// script.js

// Variables y funciones relacionadas con la vista de "Scraping"

var data = [];
var filteredData = [];
var pageSize = 20;
var currentPage = 1;
var totalPages = 0;
var lastHash = "";

// Función para cargar la vista de "Scraping"
function loadScrapingView() {
    // Limpiar el contenido principal
    $('#mainContent').empty();

    var scrapingContent = `
        <!-- Indicadores y alertas -->
        <div id="loadingIndicator" class="alert alert-info text-center" style="display:none;">Cargando datos...</div>
        <div id="newDataAlert" class="alert alert-success text-center" style="display:none;">Nuevos datos cargados</div>

        <!-- Contenedor principal -->
        <div class="container mt-5">
            <div class="row">
                <!-- Botón para desplegar los filtros en pantallas pequeñas -->
                <button class="filters-toggle-btn btn btn-secondary d-md-none mb-3" data-toggle="collapse" data-target="#filtersContainer">Mostrar Filtros</button>

                <!-- Columna para los filtros -->
                <div class="col-md-3">
                    <div id="filtersContainer" class="collapse d-md-block">
                        <div class="filter-group">
                            <label for="filterAnunciante">Filtrar por anunciante:</label>
                            <select id="filterAnunciante" class="form-control form-control-custom">
                                <option value="Ver todos">Ver todos</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label for="filterTipo">Filtrar por tipo:</label>
                            <select id="filterTipo" class="form-control form-control-custom">
                                <option value="Ver todos">Ver todos</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label for="filterBarrio">Filtrar por barrio:</label>
                            <select id="filterBarrio" class="form-control form-control-custom">
                                <option value="Ver todos">Ver todos</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label for="filterPhone">Filtrar por teléfono:</label>
                            <input type="text" id="filterPhone" class="form-control form-control-custom" placeholder="Buscar teléfono">
                        </div>
                    </div>
                </div>

                <!-- Columna para las tarjetas -->
                <div class="col-md-9">
                    <div id="cardsContainer" class="row">
                        <!-- Las tarjetas se generarán dinámicamente aquí -->
                    </div>
                    <!-- Controles de paginación -->
                    <div class="d-flex justify-content-between my-3">
                        <button id="prevPageTop" class="btn btn-secondary">Anterior</button>
                        <span id="pageInfoTop" class="align-self-center">Página 1 de X</span>
                        <button id="nextPageTop" class="btn btn-secondary">Siguiente</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    $('#mainContent').html(scrapingContent);

    // Inicializar variables específicas de Scraping
    data = [];
    filteredData = [];
    currentPage = 1;
    totalPages = 0;
    lastHash = "";

    // Configurar eventos y cargar datos
    configureScrapingEvents();
    loadCSV();
}

function configureScrapingEvents() {
    // Eventos para los filtros
    $('#filterAnunciante').on('change', function () {
        applyFilters();
    });

    $('#filterTipo').on('change', function () {
        applyFilters();
    });

    $('#filterBarrio').on('change', function () {
        applyFilters();
    });

    $('#filterPhone').on('input', function () {
        applyFilters();
    });

    // Paginación
    $('#prevPageTop').on('click', function () {
        if (currentPage > 1) {
            currentPage--;
            renderPage(currentPage);
            updatePaginationControls();
            scrollToTop();
        }
    });

    $('#nextPageTop').on('click', function () {
        if (currentPage < totalPages) {
            currentPage++;
            renderPage(currentPage);
            updatePaginationControls();
            scrollToTop();
        }
    });
}

// Mostrar y ocultar indicador de carga
function showLoading() {
    $('#loadingIndicator').show();
}

function hideLoading() {
    $('#loadingIndicator').hide();
}

// Cargar el archivo CSV de Scraping
function loadCSV() {
    showLoading();
    $.ajax({
        url: './data/inmuebles.csv',
        dataType: 'text',
        success: function (csvData) {
            var currentHash = sha256(csvData);
            if (currentHash !== lastHash) {
                lastHash = currentHash;
                Papa.parse(csvData, {
                    header: true,
                    dynamicTyping: true,
                    complete: function (results) {
                        data = results.data;
                        filteredData = data;
                        updateAnuncianteFilter(data);
                        updateTipoFilter(data);
                        updateBarrioFilter(data);
                        applyFilters();
                        $('#newDataAlert').fadeIn().delay(2000).fadeOut();
                        hideLoading();
                    }
                });
            } else {
                hideLoading();
            }
        },
        error: function() {
            hideLoading();
        }
    });
}

// Actualizar los filtros con valores únicos del CSV
function updateAnuncianteFilter(data) {
    var uniqueAnunciantes = _.uniq(data.map(function(row) {
        return row['anunciante'];
    }).filter(Boolean));

    var $filter = $('#filterAnunciante');
    $filter.empty();
    $filter.append('<option value="Ver todos">Ver todos</option>');
    uniqueAnunciantes.forEach(function(anunciante) {
        $filter.append('<option value="' + anunciante + '">' + anunciante + '</option>');
    });
}

function updateTipoFilter(data) {
    var uniqueTipos = _.uniq(data.map(function(row) {
        return row['tipo'];
    }).filter(Boolean));

    var $filter = $('#filterTipo');
    $filter.empty();
    $filter.append('<option value="Ver todos">Ver todos</option>');
    uniqueTipos.forEach(function(tipo) {
        $filter.append('<option value="' + tipo + '">' + tipo + '</option>');
    });
}

function updateBarrioFilter(data) {
    var uniqueBarrios = _.uniq(data.map(function(row) {
        return row['barrio'];
    }).filter(Boolean));

    var $filter = $('#filterBarrio');
    $filter.empty();
    $filter.append('<option value="Ver todos">Ver todos</option>');
    uniqueBarrios.forEach(function(barrio) {
        $filter.append('<option value="' + barrio + '">' + barrio + '</option>');
    });
}

// Aplicar los filtros
function applyFilters() {
    var selectedAnunciante = $('#filterAnunciante').val();
    var selectedTipo = $('#filterTipo').val();
    var selectedBarrio = $('#filterBarrio').val();
    var selectedPhone = $('#filterPhone').val();

    filteredData = data.filter(function (row) {
        var matchesAnunciante = selectedAnunciante === "Ver todos" || row['anunciante'] === selectedAnunciante;
        var matchesTipo = selectedTipo === "Ver todos" || row['tipo'] === selectedTipo;
        var matchesBarrio = selectedBarrio === "Ver todos" || row['barrio'] === selectedBarrio;
        var matchesPhone = row['tlf'] && String(row['tlf']).includes(selectedPhone);
        return matchesAnunciante && matchesTipo && matchesBarrio && matchesPhone;
    });

    currentPage = 1;
    totalPages = Math.ceil(filteredData.length / pageSize);
    renderPage(currentPage);
    updatePaginationControls();
}

// Renderizar la página
function renderPage(page) {
    $('#cardsContainer').empty();
    var start = (page - 1) * pageSize;
    var end = start + pageSize;
    var pageData = _.slice(filteredData, start, end);

    pageData.forEach(function (row) {
        var card = $('<div class="col-12 mb-4"></div>');
        var cardContent = '<div class="card-custom">';
        cardContent += '<h4>' + (row['titulo'] || 'Título desconocido') + '</h4>'; // Título en la parte superior

        cardContent += '<div class="separator"></div>';

        cardContent += '<div class="row-custom">';
        cardContent += '<div class="col-custom"><strong>Precio:</strong> ' + (row['precio'] || 'N/A') + '</div>';
        cardContent += '<div class="col-custom"><strong>Precio/m²:</strong> ' + (row['precio_por_metro'] || 'N/A') + '</div>';
        cardContent += '</div>';

        cardContent += '<div class="row-custom">';
        cardContent += '<div class="col-custom"><strong>Superficie:</strong> ' + (row['superficie'] || 'N/A') + ' m²</div>';
        cardContent += '<div class="col-custom"><strong>Barrio:</strong> ' + (row['barrio'] || 'N/A') + '</div>';
        cardContent += '</div>';

        // Añadir Nombre Anunciante y Teléfono
        cardContent += '<div class="row-custom">';
        cardContent += '<div class="col-custom"><strong>Nombre Anunciante:</strong> ' + (row['nombre_anunciante'] || 'N/A') + '</div>';

        // Enlace telefónico seguro
        var telefono = row['tlf'] ? String(row['tlf']) : '';
        if (telefono && telefono.length > 2) {
            var prefijo = telefono.slice(0, 2);
            var numero = telefono.slice(2);
            cardContent += '<div class="col-custom"><strong>Teléfono:</strong> <a href="tel:+' + prefijo + numero + '">' + numero + '</a></div>';
        } else {
            cardContent += '<div class="col-custom"><strong>Teléfono:</strong> N/A</div>';
        }

        cardContent += '</div>';
        
        // Añadir el botón con la URL
        if (row['url']) {
            cardContent += '<a href="' + row['url'] + '" target="_blank" class="btn btn-primary btn-custom">Ver Inmueble</a>';
        }
        
        // Mostrar las características como etiquetas si existen
        if (row['caracteristicas']) {
            cardContent += '<div class="tags">';
            var caracteristicas = row['caracteristicas'].replace('[', '').replace(']', '').split(',');
            caracteristicas.forEach(function (caracteristica) {
                caracteristica = caracteristica.replace(/'/g, '').trim();
                cardContent += '<span class="badge-custom">' + caracteristica + '</span>';
            });
            cardContent += '</div>';
        }

        // Botón desplegable para realizar cálculo
        cardContent += '<button class="btn btn-secondary btn-sm mt-2" data-toggle="collapse" data-target="#calculo-' + row['id'] + '">Mostrar cálculo</button>';
        cardContent += '<div id="calculo-' + row['id'] + '" class="collapse mt-2">';

        // Seleccionar porcentaje
        cardContent += '<label for="porcentaje-' + row['id'] + '">Seleccione porcentaje (%):</label>';
        cardContent += '<select id="porcentaje-' + row['id'] + '" class="form-control">';
        for (var i = 1; i <= 10; i++) {
            cardContent += '<option value="' + i + '">' + i + '%</option>';
        }
        cardContent += '</select>';

        // Añadir un campo para ingresar el precio y metros
        cardContent += '<input type="text" id="input-precio-' + row['id'] + '" class="form-control mt-2" value="' + (row['precio'] || 0) + '" readonly>';

        // Botón para realizar cálculo
        cardContent += '<button class="btn btn-primary mt-2" onclick="realizarCalculo(' + row['id'] + ', \'' + row['tipo'] + '\')">Calcular Rentabilidad</button>';

        // Contenedor donde se mostrará el resultado del cálculo
        cardContent += '<div id="resultado-calculo-' + row['id'] + '" class="mt-2"></div>';

        cardContent += '</div>';

        // Añadir separador
        cardContent += '<hr class="separator">';

        // Botón para mostrar/ocultar funcionalidades adicionales
        cardContent += '<button class="btn btn-info btn-sm mt-2" data-toggle="collapse" data-target="#funcionalidades-' + row['id'] + '">Mostrar Funcionalidades</button>';

        // Contenedor colapsable para funcionalidades adicionales
        cardContent += '<div id="funcionalidades-' + row['id'] + '" class="collapse mt-2">';

        // Sección de comentarios
        cardContent += '<div class="comment-section">';
        cardContent += '<label for="commentInput-' + row['id'] + '">Comentarios:</label>';
        cardContent += '<textarea id="commentInput-' + row['id'] + '" class="form-control" placeholder="Escribe un comentario..."></textarea>';
        cardContent += '<button class="btn btn-custom mt-2" onclick="guardarComentario(' + row['id'] + ')">Guardar Comentario</button>';
        cardContent += '<ul id="commentList-' + row['id'] + '" class="comment-list mt-3"></ul>';
        cardContent += '</div>';

        // Registro de día y llamadas
        cardContent += '<div class="log-section mt-3">';
        cardContent += '<label for="dateInput-' + row['id'] + '">Fecha:</label>';
        cardContent += '<input type="date" id="dateInput-' + row['id'] + '" class="form-control">';
        cardContent += '<button class="btn btn-secondary mt-2" onclick="registrarLlamada(' + row['id'] + ')">Registrar Llamada</button>';
        cardContent += '<div id="callLog-' + row['id'] + '" class="mt-2"></div>';
        cardContent += '</div>';

        // Botón de "No Disponible"
        cardContent += '<button class="btn btn-danger mt-3" onclick="marcarNoDisponible(' + row['id'] + ')">Marcar como No Disponible</button>';

        cardContent += '</div>'; // Cierre del contenedor colapsable

        cardContent += '</div>'; // Cierre de la tarjeta
        card.append(cardContent);

        $('#cardsContainer').append(card);
    });
}

// Actualizar controles de paginación
function updatePaginationControls() {
    $('#pageInfoTop').text('Página ' + currentPage + ' de ' + totalPages);
    $('#prevPageTop').prop('disabled', currentPage === 1);
    $('#nextPageTop').prop('disabled', currentPage === totalPages);
}

// Función para volver a la parte superior de la página
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Funciones para las funcionalidades adicionales
window.guardarComentario = function(id) {
    alert('Pendiente de implementar');
}

window.registrarLlamada = function(id) {
    alert('Pendiente de implementar');
}

window.marcarNoDisponible = function(id) {
    alert('Pendiente de implementar');
}

window.realizarCalculo = function(id, tipo) {
    alert('Pendiente de implementar');
}
