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
- Use Python 3.12 and whatever dependencies aid readability

## Configuration

Initially, there's no configuration. Everything is hard coded in the source code. The script should have a single, obvious place near the top where each tool's install is called directly — e.g. `install_zellij()`. To skip a tool, the user comments out that line.

## Functional Requirements

- Installation commands should be clearly displayed while the command runs (not pushed off top of terminal).
- Idempotency - if a tool installed, skip it, if a config exists do nothing, bu warn and summarise at the end of the run.
- Minimal interaction once started - user starts it and goes to get coffee.
- Error handling - fail fast, with breadcrumbs indicating on how far it got.
- Prompts for user password once at start if required.
- Wherever possible, the tool will install its own dependencies at runtime (e.g. `uv`, `curl`).
- When installing assets, copy from a relative rather than an absolute path.

### Third-party tools to install
All latest stable versions
- `uv` (via `curl`) - bootstrapped via outer BASH script or manually by user.
- Rust and Cargo with rust analyzer (via RustUp (via `curl`))
- Helix editor (download latest stable deb from GitHub).
 - `harper-ls`
- Zellij (via `cargo binstall`)
- `htop`, `btop` and `incus` (installed non-interactively via apt repos - no PPA)
- Incus initialisation (`incus admin init`) with ZFS storage backend.  Falls back to `dir` backend when running inside a container (ZFS kernel modules unavailable).

### Scripts / Aliases to Install
- `tok` (see `resources`) to be installed in `.local/bin`

### Configuration to Set Up

#### General Requirements
- When installing a config, soft link it from the resources folder. Perform the linking operation using a relative path so it doesn't matter where the project has been checked out.
- If config file exists, don't overwrite it. Perform a diff to determine if there is a non-whitespace difference between the existing and installable config and then:
  - Warn the user if the installable config is different and they can delete the current config and rerun if they want to overwrite.
  - Record the warning so all warnings can be summarised at the end
  - When displaying config warnings at the end of the run, show a diff

#### Specific Requirements
- Ensure that `.local/bin/` is on the users path.
- Helix config (via soft link to a local resources directory if possible):
     ```
     theme = "autumn"

     [editor]
     true-color = true
     line-number = "relative"
     bufferline = "always"
     rulers = [80]
     ```
  - Configure `harper-ls` to use a British English dictionary

## Non-Functional Requirements

- Use the POS style.
- Root structure to include these key files:
```
<project root>/
├── resources/  # Config files to be soft linked during installation
├── setup.sh    # Bash entry point, bootstraps `uv`
├── setup.py    # Python logic (uv single-file script)
├── test.sh     # Incus test harness
```


## Testing

- Testing where possible without compromising the simplicity of the code.
- Testing can be undertaken within an `incus` container where relevant.
- Use the latest LTS Ubuntu for testing.

### Test Scenarios

- Test existing configs are not overwritten. Warn that they will not be overwritten and move on.
- Check that new terminals get `.local/bin` on their path.
- Test the overall installation process completes without error

### Logging / Output

- No logging to file, only stdout/stderr
- Use a structured/hierarchical log output format, which reveals which stage/sub-stage we're at, as well as output from any processes being run.

## Non-Goals

- No flags and config files at this stage, as prefer to simply edit the code.
