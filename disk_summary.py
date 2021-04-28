#!/usr/bin/python3.8

import subprocess
from tabulate import tabulate
import argparse


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

TEMP_FILE1="/tmp/disk-health1.tmp"
TEMP_FILE2="/tmp/disk-health2.tmp"
table = []
disks = []



parser = argparse.ArgumentParser(description="disk summary")
parser.add_argument("--disk", help="disk device name, can be part of it")
args = parser.parse_args()



subprocess.getoutput("sudo ls")

subprocess.getoutput(f"df -m > {TEMP_FILE2}")
if args.disk is None:
  output = subprocess.getoutput(f"lsblk -r | grep disk").split("\n")
else:
  output = subprocess.getoutput(f"lsblk -r | grep disk | grep {args.disk}").split("\n")

disks=[]
for line in output:
  disks.append(line.split(" ")[0])
if disks[0] == '':
  disks.pop(0)
if not disks:
  print("no disks found")
  exit()



for disk in disks:
  subprocess.getoutput(f"sudo smartctl -a /dev/{disk} > {TEMP_FILE1}")

  table.append(["disk",f"/dev/{disk}"])



  lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Rotation").split("\n")
  type = "SSD"
  if "rpm" in lines[0]:
    type = "HDD"
  table.append(["type",f"{type}"])



  lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Model").split("\n")
  model = []
  for i in range(len(lines)):
    model.append(lines[i].split(":")[1].strip())
  table.append(["model",f"{' '.join(model)}"])



  lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Capac | egrep -v 'Unallocated|NVM'")
  lines=lines[lines.rfind("[")+1:-1].strip()
  table.append(["capacity",f"{colors.BOLD}{colors.OKGREEN}{lines}{colors.ENDC}"])



  lines = subprocess.getoutput(f"cat {TEMP_FILE2} | egrep {disk} | egrep -v efi")
  tmp = lines.split(" ")
  # if 1st element is empty string -> remove it
  if tmp[0] =='':
    tmp.pop(0)
  # if list is not empty
  if tmp:
    tmp = tmp[len(tmp)-2].strip()
    used = int(tmp[0:-1])
    tmp=f"{used}% ["
    scale=2.5
    for i in range(int(int(used)/scale)):
      tmp+="#"
    for i in range(int(100/scale-int(used)/scale)):
      tmp+="."
    tmp+="]"
    if used > 70:
      color = colors.FAIL
    elif used > 55:
      color = colors.WARNING
    else:
      color = colors.OKGREEN
    table.append(["used space",f"{color}{colors.BOLD}{tmp}{colors.ENDC}"])
  else:
    table.append(["used space",f"{colors.OKGREEN}{colors.BOLD}not mounted{colors.ENDC}"])




  lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Hour | egrep -v 'Fly|Load'")
  if "(" in lines:
    tmp = lines.split("(")
    lines = tmp[0]
  lines=lines[lines.strip().rfind(" "):].strip()
  table.append(["power on hours",f"{colors.BOLD}{colors.WARNING}{lines}{colors.ENDC}"])



  if type == "SSD":
    lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Writ | egrep -v 'Comma|NAND'")
    if "[" in lines:
      lines=lines[lines.rfind("[")+1:-1]
      table.append(["data written",f"{colors.BOLD}{colors.FAIL}{lines}{colors.ENDC}"])
    else:
      lines=int(lines[lines.rfind(" ")+1:])/931
      table.append(["data written",f"{colors.BOLD}{colors.FAIL}{lines:.2f} TB{colors.ENDC}"])


  # empty row
  table.append(["--------------","---------------------------------------------"])




print(tabulate(table,colalign=("right",),tablefmt="orgtbl"))
subprocess.getoutput(f"rm {TEMP_FILE1}")
subprocess.getoutput(f"rm {TEMP_FILE2}")


