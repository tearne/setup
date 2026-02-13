# AGENTS Guidelines

- Read definitions and terminology in `DEFNS.md`
- Read specifications (`SPEC.md`), which may also be nested within sub folders

- When planning non-trivial changes, offer to save or update/append to a `TODO.md` (in the root of the project or relevant sub dir) and keep it up to date as features are implemented.

- Prompt to consider committing before starting work on a new feature

# Testing: Incus Nested Container Harness

`test.sh` launches an Ubuntu 24.04 incus container and runs `setup.sh` inside it.
This requires nested container support.

## Prerequisites

No special configuration — just have `incus` installed and initialised (`incus admin init`).

