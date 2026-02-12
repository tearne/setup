# Project: Dev Environment Setup CLI

## Admin

- Read `specification.md` before making changes.
- Ignore files in `archive` unless specifically mentioned.

## Style

- Python 3. Flat and procedural, script-like, style.
- Functions over classes, unless state genuinely helps (e.g. `Password`).
- No docstrings or comments unless the logic is non-obvious.

## Principles

- Conciseness over abstraction. Three similar lines are better than a helper nobody asked for.
- Don't add error handling, flags, or configurability beyond what the spec requires.
- If a change would add significant complexity, ask first.

## Testing

- Test where possible, but not if it introduces excessive complexity
- `test.sh` requires nested incus support — see `TESTING.md` for outer container prerequisites.

## Target platform

Ubuntu / Debian (`apt`-based) only.  If run on other systems just exit.
