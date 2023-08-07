#!/usr/bin/env python

import argparse
import datetime
import logging
import os
import select
import socket

parser = argparse.ArgumentParser()
parser.add_argument(
    "-o", "--out-dir", help="specify output directory", default=os.getcwd()
)
parser.add_argument("-p", "--port", help="listen port", type=int, default=9100)
args = parser.parse_args()


logging.basicConfig(level=logging.INFO)
logging.info("starting server")

s = socket.create_server(("", args.port))
s.setblocking(False)
s.listen()

while True:
    r, _, _ = select.select([s], [], [])
    if not r:
        continue

    (clientsocket, address) = s.accept()
    logging.info(f"new connection from {address[0]}")
    outfile = f"{args.out_dir}/{datetime.datetime.now().isoformat()}_{address[0]}"
    total_bytes = 0
    with open(outfile, "wb") as f:
        while True:
            try:
                r, _, _ = select.select([clientsocket], [], [], 15)
                if not r:
                    logging.info("timed out waiting for recv")
                    break
                buf = clientsocket.recv(1024)
                if b"@PJL INFO STATUS" in buf:
                    clientsocket.send(
                        b'CODE=10001\r\nDISPLAY="00 READY"\r\nONLINE=TRUE\r\n\f'
                    )
                elif b"@PJL INFO ID" in buf:
                    clientsocket.send(b"HP COLOR LASERJET 9500\r\n\f")
                total_bytes += len(buf)
                logging.debug(f"received {len(buf)} bytes")
            except ConnectionResetError:
                logging.info("connection reset")
                break
            except TimeoutError:
                break

            f.write(buf)

        logging.info(f"wrote out {outfile} ({total_bytes} bytes)")
        clientsocket.close()
