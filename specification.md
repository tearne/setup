# Specification: Dev Environment Setup CLI

## Overview

A script to install basic dev tools on Ubuntu/Debian.

## Usage

- Run one command to set everything up:
  - setup.sh if system doesn't have `uv` installed already
  - setup.py if it does.

## Dependencies

- BASH
- `uv` will ensure Python is used at runtime.
- Use Python 3.12 and whatever dependencies aid readabiliy

## Configuration

Intially, there's no configuration.  Everything is hard coded in the source code.  If a tool isn't needed the user should be able to simply open the code and comment out a clearly named function call (e.g. `install_zellij()`).

## Functional Requirements

- Installation commands should be clearly displayed while the command runs (not pushed off top of terminal).
- Idempotency - if a tool installed, skip it, if a config exists, warn.
- Minimal interaction once started - user starts it and goes to get coffee.
- Error handling - fail fast, with breadcrumbs indicating on how far it got.
- Prompts for user password once at start if required.
- Wherever possible, the tool will install its own dependencies at runtime (e.g. `uv`, `curl`).

### Tools to install
All latest stable versions
- `uv` (via `curl`) - bootstrapped via outer BASH script or manually by user.
- Rust and Cargo with rust analyzer (via RustUp (via `curl`))
- Helix editor (download latest stable deb from GitHub).
- Helix config (via soft link to a local resources directory if possible):
     ```
     theme = "autumn"

     [editor]
     true-color = true
     line-number = "relative"
     bufferline = "always"
     rulers = [80]
     ```
- Zellij (via `cargo binstall`)
- `htop`, `btop` and `incus` (installed non-interactively via apt repos - no PPA)


## Non-Functional Requirements

- Prefer a single Python source file, unless it compromises readabiliy.
- Concise source code, easily hackable, similar in spirit to a script.
- Root structure to include:
```
/root/setup/
├── setup.sh    # Bash entry point (the one command)
├── setup.py    # All Python logic (uv single-file script)
├── test.sh     # Incus test harness
```
- Use `#!/usr/bin/env -S uv run --script` in `setup.sh`


## Testing

- Testing where possible without compromising the simplicity of the code.
- Testing can be undertaken within an incus container where relevant.
- Use the latest LTS Ubuntu for testing.

### Test scenarios

- Test existing configs are not overwritten.  Warn that they will not be overwritten and move on.
- Check that new terminals get `.local/bin` on their path.
- Test the overall installation process completes without error

### Logging / Output

- No logging to file, only stdout/stderr
- Use a structured/hierarchical log output format, which reveals which stage/sub-stage we're at, as well as output from any processes being run.

## Non-Goals

- No flags and config files at this stage, as prefer to simply edit the code.
- Not cross platform - Debian/Ubuntu based only.
- No fancy logging, just fail fast with breadcrumbs. 

## Future goals

- Colourful and pretty stdout with progress bar(s)

## Open Questions

- The goal is for minimal user effort for installation, but with a readable and hackable script.  If there are other options than BASH bootsrtapping `uv` install which installs Python then these should be considered.
