"""
输入：digits = "23"
输出：["ad","ae","af","bd","be","bf","cd","ce","cf"]

输入：digits = ""
输出：[]

---
backtrack，或者说是深度优先搜索。

"""

digits2alph = {
    2: 'abc',
    3: 'def',
    4: 'ghi',
    5: 'jkl',
    6: 'mno',
    7: 'pqrs',
    8: 'tuv',
    9: 'wxyz'
}

class Solution:
    # def letterCombinations(self, digits: str) -> List[str]:
    def letterCombinations(self, digits):
        if not digits:
            return []
        results = []

        combination = []
        def backtrack(depth):
            if depth == len(digits):
                results.append(''.join(combination))
            else:
                d = int(digits[depth])
                for char in digits2alph[d]:
                    combination.append(char)
                    backtrack(depth+1)
                    combination.pop()
        backtrack(0)
        return results

digits = "23"
print(Solution().letterCombinations(digits))