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
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return 'Bad Request', 400

    response = make_response("answer from FS")
    return response


app.run(host='0.0.0.0',
        port=8080,
        debug=True)

UDP_IP = "127.0.0.1"
UDP_PORT = 53533
MESSAGE = b"Hello, World!"

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

TYPE = A
NAME = fibonacci.com
VALUE = IP_ADDRESS
TTL = 10
