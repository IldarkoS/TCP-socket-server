import asyncio
import socket
import logging

from asyncio import AbstractEventLoop


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    try:
        while data := await loop.sock_recv(connection, 1024):
            print('Data received!')
        if data == b'\r\n':
            raise Exception("Empty")
        await loop.sock_sendall(connection, data)
    except Exception as ex:
        logging.exception(ex)
    finally:
        connection.close()


async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Request to connect from {address}")
        asyncio.create_task(echo(connection, loop))


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    await listen_for_connection(server_socket, asyncio.get_event_loop())


if __name__ == '__main__':
    asyncio.run(main())