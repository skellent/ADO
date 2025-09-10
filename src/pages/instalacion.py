# Importacion de Streamlit
import streamlit as st
import streamlit_option_menu as StreamlitMenu

# Importacion de Rich para mejorar la depuracion
from rich import print
from time import sleep as esperar

# Importacion de clases
from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase

# Declaracion de funcion Principal
def main() -> None:
    # Creacion de instancia de configuracion
    ADOconf: object = ADOconfiguracion()
    ADOconf.SetupStreamlit()
    # Creacion de una instancia de database
    ADOdb: object = ADOdatabase(st.secrets)
    # ADOdb.ImprimirValores() # Impresion para verificar correcta creacion

    # Interfaz
    st.title("Instalación del Software")
    # Aqui va el mensaje informativo
    with st.container(border=True):
        col1, col2 = st.columns(2, vertical_alignment='bottom')
        with col1:
            # Input para escribir la contrasena del administrador
            contrasena: st = st.text_input(
                label = 'Contrasena del Administrador',
                max_chars = 20,
                type = 'password',
                placeholder = '123456789$r',
                icon = ':material/shield_person:'
            )
        with col2:
            # Boton para guardar contrasena del administrador
            crearAdmin: st = st.button(
                label = "Crear Administrador",
                help = 'Al presionar este boton, automaticamente se completara la instalacion del Programa.',
                type = 'primary',
                icon = ':material/shield_person:',
                use_container_width = True
            )
    
    # Logica de creacion de tablas
    if crearAdmin: 
        if contrasena:
            if len(contrasena) > 4:
                # Creacion de la Tabla de Usuarios y del Registro de $root en la tabla
                if ADOdb.CreacionInsercion(ADOconf.LeerTOML()['tablas']['usuarios']) and ADOdb.CreacionInsercion(f"""INSERT INTO usuarios (usuario, contrasena, tipo) VALUES ('$root', '{contrasena}', 0)"""):
                    st.success('Usuario "$root" creado exitosamente!')
                    esperar(2)
                    st.rerun()
                else:
                    st.error("Ha ocurrido un error al crear al administrador, consulte con soporte")
            else:
                st.warning("Contrasena demasiado corta!")
        else:
            st.warning("Escriba la contrasena para el administrador!")
    
main()