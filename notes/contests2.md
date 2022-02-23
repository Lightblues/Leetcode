### D71

- 2160. 拆分数位后四位数字的最小和
- 2161. 根据给定数字划分数组
- 2162. 设置时间的最少代价
    - 设置四位的时间, 前后两位分别表示分钟和秒钟, 例如 `8090` 表示 80*60+90 秒
    - 给定 startAt ，moveCost ，pushCost 和 targetSeconds 分别表示初始的手指位置, 移动和按按钮的代价, 以及目标的秒数, 要求返回最小的代价. **前置0可以不输入**
    - 思路: 模拟
        - 注意到, 犹豫两位数字可以大于59, 因此同样的秒数可能有多种表示. 除了 1. 基本的 `minutes, seconds = targetSeconds//60 , targetSeconds%60`, 还有可能 2. 是 `minutes-1, seconds+60` (`seconds+60<100`), 计算两者较小的代价.
        - 用函数 `getCost(minutes, seconds)` 模拟该方案的代价.
        - 需要注意边界: 1. 当 `targetSeconds<60` 时 第二种方案非法; 2. 当 `targetSeconds>=60000` 时, 第一种方案非法. 因此可以在 getCost 函数中增加判断: `minutes>99 or seconds>99 or minutes<0 or seconds<0` 时返回 Inf, 更简单.
- 2163. 删除元素后和的最小差值
    - 给一个长度为 3n 的数组 nums, 要求删除其中 n个数字, 使得删除后, 数组前n个数字之和 - 后n个数字之和最小.
    - 方法一：优先队列 [here](https://leetcode-cn.com/problems/minimum-difference-in-sums-after-removal-of-elements/solution/shan-chu-yuan-su-hou-he-de-zui-xiao-chai-ah0j/)
        - 目标: 前n个数字之和最小, 后n个数字之和最大.
        - 可知, 最后剩余的两组数字, 其原始的分割点一定在 [n, 2n] 之间. 因此, 可以 遍历遍历每一个分割点, 分别计算前后的最小和最大和, 然后求最小值.
        - 为此, 可以分别建立一个最大堆和最小堆, 遍历 [n, 2n] 个数字 (pushpop), 记录每一个分割点的的值. 需要注意的是, 后半部分应该逆序, 注意代码.
