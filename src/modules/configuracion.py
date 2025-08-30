# Importacion de tomllib para lectura de archivos manual
import tomllib
# Importacion de Rich para mejorar la depuracion
from rich import print

# Leer el archivo .toml para obtener constantes y configuraciones
def cargar_constantes():
    with open("ado.toml", "rb") as archivo:
        CONSTANTES = tomllib.load(archivo)
        if CONSTANTES["desarrollo"]["debug"]:
            print("Configuraciones cargadas:")
            print(CONSTANTES)
        return CONSTANTES
