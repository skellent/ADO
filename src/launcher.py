# Importacion de Librerias
import subprocess
import sys
import time
import pyqrcode # type: ignore — Importa pyqrcode

streamlit_script_name = "./main.py"

# Comando para ejecutar Streamlit
comando = [
    sys.executable,
    "-m",
    "streamlit",
    "run",
    streamlit_script_name,
    "--server.port", # Parametro para seleccioanr un puerto
    "8501"
]

# Limpiar la pantalla
import os
os.system('cls' if os.name == 'nt' else 'clear')

print("—" * 80, end="")
print("""
  ╔═════════════════════════╗   ╔══════════════════════════════════════════════╗
┌─║ ▄▄▄ █  ▄ ▄▄▄ ▄  ▄ █ ▄▄▄ ║ ┌─║ Skell's ADO es un software basado en hosting ║
│ ║ █▄▄ █▄▀  █▄▄ █  █   █▄▄ ║ │ ║ que permite gestionar clientes, ventas, in-  ║
│ ║ ▄▄█ █ ▀▄ █▄▄ █▄ █▄  ▄▄█ ║ │ ║ ventario y más dentro de una empresa.        ║
│ ║ ─────  A   D   O  ───── ║ │ ║   — Todos los créditos a Robert Rodríguez —  ║
│ ╚═════════════════════════╝ │ ╚══════════════════════════════════════════════╝
└─────────────────────────┘   └──────────────────────────────────────────────┘""")
proceso = None
urlApp = None

try:
    # Ejecutar Streamlit como un subproceso
    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

    # Busqueda de la URL con temporizador para detener en caso de no encontrarla
    lines_read = 0
    start_time = time.time()
    timeout = 15 # segundos
    max_lines = 30

    while lines_read < max_lines and (time.time() - start_time) < timeout:
        line = proceso.stdout.readline()
        if not line:
            if proceso.poll() is not None:
                 break
            time.sleep(0.1)
            continue

        if "Network URL:" in line:
            urlApp = line.split("Network URL:")[1].strip()
            break
        lines_read += 1

    if urlApp:
        print("\nGenerando código QR para uso desde celulares...")
        try:
            codigoQR = pyqrcode.create(urlApp)
            print("\nCodigo QR para acceso movil:")
            qr_text_representation = codigoQR.text(quiet_zone = 1) # quiet_zone añade un borde
            #remplazo de caracteres
            nuevoCodigoQR = qr_text_representation.replace('1','  ').replace('0','██')
            print(nuevoCodigoQR) # Imprime la cadena directamente

            print("\n" + "—" * 70)
            print(f"Skell's ADO ejecutándose en: {urlApp}\n")
            print("Presiona Ctrl+C aquí para detener la aplicación.")
            print("—" * 70)

        except Exception as qr_error:
            # Captura errores si create() falla o text() falla por alguna razón
            print(f"\nError al generar la representación de texto del código QR con pyqrcode: {qr_error}")
            print(f"La aplicación Streamlit debería estar ejecutándose en: {urlApp}")
            print("Puedes intentar acceder manualmente a esta URL.")
            print("—" * 70)

        # Mantener el script lanzador vivo
        try:
            proceso.wait()
        except KeyboardInterrupt:
            print("\nDeteniendo Skell's ADO...")
            if proceso and proceso.poll() is None:
                 proceso.terminate()
                 proceso.wait()
            print("Skell's CRM detenido.")

    else:
        print("\nNo se pudo encontrar el 'Network URL' en la salida de Streamlit después de esperar.")

except FileNotFoundError:
    print(f"Error: No se encontró el comando 'streamlit' o '{sys.executable}'.")
except Exception as e:
    print(f"Ocurrió un error general al iniciar o manejar el proceso Streamlit: {e}")
    if proceso and proceso.poll() is None:
         proceso.terminate()