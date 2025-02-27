<?php
// Configuración de la base de datos
$dbHost = 'db826038170.hosting-data.io';
$dbName = 'db826038170';
$dbUser = 'dbo826038170';
$dbPass = 'promurcia2165';

try {
    // Conexión a la base de datos
    $pdo = new PDO("mysql:host=$dbHost;dbname=$dbName;charset=utf8mb4", $dbUser, $dbPass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    sendResponse("error", "Error de conexión: " . $e->getMessage());
}

// Leer método HTTP
$method = $_SERVER['REQUEST_METHOD'];
$id = $_GET['id'] ?? null; // ID opcional para operaciones específicas

// Función para enviar respuestas JSON estandarizadas
function sendResponse($status, $message, $data = null, $errors = null) {
    header('Content-Type: application/json');
    $response = [
        "status" => $status,
        "message" => $message,
        "data" => $data,
    ];
    if ($errors !== null) {
        $response["errors"] = $errors;
    }
    echo json_encode($response);
    exit;
}

// CRUD y operaciones relacionadas
try {
    switch ($method) {
        case 'GET':
            if ($id) {
                // Obtener un registro específico
                $stmt = $pdo->prepare("SELECT * FROM cartera WHERE id_cartera = :id");
                $stmt->execute(['id' => $id]);
                $data = $stmt->fetch(PDO::FETCH_ASSOC);
                sendResponse("success", "Registro obtenido con éxito", $data ?: []);
            } else {
                // Obtener todos los registros
                $stmt = $pdo->query("SELECT * FROM cartera");
                $data = $stmt->fetchAll(PDO::FETCH_ASSOC);
                sendResponse("success", "Registros obtenidos con éxito", $data ?: []);
            }
            break;

        case 'POST':
            // Crear un nuevo registro
            $input = json_decode(file_get_contents('php://input'), true);
            if (!$input || !isset($input['estado'], $input['acciones'], $input['fecha_accion'], $input['enlace'], $input['id_inmueble'], $input['id_transaccion'])) {
                sendResponse("error", "Campos requeridos: estado, acciones, fecha_accion, enlace, id_inmueble, id_transaccion.");
            }

            $stmt = $pdo->prepare("
                INSERT INTO cartera (estado, acciones, fecha_accion, enlace, id_inmueble, id_transaccion) 
                VALUES (:estado, :acciones, :fecha_accion, :enlace, :id_inmueble, :id_transaccion)
            ");

            try {
                $stmt->execute([
                    'estado' => $input['estado'],
                    'acciones' => $input['acciones'],
                    'fecha_accion' => $input['fecha_accion'],
                    'enlace' => $input['enlace'],
                    'id_inmueble' => $input['id_inmueble'],
                    'id_transaccion' => $input['id_transaccion']
                ]);

                sendResponse("success", "Registro creado con éxito.", ["id_cartera" => $pdo->lastInsertId()]);
            } catch (PDOException $e) {
                sendResponse("error", "No se pudo crear el registro.", null, [$e->getMessage()]);
            }
            break;

        case 'PUT':
            if (!$id) {
                sendResponse("error", "ID requerido para actualizar.");
            }

            $input = json_decode(file_get_contents('php://input'), true);
            if (!$input || !is_array($input)) {
                sendResponse("error", "Cuerpo JSON inválido o faltante.");
            }

            // Generar la consulta de actualización
            $sets = [];
            foreach ($input as $key => $value) {
                $sets[] = "$key = :$key";
            }
            $sql = "UPDATE cartera SET " . implode(", ", $sets) . " WHERE id_cartera = :id";
            $input['id'] = $id;

            $stmt = $pdo->prepare($sql);
            try {
                $stmt->execute($input);
                if ($stmt->rowCount() > 0) {
                    sendResponse("success", "Registro actualizado con éxito.");
                } else {
                    sendResponse("success", "No se realizaron cambios; el registro no existe o los datos son idénticos.");
                }
            } catch (PDOException $e) {
                sendResponse("error", "No se pudo actualizar el registro.", null, [$e->getMessage()]);
            }
            break;

        case 'DELETE':
            if (!$id) {
                sendResponse("error", "ID requerido para eliminar.");
            }

            $stmt = $pdo->prepare("DELETE FROM cartera WHERE id_cartera = :id");
            try {
                $stmt->execute(['id' => $id]);
                if ($stmt->rowCount() > 0) {
                    sendResponse("success", "Registro eliminado con éxito.");
                } else {
                    sendResponse("error", "No se encontró el registro para eliminar.");
                }
            } catch (PDOException $e) {
                sendResponse("error", "No se pudo eliminar el registro.", null, [$e->getMessage()]);
            }
            break;

        default:
            sendResponse("error", "Método no permitido.");
    }
} catch (PDOException $e) {
    sendResponse("error", "Error al procesar la solicitud", null, [$e->getMessage()]);
}
?>
