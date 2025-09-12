# Importacion de Streamlit
import streamlit as st

# Importacion de Rich para mejorar la depuracion
# from rich import print

# Importacion de clases
from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase

# Importacion de constantes para paginas
from modules.constPages import instalacion as PagesInstalacion
from modules.constPages import login as PagesLogin
from modules.constPages import administrador as PagesAdministrador

# Declaracion de funcion Principal
def main() -> None:
    # Creacion de una instancia de Configuracion
    ADOconf: object = ADOconfiguracion()
    ADOconf.SetupStreamlit()
    # Creacion de una instancia de database
    ADOdb: object = ADOdatabase(st.secrets)
    # ADOdb.ImprimirValores() # Impresion para verificar correcta creacion
    if ADOdb.ListarTablas() == []:
        # SOFTWARE NO INSTALADO O AL MENOS NO POR COMPLETO
        pg = st.navigation(PagesInstalacion)
        pg.run()
    else:
        # SOFTWARE INSTALADO POR COMPLETO
        if 'usuario' in st.session_state:
            # Mensaje de Bienvenida para el usuario
            st.write(f"Bienvenido, {st.session_state['usuario']}")
            # Actualizar el SideBar segun el tipo de usuario
            if st.session_state['usuarioTipo'] == 4:
                pg = st.navigation(PagesAdministrador)
            pg.run()

            # Agregar al final siempre un boton para cerrar la sesion
            with st.sidebar:
                logOut: st = st.button(
                    "Cerrar Sesión",
                    help = "Al presionar este botón se cerrará su sesión.",
                    type = 'primary',
                    use_container_width = True,
                    icon = ':material/logout:')
                if logOut:
                    del st.session_state['usuario']
                    st.rerun()
        else:
            pg = st.navigation(PagesLogin)
            pg.run()

# Ejecucion de la funcion Principal
if __name__ == "__main__":
    main()