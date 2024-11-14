import tkinter
from tkinter.constants import *
import modules.usuarios as usuarios

def actualizarCampos(cursor, dni, marco):
    tkinter.Entry().get()
    hijos = marco.children.copy()
    resultado = usuarios.consultaUsuario(cursor, dni)
    
    if resultado != "Usuario inexistente":
        for hijo in hijos:
            if isinstance(marco.children[hijo], tkinter.Entry):


def altaUsuario(conn, cursor, dni, nombre, direccion, telefono, correo):
    resultado = usuarios.altaUsuario(conn, cursor, dni, nombre, direccion, telefono, correo)

    ventana = tkinter.Tk()

    marco = tkinter.Frame(ventana)
    marco.pack()

    mensaje = tkinter.Label(marco)

    if resultado == 0:
        mensaje.configure(text="¡Usuario cargado con éxito!")
    else:
        mensaje.configure(text="Ha habido un error en la carga.")

    mensaje.pack()

def consultaUsuario(cursor, dni, marco):
    hijos = marco.children.copy()
    for hijo in hijos:
        hijos[hijo].destroy()

    resultado = usuarios.consultaUsuario(cursor, dni)
    if resultado != "Usuario inexistente":
        resultado = resultado.split("\n")[:-1]

        campos = []
        for campo in resultado:
            campos.append(campo.split(": ")[1])
        
        for i in range(7):
            texto = tkinter.Label(marco)
            texto.configure(text=f"{campos[i]}")
            texto.grid_configure(column=i, row=1)
    else:
        texto = tkinter.Label(marco)
        texto.configure(text=f"{resultado}")
        texto.pack()

def modificarUsuario(conn, cursor, dni_viejo, dni_nuevo, nombre, direccion, telefono, correo):
    resultado = usuarios.modificarUsuario(conn, cursor, dni_viejo, dni_nuevo, nombre, direccion, telefono, correo)

    ventana = tkinter.Tk()

    marco = tkinter.Frame(ventana)
    marco.pack()

    mensaje = tkinter.Label(marco)

    if resultado == 0:
        mensaje.configure(text="¡Usuario actualizado con éxito!")
    else:
        mensaje.configure(text=f"El usuario con DNI {dni_viejo} no existe.")    

    mensaje.pack()

def eliminarUsuario(conn, cursor, dni):
    resultado = usuarios.bajaUsuario(conn, cursor, dni)

    ventana = tkinter.Tk()
    
    marco = tkinter.Frame(ventana)
    marco.pack()

    mensaje = tkinter.Label(marco)

    if resultado == 0:
        mensaje.configure(text="¡Usuario eliminado con éxito!")
    else:
        mensaje.configure(text=f"El usuario con DNI {dni} no existe.")
    
    mensaje.pack()

def anadirUsr(conn, cursor):
    textos = [["DNI", "Nombre"], ["Dirección", "Teléfono"], ["Correo", None]]
    campos = {}

    ventana = tkinter.Tk()

    marco_principal = tkinter.Frame(ventana)
    marco_principal.pack()

    titulo = tkinter.Label(marco_principal)
    titulo.configure(text="Añadir usuario nuevo")
    titulo.pack()

    marco_entradas = tkinter.Frame(marco_principal)
    marco_entradas.pack()

    for i in range(3):
        for j in range(0, 5, 2):
            if j != 2 and textos[i][int(j>0)] != None:
                texto = tkinter.Label(marco_entradas)
                texto.configure(text=f"{textos[i][int(j>0)]}: ")
                texto.grid_configure(column=j, row=i)

                entrada = tkinter.Entry(marco_entradas)
                entrada.grid_configure(column=j+1, row=i)

                campos[textos[i][int(j>0)]] = entrada
            else:
                separador = tkinter.Label(marco_entradas)
                separador.configure(width=10)
                separador.grid_configure(column=j, row=i)
        
    boton = tkinter.Button(marco_entradas)
    boton.configure(text="Cancelar", command=ventana.destroy)
    boton.grid_configure(column=4, row=2)

    boton = tkinter.Button(marco_entradas)
    boton.configure(text="Aceptar", command= lambda: altaUsuario(conn, cursor,
                                                     int(campos["DNI"].get()),campos["Nombre"].get(),
                                                     campos["Dirección"].get(), campos["Teléfono"].get(),
                                                     campos["Correo"].get()))
    boton.grid_configure(column=5, row=2)

def consultaUsr(cursor):
    textos = ["DNI", "Nombre", "Dirección", "Teléfono", "Correo", "Membresía", "Vencimiento"]

    ventana = tkinter.Tk()

    marco_principal = tkinter.Frame(ventana)
    marco_principal.pack()

    titulo = tkinter.Label(marco_principal)
    titulo.configure(text="Consulta de usuario existente")
    titulo.pack()

    marco_entrada = tkinter.Frame(marco_principal)
    marco_entrada.pack()

    marco_lista = tkinter.Frame(marco_principal)
    marco_lista.pack()

    for i in range(7):
        texto = tkinter.Label(marco_lista)
        texto.configure(text=f"{textos[i]}")
        texto.grid_configure(column=i, row=0)

    marco_resultados = tkinter.Frame(marco_lista)
    marco_resultados.grid_configure(column=0, row=1, columnspan=7)

    texto = tkinter.Label(marco_entrada)
    texto.configure(text="DNI: ")
    texto.grid_configure(column=0, row=0)

    entrada = tkinter.Entry(marco_entrada)
    entrada.grid_configure(column=1, row=0)

    separador = tkinter.Label(marco_entrada)
    separador.configure(width=10)
    separador.grid_configure(column=2, row=0)

    boton = tkinter.Button(marco_entrada)
    boton.configure(text="Consultar", command= lambda: consultaUsuario(cursor, int(entrada.get()),
                                                                       marco_resultados))
    boton.grid_configure(column=3, row=0)

def modificarUsr(conn, cursor):
    textos = [["DNI viejo", "DNI nuevo"], ["Nombre", "Dirección"], ["Teléfono", "Correo"]]
    campos = {}

    ventana = tkinter.Tk()

    marco_principal = tkinter.Frame(ventana)
    marco_principal.pack()

    titulo = tkinter.Label(marco_principal)
    titulo.configure(text="Modificar usuario existente")
    titulo.pack()

    marco_entradas = tkinter.Frame(marco_principal)
    marco_entradas.pack()

    for i in range(3):
        for j in range(0, 5, 2):
            if j != 2:
                texto = tkinter.Label(marco_entradas)
                texto.configure(text=f"{textos[i][int(j>0)]}: ")
                texto.grid_configure(column=j, row=i)

                entrada = tkinter.Entry(marco_entradas)
                entrada.grid_configure(column=j+1, row=i)

                campos[textos[i][int(j>0)]] = entrada
            else:
                separador = tkinter.Label(marco_entradas)
                separador.configure(width=10)
                separador.grid_configure(column=j, row=i)
        
    boton = tkinter.Button(marco_entradas)
    boton.configure(text="Cancelar", command=ventana.destroy)
    boton.grid_configure(column=0, row=3)

    boton = tkinter.Button(marco_entradas)
    boton.configure(text="Buscar datos", command= lambda: actualizarCampos(cursor,
                                                  int(campos["DNI viejo"].get()), marco_entradas))
    boton.grid_configure(column=2, row=3)

    boton = tkinter.Button(marco_entradas)
    boton.configure(text="Aceptar", command= lambda: modificarUsuario(conn, cursor,
                                                     int(campos["DNI viejo"].get()),
                                                     int(campos["DNI nuevo"].get()),campos["Nombre"].get(),
                                                     campos["Dirección"].get(), campos["Teléfono"].get(),
                                                     campos["Correo"].get()))
    boton.grid_configure(column=5, row=3)

def eliminarUsr(conn, cursor):
    ventana = tkinter.Tk()

    marco = tkinter.Frame(ventana)
    marco.pack()

    titulo = tkinter.Label(marco)
    titulo.configure(text="Eliminar usuario existente")
    titulo.pack()

    marco_campos = tkinter.Frame(marco)
    marco_campos.pack()

    texto = tkinter.Label(marco_campos)
    texto.configure(text="DNI: ")
    texto.grid_configure(column=0, row=0)

    entrada = tkinter.Entry(marco_campos)
    entrada.grid_configure(column=1, row=0)

    boton = tkinter.Button(marco_campos)
    boton.configure(text="Cancelar", command=ventana.destroy)
    boton.grid_configure(column=0, row=1)
    
    boton = tkinter.Button(marco_campos)
    boton.configure(text="Aceptar", command= lambda: eliminarUsuario(conn, cursor, int(entrada.get())))
    boton.grid_configure(column=1, row=1)

def main(conn, cursor):
    tk = tkinter.Tk()

    marco_principal = tkinter.Frame(tk)
    marco_principal.pack()

    titulo = tkinter.Label(marco_principal)
    titulo.configure(text="Gestor de usuarios y membresías")
    titulo.pack()

    marco_botones = tkinter.Frame(marco_principal)
    marco_botones.pack()

    boton_añadir = tkinter.Button(marco_botones)
    boton_añadir.configure(text="Añadir usuario", command= lambda: anadirUsr(conn, cursor))
    boton_añadir.grid_configure(column=0, row=0)

    boton_consultar = tkinter.Button(marco_botones)
    boton_consultar.configure(text="Buscar usuario", command= lambda: consultaUsr(cursor))
    boton_consultar.grid_configure(column=1, row=0)

    boton_modificar = tkinter.Button(marco_botones)
    boton_modificar.configure(text="Modificar usuario", command= lambda: modificarUsr(conn, cursor))
    boton_modificar.grid_configure(column=2, row=0)

    boton_eliminar = tkinter.Button(marco_botones)
    boton_eliminar.configure(text="Eliminar usuario", command= lambda: eliminarUsr(conn, cursor))
    boton_eliminar.grid_configure(column=3, row=0)

    tkinter.mainloop()

if __name__ == "__main__":
    conn, cursor = usuarios.inicializar("bdd_usuarios_membresias.db")

    main(conn, cursor)

    conn.close()