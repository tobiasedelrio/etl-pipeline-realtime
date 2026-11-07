import sqlite3
import os

def aplicar_vistas_sql():
    db_path = os.path.join(os.path.dirname(__file__), 'empresa_analytics.db')
    views_path = os.path.join(os.path.dirname(__file__), 'views.sql')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(views_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
        
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    print("✅ Vistas analíticas de Business Intelligence creadas exitosamente.")

if __name__ == "__main__":
    aplicar_vistas_sql()