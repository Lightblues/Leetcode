""" 
from https://atcoder.jp/contests/abc259/submissions/33172480
为什么这个可以过而我写的版本 https://atcoder.jp/contests/abc259/submissions/33157146 会 TLE??
"""

class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1 for _ in range(n)]
 
    def find(self, x):
        if self.parents[x] < 0:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.parents[x]
 
    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
 
        if x == y:
            return
 
        if self.parents[x] > self.parents[y]:  # マージテク
            x, y = y, x
 
        self.parents[x] += self.parents[y]
        self.parents[y] = x
 
def dist(x1, y1, x2, y2):
   return (x1 - x2) ** 2 + (y1 - y2) ** 2
 
 
N = int(input())
sx, sy, tx, ty = map(int, input().split())
 
X = []
Y = []
R = []
for _ in range(N):
    x, y, r = map(int, input().split())
    X.append(x)
    Y.append(y)
    R.append(r)
 
uf = UnionFind(N)
for i in range(N):
    for j in range(i + 1, N):
        d = dist(X[i], Y[i], X[j], Y[j])
        if abs(R[i] - R[j])**2 <= d <= (R[i] + R[j])**2: uf.union(i, j)
 
for i in range(N):
    sd = dist(X[i], Y[i], sx, sy)
    if sd == R[i]**2 : sn = i
 
    td = dist(X[i], Y[i], tx, ty)
    if td == R[i]**2 : tn = i
 
if uf.find(sn) == uf.find(tn): print('Yes')
else: print('No')