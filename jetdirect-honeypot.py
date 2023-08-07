#!/usr/bin/env python

import argparse
import datetime
import logging
import os
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
s.settimeout(15)
s.listen()

while True:
    (clientsocket, address) = s.accept()
    logging.info(f"new connection from {address[0]}")
    outfile = f"{args.out_dir}/{datetime.datetime.now().isoformat()}_{address[0]}"
    total_bytes = 0
    with open(outfile, "wb") as f:
        buf = "foobar"
        while buf:
            try:
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
                print("connection reset")
                break
            f.write(buf)

        logging.info(f"wrote out {outfile} ({total_bytes} bytes)")
        clientsocket.close()
