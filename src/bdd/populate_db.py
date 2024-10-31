import sqlite3

usuarios = ((123, "Harry Potter", "Hogwarts", "+00112233", "potter@hogwarts.magic"),
            (234, "Indiana Jones", "Estados Unidos", "+11223344", "jones@archaic.usa"),
            (345, "Brad Pitt", "Hollywood", "+22334455", "contacto@bradpitt.movies"),
            (456, "Isshin Ashina", "Japon", "+33445566", "tengu@sekiro.jp"),
            (567, "Franco Colapinto", "Argentina PAPÁ", "+44556677", "elmasrapido@formula1.ar"))

db_path = "bdd_usuarios_membresias.db"

conn =  sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("DELETE FROM usuarios")

for usuario in usuarios:
    sql = f"""INSERT INTO usuarios VALUES
              {str(usuario)[:-1]}, NULL, NULL)"""
    cursor.execute(sql)

conn.commit()
conn.close()