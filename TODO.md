# TODO

- [x] Fix 1: Install `harper-ls` (SPEC.md line 38)
- [x] Fix 2: Preserve existing configs instead of replacing (SPEC.md line 26, 80)
- [x] Fix 3: End-of-run warning summary (SPEC.md line 26)
- [x] Fix 4: Hardcoded paths in `test.sh` (lines 24-28)
- [x] Fix 5: Use relative symlinks for configs (SPEC.md line 49)
- [x] Fix 6: Diff-based config conflict detection with end-of-run diff display (SPEC.md lines 50-53)
- [x] Fix 7: Configure harper-ls with British English dictionary (SPEC.md line 67)
- [x] Fix 8: Replace `pylsp` with `pyright` + `ruff` in setup.py and test.sh
- [x] Fix 9: Add `soft-wrap` for markdown in `resources/helix/languages.toml`
- [x] Fix 10: Add language server config for `pyright`/`ruff` in `resources/helix/languages.toml`
- [x] Fix 11: Add `venv` guard to `setup.py`
- [x] Fix the issue of passphrase being visible in the process list, but only for the python version.  Update the spec to indicate this security requirement
- [x] Remove BASH version of tok
- [x] Rewrite the `tok` tests in a Pythonic style
- [x] Write a brief README.md
- [x] Display the shell command being run alongside the task description (SPEC.md line 34)
- [x] Prevent long command output from pushing task headers off screen (SPEC.md line 34)
- [x] Create install log file with commands and full output (SPEC.md Logging/Output)
- [x] Incus ZFS fallback: check if ZFS is installed instead of detecting container (SPEC.md line 53)
- [x] Rename setup.py to install.py and setup.sh to bootstrap_inst.sh, and update SPEC accordingly

