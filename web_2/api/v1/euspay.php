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
    http_response_code(500);
    echo json_encode(["error" => "Error de conexión: " . $e->getMessage()]);
    exit;
}

// Obtener la ruta de la API
$uri = $_SERVER['REQUEST_URI'];
$basePath = '/api/v1/euspay.php';
$path = str_replace($basePath, '', parse_url($uri, PHP_URL_PATH));
$segments = explode('/', trim($path, '/'));

$table = $segments[0] ?? null; // Primera parte: nombre de la tabla
$id = $segments[1] ?? null;    // Segunda parte: ID opcional

// Validar tabla
$validTables = ["inmuebles", "contactos", "comentarios"];
if (!in_array($table, $validTables) && $table !== 'relacionados') {
    sendResponse(400, ["error" => "Tabla no permitida o inexistente."]);
}

// Leer método HTTP
$method = $_SERVER['REQUEST_METHOD'];

// Función para enviar respuestas JSON
function sendResponse($status, $data) {
    http_response_code($status);
    header('Content-Type: application/json');
    echo json_encode($data);
    exit;
}

// Función para manejar errores
function handleError($e) {
    sendResponse(500, ["error" => "Error en la base de datos: " . $e->getMessage()]);
}

// CRUD y joins
try {
    switch ($method) {
        case 'GET':
            if ($table === 'relacionados') {
                if ($id) {
                    // Obtener un inmueble específico con contactos y comentarios
                    $stmt = $pdo->prepare("
                        SELECT 
                            inmuebles.*,
                            contactos.nombre AS contacto_nombre,
                            contactos.telefono AS contacto_telefono,
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
                    if (!$rows) sendResponse(404, ["error" => "Inmueble no encontrado."]);
                    sendResponse(200, formatInmuebleWithComments($rows));
                } else {
                    // Obtener todos los inmuebles con contactos y comentarios
                    $stmt = $pdo->query("
                        SELECT 
                            inmuebles.*,
                            contactos.nombre AS contacto_nombre,
                            contactos.telefono AS contacto_telefono,
                            comentarios.id_comentario,
                            comentarios.comentario AS comentario_texto,
                            comentarios.fecha AS comentario_fecha
                        FROM inmuebles
                        LEFT JOIN contactos ON inmuebles.id_contacto = contactos.id_contacto
                        LEFT JOIN comentarios ON inmuebles.id_inmueble = comentarios.id_inmueble
                    ");
                    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
                    if (!$rows) sendResponse(404, ["error" => "No se encontraron inmuebles."]);
                    sendResponse(200, formatMultipleInmueblesWithComments($rows));
                }
            } else {
                // Obtener registros de una tabla específica (opcionalmente por ID)
                if ($id) {
                    $stmt = $pdo->prepare("SELECT * FROM `$table` WHERE id_" . rtrim($table, 's') . " = :id");
                    $stmt->execute(['id' => $id]);
                    $data = $stmt->fetch(PDO::FETCH_ASSOC);
                    sendResponse(200, $data ?: ["error" => "Registro no encontrado."]);
                } else {
                    $stmt = $pdo->query("SELECT * FROM `$table`");
                    $data = $stmt->fetchAll(PDO::FETCH_ASSOC);
                    sendResponse(200, $data);
                }
            }
            break;

        case 'POST':
            // Crear un nuevo registro
            $input = json_decode(file_get_contents('php://input'), true);
            if (!$input) sendResponse(400, ["error" => "Cuerpo JSON inválido."]);
            $columns = implode(", ", array_keys($input));
            $placeholders = ":" . implode(", :", array_keys($input));
            $stmt = $pdo->prepare("INSERT INTO `$table` ($columns) VALUES ($placeholders)");
            $stmt->execute($input);
            sendResponse(201, ["message" => "Registro creado", "id" => $pdo->lastInsertId()]);
            break;

        case 'PUT':
            // Actualizar un registro existente
            if (!$id) sendResponse(400, ["error" => "ID requerido para actualizar."]);
            $input = json_decode(file_get_contents('php://input'), true);
            if (!$input) sendResponse(400, ["error" => "Cuerpo JSON inválido."]);
            $sets = [];
            foreach ($input as $key => $value) {
                $sets[] = "$key = :$key";
            }
            $stmt = $pdo->prepare("UPDATE `$table` SET " . implode(", ", $sets) . " WHERE id_" . rtrim($table, 's') . " = :id");
            $input['id'] = $id;
            $stmt->execute($input);
            sendResponse(200, ["message" => "Registro actualizado."]);
            break;

            case 'DELETE':
                if ($id) {
                    // Eliminar un registro específico
                    $stmt = $pdo->prepare("DELETE FROM `$table` WHERE id_" . rtrim($table, 's') . " = :id");
                    $stmt->execute(['id' => $id]);
                    sendResponse(200, ["message" => "Registro eliminado."]);
                } else {
                    // Eliminar todos los registros de la tabla si no se especifica un ID
                    $stmt = $pdo->prepare("DELETE FROM `$table`");
                    $stmt->execute();
                    sendResponse(200, ["message" => "Todos los registros de la tabla '$table' han sido eliminados."]);
                }
                break;
        default:
            sendResponse(405, ["error" => "Método no permitido."]);
    }
} catch (PDOException $e) {
    handleError($e);
}

function formatInmuebleWithComments($rows) {
    if (empty($rows)) {
        return [];
    }

    // Inicializar el resultado con todos los campos dinámicamente
    $result = [];
    foreach ($rows[0] as $key => $value) {
        if (!str_starts_with($key, 'contacto_') && !str_starts_with($key, 'comentario_')) {
            $result[$key] = $value;
        }
    }

    // Agregar la información del contacto
    $result['contacto'] = [
        "nombre" => $rows[0]['contacto_nombre'] ?? null,
        "telefono" => $rows[0]['contacto_telefono'] ?? null
    ];

    // Agregar los comentarios
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

function formatMultipleInmueblesWithComments($rows) {
    if (empty($rows)) {
        return [];
    }

    $inmuebles = [];
    foreach ($rows as $row) {
        $id_inmueble = $row['id_inmueble'];

        // Si el inmueble no existe aún, inicialízalo
        if (!isset($inmuebles[$id_inmueble])) {
            $inmuebles[$id_inmueble] = [];
            foreach ($row as $key => $value) {
                if (!str_starts_with($key, 'contacto_') && !str_starts_with($key, 'comentario_')) {
                    $inmuebles[$id_inmueble][$key] = $value;
                }
            }

            // Agregar la información del contacto
            $inmuebles[$id_inmueble]['contacto'] = [
                "nombre" => $row['contacto_nombre'] ?? null,
                "telefono" => $row['contacto_telefono'] ?? null
            ];

            // Inicializar los comentarios como un array vacío
            $inmuebles[$id_inmueble]['comentarios'] = [];
        }

        // Agregar los comentarios
        if (isset($row['id_comentario'])) {
            $inmuebles[$id_inmueble]['comentarios'][] = [
                "id_comentario" => $row['id_comentario'],
                "comentario" => $row['comentario_texto'] ?? null,
                "fecha" => $row['comentario_fecha'] ?? null
            ];
        }
    }

    return array_values($inmuebles);
}
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
    http_response_code(500);
    echo json_encode(["error" => "Error de conexión: " . $e->getMessage()]);
    exit;
}

// Obtener la ruta de la API
$uri = $_SERVER['REQUEST_URI'];
$basePath = '/api/v1/euspay.php';
$path = str_replace($basePath, '', parse_url($uri, PHP_URL_PATH));
$segments = explode('/', trim($path, '/'));

$table = $segments[0] ?? null; // Primera parte: nombre de la tabla
$id = $segments[1] ?? null;    // Segunda parte: ID opcional

// Validar tabla
$validTables = ["inmuebles", "contactos", "comentarios"];
if (!in_array($table, $validTables) && $table !== 'relacionados') {
    sendResponse(400, ["error" => "Tabla no permitida o inexistente."]);
}

// Leer método HTTP
$method = $_SERVER['REQUEST_METHOD'];

// Función para enviar respuestas JSON
function sendResponse($status, $data) {
    http_response_code($status);
    header('Content-Type: application/json');
    echo json_encode($data);
    exit;
}

// Función para manejar errores
function handleError($e) {
    sendResponse(500, ["error" => "Error en la base de datos: " . $e->getMessage()]);
}

// CRUD y operaciones relacionadas con comentarios e inmuebles
try {
    switch ($method) {
        case 'GET':
            if ($table === 'comentarios') {
                if ($id) {
                    // Obtener comentarios para un inmueble específico
                    $stmt = $pdo->prepare("SELECT * FROM comentarios WHERE id_inmueble = :id ORDER BY fecha DESC");
                    $stmt->execute(['id' => $id]);
                    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
                    sendResponse(200, $rows);
                } else {
                    sendResponse(400, ["error" => "ID del inmueble requerido para obtener comentarios."]);
                }
            } elseif ($table === 'relacionados') {
                if ($id) {
                    // Obtener un inmueble específico con contactos y comentarios
                    $stmt = $pdo->prepare("
                        SELECT 
                            inmuebles.*,
                            contactos.nombre AS contacto_nombre,
                            contactos.telefono AS contacto_telefono,
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
                    if (!$rows) sendResponse(404, ["error" => "Inmueble no encontrado."]);
                    sendResponse(200, formatInmuebleWithComments($rows));
                } else {
                    // Obtener todos los inmuebles con contactos y comentarios
                    $stmt = $pdo->query("
                        SELECT 
                            inmuebles.*,
                            contactos.nombre AS contacto_nombre,
                            contactos.telefono AS contacto_telefono,
                            comentarios.id_comentario,
                            comentarios.comentario AS comentario_texto,
                            comentarios.fecha AS comentario_fecha
                        FROM inmuebles
                        LEFT JOIN contactos ON inmuebles.id_contacto = contactos.id_contacto
                        LEFT JOIN comentarios ON inmuebles.id_inmueble = comentarios.id_inmueble
                    ");
                    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
                    if (!$rows) sendResponse(404, ["error" => "No se encontraron inmuebles."]);
                    sendResponse(200, formatMultipleInmueblesWithComments($rows));
                }
            } else {
                // Obtener registros de una tabla específica (opcionalmente por ID)
                if ($id) {
                    $stmt = $pdo->prepare("SELECT * FROM `$table` WHERE id_" . rtrim($table, 's') . " = :id");
                    $stmt->execute(['id' => $id]);
                    $data = $stmt->fetch(PDO::FETCH_ASSOC);
                    sendResponse(200, $data ?: ["error" => "Registro no encontrado."]);
                } else {
                    $stmt = $pdo->query("SELECT * FROM `$table`");
                    $data = $stmt->fetchAll(PDO::FETCH_ASSOC);
                    sendResponse(200, $data);
                }
            }
            break;

        case 'POST':
            if ($table === 'comentarios') {
                // Crear un nuevo comentario
                $input = json_decode(file_get_contents('php://input'), true);
                if (!$input) sendResponse(400, ["error" => "Cuerpo JSON inválido."]);
                $stmt = $pdo->prepare("
                    INSERT INTO comentarios (id_inmueble, comentario, fecha) 
                    VALUES (:id_inmueble, :comentario, :fecha)
                ");
                $stmt->execute([
                    'id_inmueble' => $input['id_inmueble'],
                    'comentario' => $input['comentario'],
                    'fecha' => $input['fecha']
                ]);
                sendResponse(201, [
                    "id_comentario" => $pdo->lastInsertId(),
                    "id_inmueble" => $input['id_inmueble'],
                    "comentario" => $input['comentario'],
                    "fecha" => $input['fecha']
                ]);
            } else {
                // Crear un nuevo registro
                $input = json_decode(file_get_contents('php://input'), true);
                if (!$input) sendResponse(400, ["error" => "Cuerpo JSON inválido."]);
                $columns = implode(", ", array_keys($input));
                $placeholders = ":" . implode(", :", array_keys($input));
                $stmt = $pdo->prepare("INSERT INTO `$table` ($columns) VALUES ($placeholders)");
                $stmt->execute($input);
                sendResponse(201, ["message" => "Registro creado", "id" => $pdo->lastInsertId()]);
            }
            break;

        case 'PUT':
            // Actualizar un registro existente
            if (!$id) sendResponse(400, ["error" => "ID requerido para actualizar."]);
            $input = json_decode(file_get_contents('php://input'), true);
            if (!$input) sendResponse(400, ["error" => "Cuerpo JSON inválido."]);
            $sets = [];
            foreach ($input as $key => $value) {
                $sets[] = "$key = :$key";
            }
            $stmt = $pdo->prepare("UPDATE `$table` SET " . implode(", ", $sets) . " WHERE id_" . rtrim($table, 's') . " = :id");
            $input['id'] = $id;
            $stmt->execute($input);
            sendResponse(200, ["message" => "Registro actualizado."]);
            break;

        case 'DELETE':
            if ($id) {
                // Eliminar un registro específico
                $stmt = $pdo->prepare("DELETE FROM `$table` WHERE id_" . rtrim($table, 's') . " = :id");
                $stmt->execute(['id' => $id]);
                sendResponse(200, ["message" => "Registro eliminado."]);
            } else {
                // Eliminar todos los registros de la tabla si no se especifica un ID
                $stmt = $pdo->prepare("DELETE FROM `$table`");
                $stmt->execute();
                sendResponse(200, ["message" => "Todos los registros de la tabla '$table' han sido eliminados."]);
            }
            break;

        default:
            sendResponse(405, ["error" => "Método no permitido."]);
    }
} catch (PDOException $e) {
    handleError($e);
}

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
        "telefono" => $rows[0]['contacto_telefono'] ?? null
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
                "telefono" => $row['contacto_telefono'] ?? null
            ];

            $inmuebles[$id_inmueble]['comentarios'] = [];
        }

        if (isset($row['id_comentario'])) {
            $inmuebles[$id_inmueble]['comentarios'][] = [
                "id_comentario" => $row['id_comentario'],
                "comentario" => $row['comentario_texto'] ?? null,
                "fecha" => $row['comentario_fecha'] ?? null
            ];
        }
    }

    return array_values($inmuebles);
}
