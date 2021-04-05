"""
给定一个单词数组和一个长度maxWidth，重新排版单词，使其成为每行恰好有maxWidth个字符，且左右两端对齐的文本。
你应该使用“贪心算法”来放置给定的单词；也就是说，尽可能多地往每行中放置单词。必要时可用空格' '填充，使得每行恰好有 maxWidth个字符。
要求尽可能均匀分配单词间的空格数量。如果某一行单词间的空格不能均匀分配，则左侧放置的空格数要多于右侧的空格数。
文本的最后一行应为左对齐，且单词之间不插入额外的空格。

输入:
words = ["This", "is", "an", "example", "of", "text", "justification."]
maxWidth = 16
输出:
[
 "This    is    an",
 "example  of text",
 "justification.  "
]

输入:
words = ["What","must","be","acknowledgment","shall","be"]
maxWidth = 16
输出:
[
 "What  must  be",
 "acknowledgment ",
 "shall be    "
]
解释: 注意最后一行的格式应为 "shall be    " 而不是 "shall     be",
    因为最后一行应为左对齐，而不是左右两端对齐。
     第二行同样为左对齐，这是因为这行只包含一个单词。

输入:
words = ["Science","is","what","we","understand","well","enough","to","explain",
        "to","a","computer.","Art","is","everything","else","we","do"]
maxWidth = 20
输出:
[
 "Science is what we",
  "understand   well",
 "enough to explain to",
 "a computer. Art is",
 "everything else we",
 "do         "
]

"""
from typing import List
class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        wordlens = [len(w) for w in words]
        nwords = len(words)
        start = 0
        output = []
        while start <= nwords-1:
            acc = wordlens[start]
            p = start
            while p+1<=nwords-1 and acc+wordlens[p+1]+1 <= maxWidth:
                p += 1
                acc += wordlens[p]+1
            # [start, p] 之前的 word 作为一行
            n_words = p-start+1
            n_spaces = maxWidth-sum(wordlens[start:p+1])
            if n_words == 1:
                s = words[start] + ' '*n_spaces
            else:
                if p != nwords-1:
                    avg_spaces, q = divmod(n_spaces, (n_words-1))
                    s = ''
                    for i in range(q):
                        s += words[start+i] + ' '*(avg_spaces+1)
                    s += (' '*avg_spaces).join(words[start+q: p+1])
                else:
                    # 最后的几个 words
                    s = ' '.join(words[start: p+1]) + ' '*(n_spaces-(p-start))
            output.append(s)
            start = p+1
        return output





# words = ["This", "is", "an", "example", "of", "text", "justification."]
# maxWidth = 16
words = ["What","must","be","acknowledgment","shall","be"]
maxWidth = 16
res = Solution().fullJustify(words, maxWidth)
for l in res:
    print(l, len(l))
