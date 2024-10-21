$(document).ready(function () {
    var data = [];
    var filteredData = [];
    var pageSize = 20;
    var currentPage = 1;
    var totalPages = 0;
    var lastHash = "";

    // Mostrar el indicador de carga
    function showLoading() {
        $('#loadingIndicator').show();
    }

    // Ocultar el indicador de carga
    function hideLoading() {
        $('#loadingIndicator').hide();
    }

    // Cargar el archivo CSV automáticamente
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
                            filteredData = data; // Inicialmente, sin filtrar
                            updateAnuncianteFilter(data);
                            updateTipoFilter(data);
                            updateBarrioFilter(data);
                            updateDistritoFilter(data);
                            applyFilters(); // Aplicar filtros al cargar nuevos datos
                            $('#newDataAlert').fadeIn().delay(2000).fadeOut(); // Mostrar alerta
                            hideLoading(); // Ocultar el indicador de carga
                        }
                    });
                } else {
                    hideLoading(); // Ocultar el indicador de carga
                }
            },
            error: function() {
                hideLoading(); // Ocultar el indicador de carga en caso de error
            }
        });
    }

    // Verificar cambios en el archivo cada 5 segundos
    setInterval(loadCSV, 5000);

    // Cargar el CSV al iniciar la página
    loadCSV();

    // Mostrar/ocultar los filtros cuando se hace clic en el botón en pantallas pequeñas
    $('.filters-toggle-btn').click(function() {
        $('.filters-container').toggleClass('show');
    });

    // Filtro por anunciante
    $('#filterAnunciante').on('change', function () {
        applyFilters();
    });

    // Filtro por tipo
    $('#filterTipo').on('change', function () {
        applyFilters();
    });

    // Filtro por barrio
    $('#filterBarrio').on('change', function () {
        applyFilters();
    });

    // Filtro por distrito
    $('#filterDistrito').on('change', function () {
        applyFilters();
    });

    // Filtro por precio
    $('#filterPhone').on('input', function () {
        applyFilters();
    });

    // Actualizar el filtro de anunciante con los valores únicos del CSV
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

    // Actualizar el filtro de tipo con los valores únicos del CSV
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

    // Actualizar el filtro de barrio con los valores únicos del CSV
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

    // Actualizar el filtro de distrito con los valores únicos del CSV
    function updateDistritoFilter(data) {
        var uniqueDistritos = _.uniq(data.map(function(row) {
            return row['distrito'];
        }).filter(Boolean));

        var $filter = $('#filterDistrito');
        $filter.empty();
        $filter.append('<option value="Ver todos">Ver todos</option>');
        uniqueDistritos.forEach(function(distrito) {
            $filter.append('<option value="' + distrito + '">' + distrito + '</option>');
        });
    }

    // Actualizar el filtro de tlf con los valores únicos del CSV
    function updatePhoneFilter(data) {
        var uniquePhones = _.uniq(data.map(function(row) {
            return row['tlf'];
        }).filter(Boolean));

        var $filter = $('#filterPhone');
        $filter.empty();
        $filter.append('<option value="Ver todos">Ver todos</option>');
        uniquePhones.forEach(function(precio) {
            $filter.append('<option value="' + precio + '">' + precio + '</option>');
        });
    }

    // Aplicar los filtros de búsqueda
    function applyFilters() {
        var selectedAnunciante = $('#filterAnunciante').val();
        var selectedTipo = $('#filterTipo').val();
        var selectedBarrio = $('#filterBarrio').val();
        var selectedDistrito = $('#filterDistrito').val();
        var selectedPhone = $('#filterPhone').val();

        filteredData = data.filter(function (row) {
            var matchesAnunciante = selectedAnunciante === "Ver todos" || row['anunciante'] === selectedAnunciante;
            var matchesTipo = selectedTipo === "Ver todos" || row['tipo'] === selectedTipo;
            var matchesBarrio = selectedBarrio === "Ver todos" || row['barrio'] === selectedBarrio;
            var matchesDistrito = selectedDistrito === "Ver todos" || row['distrito'] === selectedDistrito;
            var matchesPhone = row['tlf'] && String(row['tlf']).includes(selectedPhone);
            return matchesAnunciante && matchesTipo && matchesBarrio && matchesDistrito && matchesPhone;
        });

        currentPage = 1;
        totalPages = Math.ceil(filteredData.length / pageSize);
        renderPage(currentPage);
        updatePaginationControls();
    }

    // Paginación
    $('#prevPageTop, #prevPageBottom').on('click', function () {
        if (currentPage > 1) {
            currentPage--;
            renderPage(currentPage);
            updatePaginationControls();
            scrollToTop(); // Volver a la parte superior
        }
    });

    $('#nextPageTop, #nextPageBottom').on('click', function () {
        if (currentPage < totalPages) {
            currentPage++;
            renderPage(currentPage);
            updatePaginationControls();
            scrollToTop(); // Volver a la parte superior
        }
    });

    // Renderizar la página con las tarjetas
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
            cardContent += '<div class="col-custom"><strong>Precio:</strong> ' + (row['precio'] || 'N/A') + ' €</div>';
            cardContent += '<div class="col-custom"><strong>Precio/m²:</strong> ' + (row['precio_por_metro'] || 'N/A') + '€/m²</div>';
            cardContent += '</div>';

            cardContent += '<div class="row-custom">';
            cardContent += '<div class="col-custom"><strong>Superficie:</strong> ' + (row['superficie'] || 'N/A') + ' m²</div>';
            cardContent += '</div>';

            // Añadir Barrio y Distrito
            cardContent += '<div class="row-custom">';
            cardContent += '<div class="col-custom"><strong>Barrio:</strong> ' + (row['barrio'] || 'N/A') + '</div>';
            cardContent += '<div class="col-custom"><strong>Distrito:</strong> ' + (row['distrito'] || 'N/A') + '</div>';
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

            
            // Añadir la valoración de venta
            var avgVentaRating = row['valoracion_venta'] || 'Sin valoración';
            cardContent += '<div class="row-custom">';
            cardContent += '<div class="col-custom"><strong>Valoración de venta:</strong> ' + avgVentaRating + '</div>';
            
            // Añadir desplegable para valoración de venta
            cardContent += '<div class="col-custom">';
            cardContent += '<label for="ventaRatingSelect">Valoración de venta:</label>';
            cardContent += '<select class="ventaRatingSelect" data-id="' + row['id'] + '">';
            for (var j = 1; j <= 10; j++) {
                cardContent += '<option value="' + j + '">' + j + '</option>';
            }
            cardContent += '</select>';
            cardContent += '</div>';
            
            cardContent += '</div>'; // Cerrar row-custom para valoración de venta
            cardContent += '</div>'; // Cerrar card-custom
            card.append(cardContent);
            
            // Añadir características como badges
            if (row['caracteristicas']) {
                cardContent += '<div class="badge-container">';
                var caracteristicas = row['caracteristicas'];

                // Eliminar corchetes, comillas simples y dividir en elementos separados por comas
                caracteristicas = caracteristicas.replace(/^\[|\]$/g, '').split(',');
                caracteristicas.forEach(function(caracteristica) {
                    // Eliminar comillas simples y espacios adicionales
                    caracteristica = caracteristica.replace(/'/g, '').trim();
                    cardContent += '<span class="badge-custom">' + caracteristica + '</span>';
                });

                cardContent += '</div>';
            }
            
            // Añadir el botón con la URL
            if (row['url']) {
                cardContent += '<a href="' + row['url'] + '" target="_blank" class="btn btn-primary btn-custom">Ver Inmueble</a>';
            }

            $('#cardsContainer').append(card);
        });

        // Añadir evento para manejar cambios en el desplegable de valoración media
        $('.ratingSelect').on('change', function() {
            var selectedValue = $(this).val();
            var inmuebleId = $(this).data('id');
            updateRating(inmuebleId, selectedValue, 'media');
        });

        // Añadir evento para manejar cambios en el desplegable de valoración de venta
        $('.ventaRatingSelect').on('change', function() {
            var selectedValue = $(this).val();
            var inmuebleId = $(this).data('id');
            updateRating(inmuebleId, selectedValue, 'venta');
        });
    }

    // Actualizar los controles de paginación
    function updatePaginationControls() {
        $('#currentPageTop, #currentPageBottom').text(currentPage);
        $('#totalPagesTop, #totalPagesBottom').text(totalPages);
        $('#prevPageTop, #prevPageBottom').prop('disabled', currentPage === 1);
        $('#nextPageTop, #nextPageBottom').prop('disabled', currentPage === totalPages);
    }

    // Volver a la parte superior de la página después de cambiar de página
    function scrollToTop() {
        $('html, body').animate({ scrollTop: 0 }, 'fast');
    }

    // Función para actualizar las valoraciones
    function updateRating(inmuebleId, rating, tipo) {
        // Encuentra el inmueble por id
        var inmueble = data.find(function (row) {
            return row['id'] == inmuebleId;
        });

        if (inmueble) {
            if (tipo === 'media') {
                // Actualizar la valoración media
                var valoraciones = inmueble.valoraciones || [];
                valoraciones.push(parseInt(rating));
                inmueble.valoraciones = valoraciones;

                var totalValoraciones = valoraciones.reduce(function (acc, val) {
                    return acc + val;
                }, 0);

                var avgRating = (totalValoraciones / valoraciones.length).toFixed(1);
                inmueble.valoracion_media = avgRating;

                // Actualizar visualmente la tarjeta
                $('select[data-id="' + inmuebleId + '"]').closest('.card-custom').find('.col-custom strong:contains("Valoración media")').next().text(avgRating);
            } else if (tipo === 'venta') {
                // Actualizar la valoración de venta
                var valoracionesVenta = inmueble.valoraciones_venta || [];
                valoracionesVenta.push(parseInt(rating));
                inmueble.valoraciones_venta = valoracionesVenta;

                var totalValoracionesVenta = valoracionesVenta.reduce(function (acc, val) {
                    return acc + val;
                }, 0);

                var avgVentaRating = (totalValoracionesVenta / valoracionesVenta.length).toFixed(1);
                inmueble.valoracion_venta = avgVentaRating;

                // Actualizar visualmente la tarjeta
                $('select[data-id="' + inmuebleId + '"]').closest('.card-custom').find('.col-custom strong:contains("Valoración de venta")').next().text(avgVentaRating);
            }
        }
    }
});
