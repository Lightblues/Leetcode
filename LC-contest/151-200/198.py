from easonsi import utils
from easonsi.util.leetcode import *
def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
https://leetcode.cn/contest/weekly-contest-198
T3 也是 hard, 一开始还理解错题目了...虽然本来的问题也很难就是了... T4考了AND的运算性质, 也比较少见.

@2022 """
class Solution:
    """ 1518. 换酒问题 """
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:
        acc = numBottles
        while numBottles >= numExchange:
            new, left = divmod(numBottles, numExchange)
            acc += new
            numBottles = left + new
        return acc
    """ 1519. 子树中标签相同的节点数 """
    def countSubTrees(self, n: int, edges: List[List[int]], labels: str) -> List[int]:
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        
        visited = set()
        ans = [0] * n
        def f(root):
            visited.add(root)
            label = labels[root]
            cnt = Counter()
            cnt[label] += 1
            for child in g[root]:
                if child in visited: continue
                r = f(child)
                cnt += r
            ans[root] = cnt[label]
            return cnt
        f(0)
        return ans
    
    """ 1520. 最多的不重叠子字符串 #hard #题型 #细节
给定一个字符串s, 要求返回一组不重叠子串, 其中每一个子串, 其包含的字符需要是在s中出现的全部. 要求返回的数组长度最大; 若有多个相同长度的, 则返回总长度最小的. e.g. "abbaccd" -> ["d","bb","cc"]. 注意 "abab" -> ["abab"].
限制: ch均为小写; 长度 1e5
思路0: 理解错题目为「给定一个字符串s, 要求返回一组不重叠子串, 其中每一个子串都包含s中全部的某一字符」. 也即 "abab" -> ["aba"].
    将错就错, 但也花了好久写了个 #DP
    对于每一个字符, 其在s中出现的位置区间是 [si,ei]. 假设我们对于其end排序.
    记 `f(idx,i)` 表示在 s[:idx] 中, 仅考虑前i种(根据end排序)字符, 可以得到的不重叠子串有多少.
        递推: `f(idx,i) = max{ f(ei-1,i-1) + 1, f(idx,i-1) }`
思路1: 拓展成符合要求的子串, 然后 #贪心
    对于s中出现的每一个字符, 我们将其对应的区间进行拓展, 使其成为合法的子串.
        问题定义: 每一个字符出现的位置是一个span, 现在要对于span中包含的其他字符进行拓展. 这个问题其实很乱.
        答案中用了更为「暴力」的解法: 直接 `while j<=r` 遍历这一区间, 若出现新的字符则更新l,r指针. (这样复杂度似乎无法保证?)
    这样, 问题就转化为: 「给定一组线段, 要求得到一组数量最多的不重叠线段, 数量相同时要求长度更小」.
        注意, 在本题中, 线段之间不会出现部分重叠 (可能会嵌套). 因此可以用 #贪心 来放置. 具体为「右端点, 线段长度」 #双关键字排序. 见官答.
        除了贪心: 更为直觉的思路是, 在发生嵌套的线段中去除较长的那些线段即可, 但不如贪心直接排序好实现.
[官答](https://leetcode.cn/problems/maximum-number-of-non-overlapping-substrings/solution/zui-duo-de-bu-zhong-die-zi-zi-fu-chuan-by-leetcode/)
"""
    def maxNumOfSubstrings_wa(self, ss: str):
        # 思路0: 理解错题目为「给定一个字符串s, 要求返回一组不重叠子串, 其中每一个子串都包含s中全部的某一字符」. 也即 "abab" -> ["aba"].
        n = len(ss)
        starts = defaultdict(lambda: inf)
        ends = defaultdict(lambda: -inf)
        for i,ch in enumerate(ss):
            starts[ch] = min(starts[ch], i)
            ends[ch] = max(ends[ch], i)
        ranges = [(ch,starts[ch],ends[ch]) for ch in starts]
        ranges.sort(key=lambda x: x[2])
        l = len(ranges)
        # 
        f = [[[0, 0]]*(l+1) for _ in range(n+1)]
        cache = defaultdict(set)
        for idx in range(n):
            for i,(ch,s,e) in enumerate(ranges):
                f[idx+1][i+1] = f[idx+1][i]
                cache[(idx+1, i+1)] = cache[(idx+1, i)]
                if e<=idx:
                    num, totollen = f[s][i][0] + 1, f[s][i][1] + e-s+1
                    if num > f[idx+1][i][0] or (num == f[idx+1][i][0] and totollen < f[idx+1][i][1]):
                        f[idx+1][i+1] = [num, totollen]
                        cache[(idx+1, i+1)] = cache[(s, i)]
                        cache[(idx+1, i+1)].add(ch)
        # return f[-1][-1]
        ans = []
        for ch in cache[(n, l)]:
            ans.append(ss[starts[ch]:ends[ch]+1])
        return ans

    def maxNumOfSubstrings(self, ss: str):
        # 思路1: 拓展成符合要求的子串, 然后 #贪心
        chs = set(ss)
        starts, ends = defaultdict(lambda: inf), defaultdict(lambda: -inf)
        for i,ch in enumerate(ss):
            starts[ch] = min(starts[ch], i); ends[ch] = max(ends[ch], i)
        
        def extend(ch):
            # 拓展包含i的子串, 返回 [l,r] 区间是符合题意的
            ava = chs.copy(); ava.remove(ch)
            l,r = starts[ch], ends[ch]
            j = l
            while j<=r:
                ch = ss[j]
                if ch in ava:
                    ava.remove(ch)
                    if starts[ch] < l:
                        l = starts[ch]
                        j = starts[ch]
                    r = max(ends[ch], r)
                j += 1
            return [l,r]
        # 对于每一个字符进行拓展
        ranges = [extend(ch) for ch in starts]
        # 双关键字排序
        ranges.sort(key = lambda x: (x[1], x[1]-x[0]))
        
        # 贪心选择
        last = -1; ans = []
        for l,r in ranges:
            if last==-1 or l>last:
                ans.append(ss[l:r+1]); last = r
        return ans
    
    def maxNumOfSubstrings(self, s: str) -> List[str]:
        # 思路1 official
        class Seg:
            def __init__(self, left=-1, right=-1):
                self.left = left
                self.right = right
            # 定义比较, 双关键字
            def __lt__(self, rhs):
                return self.left > rhs.left if self.right == rhs.right else self.right < rhs.right

        seg = [Seg() for _ in range(26)]
        # 预处理左右端点
        for i in range(len(s)):
            charIdx = ord(s[i]) - ord('a')
            if seg[charIdx].left == -1:
                seg[charIdx].left = seg[charIdx].right = i
            else:
                seg[charIdx].right = i

        for i in range(26):
            if seg[i].left != -1:
                j = seg[i].left
                while j <= seg[i].right:
                    charIdx = ord(s[j]) - ord('a')
                    if seg[i].left <= seg[charIdx].left and seg[charIdx].right <= seg[i].right:
                        pass
                    else:
                        seg[i].left = min(seg[i].left, seg[charIdx].left)
                        seg[i].right = max(seg[i].right, seg[charIdx].right)
                        j = seg[i].left
                    j += 1

        # 贪心选取
        seg.sort()
        ans = list()
        end = -1
        for segment in seg:
            left, right = segment.left, segment.right
            if left == -1:
                continue
            if end == -1 or left > end:
                end = right
                ans.append(s[left:right+1])
        
        return ans


    """ 1521. 找到最接近目标值的函数值 #hard #math #位运算 #题型
给定一个arr, 要求其子数组中, 元素 and 的结果与target的最小差值.
限制: 数组长度 1e5; 元素大小 C=1e6
提示: 对于 [l...r] 的and结果, 假设我们固定r, 则有结论: 1) 随着l的减小, and的结果变小; 2) 因为要求是连续的区间, 因此以r结尾的and结果数量有限, 最多为 logC 个.
思路1: 维护每一个右端点可能得到的and结果集合
    根据提示, 可以顺序遍历上述右端点r, 用一个集合 valid 记录所有可能的and结果. 注意这一set的大小较小.
    转移: 对于r+1, 其和可能的l匹配的and结果只有 `{ v&num for v in valid, num }`
    复杂度: `O(n logC)`
    see [official](https://leetcode.cn/problems/find-a-value-of-a-mysterious-function-closest-to-target/solution/zhao-dao-zui-jie-jin-mu-biao-zhi-de-han-shu-zhi-by/)
"""
    def closestToTarget(self, arr: List[int], target: int) -> int:
        ans = inf
        valid = set()
        for num in arr:
            valid = {v&num for v in valid} | {num}
            ans = min(ans, min(abs(target-v) for v in valid))
        return ans

sol = Solution()
result = [
    # sol.countSubTrees(n = 5, edges = [[0,1],[0,2],[1,3],[0,4]], labels = "aabab"),
    # sol.maxNumOfSubstrings_wa("adefaddaccc"),
    # sol.maxNumOfSubstrings_wa("abbaccd"),
    # sol.maxNumOfSubstrings("adefaddaccc"),
    # sol.maxNumOfSubstrings("abbaccd"),
    sol.maxNumOfSubstrings("abab"),
    # sol.closestToTarget(arr = [9,12,3,7,15], target = 5),
]
for r in result:
    print(r)
