from easonsi.util.leetcode import *

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
Easonsi @2023 """
class Solution:
    """ 0036. 有效的数独 #medium 只需要检查填入部分是否合法即可, 并不要求是否可解 """
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # isValid = True
        def isUnique(l):
            return len(set(l))==len(l)
        for line in board:
            if not isUnique([n for n in line if n!='.']):
                return False
        for i in range(9):
            col = [line[i] for line in board if line[i]!='.']
            if not isUnique(col):
                return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                subBoard = [line[j:j+3] for line in board[i:i+3]]
                subBoard = [i for line in subBoard for i in line if i!= '.']
                if not isUnique(subBoard):
                    return False
        return True
    
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
