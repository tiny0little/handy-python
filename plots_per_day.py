#!/usr/bin/python3

import subprocess
import argparse
import os
from dateutil.parser import *
from dateutil.relativedelta import relativedelta


TEMP_FILE = "/tmp/plots_per_day.tmp"
dates = []



parser = argparse.ArgumentParser(description="counting how many CHIA plots made per day")
parser.add_argument("-f", "--files", action='store_true', help="show plot files")
args = parser.parse_args()


subprocess.getoutput(f"find /media/ -name plot*plot -exec ls -al {{}} \; 2> /dev/null > {TEMP_FILE}")
plots = subprocess.getoutput(f"cat {TEMP_FILE}").split("\n")

for plot in plots:
  tmp0 = " ".join(plot.split()).split(" ")
  mon = tmp0[5]
  day = int(tmp0[6])
  dates.append((mon,day))

# remove duplicates and sort
dates = list(set(dates))
dates.sort()


for (mon,day) in dates:
  print(f"{mon}:{day}")

  tmp0 = subprocess.getoutput(f"cat {TEMP_FILE} | egrep '{mon}\s+{day}' | wc")
  numberOfPlots = " ".join(tmp0.split()).split(" ")[0]
  print(f"- number of plots: {numberOfPlots}")

  tmp0 = subprocess.getoutput(f"cat {TEMP_FILE} | egrep '{mon}\s+{day}'").split("\n")
  size=0
  for tmp1 in tmp0:
    size += int(tmp1.split(" ")[4])
  size = size / (1024 * 1024 * 1024 * 1024)
  print(f"- size of plots: {size:.1f}TB")

  if args.files is True:
    tmp0 = subprocess.getoutput(f"cat {TEMP_FILE} | egrep '{mon}\s+{day}'").split("\n")
    for tmp1 in tmp0:
      tmp2 = " ".join(tmp1.split()).split(" ")
      fileName = tmp2[8]
      plotFileDataTime = parse(f"{tmp2[5]} {tmp2[6]} {tmp2[7]}")
      tmp3 = fileName.split("-")
      plotStartDatTime = parse(f"{tmp3[4]}-{tmp3[5]}-{tmp3[6]} {tmp3[7]}:{tmp3[8]}:00")
      plotProcTime = relativedelta(plotFileDataTime, plotStartDatTime)
      plotProcTimeInHours = plotProcTime.days * 24 + plotProcTime.hours
      print(f"- {fileName} - completed in {plotProcTimeInHours} hours ")


#subprocess.getoutput(f"rm {TEMP_FILE}")

