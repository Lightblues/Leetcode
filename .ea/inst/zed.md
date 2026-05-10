- [language support](https://zed.dev/docs/configuring-languages) 语言支持
  - [python](https://zed.dev/docs/languages/python)
    - LSP config
    - debug

## Python
语言支持通常由以下三层构成：
1. Tree-sitter 语法解析 — 负责语法高亮、代码折叠、结构识别，速度极快，无需额外配置。
2. Language Server (LSP) — 提供智能补全、跳转定义、类型检查、诊断报错等功能。
3. Debug Adapter — 支持断点调试。

Zed 的格式化分两个阶段：第一阶段执行 code actions（如 Ruff 的 import 整理），第二阶段执行 formatter（如 Ruff 或 Black）。两个阶段独立配置，可以组合使用，比如用 Ruff 整理 import、用 Black 做最终格式化。

- 如何禁止 zed python 的自动 format (save的时候)
- 如何配置禁用一些警告? e.g.
```sh
`from typing import *` used; unable to detect undefined names
`List` may be undefined, or defined from star imports
Multiple statements on one line (colon)
```
// @pyproject.toml ; @/Users/frankshi/.config/zed/settings.json

# Notes
[config]
- @/Users/frankshi/.config/zed/settings.json
- debug: @.zed/debug.json
