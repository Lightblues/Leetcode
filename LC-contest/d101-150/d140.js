/* 
@2025-06-07
https://leetcode.cn/contest/biweekly-contest-140
*/

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
见 Python 题解
*/
/**
 * @param {string} word1
 * @param {string} word2
 * @return {number[]}
 */
var validSequence = function(word1, word2) {
    let m = word1.length;
    let n = word2.length;
    
    // Initialize suffix array
    let suf = new Array(m + 1).fill(0);
    let j = n - 1;
    for (let i = m - 1; i >= 0; i--) {
        if (word1[i] === word2[j]) {
            j -= 1;
        }
        if (j === -1) break;
        suf[i] = j + 1;
    }
    
    let ans = [];
    j = 0;
    let changed = false;
    
    // Approach 2: Try to match as much as possible
    for (let i = 0; i < m; i++) {
        if (word1[i] === word2[j] || (!changed && suf[i+1] <= j+1)) {
            if (word1[i] !== word2[j]) changed = true;
            j += 1;
            ans.push(i);
            if (j === n) return ans;
        }
    }
    return [];
};


// main
var results = [
    // minElement(nums = [10,12,13,14]),
    // maximumTotalSum(maximumHeight = [2,3,4,3]),
    validSequence(word1 = "vbcca", word2 = "abc"),
    validSequence(word1 = "bacdc", word2 = "abc"),
];
for (let r of results) {
    console.log(r);
}
