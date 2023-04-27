""" 有一组商品(包括了类目), 要求实现下面的需求,
1] 在每一个长为n的窗口内, 保证至少有两种类目
2] 在满足1]的情况下, 使得物品向后移动的尽可能少
另一种表述: 保证不出现连续n个相同类目的前提下, 尽量是的物品向后移动的距离最小

n = 3
1 2 3 4 5 6 7 8 9 10
a a a a b c c c d d
输出: 
1 2 5 3 4 6 7 9 8 10

思路1: 贪心, 每次保证不会出现连续的长度为n的相同类目
    基本的思路, 就是模拟滑动窗口, 
        然后检查当前滑窗内是否只有一种类目, 
        如果是的话, 找到下一个不是该类目的商品, 将它提前放到滑窗内
    如何实现最小向后移动? 贪心, 向前移动物品的数量最少. 
"""

from collections import Counter

def f(items, cats, n):
    l = len(items)
    # 利用 Counter 检查是否只有一种类目
    c = Counter(cats[:n])
    # 遍历滑动窗口
    for i in range(n-1,l):
        # 更新窗口 [i-n+1:i] 窗口内的类目计数
        c[cats[i]] += 1
        # 删除滑窗过期的那个商品, 更新cnt
        if i>=n:
            cc = cats[i-n]
            c[cc] -= 1
            if c[cc] == 0:
                del c[cc]
        
        # 若发生了冲突, 找到下一个不同的类目, 然后进行修改
        if len(c)==1:
            cat = list(c)[0]
            # 找到下一个不同的类目
            for j in range(i,l):
                if cats[j] != cat:
                    break
            # 将那个类目提前放到 i 位置
            items = items[:i] + [items[j]] + items[i:j] + items[j+1:]
            cats = cats[:i] + [cats[j]] + cats[i:j] + cats[j+1:]
            # 更新cnt
            c = Counter(cats[i-n+1:i+1])

    return items

res = f(
    "1 2 3 4 5 6 7 8 9 10".split(), "a a a a b c c c d d".split(), 3
)
print(res)

