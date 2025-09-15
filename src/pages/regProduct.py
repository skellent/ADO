import streamlit as st

# Importacion de Rich para mejorar la depuracion
from rich import print

# Importacion de clases
from modules.configuracion import ADOconfiguracion
from modules.database import ADOdatabase

# Declaracion de funcion Principal
def main() -> None:
    # Creacion de instancia de configuracion
    ADOconf: object = ADOconfiguracion()
    ADOconf.SetupStreamlit()
    # Creacion de una instancia de database
    ADOdb: object = ADOdatabase(st.secrets)
    # ADOdb.ImprimirValores() # Impresion para verificar correcta creacion

    st.title("Registrar Producto")
    # Crea la tabla en caso de que no exista
    if ADOdb.CreacionInsercion(ADOconf.LeerTOML()['tablas']['productos']):
        with st.form("registro", clear_on_submit = False, enter_to_submit = False):
            # Codigo del Producto
            codigoProducto: str = st.number_input(
                "Codigo del Producto (Obligatorio)",
                help = "Ingrese aqui el codigo del producto a registrar",
                placeholder = "Ej: 10",
                icon = ":material/barcode:",
                min_value = 1,
                step = 1
            )
            # Nombre completo del Cliente a Registrar
            nombre: str = st.text_input(
                "Nombre del Producto (obligatorio)",
                help = "Ingrese aqui el nombre completo del producto a registrar.",
                placeholder = "Ej: Smart TV 16 pulgadas",
                icon = ":material/box:"
            )
            # Numero Telefonioco del Cliente dentro del Sistema
            cantidadInicial: str = st.number_input(
                "Cantidad Inicial en Inventario",
                help = "Ingrese aqui las unidades existentes del producto al momento de su registro",
                placeholder = "Ej: 10",
                icon = ":material/package_2:",
                min_value = 0,
                step = 1
            )
            # Numero Telefonioco del Cliente dentro del Sistema
            precio: str = st.number_input(
                "Precio del Producto (obligatorio)",
                help = "Ingrese aqui el precio de venta del producto",
                placeholder = "Ej: 10.00",
                icon = ":material/paid:",
                min_value = 0.00,
                step = 1.00
            )
            # Ubicacion o Direccion del Cliente
            proveedor: str = st.text_input(
                "Proveedor del Producto",
                help = "Ingrese aqui el nombre del proveedor del producto.",
                placeholder = "Ej: Polar C.A.",
                icon = ":material/enterprise:"
            )
            # Boton de Submit para registrar al Cliente
            boton: bool = st.form_submit_button(
                "Registrar Producto",
                help = 'Al presionar este boton, se registrara el producto si los datos ingresados son validos.',
                type = 'primary',
                use_container_width = True,
                icon = ':material/box_add:'
            )
    else:
        st.error("Error con Base de Datos")

    # Logica para Registro de Cliente
    if boton:
        if codigoProducto and nombre and precio:
            # Se verifica que no exista ya en la base
            if ADOdb.ConsultaManual(f"""SELECT * FROM productos WHERE codigo = '{codigoProducto}'""") == []:
                # Se procede con el registro en la base de datos
                if ADOdb.CreacionInsercion(f"""INSERT INTO productos (codigo, nombre, precio, cantidad, proveedor) VALUES ('{codigoProducto}', '{nombre}', '{precio}', '{cantidadInicial if cantidadInicial else 0}', '{proveedor if proveedor else 'NULL'}')"""):
                    st.success("Producto Registrado")
                else:
                    st.error("Hubo un error al registrar al producto")
            else:
                st.error("Este producto ya existe en la base de datos")
        else:
            st.warning("Ingrese todos los campos obligatorios")

main()