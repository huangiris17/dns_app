from flask import Flask, request, make_response, jsonify
import socket
import json
import requests
# APP2

app = Flask(__name__)

# order between request DNS to get IP and receive GET request


@app.route("/home", methods=['GET'])
def home():
    return "Hi!"


@app.route("/fibonacci", methods=['GET'])
def fibonacci():
    hostname = request.args['hostname']  # Fibanocci server hostname
    number = request.args['number']  # Fibonacci number asked
    as_ip = request.args['as_ip']  # IP address of the Authoritative Server
    as_port = request.args['as_port']  # Authoritative Server port number
    if not all([hostname, number, as_ip, as_port]):
        return 'Bad Request', 400

    # DNS query to get FS IP from AS
    body = {'NAME': hostname, 'TYPE': 'A'}
    message = json.dumps(body).encode()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(message, (as_ip, as_port))
    data, addr = s.recv(2048)  # DNS response from AS, JSON
    data = data.decode()
    fs_ip = data.get("VALUE")
    s.close()

    response = requests.get(
        "http://{}/fibonacci".format(fs_ip), params={"number": number})
    return response

    # the only problem is that US does not know the IP address of the given
    # hostname and therefore needs to query its authoritative DNS server
    # to learn about it.


app.run(host='0.0.0.0', port=8080, debug=True)
