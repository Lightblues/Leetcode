

类型1: 同向交替移动的两个变量 (固定长度)
0643. 子数组最大平均数 I #easy
1052. 爱生气的书店老板 #medium

类型2: 不定长度的滑动窗口
0076. 最小覆盖子串 #hard #题型
    给定字符串s和t, 要求s中长度最小的包含t中所有元素的子串. 限制: 长度 1e5
2062. 统计字符串中的元音子字符串 #easy #题型
    要求统计连续子序列的数量. 条件为: 1) 所有元素为元音字符 2) 包含所有aeiou五个元素.
    思路1: #双指针. 在满足条件的情况下尽量移动左边界.

类型3: 计数问题
0340. 至多包含 K 个不同字符的最长子串 #medium #题型 给定一个字符串, 要求找到拥有最多k个不同字符的子串的最大长度
    关联: 「159. 至多包含两个不同字符的最长子串」 #medium
0795. 区间子数组个数 #medium 求数组中, 最大元素在 [l,r] 范围内的子数组数量
    思路2: #分解. 考虑子问题「最大元素小于等于x的子数组数量」
0992. K 个不同整数的子数组 #hard #题型
    对于一个数字, 给定数字k, 统计所有子数组中, 「刚好包含k个不同数字」的子数组数量. 限制: 2e4
    思路1: #滑动窗口. 维护「两个窗口」, 从而实现区间的计数.
    思路2: 问题 #转化 为「求最多包含k个不同数字的子数组数量」, 再减去「最多包含k-1个不同数字的子数组数量」


类型4: 使用数据结构维护窗口性质
1438. 绝对差不超过限制的最长连续子数组 #medium #题型 找最长的子数组, 其中的任意两元素绝对差不超过limit 限制: 1e5
    思路1: #有序集合 暴力 复杂度 O(n logn)
    思路2: 本质上就是维护 #滑动窗口 范围内的最大值和最小值! 因此可以用 #单调队列 分别维护递增和递减的序列. 复杂度 O(n)
    关联: 0239. 滑动窗口最大值

