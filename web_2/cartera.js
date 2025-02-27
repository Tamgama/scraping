const API_URL = "http://euspay.com/api/v1/euspay.php/cartera"; // URL de la API de Cartera

var data = [];
let currentPage = 1;
let pageSize = 10; // Cantidad predeterminada de inmuebles por página

function formatNumber(value, locale = 'es-ES', options = {}) {
    return new Intl.NumberFormat(locale, options).format(value);
}

async function loaddata() {
    try {
        showLoading();

        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("Error al cargar los datos");

        data = await response.json();

        // Generar código alfanumérico basado en id_cartera
        data.forEach((prop) => {
            prop.codigo = `CAR${String(prop.id_cartera).padStart(3, '0')}`;
        });

        document.getElementById("totaldata").textContent = data.length;

        renderPage(currentPage);

        hideLoading();
    } catch (error) {
        console.error("Error obteniendo datos:", error);
        hideLoading();
    }
}

// Renderizar la tabla con paginación
function renderPage(page) {
    const tableBody = document.getElementById("carteraTableBody");
    tableBody.innerHTML = "";

    let start = (page - 1) * pageSize;
    let end = pageSize === "all" ? data.length : start + pageSize;
    let paginatedData = data.slice(start, end);

    paginatedData.forEach((prop) => {
        tableBody.innerHTML += `
            <tr data-status="${prop.estado}">
                <td>${prop.id_inmueble}</td>
                <td>
                    <a href="${prop.enlace}" target="_blank">${prop.codigo}</a>
                </td>
                <td>${prop.titulo}</td>
                <td>${prop.precio ? prop.precio + '€' : 'N/A'}</td>
                <td><span class="badge ${getBadgeClass(prop.estado)}">${prop.estado}</span></td>
                <td>${prop.fase || 'N/A'}</td>
                <td>${prop.siguiente_accion || 'N/A'}</td>
                <td>${prop.fecha_accion ? new Date(prop.fecha_accion).toLocaleDateString('es-ES') : 'N/A'}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="editProperty(${prop.id_inmueble})">✏️</button>
                    <button class="btn btn-sm btn-info" onclick="viewHistory(${prop.id_inmueble})">📜</button>
                </td>
            </tr>`;
    });

    updatePaginationControls();
}

// Actualizar controles de paginación
function updatePaginationControls() {
    let totalPages = Math.ceil(data.length / pageSize);
    document.getElementById("pageInfo").textContent = `Página ${currentPage} de ${totalPages}`;
    document.getElementById("prevPage").disabled = currentPage === 1;
    document.getElementById("nextPage").disabled = currentPage >= totalPages;
}

// Función para cambiar de página
function changePage(direction) {
    let totalPages = Math.ceil(data.length / pageSize);
    if (direction === "prev" && currentPage > 1) {
        currentPage--;
    } else if (direction === "next" && currentPage < totalPages) {
        currentPage++;
    }
    renderPage(currentPage);
}

// Función para cambiar cantidad de inmuebles por página
function changePageSize(size) {
    pageSize = size === "all" ? "all" : parseInt(size);
    currentPage = 1;
    renderPage(currentPage);
}

// Función para asignar colores según el estado
function getBadgeClass(status) {
    return status === "Pendiente" ? "badge-pendiente" :
           status === "En Negociación" ? "badge-negociacion" :
           "badge-cerrado";
}

// Función para mostrar indicador de carga
function showLoading() {
    document.getElementById("loadingIndicator").style.display = "block";
}

// Función para ocultar indicador de carga
function hideLoading() {
    document.getElementById("loadingIndicator").style.display = "none";
}

// Cargar los datos al inicio
document.addEventListener("DOMContentLoaded", loaddata);
