""" 一个基本的BFS求距离

"""
#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'bfs' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER n
#  2. INTEGER m
#  3. 2D_INTEGER_ARRAY edges
#  4. INTEGER s
#
from collections import deque
def bfs(n, m, edges, start):
    # Write your code here
    g = [[] for _ in range(n)]
    for s,e in edges:
        s,e = s-1,e-1
        g[s].append(e)
        g[e].append(s)
    start -= 1
    dist = [-1] * n
    dist[start] = 0
    visited = set([start])
    q = deque([(start,0)])
    while q:
        u,d = q.popleft()
        for v in g[u]:
            if v in visited:
                continue
            q.append((v,d+6))
            dist[v] = d+6
            visited.add(v)
    return [i for i in dist if i!=0]
    
    
    

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input().strip())

    for q_itr in range(q):
        first_multiple_input = input().rstrip().split()

        n = int(first_multiple_input[0])

        m = int(first_multiple_input[1])

        edges = []

        for _ in range(m):
            edges.append(list(map(int, input().rstrip().split())))

        s = int(input().strip())

        result = bfs(n, m, edges, s)

        fptr.write(' '.join(map(str, result)))
        fptr.write('\n')

    fptr.close()

