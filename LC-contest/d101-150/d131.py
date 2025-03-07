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
https://leetcode.cn/contest/biweekly-contest-131

T4: 看上去很经典的题目, TODO #线段树
Easonsi @2025 """
class Solution:
    """ 3158. 求出出现两次数字的 XOR 值 """
    def duplicateNumbersXOR(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        ans = 0
        for k, v in cnt.items():
            if v == 2:
                ans ^= k
        return ans

    """ 3159. 查询数组中元素的出现位置 """
    def occurrencesOfElement(self, nums: List[int], queries: List[int], x: int) -> List[int]:
        cnt2idx = {}
        for i,xx in enumerate(nums):
            if xx==x:
                cnt2idx[len(cnt2idx) + 1] = i
        return [cnt2idx[k] if k in cnt2idx else -1 for k in queries]
        
    """ 3160. 所有球里面不同颜色的数目 """
    def queryResults(self, limit: int, queries: List[List[int]]) -> List[int]:
        idx2color = {}
        color2cnt = defaultdict(int)
        ans = []
        for x,y in queries:
            if x in idx2color:
                color2cnt[idx2color[x]] -= 1
                if color2cnt[idx2color[x]]==0:
                    color2cnt.pop(idx2color[x])
            idx2color[x] = y
            color2cnt[y] += 1
            ans.append(len(color2cnt))
        return ans
        
    """ 3161. 物块放置查询 #medium 对于 [0,inf) 的数轴, 有两种操作: 1) 在位置x放一个障碍物; 2) 在 [0,x] 范围内检查是否可以放置一个长sz的物体. 返回每次操作2的结果. 
限制: q 1.5e5; x 5e4
ling: 
    方法一：正序回答询问+有序集合+线段树
    方法二：倒序回答询问+有序集合+树状数组
    方法三：倒序回答询问+并查集+树状数组
 """
    def getResults(self, queries: List[List[int]]) -> List[bool]:
        pass


sol = Solution()
result = [
    # sol.duplicateNumbersXOR(nums = [1,2,1,3]),
    # sol.occurrencesOfElement(nums = [1,3,1,7], queries = [1,3,2,4], x = 1),
    sol.queryResults(limit = 4, queries = [[0,1],[1,2],[2,2],[3,4],[4,5]]),

]
for r in result:
    print(r)
