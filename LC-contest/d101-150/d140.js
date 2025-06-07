/* 3300. 替换为数位和以后的最小元素 #easy 将数组中每个数字都替换为数位和 */
/**
 * @param {number[]} nums
 * @return {number}
 */
var minElement = function(nums) {
    for (let i = 0; i < nums.length; i++) {
        nums[i] = nums[i].toString().split('').reduce((a, b) => a + parseInt(b), 0);
    }
    return Math.min(...nums);
};

/* 3301. 高度互不相同的最大塔高和 #medium 每个位置有一个最大高度限制, 要为每个位置设置一个高度, 使得各不相等的情况下, 求最大和, 不满足返回 -1 
思路: 排序
*/
/**
 * @param {number[]} maximumHeight
 * @return {number}
 */
var maximumTotalSum = function(maximumHeight) {
    maximumHeight.sort((a, b) => b - a);
    var acc = 0;
    var preMax = maximumHeight[0] + 1;
    for (let x of maximumHeight) {
        if (preMax == 1) return -1;
        var y = Math.min(preMax - 1, x);
        acc += y;
        preMax = y;
    }
    return acc;
};

/* 3302. 字典序最小的合法序列 #medium 找到一个最小的递增的index序列, 让 word1 的子序列 "几乎等于" word2, 这里的 "几乎等于" 是指最多只相差一个字符
限制: n 3e5
思路1: #前后缀分解
    关联: [2565. 最少得分子序列] 也是找子序列
    预处理: 先计算后缀 suf[i] 表示 words1[i:] 可以匹配 word2 的最长后缀的左下标
    关键是如何 "字典序最小"? 枚举前缀位置i, 同时记录word2的匹配位置j:
        若 word1[i] == word2[j], 直接使用;
        若 不等, 且 suf[i+1] <= j+1, 说明一定要修改了 (同时后缀可以匹配上!)
        注意! 为了避免仅修改一次, 需要用一个flag来标记是否修改过

*/
/**
 * @param {string} word1
 * @param {string} word2
 * @return {number[]}
 */
var validSequence = function(word1, word2) {
    
};

// main
var results = [
    // minElement(nums = [10,12,13,14]),
    maximumTotalSum(maximumHeight = [2,3,4,3]),
];
for (let r of results) {
    console.log(r);
}
