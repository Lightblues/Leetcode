
[labuladong](https://labuladong.gitee.io/algo/di-yi-zhan-da78c/shou-ba-sh-03a72/)


BFS, DFS

拓扑排序
0207. 课程表 #medium 一组课程有依赖关系, 问是否能完成
    思路1: 基本的 #拓扑排序 模版题
2050. 并行课程 III #hard #题型
    课程之间存在DAG依赖关系, 每个课程修习需要一定的月份, 前序依赖满足的情况下, 不同课程可以同时修习. 求完成所有可能的最小时间.
    在遍历的过程中记录每个节点的timeLimit, 这样, 遍历每一条边的时候, 可以更新 `timeLimit[v]` 为 max(timeLimit[v], timeLimie[u]+time[v])`
2392. 给定条件下构造矩阵 #hard #题型
    给定一个k, 要求构造 k*k 的矩阵, 填充 1~k 共k个数字, 其他位置填0. 要求满足行/列约束. 约束的形式是, 给定一组 (i,j), 要求数字i所在行应该在j所在行的上面. 限制: k 400, 约束数量 n 1e4
    思路1: 实际上就是一个 #拓扑排序. 分解行列的约束

