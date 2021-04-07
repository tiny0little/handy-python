#!/usr/local/bin/python3

# validate if entered numbers is odd or even


number = int(input("Enter your number "))
if number % 2 == 0:
  print(f"{number} is even")
else:
  print(f"{number} is odd")
