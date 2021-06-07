#!/usr/bin/python3

import subprocess
import argparse
import os
from halo import Halo
from tabulate import tabulate

#
#
#
colorGREEN = '\033[92m'
colorYELLOW = '\033[93m'
colorRED = '\033[91m'
colorENDC = '\033[0m'
colorBOLD = '\033[1m'
colorWHITEonPURPLE = '\33[45m'
colorWHITEonGREEN = '\33[42m'
colorWHITEonBLUE = '\33[44m'
colorWHITEonRED = '\33[41m'
#
#
#


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
    if args.k is None:
        plots = subprocess.getoutput(
            f"find /media/ -path '*CHIA*' -name 'plot*plot' 2> /dev/null").split("\n")
    else:
        plots = subprocess.getoutput(
            f"find /media/ -path '*CHIA*' -name 'plot*plot' 2> /dev/null | egrep 'k{args.k}-'").split("\n")

    if plots[0] == '':
        plots.pop(0)

    size = 0
    for plot in plots:
        size += os.path.getsize(plot)

    #
    # convert bytes to TiB

    size = size / 1.099511628e+12
    possible_reward = (4608 * 2 * size / (netspace * 1.049e+6))
    days_to_win = f"{int(2 / possible_reward)}"

    if args.k is None:
        finalTable.append(["total plots count", f"{colorWHITEonGREEN}{colorBOLD}{len(plots)}{colorENDC}"])
        finalTable.append(["total plots  size", f"{colorWHITEonPURPLE}{colorBOLD}{size:.2f}{colorENDC} TiB"])
        finalTable.append(["total XCH netspace", f"{netspace:.2f} EiB"])
        finalTable.append(["my netspace %", f"{(size / (netspace * 1.049e+6)):.10f}%"])
        finalTable.append(["possible reward", f"{possible_reward:.5f}xch per day"])
        finalTable.append(["days to win 2xch", days_to_win])
    else:
        finalTable.append([f"plot-k{args.k} count", f"{len(plots)}"])
        finalTable.append([f"plot-k{args.k}  size", f"{size:.2f} TB"])

#
#

row0 = ['right', 'left']
print(tabulate(finalTable, colalign=row0, tablefmt="pretty"))
