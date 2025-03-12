import socket
import sys

# Colores para la terminal
cColorRojo = '\033[1;31m'
cColorVerde = '\033[1;32m'
cColorAzul = '\033[1;34m'
cFinColor = '\033[0m'

def mostrar_mensaje_inicial():
    print(cColorAzul + "\n===============================" + cFinColor)
    print(cColorVerde + "      ⚙️  Aviso Navegante ⚙️" + cFinColor)
    print(cColorAzul + "===============================" + cFinColor)
    print("\nEstas son las opciones que tienes para el script:\n")
    print(cColorVerde + "  - encender   ➜ Enciende el PLC" + cFinColor)
    print(cColorRojo + "  - apagar     ➜ Apaga el PLC" + cFinColor)
    print(cColorVerde + "  - modificar  ➜ Modifica las salidas del PLC" + cFinColor)
    print("\nParámetros de uso:\n")
    print("  " + cColorAzul + "python3 script.py [IP plc] [opción]" + cFinColor)
    print("\nEjemplo:")
    print("  python3 script.py 192.168.1.100 encender")
    print("  python3 script.py 192.168.1.100 apagar")
    print("  python3 script.py 192.168.1.100 modificar Q0.0 on")
    print(cColorAzul + "\n===============================" + cFinColor + "\n")

def fConectar(pHost):
    print(f"Intentando conectar con {pHost} en el puerto 102...")
    vSocketPLC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vSocketPLC.settimeout(5)
    try:
        vSocketPLC.connect((pHost, 102))
        print("\n  Conexión establecida.")
        return vSocketPLC
    except socket.error as e:
        print(f"\n  Error al conectar con el PLC: {e}")
        return None

def fModificarSalida(pHost, salida, estado):
    vSocketPLC = fConectar(pHost)
    if not vSocketPLC:
        return

    vComando = {
        "on": '0300002502f08032010000001f000e00060501120a10010001000082000000000300010100',
        "off": '0300002502f08032010000001f000e00060501120a10010001000082000000000300010000'
    }

    if estado not in vComando:
        print(cColorRojo + "\n  Estado no válido. Usa 'on' o 'off'. \n" + cFinColor)
        return

    print(f"\n  Modificando salida {salida} a estado {estado}...\n")
    fEnviarPayload(vComando[estado], vSocketPLC)
    print(f"\n  Salida {salida} modificada correctamente.\n")
    vSocketPLC.close()

def fEnviarPayload(pData, pSocket):
    print(f"Intentando enviar: {pData}")
    pSocket.send(bytearray.fromhex(pData))
    try:
        vResp = pSocket.recv(1024)
        if vResp:
            print(f"\n  Respuesta del PLC: {vResp.hex()} \n")
        else:
            print("\n  No se recibió respuesta del PLC. \n")
        return vResp
    except socket.timeout:
        print("\n  Se esperó 5 segundos y el PLC no respondió.")
        return None

def fEncenderPLC(pHost):
    vSocketPLC = fConectar(pHost)
    if not vSocketPLC:
        return
    
    vPayloadEncender = '0300004302f0807202003431000004f200000010000003ca3400000034019077000803000004e88969'
    fEnviarPayload(vPayloadEncender, vSocketPLC)
    print("\n  PLC iniciado correctamente \n.")
    vSocketPLC.close()

def fApagarPLC(pHost):
    vSocketPLC = fConectar(pHost)
    if not vSocketPLC:
        return
    
    vPayloadApagar = '0300004302f0807202003431000004f200000010000003ca3400000034019077000801000004e88969'
    fEnviarPayload(vPayloadApagar, vSocketPLC)
    print("\n  PLC detenido correctamente. \n")
    vSocketPLC.close()

if __name__ == "__main__":
    mostrar_mensaje_inicial()
    if len(sys.argv) < 3:
        print(cColorRojo + "\n  Uso incorrecto. Debes indicar la IP del PLC y la acción a realizar. \n" + cFinColor)
        print("  Uso correcto: python3 script.py [IPDelPLC] [encender|apagar|modificar] [salida] [on|off] \n")
    else:
        vHost = sys.argv[1]
        accion = sys.argv[2].lower()
        if accion == "encender":
            fEncenderPLC(vHost)
        elif accion == "apagar":
            fApagarPLC(vHost)
        elif accion == "modificar" and len(sys.argv) == 5:
            salida = sys.argv[3]
            estado = sys.argv[4].lower()
            fModificarSalida(vHost, salida, estado)
        else:
            print(cColorRojo + "\n  Acción no válida o parámetros incorrectos. \n" + cFinColor)
