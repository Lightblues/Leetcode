""" Lego Blocks 
有大小分别为 (1,1),(1,2),(1,3),(1,4) 的砖块要构成 (n,m) 的矩形, 问有多少种构造方法?
要求: 1] 砖块只能横着放, 也即拼成宽度为m的一条; 2] 构成的矩形不能被竖着切开 (有竖线) 
思路1: 简化问题; #DP
    先不考虑条件2, 则问题化简为, 若构成宽m的方案数量为 f[m], 则不考虑条件2可以平铺的方案数量 g[m,n] = f[m] ^ n
        显然, 对于 f有DP转移 f[x] = sum{ f[x-i] } i=1...4
    再考虑约束2下的方案 h[m,n], 我们只需要去掉不合法的情况. 为了避免重复, 我们枚举第一个竖线的位置 1... m-1
        则有 h[m,n] = g[m,n] - sum{ h[i,n] * g[m-i,n] }
"""

#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'legoBlocks' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. INTEGER m
#

def legoBlocks(n, m):
    # Write your code here
    MOD = 10**9+7
    f = [0] * m
    f[:4] = [1,2,4,8]       # 直接暴力初始化了
    for i in range(4,m):
        f[i] = f[i-1]+f[i-2]+f[i-3]+f[i-4]
    g = [pow(x,n,MOD) for x in f]
    h = g[:]
    # 注意下面的下标都是 -1 的!
    for i in range(1,m):
        width = i+1
        for j in range(1,width):
            h[i] -= h[j-1]*g[width-j-1]
    return h[m-1] % MOD


if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')
    # fptr = open('tmp.txt', 'w')

    t = int(input().strip())

    for t_itr in range(t):
        first_multiple_input = input().rstrip().split()

        n = int(first_multiple_input[0])

        m = int(first_multiple_input[1])

        result = legoBlocks(n, m)
        print(result)

        # fptr.write(str(result) + '\n')

    # fptr.close()
