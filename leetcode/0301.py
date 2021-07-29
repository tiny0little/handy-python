#!/usr/bin/python3
"""
301. Remove Invalid Parentheses
Difficulty: Hard

"""
from typing import List
import time


class Solution:
    def count_invalid_parentheses(self, s: str) -> List[int]:
        left_p_count = 0
        right_p_count = 0
        for i in range(len(s)):
            if s[i] == '(': left_p_count += 1
            if s[i] == ')':
                if left_p_count > 0:
                    left_p_count -= 1
                else:
                    right_p_count += 1

        return [left_p_count, right_p_count]

    def bit_mask_to_list(self, bit_mask: int, bits: int) -> List[int]:
        tmp1 = str(bin(bit_mask))[2:].zfill(bits)[:bits]
        return [int(_) for _ in tmp1]

    def removeInvalidParentheses(self, s: str) -> List[str]:
        s = ''.join(s.split())
        # optimization
        # removing heading and tailing `wrong` parentheses
        if len(s) > 0:
            while s[0] == ')':
                s = s[1:]
                if len(s) == 0: break
        if len(s) > 0:
            while s[-1] == '(':
                s = s[:len(s) - 1]
                if len(s) == 0: break

        invalid_parentheses = self.count_invalid_parentheses(s)
        invalid_parentheses_sum = sum(invalid_parentheses)
        if invalid_parentheses_sum == 0: return [s]

        bit_mask = 0
        s_len = len(s)
        result = []

        while bit_mask < 2 ** s_len:

            # will only use bit_mask which has same number of 1s as number of invalid parentheses
            bit_mask += 1
            while bin(bit_mask).count('1') != invalid_parentheses_sum: bit_mask += 1
            bit_mask_list = self.bit_mask_to_list(bit_mask, s_len)

            # compare count of removed parentheses to invalid_parentheses
            removed_parentheses = [0, 0]
            for i in range(s_len):
                if bit_mask_list[i] == 1:
                    if s[i] == '(': removed_parentheses[0] += 1
                    if s[i] == ')': removed_parentheses[1] += 1
            if removed_parentheses != invalid_parentheses: continue

            # will keep bit positions which are '0'
            s_candidate = ''
            for i in range(s_len):
                if bit_mask_list[i] == 0:
                    s_candidate += s[i]

            if self.count_invalid_parentheses(s_candidate) == [0, 0]:
                if s_candidate not in result:
                    result.append(s_candidate)

        if len(result) == 0: result.append('')
        return result


sol = Solution()
stime = time.time()
print(sol.removeInvalidParentheses(s="((()()()(())()))))))))))"))
print(f'runtime: {time.time() - stime:.2f}sec')

stime = time.time()
if sorted(sol.removeInvalidParentheses(s="()())()")) != sorted(['(())()', '()()()']): print('err-1')
if sorted(sol.removeInvalidParentheses(s="(a)())()")) != sorted(['(a())()', '(a)()()']): print('err-2')
if sol.removeInvalidParentheses(s=")(") != ['']: print('err-3')
if sol.removeInvalidParentheses(s=")()(") != ['()']: print('err-53')
if sol.removeInvalidParentheses(s="n") != ['n']: print('err-40')
if sol.removeInvalidParentheses(s=")(f") != ['f']: print('err-43')
if sorted(sol.removeInvalidParentheses(s=")(()(()))(a(e()")) != \
        sorted(["(()(()))ae()", "(()(()))a(e)", "(()(()))(ae)"]): print('err-87')
if sol.removeInvalidParentheses(s=")((())))))()(((l((((") != ['((()))()l']: print('err-114')
if sol.removeInvalidParentheses(s="))") != ['']: print('err-5')
if sorted(sol.removeInvalidParentheses(s="(((k()((")) != sorted(["k()", "(k)"]): print('err-120')

if sorted(sol.removeInvalidParentheses(s="()((c))()())(m)))()(")) != \
        sorted(["(((c()())(m)))()", "(((c)(())(m)))()", "(((c)()()(m)))()", "(((c)()())(m))()", "(((c))(()(m)))()",
                "(((c))(())(m))()", "(((c))()((m)))()", "(((c))()()(m))()", "(((c))()())(m)()", "()((c(())(m)))()",
                "()((c()()(m)))()", "()((c()())(m))()", "()((c)(()(m)))()", "()((c)(())(m))()", "()((c)()((m)))()",
                "()((c)()()(m))()", "()((c)()())(m)()", "()((c))(((m)))()", "()((c))(()(m))()", "()((c))(())(m)()",
                "()((c))()((m))()", "()((c))()()(m)()"]): print('err-122')

if sorted(sol.removeInvalidParentheses(s=")()()i)())b(())h))))")) != sorted(
        ["((i(b(()h))))", "((i(b(())h)))", "((i()b((h))))", "((i()b(()h)))", "((i()b(())h))", "((i())b((h)))",
         "((i())b(()h))", "((i())b(())h)", "((i)(b((h))))", "((i)(b(()h)))", "((i)(b(())h))", "((i)()b((h)))",
         "((i)()b(()h))", "((i)()b(())h)", "((i)())b((h))", "((i)())b(()h)", "((i)())b(())h", "(()i(b((h))))",
         "(()i(b(()h)))", "(()i(b(())h))", "(()i()b((h)))", "(()i()b(()h))", "(()i()b(())h)", "(()i())b((h))",
         "(()i())b(()h)", "(()i())b(())h", "(()i)(b((h)))", "(()i)(b(()h))", "(()i)(b(())h)", "(()i)()b((h))",
         "(()i)()b(()h)", "(()i)()b(())h", "()(i(b((h))))", "()(i(b(()h)))", "()(i(b(())h))", "()(i()b((h)))",
         "()(i()b(()h))", "()(i()b(())h)", "()(i())b((h))", "()(i())b(()h)", "()(i())b(())h", "()(i)(b((h)))",
         "()(i)(b(()h))", "()(i)(b(())h)", "()(i)()b((h))", "()(i)()b(()h)", "()(i)()b(())h", "()()i(b((h)))",
         "()()i(b(()h))", "()()i(b(())h)", "()()i()b((h))", "()()i()b(()h)", "()()i()b(())h"]): print('err-125')

print(f'>>> all tests runtime: {time.time() - stime:.2f}sec')
