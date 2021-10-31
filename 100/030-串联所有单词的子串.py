"""
给定一字符串 s 和一些长度相同的单词 words，找出 s 中恰好可以由 words 中所有单词串联形成的子串的起始位置。
注意子串要与 words 中的单词完全匹配，中间不能有其他字符，但不需要考虑 words 中单词串联的顺序。

输入：
  s = "barfoothefoobarman",
  words = ["foo","bar"]
输出：[0,9]
解释：
从索引 0 和 9 开始的子串分别是 "barfoo" 和 "foobar" 。
输出的顺序不重要, [9,0] 也是有效答案。

输入：
  s = "wordgoodgoodgoodbestword",
  words = ["word","good","best","word"]
输出：[]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/substring-with-concatenation-of-all-words
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        results = []

        from collections import Counter
        words_counter = Counter(words)

        L = len(words[0])
        n_words = len(words)
        for i in range(len(s)-L*n_words+1):
            sub_str = s[i : i+L*n_words]
            """
            原本还以为 words 中的所有字均不同，所以想统计不同的字出现频次，若不同字出现的数量 < n_words 则不匹配
            结果是可能相同的如 words = ["word","good","best","good"]
            于是用了 Counter，grand truth 是 Counter(words)。这样在第二层遍历的时候：
            1. 有不在 words 中的字直接 break；
            2. Counter[word]<0 时也 break；
            所以是在遍历过程中检查是否有不满足的条件 —— 若均满足，则临时记录的那个 Counter 中的 values 应该均为 0；为了避免这一判断，设置了一个 `flag`。
            """
            # from collections import defaultdict
            # counter = defaultdict(int)
            # for j in range(n_words):
            #     ssub_str = sub_str[j*L : (j+1)*L]
            #     if ssub_str in words:
            #         counter[ssub_str] += 1
            #     else:
            #         break
            # if len(counter)==n_words:
            #     results.append(i)

            flag = True    # 判断是否匹配的标记
            temp_counter = words_counter.copy()
            for j in range(n_words):
                ssub_str = sub_str[j*L: (j+1)*L]
                if ssub_str not in words:
                    flag = False
                    break
                if temp_counter[ssub_str]>0:
                    temp_counter[ssub_str]-=1
                else:
                    flag = False
                    break
            if flag:
                results.append(i)
        return results

s = "wordgoodgoodgoodbestword"
words = ["word","good","best","good"]
# s = "barfoothefoobarman"
# words = ["foo","bar"]
print(Solution().findSubstring(s, words))

