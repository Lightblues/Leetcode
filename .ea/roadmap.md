# Roadmap

Open questions and the order to answer them. Nothing here is decided; once the user decides, it becomes an entry in `log/decisions.md`.

## 1. Classify (agent can start this, read-only)

Walk each directory in `docs/layout.md` marked "archive candidate" or "clean up" and record, in `log/YYYY-MM-DD-cleanup-inventory.md`: what is there, last commit date, whether it is the user's own writing or a copy of third-party material (check `git log` authorship and the contents), and size. No file is moved in this step.

## 2. Decide with the user

- `interview-list/` (company interview notes, 2023-03) and `interview/`: keep here, move to `quill` `archive/`, or delete.
- Language-learning directories (`python/ go/ cpp/ js/ java/ r/ rust/ lean/ sql/ shell/ stat/ Mathematica/`): which ones still matter. Candidates to drop first: those with no commit in 2 years.
- Third-party copies (for example `interview/ML-NLP-master`, if confirmed): remove and leave a link in `README.md`.
- `test/ tests/ utils/ scripts/ docs/`: fold into one `scratch/` or delete.

## 3. Do the cleanup

One commit per directory moved or removed, so any of it can be reverted. Keep `LC-contest/`, `LC-daily/`, `LC-notes/`, `algorithm-ds-templates/` in place; they are the live part.

## 4. After the cleanup

- Shrink `README.md` to the reading list plus a pointer to `.ea/docs/layout.md`.
- Decide whether `LC-go/` merges into `LC-contest/` or stays.
