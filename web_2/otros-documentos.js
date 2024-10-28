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

    // Cargar el archivo CSV para otros documentos
    function loadCSV() {
        showLoading();
        $.ajax({
            url: './src/data-pdf.csv', // Ruta al CSV para Otros documentos
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
                            updateFilters(data);
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

    // Cargar el CSV al iniciar la página
    loadCSV();

    // Filtrar por anunciante, tipo, barrio y teléfono
    $('#filterAnunciante, #filterTipo, #filterBarrio, #filterPhone').on('change input', function () {
        applyFilters();
    });

    // Actualizar los filtros basados en los datos cargados
    function updateFilters(data) {
        updateAnuncianteFilter(data);
        updateTipoFilter(data);
        updateBarrioFilter(data);
    }

    // Actualizar el filtro de anunciante
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

    // Actualizar el filtro de tipo
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

    // Actualizar el filtro de barrio
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

    // Aplicar los filtros de búsqueda
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
                cardContent += '<a href="' + row['url'] + '" target="_blank" class="btn btn-primary btn-custom">Ver Documento</a>';
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

            cardContent += '</div>'; // Cierre del div card-custom
            card.append(cardContent);

            $('#cardsContainer').append(card);
        });
    }

    function updatePaginationControls() {
        $('#pageInfoTop, #pageInfoBottom').text('Página ' + currentPage + ' de ' + totalPages);
        $('#prevPageTop, #prevPageBottom').prop('disabled', currentPage === 1);
        $('#nextPageTop, #nextPageBottom').prop('disabled', currentPage === totalPages);
    }

    // Función para volver a la parte superior de la página
    function scrollToTop() {
        $('html, body').animate({ scrollTop: 0 }, 'fast');
    }
});
