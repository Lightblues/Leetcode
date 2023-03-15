""" Jesse and Cookies
一道基本的heap的题目
 """

#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'cookies' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER k
#  2. INTEGER_ARRAY A
#
import heapq

def cookies(k, A):
    # Write your code here
    h = A
    heapq.heapify(h)
    ans = 0
    while h[0]<k:
        if len(h)<2: return -1
        a,b = heapq.heappop(h), heapq.heappop(h)
        new = a + 2*b
        heapq.heappush(h, new)
        ans += 1
    return ans

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    k = int(first_multiple_input[1])

    A = list(map(int, input().rstrip().split()))

    result = cookies(k, A)

    fptr.write(str(result) + '\n')

    fptr.close()
