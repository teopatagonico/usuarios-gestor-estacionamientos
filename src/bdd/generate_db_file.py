import sqlite3

# Nombre de la BDD
db_path = 'bdd_usuarios_membresias.db'

# Nombre del script de SQL
sql_script_path = './src/bdd/db_generator_script.sql'

# Conectar a la BDD (si no existe es creada)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Leer el script SQL
with open(sql_script_path, 'r') as sql_file:
    sql_script = sql_file.read()

# Separar las instrucciones del script SQL
sql_script = sql_script.split("-----")

# Ejecutar las instrucciones del script SQL
for instruccion in sql_script:
    cursor.execute(instruccion)

# Confirmar cambios y cerrar la conexion
conn.commit()
conn.close()