import socket

dns_records = {}


def listen():
    UDP_IP = "0.0.0.0"
    UDP_PORT = 53533

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)

        while True:
            data, addr = socket.recvfrom(1024)
            data = data.decode('utf-8')
            response = None

            if data.startswith("TYPE=A"):
                use_registration(data)
                response = "201 Created"

            else:
                response = use_dns_query(data)

            return response


def use_registration(data):
    name = data["NAME"]
    dns_records[name] = data


def use_dns_query(data):
    name = data["NAME"]
    name = data["TYPE"]
    record = dns_records.get(name)
    if record:
        return f"TYPE=A NAME={name} VALUE={record['value']} TTL={record['ttl']}"
    return "400"
