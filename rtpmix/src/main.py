import argparse
import threading
from dataclasses import dataclass
from queue import Queue

import sock
from utils import validate_and_convert_sockets, IP_Socket_Pair

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RTP Audio Stream Muxer", epilog="This tool presently only supports uncompressed PCM audio streams.")
    parser.add_argument(
        "sockets",
        nargs="+",
        required=True,
        help="List of input RTP stream addresses in the format [ip_addr]:[port]"
    )
    args = parser.parse_args()
    socket_pairs = validate_and_convert_sockets(args.sockets)

    # Start threads for each link
    threads = []
    @dataclass
    class StreamRegistry:
        socket: IP_Socket_Pair
        thread: threading.Thread
        queue: Queue
    for socket_pair in socket_pairs:
        q = Queue(10)
        t = threading.Thread(target=sock.rtp_sock_task, args=(socket_pair, q))
        threads.append(t)

    # Start each thread
    for t in threads:
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()


    print("Input streams:", args.inputs)