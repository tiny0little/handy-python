#!/usr/local/bin/python3

# Write a Python program to get a string made of the first 2 and the last 2 chars from a given a string


myString = input("Please enter your string: ")
if len(myString) >= 4:
  print(myString[0:2]+myString[-2:])
else:
  print("Your string is too short")

