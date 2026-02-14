# AGENTS Guidelines

- Read definitions and terminology in `DEFNS.md`
- Read specifications (`SPEC.md`), both in the root, and potentially nested within subfolders

- When planning nontrivial changes update the `TODO.md` which sits alongside the relevant `SPEC.md`
- Keep the TODOs up to date
- Pause between TODO items and invite the operator to review

- If asked to make changes ad-hoc (i.e. not part of original specification) ask if you should update `SPEC.md` to match

## Tests
- `test.sh` is the integration test for `bootstrap_inst.sh`/`install.py`. It launches a fresh incus container, runs setup, and verifies all tools, symlinks, and configs. Incus must be initialised on the host.
- Subfolders with their own `SPEC.md` may have local pytest tests (e.g. `resources/tok/test.py`). pytest must be the entry point (it discovers and runs `test_*` functions), so use `uv run --with pytest pytest <path> -v` to supply pytest as an ad-hoc dependency.
