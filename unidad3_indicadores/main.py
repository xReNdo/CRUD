from conexion import Database
from autenticacion import Auth
from indicadores import IndicadoresEconomicos
import oracledb
import getpass
from datetime import datetime

def next_user_id(db: Database) -> int:
    rows = db.query("SELECT NVL(MAX(id), 0) + 1 FROM USERS")
    return int(rows[0][0])

def registrar(db: Database):
    print("\n=== Registro de usuario ===")
    username = input("Nuevo usuario: ").strip()
    password = getpass.getpass("Nueva contraseña: ").strip()

    # Verificar si ya existe
    existe = db.query("SELECT 1 FROM USERS WHERE username = :u", {"u": username})
    if existe:
        print("Ese usuario ya existe.")
        return

    uid = next_user_id(db)
    hashed = Auth.hash_password(password).hex()

    db.query(
        "INSERT INTO USERS (id, username, password_hash) VALUES (:id, :u, :p)",
        {"id": uid, "u": username, "p": hashed}
    )
    print("Usuario registrado correctamente.")

def login(db: Database) -> str | None:
    print("\n=== Login ===")
    username = input("Usuario: ").strip()
    password = getpass.getpass("Contraseña: ").strip()

    rows = db.query("SELECT password_hash FROM USERS WHERE username = :u", {"u": username})
    if not rows:
        print("Usuario no existe.")
        return None

    hashed_hex = rows[0][0]
    hashed_bytes = bytes.fromhex(hashed_hex)

    if Auth.verify_password(password, hashed_bytes):
        print("Login exitoso ✅")
        return username
    else:
        print("Contraseña incorrecta ❌")
        return None

def consultar_y_guardar(db: Database, api: IndicadoresEconomicos, usuario: str):
    print("\n=== Indicadores económicos ===")
    indicador = input("Indicador (uf, dolar, euro, utm, ipc, ivp): ").strip().lower()

    valor = api.obtener_indicador(indicador)
    if valor is None:
        print("No se pudo obtener el indicador.")
        return

    print(f"Valor actual de {indicador.upper()}: {valor}")

    guardar = input("¿Guardar en BD? (s/n): ").strip().lower()
    if guardar != "s":
        return

    db.query(
        """
        INSERT INTO INDICADORES
        (nombre, fecha_indicador, valor, fecha_consulta, usuario, fuente)
        VALUES (:n, SYSDATE, :v, SYSDATE, :u, 'mindicador.cl')
        """,
        {"n": indicador, "v": valor, "u": usuario}
    )
    print("Indicador guardado en BD ✅")

def main():
    db = Database()
    api = IndicadoresEconomicos()

    usuario_logeado = None

    while True:
        print("\n=== Sistema Unidad 3 (Auth + API + BD) ===")
        print("1) Registrar usuario")
        print("2) Login")
        print("3) Consultar indicador y guardar")
        print("0) Salir")

        op = input("Opción: ").strip()

        try:
            if op == "1":
                registrar(db)
            elif op == "2":
                usuario_logeado = login(db)
            elif op == "3":
                if not usuario_logeado:
                    print("Debes iniciar sesión primero.")
                else:
                    consultar_y_guardar(db, api, usuario_logeado)
            elif op == "0":
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")
        except oracledb.Error as e:
            print("Error de base de datos:", e)
        except Exception as e:
            print("Error inesperado:", e)

if __name__ == "__main__":
    main()
