// otros_documentos.js

// Variables y funciones relacionadas con la vista de "Otros Documentos"

var dataOtrosDocumentos = [];

// Función para cargar la vista de "Otros Documentos"
function loadOtrosDocumentosView() {
    // Limpiar el contenido principal
    $('#mainContent').empty();

    var otrosDocumentosContent = `
        <!-- Indicador de carga y alerta de nuevos datos -->
        <div id="loadingIndicatorOtros" class="alert alert-info text-center" style="display:none;">Cargando datos...</div>
        <div id="newDataAlertOtros" class="alert alert-success text-center" style="display:none;">Nuevos datos cargados</div>

        <!-- Contenedor para las tarjetas -->
        <div class="container mt-5">
            <div id="cardsContainerOtros" class="row">
                <!-- Las tarjetas se generarán aquí -->
            </div>
        </div>
    `;

    $('#mainContent').html(otrosDocumentosContent);

    // Inicializar variables específicas de Otros Documentos
    dataOtrosDocumentos = [];

    // Cargar datos
    loadCSVOtrosDocumentos();
}

function loadCSVOtrosDocumentos() {
    $('#loadingIndicatorOtros').show();
    $.ajax({
        url: './data/data-pdf.csv', // Asegúrate de que el CSV está en esta ruta
        dataType: 'text',
        success: function (csvData) {
            Papa.parse(csvData, {
                header: true,
                dynamicTyping: true,
                complete: function (results) {
                    dataOtrosDocumentos = results.data;
                    renderOtrosDocumentos(dataOtrosDocumentos);
                    $('#newDataAlertOtros').fadeIn().delay(2000).fadeOut();
                    $('#loadingIndicatorOtros').hide();
                }
            });
        },
        error: function() {
            $('#loadingIndicatorOtros').hide();
            alert('Error al cargar el archivo CSV de Otros Documentos.');
        }
    });
}

function renderOtrosDocumentos(data) {
    $('#cardsContainerOtros').empty();

    data.forEach(function (row, index) {
        var card = $('<div class="col-12 mb-4"></div>');
        var cardContent = '<div class="card-custom">';

        cardContent += '<h4>' + (row['pdf'] || 'Título desconocido') + '</h4>';
        cardContent += '<div class="separator"></div>';

        cardContent += '<div class="row-custom">';
        cardContent += '<div class="col-custom"><strong>Teléfono:</strong> ' + (row['teléfono'] || 'N/A') + '</div>';
        cardContent += '<div class="col-custom"><strong>Contacto:</strong> ' + (row['contacto'] || 'N/A') + '</div>';
        cardContent += '</div>';

        cardContent += '<div class="row-custom">';
        cardContent += '<div class="col-custom"><strong>Habitaciones:</strong> ' + (row['habitaciones'] || 'N/A') + '</div>';
        cardContent += '<div class="col-custom"><strong>Baños:</strong> ' + (row['baños'] || 'N/A') + '</div>';
        cardContent += '</div>';

        cardContent += '<div class="row-custom">';
        cardContent += '<div class="col-custom"><strong>Superficie:</strong> ' + (row['superficie'] || 'N/A') + ' m²</div>';
        cardContent += '<div class="col-custom"><strong>Precio de Alquiler:</strong> ' + (row['precio_alquiler'] || 'N/A') + ' €</div>';
        cardContent += '</div>';

        cardContent += '<div class="row-custom">';
        cardContent += '<div class="col-custom"><strong>Equipamiento:</strong> ' + (row['Equipment'] || 'N/A') + '</div>';
        cardContent += '</div>';

        // Aquí puedes agregar más contenido o funcionalidades si lo deseas

        cardContent += '</div>'; // Cierre de la tarjeta
        card.append(cardContent);

        $('#cardsContainerOtros').append(card);
    });
}
