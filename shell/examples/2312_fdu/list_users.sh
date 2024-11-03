# 列出所有的用户, 筛选用户名中带有 22 的, 输出到 o.txt 中

#!/bin/bash

fn=userlist.txt
# 使用 awk 命令来获取所有用户的用户名，并筛选包含 "22", "23", 或 "24" 的用户名
usernames=$(awk -F: '$3 >= 1000 {print $1}' /etc/passwd | grep -E "22|23|24")
echo "$usernames" > $fn
echo "筛选后的用户名已保存到 $fn"
