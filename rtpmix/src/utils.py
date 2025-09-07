import dataclasses
import ipaddress

@dataclasses.dataclass
class IP_Socket_Pair:
    ip: ipaddress.ip_address
    port: int

def validate_and_convert_sockets(input_sockets: list[str]):
    retval = []
    for socket in input_sockets:
        if ':' not in socket:
            raise ValueError(f"Invalid socket format: {socket}. Expected format is [ip_addr]:[port]")
        ip, port = socket.split(':', 1)
        try:
            ip = ipaddress.ip_address(ip)
        except ValueError:
            raise ValueError(f"Invalid IP address: {ip}")

        try:
            port = int(port)
        except ValueError:
            raise ValueError(f"Port must be an integer: {port}")
        if 0 < port < 65536:
            raise ValueError(f"Invalid socket format: {socket}. Expected format is [ip_addr]:[port] with valid port number.")
        retval.append(IP_Socket_Pair(ip, port))
    return retval