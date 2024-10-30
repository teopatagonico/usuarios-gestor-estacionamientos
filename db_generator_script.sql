CREATE TABLE IF NOT EXISTS membresia (
  id_membresia INT NOT NULL PRIMARY KEY,
  nombre VARCHAR(45) NOT NULL)
-----
CREATE TABLE IF NOT EXISTS usuarios (
  dni INT NOT NULL PRIMARY KEY,
  nombre VARCHAR(45) NOT NULL,
  direccion VARCHAR(45) NOT NULL,
  telefono VARCHAR(45) NOT NULL,
  correo VARCHAR(45) NOT NULL,
  id_membresia INT NULL,
  vencimiento_membresia DATE NULL,
  CONSTRAINT fk_membresia
    FOREIGN KEY (id_membresia)
      REFERENCES mydb.membresia (id_membresia)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION)
-----
CREATE TABLE IF NOT EXISTS estacionamientos (
  id_estacionamiento INT NOT NULL PRIMARY KEY,
  id_ocupante INT NULL,
  CONSTRAINT fk_ocupantes
    FOREIGN KEY (id_ocupante)
      REFERENCES mydb.usuarios (dni)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION)