import streamlit as st
from rich import print
from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase
import pandas as pd
from time import sleep as esperar

def main() -> None:
    ADOconf = ADOconfiguracion()
    ADOconf.SetupStreamlit()
    ADOdb = ADOdatabase(st.secrets)

    st.title("Editar Informacion de Cliente")
    if ADOdb.CreacionInsercion(ADOconf.LeerTOML()['tablas']['clientes']):
        # Mantener la cédula buscada en session_state
        if "cedula_cliente" not in st.session_state:
            st.session_state["cedula_cliente"] = ""
        if "mostrar_resultado" not in st.session_state:
            st.session_state["mostrar_resultado"] = False

        with st.form(key='buscarCliente', enter_to_submit=True):
            col1, col2 = st.columns(2, vertical_alignment='bottom')
            with col1:
                cedula = st.text_input(
                    'Cedula del Cliente',
                    value=st.session_state["cedula_cliente"],
                    placeholder="Ej: 12345786",
                    icon=":material/id_card:"
                )
            with col2:
                buscar = st.form_submit_button(
                    "Buscar Cliente",
                    help="Al presionar este boton, automaticamente se mostraran los datos del cliente si este existe",
                    type="primary",
                    use_container_width=True,
                    icon=":material/search:"
                )
        if buscar:
            st.session_state["cedula_cliente"] = cedula
            st.session_state["mostrar_resultado"] = True

        # Solo mostrar resultado si se ha buscado
        if st.session_state["mostrar_resultado"] and st.session_state["cedula_cliente"]:
            cedula = st.session_state["cedula_cliente"]
            datosClientes = ADOdb.ConsultaManual(f"SELECT * FROM clientes WHERE cedula = '{cedula}'")
            st.markdown("###### Resultado de Busqueda")
            tablaClientes = pd.DataFrame(
                datosClientes,
                columns=['id', 'Cedula', 'Codigo Socio', 'Nombre', 'Telefono', 'Correo', 'Direccion', 'Descripcion', 'Fecha de Creacion', 'Fecha de Modificacion', 'Estado']
            )
            st.dataframe(
                tablaClientes[['Cedula', 'Codigo Socio', 'Nombre', 'Telefono', 'Correo', 'Direccion', 'Descripcion', 'Fecha de Creacion', 'Fecha de Modificacion']],
                width='stretch',
                hide_index=True
            )

            if datosClientes != []:
                with st.container(border=True):
                    st.markdown("###### Edicion")
                    col3, col4 = st.columns(2, vertical_alignment="bottom")
                    with col3:
                        campo = st.selectbox(
                            "Campo a Modificar",
                            ['Cedula', 'Codigo Socio', 'Nombre', 'Telefono', 'Correo', 'Direccion', 'Descripcion'],
                            help="Este sera el campo a modificar del cliente en cuestion",
                            key="campo_modificar"
                        )
                    with col4:
                        informacion = st.text_input(
                            "Dato de Modificacion",
                            help="Escriba aqui la nueva informacion a asignar al cliente",
                            icon=":material/edit:",
                            key="info_modificar"
                        )
                    editar = st.button(
                        "Editar Campo",
                        help="Al presionar este boton, automaticamente se mostraran los datos del cliente si este existe",
                        type="primary",
                        use_container_width=True,
                        icon=":material/edit:"
                    )
                    if editar and informacion:
                        # Mapear nombres de campos a columnas reales si es necesario
                        columnas = {
                            'Cedula': 'cedula',
                            'Codigo Socio': 'codigo_socio',
                            'Nombre': 'nombre',
                            'Telefono': 'telefono',
                            'Correo': 'correo',
                            'Direccion': 'direccion',
                            'Descripcion': 'descripcion'
                        }
                        columna_sql = columnas[campo]
                        # Ejecutar actualización
                        if ADOdb.CreacionInsercion(f"UPDATE clientes SET {columna_sql} = '{informacion}' WHERE cedula = '{cedula}'"):
                            st.success("Cliente editado correctamente")
                        else:
                            st.error("Error en la edicion, verifique que la informacion insertada sea coherente")
                            st.stop()
                        # Esperar un poco para que la BD actualice y refrescar tabla
                        esperar(0.5)
                        # Refrescar datos
                        datosClientes = ADOdb.ConsultaManual(f"SELECT * FROM clientes WHERE cedula = '{cedula}'")
                        tablaClientes = pd.DataFrame(
                            datosClientes,
                            columns=['id', 'Cedula', 'Codigo Socio', 'Nombre', 'Telefono', 'Correo', 'Direccion', 'Descripcion', 'Fecha de Creacion', 'Fecha de Modificacion', 'Estado']
                        )
                        st.dataframe(
                            tablaClientes[['Cedula', 'Codigo Socio', 'Nombre', 'Telefono', 'Correo', 'Direccion', 'Descripcion', 'Fecha de Creacion', 'Fecha de Modificacion']],
                            width='stretch',
                            hide_index=True
                        )
    else:
        st.error("Error con Base de Datos")

main()