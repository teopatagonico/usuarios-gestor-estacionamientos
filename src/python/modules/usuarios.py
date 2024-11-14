import sqlite3
import datetime

campos = ["DNI", "Nombre", "Dirección", "Teléfono", "Correo", "Membresía", "Vencimiento"]

def inicializar(ruta):
    conn = sqlite3.connect(ruta)
    cursor = conn.cursor()

    return conn, cursor

def altaUsuario(conn, cursor, dni, nombre, direccion, telefono, correo):
    sql = f"""INSERT INTO usuarios VALUES
              ({dni}, '{nombre}', '{direccion}', '{telefono}', '{correo}',
              NULL, NULL)"""
    
    cursor.execute(sql)
    conn.commit()
    
    return 0

def bajaUsuario(conn, cursor, dni):
    sql = f"""DELETE FROM usuarios WHERE dni={dni}"""

    cursor.execute(sql)
    conn.commit()

    return 0

def modificarUsuario(conn, cursor, dni_viejo, dni_nuevo, nombre, direccion, telefono, correo):
    sql = f"""UPDATE usuarios SET dni={dni_nuevo}, nombre='{nombre}',
              direccion='{direccion}', telefono='{telefono}', correo='{correo}',
              id_membresia=NULL, vencimiento_membresia=NULL WHERE dni={dni_viejo}"""
    
    cursor.execute(sql)
    conn.commit()

    return 0

def consultaUsuario(cursor, dni):
    sql = f"""SELECT * FROM usuarios WHERE dni={dni}"""

    cursor.execute(sql)

    resultado = ""
    for linea in cursor:
        for i in range(7):
            resultado = f"{resultado}{campos[i]}: {linea[i]}\n"
    
    return resultado

def anadirMembresia(conn, cursor, dni, id_membresia, duracion):
    sql = f"""UPDATE usuarios SET id_membresia={id_membresia} WHERE dni={dni}"""
    
    cursor.execute(sql)
    conn.commit()

    renovarMembresia(conn, cursor, dni, duracion)

    return 0

def renovarMembresia(conn, cursor, dni, duracion):
    fecha_actual = datetime.datetime.now()

    año = fecha_actual.year
    mes = fecha_actual.month
    dia = fecha_actual.day
    
    tiempo = duracion
    while tiempo >= 12:
        año = año + 1
        tiempo = tiempo - 12
    
    mes = mes + tiempo
    while mes > 12:
        año = año + 1
        mes = mes - 12

    fecha_nueva = datetime.datetime(año, mes, dia)

    vencimiento = fecha_nueva.isoformat()

    sql = f"""UPDATE usuarios SET vencimiento_membresia='{vencimiento}' WHERE dni={dni}"""
    
    cursor.execute(sql)
    conn.commit()

    return 0

def removerMembresia(conn, cursor, dni):
    sql = f"UPDATE usuarios SET id_membresia = NULL, vencimiento_membresia = NULL WHERE dni={dni}"

    cursor.execute(sql)
    conn.commit()

    return 0