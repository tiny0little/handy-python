#!/usr/local/bin/python3

# https://www.w3resource.com/python-exercises/list/
# 1. Write a Python program to sum all the items in a list

myList = input("pleas enter your space-separated list of numbers: ").split(" ")

for k in range(len(myList)):
    if not myList[k].isnumeric():
        print(f"{myList[k]} is not a number")
        myList.pop(k)

print(myList)

