#!/usr/bin/python3

import subprocess
import argparse
import os
from halo import Halo
from tabulate import tabulate

finalTable = []

parser = argparse.ArgumentParser(description="counting CHIA plots")
parser.add_argument("-k", type=int, help="plot size (32, 33, ...)")
args = parser.parse_args()

with Halo(color='white'):
    netspace0 = subprocess.getoutput("cd ~/src/chia-blockchain/ && . ./activate && chia netspace "
                                     " | egrep 'The network has an estimated'")
    netspace0 = netspace0.split("The network has an estimated")[1].split("EiB")[0].strip()
    netspace = float(netspace0)  # in EiB

    #
    time_to_win = subprocess.getoutput("cd ~/src/chia-blockchain/ && . ./activate && chia farm summary "
                                       " | egrep 'Expected time to win'")
    time_to_win = time_to_win.split("Expected time to win:")[1].strip()

    #
    if args.k is None:
        plots = subprocess.getoutput(
            f"find /home/ /media/ -path '*CHIA*' -name 'plot*plot' 2> /dev/null").split("\n")
    else:
        plots = subprocess.getoutput(
            f"find /home/ /media/ -path '*CHIA*' -name 'plot*plot' 2> /dev/null | egrep 'k{args.k}-'").split("\n")

    if plots[0] == '':
        plots.pop(0)

    size = 0
    for plot in plots:
        size += os.path.getsize(plot)

#
# convert bytes to TiB
size = size / 1.099511628e+12

if args.k is None:
    finalTable.append(["total plots count", len(plots)])
    finalTable.append(["total plots  size", f"{size:.3f} TiB"])
    finalTable.append(["total XCH netspace", f"{netspace:.3f} EiB"])
    finalTable.append(["my space contribution", f"{(size / (netspace * 1.049e+6)):.8f}%"])
    finalTable.append(["possible reward", f"{(4608 * 2 * size / (netspace * 1.049e+6)):.5f} XCH per day"])
    finalTable.append(["expected time to win", time_to_win])
else:
    # print(f"plot k{args.k} count : {len(plots)}")
    finalTable.append([f"plot-k{args.k} count", f"{len(plots)}"])
    # print(f"plot k{args.k} size  : {size:.2f} TB")
    finalTable.append([f"plot-k{args.k}  size", f"{size:.2f} TB"])

row0 = ['right', 'left']
print(tabulate(finalTable, colalign=row0, tablefmt="pretty"))
