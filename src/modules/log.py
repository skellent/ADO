import functools
import logging
from datetime import datetime
from typing import Callable, Any

def logger_acciones(
    nombre_archivo: str = "historial.log",
    nivel: int = logging.INFO,
    formato: str = "[%(asctime)s] - [%(levelname)s] - %(message)s",
    incluir_args: bool = True,
    incluir_resultado: bool = False,
    incluir_tiempo_ejecucion: bool = True
) -> Callable:
    """
    Decorador plantilla para logging de acciones.
    
    Args:
        nombre_archivo (str): Nombre del archivo de log. Default: 'acciones.log'
        nivel (int): Nivel de logging. Default: logging.INFO
        formato (str): Formato del mensaje de log. Default: '%(asctime)s - %(levelname)s - %(message)s'
        incluir_args (bool): Si incluye argumentos en el log. Default: True
        incluir_resultado (bool): Si incluye el resultado de la función. Default: False
        incluir_tiempo_ejecucion (bool): Si incluye tiempo de ejecución. Default: True
    """
    # Configurar logging
    logging.basicConfig(
        filename=nombre_archivo,
        level=nivel,
        format=formato,
        encoding='utf-8'
    )
    def decorador(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Información inicial
            tiempo_inicio = datetime.now()
            nombre_funcion = func.__name__      
            # Registrar inicio
            mensaje_inicio = f"INICIO: {nombre_funcion}"
            if incluir_args and (args or kwargs):
                mensaje_inicio += f" - Args: {args}, Kwargs: {kwargs}"
            logging.info(mensaje_inicio)
            try:
                # Ejecutar función
                resultado = func(*args, **kwargs)
                tiempo_ejecucion = (datetime.now() - tiempo_inicio).total_seconds()
                # Registrar éxito
                mensaje_exito = f"EXITO: {nombre_funcion}"
                if incluir_tiempo_ejecucion:
                    mensaje_exito += f" - Tiempo: {tiempo_ejecucion:.4f}s"
                if incluir_resultado and resultado is not None:
                    mensaje_exito += f" - Resultado: {resultado}"
                logging.info(mensaje_exito)
                return resultado
            except Exception as e:
                # Registrar error
                tiempo_ejecucion = (datetime.now() - tiempo_inicio).total_seconds()
                mensaje_error = f"ERROR: {nombre_funcion} - {type(e).__name__}: {str(e)}"
                if incluir_tiempo_ejecucion:
                    mensaje_error += f" - Tiempo: {tiempo_ejecucion:.4f}s"
                logging.error(mensaje_error)
                raise  # Relanza la excepción
        
        return wrapper
    return decorador

# -------------------------------------------------------------------
# EJEMPLOS DE USO PERSONALIZABLES
# -------------------------------------------------------------------
def main():
    # 1. Uso básico
    @logger_acciones()
    def crear_usuario(nombre: str, email: str):
        """Función de ejemplo para crear usuario."""
        # Lógica de creación...
        return f"Usuario {nombre} creado"

    # 2. Logging detallado
    @logger_acciones(
        nombre_archivo="transacciones.log",
        incluir_resultado=True,
        incluir_tiempo_ejecucion=True
    )
    def procesar_venta(monto: float, producto: str):
        """Procesa una venta."""
        # Lógica de venta...
        return {"estado": "éxito", "monto": monto}

    # 3. Logging mínimo
    @logger_acciones(
        nombre_archivo="errores.log",
        nivel=logging.ERROR,
        incluir_args=False,
        incluir_tiempo_ejecucion=False
    )
    def funcion_critica():
        """Solo loggea errores."""
        # Lógica crítica...
        pass

    # 4. Para métodos de clase
    class MiClase:
        @logger_acciones(nombre_archivo="clase_actions.log")
        def metodo_importante(self, valor: int):
            """Método de clase con logging."""
            return valor * 2

    # -------------------------------------------------------------------
    # USO PRÁCTICO EN TU PROYECTO
    # -------------------------------------------------------------------

    # Ejemplos de uso
    usuario = crear_usuario("Ana", "ana@empresa.com")
    venta = procesar_venta(150.50, "Laptop")

    # Ver contenido del log
    with open("historial.log", "r", encoding="utf-8") as f:
        print("Contenido del log:")
        print(f.read())

if __name__ == "__main__":
    main()  