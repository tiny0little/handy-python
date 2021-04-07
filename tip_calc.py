#!/usr/local/bin/python3

bill = input("What's the total bill? ")
tip = input("How much would you like to tip (in %)? ")
people = input("How many people to split the bill? ")

result = float(bill) * (1 + (float(tip) / 100)) / float(people)
result = "{:.2f}".format(result)
print(f"Each people will pay {result}")

