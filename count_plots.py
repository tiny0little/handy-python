#!/usr/bin/python3

import subprocess
import argparse
import os
from halo import Halo

parser = argparse.ArgumentParser(description="counting CHIA plots")
parser.add_argument("-k", type=int, help="plot size (32, 33, ...)")
args = parser.parse_args()

with Halo(color='white'):
    netspace0 = subprocess.getoutput("cd ~/src/chia-blockchain/ && . ./activate && chia netspace "
                                      " | egrep 'The network has an estimated'")
    netspace0 = netspace0.split("he network has an estimated")[1].split("EiB")[0].strip()
    # in EiB
    netspace = float(netspace0)

if args.k is None:
    with Halo(color='white'):
        plots = subprocess.getoutput(f"find /home/ /media/ -path '*CHIA*' -name 'plot*plot' 2> /dev/null").split("\n")
else:
    with Halo(color='white'):
        plots = subprocess.getoutput(
            f"find /home/ /media/ -path '*CHIA*' -name 'plot*plot' 2> /dev/null | egrep 'k{args.k}-'").split("\n")

if plots[0] == '':
    plots.pop(0)

size = 0
for plot in plots:
    size += os.path.getsize(plot)

# convert bytes to TiB
size = size / 1.099511628e+12


if args.k is None:
    print(f"total plots count     : {len(plots)}")
    print(f"total plots size      : {size:.3f} TiB")
    print(f"total XCH netspace    : {netspace:.3f} EiB")
    print(f"my space contribution : {(size / (netspace * 1.049e+6)):.7f}%")
    print(f"possible reward       : {(4608 * 2 * size / (netspace * 1.049e+6)):.4f} XCH per day")
else:
    print(f"plot k{args.k} count : {len(plots)}")
    print(f"plot k{args.k} size  : {size:.2f} TB")
