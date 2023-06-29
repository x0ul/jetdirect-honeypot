#!/usr/bin/env python

import datetime
import logging
import socket

logging.basicConfig(level=logging.INFO)
logging.info("starting server")

s = socket.create_server(("", 9100))
s.listen()

while True:
    (clientsocket, address) = s.accept()
    logging.info(f"new connection from {address[0]}")
    outfile = f"/tmp/{datetime.datetime.now().isoformat()}_{address[0]}.ps"
    total_bytes = 0
    with open(outfile, "wb") as f:
        buf = "foobar"
        while buf:
            buf = clientsocket.recv(1024)
            total_bytes += len(buf)
            logging.debug(f"received {len(buf)} bytes")
            f.write(buf)

        logging.info(f"wrote out {outfile} ({total_bytes} bytes)")
        clientsocket.close()
