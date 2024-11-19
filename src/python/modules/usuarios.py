import sqlite3
import datetime

try:
    import membresias as membresias
except ImportError:
    import modules.membresias as membresias

campos = ["DNI", "Nombre", "Dirección", "Teléfono", "Correo", "Membresía", "Vencimiento"]

def numeroValido(numero):
    return numero > 0 and len(str(numero)) <=8

def telefonoValido(telefono):
    return len(telefono) == 14 and telefono[0:4] == "+549"

def correoValido(correo):

    valido = False

    try:
        direccion, dominio = correo.split("@")

        try:
            nombre_dominio, extension = dominio.split(".")
            valido = direccion != "" and nombre_dominio != "" and extension != ""

        except ValueError:
            pass

    except ValueError:
        pass

    return valido

def parametroValido(parametro, tipo):

    if tipo == "int":
        valido = numeroValido(parametro)

    elif tipo == "telefono":
        valido = telefonoValido(parametro)

    elif tipo == "correo":
        valido = correoValido(parametro)

    else:
        valido = parametro != ""

    return valido

def parametrosAltaValidos(dni, nombre, direccion, telefono, correo):

    dni_valido = parametroValido(dni, "int")
    nombre_valido = parametroValido(nombre, "nombre")
    direccion_valida = parametroValido(direccion, "direccion")
    telefono_valido = parametroValido(telefono, "telefono")
    correo_valido = parametroValido(correo, "correo")

    if not dni_valido:
        parametros_validos = 1
    elif not nombre_valido:
        parametros_validos = 2
    elif not direccion_valida:
        parametros_validos = 3
    elif not telefono_valido:
        parametros_validos = 4
    elif not correo_valido:
        parametros_validos = 5
    else:
        parametros_validos = 0
    
    return parametros_validos

def existeUsuario(cursor, dni):

    sql = f"SELECT * FROM usuarios WHERE dni={dni}"
    cursor.execute(sql)

    resultado = ""
    for linea in cursor:
        resultado = resultado + str(linea)

    if resultado != "":
        existe = 0

    else:
        existe = 1

    return existe

def tieneMembresia(cursor, dni):

    if existeUsuario(cursor, dni):
        sql = f"SELECT * FROM usuarios WHERE dni={dni}"

        cursor.execute(sql)
        for linea in cursor:
            membresia = linea[5]
        
        resultado = membresia != None
    
    else:
        resultado = False

    return resultado

def inicializar(ruta):

    conn = sqlite3.connect(ruta)
    cursor = conn.cursor()

    return conn, cursor

def altaUsuario(conn, cursor, dni, nombre, direccion, telefono, correo):

    resultado = parametrosAltaValidos(dni, nombre, direccion, telefono, correo)

    if resultado == 0:
        sql = f"""INSERT INTO usuarios VALUES
                ({dni}, '{nombre}', '{direccion}', '{telefono}', '{correo}',
                NULL, NULL)"""
        
        cursor.execute(sql)
        conn.commit()
    
    return resultado

def bajaUsuario(conn, cursor, dni):
    
    if existeUsuario(cursor, dni) == 0:    
        sql = f"""DELETE FROM usuarios WHERE dni={dni}"""

        cursor.execute(sql)
        conn.commit()

        resultado = 0

    else:
        resultado = 1
    
    return resultado

def modificarUsuario(conn, cursor, dni_viejo, dni_nuevo, nombre, direccion, telefono, correo):
    
    resultado = existeUsuario(cursor, dni_viejo)

    if resultado == 0:
        resultado = parametrosAltaValidos(dni_nuevo, nombre, direccion, telefono, correo)

        if resultado == 0:

            sql = f"""UPDATE usuarios SET dni={dni_nuevo}, nombre='{nombre}',
                    direccion='{direccion}', telefono='{telefono}', correo='{correo}',
                    id_membresia=NULL, vencimiento_membresia=NULL WHERE dni={dni_viejo}"""
            
            cursor.execute(sql)
            conn.commit()

        else:
            resultado = resultado + 1
   
    return resultado

def consultaUsuario(cursor, dni):

    if existeUsuario(cursor, dni) == 0:
        sql = f"""SELECT * FROM usuarios WHERE dni={dni}"""

        cursor.execute(sql)

        resultado = ""
        for linea in cursor:
            for i in range(7):
                resultado = f"{resultado}{campos[i]}: {linea[i]}\n"

    else:
        resultado = "Usuario inexistente"

    return resultado

def anadirMembresia(conn, cursor, dni, id_membresia, duracion):

    resultado = existeUsuario(cursor, dni)

    if resultado == 0:
        resultado = membresias.existeMembresia(cursor, id_membresia)
        
        if resultado:
            sql = f"""UPDATE usuarios SET id_membresia={id_membresia} WHERE dni={dni}"""
            
            cursor.execute(sql)
            conn.commit()

            renovarMembresia(conn, cursor, dni, duracion)
    
    return resultado

def renovarMembresia(conn, cursor, dni, duracion):

    if tieneMembresia(cursor, dni) and parametroValido(duracion, "int"):
        meses_30_dias = [4, 6, 9, 11]
        sql = f"SELECT * FROM usuarios WHERE dni={dni}"

        cursor.execute(sql)

        vencimiento_texto = ""
        for linea in cursor:
            if linea[6] != None:
                vencimiento_texto = vencimiento_texto + linea[6]

            else:
                vencimiento_texto = datetime.datetime.now().isoformat()
        
        vencimiento = datetime.datetime.fromisoformat(vencimiento_texto)

        fecha_actual = datetime.datetime.now()
        
        if fecha_actual >= vencimiento:

            año = fecha_actual.year
            mes = fecha_actual.month
            dia = fecha_actual.day
            
            tiempo = duracion
            while tiempo >= 12:
                año_= año + 1
                tiempo = tiempo - 12
            
            mes = mes + tiempo
            while mes > 12:
                año = año + 1
                mes = mes - 12

            if mes == 2:
                dia_maximo = 28

            elif mes in meses_30_dias:
                dia_maximo = 30

            else:
                dia_maximo = 31
            
            while dia > dia_maximo:
                mes = mes + 1
                dia = dia - dia_maximo

            fecha_nueva = datetime.datetime(año, mes, dia)

            vencimiento = fecha_nueva.isoformat()

            sql = f"""UPDATE usuarios SET vencimiento_membresia='{vencimiento}' WHERE dni={dni}"""
            
            cursor.execute(sql)
            conn.commit()
            resultado = 0

        else:
            resultado = 2
    else:
        resultado = 1
    return resultado

def removerMembresia(conn, cursor, dni):

    if tieneMembresia(cursor, dni):
        sql = f"UPDATE usuarios SET id_membresia = NULL, vencimiento_membresia = NULL WHERE dni={dni}"

        cursor.execute(sql)
        conn.commit()
        
        resultado = 0

    else:
        resultado = 1

    return resultado