-- 1. Vista Analítica: Rendimiento de Ventas por Categoría de Producto
CREATE VIEW IF NOT EXISTS vw_ventas_por_categoria AS
SELECT 
    c.nombre_categoria AS Categoria,
    COUNT(v.venta_id) AS Total_Transacciones,
    SUM(v.cantidad) AS Unidades_Vendidas,
    ROUND(SUM(v.monto_total), 2) AS Facturacion_Total,
    ROUND(AVG(v.monto_total), 2) AS Ticket_Promedio
FROM ventas v
JOIN productos p ON v.producto_id = p.producto_id
JOIN categorias c ON p.categoria_id = c.categoria_id
WHERE v.estado_pago = 'Completado'
GROUP BY c.nombre_categoria
ORDER BY Facturacion_Total DESC;

-- 2. Vista Analítica: Métricas Clientes y Tasa de Éxito de Transacciones
CREATE VIEW IF NOT EXISTS vw_metricas_clientes AS
SELECT 
    cl.nombre AS Cliente,
    cl.pais AS Pais,
    COUNT(v.venta_id) AS Total_Pedidos,
    ROUND(SUM(CASE WHEN v.estado_pago = 'Completado' THEN v.monto_total ELSE 0 END), 2) AS Total_Gasto_Efectivo,
    ROUND(COUNT(CASE WHEN v.estado_pago = 'Fallido' THEN 1 END) * 100.0 / COUNT(v.venta_id), 2) AS Porcentaje_Fallos
FROM clientes cl
LEFT JOIN ventas v ON cl.cliente_id = v.cliente_id
GROUP BY cl.cliente_id, cl.nombre, cl.pais;

-- 3. Vista Analítica: KPI General Diario
CREATE VIEW IF NOT EXISTS vw_kpis_generales AS
SELECT 
    DATE(v.fecha_transaccion) AS Fecha,
    COUNT(v.venta_id) AS Total_Operaciones,
    ROUND(SUM(v.monto_total), 2) AS Ingresos_Brutos,
    ROUND(SUM(CASE WHEN v.estado_pago = 'Completado' THEN v.monto_total ELSE 0 END), 2) AS Ingresos_Netos
FROM ventas v
GROUP BY DATE(v.fecha_transaccion);