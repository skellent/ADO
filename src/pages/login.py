import streamlit as st

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
    # Creacion de pestanas
    tab1, tab2 = st.tabs(['Iniciar Sesión', 'Registrar Usuario'])
    # Inicio de Sesion
    with tab1:
        with st.container(border = True):
            st.subheader("Inicio de Sesión")
            # Input para escribir el nombre de usuario
            nombreUsuario: st = st.text_input(
                key = "userName",
                label = "Nombre de Usuario",
                max_chars = 20,
                placeholder = 'Usuario123',
                help = "Escriba aquí su nombre de usuario.",
                icon = ':material/account_circle:'
            )
            # Input para escribir la contrasena
            contrasena: st = st.text_input(
                key = "passwordName",
                label = 'Contraseña de Usuario',
                max_chars = 20,
                type = 'password',
                placeholder = '123456789$r',
                icon = ':material/password:'
            )
            # Boton para Iniciar Sesion
            iniciarSesion: st = st.button(
                label = "Iniciar Sesión",
                help = 'Al presionar este boton, se iniciara sesión con su usuario ingresado.',
                type = 'primary',
                icon = ':material/login:',
                use_container_width = True
            )
    # Registro de Usuario
    with tab2:
        with st.container(border = True):
            st.subheader("Registrar Usuario")
            # Input para escribir el nombre de usuario
            nombreRegistro: st = st.text_input(
                label = "Nombre de Usuario",
                max_chars = 20,
                placeholder = 'Usuario123',
                help = "Escriba aquí su nombre de usuario.",
                icon = ':material/account_circle:'
            )
            # Input para escribir la contrasena
            contrasenaRegistro: st = st.text_input(
                label = 'Contraseña de Usuario',
                max_chars = 20,
                type = 'password',
                placeholder = '123456789$r',
                icon = ':material/password:'
            )
            # Input para escribir la contrasena y confirmarla
            contrasenaVerificacion: st = st.text_input(
                label = 'Verificar Contraseña',
                max_chars = 20,
                type = 'password',
                placeholder = 'Misma contraseña',
                icon = ':material/password:'
            )
            # Contrasena del Administrador
            adminContrasena: st = st.text_input(
                key = 'adminPassword',
                label = 'Confirmación del Administrador',
                max_chars = 20,
                type = 'password',
                placeholder = 'Contraseña del Administrador',
                icon = ':material/shield_person:'
            )
            # Boton para Iniciar Sesion
            crearUsuario: st = st.button(
                label = "Registrar Usuario",
                help = 'Al presionar este boton, se registrará el usuario y deberá dirigirse a la pestana "Iniciar Sesión" para continuar',
                type = 'primary',
                icon = ':material/login:',
                use_container_width = True
            )

    # Logica de Registro o Inicio
    if iniciarSesion:
        if nombreUsuario and contrasena:
            # Se procede con el inicio de sesion
            sesion: list = ADOdb.ConsultaManual(f"""SELECT * FROM usuarios WHERE usuario = '{nombreUsuario}' AND contrasena = '{contrasena}'""")
            # Si esta vacio, significa que no hay un usuario registrado con estos datos
            if sesion == []:
                st.error("Usuario no registrado!")
            else:
                # Formatea los datos para poder usarlos en el sesion state
                sesion = sesion[0]
                st.session_state['usuario'] = sesion[1]
                st.session_state['usuarioTipo'] = sesion[3]
                # Mensaje final
                st.success("Inicio de Sesion Exitoso")
                esperar(2)
                st.rerun()         
        else:
            st.warning("Escriba su Nombre de Usuario y Contrasena!")
main()