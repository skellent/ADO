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

    st.title("Listado de Productos")

    # Crea la tabla en caso de que no exista
    if ADOdb.CreacionInsercion(ADOconf.LeerTOML()['tablas']['productos']):
        datosProductos: list = ADOdb.ConsultarTabla('productos')
        tablaProductos: pd = pd.DataFrame(
            datosProductos,
            columns = ['id', 'Codigo', 'Nombre', 'Precio', 'Cantidad', 'Proveedor', 'Fecha de Creacion', 'Fecha de Modificacion', 'Estado']
        )
        st.dataframe(
            tablaProductos[['Codigo', 'Nombre', 'Precio', 'Cantidad', 'Proveedor', 'Fecha de Creacion', 'Fecha de Modificacion']],
            width = 'stretch',
            hide_index = True
        )
        # Sistema de descarga de tabla de excel
        output = io.BytesIO()
        try:
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                tablaProductos.to_excel(writer, index=False, sheet_name='Lista')
            excel_data = output.getvalue()
            st.download_button(
                label="Descargar Listado de Productos como Archivo de Excel",
                data=excel_data,
                file_name="Listado_de_Productos.xlsx",
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