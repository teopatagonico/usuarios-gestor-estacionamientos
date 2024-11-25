import sqlite3

campos = ["ID", "Nombre"]

def idValido(id):
    return id > 0

def nombreValido(nombre):
    return nombre != ""

def parametroValido(parametro, tipo):

    if tipo == "id":
        valido = idValido(parametro)
    
    else:
        valido = nombreValido(parametro)

    return valido

def parametrosAltaValidos(id_membresia, nombre):

    id_valido = parametroValido(id_membresia, "id")
    nombre_valido = parametroValido(nombre, "nombre")

    return id_valido and nombre_valido

def existeMembresia(cursor, id_membresia):

    sql = f"SELECT * FROM membresias WHERE id_membresia = {id_membresia}"
    cursor.execute(sql)

    resultado = ""
    for linea in cursor:
        resultado = resultado + str(linea)

    existe = resultado != ""

    return existe

def inicializar(ruta):

    conn = sqlite3.connect(ruta)
    cursor = conn.cursor()

    return conn, cursor

def altaMembresia(conn, cursor, id_membresia, nombre):

    if parametrosAltaValidos(id_membresia, nombre):
        sql = f"""INSERT INTO membresias VALUES
                ({id_membresia}, '{nombre}')"""
        
        cursor.execute(sql)
        conn.commit()

        resultado = 0

    else:
        resultado = 1
        
    return resultado

def bajaMembresia(conn, cursor, id_membresia):

    if existeMembresia(cursor, id_membresia):
        sql = f"""DELETE FROM membresias WHERE id_membresia = {id_membresia}"""

        cursor.execute(sql)
        conn.commit()

        resultado = 0

    else:
        resultado = 1

    return resultado

def modificarMembresia(conn, cursor, id_viejo, id_nuevo, nombre):

    if existeMembresia(cursor, id_viejo) and parametrosAltaValidos(id_nuevo, nombre):
        sql = f"""UPDATE membresias SET id_membresia = {id_nuevo}, nombre = {nombre}
                  WHERE id_membresia = {id_viejo}"""
        
        cursor.execute(sql)
        conn.commit()
        
        resultado = 0

    else:
        resultado = 1

    return resultado

def consultaMembresia(cursor, id_membresia):
    
    if existeMembresia(cursor, id_membresia):
        sql = f"""SELECT * FROM membresias WHERE id_membresia = {id_membresia}"""
        
        cursor.execute(sql)

        resultado = ""
        for linea in cursor:
            for i in range(2):
                resultado = f"{resultado}{campos[i]}: {linea[i]}\n"
    
    else:
        resultado = "Membresía inexistente"
    
    return resultado