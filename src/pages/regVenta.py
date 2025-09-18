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

    st.title("Punto de Venta")

    # Inicializar session_state para todos los campos necesarios
    for key, default in [
        ("cedula", ""),
        ("seleccionado", ""),
        ("cantidad", 0),
        ("calcularProducto", False),
        ("metodoPago", "Cuotas"),
        ("pagoInicial", 0.0),
        ("cuotasCantidad", 1),
        ("cuotasPrecio", 0.0)
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    # --- Sección Cliente ---
    with st.container(border=True):
        st.markdown("#### Cliente Comprador")
        st.session_state["cedula"] = st.text_input(
            'Cedula del Cliente',
            value=st.session_state["cedula"],
            placeholder="Ej: 12345786",
            key="cedula_input",
            icon=":material/id_card:"
        )
        datosClientes = ADOdb.ConsultaManual(f"SELECT * FROM clientes WHERE cedula = '{st.session_state['cedula']}'")
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
        st.markdown("#### Producto a Vender")
        productos = ADOdb.ConsultarTabla('productos')
        codigos = [str(p[1]) for p in productos]
        nombres = [p[2] for p in productos]
        if not st.session_state["seleccionado"]:
            st.session_state["seleccionado"] = nombres[0] if nombres else ""
        col1, col2, col3 = st.columns(3, vertical_alignment='bottom')
        with col1:
            st.session_state["seleccionado"] = st.selectbox(
                "Selecciona productos",
                nombres,
                index=nombres.index(st.session_state["seleccionado"]) if st.session_state["seleccionado"] in nombres else 0,
                key="producto_select"
            )
        if st.session_state["seleccionado"] in nombres:
            idx = nombres.index(st.session_state["seleccionado"])
            cantidad_disponible = productos[idx][4]
        else:
            cantidad_disponible = 0
        with col2:
            st.session_state["cantidad"] = st.number_input(
                "Unidades",
                min_value=0,
                max_value=cantidad_disponible,
                step=1,
                value=st.session_state["cantidad"],
                key="cantidad_input"
            )
        with col3:
            if st.button("Calcular", use_container_width=True, type='primary', key="calcular_btn"):
                st.session_state["calcularProducto"] = True
        # Mostrar resumen del producto seleccionado
        if st.session_state["calcularProducto"] and st.session_state["cantidad"] > 0:
            precio_unitario = productos[idx][3]
            total_producto = st.session_state["cantidad"] * precio_unitario
            df = pd.DataFrame([{
                "Codigo Producto": codigos[idx],
                "Nombre": nombres[idx],
                "Cantidad a Comprar": st.session_state["cantidad"],
                "Precio Unitario": f"${precio_unitario}",
                "Total": f"${total_producto}"
            }])
            st.dataframe(df, hide_index=True, width='stretch')
        else:
            precio_unitario = 0
            total_producto = 0

    # ...existing code...

    # --- Sección Método de Pago ---
    with st.container(border=True):
        st.markdown("#### Metodo de Pago")
        st.session_state["metodoPago"] = st.selectbox(
            "Metodo", ["Cuotas", "Instantaneo"],
            index=0 if st.session_state["metodoPago"] == "Cuotas" else 1,
            key="metodo_pago_select"
        )
        max_total = float(total_producto) if total_producto else 1.0
        if st.session_state["metodoPago"] == "Cuotas":
            st.session_state["pagoInicial"] = st.number_input(
                "Pago Inicial",
                min_value=0.0,
                max_value=float(max_total),
                value=float(st.session_state["pagoInicial"]),
                step=1.0,
                key="pago_inicial_input",
                help="El valor máximo es el total a pagar"
            )
            st.session_state["cuotasCantidad"] = st.number_input(
                "Cantidad de Cuotas",
                min_value=0,
                max_value=100,
                value=st.session_state["cuotasCantidad"],
                step=1,
                key="cuotas_cantidad_input",
                help="Debe ser un número entero"
            )
            # Calcular el precio de cada cuota automáticamente
            cuotas_restantes = max(1, st.session_state["cuotasCantidad"])
            monto_restante = max(0.0, float(total_producto) - float(st.session_state["pagoInicial"]))
            precio_cuota = monto_restante / cuotas_restantes
            st.session_state["cuotasPrecio"] = precio_cuota
            st.write(f"Precio de cada cuota: ${precio_cuota:,.2f}")
        else:  # Instantaneo
            st.session_state["pagoInicial"] = float(total_producto)
            st.session_state["cuotasCantidad"] = 0
            st.session_state["cuotasPrecio"] = 0.0

    # --- Mostrar Factura y Botón de Venta ---
    if datosClientes and st.session_state["calcularProducto"] and st.session_state["cantidad"] > 0:
        with st.container(border=True):
            st.markdown("# Factura")
            st.markdown(f"- #### C.I. Cliente: {st.session_state['cedula']}")
            st.markdown(f"- #### Cliente: {datosClientes[0][3]}.")
            st.markdown(f"- #### Vendedor: {st.session_state.get('usuario', '---')}.")
            st.markdown(f"- #### Producto: {st.session_state['seleccionado']}.")
            st.markdown(f"- #### Cantidad: {st.session_state['cantidad']} Unidades.")
            st.markdown(f"- #### SubTotal: ${precio_unitario}")
            st.markdown(f"- #### Total: ${total_producto}")
            st.markdown(f"- #### Pago Inicial: ${st.session_state['pagoInicial']}")
            st.markdown(f"- #### Cantidad de Cuotas: {st.session_state['cuotasCantidad']}")
            st.markdown(f"- #### Precio de Cuotas: ${st.session_state['cuotasPrecio']:,.2f}")
            if st.session_state["metodoPago"] == "Cuotas":
                st.markdown(f"- #### Monto a financiar: ${monto_restante:,.2f}")
                st.markdown(f"- #### Cada cuota: ${st.session_state['cuotasPrecio']:,.2f} x {st.session_state['cuotasCantidad']} cuotas")

# ...existing code...
    # --- Botón para realizar la venta ---
    boton = st.button(
        "Realizar Venta",
        use_container_width=True,
        type='primary',
        disabled=(not datosClientes or not st.session_state["calcularProducto"] or not st.session_state["cantidad"] > 0),
        key="realizar_venta_btn"
    )

    # --- Lógica de inserción y actualización de stock ---
    if boton:
        try:
            id_cliente = datosClientes[0][0]
            id_producto = productos[idx][0]
            codigo_producto = productos[idx][1]
            nombre_producto = productos[idx][2]
            precio_unitario = productos[idx][3]
            subtotal = st.session_state["cantidad"] * precio_unitario
            total = subtotal
            vendedor = st.session_state.get('usuario', '---')
            observaciones = ""

            # Determinar valores según método de pago
            if st.session_state["metodoPago"] == "Cuotas":
                inicial = float(st.session_state["pagoInicial"])
                cuotas = int(st.session_state["cuotasCantidad"])
                valor_cuota = float(st.session_state["cuotasPrecio"])
                cuotas_pagadas = 0
                estado_venta = "pendiente"
            else:  # Instantaneo
                inicial = float(total)
                cuotas = 0
                valor_cuota = 0.0
                cuotas_pagadas = 0
                estado_venta = "completada"

            # Consulta de inserción en ventas
            query_venta = """
                INSERT INTO ventas (
                    id_cliente, id_producto, codigo_producto, nombre_producto, cantidad,
                    precio_unitario, subtotal, total, inicial, valor_cuota, metodo_pago,
                    estado_venta, cuotas, cuotas_pagadas, vendedor, observaciones
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores_venta = (
                id_cliente, id_producto, codigo_producto, nombre_producto, st.session_state["cantidad"],
                precio_unitario, subtotal, total, inicial, valor_cuota, st.session_state["metodoPago"],
                estado_venta, cuotas, cuotas_pagadas, vendedor, observaciones
            )
            ok_venta = ADOdb.CreacionInsercion(query_venta, valores_venta)

            # Consulta para actualizar el stock del producto
            query_stock = "UPDATE productos SET cantidad = cantidad - %s WHERE id = %s"
            valores_stock = (st.session_state["cantidad"], id_producto)
            ok_stock = ADOdb.CreacionInsercion(query_stock, valores_stock)

            if ok_venta and ok_stock:
                st.success("Venta Realizada Correctamente")
                # Limpiar los campos de session_state para nueva venta
                for key in ["cedula", "seleccionado", "cantidad", "calcularProducto", "pagoInicial", "cuotasCantidad", "cuotasPrecio"]:
                    st.session_state[key] = "" if isinstance(st.session_state[key], str) else 0
                st.session_state["metodoPago"] = "Cuotas"
            else:
                st.error("Error al realizar venta, contacte a soporte")
        except Exception as e:
            st.error(f"Error inesperado: {e}")

main()