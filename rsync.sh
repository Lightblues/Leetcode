# 同步目录, 注意不能省略 src 的最后一个 `/` !
rsync -av learn-r/notes/ "$HOME/Library/Mobile Documents/iCloud~com~coderforart~iOS~MWeb/Documents/426-R/"
# 同步文件
rsync -av notes/Leetcode-contests.md "$HOME/Library/Mobile Documents/iCloud~com~coderforart~iOS~MWeb/Documents/400-code-basic"
