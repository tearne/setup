# Specification: Dev Environment Setup CLI

## Overview

A command-line application to set up basic tools for development on Ubuntu/Debian.

## Usage

- Just invoking one command to set everything up

## Dependencies

- BASH - no assumption of a specific version of Python, which will be installed by `uv` at runtime.
- Use Python 3.12 and whatever dependencies aid readabiliy
- `git` - if the script is to be pulled from external repository.

## Configuration

Intially, there's no configuration.  Everything is hard coded in the source code.  If a tool isn't needed the user should be able to simply open the code and comment out a clearly named function call (e.g. `install_zellij()`).

## Functional Requirements

- Idempotency - if a tool installed, skip it, if a config exists, warn.
- Minimal interaction once started - user starts it and goes to get coffee.
- Error handling - fail fast, with breadcrumbs indicating on how far it got.
- Prompts for user password once at start.
- Wherever possible, the tool will install dependencies it needs, minimising user burden

### Tools to install
All latest stable versions
- `uv` (via `curl`) - presumed bootstrapped via outer BASH script or manually by user.
- Rust and Cargo with rust analyzer (via RustUp (via `curl`))
- Helix editor (download latest stable release from GitHub and install in `~.local/bin`).
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
- The test harness should detect early if it's running inside a container without nesting support, and abort with a clear message rather than failing mid-run.

### Test scenarios

- Test existing configs are not overwritten.  Warn that they will not be overwritten and move on.
- Check that new terminals get `.local/bin` on their path.
- Test the overall installation process completes without error

### Logging / Output

- No logging to file, only stdout/stderr
- Use a structured/hierarchical log output format, which reveals which stage/sub-stage we're at, as well as output from any processes being run.

## Non-Goals

- No flags and config files at this stage, as prefer to simply edit the code.
- Not cross platform - Debian/Ubuntu based only
 
## Future goals

- Colourful and pretty stdout with progress bar(s)

## Open Questions

- The goal is for minimal user effort for installation, but with a readable and hackable script.  If there are other options than BASH bootsrtapping `uv` install which installs Python then these should be considered.
