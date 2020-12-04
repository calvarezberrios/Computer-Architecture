#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) < 2:
    print("Missing program filename...")
    sys.exit(1)

file_to_execute = sys.argv[1]

cpu.load(file_to_execute)
cpu.run()