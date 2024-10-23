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
        cardContent += '<p class="card-text"><strong>Precio alquiler mensual:</strong> ' + (row['precio'] || 'N/A') + ' €</p>';
        cardContent += '<p class="card-text"><strong>Precio de venta:</strong> ' + (row['precio_venta'] || 'N/A') + ' €</p>';
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

        // Botón desplegable para mostrar el cálculo
        cardContent += '<button class="btn btn-secondary btn-sm mt-2" data-toggle="collapse" data-target="#calculo-' + row['id'] + '">Mostrar cálculo</button>';
        cardContent += '<div id="calculo-' + row['id'] + '" class="collapse mt-2">';

        // Seleccionar porcentaje para ajustar el precio de venta
        cardContent += '<label for="porcentaje-' + row['id'] + '">Seleccione porcentaje (%):</label>';
        cardContent += '<select id="porcentaje-' + row['id'] + '" class="form-control">';
        for (var i = 1; i <= 10; i++) {
            cardContent += '<option value="' + i + '">' + i + '%</option>';
        }
        cardContent += '</select>';

        // Precio de venta original (se mostrará pero no se podrá editar)
        cardContent += '<div class="form-group mt-2"><input type="text" id="input-precio-venta-' + row['id'] + '" class="form-control" value="' + (row['precio_venta'] || 0) + '" readonly></div>';

        // Botón para realizar el cálculo
        cardContent += '<button class="btn btn-primary mt-2" onclick="realizarCalculo(' + row['id'] + ')">Calcular Rentabilidad</button>';

        // Contenedor donde se mostrará el resultado del cálculo
        cardContent += '<div id="resultado-calculo-' + row['id'] + '" class="mt-2"></div>';

        cardContent += '</div>'; // Fin del cálculo desplegable
        cardContent += '</div>'; // Fin del card-body
        cardContent += '</div>'; // Fin de la tarjeta

        card.append(cardContent);

        $('#cardsContainer').append(card);
    });
}

function realizarCalculo(id) {
    var precioAlquilerMensual = parseFloat($('#input-precio-venta-' + id).val());
    var precioVenta = parseFloat($('#input-precio-venta-' + id).val());
    var porcentaje = parseFloat($('#porcentaje-' + id).val());

    if (!isNaN(precioAlquilerMensual) && !isNaN(precioVenta) && !isNaN(porcentaje)) {
        // Calcular el ingreso anual por alquiler (precio mensual * 12)
        var ingresoAnual = precioAlquilerMensual * 12;
        
        // Ajustar el precio de venta según el porcentaje
        var precioAjustado = precioVenta + (precioVenta * (porcentaje / 100));
        
        // Calcular la rentabilidad bruta
        var rentabilidad = (ingresoAnual / precioAjustado) * 100;
        $('#resultado-calculo-' + id).html('<strong>Rentabilidad Bruta:</strong> ' + rentabilidad.toFixed(2) + ' %');
    } else {
        $('#resultado-calculo-' + id).html('<strong>Error:</strong> No se puede realizar el cálculo.');
    }
}
