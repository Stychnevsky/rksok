import asyncio
from rksok_server import RksokServer
from consts import ENCODING
from loguru import logger

connected_clients = 0
connection_id = 0
async def tcp_server(reader, writer):
    global connected_clients
    global connection_id
    connected_clients += 1
    conn_id = 0
    logger.debug(f'Connection created. Connection id {conn_id}, total connected:: {connected_clients}')
    request = b''
    while True:
        try:
            data = await reader.read(1024)
        except ConnectionResetError:
            logger.debug('[ID {conn_id}] Client broke connection')
            writer.close()
            connected_clients -= 1
            break
        request += data
        if data.decode(ENCODING)[-4:] == '\r\n\r\n':
            logger.debug(f'[ID {conn_id}] Data recieved: {data.decode(ENCODING)}')
            response = await RksokServer(request.decode(ENCODING)).process_request()
            logger.debug(f'[ID {conn_id}] Response from server:\n {response}')
            writer.write(response.encode())
            await writer.drain()
            logger.debug(f'[ID {conn_id}] Response delivered')
            request = b""

        if not data:
            logger.debug('[ID {conn_id}] Connection break')
            writer.close()
            connected_clients -= 1
            break


async def main():
    server = await asyncio.start_server(
        tcp_server, '0.0.0.0', 3333)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    logger.info(f'Server started. Serving on {addrs}')
    
    async with server:
        await server.serve_forever()

asyncio.run(main())
