document.addEventListener("DOMContentLoaded", function() {
    const propertyTypeSelect = document.getElementById('property-type');
    const operationTypeSelect = document.getElementById('operation-type');
    const zoneSelect = document.getElementById('zone');
    const bedroomsSelect = document.getElementById('bedrooms');
    const publicationDateSelect = document.getElementById('publication-date');
    const contentDiv = document.getElementById('content');
    const resultsCount = document.getElementById('results-count');
    const csvFileInput = document.getElementById('csvFileInput');

    let allItems = [];

    function filterItems() {
        const propertyType = propertyTypeSelect.value;
        const operationType = operationTypeSelect.value;
        const zone = zoneSelect.value;
        const bedrooms = bedroomsSelect.value;
        const publicationDate = publicationDateSelect.value;
        let visibleItems = 0;

        // Limpiar contenido
        contentDiv.innerHTML = '';

        allItems.forEach(item => {
            const itemPropertyType = item.propertyType;
            const itemOperationType = item.operationType;
            const itemZone = item.zone;
            const itemBedrooms = item.bedrooms;
            const itemPublicationDate = item.publicationDate;

            if (
                (propertyType === 'all' || itemPropertyType === propertyType) &&
                (operationType === 'all' || itemOperationType === operationType) &&
                (zone === 'all' || itemZone === zone) &&
                (bedrooms === 'all' || parseInt(itemBedrooms) >= parseInt(bedrooms)) &&
                (publicationDate === 'all' || itemPublicationDate === publicationDate)
            ) {
                const itemDiv = document.createElement('div');
                itemDiv.classList.add('item');
                itemDiv.innerHTML = `
                    <h3>${item.title}</h3>
                    <p>Precio: ${item.price}€</p>
                    <p>Superficie: ${item.surface}m²</p>
                    <p>Precio m²: ${item.pricePerM2}€/m²</p>
                    <p>Fecha: ${item.publicationDate}</p>
                `;
                contentDiv.appendChild(itemDiv);
                visibleItems++;
            }
        });

        // Actualiza el texto del contador de resultados
        resultsCount.textContent = visibleItems + " resultados obtenidos";
    }

    // Evento para cargar el archivo CSV
    csvFileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            Papa.parse(file, {
                header: true,
                dynamicTyping: true,
                complete: function(results) {
                    allItems = results.data.map(row => ({
                        propertyType: row["Tipo Propiedad"],
                        operationType: row["Tipo Operación"],
                        zone: row["Zona"],
                        bedrooms: row["Habitaciones"],
                        publicationDate: row["Fecha Publicación"],
                        title: row["Título"],
                        price: row["Precio"],
                        surface: row["Superficie"],
                        pricePerM2: row["Precio m²"]
                    }));

                    // Filtrar los elementos al cargar el CSV
                    filterItems();
                }
            });
        }
    });

    // Añade el evento 'change' a los selectores para aplicar filtros
    propertyTypeSelect.addEventListener('change', filterItems);
    operationTypeSelect.addEventListener('change', filterItems);
    zoneSelect.addEventListener('change', filterItems);
    bedroomsSelect.addEventListener('change', filterItems);
    publicationDateSelect.addEventListener('change', filterItems);
});
