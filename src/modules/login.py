# Importacion de Streamlit
import streamlit as st
import streamlit_option_menu as StreamlitMenu

# Importacion de Rich para mejorar la depuracion
from rich import print
from time import sleep as esperar

# Importacion de Modulos
import modules.configuracion as Configuracion
import modules.database as ADOdataBase

@st.dialog("Autorizacion del Administrador")
def autorizarAdmin() -> bool:
    
    if st.button("Autorizar", type="primary", use_container_width=True, help="Al presionar este boton se verificara el usuario y contraseña del administrador"):
        if usuarioAdmin and contrasenaAdmin:
            validacion = ADOdataBase.ValidarUsuario(st.secrets, usuarioAdmin, contrasenaAdmin, debug=st.session_state['DEBUG'])
            if validacion == (): # Si se cumple la condicion, la base no devolvio resultados
                st.error("Error al autorizar, por favor verifique las credenciales del administrador.")
                return False
            return True

def iniciarSesion() -> None:
    # Formulario para Iniciar Sesion
    with st.form("login_form", clear_on_submit=False, border=True):
        usuario = st.text_input( # Nombre de Usuario
            "Usuario",
            help="Nombre de usuario.",
            icon=":material/account_circle:",
            placeholder="Ingrese su nombre de usuario.",
        )
        contrasena = st.text_input( # Contraseña para ingresar
            "Contraseña",
            type="password",
            max_chars=20,
            help="Contraseña del usuario.",
            icon=":material/password:",
            placeholder="Ingrese su contraseña.",
        )
        if st.form_submit_button("Iniciar Sesion", type="primary", use_container_width=True, help="Al presionar este boton se iniciara sesion con el usuario y contraseña ingresados"):
            # Aqui se deberia validar el usuario y contraseña con la base de datos
            if usuario and contrasena: # Si ambos campos no estan vacios
                validacion = ADOdataBase.ValidarUsuario(st.secrets, usuario, contrasena, debug=st.session_state['DEBUG'])
                if validacion == (): # Si se cumple la condicion, la base no devolvio resultados
                    st.error("Error al iniciar sesion, por favor verifique sus credenciales.")
                    st.stop()
                st.session_state['USER'] = usuario # Se guarda el usuario en el sesion state
                st.session_state['CONTR'] = contrasena # Se guarda la contraseña en el sesion state
                st.session_state['TIPO'] = ADOdataBase.ObtenerCargoUsuario(st.secrets, usuario, debug=st.session_state['DEBUG']) # Se guarda el tipo de usuario en el sesion state
            else:
                st.error("Por favor complete todos los campos.")
                st.stop()
            st.success("Inicio de sesion exitoso, seras redirigido a la pagina principal en un momento.")
            esperar(1)
            st.rerun()

def registrarUsuario() -> None:
    with st.form("login_form", clear_on_submit=False, border=True):
        usuario = st.text_input(
            "Usuario",
            help="Nombre de usuario.",
            icon=":material/account_circle:",
            placeholder="Ingrese su nombre de usuario.",
        )
        tipo = st.selectbox(
            "Tipo de Usuario",
            options=["Caja de Venta", "Atencion al Cliente", "Administrador"],
            index=0,
            help="Seleccione el tipo de usuario a registrar.",
        )
        contrasena = st.text_input(
            "Contraseña",
            type="password",
            max_chars=20,
            help="Contraseña del usuario.",
            icon=":material/password:",
            placeholder="Ingrese su contraseña.",
        )
        contrasenaConfirmar = st.text_input(
            "Confirmar Contraseña",
            type="password",
            max_chars=20,
            help="Confirmar Contraseña.",
            icon=":material/password:",
            placeholder="Confirme su contraseña.",
        )
        usuarioAdmin = st.text_input(
            "Usuario Administrador",
            help="Nombre de usuario del administrador.",
            icon=":material/account_circle:",
            placeholder="Ingrese el nombre de usuario del administrador.",
        )
        contrasenaAdmin = st.text_input(
            "Contraseña Administrador",
            type="password",
            max_chars=20,
            help="Contraseña del administrador.",
            icon=":material/password:",
            placeholder="Ingrese la contraseña del administrador.",
        )
        if st.form_submit_button("Registrar Usuario", type="primary", use_container_width=True, help="Al presionar este boton se solicitara el usuario del administrador para registrar el nuevo usuario"):
            if usuario and contrasena and contrasenaConfirmar:
                # Configurar tipo de usuario
                # Caja de Venta = 1
                # Atencion al Cliente = 2
                # Administrador = 3
                # ADO/super admin = 0 (no se puede registrar desde aqui)
                if tipo == "Caja de Venta":
                    cargo = 1
                elif tipo == "Atencion al Cliente":
                    cargo = 2
                elif tipo == "Administrador":
                    cargo = 3
                else:
                    st.error("Error al registrar usuario, tipo de usuario no valido.")
                    st.stop()
                if contrasena != contrasenaConfirmar:
                    st.error("Error al registrar usuario, las contraseñas no coinciden.")
                    st.stop()
                # Tambien hay que asegurarse de que el usuario no exista previamente
                if ADOdataBase.ValidarUsuario(st.secrets, usuario, contrasena, debug=st.session_state['DEBUG']):
                    print(ADOdataBase.ValidarUsuario(st.secrets, usuario, contrasena, debug=st.session_state['DEBUG']))
                    st.error("Este usuario ya esta registrado...")
                    st.stop()
                # Se debe esperar la autorizacion, hasta no resivir la autorizacion, no se puede continuar tanto el usuario como este codigo
                if ADOdataBase.ValidarUsuario(st.secrets, usuarioAdmin, contrasenaAdmin, debug=st.session_state['DEBUG']):
                    if ADOdataBase.AñadirUsuario(st.secrets, usuario, contrasena, cargo, debug=st.session_state['DEBUG']):
                        st.error("Error al registrar usuario, por favor contacte con soporte.")
                        st.stop()
                    st.success("Usuario registrado exitosamente, dirigase a la pagina de inicio de sesion.")
                    st.balloons()
                    esperar(1)
                    st.rerun()
                st.error("Error al registrar usuario, autorizacion de administrador fallida.")
                st.stop()
            else:
                st.error("Por favor complete todos los campos.")
                st.stop()

def login() -> None:
    st.title("Portal de Acceso — ADO")
    menu = StreamlitMenu.option_menu(
            menu_title=None,
            options=["Iniciar Sesion", "Registrar Usuario"],
            icons=["box-arrow-in-right", "person-plus"],
            menu_icon="person-circle",
            default_index=0,
            orientation="horizontal",
        )
    if menu == "Iniciar Sesion":
        iniciarSesion()
    elif menu == "Registrar Usuario":
        registrarUsuario()
    else:
        st.error("Error al cargar el menu, contacte con soporte")
        st.stop()