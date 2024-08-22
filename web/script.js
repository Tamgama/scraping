
// Asume que tienes un archivo JSON llamado datos.json en el mismo directorio
fetch('datos.json')
    .then(response => response.json())
    .then(data => {
        displayTable(data);
    });

function displayTable(data) {
    const output = document.getElementById('output');
    let table = '<table>';

    // Adding header row
    if (data.length > 0) {
        table += '<tr>';
        Object.keys(data[0]).forEach(header => {
            table += `<th>${header}</th>`;
        });
        table += '</tr>';
    }

    // Adding data rows
    data.forEach(row => {
        table += '<tr>';
        Object.values(row).forEach(cell => {
            table += `<td>${cell !== undefined ? cell : ''}</td>`;
        });
        table += '</tr>';
    });

    table += '</table>';
    output.innerHTML = table;
}
