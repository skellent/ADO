# Importacion de Rich para mejorar la depuracion
from rich import print

# Importacion de los parametros de conexion
import tomllib
# Esto solo funciona si se ejecuta desde ~/src o si se usa el path completo, de lo contrario retornara error
# pero debido a que se utilizara desde este directorio por la ejecucion de streamlit, no habra problema
CONSTANTES = tomllib.load(open("./.streamlit/secrets.toml", "rb"))

# Importacion de mariadb para la conexion
import mariadb
import sys

# Funcion para conectar a la base de datos
def ConectarBD(usuario: str, contrasena: str, direccion: str, puerto: str, base_datos: str, debug: bool = False) -> mariadb.Connection:
    try:
        conn = mariadb.connect(
            user=usuario,
            password=contrasena,
            host=direccion,
            port=puerto,
            database=base_datos
        )
        if conn:
            if debug: print("[bold green]Conexion a la base de datos exitosa[/bold green]")
            return conn
        else:
            if debug: print("[bold red]Error al conectar a la base de datos[/bold red]")
            sys.exit(1)
    except mariadb.Error as e:
        if debug: print(f"[bold red]Error al conectar a la base de datos: {e}[/bold red]")
        sys.exit(1)

# Funcion para crear un cursor
def CrearCursor(conector, debug: bool = False) -> mariadb.Cursor:
    try:
        cursor = conector.cursor()
        if cursor:
            if debug: print("[bold green]Cursor creado exitosamente[/bold green]")
            return cursor
        else:
            if debug: print("[bold red]Error al crear el cursor[/bold red]")
    except mariadb.Error as e:
        if debug: print(f"[bold red]Error al crear el cursor: {e}[/bold red]")

# Funcion para cerrar la conexion
def CerrarConexion(conector, debug: bool = True) -> None:
    try:
        conector.close()
        if debug: print("[bold green]Conexion cerrada exitosamente[/bold green]")
    except mariadb.Error as e:
        if debug: print(f"[bold red]Error al cerrar la conexion: {e}[/bold red]")

# Se corrobora la conexion a la base de datos mediante la obtencion de las tablas
# Si hay menos de 1 tabla, la base no esta completamente creada y el programa
# No esta completamente instalado, asi que hay que crear la tabla de usuarios
# y registrar al usuario admin
def ValidarInstalacion(bd: dict, debug: bool = False) -> int:
    tablas = ObtenerTablas(bd, debug=debug)
    if type(tablas) == list: # Devolvio una lista vacia, conexion exitosa
        if len(tablas) > 0: # Verifica si hay tablas en la base, de lo contrario devuelve 1 indicando instalacion pendiente
            if ObtenerRegistrosDeTabla(bd, "usuarios", debug=debug) == "ERROR" or ObtenerRegistrosDeTabla(bd, "usuarios", debug=debug) == []:
                return 1 # La tabla de usuarios no existe, por lo tanto la base de datos no esta completamente creada
            return 0
        return 1
    elif type(tablas) == str and tablas == "ERROR":
        # Hubo un error en la consulta, esto solo ocurre si la base de datos no existe o hay un error en la conexion
        return "ERROR"
    return 1

# Funcion para crear la tabla de usuarios
def CrearTablaUsuarios(bd: dict, debug: bool = False) -> int:
    if debug: print(bd)
    cursor = CrearCursor(
        ConectarBD(
            bd["usuario"],
            bd["contrasena"],
            bd["direccion"],
            bd["puerto"],
            bd["base_datos"],
            debug=debug
        ),
        debug=debug
    )
    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS usuarios (
                id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                usuario VARCHAR(20) NOT NULL,
                contrasena VARCHAR(20) NOT NULL,
                tipo INT NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CHECK (LENGTH(usuario) >= 4),
                CHECK (LENGTH(contrasena) >= 8)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
        cursor.connection.commit()
        if debug: print(f"[bold green]Tabla de usuarios creada exitosamente[/bold green]")
        return 0
    except mariadb.Error as e:
        if debug: print(f"[bold red]Error al crear la tabla de usuarios: {e}[/bold red]")
    finally:
        CerrarConexion(cursor.connection, debug=debug)
    return 1

# Funcion para obtener lista de tablas en la base de datos
def ObtenerTablas(bd: dict, debug: bool = False) -> list | str | None:
    if debug: print(bd)
    cursor = CrearCursor(
        ConectarBD(
            bd["usuario"],
            bd["contrasena"],
            bd["direccion"],
            bd["puerto"],
            bd["base_datos"],
            debug=debug
        ),
        debug=debug
    )
    try:
        cursor.execute("SHOW TABLES")
        if debug: print(f"[bold green]Consulta ejecutada exitosamente[/bold green]")
        return cursor.fetchall()
    except mariadb.Error as e:
        if debug: print(f"[bold red]Error al ejecutar la consulta: {e}[/bold red]")
        CerrarConexion(cursor.connection, debug=debug)
        sys.exit(1)
        return "ERROR"

# Funcion para obtener todos los registros de una tabla
def ObtenerRegistrosDeTabla(bd: dict, tabla: str = "testing", debug: bool = False) -> list | int | None:
    if debug: print(bd)
    cursor = CrearCursor(
        ConectarBD(
            bd["usuario"],
            bd["contrasena"],
            bd["direccion"],
            bd["puerto"],
            bd["base_datos"],
            debug=debug
        ),
        debug=debug
    )
    try:
        cursor.execute(f"SELECT * FROM {tabla}")
        if debug: print(f"[bold green]Consulta ejecutada exitosamente[/bold green]")
    except mariadb.Error as e:
        if debug: print(f"[bold red]Error al ejecutar la consulta: {e}[/bold red]")
        CerrarConexion(cursor.connection, debug=debug)
        sys.exit(1)
        return "ERROR"
    CerrarConexion(cursor.connection, debug=debug)
    return cursor.fetchall()

# Funcion para añadir usuarios a la tabla de usuarios
def AñadirUsuario(bd: dict, usuario: str, contrasena: str, tipo: int, debug: bool = False) -> None:
    if debug: print("Insertando usuario a la base...")
    cursor = CrearCursor(
        ConectarBD(
            bd["usuario"],
            bd["contrasena"],
            bd["direccion"],
            bd["puerto"],
            bd["base_datos"],
            debug=debug
        ),
        debug=debug
    )
    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario, contrasena, tipo) VALUES (?, ?, ?)",
            (usuario, contrasena, tipo)
        )
        cursor.connection.commit()
        return 0
    except mariadb.Error as e:
        if debug: print(f"[bold red]Error al insertar el usuario: {e}[/bold red]")
        return 1
    finally:
        CerrarConexion(cursor.connection, debug=debug)

# Prueba de las funciones
def main() -> None:
    print(
        ObtenerRegistrosDeTabla(
            bd={
                "usuario": CONSTANTES["usuario"],
                "contrasena": CONSTANTES["contrasena"],
                "direccion": CONSTANTES["direccion"],
                "puerto": int(CONSTANTES["puerto"]),
                "base_datos": CONSTANTES["base_datos"]
            },
            tabla="usuarios",
            debug=True
        )
    )
    print(
        ObtenerTablas(
            bd={
                "usuario": CONSTANTES["usuario"],
                "contrasena": CONSTANTES["contrasena"],
                "direccion": CONSTANTES["direccion"],
                "puerto": int(CONSTANTES["puerto"]),
                "base_datos": CONSTANTES["base_datos"]
            },
            debug=True
        )
    )

if __name__ == "__main__":
    main()