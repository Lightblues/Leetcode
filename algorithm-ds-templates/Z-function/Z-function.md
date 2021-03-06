- 2223. 构造字符串的总得分和 `hard`
    - 对于一个字符串, 从右往左得到长度为 1,2,... 的连续子串, 分别计算该子串与原字符串的最大前缀长.
    - **Z 函数**（**扩展 KMP**） 参见 <https://oi-wiki.org/string/z-func/>
    - 我们定义 Z 函数为: **z[i] 为 s[i:n-1] 与原字符串 s 的最长前缀匹配长度**.
        - 也即, `s[i:i+z[i]-1] = s[0:z[i]-1]` (闭区间), 称为 匹配段, 也可以叫 **Z-box**
    - 核心是要维护一个匹配区间 [l,r] (Z-box)) 满足该区间为前缀匹配; 在遍历过程中, 维护 `l<=i`.
        - 对于遍历到的 i, 若 `i<=r`, 此时有 `s[i:r] = s[i-l:r-l]` (闭区间),
            - 若还满足 `z[i-l]<r-i+1` (区间 [i,r] 的长度为 r-i+1, 我们已经在遍历 i-l 时发现了前缀匹配长度比它小), 则有 z[i] = z[i-l]
            - 否则, 说明 [i,r] 区间是前缀, 从 r+1 开始继续匹配
        - 若不满足 `i<=r`, 则从 i+1 开始继续匹配 (和上面的情况2一样)
        - 注意当我们遍历超过 r 时需要更新 `l, r = i, i+z[i]-1` (显然维护的条件 `i<=l` 仍满足)
    - 复杂度分析 (看下面的代码): 外层 i 循环一遍, 内部的 while 训练每执行一次都会使得 r 向后移动, 因此最多执行 O(n) 次; 所以总的复杂度为 O(n).
