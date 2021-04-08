#!/usr/local/bin/python3

# https://www.w3resource.com/python-exercises/string/
# 8. Write a Python function that takes a list of words
# and returns the longest word and the length of the longest one

input0 = input("please input your list of words: ")
inputList = input0.split(' ')

longest_len=0
for v in inputList:
  if len(v)>longest_len:
      longest_len=len(v)
      longest_item=v

print(f"longest is '{longest_item}'")
