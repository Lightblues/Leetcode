from typing import List

class Solution:
    """ 0784.Letter-Case-Permutation/ """
    def letterCasePermutation(self, s: str) -> List[str]:
        result = [[]]
        for char in s:
            lenResult = len(result)
            if char.isalpha():
                for i in range(lenResult):
                    result.append(result[i][:])
                    result[i].append(char.lower())
                    result[lenResult+i].append(char.upper())
            else:
                for i in range(lenResult):
                    result[i].append(char)
        return list(map("".join, result))

sol = Solution()
reslts = [
    sol.letterCasePermutation("abc"),
]
for r in reslts:
    print(r)