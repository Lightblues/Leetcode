""" 对于两个序列 a,b, 可以交换对应的位置元素, 问至少交换多少次, 使得a,b两个序列相邻元素差值之和最大
限制: n 2e5
思路1: 
    化简: 考虑如何求得最大值? 可以根据DP来计算. 复杂度 O(n)
    那么如何得到最小调换? 记录当前位置的元素来自 a/b 
    
    定义 f(i, 0/1) 表示是否调换最后一个元素, 取得差值的最小次数
    
"""

def minSwap(arra:list[int], arrb:list[int]):
    """ #WA 注意 da==db 的时候是不对的! """
    n = len(arra)
    cntA = 1
    a,b = arra[0], arrb[0]
    for i in range(1, n):
        na,nb = arra[i], arrb[i]
        da,db = abs(a-na)+abs(b-nb), abs(a-nb)+abs(b-na)
        if da>=db:
            cntA += 1
            a,b = na,nb
        else:
            a,b = nb,na
    ans = min(cntA, n-cntA)
    return ans

def minSwap(arra:list[int], arrb:list[int]):
    n = len(arra)
    fa, fb = 0, 1
    # 直到该位置, 并且最后的元素交换/不交换 的最小代价
    for i in range(1, n):
        da = abs(arra[i]-arra[i-1]) + abs(arrb[i]-arrb[i-1])
        db = abs(arra[i]-arrb[i-1]) + abs(arrb[i]-arra[i-1])
        # 注意, 对于nfb总需要+1
        if da>db:
            nfa = fa
            nfb = fb + 1
        elif da<db:
            nfa = fb
            nfb = fa + 1
        else:
            nfa = min(fa, fb)
            nfb = min(fb, fa) + 1
        fa, fb = nfa, nfb
    return min(fa, fb)


n = int(input())
for _ in range(n):
    _ = int(input())
    arra = list(map(int, input().split()))
    arrb = list(map(int, input().split()))
    print(minSwap(arra, arrb))
