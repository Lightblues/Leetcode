# leetcode

Personal practice code and notes, 2021-04 to now: LeetCode contest and daily solutions (Python), algorithm templates, interview material, and per-language learning directories. About 2,000 tracked files; the repository has grown by accretion, and its cleanup is open (`.ea/roadmap.md`).

## Quick Reference

- **Where**: devcloud_cpu `/data/projects/input/leetcode` (moved from the Mac on 2026-11-03); GitHub `Lightblues/Leetcode` (private)
- **Setup**: `uv sync` (Python `~=3.10`; dependencies `easonsi`, `dotenv`, `ipython`; `package = false`, nothing is installed as a package). `js/` alone uses node (`underscore`)
- **Run a solution**: a file is a plain script with `class Solution`, written to be pasted into LeetCode; there are no tests and no CI. To check one, import the class and call the method by hand
- **Docs**: `.ea/docs/README.md` (directory map), `.ea/roadmap.md` (cleanup plan), `.ea/log/decisions.md`; layout follows forge-run `references/ea-layout.md`
- **Agent prompts**: `.ea/inst/` keeps prompts that were run against this repository (for example asking an agent to implement one method in a given contest file)

## Conventions of a contest file

`LC-contest/<range>/<contest-number>.py`, for example `LC-contest/451-550/467.py`:

- module docstring first: the contest URL, then one entry per problem with tags (`#背包`) and the user's own notes (Chinese), signed `Easonsi @YYYY`
- then one `class Solution` per problem, each with a docstring naming the problem (`""" 3683. 完成一个任务的最早时间 """`), the method signature as LeetCode gives it
- `from typing import *` at the top

Notes are the user's writing: add to them, do not rewrite them.

## Rules

- Do not move or delete directories. The cleanup plan in `.ea/roadmap.md` is undecided; anything not listed as decided stays where it is.
- New solutions go next to their siblings (`LC-contest/<range>/`, `LC-daily/`), never into the language-learning directories.
- `*.jsonl` and `*.csv` are git-ignored on purpose (data); do not commit them.
- A change to the layout updates `.ea/docs/` in the same commit.

## Coding Style

- Solutions: Python 3.10, type hints as given by LeetCode, no external dependencies
- Comments in the solutions follow the user's own style (Chinese); docs under `.ea/` are English
