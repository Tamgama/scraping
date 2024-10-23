$(document).ready(function () {
    var data = [];
    var filteredData = [];
    var pageSize = 20;
    var currentPage = 1;
    var totalPages = 0;
    var lastHash = "";

    function showLoading() {
        $('#loadingIndicator').show();
    }

    function hideLoading() {
        $('#loadingIndicator').hide();
    }

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
                            updateDistritoFilter(data);
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

    setInterval(loadCSV, 5000);
    loadCSV();

    $('#filterAnunciante').on('change', function () {
        applyFilters();
    });

    $('#filterTipo').on('change', function () {
        applyFilters();
    });

    $('#filterBarrio').on('change', function () {
        applyFilters();
    });

    $('#filterDistrito').on('change', function () {
        applyFilters();
    });

    $('#filterPhone').on('input', function () {
        applyFilters();
    });

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

    function renderPage(page) {
        $('#cardsContainer').empty();
        var start = (page - 1) * pageSize;
        var end = start + pageSize;
        var pageData = _.slice(filteredData, start, end);

        pageData.forEach(function (row) {
            var card = $('<div class="col-12 col-md-6 col-lg-4 mb-4"></div>');
            var cardContent = '<div class="card shadow-sm">';
            cardContent += '<div class="card-body">';
            
            // Título
            cardContent += '<h5 class="card-title">' + (row['titulo'] || 'Título desconocido') + '</h5>';
            
            // Información básica
            cardContent += '<p class="card-text"><strong>Precio:</strong> ' + (row['precio'] || 'N/A') + ' €</p>';
            cardContent += '<p class="card-text"><strong>Barrio:</strong> ' + (row['barrio'] || 'N/A') + '</p>';
            cardContent += '<p class="card-text"><strong>Distrito:</strong> ' + (row['distrito'] || 'N/A') + '</p>';
            
            // Nombre del anunciante y teléfono
            cardContent += '<p class="card-text"><strong>Nombre Anunciante:</strong> ' + (row['nombre_anunciante'] || 'N/A') + '</p>';

            var telefono = row['tlf'] ? String(row['tlf']) : '';
            if (telefono && telefono.length > 2) {
                var prefijo = telefono.slice(0, 2);
                var numero = telefono.slice(2);
                cardContent += '<p class="card-text"><strong>Teléfono:</strong> <a href="tel:+' + prefijo + numero + '">' + numero + '</a></p>';
            } else {
                cardContent += '<p class="card-text"><strong>Teléfono:</strong> N/A</p>';
            }

            // Campo de ingresos si es de alquiler
            if (row['tipo'] === 'Alquiler') {
                cardContent += '<div class="form-group"><input type="text" id="input-ingresos-' + row['id'] + '" class="form-control" placeholder="Ingresos anuales alquiler"></div>';
            }

            // Botón desplegable para mostrar el cálculo
            cardContent += '<button class="btn btn-secondary btn-sm mt-2" data-toggle="collapse" data-target="#calculo-' + row['id'] + '">Mostrar cálculo</button>';
            cardContent += '<div id="calculo-' + row['id'] + '" class="collapse mt-2">';

            // Seleccionar porcentaje para ajustar el precio
            cardContent += '<label for="porcentaje-' + row['id'] + '">Seleccione porcentaje (%):</label>';
            cardContent += '<select id="porcentaje-' + row['id'] + '" class="form-control">';
            for (var i = 1; i <= 10; i++) {
                cardContent += '<option value="' + i + '">' + i + '%</option>';
            }
            cardContent += '</select>';

            // Precio original (se mostrará pero no se podrá editar)
            cardContent += '<div class="form-group mt-2"><input type="text" id="input-precio-' + row['id'] + '" class="form-control" value="' + (row['precio'] || 0) + '" readonly></div>';

            // Botón para realizar el cálculo
            cardContent += '<button class="btn btn-primary mt-2" onclick="realizarCalculo(' + row['id'] + ', \'' + row['tipo'] + '\')">Calcular Rentabilidad</button>';

            // Contenedor donde se mostrará el resultado del cálculo
            cardContent += '<div id="resultado-calculo-' + row['id'] + '" class="mt-2"></div>';

            cardContent += '</div>'; // Fin del cálculo desplegable
            cardContent += '</div>'; // Fin del card-body
            cardContent += '</div>'; // Fin de la tarjeta

            card.append(cardContent);

            $('#cardsContainer').append(card);
        });
    }

    // Función para calcular y mostrar precio de venta, compra bruta, rentabilidad bruta y neta
    function realizarCalculo(id, tipo) {
        var precio = parseFloat($('#input-precio-' + id).val());
        var porcentaje = parseFloat($('#porcentaje-' + id).val());

        if (tipo === 'Alquiler') {
            var ingresos = parseFloat($('#input-ingresos-' + id).val());
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
});
