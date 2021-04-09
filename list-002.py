#!/usr/local/bin/python3

# https://www.w3resource.com/python-exercises/list/
# 3. Write a Python program to get the largest number from a list

myList = input("pleas enter your space-separated list of numbers: ").split(" ")


# removing not-numeric items
k = 0
while k < len(myList):
    if not myList[k].isnumeric():
        print(f">>> {myList[k]} is not a number")
        myList.pop(k)
        k -= 1
    k += 1


largest = 0
for v in myList:
    if largest < int(v):
        largest = int(v)

print(f"largest number from the list is {largest}")
