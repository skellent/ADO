import streamlit as st

# Importacion de Rich para mejorar la depuracion
from rich import print

# Importacion de clases
from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase

# Declaracion de funcion Principal
def main() -> None:
    ADOconf: object = ADOconfiguracion()
    ADOconf.SetupStreamlit()

main()