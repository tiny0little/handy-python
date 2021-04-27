#!/usr/bin/python3.8

import subprocess

TEMP_FILE="/tmp/disk-health.tmp"

subprocess.getoutput("sudo ls")

output = subprocess.getoutput("lsblk -r | grep disk | awk '{print $1}'")
disks = output.split("\n")
for disk in disks:
  print("--------------------------------")
  print(f"/dev/{disk}")
  subprocess.getoutput(f"sudo smartctl -a /dev/{disk} > {TEMP_FILE}")
  print(subprocess.getoutput(f"cat {TEMP_FILE} | egrep Model "))


