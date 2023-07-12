""" 爬取HOT100数据 @230713
遗憾的是 freqBar 数据是空的? 不知道是不是因为没加cookie
成果: https://v0r8x11vrv.feishu.cn/docx/YSvwdxUhwoND1Oxryw7cLCdvnmc
"""


#%%
import requests
import json
# https://blog.csdn.net/Ezrealer/article/details/106664656

url = "https://leetcode.cn/graphql/"
payload = ' {"query":"""\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    hasMore\n    total\n    questions {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId\n      isFavor\n      paidOnly\n      solutionNum\n      status\n      title\n      titleCn\n      titleSlug\n      topicTags {\n        name\n        nameTranslated\n        id\n        slug\n      }\n      extra {\n        hasVideoSolution\n        topCompanyTags {\n          imgUrl\n          slug\n          numSubscribed\n        }\n      }\n    }\n  }\n}\n    ""","variables":{"categorySlug":"","filters":{"listId":"2cktkvj"},"limit":1000},"operationName":"problemsetQuestionList"} '
payload = eval(payload)
headers = {
    'Origin': 'https://leetcode.cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'Referer': 'https://leetcode.cn/problem-list/2cktkvj/',
    # 'Cookie': 'did=web_62bf12a9aa82ae952a919547a686f5fa; ',
    'Connection': 'keep-alive',
    # 'x-original-url': 'https://live.kuaishou.com'
}

response = requests.request("POST", url, headers=headers, data = json.dumps(payload))

# print(response.content.decode())
# %%
data = response.content.decode()
# parse the data
data = json.loads(data)['data']['problemsetQuestionList']['questions']
data[0]
# %%
problems = []
for d in data:
    # frontendQuestionId, titleCn, difficulty, acRate, freqBar, titleSlug, topicTags
    # 题号, 名字, 难度, 通过率, 出现频次, 链接, 标签
    row = [d['frontendQuestionId'], d['titleCn'], d['difficulty'], d['acRate'], d['freqBar']] #, d['titleSlug']]
    row += [f"https://leetcode.cn/problems/{d['titleSlug']}"]
    tags = [i['nameTranslated'] for i in  d['topicTags']]
    row += [",".join(tags)]
    problems.append(row)
import pandas as pd
df = pd.DataFrame(problems, columns=['id', 'name', 'difficulty', 'acRate', 'freqBar', 'link', 'tags'])
df
# %%
# 转为markdown表格! 依赖 `tabulate` 包
# 想多了, 直接转为csv, 然后复制到飞书上即可! 
# with open('hot100.md', 'w') as f:
#     f.write(
#         df.to_markdown(index=False)
#     )
# %%
df.to_csv('hot100.csv', index=False)
# %%
