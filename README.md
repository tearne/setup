# devenv

Dev environment setup for Ubuntu/Debian. Installs tools, configs, and helper scripts in one command.

## What it installs

- **Tools**: uv, Rust (via rustup), Helix editor, Zellij, htop, btop, incus
- **Language servers**: harper-ls, pyright, ruff
- **Configs**: Helix (config + languages), `.local/bin` on PATH
- **Scripts**: `tok` — encrypted secret manager (clipboard with auto-clear)

## Usage

```sh
./bootstrap_inst.sh
```

This bootstraps `uv` and `curl` if missing, then runs `install.py`. Idempotent — safe to re-run.

If `uv` is already installed:

```sh
./install.py
```