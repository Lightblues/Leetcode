- VSCode 中配置 R <https://github.com/REditorSupport/vscode-R/wiki/Getting-Started>
    - 遇到无法启动的问题, 应该是环境变量没有引入, 通过 `Sys.getenv("PATH")` 查看
        - 暂时的解决策略是在 `"terminal.integrated.env.osx"` 配置项中添加 `"R_HOME": "/Library/Frameworks/R.framework/Resources",`
        - 另外 pandoc 无法识别的问题也可以添加 `"PATH": "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/Library/Frameworks/R.framework/Resources/bin:$PATH"` 解决
    - 但终归不是优雅的方案? 还是怪 VSCode 没有官方的 R 支持

R语言教程 <https://www.runoob.com/r/r-tutorial.html>
R Graph Gallery <https://www.r-graph-gallery.com/index.html>

R语言的话, 我之前的教程比较零散, 刚刚搜了一下, <https://www.math.pku.edu.cn/teachers/lidf/docs/Rbook/html/_Rbook/index.html> 这个看上去不错, 这个北大的教授超厉害, 可以配合《R语言实战》. 然后初学的话可以看看视频轻松一点, B站上这个 <https://www.bilibili.com/video/BV19x411X7C6> 似乎播放量比较大, 一个好处是评论区kennel会有讨论和资源
