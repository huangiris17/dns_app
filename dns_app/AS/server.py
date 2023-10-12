import socket
# APP3

dns_records = {}


def main():
    UDP_IP = "0.0.0.0"
    UDP_PORT = 53533

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        data = data.decode()
        response = None

        if data.get("VALUE") is not None:
            response = "success"
            # response = use_registration(data)

        else:
            response = use_dns_query(data)

        sock.sendto(response.encode(), addr)


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


if __name__ == "__main__":
    main()
