#!/usr/bin/python3

f = open('/home/user/src/python-practice/input_file', 'r')
lines = f.readlines()

for i in range(len(lines)):
    if len(lines[i]) > 1:

        items = lines[i].split(",")
        for x in range(len(items)):
            items[x].strip()
            apt_package = items[x].split("(")
            if apt_package[0][0:5] == "Purge":
                fileName = apt_package[0][7:]
            else:
                fileName = apt_package[0]
            if fileName[0] == " ":
                fileName = fileName[1:]
            print(f"sudo apt install {fileName}")
