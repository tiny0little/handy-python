#!/usr/local/bin/python3

# Write a Python program to get a string from a given string where all
# occurrences of its first char have been changed to '$', except the
# first char itself

myString = input("Please enter your string: ")

firstChar=myString[0]
myString=myString.replace(firstChar,"$")
myString=firstChar + myString[1:]
print(myString)

