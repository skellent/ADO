import streamlit as st

from rich import print
from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase

import pandas as pd
import io

def main() -> None:
    ADOconf = ADOconfiguracion()
    ADOconf.SetupStreamlit()
    ADOdb = ADOdatabase(st.secrets)

    st.title("Historial de Ventas")

    if ADOdb.CreacionInsercion(ADOconf.LeerTOML()['tablas']['ventas']):
        datosVentas = ADOdb.ConsultarTabla('ventas')
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
    else:
        st.error("Error con Base de Datos")

main()