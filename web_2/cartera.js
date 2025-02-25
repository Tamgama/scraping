const API_URL = "http://127.0.0.1:5000/api/cartera"; // URL de la API

async function loadProperties() {
    try {
        // Mostrar indicador de carga
        showLoading();

        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("Error al cargar los datos");

        let properties = await response.json();

        // Filtrar solo los inmuebles que están en cartera
        properties = properties.filter(p => p.cartera === true);

        // Contar inmuebles en cartera
        document.getElementById("totalProperties").textContent = properties.length;
        document.getElementById("privateProperties").textContent = properties.filter(p => p.tipoAnunciante === "Particular").length;
        document.getElementById("privateSaleProperties").textContent = properties.filter(p => p.tipoAnunciante === "Particular" && p.tipoTransaccion === "Venta").length;
        document.getElementById("privateRentProperties").textContent = properties.filter(p => p.tipoAnunciante === "Particular" && p.tipoTransaccion === "Alquiler").length;

        // Renderizar propiedades en la tabla
        renderProperties(properties);

        // Ocultar indicador de carga
        hideLoading();

    } catch (error) {
        console.error("Error obteniendo datos:", error);
        hideLoading();
    }
}

// Función para mostrar los inmuebles en la tabla
function renderProperties(properties) {
    const tableBody = document.getElementById("carteraTableBody");
    tableBody.innerHTML = "";

    properties.forEach((prop) => {
        tableBody.innerHTML += `
            <tr data-status="${prop.status}">
                <td>${prop.id}</td>
                <td>${prop.titulo}</td>
                <td>${prop.precio}€</td>
                <td><span class="badge ${getBadgeClass(prop.status)}">${prop.status}</span></td>
                <td>${prop.fase}</td>
                <td>${prop.siguiente_accion}</td>
                <td>${prop.fecha_accion}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="editProperty(${prop.id})">✏️</button>
                    <button class="btn btn-sm btn-info" onclick="viewHistory(${prop.id})">📜</button>
                </td>
            </tr>`;
    });
}

// Función para asignar colores según el estado
function getBadgeClass(status) {
    return status === "Pendiente" ? "badge-pendiente" :
           status === "En Negociación" ? "badge-negociacion" :
           "badge-cerrado";
}

// Función para filtrar inmuebles por estado
function filterStatus(status) {
    document.querySelectorAll("#carteraTableBody tr").forEach(row => {
        row.style.display = (status === "all" || row.dataset.status === status) ? "" : "none";
    });
}

// Función para editar un inmueble
async function editProperty(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`);
        if (!response.ok) throw new Error("Error obteniendo detalles del inmueble");

        const property = await response.json();
        document.getElementById("editPropertyId").value = property.id;
        document.getElementById("editTitle").value = property.titulo;
        document.getElementById("editPrice").value = property.precio;

        $("#editPropertyModal").modal("show");
    } catch (error) {
        console.error("Error obteniendo el inmueble:", error);
    }
}

// Función para guardar cambios de edición
async function saveEdit() {
    const id = document.getElementById("editPropertyId").value;
    const updatedProperty = {
        titulo: document.getElementById("editTitle").value,
        precio: document.getElementById("editPrice").value,
    };

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedProperty),
        });

        if (!response.ok) throw new Error("Error al guardar los cambios");

        $("#editPropertyModal").modal("hide");
        loadProperties();
    } catch (error) {
        console.error("Error al actualizar:", error);
    }
}

// Función para ver historial del inmueble
async function viewHistory(id) {
    try {
        const response = await fetch(`${API_URL}/${id}/history`);
        if (!response.ok) throw new Error("Error obteniendo historial");

        const history = await response.json();
        document.getElementById("historyContent").innerHTML = history.map(entry => `<p>${entry}</p>`).join("");

        $("#historyModal").modal("show");
    } catch (error) {
        console.error("Error cargando historial:", error);
    }
}

// Función para mostrar indicador de carga
function showLoading() {
    const loadingIndicator = document.getElementById("loadingIndicator");
    if (loadingIndicator) {
        loadingIndicator.style.display = "block";
    }
}

// Función para ocultar indicador de carga
function hideLoading() {
    const loadingIndicator = document.getElementById("loadingIndicator");
    if (loadingIndicator) {
        loadingIndicator.style.display = "none";
    }
}

// Cargar los datos al inicio
document.addEventListener("DOMContentLoaded", loadProperties);
