from flask import Flask, make_response, request
import json
import socket

app = Flask(__name__)
UDP_IP = "0.0.0.0"
UDP_PORT = 53533


def register_AS(hostname, ip, as_ip, as_port):
    body = {'NAME': hostname, 'VALUE': ip, 'TYPE': 'A', 'TTL': 10}
    message = json.dumps(body).encode('utf-8')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (UDP_IP, UDP_PORT))

    return 'Created', 201


@app.route("/register", methods=['PUT'])
def registerFib():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if not all([hostname, ip, as_ip, as_port]):
        return 'Bad Request', 400

    return register_AS(hostname, ip, as_ip, as_port)


def fibonacci(x):
    if x == 1 or x == 0:
        return x
    return fibonacci(x - 1) + fibonacci(x - 2)


@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')

    try:
        x = int(number)
    except ValueError:
        return 'Bad Format', 400

    return fibonacci(x), 200


app.run(host='0.0.0.0',
        port=9090,
        debug=True)
