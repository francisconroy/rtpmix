import dataclasses
import logging
import socketserver

import socket
import sys
from queue import Queue, Full

from rtp import RTP, PayloadType

from utils import IP_Socket_Pair

LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class StreamData:
    ssrc: int
    payload_type: PayloadType


class UDPHandler(socketserver.DatagramRequestHandler):
    def __init__(self, request, client_address, server, ):
        super().__init__(request, client_address, server)
        self.data_queue: Queue | None = None
        self.stream_data: set[StreamData] = set()

    def register_queue(self, data_queue: Queue):
        self.data_queue = data_queue

    def register_stream(self, stream: StreamData):
        if stream not in self.stream_data:
            LOGGER.info("Registering new stream with SSRC: %s and Payload Type: %s", stream.ssrc, stream.payload_type)
            self.stream_data.add(stream)

    def handle(self):
        print("Got an UDP Message from {}".format(self.client_address[0]))
        data = self.request[0]
        socket = self.request[1]
        print(f"{self.client_address[0]} wrote:")
        decoded_payload = RTP().fromBytearray(data)
        if decoded_payload.payloadType not in [PayloadType.L16_2chan, PayloadType.L16_1chan]:
            LOGGER.error("Unsupported payload type: %s", decoded_payload.payloadType)
            sys.exit(1)
        self.register_stream(StreamData(decoded_payload.ssrc, decoded_payload.payloadType))

    def buffer_audio(self, decoded_payload: RTP):
        try:
            self.data_queue.put(decoded_payload.payload, timeout=1)
        except Full:
            LOGGER.warning("Data queue is full. Dropping packet with SSRC: %s, seq_no: %s", decoded_payload.ssrc,
                           decoded_payload.sequenceNumber)


def rtp_sock_task(socket_pair: IP_Socket_Pair, data_queue):
    # this is the main entrypoint
    if __name__ == '__main__':
        # we specify the address and port we want to listen on
        listen_addr = (socket_pair.ip, socket_pair.port)

        # with allowing to reuse the address we dont get into problems running it consecutively sometimes
        socketserver.UDPServer.allow_reuse_address = True

        # register our class
        serverUDP = socketserver.UDPServer(listen_addr, UDPHandler)
        serverUDP.
        socklvl = socket.IPPROTO_IPV6 if socket_pair.ip.version == 6 else socket.IPPROTO_IPV4
        # serverUDP.socket.setsockopt(socklvl, socket.IP_HDRINCL, 1)
        serverUDP.serve_forever()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((socket_pair.ip, socket_pair.port))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data: break
                conn.sendall(data)
