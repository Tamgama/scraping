
console.log(Papa); // Esto debería mostrar el objeto Papa en la consola

document.addEventListener("DOMContentLoaded", function() {
    const contentContainer = document.getElementById('content');
    const resultsCount = document.getElementById('results-count');
    const filterButton = document.getElementById('filter-button');

    // Función para crear un item HTML basado en los datos del CSV
    function createItem(property) {
        const item = document.createElement('div');
        item.classList.add('item');
        item.setAttribute('data-property-type', property.Tipo.toLowerCase());
        // No hay `operation-type` en tu estructura, así que se elimina o se ajusta según el campo adecuado

        item.innerHTML = `
            <h3>${property.Título}</h3>
            <p>Calle: ${property.Calle}</p>
            <p>Barrio: ${property.Barrio}, Distrito: ${property.Distrito}, Ciudad: ${property.Ciudad}</p>
            <p>Área: ${property.Área} m²</p>
            <p>Precio: ${property.Precio}€</p>
            <p>Precio por m²: ${property.Precio_por_metro}€/m²</p>
            <p>Características: ${property.Características}</p>
            <p>Habitaciones: ${property.Habitaciones}, Baños: ${property.Baños}</p>
            <p>Metros construidos: ${property.Metros_construidos} m², Metros útiles: ${property.Metros_utiles} m²</p>
            <p>Anunciante: ${property.Anunciante} (${property.Nombre_Anunciante}), Teléfono: ${property.Teléfono}</p>
            <p>Última Actualización: ${property.Última_Actualización}</p>
            <a href="${property.URL}" target="_blank">Ver más detalles</a>
        `;

        contentContainer.appendChild(item);
    }

    // Función para filtrar los items
    function filterItems() {
        const propertyType = document.getElementById('property-type').value;
        const items = document.querySelectorAll('.content .item');
        let visibleItems = 0;

        items.forEach(item => {
            const itemPropertyType = item.getAttribute('data-property-type');

            if (propertyType === 'all' || itemPropertyType === propertyType) {
                item.classList.remove('hidden');
                visibleItems++;
            } else {
                item.classList.add('hidden');
            }
        });

        // Actualiza el contador de resultados
        resultsCount.textContent = visibleItems + " resultados obtenidos";
    }

    // Cargar y procesar CSV
    Papa.parse('/data/alquileres.csv', {
        download: true,
        header: true,
        complete: function(results) {
            const properties = results.data;
            properties.forEach(property => createItem(property));
            resultsCount.textContent = properties.length + " resultados obtenidos"; // Mostrar total antes de filtrar

            // Agregar funcionalidad de filtrado
            filterButton.addEventListener('click', filterItems);
        },
        error: function(err) {
            console.error("Error al cargar el archivo CSV:", err);
            resultsCount.textContent = "Error al cargar los resultados.";
        }
    });
});
