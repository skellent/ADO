import streamlit as st

# Importacion de Rich para mejorar la depuracion
from rich import print

# Importacion de clases
from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase

# Importacion de pandas
import pandas as pd

# Declaracion de funcion Principal
def main() -> None:
    # Creacion de instancia de configuracion
    ADOconf: object = ADOconfiguracion()
    ADOconf.SetupStreamlit()
    # Creacion de una instancia de database
    ADOdb: object = ADOdatabase(st.secrets)
    # ADOdb.ImprimirValores() # Impresion para verificar correcta creacion

    st.title("Editar Informacion de Cliente")
    # Crea la tabla en caso de que no exista
    if ADOdb.CreacionInsercion(ADOconf.LeerTOML()['tablas']['clientes']):
        cedula: str = st.text_input('Cedula del Cliente')
        if st.button('Buscar Cliente'):
            # Resultado de Busqueda
            datosClientes: list = ADOdb.ConsultaManual(f"""SELECT * FROM clientes WHERE cedula = '{cedula}'""")
            st.subheader("Resultado de Busqueda")
            tablaClientes: pd = pd.DataFrame(
                datosClientes,
                columns = ['id', 'Cedula', 'Codigo Socio', 'Nombre', 'Telefono', 'Correo', 'Direccion', 'Descripcion', 'Fecha de Creacion', 'Fecha de Modificacion', 'Estado']
            )
            st.dataframe(
                tablaClientes[['Cedula', 'Codigo Socio', 'Nombre', 'Telefono', 'Correo', 'Direccion', 'Descripcion', 'Fecha de Creacion', 'Fecha de Modificacion']],
                width = 'stretch',
                hide_index = True
            )
    else:
        st.error("Error con Base de Datos")

main()