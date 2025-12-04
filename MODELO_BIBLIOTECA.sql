CREATE TABLE USUARIOS (
    id NUMBER PRIMARY KEY,
    nombre VARCHAR2(100),
    rut VARCHAR2(12),
    correo VARCHAR2(120),
    tipo VARCHAR2(20) -- ESTUDIANTE, DOCENTE, INVESTIGADOR
);

CREATE TABLE ESTUDIANTES (
    idUsuario NUMBER PRIMARY KEY,
    carrera VARCHAR2(100),
    anio_ingreso NUMBER,
    FOREIGN KEY (idUsuario) REFERENCES USUARIOS(id)
);

CREATE TABLE DOCENTES (
    idUsuario NUMBER PRIMARY KEY,
    departamento VARCHAR2(100),
    asignaturas VARCHAR2(255),
    FOREIGN KEY (idUsuario) REFERENCES USUARIOS(id)
);

CREATE TABLE INVESTIGADORES (
    idUsuario NUMBER PRIMARY KEY,
    num_publicaciones NUMBER,
    area_investigacion VARCHAR2(255),
    FOREIGN KEY (idUsuario) REFERENCES USUARIOS(id)
);

CREATE TABLE LIBROS (
    id NUMBER PRIMARY KEY,
    titulo VARCHAR2(150),
    autor VARCHAR2(100),
    genero VARCHAR2(50),
    editorial VARCHAR2(100),
    disponible NUMBER(1)
);

CREATE TABLE PRESTAMOS (
    id NUMBER PRIMARY KEY,
    idUsuario NUMBER NOT NULL,
    idLibro NUMBER NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE,
    estado VARCHAR2(20),
    FOREIGN KEY (idUsuario) REFERENCES USUARIOS(id),
    FOREIGN KEY (idLibro) REFERENCES LIBROS(id)
);
