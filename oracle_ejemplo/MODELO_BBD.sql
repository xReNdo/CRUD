/*
-- Nombre
-- Atributos: TIPO DE DATO (SQL) (CONSTRAINT)
PERSONAS
EMPLEADO
DEPARTAMENTO
*/

CREATE TABLE PERSONAS (
        id INTEGER PRIMARY KEY,
        rut VARCHAR(8),
        nombres VARCHAR(64),
        apellidos VARCHAR(64),
        fecha_nacimiento DATE
    );

CREATE TABLE DEPARTAMENTO(
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(32),
    fecha_creacion DATE
);

CREATE TABLE EMPLEADO (
        id INTEGER PRIMARY KEY,
        sueldo INTEGER,
        idPersona INTEGER NOT NULL UNIQUE,
        idDepartamento INTEGER NOT NULL,
        FOREIGN KEY (idPersona) REFERENCES PERSONAS(id),
        FOREIGN KEY (idDepartamento) REFERENCES DEPARTAMENTO(id)
    );