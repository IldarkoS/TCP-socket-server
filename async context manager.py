import asyncio
import socket

from types import TracebackType
from typing import Optional, Type


class ConnectedSocket:
    def __init__(self, server_socket):
        self._connection = None
        self._server_socket = server_socket

    async def __aenter__(self):
        print('Context manager enter')
        loop = asyncio.get_event_loop()
        connection, _ = await loop.sock_accept(self._server_socket)
        self._connection = connection
        print('Connected!')
        return self._connection
    
    async def __aexit__(self,
                        exc_type: Optional[Type[BaseException]],
                        exc_val: Optional[BaseException],
                        exc_tb: Optional[TracebackType]):
        print('Exit from context manager')
        self._connection.close()
        print("Connection closed")


async def main():
    loop = asyncio.get_event_loop()

    HOST = '127.0.0.1'
    PORT = 8000
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setblocking(False)

    server_address = (HOST, PORT)
    server_socket.bind(server_address)
    server_socket.listen()

    async with ConnectedSocket(server_socket) as connection:
        data = await loop.sock_recv(connection, 1024)
        print(data)

asyncio.run(main())