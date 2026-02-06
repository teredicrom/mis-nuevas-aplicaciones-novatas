import os
import shutil
import sys
import ctypes
import subprocess
import platform
import time

# --- CONFIGURACIÓN DE COLORES ---
class Colores:
    VERDE = '\033[92m'   
    ROJO = '\033[91m'    
    AMARILLO = '\033[93m'
    AZUL = '\033[94m'    
    CYAN = '\033[96m'    
    BLANCO = '\033[97m'  
    RESET = '\033[0m'    

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def es_administrador():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def imprimir_estado(mensaje, tipo="info"):
    if tipo == "exito":
        print(f"{Colores.VERDE}[OK]{Colores.RESET} {mensaje}")
    elif tipo == "error":
        print(f"{Colores.ROJO}[X]{Colores.RESET} {mensaje}")
    elif tipo == "aviso":
        print(f"{Colores.AMARILLO}[!]{Colores.RESET} {mensaje}")
    else:
        print(f"{Colores.AZUL}[INFO]{Colores.RESET} {mensaje}")

# --- ARTE Y DISEÑO ---
def imprimir_header_arte():
    pad = " " * 22 
    print(f"\n{pad}{Colores.ROJO}      |{Colores.RESET}")     
    print(f"{pad}{Colores.ROJO}      |{Colores.RESET}")
    print(f"{pad}{Colores.VERDE}     /=\\{Colores.RESET}")    
    print(f"{pad}{Colores.VERDE}     | |{Colores.RESET}")     
    print(f"{pad}{Colores.VERDE}     | |{Colores.RESET}")
    print(f"{pad}{Colores.VERDE}     \\=/{Colores.RESET}")    
    print(f"{pad}{Colores.ROJO}     |||{Colores.RESET}")     
    print(f"{pad}{Colores.ROJO}     [---]{Colores.RESET}")    

def imprimir_creditos():
    pad = " " * 17 
    print(f"\n{pad}{Colores.CYAN}╔════════════════╗{Colores.RESET}")
    print(f"{pad}{Colores.CYAN}║   {Colores.AMARILLO}TEREDICROM   {Colores.CYAN}║{Colores.RESET}")
    print(f"{pad}{Colores.CYAN}╚════════════════╝{Colores.RESET}")

def obtener_info_windows():
    try:
        comando = 'REG QUERY "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" /v ProductName'
        resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)
        if resultado.returncode == 0:
            for linea in resultado.stdout.splitlines():
                if "ProductName" in linea:
                    return linea.split("REG_SZ")[-1].strip()
        return "Windows Detectado"
    except Exception:
        return "Sistema Windows"

# --- NUEVA FUNCIÓN: EVALUACIÓN Y DIAGNÓSTICO ---
def evaluar_sistema():
    print(f"\n{Colores.AMARILLO}" + "="*60)
    print(" INICIANDO EVALUACIÓN (MODO SOLO LECTURA)")
    print(" Buscando errores sin modificar el sistema...")
    print("="*60 + f"{Colores.RESET}")

    errores_encontrados = 0
    
    # 1. Chequeo de Imagen (Health Check)
    print(f"\n{Colores.CYAN}[PASO 1] Evaluando salud de la imagen de Windows...{Colores.RESET}")
    print("Espere un momento...")
    # /ScanHealth solo mira, no toca.
    resultado_dism = subprocess.run("DISM /Online /Cleanup-Image /ScanHealth", shell=True)
    
    # 2. Chequeo de Archivos (Verify Only)
    print(f"\n{Colores.CYAN}[PASO 2] Verificando integridad de archivos (SFC)...{Colores.RESET}")
    print("Esto compara tus archivos con los oficiales de Microsoft.")
    # /VerifyOnly solo mira, no repara.
    resultado_sfc = subprocess.run("sfc /verifyonly", shell=True)

    print(f"\n{Colores.BLANCO}" + "="*60)
    print(f"       RESULTADO DEL DIAGNÓSTICO TEREDICROM")
    print("="*60 + f"{Colores.RESET}")

    # Interpretación de resultados
    if resultado_dism.returncode == 0:
        print(f"{Colores.VERDE}[✓] IMAGEN DE WINDOWS:{Colores.RESET} Saludable. No se requiere cirugía mayor.")
    else:
        errores_encontrados += 1
        print(f"{Colores.ROJO}[X] IMAGEN DE WINDOWS:{Colores.RESET} DAÑADA.")
        print(f"    {Colores.AMARILLO}Explicación:{Colores.RESET} Los archivos base de instalación están corruptos.")
        print(f"    {Colores.AMARILLO}Solución:{Colores.RESET} Debes ejecutar la Opción 2 del menú.")

    if resultado_sfc.returncode == 0:
        print(f"{Colores.VERDE}[✓] ARCHIVOS DEL SISTEMA:{Colores.RESET} Correctos. Todos los drivers básicos parecen estar bien.")
    else:
        errores_encontrados += 1
        print(f"{Colores.ROJO}[X] ARCHIVOS DEL SISTEMA:{Colores.RESET} CORRUPTOS O MODIFICADOS.")
        print(f"    {Colores.AMARILLO}Explicación:{Colores.RESET} Windows encontró archivos (dll, exe, drivers) que no coinciden con el original.")
        print(f"    {Colores.AMARILLO}Solución:{Colores.RESET} Ejecuta la Opción 2 para que el programa descargue los originales.")

    print("-" * 60)
    if errores_encontrados == 0:
        print(f"{Colores.VERDE}CONCLUSIÓN: Tu sistema está sano. Solo se recomienda limpieza de basura (Opción 1).{Colores.RESET}")
    else:
        print(f"{Colores.ROJO}CONCLUSIÓN: Se detectaron problemas graves.{Colores.RESET}")
        print(f"Se RECOMIENDA ENCARECIDAMENTE ejecutar la {Colores.CYAN}Opción 4 (Mantenimiento Completo){Colores.RESET}.")

# --- FUNCIONES DE MANTENIMIENTO (YA EXISTENTES) ---
def reparacion_sistema():
    print(f"\n{Colores.AMARILLO}" + "="*52)
    print(" INICIANDO PROTOCOLO DE REPARACIÓN")
    print(" NO CIERRES ESTA VENTANA.")
    print("="*52 + f"{Colores.RESET}")
    imprimir_estado("Analizando imagen del sistema (DISM)...", "info")
    try:
        subprocess.run("DISM /Online /Cleanup-Image /RestoreHealth", shell=True)
        imprimir_estado("Imagen de sistema restaurada.", "exito")
    except Exception as e:
        imprimir_estado(f"Error en DISM: {e}", "error")
    imprimir_estado("Buscando archivos corruptos (SFC)...", "info")
    try:
        subprocess.run("sfc /scannow", shell=True)
        imprimir_estado("Escaneo y reparación finalizados.", "exito")
    except Exception as e:
        imprimir_estado(f"Error en SFC: {e}", "error")

def limpiar_carpeta(ruta):
    if not os.path.exists(ruta): return
    imprimir_estado(f"Limpiando ruta: {ruta}", "info")
    contador = 0
    for nombre in os.listdir(ruta):
        camino = os.path.join(ruta, nombre)
        try:
            if os.path.isfile(camino) or os.path.islink(camino):
                os.unlink(camino)
                contador += 1
            elif os.path.isdir(camino):
                shutil.rmtree(camino)
                contador += 1
        except:
            pass 
    if contador > 0:
        imprimir_estado(f"Se eliminaron {contador} elementos basura.", "exito")
    else:
        imprimir_estado("Nada que limpiar aquí.", "info")

def limpiar_dns():
    imprimir_estado("Limpiando caché DNS...", "info")
    subprocess.run("ipconfig /flushdns", shell=True)
    imprimir_estado("Conexión de red refrescada.", "exito")

# --- MENÚ PRINCIPAL ---
def mostrar_menu():
    os.system('') 
    limpiar_pantalla()
    info_windows = obtener_info_windows()
    
    while True:
        imprimir_header_arte()
        imprimir_creditos()
        
        print(f"\n{Colores.CYAN}" + "╔" + "═"*50 + "╗")
        print(f"║           DOCTOR DE PC - PRO v4.0                ║")
        print(f"╠" + "═"*50 + "╣")
        print(f"║  SISTEMA: {Colores.BLANCO}{info_windows.center(39)}{Colores.CYAN}║")
        print("╚" + "═"*50 + "╝" + f"{Colores.RESET}")
        
        print(f"{Colores.VERDE}1.{Colores.RESET} Limpieza de Archivos Temporales")
        print(f"{Colores.VERDE}2.{Colores.RESET} Reparación Profunda (SFC + DISM)")
        print(f"{Colores.VERDE}3.{Colores.RESET} Reparar Red (DNS)")
        print(f"{Colores.VERDE}4.{Colores.RESET} Mantenimiento COMPLETO")
        print(f"{Colores.AMARILLO}5. DIAGNÓSTICO (Solo evaluar, no reparar){Colores.RESET}")
        print(f"{Colores.ROJO}6. Salir{Colores.RESET}")
        
        opcion = input(f"\n{Colores.CYAN}> Selecciona una opción: {Colores.RESET}")

        temp_user = os.environ.get('TEMP')
        temp_win = "C:/Windows/Temp"

        if opcion == '1':
            limpiar_carpeta(temp_user)
            limpiar_carpeta(temp_win)
        elif opcion == '2':
            reparacion_sistema()
        elif opcion == '3':
            limpiar_dns()
        elif opcion == '4':
            limpiar_carpeta(temp_user)
            limpiar_carpeta(temp_win)
            limpiar_dns()
            reparacion_sistema()
            print(f"\n{Colores.VERDE}[!] MANTENIMIENTO FINALIZADO.{Colores.RESET}")
        elif opcion == '5':
            evaluar_sistema()
            print(f"\n{Colores.AZUL}[INFO] Este fue solo un reporte. Usa otras opciones para arreglarlo.{Colores.RESET}")
        elif opcion == '6':
            print("Saliendo...")
            time.sleep(1)
            sys.exit()
        
        input(f"\n{Colores.AMARILLO}Presiona ENTER para volver al menú...{Colores.RESET}")
        limpiar_pantalla()

if __name__ == "__main__":
    if not es_administrador():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        mostrar_menu()
