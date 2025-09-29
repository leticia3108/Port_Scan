import socket

# IP = input("Enter the IP address for the port scan: ")
LHOST = "192.168.56.1"

def parse_services(file_path = '/etc/services'):
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

def main():
    services_map = parse_services()
    for PORTS in range (1, 65535):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(0.1)
            connected = client.connect_ex ((LHOST, PORTS))
        except socket.timeout:
            print ("{} timed out".format(PORTS))
        if connected == 0:
            service = services_map.get((PORTS,'tcp'), 'unknown')
            print ("{} open {}".format(PORTS, service))