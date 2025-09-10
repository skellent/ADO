# Importacion de Streamlit
import streamlit as st
import streamlit_option_menu as StreamlitMenu

# Importacion de Rich para mejorar la depuracion
# from rich import print

# Importacion de clases
from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase

# Importacion de constantes para paginas
from modules.constPages import instalacion as PagesInstalacion

# Declaracion de funcion Principal
def main() -> None:
    # Creacion de una instancia de Configuracion
    ADOconf: object = ADOconfiguracion()
    ADOconf.SetupStreamlit()
    # Creacion de una instancia de database
    ADOdb: object = ADOdatabase(st.secrets)
    # ADOdb.ImprimirValores() # Impresion para verificar correcta creacion
    if len(ADOdb.ListarTablas()[0]) <= 1:
        # SOFTWARE NO INSTALADO O AL MENOS NO POR COMPLETO
        pg = st.navigation(PagesInstalacion)
        pg.run()
    else:
        st.write("SOFTWARE INSTALADO POR COMPLETO")

# Ejecucion de la funcion Principal
if __name__ == "__main__":
    main()