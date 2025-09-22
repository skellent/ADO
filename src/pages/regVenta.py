import streamlit as st

from rich import print

from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase

import pandas as pd
from time import sleep as esperar
import datetime

def main() -> None:
    ADOconf = ADOconfiguracion()
    ADOconf.SetupStreamlit()
    ADOdb = ADOdatabase(st.secrets)

    st.title("Punto de Venta")

    if ADOdb.CreacionInsercion(ADOconf.LeerTOML()['tablas']['ventas']):
        # --- Sección Cliente ---
        with st.container(border=True):
            st.markdown("#### Cliente Comprador")
            cola, colb = st.columns(2, vertical_alignment='top')
            with cola:
                cedulaCliente: str = st.text_input(
                    'Cedula del Cliente',
                    placeholder = "Ej: 12345786",
                    help = "Escriba la cedula del cliente al cual le vendera el producto.",
                    key = "cedula_input",
                    icon = ":material/id_card:"
                )
                datosClientes: tuple = ADOdb.ConsultaManual(f"SELECT * FROM clientes WHERE cedula = '{cedulaCliente}'")
                # Tabla con los datos del cliente
            with colb:
                if datosClientes:
                    tablaClientes = pd.DataFrame(
                        datosClientes,
                        columns=['id', 'Cedula', 'Codigo Socio', 'Nombre', 'Telefono', 'Correo', 'Direccion', 'Descripcion', 'Fecha de Creacion', 'Fecha de Modificacion', 'Estado']
                    )
                    st.dataframe(
                        tablaClientes[['Cedula', 'Codigo Socio', 'Nombre', 'Telefono', 'Correo', 'Direccion', 'Descripcion']],
                        width='stretch',
                        hide_index=True
                    )

        # --- Sección Producto ---
        with st.container(border=True):
            # Titulo del contenedor
            st.markdown("#### Producto a Vender")

            # Obtencion de productos
            productos: list[tuple] = ADOdb.ConsultarTabla('productos')
            codigos = [str(p[1]) for p in productos]
            nombres = [p[2] for p in productos]

            # Columnas
            col1, col2 = st.columns(2, vertical_alignment='bottom')
            # Producto Seleccionado
            with col1:
                productoSeleccionado = st.selectbox(
                    "Selecciona productos",
                    nombres,
                    index = 0,
                    help = "Seleccione de los productos disponibles el que vendera.",
                    key = "producto_select"
                )

            # Formatear Datos
            datosProductoSeleccionado = nombres.index(productoSeleccionado)
            cantidadDisponible = productos[datosProductoSeleccionado][4]

            # Cantidad del Producto
            with col2:
                cantidadProducto = st.number_input(
                    "Unidades",
                    min_value = 0,
                    max_value = cantidadDisponible,
                    step = 1,
                    help = "Indique la cantidad de unidades a vender del producto",
                    icon = ":material/deployed_code:",
                    key = "cantidad_input"
                )
                precioUnitario = productos[datosProductoSeleccionado][3]
                totalProducto = cantidadProducto * precioUnitario
            
            # Tabla con informacion de venta del producto
            df = pd.DataFrame([{
                "Codigo Producto": codigos[datosProductoSeleccionado],
                "Nombre": nombres[datosProductoSeleccionado],
                "Cantidad a Comprar": cantidadProducto,
                "Precio Unitario": f"${precioUnitario}",
                "Total": f"${totalProducto}"
            }])

            # Mostrar tabla
            st.dataframe(
                df, hide_index=True,
                width='stretch'
            )

        # --- Sección Método de Pago ---
        with st.container(border=True):
            st.markdown("#### Metodo de Pago")
            # Columnas
            colx, colz = st.columns(2, vertical_alignment='top')

            # Valor de la inicial
            with colx:
                pagoInicial = st.number_input(
                    "Pago Inicial",
                    min_value = 0.0,
                    max_value = float(totalProducto),
                    step = 1.0,
                    help = "El valor máximo es el total a pagar",
                    icon = ":material/sell:",
                    key = "pago_inicial_input"
                )

            # Cantidad de Cuotas
            with colz:
                cuotasCantidad = st.number_input(
                    "Cantidad de Cuotas",
                    min_value = 0,
                    max_value = 100,
                    step=1,
                    help = "Indique la cantidad de cuotas que debera cancelar el cliente",
                    icon = ":material/handshake:",
                    key = "cuotas_cantidad_input"
                )
            
            cuotasPrecio: float = (float(totalProducto) - float(pagoInicial)) / float(cuotasCantidad) if cuotasCantidad > 0 else 0.0
            st.html(f"<center>Valor Unitario de cada Cuota: ${cuotasPrecio}</center>")

        # -- Text Area con notas sobre la venta
        with st.container(border = True):
            st.markdown("#### Observaciones / Nota de Venta")
            observacionVenta: str = st.text_area(
                "Informacion",
                placeholder = "Notas relevantes sobre la venta",
                help = "Escriba aqui informacion adicional sobre la venta"
            )

        # Detener en caso de no tener un cliente valido, para evitar renderizado de factura
        if datosClientes == []:
            st.stop()

        # -- Factura final + boton de realizar venta
        with st.container(border = True):
            st.markdown("#### Factura Final")
            vendedor: str = st.session_state['usuario']
            plantilla: str = f"""
    ###### Informacion del Cliente
    - C.I. Cliente: {cedulaCliente}
    - Codigo Socio: {datosClientes[0][2]}
    - Cliente: {datosClientes[0][3]}
    ---
    ###### Informacion del Producto
    - Producto a Vender: {productoSeleccionado}
    - Unidades: {cantidadProducto}
    - Precio Unitario: ${precioUnitario}
    - Precio Total: ${totalProducto}
    ---
    ###### Metodo de Pago
    - Pago Inicial: ${pagoInicial}
    - Nro. Cuotas: {cuotasCantidad}
    - Valor de Cuotas: ${cuotasPrecio}
    ###### Informacion Adicional
    - Vendedor: {vendedor}
    - Observacion:
    > {observacionVenta}
    """
            # Informacion
            st.markdown(plantilla)

        # Boton para Realizar la Venta
        if st.button("Realizar Venta", type = 'primary', use_container_width = True):
            consulta1: str = f"""INSERT INTO ventas(
                                id_cliente,
                                id_producto,
                                codigo_producto,
                                nombre_producto,
                                cantidad,
                                precio_unitario,
                                subtotal,
                                total,
                                inicial,
                                valor_cuota,
                                metodo_pago,
                                estado_venta,
                                cuotas,
                                cuotas_pagadas,
                                vendedor,
                                observaciones
                            ) VALUES (
                                {cedulaCliente},
                                {codigos[datosProductoSeleccionado]},
                                '{codigos[datosProductoSeleccionado]}',
                                '{productoSeleccionado}',
                                {cantidadProducto},
                                {precioUnitario},
                                {totalProducto},
                                {totalProducto},
                                {pagoInicial},
                                {cuotasPrecio},
                                'Cuotas',
                                "{"Pendiente" if cuotasCantidad > 0 else "Completada"}",
                                {cuotasCantidad},
                                0,
                                '{vendedor}',
                                '{observacionVenta}'
                            )"""
            if ADOdb.CreacionInsercion(consulta1) and ADOdb.CreacionInsercion(f"UPDATE productos SET cantidad = cantidad - {cantidadProducto}"):
                st.success("Venta Realizada exitosamente")
            else:
                st.error("Ocurrio un error al realizar la venta")
    else:
        st.error("Error con Base de Datos")

main()