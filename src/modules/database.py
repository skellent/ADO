# Importacion de Rich para mejorar la depuracion
from rich import print
# Importacion de los parametros de conexion
import tomllib
# Esto solo funciona si se ejecuta desde ~/src o si se usa el path completo, de lo contrario retornara error
# pero debido a que se utilizara desde este directorio por la ejecucion de streamlit, no habra problema
CONSTANTES = tomllib.load(open("./.streamlit/secrets.toml", "rb"))
# Importacion de mariadb para la conexion
import mariadb

# Clase para Manejar Base de Datos
class ADOdatabase():      
    # Imprime los datos para conectarse a la base de datos
    def ImprimirValores(instancia) -> None:
        """
        Esta funcion simplemente imprime los valores usados en el constructor para la base de datos.
        Tambien imprime el cursor y la conexion.
        """
        print(instancia.parametroConexion)
        print(instancia.conexion)
        print(instancia.cursor)

    # Funcion para crear nuevamente la conexion y el cursor
    def CrearConexion(instancia) -> tuple:
        """
        Esta funcion se encarga de crear nuevamente la conexion de forma manual en caso de haberla cerrado por parte del desarrollador.
        """
        try:
            conexion = mariadb.connect(
                user = instancia.parametroConexion['usuario'],
                password = instancia.parametroConexion['contrasena'],
                host = instancia.parametroConexion['direccion'],
                port = instancia.parametroConexion['puerto'],
                database = instancia.parametroConexion['base_datos']
            )
        except Exception as e:
            print("Ocurrio un error al conectar a la Base de Datos: ", e)
        # Creacion del Cursor
        try:
            cursor = conexion.cursor()
        except Exception as e:
            print("Ocurrio un error al crear el cursor de la conexion: ", e)
        # retorna la conexion y al cursor
        return conexion, cursor
    
    # Funcion para cerrar la conexion
    def CerrarConexion(instancia) -> None:
        """
        Esta funcion cierra manualmente la conexion con la base de datos
        """
        if instancia.conexion:
            try:
                instancia.cursor.close()
            except Exception as e:
                print("Ocurrio un error al cerrar la conexion a la base de datos: ", e)

    # Funcion para hacer una consulta completa a una tabla en la base de datos
    def ConsultarTabla(instancia, tabla: str) -> list:
        """
        Esta funcion devuelve una tupla con todos los datos obtenidos de la tabla a consultar
        ARGUMENTOS:
        - tabla: El nombre real de la tabla en la base de datos
        """
        instancia.cursor.execute(f"""SELECT * FROM {tabla}""")
        return instancia.cursor.fetchall()

    # Funcion para listar las tablax existentes en la base de datos
    def ListarTablas(instancia) -> list:
        """
        Esta funcion simplemente revisa que tablas existen en la base de datos. en caso de no haber ninguna es porque el software no esta completamente instalado.
        """
        instancia.cursor.execute("""SHOW TABLES""")
        return instancia.cursor.fetchall()
        

    # Consulta manual por parte del desarrollador para casos particulares
    def ConsultaManual(instancia, consulta: str) -> list:
        """
        Esta funcion permite escribir consultas personalizadas para casos complejos.
        ARGUMENTOS:
        - consulta: La consulta escrita por parte del desarrollador.
        """
        try:
            instancia.cursor.execute(consulta)
            return instancia.cursor.fetchall()
        except Exception as e:
            print("Error al elaborar consulta manual: ", e)

    # Constructor
    def __init__(instancia, database: dict) -> None:
        """
        Esta clase crea una instancia que permite manejar la base de datos mediante su uso, para simplificar cosas en otros modulos, a su vez crea automaticamente la conexion a la base de datos
        """
        # Se guardan los parametros en caso de uso futuro o modificacion manual
        instancia.parametroConexion = database
        # Se intenta crear el cursor y la conexion con una funcion
        instancia.conexion, instancia.cursor = instancia.CrearConexion()


""" CREATE TABLE IF NOT EXISTS usuarios (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        usuario VARCHAR(20) NOT NULL,
        contrasena VARCHAR(20) NOT NULL,
        tipo INT NOT NULL,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CHECK (LENGTH(usuario) >= 4),
        CHECK (LENGTH(contrasena) >= 8)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

# Funcion Principal | Prueba de las funciones
def main() -> None:
    # Creacion de Objeto para Testear
    ADOdb = ADOdatabase(CONSTANTES)
    # Imprime el Parametro dado para conectarse (secrets.toml)
    ADOdb.ImprimirValores()
    # Cierra la Conexion
    ADOdb.CerrarConexion()
    # Vuelve a realizar la conexion
    ADOdb.conexion, ADOdb.cursor = ADOdb.CrearConexion()
    # Imprime nuevamente
    ADOdb.ImprimirValores()
    # Realiza una Consulta Simple
    print(ADOdb.ConsultarTabla("usuarios"))
    # Realizar Consulta Manual
    print(ADOdb.ConsultaManual("SELECT * FROM usuarios WHERE id = 2"))

if __name__ == "__main__":
    main()