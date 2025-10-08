import socket
import sys

# Terminal colors
colorRed = '\033[1;31m'
colorGreen = '\033[1;32m'
colorBlue = '\033[1;34m'
colorEnd = '\033[0m'

def show_initial_message():
    print(colorBlue + "\n===============================" + colorEnd)
    print(colorGreen + "      ⚙️  Navigator Notice ⚙️" + colorEnd)
    print(colorBlue + "===============================" + colorEnd)
    print("\nThese are the available options for the script:\n")
    print(colorGreen + "  - power_on   ➜ Turns on the PLC" + colorEnd)
    print(colorRed + "  - power_off  ➜ Turns off the PLC" + colorEnd)
    print(colorGreen + "  - modify     ➜ Modifies the PLC outputs" + colorEnd)
    print("\nUsage parameters:\n")
    print("  " + colorBlue + "python3 script.py [PLC IP] [option]" + colorEnd)
    print("\nExample:")
    print("  python3 script.py 192.168.1.100 power_on")
    print("  python3 script.py 192.168.1.100 power_off")
    print("  python3 script.py 192.168.1.100 modify Q0.0 on")
    print(colorBlue + "\n===============================" + colorEnd + "\n")

def connect_to_plc(host):
    print(f"Trying to connect to {host} on port 102...")
    plc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    plc_socket.settimeout(5)
    try:
        plc_socket.connect((host, 102))
        print("\n  Connection established.")
        return plc_socket
    except socket.error as e:
        print(f"\n  Error connecting to the PLC: {e}")
        return None

def modify_output(host, output, state):
    plc_socket = connect_to_plc(host)
    if not plc_socket:
        return

    command = {
        "on": '0300002502f08032010000001f000e00060501120a10010001000082000000000300010100',
        "off": '0300002502f08032010000001f000e00060501120a10010001000082000000000300010000'
    }

    if state not in command:
        print(colorRed + "\n  Invalid state. Use 'on' or 'off'. \n" + colorEnd)
        return

    print(f"\n  Modifying output {output} to state {state}...\n")
    send_payload(command[state], plc_socket)
    print(f"\n  Output {output} modified successfully.\n")
    plc_socket.close()

def send_payload(data, socket_conn):
    print(f"Trying to send: {data}")
    socket_conn.send(bytearray.fromhex(data))
    try:
        response = socket_conn.recv(1024)
        if response:
            print(f"\n  PLC response: {response.hex()} \n")
        else:
            print("\n  No response received from the PLC. \n")
        return response
    except socket.timeout:
        print("\n  Waited 5 seconds, but the PLC did not respond.")
        return None

def power_on_plc(host):
    plc_socket = connect_to_plc(host)
    if not plc_socket:
        return
    
    payload_on = '0300004302f0807202003431000004f200000010000003ca3400000034019077000803000004e88969'
    send_payload(payload_on, plc_socket)
    print("\n  PLC started successfully.\n")
    plc_socket.close()

def power_off_plc(host):
    plc_socket = connect_to_plc(host)
    if not plc_socket:
        return
    
    payload_off = '0300004302f0807202003431000004f200000010000003ca3400000034019077000801000004e88969'
    send_payload(payload_off, plc_socket)
    print("\n  PLC stopped successfully.\n")
    plc_socket.close()

if __name__ == "__main__":
    show_initial_message()
    if len(sys.argv) < 3:
        print(colorRed + "\n  Incorrect usage. You must specify the PLC IP and the action to perform. \n" + colorEnd)
        print("  Correct usage: python3 script.py [PLC_IP] [power_on|power_off|modify] [output] [on|off] \n")
    else:
        host = sys.argv[1]
        action = sys.argv[2].lower()
        if action == "power_on":
            power_on_plc(host)
        elif action == "power_off":
            power_off_plc(host)
        elif action == "modify" and len(sys.argv) == 5:
            output = sys.argv[3]
            state = sys.argv[4].lower()
            modify_output(host, output, state)
        else:
            print(colorRed + "\n  Invalid action or incorrect parameters. \n" + colorEnd)
