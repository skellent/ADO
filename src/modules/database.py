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
def ConectarBD(usuario: str, contrasena: str, direccion: str, puerto: str, base_datos: str, debug: bool = False):
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
def CrearCursor(conector, debug: bool = False):
    try:
        cursor = conector.cursor()
        if cursor:
            if debug: print("[bold green]Cursor creado exitosamente[/bold green]")
            return cursor
        else:
            if debug: print("[bold red]Error al crear el cursor[/bold red]")
            sys.exit(1)
    except mariadb.Error as e:
        if debug: print(f"[bold red]Error al crear el cursor: {e}[/bold red]")
        sys.exit(1)

# Funcion para cerrar la conexion
def CerrarConexion(conector, debug: bool = True):
    try:
        conector.close()
        if debug: print("[bold green]Conexion cerrada exitosamente[/bold green]")
    except mariadb.Error as e:
        if debug: print(f"[bold red]Error al cerrar la conexion: {e}[/bold red]")

# Funcion para obtener todos los registros de una tabla
def ObtenerRegistrosDeTabla(bd: dict, tabla: str = "testing", debug: bool = False):
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
    CerrarConexion(cursor.connection, debug=debug)
    return cursor.fetchone()

# Prueba de las funciones
print(
    ObtenerRegistrosDeTabla(
        bd={
            "usuario": CONSTANTES["usuario"],
            "contrasena": CONSTANTES["contrasena"],
            "direccion": CONSTANTES["direccion"],
            "puerto": int(CONSTANTES["puerto"]),
            "base_datos": CONSTANTES["base_datos"]
        },
        tabla="testing",
        debug=True
    )
)