import socket
from flask import Flask, make_response, request, jsonify, Response

app = Flask(__name__)


@app.route("/fibonacci", methods=['GET'])
def fibonacci():
    hostname = request.args['hostname']
    fs_port = request.args['fs_port']
    number = request.args['number']
    as_ip = request.args['as_ip']
    as_port = request.args['as_port']
    body = jsonify(hostname=hostname,
                   ip='172.18.0.2',
                   as_ip='10.9.10.2',
                   as_port='30001'
                   )

    response = make_response("answer from FS")
    return response


app.run(host='0.0.0.0',
        port=53533,
        debug=True)


UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    print("received message: %s" % data)


# Data structure to store DNS records
dns_records = {}


def handle_registration(data):
    # Parse and store the DNS record
    parts = data.split()
    if len(parts) == 5 and parts[0] == "TYPE=A" and parts[2] == "VALUE=IP_ADDRESS" and parts[4] == "TTL=10":
        name = parts[1]
        value = parts[3]
        dns_records[name] = {'value': value, 'type': 'A', 'ttl': 10}


def handle_dns_query(query):
    parts = query.split()
    if len(parts) == 2 and parts[0] == "TYPE=A":
        name = parts[1]
        record = dns_records.get(name)
        if record:
            return f"TYPE=A NAME={name} VALUE={record['value']} TTL={record['ttl']}"


def main():
    host = '0.0.0.0'
    port = 53533

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        print(f"Authoritative Server listening on {host}:{port}")

        while True:
            data, addr = s.recvfrom(1024)
            data = data.decode('utf-8')
            response = None

            if data.startswith("TYPE=A"):
                handle_registration(data)
                response = "HTTP 201 Created"  # Respond to registration

            else:
                response = handle_dns_query(data)  # Respond to DNS query

            if response:
                s.sendto(response.encode('utf-8'), addr)


if __name__ == "__main__":
    main()
