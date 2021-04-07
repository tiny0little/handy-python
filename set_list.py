#!/usr/local/bin/python3

# https://www.w3resource.com/python-exercises/basic/
# 1. Write a Python function that takes a sequence of numbers
#    and determines whether all the numbers are different from
#    each other

myList = list(input("Please enter your list of characters: "))
print(f"You've entered {myList}")

if len(myList) == len(set(myList)):
  print("result> Your list has no repeated elements")
else:
  print("result> Your list has repeated elements")

