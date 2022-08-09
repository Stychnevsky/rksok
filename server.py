import asyncio
from rksok_request import RksokRequestHandler
from config import ENCODING, SERVER_PORT, SERVER_IP, REQUEST_END
from loguru import logger

connected_clients = 0
connection_id = 1
async def tcp_server(reader: asyncio.StreamReader, writer: asyncio.StreamWriter ) -> None:
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
        if data.decode(ENCODING)[-4:] == REQUEST_END:
            decoded_request = request.decode(ENCODING)
            logger.debug(f'[ID {conn_id}] Data recieved: {decoded_request}')
            raw_response = await RksokRequestHandler(decoded_request).process_request()
            logger.debug(f'[ID {conn_id}] Response from server:\n {raw_response}')
            writer.write(raw_response.encode())
            await writer.drain()
            logger.debug(f'[ID {conn_id}] Response delivered')
            request = b""

        if not data:
            logger.debug('[ID {conn_id}] Connection break')
            writer.close()
            connected_clients -= 1
            break


async def main() -> None:
    server = await asyncio.start_server(
        tcp_server, SERVER_IP, SERVER_PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    logger.info(f'Server started. Port {SERVER_PORT}. Serving on {addrs}')
    
    async with server:
        await server.serve_forever()

asyncio.run(main())
