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
    sendResponse("error", "Error de conexión: " . $e->getMessage(), null, [$e->getMessage()]);
}

// Obtener la ruta de la API
$uri = $_SERVER['REQUEST_URI'];
$basePath = '/api/v1/euspay.php';
$path = str_replace($basePath, '', parse_url($uri, PHP_URL_PATH));
$segments = explode('/', trim($path, '/'));

$table = $segments[0] ?? null; // Primera parte: nombre de la tabla
$id = $segments[1] ?? null;    // Segunda parte: ID opcional

// Validar tabla
$validTables = ["inmuebles", "contactos", "comentarios", "relacionados"];
if (!in_array($table, $validTables)) {
    sendResponse("error", "Tabla no permitida o inexistente.");
}

// Leer método HTTP
$method = $_SERVER['REQUEST_METHOD'];

// Función para formatear un inmueble con comentarios y contactos
function formatInmuebleWithComments($rows) {
    if (empty($rows)) return [];

    $result = [];
    foreach ($rows[0] as $key => $value) {
        if (!str_starts_with($key, 'contacto_') && !str_starts_with($key, 'comentario_')) {
            $result[$key] = $value;
        }
    }

    $result['contacto'] = [
        "nombre" => $rows[0]['contacto_nombre'] ?? null,
        "telefono" => $rows[0]['contacto_telefono'] ?? null,
        "tipo" => $rows[0]['tipo_contacto'] ?? null
    ];

    $result['comentarios'] = [];
    foreach ($rows as $row) {
        if (isset($row['id_comentario'])) {
            $result['comentarios'][] = [
                "id_comentario" => $row['id_comentario'],
                "comentario" => $row['comentario_texto'] ?? null,
                "fecha" => $row['comentario_fecha'] ?? null
            ];
        }
    }

    return $result;
}

// Función para formatear múltiples inmuebles con comentarios
function formatMultipleInmueblesWithComments($rows) {
    if (empty($rows)) return [];

    $inmuebles = [];
    foreach ($rows as $row) {
        $id_inmueble = $row['id_inmueble'];

        if (!isset($inmuebles[$id_inmueble])) {
            $inmuebles[$id_inmueble] = [];
            foreach ($row as $key => $value) {
                if (!str_starts_with($key, 'contacto_') && !str_starts_with($key, 'comentario_')) {
                    $inmuebles[$id_inmueble][$key] = $value;
                }
            }

            $inmuebles[$id_inmueble]['contacto'] = [
                "nombre" => $row['contacto_nombre'] ?? null,
                "telefono" => $row['contacto_telefono'] ?? null,
                "tipo" => $row['tipo_contacto'] ?? null
            ];

            $inmuebles[$id_inmueble]['comentarios'] = [];
        }

        if (isset($row['id_comentario'])) {
            $inmuebles[$id_inmueble]['comentarios'][] = [
                "id_comentario" => $row['id_comentario'],
                "comentario" => $row['comentario_texto'] ?? null,
                "fecha" => $row['comentario_fecha'] ?? null,
            ];
        }
    }

    return array_values($inmuebles);
}

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
            $queryParams = $_GET;

            if ($table === 'comentarios') {
                if ($id) {
                    // Obtener comentarios para un inmueble específico
                    $stmt = $pdo->prepare("SELECT * FROM comentarios WHERE id_inmueble = :id ORDER BY fecha DESC");
                    $stmt->execute(['id' => $id]);
                    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
                    sendResponse("success", "Comentarios obtenidos con éxito", $rows ?: []);
                } else {
                    // Si no hay ID, devolver todos los comentarios
                    $stmt = $pdo->query("SELECT * FROM comentarios ORDER BY fecha DESC");
                    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
                    sendResponse("success", "Comentarios obtenidos con éxito", $rows ?: []);
                }
            } else if ($table === 'relacionados') {
                if ($id) {
                    // Obtener un inmueble específico con contactos y comentarios
                    $stmt = $pdo->prepare("
                        SELECT 
                            inmuebles.*,
                            contactos.nombre AS contacto_nombre,
                            contactos.telefono AS contacto_telefono,
                            contactos.tipo_contacto AS tipo_contacto,
                            comentarios.id_comentario,
                            comentarios.comentario AS comentario_texto,
                            comentarios.fecha AS comentario_fecha
                        FROM inmuebles
                        LEFT JOIN contactos ON inmuebles.id_contacto = contactos.id_contacto
                        LEFT JOIN comentarios ON inmuebles.id_inmueble = comentarios.id_inmueble
                        WHERE inmuebles.id_inmueble = :id
                    ");
                    $stmt->execute(['id' => $id]);
                    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
                    sendResponse("success", "Datos del inmueble obtenidos con éxito", $rows ? formatInmuebleWithComments($rows) : []);
                } else {
                    // Obtener todos los inmuebles con contactos y comentarios
                    $stmt = $pdo->query("
                        SELECT 
                            inmuebles.*,
                            contactos.nombre AS contacto_nombre,
                            contactos.telefono AS contacto_telefono,
                            contactos.tipo_contacto AS tipo_contacto,
                            comentarios.id_comentario,
                            comentarios.comentario AS comentario_texto,
                            comentarios.fecha AS comentario_fecha
                        FROM inmuebles
                        LEFT JOIN contactos ON inmuebles.id_contacto = contactos.id_contacto
                        LEFT JOIN comentarios ON inmuebles.id_inmueble = comentarios.id_inmueble
                    ");
                    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
                    sendResponse("success", "Inmuebles obtenidos con éxito", $rows ? formatMultipleInmueblesWithComments($rows) : []);
                }
            } else {
                // Obtener registros de una tabla específica
                if ($id) {
                    $stmt = $pdo->prepare("SELECT * FROM `$table` WHERE id_" . rtrim($table, 's') . " = :id");
                    $stmt->execute(['id' => $id]);
                    $data = $stmt->fetch(PDO::FETCH_ASSOC);
                    sendResponse("success", "Registro obtenido con éxito", $data ?: []);
                } else {
                    if (empty($queryParams)) {
                        $stmt = $pdo->query("SELECT * FROM `$table`");
                        $data = $stmt->fetchAll(PDO::FETCH_ASSOC);
                        sendResponse("success", "Registros obtenidos con éxito", $data ?: []);
                    } else {
                        $whereClauses = [];
                        $params = [];
                        foreach ($queryParams as $key => $value) {
                            $whereClauses[] = "$key = :$key";
                            $params[$key] = $value;
                        }
                        $whereSql = $whereClauses ? "WHERE " . implode(" AND ", $whereClauses) : "";
                        $stmt = $pdo->prepare("SELECT * FROM `$table` $whereSql");
                        $stmt->execute($params);
                        $data = $stmt->fetchAll(PDO::FETCH_ASSOC);
                        sendResponse("success", "Registros obtenidos con éxito", $data ?: []);
                    }
                }
            }
            break;

            case 'POST':
                // Crear un nuevo registro
                $input = json_decode(file_get_contents('php://input'), true);
                if (!$input || !is_array($input)) {
                    sendResponse("error", "Cuerpo JSON inválido o faltante.");
                }
                if ($table === 'comentarios') {
                    // Crear un nuevo comentario
                    if (!isset($input['id_inmueble'], $input['comentario'], $input['fecha'])) {
                        sendResponse("error", "Campos requeridos: id_inmueble, comentario, fecha.");
                    }
            
                    $stmt = $pdo->prepare("
                        INSERT INTO comentarios (id_inmueble, comentario, fecha) 
                        VALUES (:id_inmueble, :comentario, :fecha)
                    ");
            
                    try {
                        $stmt->execute([
                            'id_inmueble' => $input['id_inmueble'],
                            'comentario' => $input['comentario'],
                            'fecha' => $input['fecha']
                        ]);
            
                        sendResponse("success", "Comentario creado con éxito.", [
                            "id_comentario" => $pdo->lastInsertId(),
                            "id_inmueble" => $input['id_inmueble'],
                            "comentario" => $input['comentario'],
                            "fecha" => $input['fecha']
                        ]);
                    } catch (PDOException $e) {
                        sendResponse("error", "No se pudo crear el comentario.", null, [$e->getMessage()]);
                    }
                } else {
                    // Crear un registro genérico
                    $columns = implode(", ", array_keys($input));
                    $placeholders = ":" . implode(", :", array_keys($input));
                    $stmt = $pdo->prepare("INSERT INTO `$table` ($columns) VALUES ($placeholders)");
            
                    try {
                        $stmt->execute($input);
                        $lastInsertId = $pdo->lastInsertId();
                        sendResponse("success", "Registro creado con éxito.", ["id" => $lastInsertId]);
                    } catch (PDOException $e) {
                        sendResponse("error", "No se pudo crear el registro.", null, [$e->getMessage()]);
                    }
                }
                break;
            

        case 'PUT':
            // Actualizar un registro existente
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
            $sql = "UPDATE `$table` SET " . implode(", ", $sets) . " WHERE id_" . rtrim($table, 's') . " = :id";
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
            // Eliminar un registro o todos los registros de la tabla
            if ($id) {
                // Eliminar un registro específico
                $sql = "DELETE FROM `$table` WHERE id_" . rtrim($table, 's') . " = :id";
                $stmt = $pdo->prepare($sql);
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
            } else {
                // Eliminar todos los registros de la tabla
                $sql = "DELETE FROM `$table`";
                $stmt = $pdo->prepare($sql);
                try {
                    $stmt->execute();
                    sendResponse("success", "Todos los registros de la tabla '$table' han sido eliminados.");
                } catch (PDOException $e) {
                    sendResponse("error", "No se pudo eliminar todos los registros.", null, [$e->getMessage()]);
                }
            }
            break;

        default:
            sendResponse("error", "Método no permitido.");
    }
} catch (PDOException $e) {
    sendResponse("error", "Error al procesar la solicitud", null, [$e->getMessage()]);
}
