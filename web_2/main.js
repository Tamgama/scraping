// main.js

$(document).ready(function () {
    var currentView = 'scraping'; // Vista actual

    // Cargar la vista por defecto
    loadScrapingView();

    // Event listeners para los botones de la barra de navegación
    $('#btnScraping').on('click', function (e) {
        e.preventDefault();
        if (currentView !== 'scraping') {
            currentView = 'scraping';
            loadScrapingView();
        }
    });

    $('#btnOtrosDocumentos').on('click', function (e) {
        e.preventDefault();
        if (currentView !== 'otrosDocumentos') {
            currentView = 'otrosDocumentos';
            loadOtrosDocumentosView();
        }
    });
});