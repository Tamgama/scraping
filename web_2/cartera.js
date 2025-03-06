const API_URL = "http://euspay.com/api/v1/euspay.php/cartera";

var data = [];
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

        const result = await response.json();
        data = result.data || [];

        document.getElementById("totaldata").textContent = data.length;
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
    let end = pageSize === "all" ? data.length : start + pageSize;
    let paginatedData = data.slice(start, end);

    paginatedData.forEach((prop) => {
        tableBody.innerHTML += `
            <tr data-status="${prop.estado}">
                <td>${prop.id_inmueble}</td>
                <td>${prop.precio ? formatNumber(prop.precio) + '€' : 'N/A'}</td>
                <td><a href="${prop.enlace}" target="_blank">Ver</a></td>
                <td>${prop.titulo || 'N/A'}</td>
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
    let totalPages = Math.ceil(data.length / pageSize);
    document.getElementById("pageInfo").textContent = `Página ${currentPage} de ${totalPages}`;
    document.getElementById("prevPage").disabled = currentPage === 1;
    document.getElementById("nextPage").disabled = currentPage >= totalPages;
}

function changePage(direction) {
    let totalPages = Math.ceil(data.length / pageSize);
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
    document.getElementById("loadingIndicator").style.display = "block";
}

function hideLoading() {
    document.getElementById("loadingIndicator").style.display = "none";
}

document.addEventListener("DOMContentLoaded", loadData);
