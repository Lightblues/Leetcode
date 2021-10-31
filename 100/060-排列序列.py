"""
给出集合 [1,2,3,...,n]，其所有元素共有 n! 种排列。

按大小顺序列出所有排列情况，并一一标记，当 n = 3 时, 所有排列如下：

"123"
"132"
"213"
"231"
"312"
"321"
给定 n 和 k，返回第 k 个排列。

输入：n = 3, k = 3
输出："213"

输入：n = 4, k = 9
输出："2314"

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/permutation-sequence
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
class Solution:
    def getPermutation(self, n: int, k: int) -> str:
        from math import perm

        n_list = list(range(1, n+1))
        res = []
        # if k==perm(n):
        #     return ''.join([str(i) for i in n_list])[::-1]
        while n_list:
            if k == perm(len(n_list)):
                res += n_list[::-1]
                break
            elif k == 1:
                res += n_list
                break
            nums = perm(len(n_list) - 1)
            q, k = divmod(k, nums)
            if k==0:
                res.append(n_list.pop(q-1))
            else:
                res.append(n_list.pop(q))
        return ''.join([str(i) for i in res])
n = 4; k = 9
print(Solution().getPermutation(3,2))


