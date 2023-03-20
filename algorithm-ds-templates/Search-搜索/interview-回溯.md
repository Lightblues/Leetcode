
# 回溯 backtracking

区别于递归问题, 当我们遇到for循环比较复杂不知道怎么写的时候, 一般会用到 **回溯**.
回溯可以写成 `dfs(x)` 的形式, 对当前状态x进行搜索, 然后可以调用自身从而进行搜索. 
    递归/回溯函数. 重点包含 1] 终止条件; 2] 递归搜索, 也即调用 dfs(i) 自己
    在回溯函数中, 一般需要记录搜索的状态 (下面的path变量). 

```python
    """ 0017. 电话号码的字母组合 #medium 给定一个数字按键 (映射), 对于一串按下的数字, 问它可能对应的字符串有哪些? 限制: n<=4
思路1: #回溯
    注意, 区别于一般的递归问题, 这里的递归深度 (for的数量) 是不确定的, 需要用 回溯; 确定边界条件
    复杂度: O(n 4^n). 每次转移最多生成4个节点; 递归过程生成答案的复杂度为 O(n)
"""
    def letterCombinations(self, digits: str) -> List[str]:
        MAPPING = ("", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz")
        
        n = len(digits)
        # 边界
        if n == 0: return []
        ans = []
        path = [''] * n     # 记录当前路径
        def dfs(i: int) -> None:
            """ 递归/回溯函数. 重点包含 1] 终止条件; 2] 递归搜索, 也即调用 dfs(i) 自己 """
            if i == n:
                # 回溯终止条件! 将答案记录下来
                ans.append(''.join(path))
                return
            # 递归往下进行搜索
            for c in MAPPING[int(digits[i])]:
                path[i] = c     # 记录当前的路径
                dfs(i + 1)
                # 一般回溯还需要「恢复现场」, 不过这题中没有必要写
                # path[i] = ''
        # 开始进行搜索/递归
        dfs(0)
        return ans
```


子集回溯
枚举每个位置的可能情况

- 0017. 电话号码的字母组合 #medium 给定一个数字按键 (映射), 对于一串按下的数字, 问它可能对应的字符串有哪些?
- 0078. 子集 #medium #题型 给定一组不含重复元素的整数数组 nums, 返回该数组所有可能的子集 (幂集). 注意避免重复. 限制: n<=10 
    1.1 输入的视角（选或不选） dfs(i) 中考虑第i个元素是否加入答案
    1.2 答案的视角（选哪个数） dfs(i) 中固定 [0...i-1] 中所选, 枚举下一个是 i,i+1...
- 0131. 分割回文串 #medium 将一个字符串分割成一些回文串, 返回所有的可能.
- 0784. 字母大小写全排列 #medium 对于一个字符串中的所有英文字母, 组合其大小写可以有多种结果, 返回所有可能的结果. 限制: 字符串长度 n 12

排列

- 0046. 全排列 <https://leetcode.cn/problems/permutations/solutions/2079585/hui-su-bu-hui-xie-tao-lu-zai-ci-jing-que-6hrh/>
- 0051. N 皇后 <https://leetcode.cn/problems/n-queens/solutions/2079586/hui-su-tao-lu-miao-sha-nhuang-hou-shi-pi-mljv/>
- 0052. N皇后 II #hard 相较于 0052, 只需要返回解的数量

组合

- 0077. 组合 #medium 返回 [1, n] 中选k的所有组合 限制: n 20
    思路: 相较于子集回溯, 组合需要限定搜索深度. 复杂度: 节点数量为 C(n,k), 每个叶子为 O(k), 因此总体复杂度为 O(C(n,k)*k)
- 0216. 组合总和 #medium 返回 [1, 9] 中选k的所有组合, 使得和为 n 限制: k 9; n 60
    关联 「0077. 组合」. 不同之处在于, 需要进行一定的剪枝/条件判断. 
- 0022. 括号生成 #medium 需要生成长度为 2n的括号序列, 找到所有合法的. 

