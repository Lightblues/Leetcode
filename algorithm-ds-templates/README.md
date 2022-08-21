根据 [OIwiki](https://oi-wiki.org/) 的结构整理

---
TODO: 数据结构整理: KMP, ...

- 背包问题
- 差分数组
- 并查集 <https://leetcode-cn.com/tag/union-find/problemset/>
    - <https://leetcode-cn.com/problems/merge-intervals/>
- 区间树(线段树) Interval Tree

在力扣上这种区间问题有三大种解法，分别是: (题目整理 from [here](https://leetcode-cn.com/problems/longest-substring-of-one-repeating-character/solution/python-guo-ran-wo-huan-shi-geng-xi-huan-olhop/))

1. 区间并查集解法
   - 区间的合并就是并查集的 union(区间左端点，区间右端点) 过程
   [352. 将数据流变为多个不相交区间](https://leetcode-cn.com/problems/data-stream-as-disjoint-intervals/)
   [2158. Amount of New Area Painted Each Day](https://leetcode-cn.com/problems/amount-of-new-area-painted-each-day/)
   [meituan-002. 小美的仓库整理](https://leetcode-cn.com/problems/TJZLyC/)
2. 线段树解法
    非常普适的做法，但是感觉线段树不好写，变一下就不会了
    [715. Range 模块](https://leetcode-cn.com/problems/range-module/)
    [2158. Amount of New Area Painted Each Day](https://leetcode-cn.com/problems/amount-of-new-area-painted-each-day/)
3. 平衡树解法
    维护一个 Treemap(java)/map(C++)/SortedDict(python)，存储区间的 start=>end 映射即可
    [352. 将数据流变为多个不相交区间](https://leetcode-cn.com/problems/data-stream-as-disjoint-intervals/)

- KMP [题目汇总](https://leetcode-cn.com/problems/distinct-echo-substrings/solution/by-flix-zsuj/)
