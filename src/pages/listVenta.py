import streamlit as st

# Importacion de Rich para mejorar la depuracion
from rich import print

# Importacion de clases
from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase

# Importar pandas para formatear datos de la tabla
import pandas as pd
import io # Para generar tabla de Excel

# Declaracion de funcion Principal
def main() -> None:
    # Creacion de instancia de configuracion
    ADOconf: object = ADOconfiguracion()
    ADOconf.SetupStreamlit()
    # Creacion de una instancia de database
    ADOdb: object = ADOdatabase(st.secrets)
    # ADOdb.ImprimirValores() # Impresion para verificar correcta creacion

    st.title("Historial de Ventas")

    if ADOdb.CreacionInsercion(ADOconf.LeerTOML()['tablas']['ventas']):
        datosProductos: list = ADOdb.ConsultarTabla('ventas')
        tablaProductos: pd = pd.DataFrame(
            datosProductos,
            columns = ['id', 'Codigo Venta', 'Fecha de Venta', 'Cedula de Cliente', 'Total', 'Productos Vendidos', 'Metodo de Pago', 'Estado Venta', 'Vendedor', 'Observaciones', 'Fecha de Creacion', 'Fecha de Modificacion', 'Estado']
        )
        st.dataframe(
            tablaProductos[['Codigo Venta', 'Fecha de Venta', 'Cedula de Cliente', 'Total', 'Productos Vendidos', 'Metodo de Pago', 'Estado Venta', 'Vendedor', 'Observaciones']],
            width = 'stretch',
            hide_index = True
        )
        # Sistema de descarga de tabla de excel
        output = io.BytesIO()
        try:
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                tablaProductos.to_excel(writer, index=False, sheet_name='Historial')
            excel_data = output.getvalue()
            st.download_button(
                label="Descargar Historial de Ventas como Archivo de Excel",
                data=excel_data,
                file_name="Historial_del_ventas.xlsx",
                use_container_width= True,
                type = 'primary',
                icon = ':material/save:'
            )
        except Exception as e:
            st.error(f"Ocurrió un error al preparar el archivo Excel para descarga: {e}")
            st.write("Asegúrate de tener `openpyxl` instalado (`pip install openpyxl`)")
    else:
        st.error("Error con Base de Datos")

main()