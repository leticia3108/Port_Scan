import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# IP = input("Enter the IP address for the port scan: ")
LHOST = "192.168.56.1"

def parse_services(file_path = '/etc/services'):

    if sys.platform.startswith('linux')  or sys.platform == 'darwin':
        file_path = '/etc/services'
    elif sys.platform == 'win32':
        file_path = 'C:\\Windows\\System32\\drivers\\etc\\services'

    services = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if (line.startswith('#')) or not line.strip():
                    continue
                
                parts = line.split()
                if len(parts) < 2:
                    continue

                service = parts[0]
                port_prot = parts[1]

                if '/' in port_prot:
                    port, protocol = port_prot.split('/')
                    if protocol == 'tcp':
                        services[(int(port),protocol)] = service
    except FileNotFoundError:
        print (f"Arquivo não encontrado em {file_path}.")
        return{}
    
    return services

def scan_ports(port, services_map):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1)
        connected = client.connect_ex ((LHOST, port))

        if connected == 0:
            service = services_map.get((port,'tcp'), 'unknown')
            print ("{} open {}".format(port, service))

    except socket.timeout:
        print ("{} timed out".format(port))
    finally:
        client.close()

    return None

def main():
    services_map = parse_services()

    with ThreadPoolExecutor() as executor:
        for port in range(1, 65536):
            executor.submit(scan_ports, port, services_map)

    print("\nFinished scanning.")

if __name__ == "__main__":
    main()