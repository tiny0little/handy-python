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
colorWHITEonBLUE = '\33[44m'
colorWHITEonRED = '\33[41m'

TEMP_FILE1 = "/tmp/disk-health1.tmp"
TEMP_FILE2 = "/tmp/disk-health2.tmp"

final_table = []
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
for line in output:
    disks.append(line.split(" ")[0])
if disks[0] == '':
    disks.pop(0)
if not disks:
    print("no disks found")
    exit()

for disk in tqdm(disks, leave=False, desc='processing',
                 bar_format='{desc}:{percentage:3.0f}%|{bar:67}|[{elapsed}<{remaining}]'):
    subprocess.getoutput(f"sudo smartctl -a /dev/{disk} > {TEMP_FILE1}")

    lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Rotation").split("\n")
    type0 = f"{colorWHITEonBLUE}SSD{colorENDC}"
    if "rpm" in lines[0]:
        type0 = f"{colorWHITEonRED}HDD{colorENDC}"

    if (args.device_type not in type0.lower()) and (args.device_type != 'all'):
        continue

    disk_type.append(type0)
    disk_device.append(f"/dev/{disk}")

    tmp0 = subprocess.getoutput(f"cat {TEMP_FILE2} | egrep {disk}").split("\n")
    mount = ''
    for tmp1 in tmp0:
        mount = mount + tmp1.split(" ")[-1] + '\n'
    mount = mount[:-1]
    disk_mounts.append(f"{mount}")

    #
    #
    #
    #
    #
    lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Model").split("\n")
    model = []
    for i in range(len(lines)):
        model.append(lines[i].split(":")[1].strip())
    disk_model.append(f"{' '.join(model)}")

    #
    #
    #
    #
    #
    lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Capacity | egrep -v 'Unallocated|NVM'")
    lines = lines[lines.rfind("[") + 1:-1].strip()
    disk_capacity.append(f"{colorBOLD}{colorGREEN}{lines}{colorENDC}")

    #
    #
    #
    #
    #
    lines = subprocess.getoutput(f"cat {TEMP_FILE1} | egrep Tempera | egrep -v 'Warning|Critical|Airflow'")
    if lines.rfind("(",-20) > 0:
      lines = lines[:lines.rfind("(",-20)].strip()
    if lines.rfind("Celsius",-20) > 0:
      lines = lines[:lines.rfind("Celsius",-20)].strip()
    tmp=lines.split(" ")[-1].strip()
    if int(tmp) > 60:
      color=colorRED
    elif int(tmp) > 50:
      color0 = colorYELLOW
    else:
      color0 = colorGREEN
    tmp=f"{color0}{colorBOLD}{tmp}C{colorENDC}"
    disk_temp.append(tmp)


    #
    #
    #
    #
    #
    lines = subprocess.getoutput(f"cat {TEMP_FILE2} | egrep {disk} | egrep -v efi")
    tmp = lines.split(" ")
    # if 1st element is empty string -> remove it
    if tmp[0] == '':
        tmp.pop(0)
    # if list is not empty
    if tmp:
        tmp = tmp[len(tmp) - 2].strip()
        used = int(tmp[0:-1])
        tmp = f"{used}% ["
        scale = 2.5
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
        if "[" in lines:
            lines = lines[lines.rfind("[") + 1:-1]
            disk_writes.append(f"{colorBOLD}{colorRED}{lines}{colorENDC}")
        else:
            lines = int(lines[lines.rfind(" ") + 1:]) / 931
            disk_writes.append(f"{colorBOLD}{colorRED}{lines:.2f} TB{colorENDC}")
    else:
        disk_writes.append("-")

#
#
#
final_table.append(["--------------", "---------------------------------------------",
                    "--------------", "---------------------------------------------"])
i = 0
for disk in disks:
    if i < len(disk_device):
        if i + 1 < len(disk_device):
            final_table.append(["disk device", disk_device[i], "disk device", disk_device[i + 1]])
            final_table.append(["type", disk_type[i], "type", disk_type[i + 1]])
            final_table.append(["mounts", disk_mounts[i], "mounts", disk_mounts[i + 1]])
            final_table.append(["model", disk_model[i], "model", disk_model[i + 1]])
            final_table.append(["temperature", disk_temp[i], "temperature", disk_temp[i + 1]])
            final_table.append(["capacity", disk_capacity[i], "capacity", disk_capacity[i + 1]])
            final_table.append(["used space", disk_space[i], "used space", disk_space[i + 1]])
            final_table.append(["power on hours", disk_hours[i], "power on hours", disk_hours[i + 1]])
            final_table.append(["data written", disk_writes[i], "data written", disk_writes[i + 1]])
        else:
            final_table.append(["disk device", disk_device[i]])
            final_table.append(["type", disk_type[i]])
            final_table.append(["mounts", disk_mounts[i]])
            final_table.append(["model", disk_model[i]])
            final_table.append(["temperature", disk_temp[i]])
            final_table.append(["capacity", disk_capacity[i]])
            final_table.append(["used space", disk_space[i]])
            final_table.append(["power on hours", disk_hours[i]])
            final_table.append(["data written", disk_writes[i]])

        final_table.append(["--------------", "---------------------------------------------",
                            "--------------", "---------------------------------------------"])
        i += 2

#
#
#
#
#
print(tabulate(final_table, colalign=("right",), tablefmt="orgtbl"))
subprocess.getoutput(f"rm {TEMP_FILE1}")
subprocess.getoutput(f"rm {TEMP_FILE2}")
