import sqlite3
import pandas as pd
import requests
import random
from datetime import datetime
import os

# Ruta de la base de datos relacional
DB_PATH = os.path.join(os.path.dirname(__file__), '../database/empresa_analytics.db')

def obtener_datos_api():
    """1. EXTRACT: Captura datos de catálogo desde una API REST en tiempo real"""
    print("📥 [1/3] Obteniendo catálogo desde la API (DummyJSON Products)...")
    url = "https://dummyjson.com/products?limit=10"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['products']
    except Exception as e:
        print(f"⚠️ Error al conectar con la API: {e}")
        return []

def poblar_catalogos_iniciales(productos_api, conn):
    """Inserta Categorías, Productos y Clientes base respetando claves relacionales"""
    cursor = conn.cursor()
    
    # Categorías y Productos de la API
    for prod in productos_api:
        cat_nombre = prod['category'].capitalize()
        cursor.execute("INSERT OR IGNORE INTO categorias (nombre_categoria, descripcion) VALUES (?, ?)", 
                       (cat_nombre, f"Categoría de {cat_nombre}"))
        
        cursor.execute("SELECT categoria_id FROM categorias WHERE nombre_categoria = ?", (cat_nombre,))
        cat_id = cursor.fetchone()[0]
        
        sku = f"PROD-{prod['id']:04d}"
        cursor.execute("""
            INSERT OR IGNORE INTO productos (sku, nombre, categoria_id, precio_unitario) 
            VALUES (?, ?, ?, ?)
        """, (sku, prod['title'], cat_id, prod['price']))
        
    # Clientes de prueba
    clientes_demo = [
        ("Carlos Benítez", "carlos.b@empresa.py", "Paraguay"),
        ("María González", "maria.g@empresa.py", "Paraguay"),
        ("Juan Valdez", "jvaldez@empresa.com", "Argentina"),
        ("Ana Silva", "ana.silva@empresa.py", "Paraguay"),
        ("Lucas Ferreira", "lferreira@empresa.br", "Brasil")
    ]
    for cliente in clientes_demo:
        cursor.execute("INSERT OR IGNORE INTO clientes (nombre, email, pais) VALUES (?, ?, ?)", cliente)
        
    conn.commit()

def transformar_y_cargar_ventas(conn):
    """2 & 3. TRANSFORM & LOAD: Genera lote de transacciones, valida con Pandas y carga en BD"""
    print("⚙️ [2/3] Transformando y validando transacciones relacionales...")
    
    df_clientes = pd.read_sql_query("SELECT cliente_id FROM clientes", conn)
    df_productos = pd.read_sql_query("SELECT producto_id, precio_unitario FROM productos", conn)
    
    if df_clientes.empty or df_productos.empty:
        print("⚠️ Catálogos vacíos. No se pueden procesar ventas.")
        return

    lote_transacciones = []
    estados = ['Completado', 'Completado', 'Completado', 'Pendiente', 'Fallido']
    
    for _ in range(15):
        cliente_id = int(random.choice(df_clientes['cliente_id'].values))
        prod_row = df_productos.sample(1).iloc[0]
        producto_id = int(prod_row['producto_id'])
        precio = float(prod_row['precio_unitario'])
        cantidad = random.randint(1, 5)
        monto_total = round(precio * cantidad, 2)
        estado = random.choice(estados)
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        lote_transacciones.append({
            'cliente_id': cliente_id,
            'producto_id': producto_id,
            'cantidad': cantidad,
            'monto_total': monto_total,
            'fecha_transaccion': fecha_actual,
            'estado_pago': estado
        })
        
    df_ventas = pd.DataFrame(lote_transacciones)
    
    # Limpieza: eliminar registros con montos no válidos
    df_ventas = df_ventas[df_ventas['monto_total'] > 0]
    
    print("🚀 [3/3] Cargando transacciones limpias en la tabla de Hechos (ventas)...")
    df_ventas.to_sql('ventas', conn, if_exists='append', index=False)
    print(f"✅ Se procesaron e insertaron {len(df_ventas)} transacciones con éxito.")

def ejecutar_pipeline():
    conn = sqlite3.connect(DB_PATH)
    try:
        productos_api = obtener_datos_api()
        poblar_catalogos_iniciales(productos_api, conn)
        transformar_y_cargar_ventas(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    ejecutar_pipeline()