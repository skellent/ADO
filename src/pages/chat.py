# Importacion de Librerias
import streamlit as st

from time import sleep as esperar

from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase

import pandas as pd
from time import sleep as esperar
import datetime

# UI del Chat Global
def main():
    ADOconf = ADOconfiguracion()
    ADOconf.SetupStreamlit()
    ADOdb = ADOdatabase(st.secrets)

    st.title("Chat Global")

    if ADOdb.CreacionInsercion(ADOconf.LeerTOML()['tablas']['chat']):
        # Inicializar chat en session_state si no existe
        if 'chat' not in st.session_state:
            st.session_state.chat = ADOdb.ConsultarTabla('chat')
        else:
            st.session_state.chat = ADOdb.ConsultarTabla('chat')

        with st.container(height=450, border=True):
            for mensaje in st.session_state.chat:
                st.chat_message('human').write(f'{mensaje[1]}: {mensaje[2]}')
            if prompt := st.chat_input("Escriba aqui el mensaje a enviar", max_chars=100):
                ADOdb.CreacionInsercion(f"INSERT INTO chat (usuario, mensaje) VALUES ('{st.session_state.usuario}', '{prompt}')")
        esperar(0.5)
        st.rerun()
    else:
        st.error("Hubo un error en el chat, contacte a soporte")

main()