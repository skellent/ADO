import streamlit as st

# Importacion de Rich para mejorar la depuracion
from rich import print

# Importacion de clases
from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase

informacion: str = """
## Módulos
- ### Clientes:
    1. Lista de Clientes: Muestra una tabla con todos los clientes y con herramientas de busqueda.
    2. Registrar Cliente: Permite registrar clientes nuevos en el sistema.
    3. Editar Cliente: Permite editar información de un cliente existente.
- ### Inventario:
    1. Lista de Productos: Muestra una tabla con todos los productos y con herramientas de busqueda.
    2. Registrar Producto: Permite registrar productos nuevos en el sistema.
    3. Editar Producto: Permite editar información de un producto existente.
- ### Ventas:
    1. Historial de Ventas: Muestra el historial de ventas del sistema.
    2. Realizar Venta: Permite realizar ventas de forma simplificada y auto registrable en el sistema.
    3. Cuotas Pendientes: Permite manejar las cuotas pendientes de ventas realizadas.
"""

# Declaracion de funcion Principal
def main() -> None:
    # Creacion de instancia de configuracion
    ADOconf: object = ADOconfiguracion()
    ADOconf.SetupStreamlit()

    st.title("Documentación y Ayuda")
    st.markdown(informacion)

main()