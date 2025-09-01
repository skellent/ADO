# Importacion de Streamlit
import streamlit as st
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
    
# Funcion para cargar la configuracion y manejar errores
def Setup() -> int:
    # Obtencion de la Configuracion
    try:
        CONSTANTES = cargar_constantes()
        DEBUG = CONSTANTES["desarrollo"]["debug"]
        if DEBUG:
            print("[bold green]EL MODO DEBUG ESTA ACTIVO, TODAS LAS IMPRESIONES APARECERAN EN LA TERMINAL[/bold green]")
            print("[bold blue]Secretos Cargados:[/bold blue]")
            print(st.secrets)
        # Configuracion global de la aplicacion
        st.set_page_config(
            page_title=CONSTANTES["general"]["titulo"],
            page_icon=CONSTANTES["general"]["icono"],
            layout=CONSTANTES["general"]["wide"],
            initial_sidebar_state=CONSTANTES["general"]["sidebar_estado"],
        )
        # Configuracion del SideBar
        st.logo(
            image=CONSTANTES["general"]["logotipo"],
            icon_image=CONSTANTES["general"]["logo"]
        )
    except Exception as e:
        if DEBUG: print(f"[bold red]Error al cargar la configuracion: {e}[/bold red]")
        return 1
    return 0
