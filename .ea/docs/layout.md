# Layout

Counts are tracked files as of 2026-11-03 (`git ls-files`). "Status" is the state of use, not a decision; decisions are in `../log/decisions.md`, the cleanup plan in `../roadmap.md`.

| Path | Files | What | Status |
|---|---|---|---|
| `LC-contest/` | 503 | LeetCode weekly/biweekly contest solutions, grouped by contest-number range (`0x3`, `151-200`, … `451-550`), plus `acwing/ atcoder/ codeforce/ luogu/ LCCUP-力扣杯/ misc/ others.py`; `record-contest.md`, `crawl.py`, `utils_leetcode.py`, `structures.py` are helpers. The only part still growing (newest: contest 467, 2026-11) | active |
| `LC-daily/` | 8 | daily-problem solutions (`d001-050` … `d101-150`, `daily2201.py` …) | active, slow |
| `LC-notes/` | 37 | topic summaries and the problem log (`LeetCode 刷题记录.md`, `Leetcode-contests.md`, `Leetcode-daily.md`, `01-分类总结/`) | reference |
| `algorithm-ds-templates/` | 142 | algorithm and data-structure templates by topic (`Basic-`, `DP-`, `DS-`, `Graph-`, `Search-` …) | reference |
| `LC-go/` | 36 | Go solutions by technique (`DFS`, `SlidingWindow`, `backtrack`, …) | old |
| `interview-list/` | 329 | one directory per company interview, named `YYMMDD-<company>` (Ctrip, Meituan, Pinduoduo, Baidu, Optiver …), 2023-03 | archive candidate |
| `interview/` | 117 | interview prep material (`ML-NLP-master`, `_DL`, `quant`, `interview-README.md`); origin of `ML-NLP-master` not checked, it may be a copy of a third-party repository | archive candidate |
| `python/ go/ cpp/ js/ java/ r/ rust/ lean/ sql/ shell/ stat/ Mathematica/` | 828 | language-learning notes and exercises, one directory per language | archive candidate |
| `test/ tests/ utils/ scripts/ docs/` | 14 | scratch scripts (`test/01.py` …) and small utilities | clean up |

Not tracked and not to be committed: `.venv/`, `.ea/.tmp/`, `*.jsonl`, `*.csv`.

Root files: `README.md` (the user's reading list of solution collections and study sites, plus the TODO "clean misc codes"), `pyproject.toml` and `uv.lock` (Python environment), `package.json` (`underscore`, for `js/`).
