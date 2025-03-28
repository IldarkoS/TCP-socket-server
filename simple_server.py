import socket
import selectors

from typing import List, Tuple

selector = selectors.DefaultSelector()

# TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# reuse port after restart
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.setblocking(False)

HOST = '127.0.0.1'
PORT = 8000

server_address = (HOST, PORT)
server_socket.bind(server_address)
server_socket.listen()

selector.register(server_socket, selectors.EVENT_READ)

while True:
    events: List[Tuple[selectors.SelectorKey, int]] = selector.select(timeout=1)
    
    if len(events) == 0:
        print('No events!')
    
    for event, _ in events:
        event_socket = event.fileobj

        if event_socket == server_socket:
            connection, client_address = server_socket.accept()
            connection.setblocking(False)
            print(f'Request to connect from {client_address}')
            selector.register(connection, selectors.EVENT_READ)
        else:
            data = event_socket.recv(1024)
            print(f"Received data: {data}")
            event_socket.send(data)
