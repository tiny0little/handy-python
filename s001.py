#!/usr/bin/python3.8

import subprocess

files = subprocess.getoutput("ls /media/HDD-*/*/*plot").split("\n")

for file in files:
    tmp0 = file.split("-")[-1].split(".")[0]
    count = int(subprocess.getoutput(f"ls /media/HDD-*/*/*{tmp0}* | wc -l").split("\n")[0])
    if count > 1:
        print(f"{tmp0} is more than one")
