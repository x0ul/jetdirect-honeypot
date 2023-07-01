#!/bin/env python

# pass to `ippeveprinter` with `-c`. Handles renaming files.
# requires a modification to `ippeveprinter` that exports the `CLIENT_HOSTNAME` environment variable

import datetime
import logging
import os
import shutil
import sys

logging.basicConfig(level=logging.INFO)
in_file = sys.argv[1]
out_dir = "/home/faxspam/ipp"
client = os.environ.get("CLIENT_HOSTNAME", "0.0.0.0")
out_file = f"{out_dir}/{datetime.datetime.now().isoformat()}_{client}.ps"
logging.info(f"copying {in_file} to {out_file}")
shutil.copyfile(in_file, out_file)
