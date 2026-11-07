import sqlite3
import os

def inicializar_base_de_datos():
    # Rutas absolutas a los archivos
    db_path = os.path.join(os.path.dirname(__file__), 'empresa_analytics.db')
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    # Conexión a SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Leer y ejecutar el script SQL
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
        
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("✅ Base de datos relacional creada con éxito en: database/empresa_analytics.db")

if __name__ == "__main__":
    inicializar_base_de_datos()