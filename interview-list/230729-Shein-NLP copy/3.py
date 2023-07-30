""" 实现一个简单的计算器，输入一个字符串，其中只包含非负整数、加法、减法以及乘法和除法字符，返回该表达式的计算结果。

"""


import math

def calculate(s: str) -> int:
    stack_num = []
    stack_opt = []
    i = 0
    priorty = {'(':0,')':0,'+':1,'-':1,'*':2,'/':2}
    while i<len(s):
        if s[i]==' ':
            i += 1
            continue
        if '0'<=s[i]<='9':
            j = i
            while i+1<len(s) and '0'<=s[i+1]<='9':
                i += 1
            num = int(s[j:i+1])
            stack_num.append(num)
        elif s[i]=='(':
            stack_opt.append(s[i])
        elif s[i]==')':
            while stack_opt[-1]!='(':
                opt = stack_opt.pop()
                A = stack_num.pop()
                B = stack_num.pop()
                res = calc(A,B,opt)
                stack_num.append(res)
            stack_opt.pop()
        else:
            while stack_opt and priorty[stack_opt[-1]]>=priorty[s[i]]:
                opt = stack_opt.pop()
                A = stack_num.pop()
                B = stack_num.pop()
                res = calc(A,B,opt)
                stack_num.append(res)
            stack_opt.append(s[i])
        i += 1

    while stack_opt:
        opt = stack_opt.pop()
        A = stack_num.pop()
        B = stack_num.pop()
        res = calc(A,B,opt)
        stack_num.append(res)
    return stack_num[-1]

def calc(num1,num2,opt):
    if opt=='+':
        return int(num1)+int(num2)
    elif opt=='-':
        return int(num2)-int(num1)
    elif opt=='*':
        return int(num2)*int(num1)
    elif opt=='/':
        return math.ceil(int(num2)/int(num1))


import collections
from typing import List
def calculate(s: str) -> int:
        
    def helper(s: List) -> int:
        stack = []
        sign = '+'
        num = 0

        while len(s) > 0:
            c = s.popleft()
            if c.isdigit():
                num = 10 * num + int(c)
            # 遇到左括号开始递归计算 num
            if c == '(':
                num = helper(s)

            if (not c.isdigit() and c != ' ') or len(s) == 0:
                if sign == '+':
                    stack.append(num)
                elif sign == '-':
                    stack.append(-num)
                elif sign == '*':
                    stack[-1] = stack[-1] * num
                elif sign == '/':
                    # python 除法向 0 取整的写法
                    # stack[-1] = int(stack[-1] / float(num))      
                    stack[-1] = math.ceil(stack[-1] / num) 
                num = 0
                sign = c
            # 遇到右括号返回递归结果
            if c == ')': break
        return sum(stack)

    return helper(collections.deque(s))


s = input().strip()
print(calculate(s))