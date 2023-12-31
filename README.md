# dns_app
Lab Course repo for DNS at NYU 2023
a. User server (US) is a simple HTTP web server (e.g. Flask), running in
port 8080, that accepts a GET HTTP requests in path: “/fibonacci?hostname=fibonacci.com&fs_port=K&number=X&as_ip=
Y&as_port= Z”
The path accepts five parameters: hostname and fs_port which contains the hostname and port number of the server which will be queried to get a response for Fibonacci number for a given sequence number X. And as_ip, as_port which are the IP address and port number of the Authoritative Server (AS). If any of the parameters are missing, the server should return HTTP code 400 indicating a bad request. If the request is successful, it should return HTTP code 200 with the Fibonacci number for the sequence number X. the only problem is that US does not know the IP address of the given hostname and therefore needs to query its authoritative DNS server to learn about it.
b. Fibonacci Server (FS) is an HTTP web server, running in port 9090, that provides the Fibonacci value for a given sequence number X. In order to achieve this objective, FS performs the following:
1. Hostname Specification: FS accepts a HTTP PUT request at path “/register” where the body contains the name and IP address of the server (FS) and IP address of the Authoritative Server (AS). You can
choose any name of your choice, let’s say “fibonacci.com”. The body should contain a json object as below. FS should parse the body and noted that hostname and IP and IP, port of the AS and moved to step 2 for registration to authoritative server.
{
“hostname”:
“fibonacci.com”, “ip”: “172.18.0.2”, “as_ip”: “10.9.10.2”, “as_port”: “30001”
}
2. Registration to Authoritative Server Once the request is retrieved at path “/register”, the hostname needs be registered with Authoritative server (AS) via UDP on port 53533. Your DNS message should include (Name, Value, Type, TTL) where the type in this case is “A” and TTL in seconds. Below is a simplified DNS registration request (please follow the format as below -- without the dashes--, each line ends with a new line):
----
TYPE=A NAME=fi bonacci.co m
V ALUE=I P_ADDR ESS TTL=10 ----
3. Once registration is successful, returns back a HTTP response with code 201.
4. Serve a path in “/fibonacci?number=X” which accepts HTTP GET request and returns Fibonacci number for the sequence number X. Return 200 as a status code if successful. If X is not an integer (for example a string) return 400 indicating the bad format.
c. Authoritative Server (AS) is the authoritative server for US. It has two duties. First is to handle the registration requests to pair hostnames to IP, second is to be able to respond to DNS queries from clients.
i. Registration: Accept a UDP connection on port 53533 and register Type A DNS record into the database. Hint: You need to store the value in somewhere persistent, for example in a file

so that you can later respond to DNS queries.
ii. DNS Query: Respond to DNS Query on port 53533. Query
should include: (Name, Type). If the message conforms to this, server will return the IP address in a DNS message of form: (Name, Value, Type, TTL), retrieved from the file (note that AS can distinguish registration requests from DNS queries by simply looking at the fields provided). Here is a sample request and response:
Request: TYPE=A
NAME=fibonacci.com
Response: TYPE=A
NAME=fib onacci.com V ALUE=IP _ADDRES S TTL=10
Problem 2 will be graded based on the following. Please follow the instructions carefully for including the port numbers and message formats. Any deviation from the specification above will result losing points in the assignment:
a. US responds to requests in path /fibonacci as specified above.
b. FS accepts a registration request in /register as specified above.
c. FS responds to GET requests in /fibonacci.
d. AS performs a registration requests as specified above.
e. AS provides DNS record for a given query as specified above.
