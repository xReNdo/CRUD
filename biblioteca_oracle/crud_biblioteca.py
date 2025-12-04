from datetime import datetime
import oracledb
import os
from dotenv import load_dotenv
from typing import Optional

# Cargar variables de entorno (.env)
load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")


def get_connection():
    """Retorna una conexión a la base de datos Oracle."""
    return oracledb.connect(user=username, password=password, dsn=dsn)


# ---------------------------------------------------------------------------
# CREACIÓN DE TABLAS
# ---------------------------------------------------------------------------

def create_schema(query: str):
    """Ejecuta una sentencia de creación de tabla."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                print(f"Tabla creada:\n{query}\n")
    except oracledb.DatabaseError as error:
        print(f"No se pudo crear la tabla: {error}")


def create_all_tables():
    """Crea todas las tablas del sistema de biblioteca."""
    tables = [
        # Tabla USUARIOS
        (
            "CREATE TABLE USUARIOS ("
            "id INTEGER PRIMARY KEY,"
            "nombre VARCHAR2(100),"
            "rut VARCHAR2(12),"
            "correo VARCHAR2(100),"
            "tipo_usuario VARCHAR2(20)"
            ")"
        ),
        # Tabla LIBROS
        (
            "CREATE TABLE LIBROS ("
            "id INTEGER PRIMARY KEY,"
            "titulo VARCHAR2(150),"
            "autor VARCHAR2(100),"
            "anio_publicacion INTEGER"
            ")"
        ),
        # Tabla PRESTAMOS
        (
            "CREATE TABLE PRESTAMOS ("
            "id INTEGER PRIMARY KEY,"
            "idUsuario INTEGER NOT NULL,"
            "idLibro INTEGER NOT NULL,"
            "fecha_prestamo DATE,"
            "fecha_devolucion DATE,"
            "FOREIGN KEY (idUsuario) REFERENCES USUARIOS(id),"
            "FOREIGN KEY (idLibro) REFERENCES LIBROS(id)"
            ")"
        ),
    ]

    for query in tables:
        create_schema(query)


# ---------------------------------------------------------------------------
# CRUD USUARIOS
# ---------------------------------------------------------------------------

def create_usuario(
    id: int,
    nombre: str,
    rut: str,
    correo: str,
    tipo_usuario: str,
):
    sql = (
        "INSERT INTO USUARIOS (id,nombre,rut,correo,tipo_usuario) "
        "VALUES (:id,:nombre,:rut,:correo,:tipo_usuario)"
    )

    parametros = {
        "id": id,
        "nombre": nombre,
        "rut": rut,
        "correo": correo,
        "tipo_usuario": tipo_usuario.upper(),
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
            connection.commit()
            print("Inserción de usuario correcta.")
    except oracledb.DatabaseError as error:
        print(f"No se pudo insertar el usuario\n{error}\n{sql}\n{parametros}")


def read_usuarios():
    sql = "SELECT * FROM USUARIOS"
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql)
                for fila in cursor.execute(sql):
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"No se pudo ejecutar la query\n{error}\n{sql}")


def read_usuario_by_id(id: int):
    sql = "SELECT * FROM USUARIOS WHERE id = :id"
    parametros = {"id": id}
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql, parametros)
                resultados = cursor.execute(sql, parametros)
                encontrado = False
                for fila in resultados:
                    print(fila)
                    encontrado = True
                if not encontrado:
                    print(f"No hay usuarios con ID {id}")
    except oracledb.DatabaseError as error:
        print(f"No se pudo ejecutar la query\n{error}\n{sql}\n{parametros}")


def update_usuario(
    id: int,
    nombre: Optional[str] = None,
    rut: Optional[str] = None,
    correo: Optional[str] = None,
    tipo_usuario: Optional[str] = None,
):
    modificaciones = []
    parametros: dict = {"id": id}

    if nombre is not None:
        modificaciones.append("nombre = :nombre")
        parametros["nombre"] = nombre
    if rut is not None:
        modificaciones.append("rut = :rut")
        parametros["rut"] = rut
    if correo is not None:
        modificaciones.append("correo = :correo")
        parametros["correo"] = correo
    if tipo_usuario is not None:
        modificaciones.append("tipo_usuario = :tipo_usuario")
        parametros["tipo_usuario"] = tipo_usuario.upper()

    if not modificaciones:
        return print("No has enviado datos por modificar")

    sql = f"UPDATE USUARIOS SET {', '.join(modificaciones)} WHERE id = :id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Usuario con ID={id} actualizado.")


def delete_usuario(id: int):
    sql = "DELETE FROM USUARIOS WHERE id = :id"
    parametros = {"id": id}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Usuario eliminado\n{parametros}")
    except oracledb.DatabaseError as e:
        print(f"Error al eliminar usuario: {e}\n{sql}\n{parametros}")


# ---------------------------------------------------------------------------
# CRUD LIBROS
# ---------------------------------------------------------------------------

def create_libro(
    id: int,
    titulo: str,
    autor: str,
    anio_publicacion: int,
):
    sql = (
        "INSERT INTO LIBROS (id,titulo,autor,anio_publicacion) "
        "VALUES (:id,:titulo,:autor,:anio_publicacion)"
    )

    parametros = {
        "id": id,
        "titulo": titulo,
        "autor": autor,
        "anio_publicacion": anio_publicacion,
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
            connection.commit()
            print("Inserción de libro correcta.")
    except oracledb.DatabaseError as error:
        print(f"No se pudo insertar el libro\n{error}\n{sql}\n{parametros}")


def read_libros():
    sql = "SELECT * FROM LIBROS"
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql)
                for fila in cursor.execute(sql):
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"No se pudo ejecutar la query\n{error}\n{sql}")


def read_libro_by_id(id: int):
    sql = "SELECT * FROM LIBROS WHERE id = :id"
    parametros = {"id": id}
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql, parametros)
                resultados = cursor.execute(sql, parametros)
                encontrado = False
                for fila in resultados:
                    print(fila)
                    encontrado = True
                if not encontrado:
                    print(f"No hay libros con ID {id}")
    except oracledb.DatabaseError as error:
        print(f"No se pudo ejecutar la query\n{error}\n{sql}\n{parametros}")


def update_libro(
    id: int,
    titulo: Optional[str] = None,
    autor: Optional[str] = None,
    anio_publicacion: Optional[int] = None,
):
    modificaciones = []
    parametros: dict = {"id": id}

    if titulo is not None:
        modificaciones.append("titulo = :titulo")
        parametros["titulo"] = titulo
    if autor is not None:
        modificaciones.append("autor = :autor")
        parametros["autor"] = autor
    if anio_publicacion is not None:
        modificaciones.append("anio_publicacion = :anio_publicacion")
        parametros["anio_publicacion"] = anio_publicacion

    if not modificaciones:
        return print("No has enviado datos por modificar")

    sql = f"UPDATE LIBROS SET {', '.join(modificaciones)} WHERE id = :id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Libro con ID={id} actualizado.")


def delete_libro(id: int):
    sql = "DELETE FROM LIBROS WHERE id = :id"
    parametros = {"id": id}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Libro eliminado\n{parametros}")
    except oracledb.DatabaseError as e:
        print(f"Error al eliminar libro: {e}\n{sql}\n{parametros}")


# ---------------------------------------------------------------------------
# CRUD PRESTAMOS
# ---------------------------------------------------------------------------

def create_prestamo(
    id: int,
    idUsuario: int,
    idLibro: int,
    fecha_prestamo: str,
    fecha_devolucion: Optional[str],
):
    sql = (
        "INSERT INTO PRESTAMOS ("
        "id,idUsuario,idLibro,fecha_prestamo,fecha_devolucion"
        ") VALUES ("
        ":id,:idUsuario,:idLibro,:fecha_prestamo,:fecha_devolucion"
        ")"
    )

    parametros = {
        "id": id,
        "idUsuario": idUsuario,
        "idLibro": idLibro,
        "fecha_prestamo": datetime.strptime(fecha_prestamo, "%d-%m-%Y"),
        "fecha_devolucion": (
            datetime.strptime(fecha_devolucion, "%d-%m-%Y")
            if fecha_devolucion and fecha_devolucion.strip()
            else None
        ),
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
            connection.commit()
            print("Inserción de préstamo correcta.")
    except oracledb.DatabaseError as error:
        print(f"No se pudo insertar el préstamo\n{error}\n{sql}\n{parametros}")


def read_prestamos():
    sql = "SELECT * FROM PRESTAMOS"
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql)
                for fila in cursor.execute(sql):
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"No se pudo ejecutar la query\n{error}\n{sql}")


def read_prestamo_by_id(id: int):
    sql = "SELECT * FROM PRESTAMOS WHERE id = :id"
    parametros = {"id": id}
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql, parametros)
                resultados = cursor.execute(sql, parametros)
                encontrado = False
                for fila in resultados:
                    print(fila)
                    encontrado = True
                if not encontrado:
                    print(f"No hay préstamos con ID {id}")
    except oracledb.DatabaseError as error:
        print(f"No se pudo ejecutar la query\n{error}\n{sql}\n{parametros}")


def update_prestamo(
    id: int,
    idUsuario: Optional[int] = None,
    idLibro: Optional[int] = None,
    fecha_prestamo: Optional[str] = None,
    fecha_devolucion: Optional[str] = None,
):
    modificaciones = []
    parametros: dict = {"id": id}

    if idUsuario is not None:
        modificaciones.append("idUsuario = :idUsuario")
        parametros["idUsuario"] = idUsuario
    if idLibro is not None:
        modificaciones.append("idLibro = :idLibro")
        parametros["idLibro"] = idLibro
    if fecha_prestamo is not None:
        modificaciones.append("fecha_prestamo = :fecha_prestamo")
        parametros["fecha_prestamo"] = datetime.strptime(
            fecha_prestamo, "%d-%m-%Y"
        )
    if fecha_devolucion is not None:
        modificaciones.append("fecha_devolucion = :fecha_devolucion")
        parametros["fecha_devolucion"] = datetime.strptime(
            fecha_devolucion, "%d-%m-%Y"
        )

    if not modificaciones:
        return print("No has enviado datos por modificar")

    sql = f"UPDATE PRESTAMOS SET {', '.join(modificaciones)} WHERE id = :id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Préstamo con ID={id} actualizado.")


def delete_prestamo(id: int):
    sql = "DELETE FROM PRESTAMOS WHERE id = :id"
    parametros = {"id": id}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Préstamo eliminado\n{parametros}")
    except oracledb.DatabaseError as e:
        print(f"Error al eliminar préstamo: {e}\n{sql}\n{parametros}")


# ---------------------------------------------------------------------------
# MENÚS
# ---------------------------------------------------------------------------

def menu_usuarios():
    while True:
        os.system("cls")
        print(
            """
                ====================================
                |         Menú: Usuarios           |
                |----------------------------------|
                | 1. Insertar un usuario           |
                | 2. Consultar todos los usuarios  |
                | 3. Consultar usuario por ID      |
                | 4. Modificar un usuario          |
                | 5. Eliminar un usuario           |
                | 0. Volver al menú principal      |
                ====================================
            """
        )
        opcion = input("Elige una opción [1-5, 0]: ")

        if opcion == "1":
            os.system("cls")
            print("1. Insertar un usuario")
            id = input("ID usuario: ")
            nombre = input("Nombre: ")
            rut = input("RUT: ")
            correo = input("Correo: ")
            tipo = input("Tipo de usuario (ESTUDIANTE/DOCENTE/INVESTIGADOR): ")
            create_usuario(id, nombre, rut, correo, tipo)
            input("Ingrese ENTER para continuar...")
        elif opcion == "2":
            os.system("cls")
            print("2. Consultar todos los usuarios")
            read_usuarios()
            input("Ingrese ENTER para continuar...")
        elif opcion == "3":
            os.system("cls")
            print("3. Consultar usuario por ID")
            id = input("ID usuario: ")
            read_usuario_by_id(id)
            input("Ingrese ENTER para continuar...")
        elif opcion == "4":
            os.system("cls")
            print("4. Modificar un usuario")
            id = input("ID usuario: ")
            print("[Sólo ingrese los datos a modificar, deje vacío los que no quiera cambiar]")
            nombre = input("Nombre (opcional): ")
            rut = input("RUT (opcional): ")
            correo = input("Correo (opcional): ")
            tipo = input("Tipo de usuario (opcional): ")

            if len(nombre.strip()) == 0:
                nombre = None
            if len(rut.strip()) == 0:
                rut = None
            if len(correo.strip()) == 0:
                correo = None
            if len(tipo.strip()) == 0:
                tipo = None

            update_usuario(id, nombre, rut, correo, tipo)
            input("Ingrese ENTER para continuar...")
        elif opcion == "5":
            os.system("cls")
            print("5. Eliminar un usuario")
            id = input("ID usuario: ")
            delete_usuario(id)
            input("Ingrese ENTER para continuar...")
        elif opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal...")
            break
        else:
            os.system("cls")
            print("Opción incorrecta, intente nuevamente.")
            input("Ingrese ENTER para continuar...")


def menu_libros():
    while True:
        os.system("cls")
        print(
            """
                ====================================
                |          Menú: Libros            |
                |----------------------------------|
                | 1. Insertar un libro             |
                | 2. Consultar todos los libros    |
                | 3. Consultar libro por ID        |
                | 4. Modificar un libro            |
                | 5. Eliminar un libro             |
                | 0. Volver al menú principal      |
                ====================================
            """
        )
        opcion = input("Elige una opción [1-5, 0]: ")

        if opcion == "1":
            os.system("cls")
            print("1. Insertar un libro")
            id = input("ID libro: ")
            titulo = input("Título: ")
            autor = input("Autor: ")
            anio_str = input("Año de publicación: ")
            anio = int(anio_str) if anio_str.strip() else None
            create_libro(id, titulo, autor, anio)
            input("Ingrese ENTER para continuar...")
        elif opcion == "2":
            os.system("cls")
            print("2. Consultar todos los libros")
            read_libros()
            input("Ingrese ENTER para continuar...")
        elif opcion == "3":
            os.system("cls")
            print("3. Consultar libro por ID")
            id = input("ID libro: ")
            read_libro_by_id(id)
            input("Ingrese ENTER para continuar...")
        elif opcion == "4":
            os.system("cls")
            print("4. Modificar un libro")
            id = input("ID libro: ")
            print("[Sólo ingrese los datos a modificar, deje vacío los que no quiera cambiar]")
            titulo = input("Título (opcional): ")
            autor = input("Autor (opcional): ")
            anio_str = input("Año de publicación (opcional): ")

            if len(titulo.strip()) == 0:
                titulo = None
            if len(autor.strip()) == 0:
                autor = None
            if len(anio_str.strip()) == 0:
                anio = None
            else:
                anio = int(anio_str)

            update_libro(id, titulo, autor, anio)
            input("Ingrese ENTER para continuar...")
        elif opcion == "5":
            os.system("cls")
            print("5. Eliminar un libro")
            id = input("ID libro: ")
            delete_libro(id)
            input("Ingrese ENTER para continuar...")
        elif opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal...")
            break
        else:
            os.system("cls")
            print("Opción incorrecta, intente nuevamente.")
            input("Ingrese ENTER para continuar...")


def menu_prestamos():
    while True:
        os.system("cls")
        print(
            """
                ====================================
                |        Menú: Préstamos           |
                |----------------------------------|
                | 1. Insertar un préstamo          |
                | 2. Consultar todos los préstamos |
                | 3. Consultar préstamo por ID     |
                | 4. Modificar un préstamo         |
                | 5. Eliminar un préstamo          |
                | 0. Volver al menú principal      |
                ====================================
            """
        )
        opcion = input("Elige una opción [1-5, 0]: ")

        if opcion == "1":
            os.system("cls")
            print("1. Insertar un préstamo")
            id = input("ID préstamo: ")
            idUsuario = input("ID usuario: ")
            idLibro = input("ID libro: ")
            fecha_prestamo = input("Fecha préstamo (DD-MM-YYYY): ")
            fecha_devolucion = input("Fecha devolución (DD-MM-YYYY, opcional): ")
            create_prestamo(id, idUsuario, idLibro, fecha_prestamo, fecha_devolucion)
            input("Ingrese ENTER para continuar...")
        elif opcion == "2":
            os.system("cls")
            print("2. Consultar todos los préstamos")
            read_prestamos()
            input("Ingrese ENTER para continuar...")
        elif opcion == "3":
            os.system("cls")
            print("3. Consultar préstamo por ID")
            id = input("ID préstamo: ")
            read_prestamo_by_id(id)
            input("Ingrese ENTER para continuar...")
        elif opcion == "4":
            os.system("cls")
            print("4. Modificar un préstamo")
            id = input("ID préstamo: ")
            print("[Sólo ingrese los datos a modificar, deje vacío los que no quiera cambiar]")
            idUsuario = input("ID usuario (opcional): ")
            idLibro = input("ID libro (opcional): ")
            fecha_prestamo = input("Fecha préstamo (DD-MM-YYYY, opcional): ")
            fecha_devolucion = input("Fecha devolución (DD-MM-YYYY, opcional): ")

            if len(idUsuario.strip()) == 0:
                idUsuario_opt = None
            else:
                idUsuario_opt = int(idUsuario)

            if len(idLibro.strip()) == 0:
                idLibro_opt = None
            else:
                idLibro_opt = int(idLibro)

            fecha_prestamo_opt = fecha_prestamo if fecha_prestamo.strip() else None
            fecha_devolucion_opt = (
                fecha_devolucion if fecha_devolucion.strip() else None
            )

            update_prestamo(
                id,
                idUsuario_opt,
                idLibro_opt,
                fecha_prestamo_opt,
                fecha_devolucion_opt,
            )
            input("Ingrese ENTER para continuar...")
        elif opcion == "5":
            os.system("cls")
            print("5. Eliminar un préstamo")
            id = input("ID préstamo: ")
            delete_prestamo(id)
            input("Ingrese ENTER para continuar...")
        elif opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal...")
            break
        else:
            os.system("cls")
            print("Opción incorrecta, intente nuevamente.")
            input("Ingrese ENTER para continuar...")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    while True:
        os.system("cls")
        print(
            """
                ====================================
                |     CRUD: Biblioteca + Oracle    |
                |----------------------------------|
                | 1. Crear todas las tablas        |
                | 2. Gestionar tabla Usuarios      |
                | 3. Gestionar tabla Libros        |
                | 4. Gestionar tabla Préstamos     |
                | 0. Salir del sistema             |
                |----------------------------------|
                | * Cree primero usuarios y libros |
                |   antes de registrar préstamos.  |
                ====================================
            """
        )
        opcion = input("Elige una opción [1-4, 0]: ")

        if opcion == "1":
            os.system("cls")
            create_all_tables()
            input("Ingrese ENTER para continuar...")
        elif opcion == "2":
            menu_usuarios()
        elif opcion == "3":
            menu_libros()
        elif opcion == "4":
            menu_prestamos()
        elif opcion == "0":
            os.system("cls")
            print("Saliendo del sistema...")
            break
        else:
            os.system("cls")
            print("Opción incorrecta, intente nuevamente.")
            input("Ingrese ENTER para continuar...")


if __name__ == "__main__":
    main()
