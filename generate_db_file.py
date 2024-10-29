import sqlite3

# Path to the SQLite database file
db_path = 'bdd_usuarios_membresias.db'

# Path to the SQL script
sql_script_path = './db_generator_script.sql'

# Connect to the SQLite database (this will create the .db file if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Read and execute the SQL script
with open(sql_script_path, 'r') as sql_file:
    sql_script = sql_file.read()
    cursor.executescript(sql_script)

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"Database '{db_path}' has been created and populated with data from '{sql_script_path}'.")