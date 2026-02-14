# AGENTS Guidelines

- Read definitions and terminology in `DEFNS.md`
- Read specifications (`SPEC.md`), both in the root, and potentially nested within subfolders

- When planning nontrivial changes update the `TODO.md` which sits alongside the relevant `SPEC.md`
- Keep the TODOs up to date
- Pause between TODO items and invite the operator to review

## Tests
- `test.sh` is the integration test for `setup.sh`/`setup.py`. It launches a fresh incus container, runs setup, and verifies all tools, symlinks, and configs. Incus must be initialised on the host.
- Subfolders with their own `SPEC.md` may have local tests (e.g. `resources/tok/test_tok.sh`).
