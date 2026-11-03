# Decisions

Append-only. Reverse an entry by adding a new one; change only the old entry's status line.

## D001. Moved to devcloud_cpu as-is; cleanup comes later

**Date**: 2026-11-03　**Status**: active

The repository was cloned to `/data/projects/input/leetcode` on devcloud_cpu without reorganizing it. Four uncommitted Mac changes (contest 465-467 solutions, one deleted scratch file) were committed first as `chore: sync local changes before migrating to devcloud_cpu` so nothing was lost. The messy layout is known; cleaning it is a separate, user-reviewed task (`.ea/roadmap.md`), because moving personal notes is hard to undo by guesswork. The Mac checkout can be removed once the user is satisfied with the devcloud copy.
