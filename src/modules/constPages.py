import streamlit as st

# Opci
instalacion: dict = {
    "Instalacion": [
        st.Page("pages/instalacion.py", title="Completar Instalación")
    ],
    "Información": [
        st.Page("pages/ayuda.py", title="Ayuda con la Aplicación"),
        st.Page("pages/about.py", title="Acerca de Skell's ADO")
    ],
}

login: dict = {
    "Cuentas": [
        st.Page("pages/login.py", title="Inicio")
    ],
    "Información": [
        st.Page("pages/ayuda.py", title="Ayuda con la Aplicación"),
        st.Page("pages/about.py", title="Acerca de Skell's ADO")
    ]
}

administrador: dict = {
    "Clientes": [
        st.Page("pages/listClientes.py", title="Lista de Clientes"),
        st.Page("pages/regCliente.py", title="Registrar Cliente"),
        st.Page("pages/editCliente.py", title="Editar Cliente")
    ],
    "Inventario": [
        st.Page("pages/listProduct.py", title="Lista de Productos"),
        st.Page("pages/regProduct.py", title="Registrar Producto"),
        st.Page("pages/editProduct.py", title="Editar Producto")
    ],
    "Ventas": [
        st.Page("pages/listVenta.py", title="Historial de Ventas"),
        st.Page("pages/regVenta.py", title="Realizar Venta"),
        st.Page("pages/cuoVenta.py", title="Cuotas Pendientes")
    ],
    "Información": [
        st.Page("pages/ayuda.py", title="Ayuda con la Aplicación"),
        st.Page("pages/about.py", title="Acerca de Skell's ADO")
    ]
}

"""
## Modulos
- ### Clientes:
    1. Lista de Clientes
    1. Registrar Cliente
    1. Editar Cliente
- ### Inventario:
    1. Lista de Productos
    1. Registrar Producto
    1. Editar Producto
- ### Ventas:
    1. Historial de Ventas
    1. Realizar Venta
    1. Cuotas Pendientes
"""