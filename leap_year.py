#!/usr/local/bin/python3

leap_year=0
year=int(input("Which year to check? "))
if year % 4 == 0:
  leap_year=1
  if year % 100 == 0:
    leap_year=0
    if year % 400 == 0:
      leap_year=1
  else:
    leap_year=1

if leap_year == 1:
  print(f"{year} is leap year")
else:
  print(f"{year} is not leap year")

