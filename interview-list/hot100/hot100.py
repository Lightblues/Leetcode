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
[🔥 LeetCode 热题 HOT 100](https://leetcode.cn/problem-list/2cktkvj/)
Easonsi @2023 """

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    
    """ 0394. 字符串解码 #medium #细节 对于 10[a2[bc]] 解析成 abcbcabcbc... 的形式
[official](https://leetcode.cn/problems/decode-string/solution/zi-fu-chuan-jie-ma-by-leetcode-solution/)
"""
    def decodeString(self, s: str) -> str:
        st = []
        ans = ""
        for ch in s:
            if ch==']':
                tmp = []
                while st[-1] != '[': tmp.append(st.pop())
                st.pop()
                times = []
                while st and st[-1].isdigit(): times.append(st.pop())
                times = int("".join(times[::-1]))
                new = tmp * times
                if st:
                    # for c in new: st.append(c)
                    st += new[::-1]
                else:
                    ans += "".join(new[::-1])
                # st += list(new)
            else:
                if st or ch.isdigit():
                    st.append(ch)
                else:
                    ans += ch
        return ans
    
    """ 0406. 根据身高重建队列 #medium #排序 对于一个 (h,k), h 表示身高, k 表示前面有 k 个人身高大于等于 h, 求重建队列 
限制: n 2e3
思路1: #排序, 我们考虑从高到低排序, 这样的话, 对于当前的第i个人, 已经安排好位置的人都 >=它, 只需要插入位置k即可. 
    考虑相同身高的情况, 因此实际上是按照 (-h, k) 排序
    这样, 对于相同身高的, 先将k较小的安排后, 再插入k值更大的元素
    复杂度: 插入 O(n^2)
细节: 注意, Python 的 .insert 操作是比较robust的, 例如 a的长度为0, 允许 a.insert(2,xx) 插入最后
[here](https://leetcode.cn/problems/queue-reconstruction-by-height/solution/xian-pai-xu-zai-cha-dui-dong-hua-yan-shi-suan-fa-g/)
    """
    def reconstructQueue(self, people: List[List[int]]) -> List[List[int]]:
        people.sort(key=lambda x: (-x[0], x[1]))
        ans = []
        for h,k in people:
            # Python的 insert很棒~
            ans.insert(k, [h,k])
        return ans
    
    """ 0437. 路径总和 III #medium 求从上往下的路径和为x的数量
思路: 递归
    """
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        if not root: return 0
        ans = 0
        def dfs(root):
            nonlocal ans
            s = Counter()
            for c in root.left, root.right:
                s = s + dfs(c) if c else s
            ret = Counter()
            for k,v in s.items():
                ret[k+root.val] += v
            ret[root.val] += 1
            ans += ret[targetSum]
            return ret
        dfs(root)
        return ans
    
    """ 0438. 找到字符串中所有字母异位词 #medium 
思路1: #滑窗, 为了优化比较是否相同的代价, 可以用一个diff记录相差的绝对数量
    """
    def findAnagrams(self, s: str, p: str) -> List[int]:
        n = len(s); m = len(p)
        ref = Counter(p)
        now = Counter(s[:m])
        diff = sum(abs(ref[k]-now[k]) for k in ref+now)
        ans = []
        if diff==0: ans.append(0)
        for i in range(m, n):
            c = s[i]
            if ref[c] > now[c]: diff-=1
            else: diff+=1
            now[c] += 1
            c2 = s[i-m]
            if ref[c2] < now[c2]: diff-=1
            else: diff += 1
            now[c2] -= 1
            # ans += int(diff==0)
            if diff==0: ans.append(i-m+1)
        return ans

    
sol = Solution()
result = [
    # sol.decodeString("3[z]2[2[y]pq4[2[jk]e1[f]]]ef"),
    # sol.reconstructQueue(people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]),
    sol.findAnagrams(s = "cbaebabacd", p = "abc"),
    
]
for r in result:
    print(r)
