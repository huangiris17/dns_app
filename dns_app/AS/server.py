import socket

dns_records = {}


def listen():
    UDP_IP = "0.0.0.0"
    UDP_PORT = 53533

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.listen()
    conn, addr = sock.accept()

    with conn:
        data = conn.recv(1024)

        while True:
            data, addr = socket.recvfrom(1024)
            data = data.decode('utf-8')
            response = None

            if data.get("VALUE"):
                response = use_registration(data)

            else:
                response = use_dns_query(data)

            conn.sendall(response)


def use_registration(data):
    name = data["NAME"]
    dns_records[name] = data
    return 'Created', 201


def use_dns_query(data):
    name = data["NAME"]
    record = dns_records.get(name)
    if record:
        return record
    return "400"
