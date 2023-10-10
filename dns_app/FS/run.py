from flask import Flask, make_response, request

app = Flask(__name__)
body_info = {}


@app.route("/register", methods=['PUT'])
def registerFib():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')
    if not all([hostname, ip, as_ip, as_port]):
        return 'Bad Request', 400
    body_info = {'ip': ip, 'as_ip': as_ip, 'as_port': as_port}

    return 'Created', 201


@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')
    fib_ans = 0

    try:
        number = int(number)
    except ValueError:
        return 'Bad Format', 400

    return fib_ans


app.run(host='0.0.0.0',
        port=9090,
        debug=True)
