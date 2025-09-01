# Importacion de Streamlit
import streamlit as st

# Importacion de Rich para mejorar la depuracion
from rich import print
from time import sleep as esperar

# Importacion de Modulos
import modules.configuracion as Configuracion
import modules.database as ADOdataBase

def instalacion() -> None:
    st.title("Instalacion del Software ADO")
    st.warning("El Software no esta completamente instalado, por favor complete la instalacion")
    # Si la instalacion no esta completa, significa que no hay usuarios en la base de datos
    # Por lo tanto se debe crear la tabla de usuarios y registrar al administrador

    if ADOdataBase.CrearTablaUsuarios(st.secrets, debug=st.session_state['DEBUG']): # Si se cumple la condicion, hubo un error
        st.error("Error al crear la tabla de usuarios, contacte con soporte")
        st.stop()
    if st.session_state['DEBUG']: st.success("Tabla de usuarios creada exitosamente")

    # Ahora se crea un formulario para registrar al usuario administrador
    with st.form("registro_admin", clear_on_submit=True):
        st.subheader("Registro de Usuario Administrador")
        col1, col2 = st.columns(2)
        with col1:
            usuario = st.text_input("Usuario", max_chars=20, help="Nombre de usuario del administrador")
        with col2:
            contrasena = st.text_input("Contraseña", type="password", max_chars=20, help="Contraseña del administrador")
        
        # Se procede con el registro
        if st.form_submit_button("Registrar Administrador", type="primary", use_container_width=True, help="Al presionar este boton se registrara el usuario administrador, esta accion no se puede deshacer"):
            try:
                if usuario != "" or contrasena != "" and len(usuario) > 4 and len(contrasena) > 7: # Verificar los campos
                    if ADOdataBase.AñadirUsuario(st.secrets, usuario, contrasena, 0, debug=st.session_state['DEBUG']): # Si se cumple la condicion, hubo un error
                        st.error("Error al registrar el usuario administrador, contacte con soporte")
                        st.stop()
                    st.success("Usuario administrador registrado exitosamente, seras redirigido a la pagina de inicio de sesion en un momento")
                    st.balloons()
                    # Breve pantalla de carga antes de recargar la pagina para animar
                    carga = st.progress(0)
                    for i in range(100):
                        esperar(0.02)
                        carga.progress(i + 1)
                    st.rerun()
                else:
                    st.error("Error al registrar el usuario administrador, por favor verifique los campos")
            except Exception as e:
                print(e)