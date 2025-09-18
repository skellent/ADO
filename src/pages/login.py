import streamlit as st

# Importacion de Rich para mejorar la depuracion
from rich import print
from time import sleep as esperar

# Importacion de clases
from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase

# Funcion para convertir el tipo de usuario en funcion del string que se le pase
def convertirTipo(tipo: str) -> int:
    """
    Esta funcion devuelve el tipo de usuario identificado como un integer para su correcto registro
    """
    if tipo == 'Gestor de Ventas':
        return 1
    elif tipo == 'Gestor de Inventario':
        return 2
    elif tipo == 'Gestor de Clientes':
        return 3
    elif tipo == 'Administrador':
        return 4
    else:
        raise "Este usuario no puede ser registrado!"

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
            # Tipo de usuario
            tipoUsuario: st = st.selectbox(
                "Cargo",
                [
                    'Gestor de Ventas',
                    'Gestor de Inventario',
                    'Gestor de Clientes',
                    'Administrador'
                ],
                index = 0
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

    # Logica de Inicio
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

    # Logica de Registro
    if crearUsuario:
        if nombreRegistro and contrasenaRegistro and contrasenaVerificacion and adminContrasena and tipoUsuario:
            # Se procede con las verificaciones
            if len(nombreRegistro) > 3:
                # 1. Contrasena mayor a 7 caracteres
                if len(contrasenaRegistro) > 7:
                    # 2. Que las contrasenas sean iguales
                    if contrasenaRegistro == contrasenaVerificacion:
                        # 2. Que no exista en la base de datos
                        if ADOdb.ConsultaManual(f"""SELECT * FROM usuarios WHERE usuario = '{nombreRegistro}'""") == []:
                            # El usuario no existe, se puede registrar
                            if ADOdb.CreacionInsercion(f"""INSERT IGNORE INTO usuarios(usuario, contrasena, tipo) VALUES ('{nombreRegistro}', '{contrasenaRegistro}', '{convertirTipo(tipoUsuario)}')"""):
                                st.success("Usuario registrado exitosamente! Dirigase a Iniciar Sesion")
                            else:
                                st.error("Ocurrio un error al registrar al usuario! Contacte a soporte.")
                        else:
                            st.error("Este usuario ya existe en la aplicacion!")
                    else:
                            st.error("Las contrasenas no coinciden!")
                else:
                    st.error("Contrasena demasiado corta!")
            else:
                st.error("Usuario demasiado corto!")
        else:
            st.warning("Llene todos los campos")
main()