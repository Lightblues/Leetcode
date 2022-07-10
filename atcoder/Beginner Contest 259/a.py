""" 
A - Growth Record


https://atcoder.jp/contests/abc259/tasks/abc259_a
"""
m,n,x,t,d = map(int, input().split())
if n>=x:
    print(t)
else:
    print(t - d*(x-n))