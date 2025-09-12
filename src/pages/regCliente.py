import streamlit as st

# Importacion de Rich para mejorar la depuracion
from rich import print

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

    st.title("Registrar Cliente")
    # Crea la tabla en caso de que no exista
    if ADOdb.CreacionInsercion(ADOconf.LeerTOML()['tablas']['clientes']):
        with st.form("registro", clear_on_submit = False, enter_to_submit = False):
            # Cedula del Cliente
            cedula: str = st.text_input(
                "C.I. del Cliente (obligatorio)",
                help = "Ingrese aqui la cedula de identidad del cliente a registrar.",
                placeholder = "Ej: 12345786",
                icon = ":material/id_card:"
            )
            # Codigo del Socio dentro del Sistema
            codigoSocio: str = st.text_input(
                "Codigo de Socio",
                help = "Ingrese aqui el codigo de socio del cliente a registrar. Si el numero ya esta ocupado, el sistema le avisara y le proporcionara los numeros disponibles. En caso de no agregar el codigo de socio desde el principio del registro, podra agregarlo posteriormente en la edicion.",
                placeholder = "Ej: 1234",
                icon = ":material/badge:"
            )
            # Nombre completo del Cliente a Registrar
            nombre: str = st.text_input(
                "Nombre del Cliente (obligatorio)",
                help = "Ingrese aqui el nombre completo del cliente a registrar.",
                placeholder = "Ej: Nombre Nombre2 Apellido Apellido2",
                icon = ":material/person:"
            )
            # Numero Telefonioco del Cliente dentro del Sistema
            telefono: str = st.text_input(
                "Numero Telefonico del Cliente (obligatorio)",
                help = "Ingrese aqui el numero telefonico del cliente",
                placeholder = "Ej: 0426-4572138",
                icon = ":material/phone:"
            )
            # Correo Electronico del Cliente a Registrar
            correo: str = st.text_input(
                "Correo Electronico del Cliente",
                help = "Ingrese aqui el correo electronico del cliente a registrar.",
                placeholder = "Ej: ejemplo@email.com",
                icon = ":material/email:"
            )
            # Ubicacion o Direccion del Cliente
            direccion: str = st.text_input(
                "Direccion del Cliente",
                help = "Ingrese aqui la direccion del cliente a registrar.",
                placeholder = "Ej: Carrera 16 Entre Calle 40 y 41",
                icon = ":material/pin_drop:"
            )
            # Breve Descripcion del Cliente
            descripcion: str = st.text_area(
                "Breve Descripcion del Cliente",
                max_chars = 250,
                help = "Escriba aqui informacion complementaria a cerca del cliente.",
                placeholder = "Este cliente es el creador de Skell's CRM"
            )
            # Boton de Submit para registrar al Cliente
            boton: bool = st.form_submit_button(
                "Registrar Cliente",
                help = 'Al presionar este boton, se registrara el cliente si los datos ingresados son validos.',
                type = 'primary',
                use_container_width = True,
                icon = ':material/person_add:'
            )
    else:
        st.error("Error con Base de Datos")

    # Logica para Registro de Cliente
    if boton:
        if cedula and nombre and telefono:
            if cedula.isnumeric():
                if telefono.isnumeric():
                    # Se verifica que no exista ya en la base
                    if ADOdb.ConsultaManual(f"""SELECT * FROM clientes WHERE cedula = '{cedula}'""") == []:
                        # Se procede con el registro en la base de datos
                        if ADOdb.CreacionInsercion(f"""INSERT INTO clientes (cedula, codigo_socio, nombre, telefono, correo, direccion, descripcion) VALUES ('{cedula}', {f"'{codigoSocio}" if codigoSocio else 'NULL'}, '{nombre}', '{telefono}', '{f"'{correo}" if correo else 'Ninguno@email.com'}', {f"'{direccion}" if direccion else 'NULL'}, {f"'{descripcion}" if descripcion else 'NULL'})"""):
                            st.success("Usuario Registrado")
                        else:
                            st.error("Hubo un error al registrar al cliente")
                    else:
                        st.error("Este cliente ya existe en la base de datos")
                else:
                    st.error("Numero de Telefono Invalido")
            else:
                st.error("Cedula invalida")
        else:
            st.warning("Ingrese todos los campos obligatorios")
        
main()