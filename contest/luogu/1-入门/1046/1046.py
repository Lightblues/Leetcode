""" P1046 [NOIP2005 普及组] 陶陶摘苹果 #入门

"""
s = map(int, input().split())
ava = int(input()) + 30
print(sum(i<=ava for i in s))