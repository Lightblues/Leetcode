""" n种商品有价格, 每种至少保留一个, 问一个序列最多卖出的价格

"""
from collections import Counter
n = int(input())
goods = {}
for _ in range(n):
    name,price = input().split()
    goods[name] = int(price)
m = int(input())
goodsHave = input().split()
cnt = Counter(goodsHave)
ans = 0
for n,c in cnt.items():
    if n in goods:
        ans += (c-1) * goods[n]
print(ans)
    

