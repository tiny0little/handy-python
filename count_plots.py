#!/usr/bin/python3

import subprocess
import argparse
import os

parser = argparse.ArgumentParser(description="disk summary")
parser.add_argument("-k", type=int, help="plot size (32, 33, ...)")
args = parser.parse_args()


if args.k is None:
  plots = subprocess.getoutput(f"find /media/ -name '*plot' 2> /dev/null").split("\n")
else:
  plots = subprocess.getoutput(f"find /media/ -name '*plot' 2> /dev/null | egrep 'k{args.k}-'").split("\n")

if plots[0] == '':
  plots.pop(0)


size = 0
for plot in plots:
  size += os.path.getsize(plot)

size = size / (1024*1024*1024*1024)


if args.k is None:
  print(f"total plots count: {len(plots)}")
  print(f"total plots size: {size:.2f} TB")
else:
  print(f"plot k{args.k} count: {len(plots)}")
  print(f"plot k{args.k} size: {size:.2f} TB")


