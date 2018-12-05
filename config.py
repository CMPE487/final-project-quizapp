import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

SELF_IP = get_ip()
SUBNET = SELF_IP[:SELF_IP.rfind('.')]

DISCOVERY_PORT = 5000  # TCP

MESSAGE_TYPES = {"request": 0, "response": 1}
