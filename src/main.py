# Importacion de Streamlit
import streamlit as st
import streamlit_option_menu as StreamlitMenu

# Importacion de Rich para mejorar la depuracion
from rich import print
from time import sleep as esperar

# Importacion de Modulos, se importan como si fueran clases, para evitar problemas de nombres repetidos en casos particulares
import modules.configuracion as ADOconfiguracion
import modules.database as ADOdataBase
import modules.instalacion as ADOinstalacion
import modules.login as ADOlogin

# Corroborar estado del DEBUG
def DebugEstado() -> bool | str:
    # Obtencion de la Configuracion
    CONSTANTES = ADOconfiguracion.cargar_constantes()
    DEBUG = CONSTANTES["desarrollo"]["debug"]
    return DEBUG

# Declaracion de funcion Principal
def main() -> None:

    # Configura la pagina
    if ADOconfiguracion.Setup(): # si se cumple la condicion, hubo un error
        st.error("Error al cargar la configuracion, revise la terminal para mas detalles")
        st.stop()

    # Estado del DEBUG
    if 'DEBUG' not in st.session_state:
        st.session_state['DEBUG'] = DebugEstado() # Es imposible que falle, ya que si la configuracion falla, la funcion principal no se ejecuta
    if st.session_state['DEBUG']: st.write(f"DEBUG: {st.session_state['DEBUG']}")

    # Estado de la Base de Datos
    estadoBD = ADOdataBase.ValidarInstalacion(st.secrets, debug=st.session_state['DEBUG'])
    if estadoBD == "ERROR": # si se cumple la condicion, hubo un error
        st.error("Hubo un problema al conectar con la base de datos, contacte con soporte")
        # Debido a que la base de datos no esta creada, no se puede continuar
        st.stop()
    elif estadoBD == 1: # La base de datos no esta completamente creada
        ADOinstalacion.instalacion()
    else: # La base de datos esta completamente creada y lista para usarse al igual que el programa
        if 'USER' not in st.session_state:
            ADOlogin.login()
        else:
            st.title(f"Bienvenido, {st.session_state['USER']}")
            st.write(st.session_state)

# Ejecucion de la funcion Principal
if __name__ == "__main__":
    main()