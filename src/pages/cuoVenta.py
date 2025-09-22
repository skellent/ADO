import streamlit as st

from rich import print
from time import sleep as esperar

from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase

import pandas as pd
import io

# Declaracion de funcion Principal
def main() -> None:
    # Creacion de instancia de configuracion
    ADOconf: object = ADOconfiguracion()
    ADOconf.SetupStreamlit()
    # Creacion de una instancia de database
    ADOdb: object = ADOdatabase(st.secrets)
    # ADOdb.ImprimirValores() # Impresion para verificar correcta creacion

    st.title("Cuotas Pendientes")

    if ADOdb.CreacionInsercion(ADOconf.LeerTOML()['tablas']['ventas']):
        tab1, tab2 = st.tabs(["Cuotas Pendientes", "Gestion de Cuotas"])
        with tab1:
            # Mostrar todas las ventas con cuotas pendientes
            datosVentas = ADOdb.ConsultaManual('SELECT * FROM ventas WHERE cuotas_pagadas < cuotas and cuotas > 0;')
            tablaVentas = pd.DataFrame(
                datosVentas,
                columns=[
                    'id', 'Fecha de Venta', 'ID Cliente', 'ID Producto', 'Codigo Producto', 'Nombre Producto',
                    'Cantidad', 'Precio Unitario', 'Subtotal', 'Total', 'Inicial', 'Valor Cuota', 'Metodo de Pago',
                    'Estado Venta', 'Cuotas', 'Cuotas Pagadas', 'Vendedor', 'Observaciones',
                    'Fecha de Creacion', 'Fecha de Actualizacion', 'Activo'
                ]
            )
            st.dataframe(
                tablaVentas[
                    ['id', 'Fecha de Venta', 'ID Cliente', 'Codigo Producto', 'Nombre Producto', 'Cantidad',
                    'Precio Unitario', 'Subtotal', 'Total', 'Inicial', 'Valor Cuota', 'Metodo de Pago',
                    'Estado Venta', 'Cuotas', 'Cuotas Pagadas', 'Vendedor', 'Observaciones']
                ],
                width='stretch',
                hide_index=True
            )
            # Sistema de descarga de tabla de excel
            output = io.BytesIO()
            try:
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    tablaVentas.to_excel(writer, index=False, sheet_name='Historial')
                excel_data = output.getvalue()
                st.download_button(
                    label="Descargar Historial de Ventas como Archivo de Excel",
                    data=excel_data,
                    file_name="Historial_de_ventas.xlsx",
                    use_container_width=True,
                    type='primary',
                    icon=':material/save:'
                )
            except Exception as e:
                st.error(f"Ocurrió un error al preparar el archivo Excel para descarga: {e}")
                st.write("Asegúrate de tener `openpyxl` instalado (`pip install openpyxl`)")
        with tab2:
            with st.form(key='buscarCliente', enter_to_submit=True):
                if "codigoVenta" not in st.session_state:
                    st.session_state["codigoVenta"] = ""
                if "mostrar_resultado" not in st.session_state:
                    st.session_state["mostrar_resultado"] = False
                col1, col2 = st.columns(2, vertical_alignment='bottom')
                with col1:
                    idVenta = st.text_input(
                        'ID de Venta',
                        value = st.session_state["codigoVenta"],
                        placeholder="Ej: 12",
                        icon=":material/format_list_numbered:"
                    )
                with col2:
                    buscar = st.form_submit_button(
                        "Buscar Cuota",
                        help="Al presionar este boton, automaticamente se mostraran los datos del cliente si este existe",
                        type="primary",
                        use_container_width=True,
                        icon=":material/search:"
                    )
            
            if buscar:
                st.session_state["codigoVenta"] = idVenta
                st.session_state["mostrar_resultado"] = True

            # Solo mostrar resultado si se ha buscado
            if st.session_state["mostrar_resultado"] and st.session_state["codigoVenta"]:
                idVenta = st.session_state["codigoVenta"]
                datosVenta = ADOdb.ConsultaManual(f'SELECT * FROM ventas WHERE cuotas_pagadas < cuotas and cuotas > 0 and id = {idVenta};')
                st.markdown("###### Resultado de Busqueda")
                tablaVenta = pd.DataFrame(
                    datosVenta,
                    columns=[
                        'id', 'Fecha de Venta', 'ID Cliente', 'ID Producto', 'Codigo Producto', 'Nombre Producto',
                        'Cantidad', 'Precio Unitario', 'Subtotal', 'Total', 'Inicial', 'Valor Cuota', 'Metodo de Pago',
                        'Estado Venta', 'Cuotas', 'Cuotas Pagadas', 'Vendedor', 'Observaciones',
                        'Fecha de Creacion', 'Fecha de Actualizacion', 'Activo'
                    ]
                )
                st.dataframe(
                    tablaVenta[
                        ['ID Cliente', 'Codigo Producto', 'Cantidad',
                        'Precio Unitario', 'Subtotal', 'Total', 'Inicial', 'Valor Cuota',
                        'Cuotas', 'Cuotas Pagadas', 'Observaciones']
                    ],
                    width='stretch',
                    hide_index=True
                )
                
                # st.stop()
                
                if datosVenta != []:
                    st.markdown("###### Manejo de Cuota")
                    with st.container(border=True):
                        # Observaciones modificables, en caso de estar en blanco no modificar las existentes.
                        observacion = st.text_area(
                            "Observaciones",
                            help="Escriba aqui alguna observacion que considere importante sobre el pago de la cuota",
                            key="info_observacion"
                        )
                    with st.container(border=True):
                        # Cantidad de Cuotas pagadas (Aqui mediante un st.number se suma a las cuotas pagadas el valor indicado por el usuario) y otros datos son llenados automaticamente
                        col5, col6 = st.columns(2, vertical_alignment="center")
                        with col5:
                            valor = st.number_input(
                                "Cantidad de Cuotas a Cancelar",
                                value = 0,
                                min_value = 0,
                                max_value = 999,
                                step = 1,
                                icon = ":material/sell:"
                            )                    
                        with col6:
                            # Total a Pagar
                            st.write(f"Valor Total a Pagar: ${valor * int(tablaVenta['Valor Cuota'].values[0])}")
                            # Cuotas restantes por cancelar
                            st.write(f"Cuotas Restantes: {int(tablaVenta['Cuotas'].values[0]) - (int(tablaVenta['Cuotas Pagadas'].values[0]) + valor)}")
                        editar = st.button(
                                "Pagar Cuotas",
                                help="Al presionar este boton, se actualizaran las cuotas pagadas",
                                type="primary",
                                use_container_width=True,
                                icon=":material/box_add:"
                            )
                        if editar:
                            if valor > 0:
                                nuevasCuotasPagadas = int(tablaVenta['Cuotas Pagadas'].values[0]) + valor
                                if nuevasCuotasPagadas > int(tablaVenta['Cuotas'].values[0]):
                                    st.error("Error: La cantidad de cuotas a pagar excede las cuotas pendientes.")
                                    st.stop()
                                else:
                                    # Actualizar la base de datos
                                    consulta1: str = f"""UPDATE ventas SET 
                                        cuotas_pagadas = {nuevasCuotasPagadas},
                                        estado_venta = '{"Pendiente" if nuevasCuotasPagadas < int(tablaVenta['Cuotas'].values[0]) else "Completada"}',
                                        observaciones = '{observacion if observacion != "" else tablaVenta['Observaciones'].values[0]}',
                                        fecha_actualizacion = CURRENT_TIMESTAMP
                                        WHERE id = {idVenta};
                                    """
                                    resultado = ADOdb.CreacionInsercion(consulta1)
                                    if resultado is not None:
                                        st.success("Cuotas actualizadas correctamente")
                                        esperar(2)
                                        st.session_state["mostrar_resultado"] = False
                                        st.session_state["codigoVenta"] = ""
                                        st.rerun()
                                    else:
                                        st.error("Error al actualizar las cuotas")
                            else:
                                st.error("Error: La cantidad de cuotas a pagar debe ser mayor a 0")
    else:
        st.error("Error con Base de Datos")

main()