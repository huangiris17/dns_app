from flask import Flask, make_response, request
import json
import socket

app = Flask(__name__)
UDP_IP = "0.0.0.0"
UDP_PORT = 53533

# body = jsonify(hostname=hostname,
#                ip='172.18.0.2',
#                as_ip='0.0.0.0',
#                as_port='53533'
#                )


@app.route("/home", methods=['GET'])
def home():
    return "Hi!"


def register_AS(hostname, ip, as_ip, as_port):
    body = {'TYPE': 'A', 'NAME': hostname, 'VALUE': ip, 'TTL': 10}
    message = json.dumps(body).encode('utf-8')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(message, (as_ip, as_port))
    response, addr = s.recv(2048)  # DNS response from AS, JSON
    s.close()

    return response


@app.route("/register", methods=['PUT'])
def registerFib():
    # return "PUT SUCCESS"
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
