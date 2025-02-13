// script.js

// Variables y funciones relacionadas con la vista de "Scraping"

var data = [];
var filteredData = [];
var pageSize = 20;
var currentPage = 1;
var totalPages = 0;
var lastHash = "";

function formatNumber(value, locale = 'es-ES', options = {}) {
    return new Intl.NumberFormat(locale, options).format(value);
}

// Función para cargar la vista de "Scraping"
function loadScrapingView(view = 'scraping') {
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
                            <label for="filterTipoAnunciante">Filtrar por anunciante:</label>
                            <select id="filterTipoAnunciante" class="form-control form-control-custom" data-filter="tipoAnunciante">
                                <option value="Ver todos">Ver todos</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label for="filterTransaccion">Filtrar por tipo:</label>
                            <select id="filterTipoTransaccion" class="form-control form-control-custom" data-filter="tipoTransaccion">
                                <option value="Ver todos">Ver todos</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label for="filterMinPrice">Precio Mínimo:</label>
                            <input type="number" id="filterMinPrice" class="form-control form-control-custom" data-filter="precioMin" placeholder="Mínimo">
                        </div>
                        <div class="filter-group">
                            <label for="filterMaxPrice">Precio Máximo:</label>
                            <input type="number" id="filterMaxPrice" class="form-control form-control-custom" data-filter="precioMax" placeholder="Máximo">
                        </div>
                        <div class="filter-group">
                            <label for="filterBarrio">Filtrar por barrio:</label>
                            <select id="filterBarrio" class="form-control form-control-custom" data-filter="barrio">
                                <option value="Ver todos">Ver todos</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label for="filterHabitacion">Filtrar por habitaciones:</label>
                            <select id="filterHabitacion" class="form-control form-control-custom" data-filter="habitaciones">
                                <option value="Ver todos">Ver todos</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label for="filterPhone">Filtrar por teléfono:</label>
                            <input type="text" id="filterPhone" class="form-control form-control-custom" data-filter="tlf" placeholder="Buscar teléfono">
                        </div>
                        <div class="filter-group">
                            <label for="filterFuente">Filtrar por fuente:</label>
                            <select id="filterFuente" class="form-control form-control-custom" data-filter="fuente">
                                <option value="Ver todos">Ver todos</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label for="filterDisponibilidad">Filtrar por disponibilidad:</label>
                            <select id="filterDisponibilidad" class="form-control form-control-custom" data-filter="disponibilidad">
                                <option value="Ver todos">Ver todos</option>
                            </select>
                        </div>
                    </div>
                    <div id="sortContainer" class="mt-3">
                        <label for="sortOrder">Ordenar por:</label>
                        <select id="sortOrder" class="form-control">
                            <option value="fechaDesc" selected="1">Más nuevo a más antiguo</option>
                            <option value="fechaAsc">Más antiguo a más nuevo</option>
                        </select>
                    </div>
                </div>

                <!-- Columna para las tarjetas -->
                <div class="col-md-9">
                    <div id="cardsContainer" class="row">
                        <!-- Las tarjetas se generarán dinámicamente aquí -->
                    </div>
                    <!-- Controles de paginación -->
                    <div class="d-flex justify-content-between my-3">
                        <button id="firstPage" class="btn btn-secondary">Primera</button>
                        <button id="prevPageTop" class="btn btn-secondary">Anterior</button>
                        <span id="pageInfoTop" class="align-self-center">Página 1 de X</span>
                        <button id="nextPageTop" class="btn btn-secondary">Siguiente</button>
                        <button id="lastPage" class="btn btn-secondary">Última</button>
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
    loadDataFromAPI(view); // Cambiado para cargar desde la API
}

function configureScrapingEvents() {
    // Vincular eventos de cambio e input a todos los filtros dinámicamente
    $('[data-filter]').on('change input', function () {
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

    $('#firstPage').on('click', function () {
        if (currentPage > 1) {
            currentPage = 1;
            renderPage(currentPage);
            updatePaginationControls();
            scrollToTop();
        }
    });
    
    $('#lastPage').on('click', function () {
        if (currentPage < totalPages) {
            currentPage = totalPages;
            renderPage(currentPage);
            updatePaginationControls();
            scrollToTop();
        }
    });

    $('#sortOrder').on('change', function () {
        applySort();
    });
}

// Mostrar y ocultar indicador de carga
function showLoading() {
    $('#loadingIndicator').show();
}

function hideLoading() {
    $('#loadingIndicator').hide();
}

function getUrlFromRow(row) {
    url = '';
    if (row.fuente) {
        if (row.fuente == 'idealista') {
            url = `https://www.idealista.com/inmueble/${row.id_idealista}/`
        } else if (row.fuente == 'pdf') {
            url = `./pdf/${row.titulo}`
        } else if (row.fuente == 'fotocasa') {
            url = `${row.enlace}`
        }
    }
    return url;
}

// Cargar los datos desde la API
function loadDataFromAPI(view) {
    showLoading();
    $.ajax({
        url: 'http://euspay.com/api/v1/euspay.php/relacionados',
        dataType: 'json',
        success: function (response) {
            if (response.status === 'success'){
                data = response.data.map(row => ({
                    id: row.id_inmueble,
                    id_idealista: row.id_idealista,
                    titulo: row.titulo,
                    precio: row.precio,
                    cartera: row.cartera,
                    precio_por_metro: row.precio_metro,
                    superficie: row.superficie,
                    barrio: row.barrio,
                    calle: row.calle,
                    zona: row.zona,
                    ciudad: row.ciudad,
                    habitaciones: row.habitaciones,
                    banos: row.banos,
                    estado: row.estado,
                    tipoAnunciante: row.contacto ? row.contacto.tipo : 'Desconocido',
                    id_contacto: row.id_contacto,
                    anunciante: row.contacto ? row.contacto.nombre : 'Desconocido',
                    tlf: row.contacto ? row.contacto.telefono : null,
                    fecha: row.fecha ? new Date(row.fecha) : null,
                    caracteristicas: row.caracteristicas,
                    disponibilidad: row.disponibilidad,
                    comentarios: row.comentarios,
                    // TODO: Put this on a function, maybe fotocasa...
                    url: getUrlFromRow(row),
                    tipoTransaccion: row.tipo_transaccion,
                    fuente: row.fuente || 'Desconocida',
                }));
                if (view == 'scraping') {
                    data = data.filter(row => !row.cartera && row.tipoTransaccion !== 'Habitación');
                } else if (view == 'cartera') {
                    data = data.filter(row => !row.cartera && row.tipoTransaccion !== 'Habitación');
                } else if (view == 'habitaciones') {
                    data = data.filter(row => !row.cartera && row.tipoTransaccion === 'Habitación');
                }
                
                updateTipoAnuncianteFilter(data);
                updateTipoTransaccionFilter(data);
                updateBarrioFilter(data);
                updateFuenteFilter(data);
                updateHabitacionesFilter(data);
                updateDisponibilidadFilter(data);   
                applyFilters();
                $('#newDataAlert').fadeIn().delay(2000).fadeOut();
                hideLoading();

                // Variables para contar los inmuebles totales y los de particulares
                const totalInmuebles = data.length;
                const inmueblesParticulares = data.filter(p => p.tipoAnunciante === "Particular").length;
                const particularesVenta = data.filter(p => p.tipoAnunciante === "Particular" && p.tipoTransaccion === "Venta").lenght;
                const particularesAlquiler = data.filter(p => p.tipoAnunciante === "Particular" && p.tipoTransaccion === "Alquiler").length;
                
                document.getElementById('totalProperties').textContent = totalInmuebles;
                document.getElementById('privateProperties').textContent = inmueblesParticulares;
                document.getElementById("privateSaleProperties").textContent = particularesVenta;
                document.getElementById("privateRentProperties").textContent = particularesAlquiler;
                // console.log("Total de inmuebles:", totalInmuebles);
                // console.log("Inmuebles de particulares:", inmueblesParticulares);

                applyFilters();
                $("#loadingIndicator").hide();
            } else {
                console.error("Error al cargar los datos:", response.message);
                hideLoading();
            }
        },
        error: function (error) {
            console.error("Error en la solicitud:", error);
            hideLoading();
        }
    });
}

// Actualizar los filtros con valores únicos del dataset
function updateTipoAnuncianteFilter(data) {
    var uniqueTipoAnunciantes = _.uniq(data.map(row => row.tipoAnunciante).filter(Boolean));

    var $filter = $('#filterTipoAnunciante');
    $filter.empty();
    $filter.append('<option value="Ver todos">Ver todos</option>');
    uniqueTipoAnunciantes.forEach(tipoAnunciante => {
        $filter.append('<option value="' + tipoAnunciante + '">' + tipoAnunciante + '</option>');
    });
}

function updateDisponibilidadFilter(data) {
    var uniqueDisponibilidades = _.uniq(data.map(row => row.disponibilidad).filter(Boolean));

    var $filter = $('#filterDisponibilidad');
    $filter.empty();
    $filter.append('<option value="Ver todos">Ver todos</option>');
    uniqueDisponibilidades.forEach(disponibilidad => {
        $filter.append('<option value="' + disponibilidad + '">' + disponibilidad + '</option>');
    });
}

function updateTipoTransaccionFilter(data) {
    var uniqueTipos = _.uniq(data.map(row => row.tipoTransaccion).filter(Boolean));
    var $filter = $('#filterTipoTransaccion');
    $filter.empty();
    $filter.append('<option value="Ver todos">Ver todos</option>');
    uniqueTipos.forEach(tipoTransaccion => {
        $filter.append('<option value="' + tipoTransaccion + '">' + tipoTransaccion + '</option>');
    });
}

function updateBarrioFilter(data) {
    var uniqueBarrios = _.uniq(data.map(row => row.barrio).filter(Boolean));
    var $filter = $('#filterBarrio');
    $filter.empty();
    $filter.append('<option value="Ver todos">Ver todos</option>');
    uniqueBarrios.forEach(barrio => {
        $filter.append('<option value="' + barrio + '">' + barrio + '</option>');
    });
}

function updateFuenteFilter(data) {
    var uniqueFuentes = _.uniq(data.map(row => row.fuente).filter(Boolean));
    var $filter = $('#filterFuente');
    $filter.empty();
    $filter.append('<option value="Ver todos">Ver todos</option>');
    uniqueFuentes.forEach(fuente => {
        $filter.append('<option value="' + fuente + '">' + fuente + '</option>');
    });
}

function updateHabitacionesFilter(data) {
    // Obtener valores únicos de habitaciones
    var uniqueHabitaciones = _.uniq(data.map(row => row.habitaciones).filter(Boolean));

    // Ordenar las habitaciones de menor a mayor
    uniqueHabitaciones.sort((a, b) => a - b);

    // Buscar el filtro de habitaciones en el DOM
    var $filter = $('#filterHabitacion');
    if ($filter.length === 0) {
        console.error('No se encontró el filtro de habitaciones en el HTML.');
        return;
    }

    // Limpiar y añadir opciones al filtro
    $filter.empty();
    $filter.append('<option value="Ver todos">Ver todos</option>');
    uniqueHabitaciones.forEach(habitacion => {
        $filter.append('<option value="' + habitacion + '">' + habitacion + '</option>');
    });
}

// Aplicar los filtros
function applyFilters() {
    filteredData = data.filter(function (row) {
        let matches = true;

        // Obtener valores de los filtros de precio
        let minPrice = parseFloat($('#filterMinPrice').val()) || 0;
        let maxPrice = parseFloat($('#filterMaxPrice').val()) || Infinity;

        // Filtrar por precio dentro del rango
        if (row.precio) {
            matches = matches && row.precio >= minPrice && row.precio <= maxPrice;
        }

        // Iterar sobre todos los campos de filtro dinámicamente
        $('[data-filter]').each(function () {
            const filterKey = $(this).data('filter'); // Propiedad del objeto `row`
            let filterValue = $(this).val(); // Valor seleccionado o ingresado
            // Verificar si el filtro tiene un valor y si coincide
            if (filterValue && filterValue !== "Ver todos") {
                if (filterKey === "tlf") {
                    // Comparación especial para búsquedas parciales en teléfonos
                    matches = matches && row[filterKey] && row[filterKey].includes(filterValue);
                } else if (filterKey === 'precioMin' || filterKey === 'precioMax') {
                    // Estos filtros especiales se hacen antes de aplicar el resto de los filtros    
                } else {
                    // Habitaciones es un select, que devuelve un string, pero
                    // habitaciones es un entero, hay que parsear para poder comprobar
                    // que son iguales
                    if (filterKey === "habitaciones") {
                        filterValue = parseInt(filterValue);
                    }
                    // Comparación estándar para valores exactos
                    matches = matches && row[filterKey] === filterValue;
                }
            }
        });
        return matches;
    });

    currentPage = 1;
    totalPages = Math.ceil(filteredData.length / pageSize);
    renderPage(currentPage);
    updatePaginationControls();
    applySort(); // Ordenar los resultados filtrados
}


// Ordenar los datos filtrados
function applySort() {
    var sortOrder = $('#sortOrder').val();

    if (sortOrder === 'fechaAsc') {
        filteredData = _.sortBy(filteredData, ['fecha', 'id']); // Orden ascendente por fecha y luego ID
    } else if (sortOrder === 'fechaDesc') {
        filteredData = _.sortBy(filteredData, ['fecha', 'id']).reverse(); // Orden descendente por fecha y luego ID
    }

    currentPage = 1; // Reiniciar a la primera página después de ordenar
    renderPage(currentPage);
    updatePaginationControls();
}

// Renderizar la página actual
function renderPage(page) {
    $('#cardsContainer').empty();
    var start = (page - 1) * pageSize;
    var end = start + pageSize;
    var pageData = _.slice(filteredData, start, end);

    pageData.forEach(function (row) {
        var card = $('<div class="col-12 mb-4"></div>');
        var cardContent = '<div class="card-custom" style="position: relative;">';

        // Contenedor para los badges
        cardContent += `
            <div class="badges-container" style="display: flex; gap: 10px; position: absolute; top: 10px; right: 10px;">
        `;

        // Badge para "No disponible"
        if (row.disponibilidad === "No disponible") {
            cardContent += `
                <span class="badge badge-danger" style="font-size: 14px; padding: 5px 10px;">
                    No Disponible
                </span>
            `;
        }

        // Badge para "En cartera"
        if (row.cartera) {
            cardContent += `
                <span class="badge badge-success" style="font-size: 14px; padding: 5px 10px;">
                    En Cartera
                </span>
            `;
        }

        // Cierre del contenedor de badges
        cardContent += `</div>`;
        cardContent += '<h4>' + (row.titulo || 'Título desconocido') + '</h4>'; // Título en la parte superior

        cardContent += '<div class="separator"></div>';

        cardContent += '<div class="row-custom">';
        cardContent += `<div class="col-custom"><strong>Precio:</strong> ` + 
            (row.precio ? `${formatNumber(row.precio, 'es-ES', { style: 'currency', currency: 'EUR' })}` : 'N/A') + '</div>';
        cardContent += `<div class="col-custom"><strong>Precio/m²:</strong> ` + 
            (row.precio_por_metro ? `${formatNumber(row.precio_por_metro, 'es-ES', { style: 'currency', currency: 'EUR' })}` : 'N/A') + '</div>';
        cardContent += '</div>';

        cardContent += '<div class="row-custom">';
        cardContent += '<div class="col-custom"><strong>Superficie:</strong> ' + (row.superficie ? `${formatNumber(row.superficie, 'es-ES')} m²` : 'N/A') + '</div>';
        cardContent += '<div class="col-custom"><strong>Barrio:</strong> ' + (row.barrio || 'N/A') + '</div>';
        cardContent += '<div class="col-custom"><strong>Habitaciones:</strong> ' + (row.habitaciones || 'N/A') + '</div>';
        cardContent += '</div>';

        // Añadir Nombre Anunciante y Teléfono
        cardContent += '<div class="row-custom">';
        cardContent += '<div class="col-custom"><strong>Nombre Anunciante:</strong> ' + (row.anunciante || 'N/A') + '</div>';

        // Enlace telefónico seguro
        var telefono = row.tlf ? String(row.tlf).replace(/\s+/g, '').replace('+', '') : '';
        if (telefono && telefono.length >= 9) {
            var prefijo = telefono.length > 9 ? telefono.slice(0, 2) : ''; // Detecta prefijo si el número es mayor a 9 caracteres
            var numero = telefono.length > 9 ? telefono.slice(2) : telefono; // Si no hay prefijo, usar el número completo
            var telefonoHref = prefijo ? '+' + prefijo + numero : numero;
            cardContent += '<div class="col-custom"><strong>Teléfono:</strong> <a href="tel:' + telefonoHref + '">' + numero + '</a></div>';
        } else {
            cardContent += '<div class="col-custom"><strong>Teléfono:</strong> N/A</div>';
        }

        cardContent += '</div>';

        // Añadir fuente
        cardContent += '<div class="row-custom">';
        cardContent += '<div class="col-custom"><strong>Fuente:</strong> ' + (row.fuente || 'Desconocida') + '</div>';
        cardContent += '</div>';

        // Mostrar las características como etiquetas si existen
        if (row.caracteristicas) {
            cardContent += '<div class="tags">';
            var caracteristicas = row.caracteristicas.replace('[', '').replace(']', '').split(',');
            caracteristicas.forEach(function (caracteristica) {
                caracteristica = caracteristica.replace(/'/g, '').trim();
                cardContent += '<span class="badge-custom">' + caracteristica + '</span>';
            });
            cardContent += '</div>';
        }

        // Añadir el botón con la URL
        let viewMessage = 'Ver Inmueble';
        if (row.fuente === 'pdf') {
            viewMessage = 'Ver PDF';
        }
        if (row.url) {
            cardContent += '<a href="' + row.url + `" target="_blank" class="btn btn-primary btn-custom">${viewMessage}</a>`;
        }

        // Añadir separador
        cardContent += '<hr class="separator">';

        // Botón para mostrar/ocultar funcionalidades adicionales
        cardContent += '<button style="margin-right: 15px;" class="btn btn-info btn-sm mt-2" data-toggle="collapse" data-target="#funcionalidades-' + row.id + '">Mostrar Funcionalidades</button>';

        // Botón desplegable para realizar cálculo
        cardContent += '<button class="btn btn-secondary btn-sm mt-2" data-toggle="collapse" data-target="#calculo-' + row.id + '">Mostrar cálculo</button>';
        
        // Botoón para gestionar los contactos, bien creando o bien actualizando
        cardContent += `
            <button class="btn btn-info btn-sm mt-2" onclick="openContactModal(${row.id}, ${row.id_contacto || null})">
                Gestionar Contacto
            </button>
        `;

        // Botón para actualizar información inmueble
        cardContent += `
            <button class="btn btn-warning btn-sm mt-2" onclick="openPropertyModal(${row.id})">
                Editar Inmueble
            </button>
        `;
        
        cardContent += '<div id="calculo-' + row.id + '" class="collapse mt-2">';

        // Seleccionar porcentaje
        cardContent += '<label for="porcentaje-' + row.id + '">Seleccione porcentaje (%):</label>';
        cardContent += '<select id="porcentaje-' + row.id + '" class="form-control">';
        for (var i = 1; i <= 10; i++) {
            cardContent += '<option value="' + i + '">' + i + '%</option>';
        }
        cardContent += '</select>';

        // Añadir un campo para ingresar el precio y metros
        cardContent += '<input type="text" id="input-precio-' + row.id + '" class="form-control mt-2" value="' + (row.precio || 0) + '" readonly>';

        // Botón para realizar cálculo
        cardContent += '<button class="btn btn-primary mt-2" onclick="realizarCalculo(' + row.id + ', \'' + row.tipoTransaccion + '\')">Calcular Rentabilidad</button>';

        // Contenedor donde se mostrará el resultado del cálculo
        cardContent += '<div id="resultado-calculo-' + row.id + '" class="mt-2"></div>';

        cardContent += '</div>';

        // Contenedor colapsable para funcionalidades adicionales
        cardContent += '<div id="funcionalidades-' + row.id + '" class="collapse mt-2">';

        // Sección de comentarios
        cardContent += '<div class="comment-section">';
        cardContent += '<label for="commentInput-' + row.id + '">Comentarios:</label>';
        cardContent += '<textarea id="commentInput-' + row.id + '" class="form-control" placeholder="Escribe un comentario..."></textarea>';
        cardContent += '<button class="btn btn-custom mt-2" onclick="guardarComentario(' + row.id + ')">Guardar Comentario</button>';
        cardContent += '<ul id="commentList-' + row.id + '" class="comment-list mt-3">';

        // Cargar comentarios existentes
        if (row.comentarios && Array.isArray(row.comentarios)) {
            row.comentarios.forEach(function (comentario) {
                cardContent += `
                    <li class="comment-item">
                        <p>${comentario.comentario}</p>
                        <small><em>${new Date(comentario.fecha).toLocaleString('es-ES')}</em></small>
                        <button class="btn btn-sm btn-danger ml-2" onclick="borrarComentario(${comentario.id_comentario}, ${row.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </li>
                `;
            });
        } else {
            cardContent += '<li>No hay comentarios disponibles.</li>';
        }

        cardContent += '</ul>';
        cardContent += '</div>';

        // Registro de día y llamadas
        cardContent += '<div class="log-section mt-3">';
        cardContent += '<label for="dateInput-' + row.id + '">Fecha:</label>';
        cardContent += '<input type="date" id="dateInput-' + row.id + '" class="form-control">';
        cardContent += '<button class="btn btn-secondary mt-2" onclick="registrarLlamada(' + row.id + ')">Registrar Llamada</button>';
        cardContent += '<div id="callLog-' + row.id + '" class="mt-2"></div>';
        cardContent += '</div>';

        // Mostrar el botón para marcar como disponible si está "No disponible"
        if (row.disponibilidad === "No disponible") {
            cardContent += `
                <button class="btn btn-success mt-3" onclick="marcarDisponible(${row.id})">
                    Marcar como Disponible
                </button>
            `;
        } else {
            // Mostrar el botón para marcar como no disponible
            cardContent += `
                <button class="btn btn-danger mt-3" onclick="marcarNoDisponible(${row.id})">
                    Marcar como No Disponible
                </button>
            `;
        }
        // Botón para marcar como "En Cartera" o "No en Cartera"
        if (row.cartera) {
            cardContent += `
                <button class="btn btn-warning mt-3" onclick="toggleCartera(${row.id}, false)">
                    Quitar de cartera
                </button>
            `;
        } else {
            cardContent += `
                <button class="btn btn-success mt-3" onclick="toggleCartera(${row.id}, true)">
                    Poner en cartera
                </button>
            `;
        }

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
    $('#firstPage').prop('disabled', currentPage === 1);
    $('#lastPage').prop('disabled', currentPage === totalPages);
}

// Función para volver a la parte superior de la página
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Función para cargar comentarios desde la API
function cargarComentarios(id) {
    const commentList = $(`#commentList-${id}`);
    commentList.empty();

    $.ajax({
        url: `http://euspay.com/api/v1/euspay.php/comentarios/${id}`,
        type: 'GET',
        success: function (response) {
            if (response.status === 'success' && response.data.length) {
                response.data.forEach(comment => {
                    const commentHtml = `
                        <li class="comment-item">
                            <p>${comment.comentario}</p>
                            <small><em>${new Date(comment.fecha).toLocaleString('es-ES')}</em></small>
                        </li>
                    `;
                    commentList.append(commentHtml);
                });
            } else {
                commentList.append('<li>No hay comentarios disponibles.</li>');
            }
        },
        error: function () {
            commentList.append('<li>Error al cargar los comentarios.</li>');
        }
    });
}

// Función para guardar comentarios
window.guardarComentario = function(id) {
    const commentInput = $(`#commentInput-${id}`);
    const commentText = commentInput.val().trim();

    if (!commentText) {
        alert("El comentario no puede estar vacío.");
        return;
    }

    showLoading();

    $.ajax({
        url: 'http://euspay.com/api/v1/euspay.php/comentarios',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            id_inmueble: id,
            comentario: commentText,
            fecha: new Date().toISOString(),
        }),
        success: function (response) {
            const commentList = $(`#commentList-${id}`);
            const commentHtml = `
                <li class="comment-item">
                    <p>${response.data.comentario}</p>
                    <small><em>${new Date(response.data.fecha).toLocaleString('es-ES')}</em></small>
                    <button class="btn btn-sm btn-danger ml-2" onclick="borrarComentario(${response.data.id_comentario}, ${id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </li>
            `;
            commentList.append(commentHtml);
            commentInput.val('');
            hideLoading();
            alert("Comentario guardado exitosamente.");
        },
        error: function () {
            hideLoading();
            alert("Error al guardar el comentario.");
        }
    });
}

// Función para borrar un comentario
function borrarComentario(idComentario, idInmueble) {
    if (!confirm("¿Estás seguro de que deseas borrar este comentario?")) {
        return;
    }

    showLoading();

    $.ajax({
        url: `http://euspay.com/api/v1/euspay.php/comentarios/${idComentario}`,
        type: 'DELETE',
        success: function (response) {
            if (response.status === 'success') {
                alert("Comentario borrado exitosamente.");
                // Actualizar la lista de comentarios de la tarjeta
                const commentList = $(`#commentList-${idInmueble}`);
                commentList.find(`button[onclick="borrarComentario(${idComentario}, ${idInmueble})"]`).closest('li').remove();
            } else {
                alert("No se pudo borrar el comentario.");
            }
            hideLoading();
        },
        error: function () {
            alert("Error al intentar borrar el comentario.");
            hideLoading();
        }
    });
}


// Función para registrar llamadas
window.registrarLlamada = function(id) {
    alert('Pendiente de implementar');
    // const dateInput = $(`#dateInput-${id}`);
    // const dateValue = dateInput.val();

    // if (!dateValue) {
    //     alert("Por favor, selecciona una fecha para registrar la llamada.");
    //     return;
    // }

    // showLoading();

    // $.ajax({
    //     url: 'http://euspay.com/api/v1/euspay.php/llamadas',
    //     type: 'POST',
    //     contentType: 'application/json',
    //     data: JSON.stringify({
    //         id_inmueble: id,
    //         fecha: dateValue
    //     }),
    //     success: function (response) {
    //         const callLog = $(`#callLog-${id}`);
    //         const logHtml = `
    //             <div class="call-log-item">
    //                 <p>Llamada registrada el <strong>${new Date(dateValue).toLocaleDateString('es-ES')}</strong>.</p>
    //             </div>
    //         `;
    //         callLog.append(logHtml);
    //         dateInput.val('');
    //         hideLoading();
    //         alert("Llamada registrada exitosamente.");
    //     },
    //     error: function () {
    //         hideLoading();
    //         alert("Error al registrar la llamada.");
    //     }
    // });
}

function marcarDisponible(id) {
    if (!confirm("¿Estás seguro de que deseas marcar este inmueble como disponible?")) {
        return;
    }

    showLoading();

    $.ajax({
        url: `http://euspay.com/api/v1/euspay.php/inmuebles/${id}/disponibilidad`,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify({ disponibilidad: "disponible" }),
        success: function (response) {
            if (response.status === 'success') {
                alert("Inmueble marcado como disponible.");
                // Actualizar el estado en la lista de datos y volver a renderizar la página
                var inmueble = data.find(item => item.id === id);
                if (inmueble) {
                    inmueble.disponibilidad = "disponible";
                }
                renderPage(currentPage);
            } else {
                alert("No se pudo marcar el inmueble como disponible.");
            }
            hideLoading();
        },
        error: function () {
            alert("Error al intentar marcar el inmueble como disponible.");
            hideLoading();
        }
    });
}

// Función para marcar un inmueble como no disponible
window.marcarNoDisponible = function(id) {
    if (!confirm("¿Estás seguro de que quieres marcar este inmueble como no disponible?")) {
        return;
    }
    showLoading();
    $.ajax({
        url: `http://euspay.com/api/v1/euspay.php/inmuebles/${id}/disponibilidad`,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify({ disponibilidad: 'No disponible' }),
        success: function (response) {
            if (response.status === 'success') {
                alert("Inmueble marcado como no disponible.");
                // Opcional: Eliminar el inmueble de la vista
                var inmueble = data.find(item => item.id === id);
                if (inmueble) {
                    inmueble.disponibilidad = "No disponible";
                }
                renderPage(currentPage);
                updatePaginationControls();
            } else {
                alert("Error al marcar el inmueble como no disponible.");
            }
            hideLoading();
        },
        error: function () {
            hideLoading();
            alert("Error al marcar el inmueble como no disponible.");
        }
    });
}

function toggleCartera(id, newState) {
    const action = newState ? "Poner en cartera" : "Quitar de cartera";
    if (!confirm(`¿Estás seguro de que deseas ${action}?`)) {
        return;
    }

    showLoading();

    $.ajax({
        url: `http://euspay.com/api/v1/euspay.php/inmuebles/${id}/cartera`,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify({ cartera: newState }),
        success: function (response) {
            if (response.status === 'success') {
                alert(`Inmueble marcado como ${action}.`);
                var inmueble = data.find(item => item.id === id);
                if (inmueble) {
                    inmueble.cartera = newState;
                }
                renderPage(currentPage);
            } else {
                alert(`No se pudo ${action.toLowerCase()}.`);
            }
            hideLoading();
        },
        error: function () {
            alert(`Error al intentar ${action.toLowerCase()}.`);
            hideLoading();
        }
    });
}

function openContactModal(idInmueble, idContacto) {
    $('#inmuebleId').val(idInmueble);

    if (idContacto) {
        // Cargar datos del contacto desde la API
        $.ajax({
            url: `http://euspay.com/api/v1/euspay.php/contactos/${idContacto}`,
            type: 'GET',
            success: function (response) {
                if (response.status === 'success' && response.data) {
                    $('#contactId').val(idContacto);
                    $('#contactName').val(response.data.nombre);
                    $('#contactPhone').val(response.data.telefono);
                    $('#contactType').val(response.data.tipo_contacto);
                } else {
                    alert("No se pudo cargar la información del contacto.");
                }
            },
            error: function () {
                alert("Error al cargar el contacto.");
            }
        });
    } else {
        // Inicializar formulario vacío para crear un nuevo contacto
        $('#contactId').val('');
        $('#contactName').val('');
        $('#contactPhone').val('');
        $('#contactType').val('Particular');
    }

    // Mostrar el modal
    $('#contactModal').modal('show');
}

function saveContact() {
    const idContacto = $('#contactId').val();
    const idInmueble = $('#inmuebleId').val();
    const nombre = $('#contactName').val().trim();
    const telefono = $('#contactPhone').val().trim();
    const tipo = $('#contactType').val();

    if (!nombre || !telefono) {
        alert("Por favor, completa todos los campos.");
        return;
    }

    const payload = {
        nombre,
        telefono,
        tipo_contacto: tipo
    };

    const url = idContacto
        ? `http://euspay.com/api/v1/euspay.php/contactos/${idContacto}`
        : 'http://euspay.com/api/v1/euspay.php/contactos';

    const method = idContacto ? 'PUT' : 'POST';

    // Enviar datos a la API
    $.ajax({
        url: url,
        type: method,
        contentType: 'application/json',
        data: JSON.stringify(payload),
        success: function (response) {
            if (response.status === 'success') {
                alert("Contacto guardado con éxito.");

                // Si es un nuevo contacto, asociarlo al inmueble
                if (!idContacto) {
                    associateContactToInmueble(response.data.id, idInmueble);
                } else {
                    $('#contactModal').modal('hide');
                }
            } else {
                alert("No se pudo guardar el contacto.");
            }
        },
        error: function () {
            alert("Error al guardar el contacto.");
        }
    });
}

function associateContactToInmueble(idContacto, idInmueble) {
    $.ajax({
        url: `http://euspay.com/api/v1/euspay.php/inmuebles/${idInmueble}`,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify({ id_contacto: idContacto }),
        success: function (response) {
            if (response.status === 'success') {
                alert("Contacto asociado al inmueble.");
                $('#contactModal').modal('hide');
                // Recargar la página o actualizar la tarjeta
                loadDataFromAPI();
            } else {
                alert("No se pudo asociar el contacto al inmueble.");
            }
        },
        error: function () {
            alert("Error al asociar el contacto al inmueble.");
        }
    });
}

function openPropertyModal(idInmueble) {
    $('#propertyId').val(idInmueble);

    // Cargar datos del inmueble desde la API
    $.ajax({
        url: `http://euspay.com/api/v1/euspay.php/inmuebles/${idInmueble}`,
        type: 'GET',
        success: function (response) {
            if (response.status === 'success' && response.data) {
                const property = response.data;
                $('#propertyTitle').val(property.titulo || '');
                $('#propertyPrice').val(property.precio || '');
                $('#propertyPricePerMeter').val(property.precio_metro || '');
                $('#propertySurface').val(property.superficie || '');
                $('#propertyLocation').val(property.localizacion || '');
                $('#propertyNeighborhood').val(property.barrio || '');
                $('#propertyCity').val(property.ciudad || '');
                $('#propertyStreet').val(property.calle || '');
                $('#propertyBathrooms').val(property.banos || '');
                $('#propertyRooms').val(property.habitaciones || '');
                $('#propertyState').val(property.estado || '');
                $('#propertyZone').val(property.zona || '');
                $('#propertyModal').modal('show');
            } else {
                alert("No se pudo cargar la información del inmueble.");
            }
        },
        error: function () {
            alert("Error al cargar la información del inmueble.");
        }
    });
}

function saveProperty() {
    const idInmueble = $('#propertyId').val();
    const payload = {
        titulo: $('#propertyTitle').val().trim(),
        precio: parseFloat($('#propertyPrice').val()) || 0,
        precio_metro: parseFloat($('#propertyPricePerMeter').val()),
        superficie: parseFloat($('#propertySurface').val()),
        localizacion: $('#propertyLocation').val().trim(),
        barrio: $('#propertyNeighborhood').val().trim(),
        ciudad: $('#propertyCity').val().trim(),
        calle: $('#propertyStreet').val().trim(),
        banos: parseInt($('#propertyBathrooms').val(), 10),
        habitaciones: parseInt($('#propertyRooms').val(), 10),
        estado: $('#propertyState').val().trim(),
        zona: $('#propertyZone').val().trim(),
    };

    // Validar campos obligatorios
    if (!payload.titulo || isNaN(payload.precio) || isNaN(payload.superficie)) {
        alert("Por favor, completa todos los campos obligatorios.");
        return;
    }

    // Enviar los datos al servidor
    $.ajax({
        url: `http://euspay.com/api/v1/euspay.php/inmuebles/${idInmueble}`,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(payload),
        success: function (response) {
            if (response.status === 'success') {
                alert("Inmueble actualizado con éxito.");
                $('#propertyModal').modal('hide');
                // Recargar la página o actualizar la tarjeta
                loadDataFromAPI();
            } else {
                alert("No se pudo actualizar el inmueble.");
            }
        },
        error: function () {
            alert("Error al actualizar el inmueble.");
        }
    });
}


// Implementación de la función realizarCalculo
window.realizarCalculo = function(id, tipoTransaccion) {
    var precio = parseFloat($('#input-precio-' + id).val());
    var porcentaje = parseFloat($('#porcentaje-' + id).val());
  
    if (tipoTransaccion === 'Alquiler') {
        var ingresos = precio * 12;
        if (!isNaN(ingresos) && !isNaN(precio) && !isNaN(porcentaje)) {
            // Calcular el precio ajustado con el porcentaje seleccionado
            var precioAjustado = precio + (precio * (porcentaje / 100));
            // Calcular el precio de venta original sin aumento
            var precioVenta = (ingresos / porcentaje) * 100;
            // Calcular el precio de compra bruta (con el 15% de aumento)
            var precioCompraBruta = precioVenta * 1.15;
            // Calcular la rentabilidad bruta
            var rentabilidadBruta = (ingresos / precioCompraBruta) * 100;
            // Asumimos un 25% de gastos anuales para el cálculo de la rentabilidad neta
            var gastosAnuales = ingresos * 0.25;
            var ingresosNetos = ingresos - gastosAnuales;
            var rentabilidadNeta = (ingresosNetos / precioCompraBruta) * 100;
            $('#resultado-calculo-' + id).html('<strong>Precio de Venta:</strong> ' + precioVenta.toFixed(2) + ' €<br>' +
                '<strong>Precio Compra Bruta (con 15%):</strong> ' + precioCompraBruta.toFixed(2) + ' €<br>' +
                '<strong>Rentabilidad Bruta:</strong> ' + rentabilidadBruta.toFixed(2) + ' %<br>' +
                '<strong>Rentabilidad Neta:</strong> ' + rentabilidadNeta.toFixed(2) + ' %');
        } else {
            $('#resultado-calculo-' + id).html('<strong>Error:</strong> No se puede realizar el cálculo.');
        }
    } else {
        $('#resultado-calculo-' + id).html('<strong>Error:</strong> Solo se puede calcular la rentabilidad en inmuebles de alquiler.');
    }
}
