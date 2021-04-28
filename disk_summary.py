#!/usr/bin/python3.8

import subprocess
from tabulate import tabulate



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

subprocess.getoutput("sudo ls")

subprocess.getoutput(f"df -m > {TEMP_FILE2}")
output = subprocess.getoutput("lsblk -r | grep disk | awk '{print $1}'")
disks = output.split("\n")
table = []
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
  tmp = tmp[len(tmp)-2].strip()
  used = int(tmp[0:-1])
  tmp=f"{used}% ["
  scale=2.5
  for i in range(int(int(used)/scale)):
    tmp+="#"
  for i in range(int(100/scale-int(used)/scale)):
    tmp+="."
  tmp+="]"
  if used > 60:
    color = colors.WARNING
  else:
    color = colors.OKGREEN
  table.append(["used",f"{color}{tmp}{colors.ENDC}"])


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


