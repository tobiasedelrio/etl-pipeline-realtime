-- 1. Tabla de Categorías de Productos
CREATE TABLE IF NOT EXISTS categorias (
    categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_categoria VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

-- 2. Tabla de Productos (Dimensión)
CREATE TABLE IF NOT EXISTS productos (
    producto_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    categoria_id INTEGER NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL CHECK(precio_unitario >= 0),
    FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id) ON DELETE CASCADE
);

-- 3. Tabla de Clientes (Dimensión)
CREATE TABLE IF NOT EXISTS clientes (
    cliente_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    pais VARCHAR(50) DEFAULT 'Paraguay',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabla de Transacciones / Ventas (Tabla de Hechos)
CREATE TABLE IF NOT EXISTS ventas (
    venta_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    monto_total DECIMAL(10, 2) NOT NULL,
    fecha_transaccion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado_pago VARCHAR(20) CHECK(estado_pago IN ('Completado', 'Pendiente', 'Fallido')),
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id),
    FOREIGN KEY (producto_id) REFERENCES productos(producto_id)
);

-- 5. Índices para Optimización de Consultas Analíticas
CREATE INDEX IF NOT EXISTS idx_ventas_fecha ON ventas(fecha_transaccion);
CREATE INDEX IF NOT EXISTS idx_ventas_cliente ON ventas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_ventas_producto ON ventas(producto_id);