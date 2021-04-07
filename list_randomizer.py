#!/usr/local/bin/python3

# Write a Python program to create all possible strings by using entered list characters

import random
import math


myList=list(input("Enter you list: "))
number_of_combinations=math.factorial(len(myList))
print(f"Number of combinations is {number_of_combinations}")
for i in range(1,number_of_combinations):
  random.shuffle(myList)
  print(''.join(myList), end=' ')

