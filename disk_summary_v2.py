#!/usr/bin/python3.8

#
# v2 with threading
#
#

import subprocess
from tabulate import tabulate
import argparse
from halo import Halo
import threading



colorGREEN = '\033[92m'
colorYELLOW = '\033[93m'
colorRED = '\033[91m'
colorENDC = '\033[0m'
colorBOLD = '\033[1m'
colorWHITEonPURPLE = '\33[45m'
colorWHITEonGREEN = '\33[42m'
colorWHITEonBLUE = '\33[44m'
colorWHITEonRED = '\33[41m'

tempFilePrefix = "/tmp/diskSummary_"
tempFiles = {}
tempFileDF = "/tmp/diskSummary_DF.tmp"
th = {}
scale = 2.5 # for disk space gauge

finalTable = []
disks = []
disk_device = []
disk_type = []
disk_model = []
disk_capacity = []
disk_mounts = []
disk_space = []
disk_hours = []
disk_writes = []
disk_temp = []
disk_errors = []


totalCapacity = 0
totalUsedSpace = 0
totalFreeSpace = 0



if __name__ != "__main__": exit()

#
#
#
#
#

parser = argparse.ArgumentParser(description="disk summary")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-d", "--disk", help="disk device name, can be part of it")
parser.add_argument("-c", "--col", help="number of columns in the output", default=3, type=int, choices=[1, 2, 3],)
parser.add_argument("device_type", choices=['all', 'ssd', 'hdd'], nargs='?', default='all', const='all',
                    help="which type of devices you would like to see? (default: %(default)s)")
args = parser.parse_args()

# get sudo before we start, we'll need it for smartctl
subprocess.getoutput("sudo ls")

subprocess.getoutput(f"df -m > {tempFileDF}")
if args.disk is None:
    output = subprocess.getoutput(f"lsblk -r | grep disk").split("\n")
else:
    # remove path to the device, leave only device name
    tmp = args.disk[args.disk.rfind("/") + 1:].strip()
    output = subprocess.getoutput(f"lsblk -r | grep disk | cut -d' ' -f1 | grep {tmp}").split("\n")

for line in output : disks.append(line.split(" ")[0])
if disks[0] == '' : disks.pop(0)
if not disks:
    print("no disks found")
    exit()

if args.verbose: print(f"found following disks: {disks}")

#
# Gather all disks SMART info and store it into tmp files
#
def gatherSmart(_disk,_tempFile):
  subprocess.getoutput(f"sudo smartctl -a /dev/{_disk} > {_tempFile}")
  # let's see if we have anything, if nothing, let's try 1st partition -> works for USB flash drives
  lines = subprocess.getoutput(f"cat {_tempFile} | egrep Model").split("\n")
  if lines[0] == '' : subprocess.getoutput(f"sudo smartctl -a /dev/{_disk}1 > {_tempFile}")


#
# Launching all smartctl in parralel as threads
#
for disk in disks:
  tempFiles[disk] = tempFilePrefix + disk + ".tmp"
  th[disk] = threading.Thread(target=gatherSmart, args=(disk,tempFiles[disk],), daemon=True)
  th[disk].start()

#
# Waiting for all threads to complete
#
with Halo(color='white'):
  for disk in disks:
    th[disk].join()


#
# go disk by disk and build the final table
#
for disk in disks:

    lines = subprocess.getoutput(f"cat {tempFiles[disk]} | egrep Rotation").split("\n")
    type0 = f"{colorWHITEonGREEN}SSD{colorENDC}"
    if "rpm" in lines[0] : type0 = f"{colorWHITEonPURPLE}HDD{colorENDC}"



    if (args.device_type not in type0.lower()) and (args.device_type != 'all'):
      disks.pop()
      continue




    disk_type.append(type0)
    disk_device.append(f"/dev/{disk}")


    #
    #
    #
    #

    tmp0 = subprocess.getoutput(f"cat {tempFileDF} | egrep {disk}").split("\n")
    mount = ''
    for tmp1 in tmp0 : mount = mount + tmp1[tmp1.rfind("%")+1:].strip()+ '\n'
    mount = mount[:-1]
    disk_mounts.append(f"{mount}")

    #
    #
    #
    #
    #
    lines = subprocess.getoutput(f"cat {tempFiles[disk]} | egrep 'Model|Vendor:|Product:'").split("\n")
    if lines[0] == '' : lines.pop(0)
    model = []
    for i in range(len(lines)) : model.append(lines[i].split(":")[1].strip())
    disk_model.append(f"{' - '.join(model)}")

    #
    #
    #
    #
    #
    lines = subprocess.getoutput(f"cat {tempFiles[disk]} | egrep Capacity | egrep -v 'Unallocated|NVM'")
    capacity = lines[lines.rfind("[") + 1:-1].strip()
    disk_capacity.append(f"{colorBOLD}{colorGREEN}{capacity}{colorENDC}")
    capacityInBytes = lines[lines.rfind(":")+1:lines.rfind("byte")-1].replace(',','').strip()
    if not capacityInBytes.isnumeric() : capacityInBytes = lines[lines.rfind(":")+1:lines.rfind("[")-1].replace(',','').strip()
    if capacityInBytes.isnumeric() : totalCapacity += int(capacityInBytes)

    #
    #
    #
    #
    #
    lines = subprocess.getoutput(f"cat {tempFiles[disk]} | egrep Tempera | egrep -v 'Trip|Warning|Critical|Airflow'")
    if len(lines) > 0:
      if lines[0] == '':
        lines.pop(0)
    if len(lines) > 0:
      if lines.rfind("(",-20) > 0:
        lines = lines[:lines.rfind("(",-20)].strip()
      if lines.rfind("Celsius",-20) > 0:
        lines = lines[:lines.rfind("Celsius",-20)].strip()
      if lines.rfind("C",-10) > 0:
        lines = lines[:lines.rfind("C",-10)].strip()
      tmp=lines.split(" ")[-1].strip()
      if int(tmp) > 60:
        color0=colorRED
      elif int(tmp) > 50:
        color0 = colorYELLOW
      else:
        color0 = colorGREEN
      tmp=f"{color0}{colorBOLD}{tmp}C{colorENDC}"
    else:
      tmp=''
    disk_temp.append(tmp)
    


    #
    #
    #
    #
    #

    lines = subprocess.getoutput(f"cat {tempFileDF} | egrep {disk} | egrep -v efi")
    used = 0
    if lines.rfind("%") > 0:
      used = int(lines[lines.rfind("%")-3:lines.rfind("%")].strip())
    if used > 0:
      if capacityInBytes.isnumeric():
        totalUsedSpace += used * int(capacityInBytes) / 100
      tmp = f"{used}% ["
      for i in range(int(int(used) / scale)):
        tmp += "#"
      for i in range(int(100 / scale - int(used) / scale)):
        tmp += "."
      tmp += "]"
      if used > 70:
        color0 = colorRED
      elif used > 55:
        color0 = colorYELLOW
      else:
        color0 = colorGREEN
      disk_space.append(f"{color0}{colorBOLD}{tmp}{colorENDC}")
    else:
      disk_space.append(f"{colorGREEN}{colorBOLD}not mounted{colorENDC}")

    #
    #
    #
    #
    #
    lines = subprocess.getoutput(f"cat {tempFiles[disk]} | egrep Hour | egrep -v 'Fly|Load'")
    if "(" in lines:
        tmp = lines.split("(")
        lines = tmp[0]
    lines = lines[lines.strip().rfind(" "):].strip()
    disk_hours.append(f"{colorBOLD}{colorYELLOW}{lines}{colorENDC}")

    #
    #
    #
    #
    #
    if "SSD" in type0:
        lines = subprocess.getoutput(f"cat {tempFiles[disk]} | egrep Writ | egrep -v 'Comma|NAND'")
        if len(lines) > 0:
          if "[" in lines:
              lines = lines[lines.rfind("[") + 1:-1]
              disk_writes.append(f"{colorBOLD}{colorRED}{lines}{colorENDC}")
          else:
              lines = int(lines[lines.rfind(" ") + 1:]) / 931
              disk_writes.append(f"{colorBOLD}{colorRED}{lines:.2f} TB{colorENDC}")
        else:
          disk_writes.append("")
    else:
        disk_writes.append("")


    #
    #
    #
    #
    #

    errors = ""
    tmp0 = subprocess.getoutput(f"cat {tempFiles[disk]} | egrep 'Reallocated_Sector|Current_Pending_Sector|Calibration_Retry_Count|Command_Timeout|Spin_Retry_Count|Calibration_Retry_Count|Offline_Uncorrectable|Error' | egrep -v 'Error_Rate'").split("\n")
    for tmp1 in tmp0:
      tmp2 = " ".join(tmp1.split()).split(" ")
      if len(tmp2) > 1:
        propertyName = tmp2[1].strip()
        tmp1 = " ".join(tmp1.split())
        value = tmp1[tmp1.rfind("-")+1:].strip()
        if not value.isnumeric():
          value = value.split(" ")[0].strip()
        if value.isnumeric():
          if int(value) > 0:
            errors = errors + f"{propertyName} = {colorRED}{colorBOLD}{value}{colorENDC}\n"

    disk_errors.append(errors)


#
#
#

def rowSeparator():
  row0 = []
  for x in range(args.col):
    row0.append("--------------")
    row0.append("---------------------------------------------")
  finalTable.append(row0)


def rowBuilder(infoText, data, index):
  row0 = []
  for x in range(args.col):
    if x + index < len(data):
      row0.append(infoText)
      row0.append(data[x + index])
  finalTable.append(row0)


rowSeparator()

for i in range(0, len(disks), args.col):
  rowBuilder("device", disk_device, i)
  rowBuilder("type", disk_type, i)
  rowBuilder("mounts", disk_mounts, i)
  rowBuilder("model", disk_model, i)
  rowBuilder("temperature", disk_temp, i)
  rowBuilder("capacity", disk_capacity, i)
  rowBuilder("space", disk_space, i)
  rowBuilder("power on hours", disk_hours, i)
  rowBuilder("data writes", disk_writes, i)
  rowBuilder("errors", disk_errors, i)
  rowSeparator()


#
#
#
#
#
   
totalCapacity  /= (1024*1024*1024*1024) # convert bytes to TB
totalUsedSpace /= (1024*1024*1024*1024)
totalFreeSpace = totalCapacity - totalUsedSpace
if totalCapacity > 0:
  used = 100 * totalUsedSpace / totalCapacity
tmp = f"{used:.0f}% ["
for i in range(int(int(used) / scale)):
  tmp += "#"
for i in range(int(100 / scale - int(used) / scale)):
  tmp += "."
tmp += "]"
if used > 70:
  color0 = colorRED
elif used > 55:
  color0 = colorYELLOW
else:
  color0 = colorGREEN

finalTable.append(["TOTAL space", f"{colorYELLOW}{colorBOLD}{totalCapacity:.1f} TB{colorENDC}"])
finalTable.append(["TOTAL free",f"{colorYELLOW}{colorBOLD}{totalFreeSpace:.1f} TB{colorENDC}"])
finalTable.append(["TOTAL used",f"{color0}{colorBOLD}{tmp}{colorENDC}"])
rowSeparator()


#
#
#
#
#

print(tabulate(finalTable, colalign=("right",), tablefmt="orgtbl"))


#
# delete all tmp files
#
subprocess.getoutput(f"rm {tempFileDF}")
for disk in disks: subprocess.getoutput(f"rm {tempFiles[disk]}")

