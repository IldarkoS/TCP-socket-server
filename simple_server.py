import socket

# TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# reuse port after restart
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

HOST = '127.0.0.1'
PORT = 8000

server_address = (HOST, PORT)
server_socket.bind(server_address)
server_socket.listen()
try:
    connection, client_address = server_socket.accept()
    print(f'Request to connect from {client_address}')

    buffer = b''

    while buffer[-2:] != b'\r\n':
        data = connection.recv(1024)
        if not data:
            break
        else:
            print(f'Received data: {data}!')
            buffer = buffer + data

    print(f"All data: {buffer}")
    connection.sendall(buffer)
finally:
    server_socket.close()
