# Importacion de Streamlit
import streamlit as st
import streamlit_option_menu as StreamlitMenu

# Importacion de Rich para mejorar la depuracion
# from rich import print

# Importacion de clases
from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase

# Declaracion de funcion Principal
def main() -> None:
    ADOconf: object = ADOconfiguracion()
    ADOconf.SetupStreamlit()

# Ejecucion de la funcion Principal
if __name__ == "__main__":
    main()