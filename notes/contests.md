## 周赛笔记

### 268

- 2078. 两栋颜色不同且距离最远的房子
- 2079. 给植物浇水
  - 模拟法
- 2080. 区间内查询数字的频率 `中`
  - 需求是查询子数组 arr[left...right] 中 value 的 频率; 考虑到查询数量可能较大, 因此设计一个数据结构存储数据分布信息
  - 解法: 用 map 保存数字所出现的位置列表, 从而查询时候可以用**二分查找**.
    - Python 可以直接用 `bisect.bisect` 好方便!
- 2081. k 镜像数字的和 `难`
  - 找到前 n 个, 在 10进制 和k进制下均为回文数的数字, 返回其最大值
  - 注意题目要求, 2 <= k <= 9, 1 <= n <= 30 当k和n均取较大值时会超时(约10**10量级); 因此重点是如何所见搜索空间.
    - 由于是回文数, 因此只需遍历前半部分即可, 注意可生成奇数或偶数长度的, 例如 1234 -> 1234321 或 12344321;
    - 另外, 每次遍历 [1,9], [10,99]... 的数字, 对于j位十进制数, 可分别生成 2j-1, 2j 位十进制数

### 269

- 2089. 找出数组排序后的目标下标
- 2090. 半径为 k 的子数组平均值
- 2091. 从数组中移除最大值和最小值
  - 滑动平均
- 2092. 找出知晓秘密的所有专家 `难`
  - 包括 (x, y, time) 的三元组, 若 x 和 y 中某一个知道了「秘密」, 则会进行传播; 要求最后知道「秘密」的所有人
  - 解法一: **构建图**, 传播
    - 按照时间排序, 难点在于判断同一时间的多人传播关系 —— 简单的方案是构建图
    - 解法的具体实现: 利用 edges 字典记录连接关系, 建立图后, 利用 一个 `deque` 记录所有激活节点, 迭代直至队列空
  - 解法二: **并查集**

### 270

- 2094. 找出 3 位偶数
  - 给你一个整数数组, 找出所有的三位偶数(也即要求首位不为 0), 顺序输出(直接排序即可)
  - 简单题 (也可根据提示的范围知道不复杂) 别想太多, 直接暴力遍历即可; 为了避免重复可以用 set()
- 2095. 删除链表的中间节点 `中`
  - 长度为 n 链表的中间节点是从头数起第 ⌊n / 2⌋ 个节点（下标从 0 开始）
  - 解法一: 快慢指针即可, 可以在最开始加上一个「哨兵」
- 2096. 从二叉树一个节点到另一个节点每一步的方向 `中`
  - 找到二叉树两个节点之间的路径
  - 解法一: 直接 DFS 找到两个点从 root 出发的路径, 除去公共路径即可
- 2097. 合法重新排列数对 `难`
  - 给定 pairs(表示区间), 重新排列要求排列后每个区间首尾数字相同; 核心在于理解「[欧拉通路](https://oi-wiki.org/graph/euler/)」, 将问题转换
  - `Hierholzer 算法`: 首先很容易想到, 若仅为「**半欧拉图**」(即存在两个奇数度数节点), 可以确定开始和结束的数字, 否则为「欧拉图」随便选择初始数字/节点即可.
    - 若随便选择一条边, 则可能走到「死路」, 注意此时剩下的图构成了一个「欧拉图」 —— 可以用DFS探索
    - 因此, 1. 每次选择一条边, 在图上删去这条边; 2. 递归; 3. 记录这条边. 注意这里的边是在遍历之后加入记录的 (也即是逆序的, 最后要再逆序输出), 这样可以保证可能漏过的「欧拉图」在此之前被遍历.
  - 参见 「332. 重新安排行程」「753. 破解保险箱」
  - 332 重新安排行程, `难`
    - 区别在于, 需要返回所有的通路中, 字母排序最小的那一个 —— 也即, 每次应该选择较小的那一个节点
    - [solution](https://leetcode-cn.com/problems/reconstruct-itinerary/solution/zhong-xin-an-pai-xing-cheng-by-leetcode-solution/) 非常清楚
  - 753. 破解保险箱, `难`
    - 密码是 n 位数, 密码的每一位是 k 位序列 0, 1, ..., k-1 中的一个 。要求返回一个最短字符串, 其子字符串包括所有可能的密码.
    - 关键在于将其转化为一个规范的欧拉通路问题: see [here](https://leetcode-cn.com/problems/cracking-the-safe/solution/po-jie-bao-xian-xiang-by-leetcode-solution/) 官方解答有点fancy
    - 解法: 转换为**欧拉通路问题**
      - 简言之, 要求的是 n 长序列, 都可将其看成 n-1长序列加上 0~k-1 的数字. 因此, 可以构建一个图, 节点为所有的 n-1长序列, 其第i个出边就是在最后加上数字i并去除第一位数字, 跳到相应的节点上.
      - 例如, 节点u的第v的出边就跳转到数值为 u*k % (k**(n-1)) + v 的节点上.
      - 可知, 这样构造的图, 每个节点都有 k条出边和入边, 共可代表 $k^{n-1} * k$ 个不同的数字, 正好对应了所有可能的密码.
      - 显然, 这张图是欧拉图, 并且可基于一个欧拉回路对应一个题目所要求的字符串.

### 271

- 2105. 给植物浇水 II
  - 模拟法即可
- 2106. 摘水果 `难`
  - 在一个无限的 x 坐标轴上, 分布一定的水果, 给定 startPos 和可以移动的步数 k, 计算可以拿到的最大数量
  - 题型: 其实就是给定一个累加和, 探索所有可能的范围内的最大值; 问题在于如何在离散存储的数组中找到对应的元素
    - 存储方式: 例如对 `[[2,8],[6,3],[8,6]]` 水果分布而言, 记录位置 `pos=[-Inf, 2,6,8]` 和 累计和 `[0,8,11,17]`
    - **二分查找**. 要注意 **边界情况**, 左边应该是 `bisect.bisect_left`, 而右边是 `bisect.bisect_right`, 注意函数返回的是待插入的 index, 因此最终能采集的水果数量为 `cumsum[rindex-1] - cumsum[lindex-1]`
    - 错误记录: 注意, 先往左边走和先往右边走所能达到的范围是不一样的! 因此两侧的情况都应该考虑到.

### 272

- 2110. 股票平滑下跌阶段的数目
  - 一次遍历即可
- 2111. 使数组 K 递增的最少操作次数 `难`
  - 如果对于每个满足 `k <= i <= n-1` 的下标 i ，都有 `arr[i-k] <= arr[i]` ，那么我们称 arr 是 K 递增 的。
  - 给定一个数组和 k,要求找到使得这个数组 k递增的最小修改次数.
  - 问题可转化为: 寻找一个数组中的最长递增序列, 参见 300 题 [最长上升子序列](https://leetcode-cn.com/problems/longest-increasing-subsequence/solution/zui-chang-shang-sheng-zi-xu-lie-by-leetcode-soluti/)
    - 思路 1: DP, 定义 `dp[i]` 为 第 i 个数字结尾的最长上升子序列的长度, 注意 第 i 个元素必须被选中; 递推公式 `dp[i] = max(dp[j]) + 1`, 其中的 j 要求 `nums[j]<=nums[i]`
      - 时间复杂度 $O(n^2)$
    - 方法二：贪心 + 二分查找
      - 维护一个数组 `d[i]` ，表示**长度为 i 的最长上升子序列的末尾元素的最小值**, 用 len 记录目前最长上升子序列的长度. 注意到数组 d 是单调递增的
      - 我们依次遍历数组 nums 中的每个元素，并更新数组 d 和 len 的值。如果 `nums[i]>d[len]` 则更新 `len = len + 1`，否则在 `d[1…len]`中找满足 `d[i−1]<nums[j]<d[i]` 的下标 i，并更新 `d[i]=nums[j]`。
      - 由于是递增数列, 可以用二分搜索
      - 时间复杂度 $O(n log(n))$

### 273

- 2120. 执行所有后缀指令
  - 模拟机器人动作即可
- 2121. 相同元素的间隔之和 `中`
  - 给定一个数组, 计算其中相同元素所在的 index 之差, 返回所有这些距离的和
  - 用一个 defaultdict(list) 记录各个元素出现的位置.
  - 问题转化为对于一个数字出现的位置, 计算各个位置的 dist 和.
    - 注意数据量, 直接暴力遍历复杂度为 $O(n^2)$ 会超时
    - 思路1: 观察相邻两个元素相差的(子距离数量), 可得递推公式 `dp[i+1] = dp[i] -(n-2i-2) * (arr[i-1]-arr[i])`
    - 思路2: 计算 cumsum, 则 i 处的距离和为 `(cumsum[-1]-cumsum[i] - arr[i]*(n-1-i)) + (cumsum[i]-cumsum[0] - arr[0]*i)`
- 2122. 还原原数组 `难`
  - 就是对于一个数组 arr, 用一个正整数 k, 分别生成两个数组, `lower[i] = arr[i] - k, higher[i] = arr[i] + k`. 要求给定这两个数组的混合, 还原 arr
  - 注意看约束条件, 数组大小最多为 `1000` 所以暴力搜索即可, 题目只是比较繁琐
    - sort, 得到可能的 k
    - 用 `indexRecord` 记录每个数字对应的位置
    - 关键在判断一个 k 是否满足条件. 这里用了一个 `used` 记录每个所对应的元素所在位置, 遍历 nums 后, 若 `sum(used) == n` 则说明 k 满足条件
  - see [here](https://leetcode-cn.com/problems/recover-the-original-array/solution/huan-yuan-yuan-shu-zu-by-leetcode-soluti-nizi/)

### 274

- 5970. 参加会议的最多员工数 `难`
  - 每个人只有一个喜欢的人, 要求安排坐圆桌, 每个人左右要有他喜欢的人, 最大的可安排人数
  - 比较容易想到, 问题主要转化为求这样的有向图上的最大环,
    - 特殊情况是两个互相喜欢的人, 他们相互满足了要求, 因此左右可以有一条「喜欢人的链」, 并且左右的人都是满足的; 因此, 这种大小为 2 的环一个桌上可以安排多个
    - 参见 [这个题解](https://leetcode-cn.com/problems/maximum-employees-to-be-invited-to-a-meeting/solution/nei-xiang-ji-huan-shu-tuo-bu-pai-xu-fen-c1i1b/), 这种图叫做 **内向基环树 (pseudotree)**
  - 所以核心问题在于如何在 pseudotree 中找环, 比赛中的尝试没有想到如何「**剪枝**」超时了; 实际上, 可以通过一次 **拓扑排序** 剪掉所有的分支 (最后留在图上的点的度数最大为 1)
    - 具体实现上, 维护一个入度为 0 的队列, 对其喜欢的人的入度 -1, 如果减到了 0 则继续加入队列;
    - 这样, **拓扑排序后最终剩下的点都是成环的**(入度为 1).

### 275

- 5976. 检查是否每一行每一列都包含全部整数
- 5977. 最少交换次数来组合所有的 1 II
  - 滑动平均
- 5978. 统计追加字母可以获得的单词数
  - 注意审题
- 5979. 全部开花的最早一天
  - 两个数组, 分别是 播种 和 开花 所需的时间, 要求使得所有花都开放的最小时间
  - 题目给了干扰: 将一种花分成两次播种没有意义, 因为两者总的播种时间是一样的, 因此在过程中两种花都不会提早开花.
  - 于是可以化简为, 给依次播种的花进行排序
  - 可知, 总的播种时间是一定的, 目标在于减少开花所需时间. 因此每次根据开花所需时间排序, 选择需要最长时间的那种即可.

### 276

- 5980. 将字符串拆分为若干长度为 k 的组
- 5194. 得到目标值的最少行动次数
  - 给定一个目标数, 从 1 开始 +1, *2 两种操作, 限定了倍乘的次数 maxDoubles
  - 贪心, 从 target 往下 /2
- 5982. 解决智力问题
  - 给定一系列的题目, questions[i] = [pointsi, brainpoweri], 你选择做某一题的代价是只能跳过后面 brainpower 题
  - DP, 从后往前, 记录从该位置往后的最大解, 递推公式 `dp[i] = max([dp[i+1], point+dp[i+skip+1]])`
- 5983. 同时运行 N 台电脑的最长时间
  - 给定一组电池 batteries, 每个电池可以给一台电脑运行一定的时间. 可以把一个电池替换给不同的电脑, 要求让所有电脑同时运行的最长时间
  - 这里的限制条件为电量最大的 n 个电池, 小的电池看作对它们的补充.
  - 注意到: 一个电池的电量可以以**任意的比例**分到若干块电池上.
  - 因此, 可以将最大的 n 个电池看成一个「阶梯」, 其余的小电池理解为在这个池子里注水, 求高度

### 277

- 2148. 元素计数
- 2149. 按符号重排数组
- 2150. 找出数组中的所有孤独数字
- 2151. 基于陈述统计最多好人数 `hard`
  - 两种角色: 好人只说真话, 坏人可能真也可能假
  - 给定一个矩阵表示每个人的陈述 (0,1,2 分别表示 坏人, 好人, 未判断), 要求计算好人最多可能数量
  - 注意到, **此题中坏人的陈述毫无信息量**!
  - 方法一：使用状态压缩枚举所有可能的情况
    - [here](https://leetcode-cn.com/problems/maximum-good-people-based-on-statements/solution/ji-yu-chen-shu-tong-ji-zui-duo-hao-ren-s-lfn9/)
    - 用一个长度为 n 的二进制数 mask 表示好人坏人情况, 针对 mask 所表示的好人坏人分布, 判断是否合法
      - 冲突的情况只会出现在好人 i 的陈述中 (mask[i]=1)
      - 当 `s[i][j]=0 and mask[j]=1`, 或 `s[i][j]=1 and mask[j]=0` 时冲突
    - 实现一个 `check(mask)` 函数判断是否冲突
    - check 复杂度最大为 n^2, 枚举复杂度为 2^n, 因此总体复杂度为 `n^2 2^n`, 这里用位运算所以比较快?
  - 方法二: 回溯
    - 暴力枚举每个人是好人或坏人, 注意剪枝!!

### 278

- 2154. 将找到的值乘以 2
- 2155. 分组得分最高的所有下标
- 5994. 查找给定哈希值的子串
  - 定义一个字符串的哈希值 `hash(s, p, m) = (val(s[0]) * p0 + val(s[1]) * p1 + ... + val(s[k-1]) * pk-1) mod m`
  - 给你一个字符串 s 和整数 power，modulo，k 和 hashValue 。请你返回 s 中 第一个 长度为 `k` 的 子串 sub ，满足 `hash(sub, power, modulo) == hashValue` 。
  - 字符串长度为 e4, 如果暴力遍历, 当所要求的 k 数量级接近是复杂度是 e8, 会超时
  - 方法一: **滑动平均**, O(n)
    - 给出的哈希计算函数是一个等比求和数列，两者可以通过减去首元素，除以power再加上新元素的power的k-1次方计算。
    - 但是 **除法不满足取余的恒等性**。因此需要倒序，减去当前的值，乘以power再加上新元素的值。(乘法满足取余恒等)
    - 参见 [here](https://leetcode-cn.com/problems/find-substring-with-given-hash-value/solution/cha-zhao-gei-ding-ha-xi-zhi-de-zi-chuan-fi8jd/)
- 2157. 字符串分组 `hard`
  - 每个字符串包括了一组不相同的字符 (比如 cde), 定义两个字符串「相连」: 其一可以通过 添加/删除/替换(替换成相同字符也可, 即包括相同字符集合的两字符串相连) 一个字符得到另一个字符串。
  - 定义组: 如果一个字符串与该组中的任一字符串相连，则这个字符串属于该组。
  - 给一组字符串, 计算有多少个不同的组, 以及最大组包括的字符串数量。
  - 方法一：状态压缩 + 广度优先搜索
    - 显然是求连通分量的数量, 问题在于如何构建图? 如果是两两计算复杂度为 O(n^2) 超时;
    - 像这类题, 可以从每一个节点出发, 构造其所有可能相连的边, 例如这里就是按照「相连」的定义, 增删或者替换所有可能的字符, 这样复杂度为 O(nD^2), 其中 D 为字符字典大小
    - 具体而言, 为了进行图遍历, 用一个 used 集合记录所有遍历过的节点, queue 来维护当前进行BFS, 对于所有的节点进行遍历.
    - 状态压缩: 如何表示一个(小写字母)字符集合? 01编码转化为数字以进行压缩. 这样的好处还有方便表示相连边, 参见 `get_adjacent`
    - 参见 [here](https://leetcode-cn.com/problems/groups-of-strings/solution/zi-fu-chuan-fen-zu-by-leetcode-solution-a8dr/)

### 279

- 6000. 对奇偶下标分别排序
- 6001. 重排数字的最小值
  - 给一个数字 (可能为负数), 重拍求最小值
- 6002. 设计位集 `medium`
  - 能够快速实现 fix(设置某一位为1), unfix, flip(翻转每一位), add, one(至少一个非零), count(非零位数量) 操作
  - 尝试直接用列表存储, 超时了, 可能是 flip, add, one, count 复杂度较高
  - 优化为 位存储+一个变量intcount存储非零位数量, 从而优化时间复杂度; 可以重新看看**位运算**使用技巧
- 6003. 移除所有载有违禁货物车厢所需的最少时间
  - 一个 01 序列表示违禁物品, 前后移除一辆火车代价位 1, 移除中间的一辆代价为2, 求移除所有违禁货车最小代价
  - 思路一: 从左边和右边非别累加计算单面的最小代价, 加起来求最小 (其实就是在不同的点分割).
    - 注意 更新公式(DP): 当 `s[i+1]=='1'` 时 `dp[i+1] = min(dp[i]+2, i+1)`, 因为若从左边全部移除的代价是 i+1, 从中间取走的代价是 +2
    - 为了计算的方便在头部加一个 [0]; 注意到在点 i 处分割的总代价为 `dp1[i]+dp2[i+1]`, 正好错位加和. 参见 [here](https://leetcode-cn.com/problems/minimum-time-to-remove-all-cars-containing-illegal-goods/solution/qian-hou-zhui-fen-jie-dp-by-endlesscheng-6u1b/)

### 280

- 6004. 得到 0 的操作数
- 6005. 使数组变成交替数组的最少操作数
  - `[2,1,2,1,2,1,2]` 的形式, 要求奇数和偶数位置的数字不同
  - 分别对于 nums[0::2] 和 nums[1::2] 计数, 注意边界情况 (`len(collections.Counter(nums[0::2])) == 1`)
- 6006. 拿出最少数目的魔法豆
  - 给定一组袋子, 要么拿空, 要求最后剩下来的非空袋子里的豆子数量相同
  - 排序, 想像成一个阶梯, 最后留下来的就是一个矩形; 转化为遍历求矩形最大面积
- 6007. 数组的最大与和
  - 有编号为 1,2,...,numSlot的篮子, 要求把一个长度为 n 的数组放入篮子中, 每个篮子最多放两个数字!
  - 定义放置的分数为, 数字和篮子编号与 `nums[i] & (assign[i]+1)`, 其中 assign 表示 第 i 个数字放在第 assign[i] 个篮子中
  - 方式一: 暴力回溯
    - 用一个 records 数组保存每个篮子中球的数量
    - 回溯函数 `dfs(idx, curSum, curMax)`, 遍历 idx 放置每一颗球

## 双周赛

### D68

- 2114. 句子中的最多单词数
- 2115. 从给定原材料中找到所有可以做出的菜
  - 给定一个菜单, 每道菜的成分可能包括食材或其他的菜品, 要求在一定的初始食材下能够得到的所有菜品
  - 思路一: 本题数据量比较小, 可以暴力遍历. 用一个 flag 记录一次遍历是否有新的菜品(食材) 生成, 当没有时即结束
  - 思路二: 依赖关系构成图, 显然可以用 `拓扑排序` 解决, see [here](https://leetcode-cn.com/problems/find-all-possible-recipes-from-given-supplies/solution/cong-gei-ding-yuan-cai-liao-zhong-zhao-d-d02i/)
- 2116. 判断一个括号字符串是否有效 `中`
  - 给定一个在某些位上固定的字符串 (例如 `s = "))()))", locked = "010100"`), 判断能够通过修改其他自由位使其成为合法的括号序列
  - 思路一: 关注 lock 部分 (剩下偶数个自由位一定可以匹配)
    - 先尝试匹配 lock 部分的字符串, 记录未成功匹配的位置 (三种情况, 最后剩下 `((`, `))` or `))((`; 和 空白符号的位置;
    - 利用 space 字符串来匹配剩下的左右括号 leftStack, rightStack
    - 原本分了上面三种情况讨论, 实际上可以合并: 用 space 最前面的部分匹配右括号, 最后面的部分匹配左括号, `len(spaces)>=len(leftStack)+len(rightStack) and all([i>j for i,j in zip(spaces[-len(leftStack):], leftStack)]) and all([i<j for i,j in zip(spaces[:len(rightStack)], rightStack)])`
  - 方法一：数学, see [here](https://leetcode-cn.com/problems/check-if-a-parentheses-string-can-be-valid/solution/pan-duan-yi-ge-gua-hao-zi-fu-chuan-shi-f-0s47/)
    - 定义了有效字符串「分数」的概念, 然后通过: 维护 1. 前缀 s[0..i] 可以达到的最大分数；2. 前缀 s[0..i] 「可以达到的最小分数」及「作为有效前缀所需的最小分数」两者的较大值. 这两个数组来进行判断.
- 2117. 一个区间内所有数乘积的缩写 `难`
  - 放弃了
  - 参见 [思路详解+详细讨论一下精度问题](https://leetcode-cn.com/problems/abbreviating-the-product-of-a-range/solution/fen-bie-ji-suan-qian-5wei-he-hou-5wei-si-dc9x/), Python 超时了. 另外 [here](https://leetcode-cn.com/problems/abbreviating-the-product-of-a-range/solution/yi-ge-shu-ju-tuan-mie-jue-da-bu-fen-dai-234yd/) 做了更多的分析