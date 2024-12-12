// main.js

$(document).ready(function () {
    var currentView = 'scraping'; // Vista actual

    // Cargar la vista por defecto (no en cartera)
    loadScrapingView(false);

    // Event listeners para los botones de la barra de navegación
    $('#btnScraping').on('click', function (e) {
        e.preventDefault();
        if (currentView !== 'scraping') {
            currentView = 'scraping';
            loadScrapingView(false);
        }
    });

    $('#btnEnCartera').on('click', function (e) {
        e.preventDefault();
        if (currentView !== 'cartera') {
            currentView = 'cartera';
            loadScrapingView(true);
        }
    });
});
