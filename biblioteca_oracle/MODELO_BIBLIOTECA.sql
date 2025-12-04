/* ============================
   TABLA: USUARIOS
   ============================ */

CREATE TABLE USUARIOS (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR2(100),
    rut VARCHAR2(12),
    correo VARCHAR2(100),
    tipo_usuario VARCHAR2(20)   -- ESTUDIANTE / DOCENTE / INVESTIGADOR
);


/* ============================
   TABLA: LIBROS
   ============================ */

CREATE TABLE LIBROS (
    id INTEGER PRIMARY KEY,
    titulo VARCHAR2(150),
    autor VARCHAR2(100),
    anio_publicacion INTEGER
);


/* ============================
   TABLA: PRESTAMOS
   ============================ */

CREATE TABLE PRESTAMOS (
    id INTEGER PRIMARY KEY,
    idUsuario INTEGER NOT NULL,
    idLibro INTEGER NOT NULL,
    fecha_prestamo DATE,
    fecha_devolucion DATE,
    FOREIGN KEY (idUsuario) REFERENCES USUARIOS(id),
    FOREIGN KEY (idLibro) REFERENCES LIBROS(id)
);
