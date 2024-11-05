import sqlite3

usuarios = [(123, "Harry Potter", "Hogwarts", "+5491112223333", "potter@hogwarts.magic"),
            (234, "Indiana Jones", "Estados Unidos", "+5492223334444", "jones@archaic.usa"),
            (345, "Brad Pitt", "Hollywood", "+5493334445555", "contacto@bradpitt.movies"),
            (456, "Isshin Ashina", "Japon", "+5494445556666", "tengu@sekiro.jp"),
            (567, "Franco Colapinto", "Argentina PAPÁ", "+5495556667777", "elmasrapido@formula1.ar")]

membresias = [(1, "Membresia Obligatoria")]

db_path = "bdd_usuarios_membresias.db"

conn =  sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("DELETE FROM usuarios")

for usuario in usuarios:
    sql = f"""INSERT INTO usuarios VALUES
              {str(usuario)[:-1]}, NULL, NULL)"""
    cursor.execute(sql)

for membresia in membresias:
    sql = f"""INSERT INTO membresias VALUES
              {str(membresia)}"""
    cursor.execute(sql)

conn.commit()
conn.close()