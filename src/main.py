# Importacion de Streamlit
import streamlit as st

# Importacion de Rich para mejorar la depuracion
from rich import print

# Importacion de Modulos
import modules.configuracion as configuracion
import modules.database as ADOdataBase

# Obtencion de la Configuracion
CONSTANTES = configuracion.cargar_constantes()
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

# Prueba de la conexion a la base de datos mediante consulta directa
if DEBUG: print("[bold blue]Probando la conexion a la base de datos...[/bold blue]")
registros = ADOdataBase.ObtenerRegistrosDeTabla(st.secrets, tabla="testing", debug=DEBUG)
print(registros)