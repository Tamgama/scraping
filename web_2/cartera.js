const API_URL = "http://euspay.com/api/v1/cartera"; // URL de la API de Cartera

var data = []; // Los datos originales
let filteredData = []; // Datos filtrados por estado
let selectedStatus = "all"; // Estado seleccionado
let currentPage = 1;
let pageSize = 10;

function formatNumber(value, locale = 'es-ES', options = {}) {
    return new Intl.NumberFormat(locale, options).format(value);
}

async function loadData() {
    try {
        showLoading();

        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("Error al cargar los datos");

        const response_info = await response.json();
        // La respuesta tiene formato: {"status":"success","message":"Registros obtenidos con éxito","data":[]}
        // los inmuebles están en el data dentro de la respuesta
        data = response_info.data;
        // Generar código alfanumérico basado en id_cartera
        data.forEach((prop) => {
            // 3 es bastante poco, por experiencia mínimo 5 99999
            prop.codigo = `CAR${String(prop.id_cartera).padStart(3, '0')}`;
        });

        document.getElementById("totalProperties").textContent = data.length;
        filteredData = [...data]; // Inicializar datos filtrados
        renderPage(currentPage);

        hideLoading();
    } catch (error) {
        console.error("Error obteniendo datos:", error);
        hideLoading();
    }
}

function renderPage(page) {
    const tableBody = document.getElementById("carteraTableBody");
    tableBody.innerHTML = "";

    let start = (page - 1) * pageSize;
    let end = pageSize === "all" ? filteredData.length : start + pageSize;
    let paginatedData = filteredData.slice(start, end);

    paginatedData.forEach((prop) => {
        tableBody.innerHTML += `
            <tr data-status="${prop.estado}">
                <td>${prop.id_inmueble}</td>
                <td>
                    <a href="${prop.enlace}" target="_blank">${prop.codigo}</a>
                </td>
                <td>${prop.titulo}</td>
                <td>${prop.precio ? formatNumber(prop.precio) + ' €' : 'N/A'}</td>
                <td><span class="badge ${getBadgeClass(prop.estado)}">${prop.estado}</span></td>
                <td>${prop.accion || 'N/A'}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="editProperty(${prop.id_cartera})">✏️</button>
                    <button class="btn btn-sm btn-info" onclick="viewHistory(${prop.id_cartera})">📜</button>
                </td>
            </tr>`;
    });

    updatePaginationControls();
}

function updatePaginationControls() {
    let totalPages = Math.ceil(filteredData.length / pageSize);
    document.getElementById("pageInfo").textContent = `Página ${currentPage} de ${totalPages || 1}`;
    document.getElementById("prevPage").disabled = currentPage === 1;
    document.getElementById("nextPage").disabled = currentPage >= totalPages;
}

function changePage(direction) {
    let totalPages = Math.ceil(filteredData.length / pageSize);
    if (direction === "prev" && currentPage > 1) {
        currentPage--;
    } else if (direction === "next" && currentPage < totalPages) {
        currentPage++;
    }
    renderPage(currentPage);
}

function changePageSize(size) {
    pageSize = size === "all" ? "all" : parseInt(size);
    currentPage = 1;
    renderPage(currentPage);
}

function getBadgeClass(status) {
    return status === "En proceso" ? "badge-proceso" : status === "Finalizado" ? "badge-cerrado" : "badge-cerrado";
}

function showLoading() {
    // Si no existe el loadingIndicator falla, asi que se crea uno en caso de que no
    // exista, a esto se le conoce como lazy inicialization
    let loadingIndicator = document.getElementById("loadingIndicator");
    if (!loadingIndicator) {
        if (!loadingIndicator) {
            loadingIndicator = document.createElement("div");
            loadingIndicator.id = "loadingIndicator";
            // El css se mete aquí directamente, pero 
            // podría ir al archivo cartera.css para dejar esto limpio
            loadingIndicator.innerHTML = `
                <div style="
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.5);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    z-index: 9999;
                ">
                    <div style="
                        background: white;
                        padding: 20px;
                        border-radius: 10px;
                        text-align: center;
                    ">
                        <span class="spinner-border text-primary" role="status"></span>
                        <p>Cargando...</p>
                    </div>
                </div>
            `;
            document.body.appendChild(loadingIndicator);
        }    
    }
    loadingIndicator.style.display = "block";
}

// Función para ocultar indicador de carga
function hideLoading() {
    // Puede que falle si no se ha llamado primero a showLoading, pero no debería
    // de todas maneras se comprueba que exista
    const loadingIndicator = document.getElementById("loadingIndicator")
    if (loadingIndicator) {
        loadingIndicator.style.display = "none";
    }
}

// Función para filtra, esto quizá interesa que sea una llamada a la api
// por tema de eficiencia, pero de momento lo hacemo aquí
function filterStatus(status) {
    selectedStatus = status; // Guardamos el estado seleccionado
    if (status === "all") {
        filteredData = [...data]; // Restauramos todos los datos
    } else {
        filteredData = data.filter(prop => prop.estado === status);
    }
    currentPage = 1; // Reiniciar a la primera página después del filtrado
    renderPage(currentPage); // Volver a renderizar la tabla
    // actualizar el total de inmuebles ??
    document.getElementById("totalProperties").textContent = filteredData.length;

}


function editProperty(idInmueble) {
    alert('Pendiente de implementar')
}

function viewHistory(idInmueble) {
    alert('Pendiente de implementar')
}

// Cargar los datos al inicio
document.addEventListener("DOMContentLoaded", loadData);
