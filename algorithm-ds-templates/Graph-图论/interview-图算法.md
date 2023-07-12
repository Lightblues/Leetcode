
[labuladong](https://labuladong.gitee.io/algo/di-yi-zhan-da78c/shou-ba-sh-03a72/)
DFS 题目列表 [潮汐朝夕](https://chengzhaoxi.xyz/18482.html)


BFS, DFS

- 0104. 二叉树的最大深度 #easy
- 0200. 岛屿数量 #medium
- 0111. 二叉树的最小深度 #easy
- 0100. 相同的树 #easy
- 1254. 统计封闭岛屿的数目 #medium 
- 0329. 矩阵中的最长递增路径 #hard
- 2415. 反转二叉树的奇数层 #medium

最短路

- 1514. 概率最大的路径 #medium
- 1976. 到达目的地的方案数 #medium

拓扑排序

- 0207. 课程表 #medium 一组课程有依赖关系, 问是否能完成
    思路1: 基本的 #拓扑排序 模版题
- 2050. 并行课程 III #hard #题型
    课程之间存在DAG依赖关系, 每个课程修习需要一定的月份, 前序依赖满足的情况下, 不同课程可以同时修习. 求完成所有可能的最小时间.
    在遍历的过程中记录每个节点的timeLimit, 这样, 遍历每一条边的时候, 可以更新 `timeLimit[v]` 为 max(timeLimit[v], timeLimie[u]+time[v])`
- 2392. 给定条件下构造矩阵 #hard #题型
    给定一个k, 要求构造 k*k 的矩阵, 填充 1~k 共k个数字, 其他位置填0. 要求满足行/列约束. 约束的形式是, 给定一组 (i,j), 要求数字i所在行应该在j所在行的上面. 限制: k 400, 约束数量 n 1e4
    思路1: 实际上就是一个 #拓扑排序. 分解行列的约束

二叉树
下面整理了一些二叉搜索树的题目, 代码上看懂了的话二叉树应该没啥问题

- 0098. 验证二叉搜索树 <https://leetcode.cn/problems/validate-binary-search-tree/solutions/2020306/qian-xu-zhong-xu-hou-xu-san-chong-fang-f-yxvh/>
- 0230. 二叉搜索树中第K小的元素 <https://leetcode.cn/problems/kth-smallest-element-in-a-bst/>
- 0501. 二叉搜索树中的众数 <https://leetcode.cn/problems/find-mode-in-binary-search-tree/>
- 0530. 二叉搜索树的最小绝对差 <https://leetcode.cn/problems/minimum-absolute-difference-in-bst/>
- 0700. 二叉搜索树中的搜索 <https://leetcode.cn/problems/search-in-a-binary-search-tree/>

