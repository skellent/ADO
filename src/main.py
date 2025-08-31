# Importacion de Streamlit
import streamlit as st

# Importacion de Rich para mejorar la depuracion
from rich import print
from time import sleep as esperar

# Importacion de Modulos
import modules.configuracion as Configuracion
import modules.database as ADOdataBase

def configuracion() -> int:
    # Obtencion de la Configuracion
    try:
        CONSTANTES = Configuracion.cargar_constantes()
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
    except Exception as e:
        if DEBUG: print(f"[bold red]Error al cargar la configuracion: {e}[/bold red]")
        return 1
    return 0

# Corroborar estado del DEBUG
def DebugEstado() -> bool | str:
    # Obtencion de la Configuracion
    CONSTANTES = Configuracion.cargar_constantes()
    DEBUG = CONSTANTES["desarrollo"]["debug"]
    return DEBUG

# Se corrobora la conexion a la base de datos mediante la obtencion de las tablas
# Si hay menos de 1 tabla, la base no esta completamente creada y el programa
# No esta completamente instalado, asi que hay que crear la tabla de usuarios
# y registrar al usuario admin
def BaseDatosEstado(bd: dict, debug: bool = False) -> int:
    tablas = ADOdataBase.ObtenerTablas(bd, debug=debug)
    if type(tablas) == list: # Devolvio una lista vacia, conexion exitosa
        if len(tablas) > 0: # Verifica si hay tablas en la base, de lo contrario devuelve 1 indicando instalacion pendiente
            if ADOdataBase.ObtenerRegistrosDeTabla(bd, "usuarios", debug=debug) == "ERROR" or ADOdataBase.ObtenerRegistrosDeTabla(bd, "usuarios", debug=debug) == []:
                return 1 # La tabla de usuarios no existe, por lo tanto la base de datos no esta completamente creada
            return 0
        return 1
    elif type(tablas) == str and tablas == "ERROR":
        # Hubo un error en la consulta, esto solo ocurre si la base de datos no existe o hay un error en la conexion
        return "ERROR"
    return 1

# Declaracion de funcion Principal
def main() -> None:

    # Configura la pagina
    if configuracion(): # si se cumple la condicion, hubo un error
        st.error("Error al cargar la configuracion, revise la terminal para mas detalles")
        st.stop()

    # Estado del DEBUG
    if 'DEBUG' not in st.session_state:
        st.session_state['DEBUG'] = DebugEstado() # Es imposible que falle, ya que si la configuracion falla, la funcion principal no se ejecuta
    if st.session_state['DEBUG']: st.write(f"DEBUG: {st.session_state['DEBUG']}")

    # Estado de la Base de Datos
    estadoBD = BaseDatosEstado(st.secrets, debug=st.session_state['DEBUG'])
    if estadoBD == "ERROR": # si se cumple la condicion, hubo un error
        st.error("Hubo un problema al conectar con la base de datos, contacte con soporte")
        # Debido a que la base de datos no esta creada, no se puede continuar
        st.stop()
    elif estadoBD == 1: # La base de datos no esta completamente creada
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
    
    else: # La base de datos esta completamente creada y lista para usarse al igual que el programa
        st.success("El Software esta completamente instalado y listo para usarse")

# Ejecucion de la funcion Principal
if __name__ == "__main__":
    main()