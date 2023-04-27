""" abc250e 难度 1421
https://atcoder.jp/contests/abc250/tasks/abc250_e

输入 n(≤2e5) 和两个长为 n 的数组 a 和 b，元素范围在 [1,1e9]。
然后输入 q(≤2e5) 表示 q 个询问，每个询问输入两个数 x 和 y，范围在 [1,n]。
对每个询问，设 a 的前 x 个元素去重得到集合 A，b 的前 y 个元素去重得到集合 B，如果 A = B，输出 "Yes"，否则输出 "No"。


https://atcoder.jp/contests/abc250/submissions/35814659

为方便处理，首先把数组 a 转换成升序：
例如，先把 31412 置换为 12324，然后求前缀最大值得到 12334（不影响答案的正确性）。
数组 b 也做同样的置换，然后用 https://leetcode.cn/problems/max-chunks-to-make-sorted/ 中提到的技巧，标记 b[i] 应该匹配到 a 中的哪个数字。

思路1: 参考灵神
    如何标记 arra 的前缀数组中出现的数字有哪些? 将数字 #替换 为升序结构, 然后求前缀最大值即可! 我们仅需要用一个数字即可表示 arra[:i] 中的元素了
    如何将 arrb 关联上来? 做同样的替换. 我们可以依次判断前缀set是否完整 (下面的 `mx + 1 == len(setb)`), 来判断是否可以匹配到arra的某个前缀. 
    关联: 0769. 最多能完成排序的块 #medium

5
1 2 3 4 5
1 2 2 4 3
7
1 1
2 2
2 3
3 3
4 4
4 5
5 5

"""

N = int(input())
arra = list(map(int, input().split()))
arrb = list(map(int, input().split()))

val2map = {}
for i,a in enumerate(arra):
    if a not in val2map:
        val2map[a] = len(val2map)
arra = [val2map[a] for a in arra]
arrb = [val2map[b] if b in val2map else -1 for b in arrb]
# 计算前缀最大值
mx = 0
for i in range(N):
    mx = max(arra[i], mx)
    arra[i] = mx
setb = set()
mx = 0
for i,b in enumerate(arrb):
    if b == -1:
        for j in range(i,N): arrb[j]= -1
        break
    mx = max(b, mx)
    setb.add(b)
    # 关键: 判断前缀set是否完整!
    if mx + 1 == len(setb):
        arrb[i] = mx
    else:
        arrb[i] = -1

Q = int(input())
for _ in range(Q):
    x,y = map(int, input().split())
    print("Yes" if arra[x-1] == arrb[y-1] else "No")

