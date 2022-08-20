""" H. Gambling
题目搞得花里胡哨, 归纳: 给定一个长n的数组, 返回一个区间 [l,r] 和数字a, 使区间中数字a出现的次数 - 其他数字的数量最大.
限制: 数组长度 n 2e5, 数组元素 1e9.
思路1: 直接遍历 #模拟
    考虑每一个数字, 我们将其看成 1/-1 的数组中, 求区间得到最大值. (实际上用idx数组记录). 遍历过程中, 我们 #贪心 舍弃不需要的部分.
    例如, 若之前记录了 [0,1] 位置为正数 (此时最大正数记录为2), 下一个正数坐标为 4, 由于 `sum(nums[:4]) = 2; +2 - (4-2) = 0 <=0`, 我们可以不考虑, 将记录重置为 `[4]`
    复杂度: 具体的实现上, 用了dict来存储数字到位置的映射. 若哈希表的操作复杂度为 O(1), 则时间复杂度为 O(n).
        但实际上被hack了😭. 因为发生哈希冲突的情况下, 复杂度可能上升为 `O(n^2)` ! 另外的答案中, 所有的数字都用的是 str 就可以过 (理论上也可以被hack 只不过还没有).
    参见: [哈希冲突及解决方法](https://blog.csdn.net/qq_41963107/article/details/107849048) 以及 [Python的字典实现](https://harveyqing.gitbooks.io/python-read-and-write/content/python_advance/python_dict_implementation.html), 另外 [这篇](https://zhuanlan.zhihu.com/p/74003719) 更加直观一些.
思路2: 也是因为上述原因? 所以官答用了 #线段树 来解的.

https://codeforces.com/contest/1692/problem/H
"""
# from collections import defaultdict
# import sys
# input = sys.stdin.readline
# def f0():
#     n = int(input())
#     arr = list(map(int, input().split()))
#     a2idx = defaultdict(list)
#     mx = 1; ans = [arr[0], 0, 0]
#     for i,a in enumerate(arr):
#         idxs = a2idx[a]
#         if len(idxs)==0:
#             idxs.append(i)
#         else:
#             acc = len(idxs) - (i-idxs[0] - len(idxs))
#             if  acc <= 0:
#                 a2idx[a] = [i]
#             else:
#                 idxs.append(i)
#                 if acc+1 > mx:
#                     mx = acc+1
#                     ans = [a, idxs[0], idxs[-1]]
#     print(ans[0], ans[1]+1, ans[2]+1)

""" 尝试三个地方优化: 不用defaultdict; 用sys.stdin.readline; 不用list
发现原因在于 list(map(int, ...)), 因为用了 dict+int 被hack了: 哈希表冲突导致复杂度可能上升到 O(n^2); 而答案中用了str理论上可以被hack只不过还没有罢了.
"""
from collections import defaultdict
# import sys
# input = sys.stdin.readline
def f():
    n = int(input())
    # 魔鬼... 这里转了 list 就过不了
    arr = list(map(int, input().split()))
    # arr = input().split()
    a2idx = defaultdict(int); a2len = defaultdict(int)
    # a2idx = {}; a2len = {}
    mx = 1; ans = [arr[0], 0, 0]
    for i,a in enumerate(arr):
        if a not in a2idx:
            a2idx[a] = i; a2len[a] = 1
        else:
            acc = a2len[a] - (i-a2idx[a] - a2len[a])
            if  acc <= 0:
                a2idx[a] = i; a2len[a] = 1
            else:
                a2len[a] += 1
                if acc+1 > mx:
                    mx = acc+1
                    ans = [a, a2idx[a], i]
    print(ans[0], ans[1]+1, ans[2]+1)

for _ in range(int(input())): f()


# Test #38
# 1
# 200000
# 131073 131073 6 6 31 31 156 156 7 ....

# l = map(str, "131073 131073 6 6 31 31 156 156 781 781 3906 3906 19531 19531 97656 97656 95065 95065 82110 82110 17335 17335 86676 86676 40165 40165 69754 69754 86627 86627 39920 39920 68529 68529 80502 80502 9295 9295 46476 46476 101309 101309 113330 113330 42363 42363 80744 80744 10505 10505 52526 52526 487 487 2436 2436 12181 12181 60906 60906 42387 42387 80864 80864 11105 11105 55526 55526 15487 15487 77436 77436 125037 125037 100898 100898 111275 111275 32088 32088 29369 29369 15774 15774 78871 78871 1140".split())
# from collections import Counter
# c = Counter(map(hash, l))
# sorted(c)