# Importacion de Streamlit
import streamlit as st
# Importacion de tomllib para lectura de archivos manual
import tomllib
# Importacion de Rich para mejorar la depuracion
from rich import print

# Creacion de Clase Configuracion
class ADOconfiguracion():
    # Leer el archivo .toml para obtener constantes y configuraciones
    def LeerTOML(instancia, rutaToml: str = "ado.toml") -> dict:
        """
        Esta funcion permite leer archivos toml sin tanta complejidad, retornando directamente un diccionario
        """
        try:
            with open(rutaToml, "rb") as archivo:
                return tomllib.load(archivo)
        except Exception as e:
            return f"[bold red]Error al leer el archivo .toml: {e}[/bold red]"

    # Funcion para obtener TODAS las configuraciones de ADO
    def VerConfiguraciones(instancia) -> dict:
        """
        Esta funcion retorna todas las configuraciones que se proporcionaron al crear la instancia.
        """
        return instancia.configuraciones

    # Funcion para cargar los ajustes automaticamente
    def SetupStreamlit(instancia) -> None:
        try:
            # Configuracion global de la aplicacion
            st.set_page_config(
                page_title = instancia.configuraciones["general"]["titulo"],
                page_icon = instancia.configuraciones["general"]["icono"],
                layout = instancia.configuraciones["general"]["wide"],
                initial_sidebar_state = instancia.configuraciones["general"]["sidebar_estado"],
            )
            # Configuracion del SideBar
            st.logo(
                image = instancia.configuraciones["general"]["logotipo"],
                icon_image = instancia.configuraciones["general"]["logo"]
            )
        except Exception as e:
            print(f"[bold red]Error al cargar la configuracion: {e}[/bold red]")

    # Constructor
    def __init__(instancia) -> None:
        """
        Esta clase permite configurar Streamlit instanciandola cuando es necesario, como en las pages por ejemplo.
        Automaticamente tratara de obtener las configuraciones al instanciarse.
        """
        instancia.configuraciones = instancia.LeerTOML()
        
def main():
    ADOconf = ADOconfiguracion()
    print(ADOconf.VerConfiguraciones())
    print(ADOconf.LeerTOML("./.streamlit/secrets.toml"))

if __name__ == '__main__':
    main()