""" New Year Chaos 
对于一个 [1,2....n] 序列, 每次可以通过bride让一个人与前一个人进行交换, 但每个人最多交换两次; 问最少需要多少次交换才能得到目标序列.
思路1: 问题等价于求 #逆序对 但是有移动的限制! 
    可以通过 #归并排序 来实现
    复杂度: O(nlogn) 但没写出来orz
思路2: 考虑本题最多bride两次的特殊性! 
    只需要「从后往前」考虑 (不考虑x往后移动的情况, 原本在x的人只可能出现在x,x-1,x-2位置上)
    因此, 从后往前, 每次找当前序列中的最大值x, 从而得到规模 -1 的子问题. 
[官答](https://www.hackerrank.com/challenges/one-week-preparation-kit-new-year-chaos/editorial)
"""

#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'minimumBribes' function below.
#
# The function accepts INTEGER_ARRAY q as parameter.
#

def minimumBribes(q):
    # Write your code here
    ans = 0
    n = len(q)
    for i in range(n-1,-1,-1):
        x = q[i]
        if x!=i+1:
            if q[i-1]==i+1:
                q[i-1] = x
                ans += 1
            elif q[i-2]==i+1:
                q[i-2],q[i-1] = q[i-1],x
                ans += 2
            else:
                print("Too chaotic")
                return 
    print(ans)
    

def minimumBribes(q):
    """ 尝试写归并排序, 但是WA了! """
    # Write your code here
    for i,x in enumerate(q):
        if i<x-3: print("Too chaotic"); return
    n = len(q)
    def merge(i,j):
        if i==j: return 0
        ans = 0
        mid = (i+j)//2
        a,b = merge(i,mid),merge(mid+1,j)
        if a<0 or b<0: return -1
        ans += a+b
        l,r = i,mid+1
        new = []
        while l<=mid or r<=j:
            if l>mid:
                new += q[r:j+1]; break
            elif r>j:
                new += q[l:mid+1]; break
            else:
                if q[l]>q[r]:
                    steps = mid+1-l
                    if steps>2: return -1
                    ans += steps
                    new.append(q[r]); r += 1
                else:
                    new.append(q[l]); l += 1
        q[i:j+1] = new
        return ans
    a = merge(0,n-1)
    if a<0: print("Too chaotic")
    else: print(a)
    

if __name__ == '__main__':
    t = int(input().strip())

    for t_itr in range(t):
        n = int(input().strip())

        q = list(map(int, input().rstrip().split()))

        minimumBribes(q)
