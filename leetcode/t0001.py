#!/usr/bin/python3

dictionary = 'ABCDEFG'
dictionary_len = len(dictionary)
result = []


def backtracker(s0: str, l_idx: int, result0: str):
    if l_idx == dictionary_len - 1:
        result.append(result0)
    else:
        for i in range(l_idx, dictionary_len):
            backtracker(s0[:i] + s0[i + 1:], l_idx + 1, result0 + s0[i])


backtracker(dictionary, 0, '')
print(result)
