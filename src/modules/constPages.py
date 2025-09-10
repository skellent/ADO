import streamlit as st

instalacion = {
    "Instalacion": [
        st.Page("pages/instalacion.py", title="Completar Instalación")
    ],
    "Información": [
        st.Page("pages/ayuda.py", title="Ayuda con la Aplicación"),
        st.Page("pages/about.py", title="Acerca de Skell's ADO"),
    ],
}

login = {
    "Cuentas": [
        st.Page("pages/login.py", title="Inicio")
    ],
    "Información": [
        st.Page("pages/ayuda.py", title="Ayuda con la Aplicación"),
        st.Page("pages/about.py", title="Acerca de Skell's ADO"),
    ],
}