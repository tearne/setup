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

Intially, there's no configuration.  Everything is hard coded in the source code.  The script should have a single, obvious place near the top where each tool's install is called directly — e.g. `install_zellij()`. To skip a tool, the user comments out that line.

## Functional Requirements

- Installation commands should be clearly displayed while the command runs (not pushed off top of terminal).
- Idempotency - if a tool installed, skip it, if a config exists, warn.
- Minimal interaction once started - user starts it and goes to get coffee.
- Error handling - fail fast, with breadcrumbs indicating on how far it got.
- Prompts for user password once at start if required.
- Wherever possible, the tool will install its own dependencies at runtime (e.g. `uv`, `curl`).

### Third-party tools to install
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
- Incus initialisation (`incus admin init`) with ZFS storage backend.  Falls back to `dir` backend when running inside a container (ZFS kernel modules unavailable).

### Scripts / aliases to install
- `tok` (see `resources`) to be installed in `.local/bin`

### Configuration to set up
- Ensure that `.local/bin/` is on the users path.

## Non-Functional Requirements

- The code should be written in a "Python orchestrated shell script" (POSS) style:
  - If there is a reasonable way to achieve an installation sub-task in the shell, prefer running that command that over the Pythonic equivalant.
  - Examples:
    - To download the latest vesion of `helix`:
```sh
curl -s https://api.github.com/repos/helix-editor/helix/releases/latest | grep -oP '"browser_download_url": "\K[^"]*amd64.deb' | xargs wget
````
    - To apt install `curl`:
```sh
DEBIAN_FRONTEND=noninteractive apt-get install -y curl
```
   - To run a command which needs a variable substitution:
    
  - But we don't need to take this to an extreme and force trivial actions (e.g. loops) to the shell.
  - Prefer a single Python source file, unless it compromises readabiliy.
  - The code is not only intended to be run, but to be reference documentation on shell commands.  It should be easy to copy the shell commands and paste them into a terminal if a manual approach is preferred.
- Root structure to include these key files:
```
/root/setup/
├── resources/  # Config files to be soft linked during installation
├── setup.sh    # Bash entry point, bootstraps `uv`
├── setup.py    # Python logic (uv single-file script)
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
- Not cross architecture - unles it doesn't conflict with the POSS goal.
- No fancy logging, just fail fast with breadcrumbs. 

## Future goals

- Colourful and pretty stdout with progress bar(s)

## Open Questions

- The goal is for minimal user effort for installation, but with a readable and hackable script.  If there are other options than BASH bootsrtapping `uv` install which installs Python then these should be considered.
