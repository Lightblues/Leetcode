#!/bin/bash

# 自动提交并推送到GitHub的脚本
# 使用方法: ./auto_commit.sh [提交信息]

# 设置工作目录为项目根目录（脚本所在目录的上一级）
cd "$(dirname "$0")/.."

# 获取当前时间作为默认提交信息
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
COMMIT_MESSAGE="${1:-自动提交: $TIMESTAMP}"

# 检查是否有变更
if [[ -z $(git status --porcelain) ]]; then
    echo "没有需要提交的变更。"
    exit 0
fi

# 添加所有变更
git add .

# 提交变更
git commit -m "$COMMIT_MESSAGE"

# 推送到远程仓库
git push origin main

echo "成功提交并推送变更到GitHub。"
echo "提交信息: $COMMIT_MESSAGE"
