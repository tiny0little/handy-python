#!/usr/bin/python3.8

import subprocess
from tabulate import tabulate
import argparse
from tqdm import tqdm

colorGREEN = '\033[92m'
colorYELLOW = '\033[93m'
colorRED = '\033[91m'
colorENDC = '\033[0m'
colorBOLD = '\033[1m'
colorWHITEonPURPLE = '\33[45m'
colorWHITEonGREEN = '\33[42m'
colorWHITEonBLUE = '\33[44m'
colorWHITEonRED = '\33[41m'

TEMP_FILE1 = "/tmp/disk-health1.tmp"
TEMP_FILE2 = "/tmp/disk-health2.tmp"
scale = 2.5

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

#
#
#
#
#
parser = argparse.ArgumentParser(description="disk summary")
parser.add_argument("-d", "--disk", help="disk device name, can be part of it")
parser.add_argument("device_type", choices=['all', 'ssd', 'hdd'], nargs='?', default='all', const='all',
                    help="which type of devices you would like to see? (default: %(default)s)")
args = parser.parse_args()

# get sudo before we start, we'll need it for smartctl
subprocess.getoutput("sudo ls")

subprocess.getoutput(f"df -m > {TEMP_FILE2}")
if args.disk is None:
    output = subprocess.getoutput(f"lsblk -r | grep disk").split("\n")
else:
    # remove path to the device, leave only device name
    tmp = args.disk[args.disk.rfind("/") + 1:].strip()
    output = subprocess.getoutput(f"lsblk -r | grep disk | cut -d' ' -f1 | grep {tmp}").split("\n")

disks = []
for line in output : disks.append(line.split(" ")[0])
if disks[0] == '' : disks.pop(0)
if not disks:
    print("no disks found")
    exit()

for disk in tqdm(disks, leave=False, desc='processing',
                 bar_format='{desc}:{percentage:3.0f}%|{bar:67}|[{elapsed}<{remaining}]'):
    subprocess.getoutput(f"sudo smartctl -a /dev/{disk} > {TEMP_FILE1}")

    # let's see if we have anything, if nothing, let's try 1st partition -> works for USB flash drives
    lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Model").split("\n")
    if lines[0] == '' : subprocess.getoutput(f"sudo smartctl -a /dev/{disk}1 > {TEMP_FILE1}")




    lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Rotation").split("\n")
    type0 = f"{colorWHITEonGREEN}SSD{colorENDC}"
    if "rpm" in lines[0] : type0 = f"{colorWHITEonPURPLE}HDD{colorENDC}"



    if (args.device_type not in type0.lower()) and (args.device_type != 'all') : continue




    disk_type.append(type0)
    disk_device.append(f"/dev/{disk}")


    #
    #
    #
    #

    tmp0 = subprocess.getoutput(f"cat {TEMP_FILE2} | egrep {disk}").split("\n")
    mount = ''
    for tmp1 in tmp0 : mount = mount + tmp1[tmp1.rfind("%")+1:].strip()+ '\n'
    mount = mount[:-1]
    disk_mounts.append(f"{mount}")

    #
    #
    #
    #
    #
    lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep 'Model|Vendor:|Product:'").split("\n")
    if lines[0] == '' : lines.pop(0)
    model = []
    for i in range(len(lines)) : model.append(lines[i].split(":")[1].strip())
    disk_model.append(f"{' - '.join(model)}")

    #
    #
    #
    #
    #
    lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Capacity | egrep -v 'Unallocated|NVM'")
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
    lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Tempera | egrep -v 'Trip|Warning|Critical|Airflow'")
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

    lines = subprocess.getoutput(f"cat {TEMP_FILE2} | egrep {disk} | egrep -v efi")
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
    lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Hour | egrep -v 'Fly|Load'")
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
        lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Writ | egrep -v 'Comma|NAND'")
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
    tmp0 = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep 'Reallocated_Sector|Current_Pending_Sector|Calibration_Retry_Count|Command_Timeout|Spin_Retry_Count|Calibration_Retry_Count|Offline_Uncorrectable|Error' | egrep -v 'Error_Rate'").split("\n")
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

finalTable.append(["--------------", "---------------------------------------------",
                    "--------------", "---------------------------------------------"])
i = 0
for disk in disks:
    if i < len(disk_device):
        if i + 1 < len(disk_device):
            finalTable.append(["disk device", disk_device[i], "disk device", disk_device[i + 1]])
            finalTable.append(["type", disk_type[i], "type", disk_type[i + 1]])
            finalTable.append(["mounts", disk_mounts[i], "mounts", disk_mounts[i + 1]])
            finalTable.append(["model", disk_model[i], "model", disk_model[i + 1]])
            finalTable.append(["temperature", disk_temp[i], "temperature", disk_temp[i + 1]])
            finalTable.append(["capacity", disk_capacity[i], "capacity", disk_capacity[i + 1]])
            finalTable.append(["used space", disk_space[i], "used space", disk_space[i + 1]])
            finalTable.append(["power on hours", disk_hours[i], "power on hours", disk_hours[i + 1]])
            finalTable.append(["data writes", disk_writes[i], "data writes", disk_writes[i + 1]])
            finalTable.append(["errors", disk_errors[i], "errors", disk_errors[i + 1]])
        else:
            finalTable.append(["disk device", disk_device[i]])
            finalTable.append(["type", disk_type[i]])
            finalTable.append(["mounts", disk_mounts[i]])
            finalTable.append(["model", disk_model[i]])
            finalTable.append(["temperature", disk_temp[i]])
            finalTable.append(["capacity", disk_capacity[i]])
            finalTable.append(["used space", disk_space[i]])
            finalTable.append(["power on hours", disk_hours[i]])
            finalTable.append(["data writes", disk_writes[i]])
            finalTable.append(["errors", disk_errors[i]])

        finalTable.append(["--------------", "---------------------------------------------",
                            "--------------", "---------------------------------------------"])
        i += 2

#
#
#
#
#
   
totalCapacity  /= (1024*1024*1024*1024)
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

finalTable.append(["--------------", "---------------------------------------------",
                   "--------------", "---------------------------------------------"])
finalTable.append(["total capacity", f"{colorYELLOW}{colorBOLD}{totalCapacity:.1f} TB{colorENDC}"])
finalTable.append(["total free space",f"{colorYELLOW}{colorBOLD}{totalFreeSpace:.1f} TB{colorENDC}"])
finalTable.append(["total used space",f"{color0}{colorBOLD}{tmp}{colorENDC}"])
finalTable.append(["--------------", "---------------------------------------------",
                   "--------------", "---------------------------------------------"])

#
#
#
#
#

print(tabulate(finalTable, colalign=("right",), tablefmt="orgtbl"))

subprocess.getoutput(f"rm {TEMP_FILE1}")
subprocess.getoutput(f"rm {TEMP_FILE2}")
