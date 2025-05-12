#!/bin/bash

# 设置自动提交的定时任务
# 此脚本将创建一个cron任务，定期执行auto_commit.sh

# 获取当前脚本所在的绝对路径
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 检查auto_commit.sh是否存在且可执行
if [ ! -x "$SCRIPT_DIR/auto_commit.sh" ]; then
    echo "错误: $SCRIPT_DIR/auto_commit.sh 不存在或不可执行"
    exit 1
fi

# 创建临时crontab文件
TEMP_CRONTAB=$(mktemp)
crontab -l > "$TEMP_CRONTAB" 2>/dev/null

# 检查是否已经存在相同的cron任务
if grep -q "$SCRIPT_DIR/auto_commit.sh" "$TEMP_CRONTAB"; then
    echo "自动提交任务已经存在于crontab中。"
    rm "$TEMP_CRONTAB"
    exit 0
fi

# 添加每小时执行一次的cron任务
echo "0 * * * * $SCRIPT_DIR/auto_commit.sh" >> "$TEMP_CRONTAB"

# 应用新的crontab
crontab "$TEMP_CRONTAB"
rm "$TEMP_CRONTAB"

echo "已设置自动提交任务，将每小时执行一次。"
echo "您可以通过运行 'crontab -l' 查看所有定时任务。"
echo "如需修改执行频率，请编辑crontab（运行 'crontab -e'）。"
