import streamlit as st

# Importacion de Rich para mejorar la depuracion
from rich import print

# Importacion de la configuracion
from modules.configuracion import cargar_constantes
CONSTANTES = cargar_constantes()
DEBUG = CONSTANTES["desarrollo"]["debug"]
if DEBUG:
    print("[bold green]EL MODO DEBUG ESTA ACTIVO, TODAS LAS IMPRESIONES APARECERAN EN LA TERMINAL[/bold green]")

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

st.title("Hello, Streamlit!")
st.write("This is a simple Streamlit app. in test1.py")