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

    st.title("Editar Informacion de Producto")
    if ADOdb.CreacionInsercion(ADOconf.LeerTOML()['tablas']['productos']):
        tab1, tab2 = st.tabs(['Informacion General', 'Stock'])
        with tab1:
            # Mantener la cédula buscada en session_state
            if "codigo_producto" not in st.session_state:
                st.session_state["codigo_producto"] = ""
            if "mostrar_resultado" not in st.session_state:
                st.session_state["mostrar_resultado"] = False

            with st.form(key='buscarCliente', enter_to_submit=True):
                col1, col2 = st.columns(2, vertical_alignment='bottom')
                with col1:
                    codigo = st.text_input(
                        'Codigo del Producto',
                        value=st.session_state["codigo_producto"],
                        placeholder="Ej: 1234",
                        icon=":material/barcode:"
                    )
                with col2:
                    buscar = st.form_submit_button(
                        "Buscar Producto",
                        help="Al presionar este boton, automaticamente se mostraran los datos del producto si este existe",
                        type="primary",
                        use_container_width=True,
                        icon=":material/search:"
                    )
            if buscar:
                st.session_state["codigo_producto"] = codigo
                st.session_state["mostrar_resultado"] = True

            # Solo mostrar resultado si se ha buscado
            if st.session_state["mostrar_resultado"] and st.session_state["codigo_producto"]:
                codigo = st.session_state["codigo_producto"]
                datosProducto = ADOdb.ConsultaManual(f"SELECT * FROM productos WHERE codigo = '{codigo}'")
                st.markdown("###### Resultado de Busqueda")
                tablaProductos = pd.DataFrame(
                    datosProducto,
                    columns=['id', 'Codigo', 'Nombre', 'Precio', 'Cantidad', 'Proveedor', 'Fecha de Creacion', 'Fecha de Modificacion', 'Estado']
                )
                st.dataframe(
                    tablaProductos[['Codigo', 'Nombre', 'Precio', 'Cantidad', 'Proveedor', 'Fecha de Creacion', 'Fecha de Modificacion']],
                    width='stretch',
                    hide_index=True
                )

                if datosProducto != []:
                    with st.container(border=True):
                        st.markdown("###### Edicion")
                        col3, col4 = st.columns(2, vertical_alignment="bottom")
                        with col3:
                            campo = st.selectbox(
                                "Campo a Modificar",
                                ['Codigo', 'Nombre', 'Precio', 'Proveedor'],
                                help="Este sera el campo a modificar del producto en cuestion",
                                key="campo_modificar"
                            )
                        with col4:
                            informacion = st.text_input(
                                "Dato de Modificacion",
                                help="Escriba aqui la nueva informacion a asignar al producto",
                                icon=":material/edit:",
                                key="info_modificar"
                            )
                        editar = st.button(
                            "Editar Campo",
                            help="Al presionar este boton, automaticamente se mostraran los datos del producto si este existe",
                            type="primary",
                            use_container_width=True,
                            icon=":material/edit:"
                        )
                        if editar and informacion:
                            # Mapear nombres de campos a columnas reales si es necesario
                            columnas = {
                                'Codigo': 'codigo',
                                'Nombre': 'nombre',
                                'Precio': 'precio',
                                'Proveedor': 'proveedor'
                            }
                            columna_sql = columnas[campo]
                            # Ejecutar actualización
                            if ADOdb.CreacionInsercion(f"UPDATE productos SET {columna_sql} = '{informacion}' WHERE codigo = '{codigo}'"):
                                st.success("Producto editado correctamente")
                            else:
                                st.error("Error en la edicion, verifique que la informacion insertada sea coherente")
                                st.stop()
                            # Esperar un poco para que la BD actualice y refrescar tabla
                            esperar(0.5)
                            # Refrescar datos
                            datosProducto = ADOdb.ConsultaManual(f"SELECT * FROM productos WHERE codigo = '{codigo}'")
                            tablaProductos = pd.DataFrame(
                                datosProducto,
                                columns=['id', 'Codigo', 'Nombre', 'Precio', 'Cantidad', 'Proveedor', 'Fecha de Creacion', 'Fecha de Modificacion', 'Estado']
                            )
                            st.dataframe(
                                tablaProductos[['Codigo', 'Nombre', 'Precio', 'Cantidad', 'Proveedor', 'Fecha de Creacion', 'Fecha de Modificacion']],
                                width='stretch',
                                hide_index=True
                            )
        with tab2:
            # Mantener la cédula buscada en session_state
            if "codigo_producto" not in st.session_state:
                st.session_state["codigo_producto"] = ""
            if "mostrar_resultado" not in st.session_state:
                st.session_state["mostrar_resultado"] = False

            with st.form(key='buscarProducto', enter_to_submit=True):
                col1, col2 = st.columns(2, vertical_alignment='bottom')
                with col1:
                    codigo = st.text_input(
                        'Codigo del Producto',
                        value=st.session_state["codigo_producto"],
                        placeholder="Ej: 1234",
                        icon=":material/barcode:"
                    )
                with col2:
                    buscar2 = st.form_submit_button(
                        "Buscar Producto",
                        help="Al presionar este boton, automaticamente se mostraran los datos del producto si este existe",
                        type="primary",
                        use_container_width=True,
                        icon=":material/search:"
                    )
            if buscar2:
                st.session_state["codigo_producto"] = codigo
                st.session_state["mostrar_resultado"] = True

            datosStock = ADOdb.ConsultaManual(f"SELECT * FROM productos WHERE codigo = '{codigo}'")
            # Solo mostrar resultado si se ha buscado
            if st.session_state["mostrar_resultado"] and st.session_state["codigo_producto"]:
                codigo = st.session_state["codigo_producto"]
                st.markdown("###### Resultado de Busqueda")
                tablaStock = pd.DataFrame(
                    datosStock,
                    columns=['id', 'Codigo', 'Nombre', 'Precio', 'Cantidad', 'Proveedor', 'Fecha de Creacion', 'Fecha de Modificacion', 'Estado']
                )
                st.dataframe(
                    tablaStock[['Codigo', 'Nombre', 'Precio', 'Cantidad']],
                    width='stretch',
                    hide_index=True
                )
            if datosStock != []:
                with st.container(border=True):
                    st.markdown("###### Manipular Stock")
                    col5, col6 = st.columns(2, vertical_alignment="bottom")
                    with col5:
                        valor = st.number_input(
                            "Cantidad a manipular",
                            value = 0,
                            min_value = -999,
                            max_value = 999,
                            step = 1,
                            icon = ":material/package_2:"
                        )                    
                    with col6:
                        editar = st.button(
                            "Manipular Stock",
                            help="Al presionar este boton, se actualizara el stock del producto en cuestion",
                            type="primary",
                            use_container_width=True,
                            icon=":material/box_add:"
                        )
                    if editar and valor:
                        # Ejecutar actualización
                        if ADOdb.CreacionInsercion(f"UPDATE productos SET cantidad = cantidad + ({valor}) WHERE codigo = '{codigo}'"):
                            st.success("Producto editado correctamente")
                        else:
                            st.error("Error en la edicion, verifique que la informacion insertada sea coherente")
                            st.stop()
                        # Esperar un poco para que la BD actualice y refrescar tabla
                        esperar(0.5)
                        # Refrescar datos
                        datosStock = ADOdb.ConsultaManual(f"SELECT * FROM productos WHERE codigo = '{codigo}'")
                        tablaStock = pd.DataFrame(
                            datosStock,
                            columns=['id', 'Codigo', 'Nombre', 'Precio', 'Cantidad', 'Proveedor', 'Fecha de Creacion', 'Fecha de Modificacion', 'Estado']
                        )
                        st.dataframe(
                            tablaStock[['Codigo', 'Nombre', 'Precio', 'Cantidad', 'Proveedor', 'Fecha de Creacion', 'Fecha de Modificacion']],
                            width='stretch',
                            hide_index=True
                        )
    else:
        st.error("Error con Base de Datos")

main()