import socket
import sys

# Terminal colors
cColorRojo = '\033[1;31m'
cColorVerde = '\033[1;32m'
cColorAzul = '\033[1;34m'
cFinColor = '\033[0m'

def mostrar_mensaje_inicial():
    print(cColorAzul + "\n===============================" + cFinColor)
    print(cColorVerde + "      ⚙️  Navigator Notice ⚙️" + cFinColor)
    print(cColorAzul + "===============================" + cFinColor)
    print("\nThese are the available options for the script:\n")
    print(cColorVerde + "  - power_on   ➜ Turns on the PLC" + cFinColor)
    print(cColorRojo + "  - power_off  ➜ Turns off the PLC" + cFinColor)
    print(cColorVerde + "  - modify     ➜ Modifies the PLC outputs" + cFinColor)
    print("\nUsage parameters:\n")
    print("  " + cColorAzul + "python3 script.py [PLC IP] [option]" + cFinColor)
    print("\nExample:")
    print("  python3 script.py 192.168.1.100 power_on")
    print("  python3 script.py 192.168.1.100 power_off")
    print("  python3 script.py 192.168.1.100 modify Q0.0 on")
    print(cColorAzul + "\n===============================" + cFinColor + "\n")

def fConectar(pHost):
    print(f"Trying to connect to {pHost} on port 102...")
    vSocketPLC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vSocketPLC.settimeout(5)
    try:
        vSocketPLC.connect((pHost, 102))
        print("\n  Connection established.")
        return vSocketPLC
    except socket.error as e:
        print(f"\n  Error connecting to the PLC: {e}")
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
        print(cColorRojo + "\n  Invalid state. Use 'on' or 'off'. \n" + cFinColor)
        return

    print(f"\n  Modifying output {salida} to state {estado}...\n")
    fEnviarPayload(vComando[estado], vSocketPLC)
    print(f"\n  Output {salida} modified successfully.\n")
    vSocketPLC.close()

def fEnviarPayload(pData, pSocket):
    print(f"Trying to send: {pData}")
    pSocket.send(bytearray.fromhex(pData))
    try:
        vResp = pSocket.recv(1024)
        if vResp:
            print(f"\n  PLC response: {vResp.hex()} \n")
        else:
            print("\n  No response received from the PLC. \n")
        return vResp
    except socket.timeout:
        print("\n  Waited 5 seconds, but the PLC did not respond.")
        return None

def fEncenderPLC(pHost):
    vSocketPLC = fConectar(pHost)
    if not vSocketPLC:
        return
    
    vPayloadEncender = '0300004302f0807202003431000004f200000010000003ca3400000034019077000803000004e88969'
    fEnviarPayload(vPayloadEncender, vSocketPLC)
    print("\n  PLC started successfully.\n")
    vSocketPLC.close()

def fApagarPLC(pHost):
    vSocketPLC = fConectar(pHost)
    if not vSocketPLC:
        return
    
    vPayloadApagar = '0300004302f0807202003431000004f200000010000003ca3400000034019077000801000004e88969'
    fEnviarPayload(vPayloadApagar, vSocketPLC)
    print("\n  PLC stopped successfully.\n")
    vSocketPLC.close()

if __name__ == "__main__":
    mostrar_mensaje_inicial()
    if len(sys.argv) < 3:
        print(cColorRojo + "\n  Incorrect usage. You must specify the PLC IP and the action to perform. \n" + cFinColor)
        print("  Correct usage: python3 script.py [PLC_IP] [power_on|power_off|modify] [output] [on|off] \n")
    else:
        vHost = sys.argv[1]
        accion = sys.argv[2].lower()
        if accion == "power_on":
            fEncenderPLC(vHost)
        elif accion == "power_off":
            fApagarPLC(vHost)
        elif accion == "modify" and len(sys.argv) == 5:
            salida = sys.argv[3]
            estado = sys.argv[4].lower()
            fModificarSalida(vHost, salida, estado)
        else:
            print(cColorRojo + "\n  Invalid action or incorrect parameters. \n" + cFinColor)
